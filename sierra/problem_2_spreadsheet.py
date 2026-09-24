"""
Spreadsheet Cells + Circular References (Sierra)
Reported: "Implement a function to traverse cell dependencies in an Excel-like
spreadsheet and detect circular references between cells."
Sources: https://www.tryexponent.com/questions?company=sierra-ai&role=swe
         https://www.tryexponent.com/guides/sierra-agent-engineer-interview

Suggested time: 50 min.    Run: python sierra/run.py 2

================================================================================
PART 1: Values and formulas
================================================================================

class Sheet:
    def set(self, cell: str, raw: str) -> None
    def get(self, cell: str) -> int

- Cells are named column letters + row number: "A1", "B12", "AA3".
  Treat names case-insensitively ("a1" == "A1").
- raw is either an integer literal ("5", "-3"), a formula ("=A1+B2+7"), or ""
  (clears the cell). Part 1 formulas only use "+". Spaces are allowed.
- An unset / cleared cell evaluates to 0.
- get() always reflects the latest values of everything a cell depends on.
- Malformed input ("=A1+", "=hello", "abc") -> FormulaError; sheet unchanged.

    s = Sheet()
    s.set("A1", "5"); s.set("B1", "=A1+10")
    s.get("B1") -> 15
    s.set("A1", "7")
    s.get("B1") -> 17

================================================================================
PART 2: Circular references
================================================================================

- If set() would create a cycle (including a self-reference "=A1+1" on A1),
  raise CircularReferenceError and leave the sheet exactly as it was.
- err.cycle is the path of cells, starting and ending with the cell being set,
  following "depends on" edges:
      A1 = "=B1", B1 = "=C1", then set C1 = "=A1"
      -> err.cycle == ["C1", "A1", "B1", "C1"]

================================================================================
PART 3: Cached values, minimal recomputation
================================================================================

- get() must be O(1): store computed values, don't evaluate on read.
- On set(), re-evaluate only the changed cell and its transitive dependents,
  each exactly once, in dependency order (a diamond A1 -> B1, C1 -> D1
  evaluates D1 once, after both B1 and C1).
- Increment self.evaluations by 1 every time you evaluate a cell.

================================================================================
PART 4: More syntax
================================================================================

- Subtraction: "=A1-B1+3", and a leading sign: "=-A1".
- Ranges: "=SUM(A1:B3)" sums the rectangle A1..B3 (6 cells). Mixed:
  "=SUM(A1:A3)-B1+2". Every cell in a range is a dependency.

================================================================================
FOLLOW-UPS
================================================================================

- Complexity of set() in terms of dependents? Of cycle detection?
- 1M cells, one hot cell with 100k dependents: what changes?
- How would you add multiplication / precedence? (tokenizer -> parser -> AST)
- Undo/redo; persisting the sheet; concurrent editors.
"""
from __future__ import annotations


class FormulaError(ValueError):
    pass


class CircularReferenceError(ValueError):
    def __init__(self, cycle: list[str]):
        super().__init__(" -> ".join(cycle))
        self.cycle = cycle


class Sheet:
    def __init__(self) -> None:
        self.evaluations = 0

    def set(self, cell: str, raw: str) -> None:
        raise NotImplementedError

    def get(self, cell: str) -> int:
        raise NotImplementedError
