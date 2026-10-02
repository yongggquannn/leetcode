"""
Flaky API Retries + Catalogue Suggestions (Sierra)
Reported as a Sierra SWE technical screen on CoderPad. The exercises cover
retrying an unreliable product API and resolving product suggestion chains.
Source: https://gaijineer.co/sierra-software-engineer-agent-interview-experience

Suggested time: 45 min.    Run: python sierra/run.py 1

================================================================================
GIVEN (do not edit): TransientError, PermanentError, ProductNotFound,
RetryExhaustedError
================================================================================

================================================================================
PART 1: Retry with exponential backoff
================================================================================

call_with_retry(fn, *, max_attempts=4, base_delay=0.1, max_delay=1.0, sleep=time.sleep)

- Call fn() (no args). Return its result on success.
- On TransientError, sleep, then retry.
  Delay before retry n (n = 1, 2, ...) = min(max_delay, base_delay * 2 ** (n - 1)).
- Never sleep after the final failed attempt.
- After max_attempts transient failures, raise RetryExhaustedError(attempts)
  chained to the last error (`raise ... from last_err`).

Example: fn fails twice then returns 42, base_delay=0.1
    -> sleeps [0.1, 0.2], returns 42

================================================================================
PART 2: Resolve product suggestions
================================================================================

resolve_catalog(products) -> list[dict]

- Each product has an `id`, a unique `sku`, and an `inStock` boolean.
- `fallbackSku`, when present, names another product's SKU.
- Add `relatedItems` to each returned product: IDs of every product reached by
  following its fallbackSku chain, in order. Do not include the starting
  product if a cycle leads back to it.
- Stop safely on missing SKUs and circular references.
- Return only products whose `inStock` value is true. Out-of-stock products
  can still be followed as links while resolving another product's chain.
- Products without a fallback get `relatedItems: []`.

================================================================================
FOLLOW-UPS (answer out loud / in the video)
================================================================================

- Add jitter: why (thundering herd)? How do you keep tests deterministic?
- 10k listings: bounded concurrency, 429 + Retry-After, overall deadline.
- API fully down: circuit breaker instead of retrying every call.
- Is retrying safe here? What changes for a non-idempotent POST?
- What would you log / measure (attempts, exhaustions, latency per id)?

================================================================================
EXAMPLE REFERENCE
================================================================================

Part 1 - retries (max_attempts=4, base_delay=0.1)

    fn:      error, error, 42      -> result 42; sleeps [0.1, 0.2]
    fn:      error on all calls    -> RetryExhaustedError; sleeps [0.1, 0.2, 0.4]
    fn:      PermanentError         -> raised immediately; no sleep

Part 2 - related items and cycles

    Input:
        {"id": 1, "sku": "A", "fallbackSku": "B", "inStock": True}
        {"id": 2, "sku": "B", "fallbackSku": "C", "inStock": True}
        {"id": 3, "sku": "C", "inStock": False}
        {"id": 4, "sku": "D", "fallbackSku": "E", "inStock": True}
        {"id": 5, "sku": "E", "fallbackSku": "D", "inStock": True}

    Returned products:
        {"id": 1, "sku": "A", "fallbackSku": "B", "inStock": True,
         "relatedItems": [2, 3]}
        {"id": 2, "sku": "B", "fallbackSku": "C", "inStock": True,
         "relatedItems": [3]}
        {"id": 4, "sku": "D", "fallbackSku": "E", "inStock": True,
         "relatedItems": [5]}
        {"id": 5, "sku": "E", "fallbackSku": "D", "inStock": True,
         "relatedItems": [4]}

    Product 3 is excluded from the returned catalog because it is out of
    stock. D -> E -> D is a cycle; traversal stops before revisiting the
    starting product. A product with no fallback gets relatedItems=[].
"""
from __future__ import annotations

import copy
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Callable
import random


# ---------------------------------------------------------------- GIVEN
class TransientError(Exception):
    """Retryable: timeouts, 503s."""


class PermanentError(Exception):
    """Not retryable: 400s."""


class ProductNotFound(PermanentError):
    """404 for a product id."""


class RetryExhaustedError(Exception):
    def __init__(self, attempts: int):
        super().__init__(f"gave up after {attempts} attempts")
        self.attempts = attempts


