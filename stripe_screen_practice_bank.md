# Stripe Technical Screen — OOD Practice Bank

Companion to [stripe_oa_prep_cheatsheet.md](stripe_oa_prep_cheatsheet.md). That doc is for the **async OA** (parse + aggregate). This doc is for the **live technical screen**: 45–60 min with an interviewer, design a class, then iterate through follow-ups as they add requirements.

---

## 1. What Stripe grades in the screen

Based on reported experiences (LeetCode Discuss, Glassdoor, Medium write-ups for 2025–2026 new-grad loops):

1. **Clean class structure, not clever algorithms.** Small methods, descriptive names, a clear data model. Interviewers flag "one giant function that does everything".
2. **Invariants up front.** State what cannot happen (e.g. "a payment_id is recorded at most once"). Enforce it in code — raise, don't silently overwrite.
3. **Extensibility.** Part 2–4 add refunds, partial refunds, time-range queries, persistence. Your Part 1 data model should make Part 3 a 10-line addition, not a rewrite. This is the #1 signal they watch for.
4. **Correctness under edge cases.** Duplicate IDs, refunds > original amount, refunds for unknown payments, empty date ranges, timestamps in the wrong order.
5. **Complexity awareness, not optimization.** They want you to say "this is O(n) per query, for big data I'd index by date bucket" — not to actually build the index unless they ask.
6. **Pair-programming feel.** Talk through trade-offs out loud. Silence reads as stuck. The interviewer often nudges — take the nudge.

