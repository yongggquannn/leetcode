"""
Subscription Cancellation Flow (Sierra)
Reported: "Design an agentic service for a given use case, such as a
subscription-cancellation flow." Sierra builds customer-service agents, so the
coding version is a guard-railed conversation state machine.
Source: https://www.tryexponent.com/guides/sierra-agent-engineer-interview

Suggested time: 50 min.    Run: python sierra/run.py 8

flow = CancellationFlow(Subscription("sam@example.com", "annual", 120_000, 100))
flow.handle({"type": "start"}) -> str   (the agent's reply; tests only check state)

States: START, VERIFY, REASON, OFFER, CONFIRM, and terminal CANCELLED,
RETAINED, ESCALATED.

================================================================================
PART 1: Happy path
================================================================================

    START   --start-->                                     VERIFY
    VERIFY  --verify {email}--> (matches, case/space-insensitive) REASON
                                (no match: stay in VERIFY)
    REASON  --reason {reason}-->                           CONFIRM   (Part 1)
    CONFIRM --confirm-->                                   CANCELLED
    CONFIRM --abort-->                                     RETAINED

================================================================================
PART 2: Retention offers
================================================================================

After REASON, go to OFFER if the reason has an offer, otherwise CONFIRM:

    "too_expensive"   -> {"kind": "discount", "percent": 50, "months": 3}
    "not_using"       -> {"kind": "pause", "months": 2}
    "missing_feature", "other" -> no offer

    OFFER --accept--> RETAINED   (flow.applied_offer = the offer)
    OFFER --decline--> CONFIRM

From any non-terminal state, {"type": "human"} -> ESCALATED.

================================================================================
PART 3: Guardrails + refunds
================================================================================

- Invalid input never crashes and never changes state; reply with a hint.
  Invalid = event type not allowed in this state, unknown reason value, or a
  failed verification.
- The 3rd invalid input in a session -> ESCALATED.
- Any event in a terminal state -> polite "closed" reply, nothing changes.
- On CANCELLED set flow.refund_cents (None until then):
    monthly                     -> 0
    annual, days_into_term <= 30 -> full price_cents
    annual, otherwise           -> price_cents * (365 - days_into_term) // 365, min 0

================================================================================
PART 4: Audit log + resumable sessions
================================================================================

- flow.audit: list of (from_state, to_state, event_type) for every state change
  (no entry when state doesn't change).
- flow.to_dict() -> JSON-serialisable dict; CancellationFlow.from_dict(sub, d)
  restores state, invalid-input count, pending offer and audit, so a dropped
  conversation can resume on another server.

================================================================================
FOLLOW-UPS
================================================================================

- Where does the LLM fit? (classify free text -> event; the state machine
  stays deterministic and enforces policy)
- How do you stop the model from promising an offer the policy doesn't allow?
- Offers per region / A-B test: where does that config live?
- Metrics: retention rate, escalation rate, drop-off per state.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Subscription:
    customer_email: str
    plan: str  # "monthly" | "annual"
    price_cents: int  # per term
    days_into_term: int


class CancellationFlow:
    def __init__(self, sub: Subscription) -> None:
        self.sub = sub
        self.state = "START"
        self.applied_offer: dict | None = None
        self.refund_cents: int | None = None
        self.audit: list[tuple[str, str, str]] = []

    def handle(self, event: dict) -> str:
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError

    @classmethod
    def from_dict(cls, sub: Subscription, data: dict) -> "CancellationFlow":
        raise NotImplementedError
