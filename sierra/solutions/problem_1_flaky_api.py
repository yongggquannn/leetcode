"""Reference solution - problem 1."""
from __future__ import annotations

import time
from typing import Any, Callable

from problem_1_flaky_api import (  # noqa: F401 - re-exported for tests
    FakeProductAPI,
    PermanentError,
    ProductNotFound,
    ResolveResult,
    RetryExhaustedError,
    TransientError,
)


def call_with_retry(
    fn: Callable[[], Any],
    *,
    max_attempts: int = 4,
    base_delay: float = 0.1,
    max_delay: float = 1.0,
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    if max_attempts < 1:
        raise ValueError("max_attempts must be >= 1")
    last_err: TransientError | None = None
    for attempt in range(1, max_attempts + 1):
        try:
            return fn()
        except TransientError as err:
            last_err = err
            if attempt < max_attempts:
                sleep(min(max_delay, base_delay * 2 ** (attempt - 1)))
    raise RetryExhaustedError(max_attempts) from last_err


def resolve_catalog(products: list[dict]) -> list[dict]:
    """Add fallback-chain product IDs and omit out-of-stock products."""
    products_by_sku = {product["sku"]: product for product in products}

    def collect_related(sku: str | None, visited: set[str]) -> list[Any]:
        if sku is None or sku in visited or sku not in products_by_sku:
            return []

        visited.add(sku)
        product = products_by_sku[sku]
        return [product["id"], *collect_related(product.get("fallbackSku"), visited)]

    resolved = []
    for product in products:
        related_items = collect_related(product.get("fallbackSku"), {product["sku"]})
        if product.get("inStock", True):
            resolved.append({**product, "relatedItems": related_items})

    return resolved
