# Problem 5: Debug the support agent (Sierra)

This mirrors the reported Sierra CoderPad round: *"a small codebase (around 4-5 files) that
implements an agent, plus a diagram showing how the agent should work. The diagram is the
source of truth. ... At each part, the interviewer describes a scenario ... figure out what's
wrong in the code and fix it."* It's also close to Sierra's pilot debugging interview, where you
improve a colleague's PR alongside AI agents.
Source: [1Point3Acres](https://www.1point3acres.com/interview/thread/1147618), [Sierra blog](https://sierra.ai/blog/the-ai-native-interview)

Suggested time: 60 min. Fix the scenarios **in order**, because later ones assume earlier fixes.

```
python sierra/run.py 5              # scenario tests
cd sierra && python -m problem_5_agent_debug   # chat with the agent yourself
```

`llm.py` is a deterministic stand-in for the model. **Treat it as correct and don't edit it.**
Every bug is in `agent.py` or `tools.py`. There is exactly one bug per failing scenario.

## Diagram (source of truth)

```
 user message
      |
      v
 +--------------------------- Agent.handle ----------------------------+
 | append user message to history                                      |
 | repeat up to MAX_STEPS (5):                                         |
 |    action = llm.decide(history)                                     |
 |    Reply?    -> append assistant message, RETURN text               |
 |    ToolCall? -> tool requires auth and user not verified?           |
 |                     yes: result = {"error": "AUTH_REQUIRED"}        |
 |                     no:  result = tool(ctx, **args)                 |
 |                 append EVERY tool result to history (role "tool")   |
 | steps exhausted -> escalate_to_human("max_steps"), RETURN handoff   |
 +---------------------------------------------------------------------+

 Tools                       auth?  rules
 verify_identity(email)      no     email must belong to a customer; on the
                                    2nd failed attempt IN THE CONVERSATION ->
                                    escalate_to_human("verification_failed")
 lookup_order(order_id)      YES    only the verified customer's own orders;
                                    anyone else's order is NOT_FOUND
 issue_refund(order_id)      YES    own order only; never refund twice
                                    (ALREADY_REFUNDED); auto-refund only if
                                      status == delivered
                                      AND delivered <= 30 days ago (day 30 ok)
                                      AND amount <= $200.00
                                    otherwise INELIGIBLE + escalate(reason)
 escalate_to_human(reason)   no     marks the conversation escalated
```

## Scenarios (one per test)

| Part | Scenario | Expected |
|---|---|---|
| 0 | "hello" | Greeting. Already passes. |
| 1 | Sam verifies, then asks "Where is order #1001?" | "verified", then "shipped". No escalation. |
| 2 | An unverified user asks about #1001 | Asked to verify. The status is **not** leaked. |
| 3 | Sam asks about #2001, which is Lee's order | "couldn't find". Nothing leaked. |
| 4 | Sam asks for refunds on #1003 ($150) and #1004 ($250) | $150 refunded. $250 escalated as `over_limit`. |
| 5 | Refunds for #1002 (delivered exactly 30 days ago) and #1005 (31 days) | #1002 refunded. #1005 escalated as `outside_window`. |
| 6 | Sam asks for a refund on #1003 twice | One refund only. Second reply says "already". |
| 7 | Two wrong emails in a row | Second attempt escalates (`verification_failed`). |

## What to say in the video

For each fix: the symptom → how you localised it (which log/print, which file) → the root cause
→ the fix → the test that proves it. Then say what would have caught it earlier (a unit test per
tool, a type for money, an auth decorator, idempotency keys).
