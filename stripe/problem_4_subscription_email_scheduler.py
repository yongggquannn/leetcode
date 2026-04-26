"""
Subscription Email Scheduler (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/90aba2b5-6b47-4b25-a27b-a3c330d04459
Reconstructed from: oavoservice.com stripe-subscription-notifications-2026 + 1point3acres

Tests event scheduling, timeline sorting, and state propagation.

Stripe Billing needs to send email notifications across each subscriber's
lifecycle. Given a schedule template and a list of user subscriptions, output
all email logs sorted by time.

================================================================================
SCHEDULE TEMPLATE
================================================================================

    Start  -> "Welcome email"
    T-15   -> "Upcoming expiry"     (15 days before End)
    End    -> "Subscription expired"

================================================================================
PART 1: Static Schedule
================================================================================

Input:
    template = [
        {"offset": "start",  "subject": "Welcome email"},
        {"offset": "T-15",   "subject": "Upcoming expiry"},
        {"offset": "end",    "subject": "Subscription expired"},
    ]
    users = [
        {"name": "Alice", "start": 0,  "duration": 30, "plan": "Silver"},
        {"name": "Bob",   "start": 10, "duration": 30, "plan": "Gold"},
    ]

Output: chronologically sorted email logs, each:
    {"time": <int day>, "user": <name>, "subject": <string>, "plan": <plan>}

Expected (Alice end=30, T-15=15; Bob start=10, T-15=25, end=40):
    Day 0:  Alice  Welcome email           (Silver)
    Day 10: Bob    Welcome email           (Gold)
    Day 15: Alice  Upcoming expiry         (Silver)
    Day 25: Bob    Upcoming expiry         (Gold)
    Day 30: Alice  Subscription expired    (Silver)
    Day 40: Bob    Subscription expired    (Gold)

================================================================================
PART 2: Dynamic Plan Changes
================================================================================

Mid-cycle plan modifications. Additional input:
    plan_changes = [
        {"user": "Alice", "time": 5, "new_plan": "Gold"},
    ]

New rules:
- On a plan change, immediately send a "Plan Changed" email at that time.
- All subsequent scheduled emails for that user must reflect the latest plan
  in the subject line / payload.

Recommended approach:
    - Combine all events (scheduled emails + plan changes) into one collection.
    - Sort chronologically.
    - Maintain a user -> current plan map. Update on change events; render
      email events using the current state.
    - O(N log N) time.
"""


def schedule_part1(template: list[dict], users: list[dict]) -> list[dict]:
    pass


def schedule_part2(template: list[dict], users: list[dict],
                   plan_changes: list[dict]) -> list[dict]:
    pass


if __name__ == "__main__":
    pass
