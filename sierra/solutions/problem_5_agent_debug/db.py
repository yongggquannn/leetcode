from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Order:
    order_id: str
    customer_email: str
    status: str  # "processing" | "shipped" | "delivered"
    amount_cents: int
    delivered_on: date | None = None
    refunded: bool = False


class OrderDB:
    def __init__(self, orders: list[Order]):
        self.orders = {o.order_id: o for o in orders}
        self.refunds: list[tuple[str, int]] = []
        self.escalations: list[str] = []

    def get(self, order_id: str) -> Order | None:
        return self.orders.get(order_id)

    def has_customer(self, email: str) -> bool:
        return any(o.customer_email == email for o in self.orders.values())


def demo_db(today: date) -> OrderDB:
    ago = lambda days: today - timedelta(days=days)  # noqa: E731
    return OrderDB([
        Order("1001", "sam@example.com", "shipped", 45_00),
        Order("1002", "sam@example.com", "delivered", 40_00, ago(30)),
        Order("1003", "sam@example.com", "delivered", 150_00, ago(5)),
        Order("1004", "sam@example.com", "delivered", 250_00, ago(5)),
        Order("1005", "sam@example.com", "delivered", 20_00, ago(31)),
        Order("2001", "lee@example.com", "delivered", 30_00, ago(3)),
    ])
