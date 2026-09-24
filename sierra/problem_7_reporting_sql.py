"""
Reporting Queries with CTEs (Sierra)
Reported: "Simplify Reporting Queries with CTEs" on a recent Sierra SWE screen.
Source: https://www.glassdoor.com/Interview/Sierra-Interview-Questions-E10032095.htm

Uses stdlib sqlite3 (window functions need SQLite >= 3.25 - any modern Python).
Suggested time: 40 min.    Run: python sierra/run.py 7

Schema (support conversations handled by AI agents for brand customers):

    customers(id, name, plan)                         plan: 'enterprise' | 'growth'
    conversations(id, customer_id, channel, started_at, resolved, escalated)
        channel: 'chat' | 'voice' | 'email'; started_at: 'YYYY-MM-DD';
        resolved / escalated: 0 or 1
    csat(conversation_id, score)                      score 1-5; not every conversation has one

Fill in the query strings at the bottom. Try each in a REPL with:
    conn = connect(); print(run(conn, YOUR_QUERY))

================================================================================
PART 1: Refactor LEGACY_QUERY into REFACTORED_QUERY using CTEs
================================================================================

Same rows, same order, but: start with WITH, compute each per-customer metric
once, no correlated subqueries. Be ready to explain why it's easier to review.

================================================================================
PART 2: CHANNEL_WEEKLY_QUERY
================================================================================

Per channel per week: channel, week, conversations, escalation_rate
- week = strftime('%Y-%W', started_at)     (e.g. '2026-01')
- escalation_rate = ROUND(share of conversations escalated, 2)
- ORDER BY channel, week

================================================================================
PART 3: TOP_ESCALATED_QUERY
================================================================================

For each plan, the single customer with the most escalated conversations:
plan, name, escalations. Ties -> alphabetically first name. Skip customers with
zero escalations. ORDER BY plan. Use a window function (ROW_NUMBER / RANK).

================================================================================
PART 4: DATE_RANGE_QUERY (parameterised)
================================================================================

Conversation count per customer between two dates, inclusive, passed as
parameters: run(conn, DATE_RANGE_QUERY, ("2026-01-12", "2026-01-18")).
Columns: name, conversations. Only customers with >= 1 conversation in range.
ORDER BY conversations DESC, name. Use `?` placeholders, never string
formatting (why? say it out loud).

================================================================================
FOLLOW-UPS
================================================================================

- CTE vs subquery vs temp table vs view: readability and performance.
- Which indexes help these queries? (conversations(customer_id), (started_at))
- NULL csat scores: how does AVG treat them? What would you show the user?
- Materialising daily rollups instead of querying raw rows at scale.
"""
from __future__ import annotations

import sqlite3

SCHEMA = """
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT NOT NULL, plan TEXT NOT NULL);
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    channel TEXT NOT NULL,
    started_at TEXT NOT NULL,
    resolved INTEGER NOT NULL,
    escalated INTEGER NOT NULL
);
CREATE TABLE csat (conversation_id INTEGER PRIMARY KEY REFERENCES conversations(id), score INTEGER NOT NULL);
"""

SEED = """
INSERT INTO customers VALUES
    (1, 'Acme Outdoors', 'enterprise'), (2, 'Birch Telecom', 'enterprise'),
    (3, 'Cobalt Bank', 'growth'), (4, 'Dune Streaming', 'growth'), (5, 'Elm Grocers', 'growth');
INSERT INTO conversations VALUES
    (1, 1, 'chat', '2026-01-05', 1, 0), (2, 1, 'chat', '2026-01-06', 1, 0),
    (3, 1, 'voice', '2026-01-07', 0, 1), (4, 1, 'email', '2026-01-13', 1, 0),
    (5, 2, 'voice', '2026-01-05', 0, 1), (6, 2, 'voice', '2026-01-08', 1, 0),
    (7, 2, 'chat', '2026-01-14', 0, 1), (8, 2, 'chat', '2026-01-15', 0, 1),
    (9, 3, 'chat', '2026-01-06', 1, 0), (10, 3, 'chat', '2026-01-12', 1, 0),
    (11, 3, 'voice', '2026-01-13', 1, 0), (12, 4, 'email', '2026-01-07', 0, 1),
    (13, 4, 'chat', '2026-01-09', 1, 0), (14, 4, 'voice', '2026-01-16', 0, 0),
    (15, 5, 'chat', '2026-01-08', 1, 0), (16, 5, 'chat', '2026-01-14', 0, 1);
INSERT INTO csat VALUES
    (1, 5), (2, 4), (3, 2), (4, 5), (5, 1), (6, 4),
    (9, 5), (10, 4), (11, 5), (12, 2), (13, 4), (15, 5);
"""


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA + SEED)
    return conn


def run(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[tuple]:
    return conn.execute(sql, params).fetchall()


LEGACY_QUERY = """
SELECT c.name, c.plan,
       (SELECT COUNT(*) FROM conversations v WHERE v.customer_id = c.id) AS conversations,
       ROUND((SELECT AVG(CASE WHEN v.resolved = 1 AND v.escalated = 0 THEN 1.0 ELSE 0 END)
              FROM conversations v WHERE v.customer_id = c.id), 2) AS resolution_rate,
       ROUND((SELECT AVG(s.score) FROM csat s
              WHERE s.conversation_id IN (SELECT v.id FROM conversations v WHERE v.customer_id = c.id)), 2) AS avg_csat
FROM customers c
WHERE (SELECT COUNT(*) FROM conversations v WHERE v.customer_id = c.id) >= 3
ORDER BY resolution_rate DESC, c.name
"""

# ---------------------------------------------------------------- YOUR CODE
REFACTORED_QUERY = ""
CHANNEL_WEEKLY_QUERY = ""
TOP_ESCALATED_QUERY = ""
DATE_RANGE_QUERY = ""
