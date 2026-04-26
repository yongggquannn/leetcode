"""
Rate Limiter (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/bd6fd9ae-d5d2-4565-b262-2e3873a171d7
Reference: Stripe blog "Scaling your API with rate limiters",
           HelloInterview / SystemDesign rate-limiter breakdowns.

Stripe's coding rate-limiter problem is typically a CODING (not pure system
design) variant: implement a per-user / per-key rate limiter that decides
ALLOW / DENY for each incoming request.

================================================================================
PART 1: Fixed-Window Counter
================================================================================

class FixedWindowLimiter:
    def __init__(self, capacity: int, window_seconds: int): ...
    def allow(self, key: str, ts: float) -> bool: ...

Allow at most `capacity` requests per key in any window of length
`window_seconds` aligned to epoch (window = floor(ts / window_seconds)).

Example (capacity=3, window=10s):
    rl = FixedWindowLimiter(capacity=3, window_seconds=10)
    rl.allow("alice", ts=0)    -> True   (window [0, 10), count 1)
    rl.allow("alice", ts=2)    -> True   (count 2)
    rl.allow("alice", ts=5)    -> True   (count 3)
    rl.allow("alice", ts=7)    -> False  (window full)
    rl.allow("alice", ts=10)   -> True   (new window [10, 20), count 1)
    rl.allow("bob",   ts=10)   -> True   (per-key state, bob is fresh)

================================================================================
PART 2: Sliding-Window Log
================================================================================

class SlidingWindowLimiter:
    def __init__(self, capacity: int, window_seconds: int): ...
    def allow(self, key: str, ts: float) -> bool: ...

Per key, keep a deque of recent timestamps. On allow(ts):
    1. Drop timestamps <= ts - window_seconds.
    2. If len(deque) < capacity, append ts, return True. Else False.

Example (capacity=3, window=10s):
    rl = SlidingWindowLimiter(capacity=3, window_seconds=10)
    rl.allow("alice", ts=0)    -> True   deque=[0]
    rl.allow("alice", ts=2)    -> True   deque=[0,2]
    rl.allow("alice", ts=5)    -> True   deque=[0,2,5]
    rl.allow("alice", ts=7)    -> False  (still 3 in last 10s; 0 not yet expired)
    rl.allow("alice", ts=11)   -> True   ts=0 expired (0 <= 1), deque=[2,5,11]
    rl.allow("alice", ts=12)   -> False  (2 not yet expired; deque has 3)
    rl.allow("alice", ts=13)   -> True   ts=2 expired, deque=[5,11,13]

Notice: unlike fixed-window, no boundary spike at ts=10.

================================================================================
PART 3: Token Bucket (Stripe's actual production algorithm)
================================================================================

class TokenBucketLimiter:
    def __init__(self, capacity: int, refill_per_second: float): ...
    def allow(self, key: str, ts: float, cost: int = 1) -> bool: ...

Per key: track (tokens, last_refill_ts). On allow(ts, cost):
    1. tokens = min(capacity, tokens + (ts - last_refill_ts) * refill_rate)
    2. last_refill_ts = ts
    3. If tokens >= cost: tokens -= cost; return True. Else False.

Example (capacity=5, refill=1 token/sec):
    rl = TokenBucketLimiter(capacity=5, refill_per_second=1.0)
    # Bucket starts full.
    rl.allow("alice", ts=0)    -> True   tokens 5 -> 4
    rl.allow("alice", ts=0)    -> True   tokens 4 -> 3
    rl.allow("alice", ts=0)    -> True   tokens 3 -> 2
    rl.allow("alice", ts=0)    -> True   tokens 2 -> 1
    rl.allow("alice", ts=0)    -> True   tokens 1 -> 0
    rl.allow("alice", ts=0)    -> False  empty
    rl.allow("alice", ts=2)    -> True   refilled 2 tokens; 2 -> 1
    rl.allow("alice", ts=10)   -> True   capped at 5; 5 -> 4
    rl.allow("alice", ts=10, cost=10) -> False  (not enough for cost=10)

Key property: bursts up to `capacity` allowed, sustained rate = refill_rate.

================================================================================
TYPICAL FOLLOW-UPS
================================================================================

- Layered limits per user: per-second AND per-minute AND per-day simultaneously.
- Different limits per endpoint or HTTP method.
- Distributed: multiple processes share state via Redis (atomicity matters).
"""


class FixedWindowLimiter:
    def __init__(self, capacity: int, window_seconds: int):
        pass

    def allow(self, key: str, ts: float) -> bool:
        pass


class SlidingWindowLimiter:
    def __init__(self, capacity: int, window_seconds: int):
        pass

    def allow(self, key: str, ts: float) -> bool:
        pass


class TokenBucketLimiter:
    def __init__(self, capacity: int, refill_per_second: float):
        pass

    def allow(self, key: str, ts: float, cost: int = 1) -> bool:
        pass


if __name__ == "__main__":
    pass
