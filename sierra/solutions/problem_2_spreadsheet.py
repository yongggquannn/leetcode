"""Reference solution - problem 2."""
from __future__ import annotations

import re
from collections import defaultdict, deque

from problem_2_spreadsheet import CircularReferenceError, FormulaError

CELL_RE = re.compile(r"^([A-Z]+)(\d+)$")
TERM_RE = re.compile(r"([+-]?)(?:SUM\(([A-Z]+\d+):([A-Z]+\d+)\)|([A-Z]+\d+)|(\d+))")

# A term is (sign, cells) or (sign, int literal).
Term = tuple[int, "list[str] | int"]


def _col_to_num(col: str) -> int:
    n = 0
    for ch in col:
        n = n * 26 + ord(ch) - ord("A") + 1
    return n


def _num_to_col(n: int) -> str:
    out = ""
    while n:
        n, rem = divmod(n - 1, 26)
        out = chr(ord("A") + rem) + out
    return out


def _normalize(cell: str) -> str:
    cell = cell.strip().upper()
    if not CELL_RE.match(cell):
        raise FormulaError(f"bad cell name {cell!r}")
    return cell


def _expand(start: str, end: str) -> list[str]:
    (c1, r1), (c2, r2) = CELL_RE.match(start).groups(), CELL_RE.match(end).groups()
    cols = sorted((_col_to_num(c1), _col_to_num(c2)))
    rows = sorted((int(r1), int(r2)))
    return [f"{_num_to_col(c)}{r}" for c in range(cols[0], cols[1] + 1) for r in range(rows[0], rows[1] + 1)]


def _parse(raw: str) -> list[Term]:
    raw = raw.strip()
    if not raw:
        return []
    if not raw.startswith("="):
        try:
            return [(1, int(raw))]
        except ValueError:
            raise FormulaError(f"not a number or formula: {raw!r}") from None
    body = raw[1:].replace(" ", "").upper()
    terms: list[Term] = []
    pos = 0
    while pos < len(body):
        m = TERM_RE.match(body, pos)
        if not m or (terms and not m.group(1)):
            raise FormulaError(f"cannot parse {raw!r} at position {pos + 1}")
        sign = -1 if m.group(1) == "-" else 1
        if m.group(2):
            terms.append((sign, _expand(m.group(2), m.group(3))))
        elif m.group(4):
            terms.append((sign, [m.group(4)]))
        else:
            terms.append((sign, int(m.group(5))))
        pos = m.end()
    if not terms:
        raise FormulaError(f"empty formula {raw!r}")
    return terms


def _refs(terms: list[Term]) -> set[str]:
    return {c for _, payload in terms if isinstance(payload, list) for c in payload}


class Sheet:
    def __init__(self) -> None:
        self.evaluations = 0
        self._terms: dict[str, list[Term]] = {}
        self._deps: dict[str, set[str]] = {}
        self._dependents: dict[str, set[str]] = defaultdict(set)
        self._values: dict[str, int] = {}

    def get(self, cell: str) -> int:
        return self._values.get(_normalize(cell), 0)

    def set(self, cell: str, raw: str) -> None:
        cell = _normalize(cell)
        terms = _parse(raw)
        refs = _refs(terms)
        cycle = self._find_cycle(cell, refs)
        if cycle:
            raise CircularReferenceError(cycle)

        for old in self._deps.get(cell, ()):
            self._dependents[old].discard(cell)
        for ref in refs:
            self._dependents[ref].add(cell)
        self._deps[cell], self._terms[cell] = refs, terms
        self._recompute_from(cell)

    def _find_cycle(self, cell: str, new_refs: set[str]) -> list[str] | None:
        seen: set[str] = set()

        def dfs(node: str, path: list[str]) -> list[str] | None:
            if node == cell:
                return path
            if node in seen:
                return None
            seen.add(node)
            for nxt in sorted(self._deps.get(node, ())):
                if found := dfs(nxt, path + [nxt]):
                    return found
            return None

        for ref in sorted(new_refs):
            if found := dfs(ref, [cell, ref]):
                return found
        return None

    def _recompute_from(self, cell: str) -> None:
        affected, queue = {cell}, deque([cell])
        while queue:
            for dep in self._dependents[queue.popleft()]:
                if dep not in affected:
                    affected.add(dep)
                    queue.append(dep)

        # Kahn's algorithm restricted to the affected subgraph.
        indegree = {c: len(self._deps.get(c, set()) & affected) for c in affected}
        ready = deque(c for c, d in indegree.items() if d == 0)
        while ready:
            current = ready.popleft()
            self._values[current] = self._evaluate(current)
            for dep in self._dependents[current]:
                if dep in affected:
                    indegree[dep] -= 1
                    if indegree[dep] == 0:
                        ready.append(dep)

    def _evaluate(self, cell: str) -> int:
        self.evaluations += 1
        total = 0
        for sign, payload in self._terms.get(cell, []):
            value = payload if isinstance(payload, int) else sum(self._values.get(c, 0) for c in payload)
            total += sign * value
        return total
