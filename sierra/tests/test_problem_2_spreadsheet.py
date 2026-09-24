from _harness import load

m = load("problem_2_spreadsheet")


def _raises(exc_type, fn):
    try:
        fn()
    except exc_type as err:
        return err
    raise AssertionError(f"expected {exc_type.__name__}")


# ---- Part 1
def test_part1_literals_and_formulas():
    s = m.Sheet()
    s.set("A1", "5")
    s.set("B1", "=A1+10")
    assert s.get("B1") == 15
    s.set("A1", "7")
    assert s.get("B1") == 17
    assert s.get("Z99") == 0


def test_part1_chain_unset_and_case():
    s = m.Sheet()
    s.set("c1", "= b1 + a1 + 1")
    assert s.get("C1") == 1, "unset cells are 0"
    s.set("A1", "-3")
    s.set("B1", "=A1+A1")
    assert s.get("c1") == -8
    s.set("A1", "")
    assert s.get("C1") == 1, "cleared cell is 0"


def test_part1_malformed_input_leaves_sheet_unchanged():
    s = m.Sheet()
    s.set("A1", "4")
    for bad in ["=A1+", "=hello", "abc", "=+"]:
        _raises(m.FormulaError, lambda: s.set("A1", bad))
    assert s.get("A1") == 4


# ---- Part 2
def test_part2_self_reference():
    s = m.Sheet()
    err = _raises(m.CircularReferenceError, lambda: s.set("A1", "=A1+1"))
    assert err.cycle == ["A1", "A1"], err.cycle


def test_part2_cycle_path_and_rollback():
    s = m.Sheet()
    s.set("A1", "=B1")
    s.set("B1", "=C1")
    s.set("C1", "5")
    err = _raises(m.CircularReferenceError, lambda: s.set("C1", "=A1"))
    assert err.cycle == ["C1", "A1", "B1", "C1"], err.cycle
    assert s.get("A1") == 5 and s.get("C1") == 5, "sheet must be unchanged after a rejected set"
    s.set("C1", "9")
    assert s.get("A1") == 9, "dependency graph corrupted by the rejected set"


def test_part2_non_cycle_diamond_allowed():
    s = m.Sheet()
    s.set("A1", "1")
    s.set("B1", "=A1")
    s.set("C1", "=A1")
    s.set("D1", "=B1+C1")
    assert s.get("D1") == 2


# ---- Part 3
def test_part3_only_dependents_recomputed():
    s = m.Sheet()
    s.set("A1", "1")
    s.set("B1", "=A1+1")
    s.set("C1", "=B1+1")
    s.set("X1", "100")
    s.set("Y1", "=X1+1")
    before = s.evaluations
    s.set("A1", "10")
    assert s.evaluations - before == 3, f"expected A1,B1,C1 only; got {s.evaluations - before}"
    assert s.get("C1") == 12 and s.get("Y1") == 101


def test_part3_diamond_evaluated_once():
    s = m.Sheet()
    s.set("A1", "1")
    s.set("B1", "=A1+1")
    s.set("C1", "=A1+2")
    s.set("D1", "=B1+C1")
    before = s.evaluations
    s.set("A1", "5")
    assert s.evaluations - before == 4, f"D1 must be evaluated once; got {s.evaluations - before} evaluations"
    assert s.get("D1") == 13


def test_part3_get_does_not_evaluate():
    s = m.Sheet()
    s.set("A1", "1")
    s.set("B1", "=A1")
    before = s.evaluations
    for _ in range(10):
        s.get("B1")
    assert s.evaluations == before, "get() must read a cached value"


def test_part3_rewiring_drops_old_dependency():
    s = m.Sheet()
    s.set("A1", "1")
    s.set("B1", "=A1")
    s.set("B1", "7")
    before = s.evaluations
    s.set("A1", "2")
    assert s.evaluations - before == 1, "B1 no longer depends on A1"


# ---- Part 4
def test_part4_subtraction_and_leading_sign():
    s = m.Sheet()
    s.set("A1", "10")
    s.set("B1", "4")
    s.set("C1", "=A1-B1+3")
    s.set("D1", "=-A1")
    assert s.get("C1") == 9 and s.get("D1") == -10


def test_part4_sum_range():
    s = m.Sheet()
    for i, cell in enumerate(["A1", "A2", "A3", "B1", "B2", "B3"], start=1):
        s.set(cell, str(i))
    s.set("C1", "=SUM(A1:B3)")
    s.set("C2", "=SUM(A1:A3)-B1+2")
    assert s.get("C1") == 21
    assert s.get("C2") == 4
    s.set("B2", "100")
    assert s.get("C1") == 116, "every cell in a range is a dependency"


def test_part4_range_cycle_detected():
    s = m.Sheet()
    s.set("A1", "1")
    _raises(m.CircularReferenceError, lambda: s.set("A2", "=SUM(A1:A3)"))
