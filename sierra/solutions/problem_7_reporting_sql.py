"""Reference solution - problem 7."""
from problem_7_reporting_sql import LEGACY_QUERY, connect, run  # noqa: F401 - re-exported for tests

REFACTORED_QUERY = """
WITH per_customer AS (
    SELECT customer_id,
           COUNT(*) AS conversations,
           AVG(CASE WHEN resolved = 1 AND escalated = 0 THEN 1.0 ELSE 0 END) AS resolution_rate
    FROM conversations
    GROUP BY customer_id
),
customer_csat AS (
    SELECT v.customer_id, AVG(s.score) AS avg_csat
    FROM csat s
    JOIN conversations v ON v.id = s.conversation_id
    GROUP BY v.customer_id
)
SELECT c.name, c.plan, p.conversations,
       ROUND(p.resolution_rate, 2) AS resolution_rate,
       ROUND(cs.avg_csat, 2) AS avg_csat
FROM customers c
JOIN per_customer p ON p.customer_id = c.id
LEFT JOIN customer_csat cs ON cs.customer_id = c.id
WHERE p.conversations >= 3
ORDER BY resolution_rate DESC, c.name
"""

CHANNEL_WEEKLY_QUERY = """
WITH tagged AS (
    SELECT channel, strftime('%Y-%W', started_at) AS week, escalated
    FROM conversations
)
SELECT channel, week, COUNT(*) AS conversations, ROUND(AVG(escalated * 1.0), 2) AS escalation_rate
FROM tagged
GROUP BY channel, week
ORDER BY channel, week
"""

TOP_ESCALATED_QUERY = """
WITH escalations AS (
    SELECT c.plan, c.name, SUM(v.escalated) AS escalations
    FROM customers c
    JOIN conversations v ON v.customer_id = c.id
    GROUP BY c.id
    HAVING SUM(v.escalated) > 0
),
ranked AS (
    SELECT plan, name, escalations,
           ROW_NUMBER() OVER (PARTITION BY plan ORDER BY escalations DESC, name) AS rn
    FROM escalations
)
SELECT plan, name, escalations FROM ranked WHERE rn = 1 ORDER BY plan
"""

DATE_RANGE_QUERY = """
SELECT c.name, COUNT(*) AS conversations
FROM conversations v
JOIN customers c ON c.id = v.customer_id
WHERE v.started_at BETWEEN ? AND ?
GROUP BY c.id
ORDER BY conversations DESC, c.name
"""
