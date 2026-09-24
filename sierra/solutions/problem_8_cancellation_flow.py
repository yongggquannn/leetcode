"""Reference solution - problem 8."""
from __future__ import annotations

from typing import Callable

from problem_8_cancellation_flow import Subscription

TERMINAL = {"CANCELLED", "RETAINED", "ESCALATED"}
MAX_INVALID = 3
FULL_REFUND_DAYS = 30
OFFERS: dict[str, dict | None] = {
    "too_expensive": {"kind": "discount", "percent": 50, "months": 3},
    "not_using": {"kind": "pause", "months": 2},
    "missing_feature": None,
    "other": None,
}
HINTS = {
    "START": "Say 'start' to begin.",
    "VERIFY": "Please confirm the email on your account.",
    "REASON": f"Why are you cancelling? One of: {', '.join(OFFERS)}.",
    "OFFER": "Would you like to accept or decline this offer?",
    "CONFIRM": "Please confirm the cancellation, or abort to keep your plan.",
}


class Invalid(Exception):
    """Input that doesn't fit the current state; counted toward escalation."""


class CancellationFlow:
    def __init__(self, sub: Subscription) -> None:
        self.sub = sub
        self.state = "START"
        self.applied_offer: dict | None = None
        self.refund_cents: int | None = None
        self.audit: list[tuple[str, str, str]] = []
        self._invalid = 0
        self._pending_offer: dict | None = None
        # (state, event type) -> handler returning (next_state, reply)
        self._transitions: dict[tuple[str, str], Callable[[dict], tuple[str, str]]] = {
            ("START", "start"): lambda e: ("VERIFY", HINTS["VERIFY"]),
            ("VERIFY", "verify"): self._on_verify,
            ("REASON", "reason"): self._on_reason,
            ("OFFER", "accept"): self._on_accept,
            ("OFFER", "decline"): lambda e: ("CONFIRM", HINTS["CONFIRM"]),
            ("CONFIRM", "confirm"): self._on_confirm,
            ("CONFIRM", "abort"): lambda e: ("RETAINED", "No problem, your plan stays active."),
        }

    def handle(self, event: dict) -> str:
        if self.state in TERMINAL:
            return "This conversation is closed. Start a new one if you need more help."
        kind = event.get("type", "")
        if kind == "human":
            return self._move("ESCALATED", kind, "Connecting you with a specialist now.")
        handler = self._transitions.get((self.state, kind))
        try:
            if handler is None:
                raise Invalid(HINTS[self.state])
            next_state, reply = handler(event)
        except Invalid as err:
            self._invalid += 1
            if self._invalid >= MAX_INVALID:
                return self._move("ESCALATED", kind, "Let me connect you with a specialist.")
            return str(err)
        return self._move(next_state, kind, reply)

    def _move(self, next_state: str, kind: str, reply: str) -> str:
        if next_state != self.state:
            self.audit.append((self.state, next_state, kind))
            self.state = next_state
        return reply

    def _on_verify(self, event: dict) -> tuple[str, str]:
        given = str(event.get("email", "")).strip().lower()
        if given != self.sub.customer_email.strip().lower():
            raise Invalid("That email doesn't match our records. " + HINTS["VERIFY"])
        return "REASON", HINTS["REASON"]

    def _on_reason(self, event: dict) -> tuple[str, str]:
        reason = event.get("reason")
        if reason not in OFFERS:
            raise Invalid(HINTS["REASON"])
        self._pending_offer = OFFERS[reason]
        if self._pending_offer is None:
            return "CONFIRM", HINTS["CONFIRM"]
        return "OFFER", f"Before you go, we can offer: {self._pending_offer}. Accept or decline?"

    def _on_accept(self, event: dict) -> tuple[str, str]:
        self.applied_offer = self._pending_offer
        return "RETAINED", "Great, the offer is applied."

    def _on_confirm(self, event: dict) -> tuple[str, str]:
        self.refund_cents = self._refund()
        return "CANCELLED", f"Your subscription is cancelled. Refund: {self.refund_cents / 100:.2f}."

    def _refund(self) -> int:
        sub = self.sub
        if sub.plan != "annual":
            return 0
        if sub.days_into_term <= FULL_REFUND_DAYS:
            return sub.price_cents
        return max(0, sub.price_cents * (365 - sub.days_into_term) // 365)

    def to_dict(self) -> dict:
        return {
            "state": self.state,
            "invalid": self._invalid,
            "pending_offer": self._pending_offer,
            "applied_offer": self.applied_offer,
            "refund_cents": self.refund_cents,
            "audit": [list(entry) for entry in self.audit],
        }

    @classmethod
    def from_dict(cls, sub: Subscription, data: dict) -> "CancellationFlow":
        flow = cls(sub)
        flow.state = data["state"]
        flow._invalid = data["invalid"]
        flow._pending_offer = data["pending_offer"]
        flow.applied_offer = data["applied_offer"]
        flow.refund_cents = data["refund_cents"]
        flow.audit = [tuple(entry) for entry in data["audit"]]
        return flow
