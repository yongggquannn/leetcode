"""
First Unique Character / Item (Sierra)
Reported: "First Unique Character Index" (LeetCode 387) on a recent Sierra SWE
screen, plus the natural streaming follow-ups.
Source: https://www.glassdoor.com/Interview/Sierra-Interview-Questions-E10032095.htm

Suggested time: 35 min.    Run: python sierra/run.py 4

================================================================================
PART 1: first_unique_index(s: str) -> int
================================================================================

Index of the first character that appears exactly once, or -1.

    "leetcode"     -> 0
    "loveleetcode" -> 2
    "aabb"         -> -1

================================================================================
PART 2: FirstUniqueTracker (streaming)
================================================================================

Messages arrive one at a time (think: user ids hitting an agent). Support:

    add(item)       -> None     amortised O(1)
    first_unique()  -> item | None   O(1)

Items are any hashable value, not just characters.

    t = FirstUniqueTracker()
    t.add("u1"); t.add("u2"); t.first_unique() -> "u1"
    t.add("u1");              t.first_unique() -> "u2"
    t.add("u2");              t.first_unique() -> None

================================================================================
PART 3: Sliding window
================================================================================

first_unique_per_window(items: list, k: int) -> list

For each window items[i-k+1 .. i] (i from k-1 to len-1), the first item (by
position) occurring exactly once in that window, or None. Target: O(n log n)
or better. k <= 0 -> ValueError.

    first_unique_per_window(["a","b","a","c","b"], 3)
      windows [a b a] [b a c] [a c b]
      -> ["b", "b", "a"]

Watch out: an item that was duplicated can become unique again when the older
copy slides out of the window.

================================================================================
FOLLOW-UPS
================================================================================

- Part 1 for a Unicode string vs lowercase ASCII: array vs dict?
- Part 2 memory grows forever - what would you bound in production?
- Part 2 across many servers: what would you shard on?
"""
from __future__ import annotations

from typing import Hashable


def first_unique_index(s: str) -> int:
    raise NotImplementedError


class FirstUniqueTracker:
    def add(self, item: Hashable) -> None:
        raise NotImplementedError

    def first_unique(self) -> Hashable | None:
        raise NotImplementedError


def first_unique_per_window(items: list, k: int) -> list:
    raise NotImplementedError
