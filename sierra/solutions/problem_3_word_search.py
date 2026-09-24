"""Reference solution - problem 3."""
from __future__ import annotations

Board = list[list[str]]

ORTHOGONAL = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAGONAL = ORTHOGONAL + [(-1, -1), (-1, 1), (1, -1), (1, 1)]


def _neighbours(board: Board, r: int, c: int, diagonal: bool):
    for dr, dc in DIAGONAL if diagonal else ORTHOGONAL:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
            yield nr, nc


def find_path(board: Board, word: str, *, diagonal: bool = False) -> list[tuple[int, int]] | None:
    if not word:
        return []
    if not board or not board[0]:
        return None
    path: list[tuple[int, int]] = []
    used: set[tuple[int, int]] = set()

    def dfs(r: int, c: int, i: int) -> bool:
        if board[r][c] != word[i] or (r, c) in used:
            return False
        path.append((r, c))
        used.add((r, c))
        if i == len(word) - 1 or any(dfs(nr, nc, i + 1) for nr, nc in _neighbours(board, r, c, diagonal)):
            return True
        path.pop()
        used.discard((r, c))
        return False

    for r in range(len(board)):
        for c in range(len(board[0])):
            if dfs(r, c, 0):
                return path
    return None


def exists(board: Board, word: str, *, diagonal: bool = False) -> bool:
    return find_path(board, word, diagonal=diagonal) is not None


def find_words(board: Board, words: list[str], *, diagonal: bool = False) -> set[str]:
    if not board or not board[0]:
        return {w for w in words if not w}
    trie: dict = {}
    for w in words:
        node = trie
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w

    found: set[str] = {w for w in words if not w}
    used: set[tuple[int, int]] = set()

    def dfs(r: int, c: int, parent: dict) -> None:
        ch = board[r][c]
        node = parent.get(ch)
        if node is None or (r, c) in used:
            return
        if "$" in node:
            found.add(node.pop("$"))
        used.add((r, c))
        for nr, nc in _neighbours(board, r, c, diagonal):
            dfs(nr, nc, node)
        used.discard((r, c))
        if not node:
            parent.pop(ch)  # prune exhausted branches

    for r in range(len(board)):
        for c in range(len(board[0])):
            dfs(r, c, trie)
    return found