@dataclass
class ResolveResult:
    products: list[dict] = field(default_factory=list)
    unresolved: list[str] = field(default_factory=list)


class FakeProductAPI:
    """`flaky` maps product id -> number of TransientErrors before it succeeds."""

    def __init__(self, listings, products, flaky=None, list_failures=0):
        self._listings = listings
        self._products = products
        self._failures_left = dict(flaky or {})
        self._list_failures_left = list_failures
        self.calls: Counter[str] = Counter()

    def list_products(self) -> list[dict]:
        self.calls["list_products"] += 1
        if self._list_failures_left > 0:
            self._list_failures_left -= 1
            raise TransientError("503 from /products")
        return copy.deepcopy(self._listings)

    def get_product(self, pid: str) -> dict:
        self.calls[pid] += 1
        if self._failures_left.get(pid, 0) > 0:
            self._failures_left[pid] -= 1
            raise TransientError(f"timeout fetching {pid}")
        if pid not in self._products:
            raise ProductNotFound(pid)
        return dict(self._products[pid])


# ---------------------------------------------------------------- YOUR CODE
def call_with_retry(
    fn: Callable[[], Any],
    *,
    max_attempts: int = 4,
    base_delay: float = 0.1,
    max_delay: float = 1.0,
) -> Any:
    # Check for curr num of attempts
    if max_attempts < 1:
        raise ValueError('Attempts cannot be zero')

    for attempt in range(1, max_attempts + 1):
        # Call the function
        try:
            return fn()
        # Handle timeout errors
        except TransientError:
            if attempt < max_attempts:
                # Start off with base delay and constantly * 2
                exponential_delay = base_delay * (2 ** (attempt - 1)) 
                delay_cap = min(max_delay, exponential_delay)
                delay = random.uniform(0, delay_cap)
                time.sleep(delay)

    # Reach max attempts, raise retry exhausted error
    raise RetryExhaustedError(max_attempts)


def resolve_catalog(products: list[dict]) -> list[dict]:
    # """Add fallback-chain product IDs and omit out-of-stock products."""
    # sku_to_product = {
    #     product['sku']: product for product in products
    # }

    # res = []

    # def dfs(curr_sku, visited):
    #     if curr_sku is None or curr_sku in visited:
    #         return []

    #     curr_product = sku_to_product[curr_sku]
    #     if curr_product is None:
    #         return []
    #     visited.add(curr_sku)

    #     product_id = product['id']
    #     next_sku = product['fallbackSku']
    #     next_related_ids = dfs(next_sku, visited)
    #     return [product_id, *next_related_ids]

    # for product in products:
    #     if product['inStock'] == True:
    #         initial_sku = product['sku'] #A
    #         first_fallback_sku = product['fallbackSku'] #B
    
    #         visited = set({initial_sku})
    #         related_item_ids = dfs(first_fallback_sku, visited)
            
    #         resolved_product = {
    #             **product,
    #             'relatedItems': related_item_ids,
    #         }
    #         res.append(resolved_product)

    # return res


"""
Part 1:
- Exponential backoff with jitter

Part 2:
    products = [
        {"id": 1, "sku": "A",
        "fallbackSku": "B", "inStock":
        True},
        {"id": 2, "sku": "B",
        "fallbackSku": "C", "inStock":
        True},
        {"id": 3, "sku": "C", "inStock":
        True},
        {"id": 4, "sku": "D",
        "fallbackSku": "E", "inStock":
        True},
        {"id": 5, "sku": "E",
        "fallbackSku": "D", "inStock":
        True},
        {"id": 6, "sku": "F",
        "fallbackSku": "C", "inStock":
        False},
    ]

    Output: 
    [
          {
              "id": 1, "sku": "A",
              "fallbackSku": "B", "inStock":
              True,
              "relatedItems": [2, 3],
          },
          {
              "id": 2, "sku": "B",
              "fallbackSku": "C", "inStock":
              True,
              "relatedItems": [3],
          },
          {
              "id": 3, "sku": "C",
              "inStock": True,
              "relatedItems": [],
          },
          {
              "id": 4, "sku": "D",
              "fallbackSku": "E", "inStock":
              True,
              "relatedItems": [5],
          },
          {
              "id": 5, "sku": "E",
              "fallbackSku": "D", "inStock":
              True,
              "relatedItems": [4],
          },
      ]

"""
