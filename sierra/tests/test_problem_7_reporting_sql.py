import re

from _harness import load

m = load("problem_7_reporting_sql")


def _query(name):
    sql = getattr(m, name)
    if not sql.strip():
        raise NotImplementedError
    return sql


# ---- Part 1
def test_part1_refactor_matches_legacy():
    sql = _query("REFACTORED_QUERY")
    conn = m.connect()
    expected = [
        ("Cobalt Bank", "growth", 3, 1.0, 4.67),
        ("Acme Outdoors", "enterprise", 4, 0.75, 4.0),
        ("Dune Streaming", "growth", 3, 0.33, 3.0),
        ("Birch Telecom", "enterprise", 4, 0.25, 2.5),
    ]
    assert m.run(conn, m.LEGACY_QUERY) == expected, "legacy query changed?"
    assert m.run(conn, sql) == expected, m.run(conn, sql)


def test_part1_uses_ctes():
    sql = _query("REFACTORED_QUERY")
    assert sql.strip().upper().startswith("WITH"), "start with a CTE"
    assert "IN (SELECT" not in re.sub(r"\s+", " ", sql.upper()), "no nested IN (SELECT ...)"


# ---- Part 2
def test_part2_channel_weekly():
    rows = m.run(m.connect(), _query("CHANNEL_WEEKLY_QUERY"))
    assert rows == [
        ("chat", "2026-01", 5, 0.0),
        ("chat", "2026-02", 4, 0.75),
        ("email", "2026-01", 1, 1.0),
        ("email", "2026-02", 1, 0.0),
        ("voice", "2026-01", 3, 0.67),
        ("voice", "2026-02", 2, 0.0),
    ], rows


# ---- Part 3
def test_part3_top_escalated_per_plan():
    sql = _query("TOP_ESCALATED_QUERY")
    rows = m.run(m.connect(), sql)
    assert rows == [("enterprise", "Birch Telecom", 3), ("growth", "Dune Streaming", 1)], rows
    assert " OVER" in sql.upper(), "use a window function"


# ---- Part 4
def test_part4_parameterised_range():
    sql = _query("DATE_RANGE_QUERY")
    assert "?" in sql and "2026" not in sql, "dates must be parameters"
    conn = m.connect()
    assert m.run(conn, sql, ("2026-01-12", "2026-01-18")) == [
        ("Birch Telecom", 2),
        ("Cobalt Bank", 2),
        ("Acme Outdoors", 1),
        ("Dune Streaming", 1),
        ("Elm Grocers", 1),
    ]
    assert m.run(conn, sql, ("2026-01-05", "2026-01-05")) == [("Acme Outdoors", 1), ("Birch Telecom", 1)]
    assert m.run(conn, sql, ("2030-01-01", "2030-12-31")) == []
