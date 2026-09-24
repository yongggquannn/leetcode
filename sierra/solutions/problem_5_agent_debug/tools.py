from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Callable

from .db import Order, OrderDB
from .state import ConversationState

REFUND_WINDOW_DAYS = 30
AUTO_REFUND_LIMIT_CENTS = 200_00  # Fix 4: same unit as Order.amount_cents
MAX_FAILED_VERIFICATIONS = 2


@dataclass
class ToolContext:
    db: OrderDB
    state: ConversationState
    today: date


@dataclass(frozen=True)
class Tool:
    fn: Callable[..., dict]
    requires_auth: bool


def _owned_order(ctx: ToolContext, order_id: str) -> Order | None:
    order = ctx.db.get(order_id)
    if order is None or order.customer_email != ctx.state.verified_email:
        return None
    return order


def escalate_to_human(ctx: ToolContext, reason: str) -> dict:
    ctx.state.escalated = True
    ctx.db.escalations.append(reason)
    return {"ok": True, "escalated": True}


def verify_identity(ctx: ToolContext, email: str) -> dict:
    email = email.strip().lower()
    if ctx.db.has_customer(email):
        ctx.state.verified_email = email
        return {"ok": True}
    ctx.state.failed_verifications += 1  # Fix 7: persist the count across turns
    if ctx.state.failed_verifications >= MAX_FAILED_VERIFICATIONS:
        return escalate_to_human(ctx, "verification_failed")
    return {"error": "VERIFICATION_FAILED"}


def lookup_order(ctx: ToolContext, order_id: str) -> dict:
    order = _owned_order(ctx, order_id)  # Fix 3: only the verified customer's orders
    if order is None:
        return {"error": "NOT_FOUND"}
    return {"order_id": order.order_id, "status": order.status}


def _ineligible_reason(order: Order, today: date) -> str | None:
    if order.status != "delivered" or order.delivered_on is None:
        return "not_delivered"
    if (today - order.delivered_on).days > REFUND_WINDOW_DAYS:  # Fix 5: day 30 is inside
        return "outside_window"
    if order.amount_cents > AUTO_REFUND_LIMIT_CENTS:
        return "over_limit"
    return None


def issue_refund(ctx: ToolContext, order_id: str) -> dict:
    order = _owned_order(ctx, order_id)
    if order is None:
        return {"error": "NOT_FOUND"}
    if order.refunded:  # Fix 6: refunds must be idempotent
        return {"error": "ALREADY_REFUNDED"}
    reason = _ineligible_reason(order, ctx.today)
    if reason:
        escalate_to_human(ctx, reason)
        return {"error": "INELIGIBLE", "reason": reason, "escalated": True}
    order.refunded = True
    ctx.db.refunds.append((order.order_id, order.amount_cents))
    return {"ok": True, "order_id": order.order_id, "amount_cents": order.amount_cents}


TOOLS: dict[str, Tool] = {
    "verify_identity": Tool(verify_identity, requires_auth=False),
    "lookup_order": Tool(lookup_order, requires_auth=True),
    "issue_refund": Tool(issue_refund, requires_auth=True),
    "escalate_to_human": Tool(escalate_to_human, requires_auth=False),
}
