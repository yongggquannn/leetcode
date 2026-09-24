"""Deterministic stand-in for the model. Treat as correct - the bugs are elsewhere."""
from __future__ import annotations

import re
from dataclasses import dataclass

from .state import Message

ORDER_RE = re.compile(r"#(\d+)")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")


@dataclass
class ToolCall:
    name: str
    args: dict


@dataclass
class Reply:
    text: str


class FakeLLM:
    def decide(self, history: list[Message]) -> ToolCall | Reply:
        last = history[-1]
        if last.role == "tool":
            return Reply(self._summarise(last))
        text, lower = last.content, last.content.lower()
        if "human" in lower:
            return ToolCall("escalate_to_human", {"reason": "customer_request"})
        if email := EMAIL_RE.search(text):
            return ToolCall("verify_identity", {"email": email.group(0)})
        order = ORDER_RE.search(text)
        if order and "refund" in lower:
            return ToolCall("issue_refund", {"order_id": order.group(1)})
        if order:
            return ToolCall("lookup_order", {"order_id": order.group(1)})
        return Reply("Hi! I can help with order status and refunds. What's your order number?")

    @staticmethod
    def _summarise(msg: Message) -> str:
        d = msg.data or {}
        err = d.get("error")
        if err == "INELIGIBLE":
            return f"This refund needs a specialist's review ({d['reason']}). I've escalated your case."
        if d.get("escalated"):
            return "I've connected you with a human agent who will follow up shortly."
        if err == "AUTH_REQUIRED":
            return "Please verify your identity first by sharing the email on your account."
        if err == "NOT_FOUND":
            return "I couldn't find that order on your account."
        if err == "VERIFICATION_FAILED":
            return "That email doesn't match our records. Please try again."
        if err == "ALREADY_REFUNDED":
            return "That order has already been refunded."
        if err:
            return "Something went wrong on our side. Please try again."
        if msg.tool_name == "verify_identity":
            return "Thanks, you're verified. How can I help?"
        if msg.tool_name == "lookup_order":
            return f"Order #{d['order_id']} is {d['status']}."
        if msg.tool_name == "issue_refund":
            return f"Done - I've refunded ${d['amount_cents'] / 100:.2f} for order #{d['order_id']}."
        return "Done."