Sources: [Stripe 2026 New Grad Round 1 VO guide](https://medium.com/@programhelp/stripe-2026-new-grad-round-1-vo-in-depth-interview-guide-0618ba9be92c), [Stripe New Grad OA discuss](https://leetcode.com/discuss/post/7428741/stripe-university-recruiting-oa-online-a-iicb/), [Exponent Stripe guide](https://www.tryexponent.com/guides/stripe-swe-interview), [Stripe idempotency blog](https://stripe.com/blog/idempotency).

---

## 2. How to practice

- **60 minutes per problem.** Split roughly: 10 min on Part 1, 15 min Part 2, 15 min Part 3, 10 min on verbal follow-ups. Leave 10 min buffer.
- Write in a single Python file. Run it. Put 3–4 asserts at the bottom as your own smoke test.
- Hit the API checklist from [stripe_oa_prep_cheatsheet.md](stripe_oa_prep_cheatsheet.md) §4 (`defaultdict`, `bisect`) and §3 (dates).
- After the timer: read the **follow-ups** section and answer each one out loud in 1–2 sentences. That's what the interviewer is looking for.
- Only open the **Reference solution** after you've taken a real swing. The hint ladder is for when you're genuinely stuck — use one rung at a time.

---

## 3. Universal skeleton

Every problem in this bank fits the same mould. Drop this in first, then specialise:

```python
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime

class LedgerError(ValueError):
    """Domain errors surface as ValueError subclasses so callers can catch narrowly."""

@dataclass(frozen=True)
class Event:
    id: str
    amount_cents: int
    ts: datetime
```

Frozen dataclass gives you immutability and a free `__repr__` — useful for debugging in the interview.

---

## Problem 1 — PaymentLedger (the reference problem)

> You're building the transaction recording layer for a payments service. Implement `PaymentLedger`:
>
> - `add_payment(payment_id, amount_cents, timestamp)`
> - `add_refund(payment_id, amount_cents, timestamp)`
> - `get_total_revenue() -> int`
> - `get_payments_by_date(d: date) -> list[Payment]`
>
> Rules: `payment_id` is unique per payment; a refund must reference a known payment; refund amount must not exceed remaining refundable balance. Timestamps are `datetime` objects.

### Part 2 — Partial refunds
Allow multiple refunds against the same payment as long as the cumulative refunded amount does not exceed the original payment amount.

### Part 3 — Range query
Add `get_payments_in_range(start: date, end: date) -> list[Payment]` (inclusive on both ends). Expect this to be called often; mention how you would scale it.

### Part 4 — Persistence (verbal)
How would you persist the ledger to a database? What schema, what indices, what guarantees do you lose vs the in-memory version?

### Follow-ups to rehearse
- "What if timestamps arrive out of order?" → Your data model already handles it; only the `by_date` index needs `bisect` or a sorted container if ordered iteration matters.
- "What if the timestamp string is malformed?" → `datetime.fromisoformat` raises `ValueError`; wrap in `LedgerError` at the boundary, fail fast.
- "How do you scale `get_payments_by_date` to billions of rows?" → Bucket index (`dict[date, list[id]]`) gives O(k) where k is matches. For true scale, move to a DB with an index on `date(ts)` or a column-store partitioned by day.
- "Concurrent writers?" → Add a per-id lock or use a transaction; dedupe becomes `INSERT ... ON CONFLICT DO NOTHING`.

### Hint ladder
1. Model `Payment` as a dataclass with `id, amount_cents, ts, refunded_cents=0`. Store in `dict[str, Payment]` for O(1) dedupe.
2. Maintain `_by_date: dict[date, list[str]]` alongside the main dict. Update on every `add_payment`.
3. `get_total_revenue` = sum of `(amount - refunded)` over all payments. Keep a running total if you want O(1).
4. Range query: iterate `self._by_date` keys in range. For large ranges, keep dates in a sorted list and `bisect` into it.

### Reference solution

```python
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime

class LedgerError(ValueError):
    pass

@dataclass
class Payment:
    id: str
    amount_cents: int
    ts: datetime
    refunded_cents: int = 0

    @property
    def net_cents(self) -> int:
        return self.amount_cents - self.refunded_cents

    @property
    def refundable_cents(self) -> int:
        return self.amount_cents - self.refunded_cents

class PaymentLedger:
    def __init__(self) -> None:
        self._payments: dict[str, Payment] = {}
        self._by_date: dict[date, list[str]] = defaultdict(list)
        self._total_cents: int = 0  # running net revenue

    def add_payment(self, payment_id: str, amount_cents: int, ts: datetime) -> None:
        if amount_cents <= 0:
            raise LedgerError(f"amount must be positive, got {amount_cents}")
        if payment_id in self._payments:
            raise LedgerError(f"duplicate payment_id: {payment_id}")
        p = Payment(payment_id, amount_cents, ts)
        self._payments[payment_id] = p
        self._by_date[ts.date()].append(payment_id)
        self._total_cents += amount_cents

    def add_refund(self, payment_id: str, amount_cents: int, ts: datetime) -> None:
        if amount_cents <= 0:
            raise LedgerError(f"refund must be positive, got {amount_cents}")
        p = self._payments.get(payment_id)
        if p is None:
            raise LedgerError(f"unknown payment_id: {payment_id}")
        if amount_cents > p.refundable_cents:
            raise LedgerError(
                f"refund {amount_cents} exceeds refundable {p.refundable_cents} on {payment_id}"
            )
        p.refunded_cents += amount_cents
        self._total_cents -= amount_cents

    def get_total_revenue(self) -> int:
        return self._total_cents

    def get_payments_by_date(self, d: date) -> list[Payment]:
        return [self._payments[pid] for pid in self._by_date.get(d, ())]

    def get_payments_in_range(self, start: date, end: date) -> list[Payment]:
        if end < start:
            return []
        out: list[Payment] = []
        # O(days * k) — fine for typical inputs. Mention bisect on sorted keys for large ranges.
        d = start
        while d <= end:
            out.extend(self.get_payments_by_date(d))
            d = d.fromordinal(d.toordinal() + 1)
        return out
```

**Talking points while coding:** "I'm keeping `_by_date` as a secondary index so `get_payments_by_date` stays O(k). The running total avoids rescanning on every `get_total_revenue` call — small memory cost, big on hot read paths."

---

## Problem 2 — IdempotencyStore

> Stripe's public API lets clients send an `Idempotency-Key` header. If the same key is retried, the server must return the original response instead of re-executing the handler. Implement `IdempotencyStore`:
>
> - `execute(key: str, request: dict, handler: Callable[[dict], Response]) -> Response`
>
> The first call with `key` runs `handler(request)` and caches the response. Subsequent calls with the same `key` return the cached response without re-running. If a second call comes in **while** the first is still in flight, it should block until the first completes and then return the same response.

### Part 2 — Request mismatch
If a later call reuses `key` but with a different `request` body, raise `IdempotencyConflict`. (Stripe's real API does this.)

### Part 3 — TTL
Keys expire after 24 hours. After expiry, reusing the key executes the handler fresh. Expose `gc()` to drop expired entries; assume it's called periodically.

### Part 4 — Distributed (verbal)
What changes in a multi-process, multi-region setup? Where's the source of truth?

### Follow-ups
- "Why not just hash the request and use that as the key?" → Then retries after network failure can't be made safe unless the client re-hashes identically; explicit keys decouple the client's notion of "same request" from byte equality.
- "What if the handler raises?" → Stripe caches the failure response too. Retries return the same error. Discuss the rationale: predictable client behaviour.
- "Race in distributed mode?" → Need a shared store (Redis, DB row) with a transaction that inserts the key in "in-flight" state; second caller sees in-flight, polls or blocks.

### Hint ladder
1. Data per key: `(request_hash, status, response, created_at, event_for_blocking)`.
2. Use `threading.Event` per in-flight key to let late callers block until completion.
3. Hash the request with `json.dumps(sort_keys=True)` then `hashlib.sha256` — don't compare dicts directly in case of ordering or nested list order.

### Reference solution

```python
import hashlib, json, threading, time
from dataclasses import dataclass, field
from typing import Any, Callable

class IdempotencyConflict(ValueError):
    pass

@dataclass
class _Entry:
    request_hash: str
    created_at: float
    response: Any = None
    error: BaseException | None = None
    done: threading.Event = field(default_factory=threading.Event)

class IdempotencyStore:
    def __init__(self, ttl_seconds: int = 24 * 3600) -> None:
        self._ttl = ttl_seconds
        self._entries: dict[str, _Entry] = {}
        self._lock = threading.Lock()

    @staticmethod
    def _hash(request: dict) -> str:
        return hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()

    def execute(self, key: str, request: dict, handler: Callable[[dict], Any]) -> Any:
        req_hash = self._hash(request)
        now = time.time()

        with self._lock:
            entry = self._entries.get(key)
            if entry and now - entry.created_at > self._ttl:
                entry = None
            if entry is None:
                entry = _Entry(request_hash=req_hash, created_at=now)
                self._entries[key] = entry
                is_leader = True
            else:
                if entry.request_hash != req_hash:
                    raise IdempotencyConflict(f"key {key} reused with different body")
                is_leader = False

        if is_leader:
            try:
                entry.response = handler(request)
            except BaseException as e:
                entry.error = e
            finally:
                entry.done.set()
        else:
            entry.done.wait()

        if entry.error is not None:
            raise entry.error
        return entry.response

    def gc(self) -> int:
        cutoff = time.time() - self._ttl
        with self._lock:
            expired = [k for k, v in self._entries.items() if v.created_at < cutoff and v.done.is_set()]
            for k in expired:
                del self._entries[k]
        return len(expired)
```

**Talking points:** "I'm using an `Event` so that a second caller on the same key doesn't re-run the handler but also doesn't return stale — it waits. The leader/follower split keeps the lock scope tiny: we only hold `_lock` during the dict lookup, not during handler execution."

---

## Problem 3 — RateLimiter (sliding window per merchant)

> Stripe enforces per-merchant API quotas. Implement a sliding-window rate limiter:
>
> - `allow(merchant_id: str, timestamp: int) -> bool`
>
> Each merchant gets `LIMIT` requests per `WINDOW` seconds. Return `True` and record the request if allowed; `False` otherwise. Timestamps arrive non-decreasing.

### Part 2 — Per-endpoint limits
Limits vary by `(merchant_id, endpoint)`. Charges endpoint might allow 100/sec, refunds 10/sec. Extend the signature.

### Part 3 — Burst allowance
Allow short bursts above the limit, paid off by subsequent idle time. (Hint: token bucket.) Discuss when to use sliding window vs token bucket.

### Part 4 — Analytics
Add `top_k_throttled(k: int) -> list[str]` returning the merchants most frequently rate-limited in the last hour. Complexity?

### Follow-ups
- "Why `deque` and not a counter?" → Sliding window requires knowing *which* requests are still in-window. A counter loses that information unless you bucket by second.
- "Timestamps not monotonic?" → Either reject or buffer-and-sort. Stripe would reject — signals clock skew.
- "Scale to 10M merchants?" → Per-merchant deque is fine memory-wise. For distributed, Redis `ZSET` with score = timestamp is the standard move.

### Hint ladder
1. `defaultdict(deque)` keyed by `merchant_id`.
2. On each `allow`, pop from the left while front < ts - window.
3. If `len(deque) < LIMIT`, append and return True; else False.

### Reference solution

```python
from collections import defaultdict, deque

class RateLimiter:
    def __init__(self, limit: int, window_seconds: int) -> None:
        self._limit = limit
        self._window = window_seconds
        self._hits: dict[str, deque[int]] = defaultdict(deque)
        self._throttled: dict[str, int] = defaultdict(int)

    def allow(self, merchant_id: str, ts: int) -> bool:
        q = self._hits[merchant_id]
        cutoff = ts - self._window
        while q and q[0] <= cutoff:
            q.popleft()
        if len(q) >= self._limit:
            self._throttled[merchant_id] += 1
            return False
        q.append(ts)
        return True

    def top_k_throttled(self, k: int) -> list[str]:
        # O(n log k) with heapq.nlargest; good enough for interview scope.
        import heapq
        return heapq.nlargest(k, self._throttled, key=self._throttled.get)
```

**Talking points:** "The deque is O(1) amortised per call. The one invariant: every appended timestamp is > every previously appended one, which is given by the non-decreasing assumption. If that assumption breaks, the `popleft` logic silently misbehaves — I'd add a monotonic assert at the top in production."

---

## Problem 4 — FraudDetector (count + ratio thresholds)

> Merchants are tagged with an MCC (Merchant Category Code). Each MCC has either an **integer** threshold (mark as fraud once N disputes) or a **float** threshold (mark as fraud once disputes / charges > ratio, with a minimum charge count). Process a stream of events:
>
> - `CHARGE,merchant_id,amount_cents`
> - `DISPUTE,merchant_id,charge_id`
>
> Implement `FraudDetector`:
>
> - `register_merchant(merchant_id, mcc)`
> - `process(event: str)`
> - `fraudulent_merchants() -> list[str]`

### Part 2 — Dispute resolution
Add `RESOLVE,merchant_id,charge_id`. Resolved disputes don't count toward the threshold. If a merchant was marked fraud and a resolve brings them below threshold, they stay marked fraud (disputes are sticky — Stripe behaviour).

### Part 3 — MCC changes
A merchant can change MCC. Thresholds re-evaluate under the new MCC's rule. Old disputes count under the new rule.

### Part 4 — Windowed version (verbal)
Now only disputes in the last 30 days count. Sketch the index.

### Follow-ups
- "Why is fraud sticky?" → Compliance and downstream systems (payouts, KYC) depend on the flag being stable. Unflagging is a human decision.
- "Ratio threshold with zero charges?" → Guarded by the minimum-charge floor; otherwise you'd flag merchants on their first dispute.

### Hint ladder
1. Two dicts: `_mcc: dict[str, str]` and `_threshold: dict[str, int | tuple[float, int]]`.
2. Per merchant: `charges_count`, `disputes_count`. Recompute flag on every event.
3. Parse event with `line.split(",")` and a dispatch dict — cleaner than nested `if`s.

### Reference solution

```python
from dataclasses import dataclass, field

@dataclass
class _Merchant:
    mcc: str
    charges: int = 0
    disputes: int = 0
    flagged: bool = False

class FraudDetector:
    def __init__(self, mcc_rules: dict[str, int | tuple[float, int]]) -> None:
        # int rule = absolute dispute count
        # tuple rule = (ratio, min_charges)
        self._rules = mcc_rules
        self._m: dict[str, _Merchant] = {}

    def register_merchant(self, merchant_id: str, mcc: str) -> None:
        if mcc not in self._rules:
            raise ValueError(f"no rule for mcc {mcc}")
        self._m[merchant_id] = _Merchant(mcc=mcc)

    def process(self, event: str) -> None:
        kind, mid, *rest = [p.strip() for p in event.split(",")]
        m = self._m.get(mid)
        if m is None:
            return  # or raise — depends on spec
        if kind == "CHARGE":
            m.charges += 1
        elif kind == "DISPUTE":
            m.disputes += 1
        else:
            raise ValueError(f"unknown event kind {kind}")
        self._reevaluate(m)

    def _reevaluate(self, m: _Merchant) -> None:
        if m.flagged:
            return  # sticky
        rule = self._rules[m.mcc]
        if isinstance(rule, int):
            if m.disputes >= rule:
                m.flagged = True
        else:
            ratio, min_ch = rule
            if m.charges >= min_ch and m.disputes / m.charges > ratio:
                m.flagged = True

    def fraudulent_merchants(self) -> list[str]:
        return sorted(mid for mid, m in self._m.items() if m.flagged)
```

**Talking points:** "Sticky flag is a one-way door — `_reevaluate` short-circuits if already flagged. The two rule types share one dispatch path so adding a third (e.g. amount-based) is a one-branch change."

---

## Problem 5 — WebhookDispatcher (retry with exponential backoff)

> Stripe delivers webhook events to merchant URLs. If the merchant's server returns non-2xx, we retry with exponential backoff. Implement:
>
> - `enqueue(event_id, url, payload, now)`
> - `tick(now)` — deliver any events whose next_attempt_at ≤ now
>
> On failure, reschedule for `now + 2 ** attempt` seconds, capped at 1 hour, up to 5 attempts. After 5 failures, move to dead-letter.

### Part 2 — Signature
Every delivery includes an `HMAC-SHA256` signature over the payload with the merchant's webhook secret. Verify in a test helper.

### Part 3 — Ordering
Merchants expect events for the same `object_id` (e.g. same charge) in timestamp order. A failed earlier event must not be overtaken by a later one. Design change?

### Part 4 — At-least-once vs exactly-once (verbal)
Which is Stripe's real guarantee, and why does it push idempotency onto the merchant?

### Follow-ups
- "Why cap backoff?" → Without a cap, a 5th retry lands weeks later — merchants have given up by then. Cap + attempt limit + dead-letter is the standard triad.
- "Min-heap or sorted list?" → Min-heap. `heapq` with `(next_attempt_at, seq, event)` tuples; `seq` breaks ties deterministically.

### Hint ladder
1. Delivery record: `event_id, url, payload, attempts, next_at, status`.
2. Pending queue = min-heap on `next_at`. `tick` pops while top `<= now`.
3. HTTP client is a handler injected at construction — makes testing trivial. Don't hard-code `requests.post`.

### Reference solution

```python
import heapq, hmac, hashlib
from dataclasses import dataclass, field
from typing import Callable

MAX_ATTEMPTS = 5
MAX_BACKOFF = 3600

@dataclass
class _Delivery:
    event_id: str
    url: str
    payload: bytes
    attempts: int = 0
    next_at: int = 0
    status: str = "pending"  # pending | delivered | dead

class WebhookDispatcher:
    def __init__(self, sender: Callable[[str, bytes, str], int], secret: bytes) -> None:
        self._send = sender  # (url, payload, signature) -> http_status
        self._secret = secret
        self._heap: list[tuple[int, int, str]] = []  # (next_at, seq, event_id)
        self._by_id: dict[str, _Delivery] = {}
        self._dead: list[str] = []
        self._seq = 0

    def enqueue(self, event_id: str, url: str, payload: bytes, now: int) -> None:
        if event_id in self._by_id:
            return  # dedupe enqueue
        d = _Delivery(event_id, url, payload, next_at=now)
        self._by_id[event_id] = d
        heapq.heappush(self._heap, (d.next_at, self._seq, event_id))
        self._seq += 1

    def _sign(self, payload: bytes) -> str:
        return hmac.new(self._secret, payload, hashlib.sha256).hexdigest()

    def tick(self, now: int) -> None:
        while self._heap and self._heap[0][0] <= now:
            _, _, eid = heapq.heappop(self._heap)
            d = self._by_id[eid]
            if d.status != "pending":
                continue  # stale heap entry
            d.attempts += 1
            status = self._send(d.url, d.payload, self._sign(d.payload))
            if 200 <= status < 300:
                d.status = "delivered"
            elif d.attempts >= MAX_ATTEMPTS:
                d.status = "dead"
                self._dead.append(eid)
            else:
                backoff = min(MAX_BACKOFF, 2 ** d.attempts)
                d.next_at = now + backoff
                heapq.heappush(self._heap, (d.next_at, self._seq, eid))
                self._seq += 1

    def dead_letter(self) -> list[str]:
        return list(self._dead)
```

**Talking points:** "I never delete from the heap — I mark the delivery done and skip stale entries on pop. Cheaper than heap reconstruction. The `sender` is injected so tests can pass a `lambda url, payload, sig: 200` to simulate happy path or `500` to exercise backoff."

---

## Problem 6 — SubscriptionBilling (lighter OOD, good warm-up)

> Implement `SubscriptionService` with:
>
> - `subscribe(customer_id, plan, monthly_amount_cents, start_date)`
> - `cancel(customer_id, plan, cancel_date)`
> - `charge_for_month(year, month) -> dict[customer_id, total_cents]`
>
> Rules: subscription is charged in a month iff `start_date` ≤ last day of that month AND (not cancelled OR `cancel_date` > last day of that month). Sort output by `customer_id`.

### Part 2 — Proration
If `start_date` falls within the month, prorate by `(days_left_including_start / days_in_month)`, floored to cents.

### Part 3 — Plan changes mid-month
A customer can switch from `basic` → `pro` on a given date. The prior plan is billed up to the day before; the new plan is billed from the switch day.

### Part 4 — What breaks at 100M customers?
How does this change with persistence, and what's the query pattern that kills a naive schema?

### Follow-ups
- "Why `int` cents and `//` not `round`?" → Floats drift, rounding policies differ per jurisdiction. Cents + floor is auditable; the <$0.01 residual is expected and reconciled separately.
- "Cancellation edge case: cancel on the 1st of the target month?" → Depends on spec — usually "no charge for the cancellation month". Read the prompt carefully, ask if ambiguous.

### Hint ladder
1. `(customer_id, plan)` is the primary key for a subscription row.
2. Store `start_date, cancel_date or None, monthly_cents`.
3. Use `calendar.monthrange(year, month)[1]` for days-in-month.

### Reference solution

```python
import calendar
from collections import defaultdict
from dataclasses import dataclass
from datetime import date

@dataclass
class _Sub:
    customer_id: str
    plan: str
    monthly_cents: int
    start: date
    end: date | None = None  # exclusive cancellation date

class SubscriptionService:
    def __init__(self) -> None:
        self._subs: dict[tuple[str, str], _Sub] = {}

    def subscribe(self, cid: str, plan: str, monthly_cents: int, start: date) -> None:
        key = (cid, plan)
        if key in self._subs and self._subs[key].end is None:
            raise ValueError(f"active subscription exists: {key}")
        self._subs[key] = _Sub(cid, plan, monthly_cents, start)

    def cancel(self, cid: str, plan: str, cancel_date: date) -> None:
        sub = self._subs.get((cid, plan))
        if sub is None or sub.end is not None:
            raise ValueError(f"no active subscription: ({cid}, {plan})")
        sub.end = cancel_date

    def charge_for_month(self, year: int, month: int) -> dict[str, int]:
        first = date(year, month, 1)
        days_in_month = calendar.monthrange(year, month)[1]
        last = date(year, month, days_in_month)
        totals: dict[str, int] = defaultdict(int)

        for sub in self._subs.values():
            if sub.start > last:
                continue
            if sub.end is not None and sub.end <= first:
                continue
            if sub.start <= first:
                totals[sub.customer_id] += sub.monthly_cents
            else:
                days_left = days_in_month - sub.start.day + 1
                totals[sub.customer_id] += (sub.monthly_cents * days_left) // days_in_month

        return dict(sorted(totals.items()))
```

**Talking points:** "I store subscriptions keyed on `(customer_id, plan)` so lookups for `cancel` are O(1). For 100M customers I'd move to a DB with an index on `customer_id` and one on `(end IS NULL, start)` to find active subs for a month; the `charge_for_month` scan becomes unacceptable past a few million rows."

---

## 4. Rehearsal schedule (one week out)

| Day | Session | Problem | Goal |
|-----|---------|---------|------|
| Mon | 60 min | Problem 1 (PaymentLedger) | Baseline. Note where you slowed. |
| Tue | 30 min | Re-do Problem 1 follow-ups out loud, then read Problem 2 prompt + hints only. | Separate "can I speak to it" from "can I code it". |
| Wed | 60 min | Problem 2 (IdempotencyStore) | Concurrency primitives (`threading.Event`). |
| Thu | 60 min | Problem 3 (RateLimiter) | `deque` fluency. |
| Fri | 60 min | Problem 4 (FraudDetector) | Multi-rule dispatch, state machines. |
| Sat | 60 min | Problem 5 (WebhookDispatcher) | `heapq`, time-based scheduling, HMAC. |
| Sun | 30 min | Problem 6 + re-read §1 grading criteria. | Light reset before the screen. |

---

## 5. What to say out loud while coding

Interviewers score the narration as much as the code. Canned phrases that map to real thinking:

- "I'll sketch the data model first — `dict[id, Record]` for O(1) dedupe, secondary index on date."
- "The invariant here is X; I'll enforce it at the write path so no reader has to check."
- "For this query I'm writing it O(n); if we cared about latency I'd add an index on Y — want me to do that now or after we get the base case working?"
- "Edge case I want to confirm: what should happen if amount is zero? Negative? Refund greater than balance?"
- "I'll inject the HTTP client / clock / sender so tests can swap it — that's worth one extra parameter."

---

## 6. Cross-links

- API and stdlib refresher: [stripe_oa_prep_cheatsheet.md](stripe_oa_prep_cheatsheet.md)
- Idempotency deep-dive: [Stripe engineering blog](https://stripe.com/blog/idempotency)
- Real reported questions: [Exponent Stripe guide](https://www.tryexponent.com/guides/stripe-swe-interview), [Stripe 2026 VO Round 1](https://medium.com/@programhelp/stripe-2026-new-grad-round-1-vo-in-depth-interview-guide-0618ba9be92c), [LeetCode Stripe discuss](https://leetcode.com/discuss/post/7428741/stripe-university-recruiting-oa-online-a-iicb/)
