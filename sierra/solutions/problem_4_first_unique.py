"""Reference solution - problem 4."""
from __future__ import annotations

import heapq
from collections import Counter, OrderedDict
from typing import Hashable


def first_unique_index(s: str) -> int:
    counts = Counter(s)
    return next((i for i, ch in enumerate(s) if counts[ch] == 1), -1)


class FirstUniqueTracker:
    def __init__(self) -> None:
        self._uniques: OrderedDict[Hashable, None] = OrderedDict()
        self._seen: set[Hashable] = set()

    def add(self, item: Hashable) -> None:
        if item in self._seen:
            self._uniques.pop(item, None)
        else:
            self._seen.add(item)
            self._uniques[item] = None

    def first_unique(self) -> Hashable | None:
        return next(iter(self._uniques), None)


def first_unique_per_window(items: list, k: int) -> list:
    if k <= 0:
        raise ValueError("k must be positive")
    counts: Counter = Counter()
    last: dict = {}
    heap: list[int] = []  # candidate positions; validated lazily
    out = []
    for i, item in enumerate(items):
        counts[item] += 1
        last[item] = i
        if counts[item] == 1:
            heapq.heappush(heap, i)
        start = i - k + 1
        if start > 0:
            gone = items[start - 1]
            counts[gone] -= 1
            if counts[gone] == 1:
                heapq.heappush(heap, last[gone])  # its only copy left is the latest one
        if start >= 0:
            while heap and not (heap[0] >= start and counts[items[heap[0]]] == 1 and last[items[heap[0]]] == heap[0]):
                heapq.heappop(heap)
            out.append(items[heap[0]] if heap else None)
    return out
