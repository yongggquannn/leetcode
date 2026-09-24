"""
Flaky API + Product Resolution (Sierra)
Reported: Sierra SWE technical screen on CoderPad - "call an API endpoint that
fails occasionally but eventually succeeds ... the response contains a product
list with fallback IDs ... resolve each product's eventual set of IDs into the
product objects."
Source: https://gaijineer.co/sierra-software-engineer-agent-interview-experience

Suggested time: 45 min.    Run: python sierra/run.py 1

================================================================================
GIVEN (do not edit): TransientError, PermanentError, ProductNotFound,
RetryExhaustedError, ResolveResult, FakeProductAPI
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
PART 2: Don't retry what can't succeed
================================================================================

- PermanentError (including ProductNotFound) propagates immediately: no sleep.
- Any other exception (a bug, e.g. KeyError) also propagates immediately.
- max_attempts < 1 -> ValueError.

================================================================================
PART 3: Resolve the catalog
================================================================================

api.list_products() -> [{"id": "p1", "fallback_ids": ["p9", "p3"]}, ...]
api.get_product(pid) -> {"id": ..., "name": ..., "price_cents": ...}
Both may raise TransientError; get_product may raise ProductNotFound.

resolve_catalog(api, *, sleep=time.sleep) -> ResolveResult

- Wrap every API call in call_with_retry (pass `sleep` through).
- For each listing, try its id, then its fallback_ids in order. The first
  product found resolves the listing.
- A candidate whose retries are exhausted counts as "not found" - move to the
  next fallback. One bad product must not fail the whole catalog.
- Listings where nothing resolves go in ResolveResult.unresolved (listing ids).
- Both lists keep catalog order. If list_products itself is exhausted, raise.

================================================================================
PART 4: Redirects + caching
================================================================================

get_product may now return {"id": "p1", "moved_to": "p7"} instead of a product.

- Follow moved_to until a real product is reached.
- A redirect cycle (p1 -> p7 -> p1) makes that candidate unresolvable; move on
  to the next fallback.
- Fetch each product id from the API at most once per resolve_catalog call
  (listings share fallbacks). Remember misses too.

================================================================================
FOLLOW-UPS (answer out loud / in the video)
================================================================================

- Add jitter: why (thundering herd)? How do you keep tests deterministic?
- 10k listings: bounded concurrency, 429 + Retry-After, overall deadline.
- API fully down: circuit breaker instead of retrying every call.
- Is retrying safe here? What changes for a non-idempotent POST?
- What would you log / measure (attempts, exhaustions, latency per id)?
"""
from __future__ import annotations

import copy
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Callable


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
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    raise NotImplementedError


def resolve_catalog(api: FakeProductAPI, *, sleep: Callable[[float], None] = time.sleep) -> ResolveResult:
    raise NotImplementedError
