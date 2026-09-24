# Sierra AI - CoderPad Assessment Practice

Practice set for Sierra's online assessment: "a few different coding questions, then a 3-5 min
video describing your approach, the tradeoffs you made under time pressure, how you worked with
AI, and how you'd make the code production ready."

Every problem is based on a question Sierra candidates have reported, or on a format Sierra has
described publicly. Each one builds up in parts, because Sierra's screens add requirements
as you go.

## Problems

| # | File | Based on | Skills | Time |
|---|---|---|---|---|
| 1 | [problem_1_flaky_api.py](problem_1_flaky_api.py) | Reported: flaky API + product fallback IDs | retry/backoff, error taxonomy, caching, cycles | 45m |
| 2 | [problem_2_spreadsheet.py](problem_2_spreadsheet.py) | Reported: spreadsheet cell deps + circular refs | parsing, DFS cycle path, topo recompute | 50m |
| 3 | [problem_3_word_search.py](problem_3_word_search.py) | Reported: Word Search (LC 79) | backtracking, trie (LC 212), extensibility | 40m |
| 4 | [problem_4_first_unique.py](problem_4_first_unique.py) | Reported: First Unique Character Index | hashing, streaming, sliding window | 35m |
| 5 | [problem_5_agent_debug/](problem_5_agent_debug/README.md) | Reported: debug a 4-5 file agent against a diagram | reading unfamiliar code, root-causing | 60m |
| 6 | [problem_6_task_graph.py](problem_6_task_graph.py) | Reported pattern: graph traversal, cycle detection | Kahn, critical path, k-worker scheduling | 50m |
| 7 | [problem_7_reporting_sql.py](problem_7_reporting_sql.py) | Reported: "Simplify reporting queries with CTEs" | CTEs, window functions, parameterised SQL | 40m |
| 8 | [problem_8_cancellation_flow.py](problem_8_cancellation_flow.py) | Reported: subscription-cancellation agent | state machine, guardrails, audit, resume | 50m |

Highest priority: **1, 2, 5**. They match the reported screen format most closely.

## Running

```bash
python sierra/run.py 1          # test your code for problem 1 (PASS / FAIL / TODO per part)
python sierra/run.py 1 -v       # with tracebacks
python sierra/run.py all        # everything
python sierra/run.py 2 --ref    # run the reference solution (only after your attempt)
```

Standard library only; no pytest needed. The spec for each problem is in its file's docstring.
Reference solutions are in `solutions/`. Problem 5's answer key is in
[solutions/problem_5_BUGS.md](solutions/problem_5_BUGS.md).

## How to practise each problem

1. **Timer on.** Read the whole docstring twice before typing. Run the tests once to see the baseline.
2. **Part by part.** Make Part N pass before reading Part N+1 closely. A working Part 2 beats a
   half-finished Part 4.
3. **Use AI the way the assessment expects**, and keep a log (below):
   - You design the data model and core logic. Give the AI small, bounded asks: "write the
     tokenizer regex", "5 edge-case tests for X", "why does this raise Y".
   - Read every suggestion before accepting it, and run tests right after each change.
   - Reject at least one suggestion per problem, and write down why (wrong edge case,
     over-engineered, a hidden behaviour change).
4. **Keep a running `NOTES` block** in a comment at the top of your file while you work:
   ```
   # TRADEOFFS: chose X over Y because ...; hard-coded Z to save time
   # AI: used for ...; rejected ... because ...
   # PROD: validation, timeouts, logging/metrics, tests for failure paths, config, auth
   ```
5. **Record the video** (see below) straight after each full mock. Watch it back once.

## 7-day schedule

| Day | Do |
|---|---|
| 1 | P1 + P4 (retry, hashing warm-up) |
| 2 | P2 + P6 (graphs, cycles, topo order) |
| 3 | P3 + P7 (backtracking/trie, SQL) |
| 4 | P5 (debugging); then re-do P1 from scratch in 30 min |
| 5 | P8 with AI assistance on purpose; practise the AI-use log |
| 6 | Full mock: P2 + P5 + P8 in 2.5h, then record a 4-min video |
| 7 | Re-do your weakest problem, review follow-ups out loud, rest |

## Video script (3-5 min)

1. **What I built** (30s): one line per question, and how far you got on each.
2. **Approach** (60-90s): the key insight in the hardest question, and why you chose that data
   structure.
3. **Tradeoffs under time pressure** (45s): what you simplified, hard-coded, or skipped, and why.
4. **How I used AI** (45s): what you delegated, how you checked it, one suggestion you rejected.
5. **Production-ready** (60s): input validation, typed errors, timeouts and retries,
   logging/metrics, tests for failure paths, config over constants, auth/PII, concurrency limits.
   Each problem's FOLLOW-UPS section lists specific points.

## Sources

- [Sierra: The AI-native interview](https://sierra.ai/blog/the-ai-native-interview)
- [Sierra SWE, Agent interview experience](https://gaijineer.co/sierra-software-engineer-agent-interview-experience)
- [Exponent: Sierra agent engineer guide](https://www.tryexponent.com/guides/sierra-agent-engineer-interview)
- [Exponent: Sierra SWE questions](https://www.tryexponent.com/questions?company=sierra-ai&role=swe)
- [Glassdoor: Sierra interviews](https://www.glassdoor.com/Interview/Sierra-Interview-Questions-E10032095.htm)
- [PracHub: CoderPad Screen assessments](https://prachub.com/resources/coderpad-screen-assessment-what-to-expect-from-take-home-projects)
