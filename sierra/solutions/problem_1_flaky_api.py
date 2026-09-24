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


def resolve_catalog(api: FakeProductAPI, *, sleep: Callable[[float], None] = time.sleep) -> ResolveResult:
    listings = call_with_retry(api.list_products, sleep=sleep)
    cache: dict[str, dict | None] = {}

    def fetch(pid: str) -> dict | None:
        if pid not in cache:
            try:
                cache[pid] = call_with_retry(lambda: api.get_product(pid), sleep=sleep)
            except (ProductNotFound, RetryExhaustedError):
                cache[pid] = None
        return cache[pid]

    def follow(pid: str) -> dict | None:
        seen: set[str] = set()
        while pid not in seen:
            seen.add(pid)
            doc = fetch(pid)
            if doc is None or "moved_to" not in doc:
                return doc
            pid = doc["moved_to"]
        return None  # redirect cycle

    result = ResolveResult()
    for listing in listings:
        for candidate in [listing["id"], *listing.get("fallback_ids", [])]:
            product = follow(candidate)
            if product is not None:
                result.products.append(product)
                break
        else:
            result.unresolved.append(listing["id"])
    return result
