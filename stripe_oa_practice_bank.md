# Stripe HackerRank OA — Practice Problem Bank

**Format for every problem:** 60 minutes total, one problem split into 4 progressive parts. Each part builds on the previous one. You'll typically be given the next part only after completing the current one in the real OA — here, resist the urge to read ahead. Treat each part as its own ~15-minute chunk.

**What Stripe is testing:**
- Clean, readable code (descriptive names, small functions, early returns)
- Correct handling of edge cases (empty inputs, malformed data, boundary values)
- Parsing and state management over clever algorithms
- Ability to extend code without rewriting it — Part 4 should reuse Parts 1-3
- Reasonable complexity, not necessarily optimal

**How to practice:**
1. Set a 60-minute timer. Don't pause it.
2. Write real code in a real file. No pseudocode shortcuts.
3. Write your own test cases before reading the hidden ones.
4. After time's up, review what you missed — edge cases are usually where points are lost.

---

## Problem 1: Subscription Billing Engine

You're building a simplified version of Stripe Billing. Customers have subscriptions with monthly charges, and you need to compute what they owe.

### Part 1 — Parse subscriptions
Given a list of subscription strings in the format `"customer_id,plan,monthly_amount_cents,start_date"`, parse them into a structured form. Dates are `YYYY-MM-DD`. Return a list of subscription records.

Example input:
```
cus_001,basic,900,2025-01-15
cus_002,pro,2900,2025-02-01
cus_001,addon,500,2025-03-10
```

Handle: malformed rows (skip them), duplicate customer entries (keep all — one customer can have multiple subscriptions).

### Part 2 — Compute monthly charges
Given subscriptions from Part 1 and a target month (e.g. `"2025-04"`), return the total cents owed per customer for that month. A subscription is charged in a given month if its start date is on or before the first of that month. Output: `dict[customer_id, total_cents]`, sorted by customer_id.

### Part 3 — Handle cancellations
Extend to accept a list of cancellation events: `"customer_id,plan,cancel_date"`. A cancelled subscription is NOT charged in the cancellation month or any month after. If a customer cancels mid-month, they still pay that month's full charge (no proration). Re-compute charges for the target month.

### Part 4 — Proration for new signups
Now add proration for subscriptions that start mid-month. If a subscription's start_date falls within the target month (not on the 1st), the customer pays a prorated amount: `monthly_amount * (days_remaining_in_month / days_in_month)`, rounded down to the nearest cent. Cancellations still don't prorate. Produce the final per-customer totals.

**What this tests:** parsing, date arithmetic, state across multiple event types, careful reading of billing rules.

---

## Problem 2: API Rate Limiter Analytics

Stripe's API enforces per-merchant rate limits. You're analyzing request logs to identify merchants hitting their limits.

### Part 1 — Parse request logs
Logs look like: `"timestamp_seconds,merchant_id,endpoint,status_code"`. Parse a list of these into structured records. Skip rows where `status_code` isn't a valid integer or `timestamp_seconds` isn't parseable.

```
1700000000,merch_A,/v1/charges,200
1700000005,merch_A,/v1/charges,429
1700000006,merch_B,/v1/refunds,200
```

### Part 2 — Count rate-limited requests
For each merchant, count the number of requests with status code `429` (rate limited). Return a dict sorted by merchant_id.

### Part 3 — Identify abusive windows
A merchant is considered "abusive" in a 60-second window if they made more than `N` total requests in any rolling 60-second window. Given a threshold `N`, return the set of merchant_ids that had at least one abusive window. Use a sliding window — do NOT re-scan for every timestamp.

### Part 4 — Suggest new limits
For each merchant flagged in Part 3, compute a suggested new rate limit: the 95th percentile of their per-minute request counts (bucketed by calendar minute, not sliding), rounded up to the nearest 10. Return `dict[merchant_id, suggested_limit]`.

**What this tests:** sliding window technique, percentile calculation, bucketing, being careful about rolling vs. fixed windows (a classic Stripe trap).

---

## Problem 3: Payout Reconciliation

Stripe pays out to merchants on a schedule. You're reconciling internal ledgers against bank confirmations.

### Part 1 — Parse the ledger
Given ledger entries `"payout_id,merchant_id,amount_cents,scheduled_date,currency"`, parse and group them by merchant_id. Amounts can be negative (refunds). Skip rows with invalid amounts or dates.

### Part 2 — Parse bank confirmations and match
Bank confirmations come as `"payout_id,confirmed_amount_cents,confirmed_date"`. Match each ledger entry to its bank confirmation by `payout_id`. Return three lists:
- `matched`: ledger entries where bank amount equals ledger amount
- `mismatched`: payout_id exists in both but amounts differ
- `unconfirmed`: ledger entry has no corresponding bank confirmation

### Part 3 — Handle multi-currency
Currencies may differ. Given a simple exchange rate table `dict[(from, to), rate]`, convert all amounts to USD before comparing. A match now allows a tolerance of ±1 cent USD (to handle rounding). Re-classify into matched/mismatched/unconfirmed.

### Part 4 — Detect duplicate payouts
A "duplicate payout" is one where the same merchant received two confirmed payouts for the exact same USD amount within 24 hours of each other. Return a list of `(merchant_id, payout_id_1, payout_id_2)` tuples for all duplicates. Order each tuple by payout_id ascending, and sort the output list.

**What this tests:** data joining, tolerance-based matching (real-world money logic), currency conversion, pairwise comparisons with a time constraint. This one feels very Stripe.

---

## Problem 4: Merchant Risk Scoring

