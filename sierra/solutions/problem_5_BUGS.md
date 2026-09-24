# Problem 5 answer key

Only read this after you've tried the problem. The fixed code is in
[problem_5_agent_debug/](problem_5_agent_debug/). Each fix is marked with a `# Fix N` comment.

| # | Scenario symptom | Root cause | Fix | Prevent next time |
|---|---|---|---|---|
| 1 | Every successful tool call ends in the "passed you to a human" handoff | `agent.py` only appends tool results containing `"error"`, so the model never sees successes, re-calls the tool, and hits MAX_STEPS | Append every tool result | Test the agent loop with one happy-path tool call; alert on max_steps escalations |
| 2 | An unverified user sees the order status | Auth gate hard-codes `call.name == "issue_refund"` and ignores `Tool.requires_auth` | `if tool.requires_auth and not verified` | One central auth check driven by tool metadata; a test per tool for unauthenticated access |
| 3 | A verified user can read someone else's order | `lookup_order` uses `db.get` instead of `_owned_order` | Use the ownership helper | Enforce ownership in the data-access layer; add a cross-tenant test |
| 4 | A $150 refund is escalated as over_limit | Limit is `200` (dollars) compared with `amount_cents` | `AUTO_REFUND_LIMIT_CENTS = 200_00` | A Money type or `_cents` suffix everywhere; boundary tests at $199.99, $200, and $200.01 |
| 5 | Refund on day 30 is refused | `>=` instead of `>` against the window | `days > REFUND_WINDOW_DAYS` | Boundary tests at day 29, 30, and 31 |
| 6 | Asking twice refunds twice | `issue_refund` never checks `order.refunded` | Return `ALREADY_REFUNDED` | Idempotency key on the payment call; unique constraint in the ledger |
| 7 | Two wrong emails never escalate | Counter computed in a local (`failed = ... + 1`) and never saved | `ctx.state.failed_verifications += 1` | Test state across turns, not within a single call |

Debugging loop worth saying in the video: reproduce with the failing scenario → print
`agent.state.history` (or use the REPL, which prints tool calls) → compare with the diagram →
fix the smallest thing → re-run all scenarios.
