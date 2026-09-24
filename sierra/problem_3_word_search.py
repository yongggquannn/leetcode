"""
Word Search (Sierra)
Reported: "Given an m x n grid of characters board and a string word, return
true if word exists in the grid" (LeetCode 79), with the usual follow-ups.
Source: https://www.tryexponent.com/questions?company=sierra-ai&role=swe

Suggested time: 40 min.    Run: python sierra/run.py 3

================================================================================
PART 1: exists(board, word) -> bool
================================================================================

The word is built from sequentially adjacent cells (up/down/left/right). A cell
may be used at most once per word. Empty word -> True. Empty board -> False
(unless word is empty).

    board = [["A","B","C","E"],
             ["S","F","C","S"],
             ["A","D","E","E"]]
    exists(board, "ABCCED") -> True
    exists(board, "SEE")    -> True
    exists(board, "ABCB")   -> False   (B reused)

================================================================================
PART 2: find_path(board, word) -> list[tuple[int, int]] | None
================================================================================

Return the (row, col) of each letter of one valid placement, or None. Any valid
path is accepted.

================================================================================
PART 3: find_words(board, words) -> set[str]
================================================================================

Return every word in `words` that exists in the board (LeetCode 212). Don't run
Part 1 once per word: share work across words with common prefixes (trie).

================================================================================
PART 4: Diagonals
================================================================================

Add a keyword argument `diagonal=False` to all three functions. When True, the
8 neighbours count as adjacent. Keep one neighbour definition, not three copies.

================================================================================
FOLLOW-UPS
================================================================================

- Time/space complexity of Parts 1 and 3?
- Pruning: letter-frequency check before searching; searching from the rarer end.
- Board of all "a" and word "aaaa...ab": why is this the worst case?
- Recursion depth limits in Python: when would you go iterative?
"""
from __future__ import annotations

Board = list[list[str]]


def exists(board: Board, word: str, *, diagonal: bool = False) -> bool:
    raise NotImplementedError


def find_path(board: Board, word: str, *, diagonal: bool = False) -> list[tuple[int, int]] | None:
    raise NotImplementedError


def find_words(board: Board, words: list[str], *, diagonal: bool = False) -> set[str]:
    raise NotImplementedError