You're scoring merchants based on transaction patterns to flag potential fraud.

### Part 1 — Parse transactions
Transactions: `"txn_id,merchant_id,amount_cents,status,timestamp"`. Status is one of `authorized`, `captured`, `refunded`, `disputed`, `failed`. Parse into records. Discard rows with unknown status values.

### Part 2 — Compute per-merchant stats
For each merchant, compute:
- total volume (sum of `captured` amounts, minus `refunded`)
- dispute rate: `disputed / captured` count (0 if no captures)
- failure rate: `failed / (failed + authorized + captured)` count

Return `dict[merchant_id, {"volume": ..., "dispute_rate": ..., "failure_rate": ...}]`.

### Part 3 — Score merchants
Assign a risk score 0–100 to each merchant:
- Start at 0
- +40 if dispute_rate > 0.01 (1%)
- +30 if failure_rate > 0.10 (10%)
- +20 if volume > 1,000,000 cents AND dispute_rate > 0.005
- +10 if merchant has any transaction above 500,000 cents

Return merchants sorted by score descending, ties broken by merchant_id ascending.

### Part 4 — Time-weighted scoring
Disputes in the last 7 days (relative to the latest timestamp in the dataset) count double toward the dispute rate. Recompute scores. The same merchant may now cross thresholds they didn't before. Return the new ranking.

**What this tests:** aggregation, multiple derived metrics, threshold-based logic, relative time windows. Be careful with division by zero.

---

## Problem 5: Webhook Delivery Queue

Stripe delivers webhooks to merchants. Deliveries can fail and need retry logic.

### Part 1 — Parse delivery events
Events: `"event_id,merchant_id,timestamp,status"`. Status is `sent`, `delivered`, `failed`, or `retrying`. Group events by `event_id` (each event may have multiple delivery attempts).

### Part 2 — Determine final status
For each event_id, determine the final delivery status: the status of the attempt with the latest timestamp. Return `dict[event_id, final_status]`.

### Part 3 — Compute retry intervals
For events that had retries, compute the time elapsed (in seconds) between consecutive attempts. Return `dict[event_id, list[int]]` where the list holds the gaps in chronological order. Events with only one attempt are excluded.

### Part 4 — Apply backoff policy check
Stripe's retry policy requires exponential backoff: each retry interval should be at least `2 * previous_interval` (with the first retry at least 60 seconds after the initial send). Identify events that **violated** the backoff policy — i.e. where any retry came too soon. Return the list of violating event_ids sorted ascending.

**What this tests:** grouping, time-series within groups, policy validation, careful iteration (off-by-one errors love this kind of problem).

---

## Problem 6: Tax Calculation Pipeline

Compute sales tax for transactions across jurisdictions.

### Part 1 — Parse transactions and tax rules
Transactions: `"txn_id,amount_cents,jurisdiction,product_type"`. Tax rules: `"jurisdiction,product_type,rate_bps"` where `rate_bps` is basis points (100 bps = 1%). Build a lookup from `(jurisdiction, product_type) → rate_bps`. If multiple rules match, use the last one seen.

### Part 2 — Compute tax per transaction
For each transaction, compute `tax_cents = floor(amount_cents * rate_bps / 10000)`. Use integer arithmetic only — no floats. If no rule matches the `(jurisdiction, product_type)` pair, fall back to a default rate of 0. Return `dict[txn_id, tax_cents]`.

### Part 3 — Handle tax exemptions
Given a list of exempt customer IDs and a mapping `txn_id → customer_id`, set tax to 0 for any transaction belonging to an exempt customer. Also handle a list of exempt product types (globally exempt regardless of jurisdiction).

### Part 4 — Compute jurisdiction totals with rounding reconciliation
For each jurisdiction, compute:
- total taxable amount (pre-tax)
- total tax collected
- "rounding loss": the difference between tax-if-computed-at-aggregate-level vs. tax-summed-from-individual-txns

Return `dict[jurisdiction, {"taxable": ..., "collected": ..., "rounding_loss": ...}]`. Rounding loss is a real accounting concept — expect it to be small but non-zero.

**What this tests:** integer arithmetic (avoiding float pitfalls), lookup with fallbacks, aggregation, and a genuinely subtle final part that rewards careful reading.

---

## General Tips for All Problems

**Before you start coding (spend 3–5 min):**
- Re-read the problem. Note every edge case mentioned.
- Sketch the data shapes you'll produce.
- Decide on your parsing approach — usually `[line.split(",") for line in input]` with a try/except per row.

**Structuring across 4 parts:**
- Write Part 1 as a function that returns a clean data structure.
- Parts 2-4 should CALL Part 1's output, not reparse.
- Don't prematurely optimize — clarity wins points.
- If you finish a part early, write 2-3 test cases before moving on.

**Common edge cases Stripe tests:**
- Empty input lists
- Malformed rows (missing fields, wrong types)
- Duplicate keys
- Zero amounts / zero counts (division)
- Exact boundary values (`>=` vs `>`)
- Timezone/date-boundary edge cases
- Amounts at integer overflow boundaries (less common but possible)

**Your Python strengths to lean on:**
- `collections.defaultdict`, `collections.Counter`
- `datetime` for date math (not `time`)
- `bisect` for sorted insertions if needed
- List comprehensions for clarity, not for showing off

**What kills candidates:**
- Using floats for money (always use integer cents)
- Skipping edge case handling to finish faster (points are weighted toward edge cases)
- Rewriting Part 1 for Part 4 instead of extending
- Getting cute with one-liners at the cost of readability

Good luck. When you've done a couple, ping me with solutions and I'll review them.
