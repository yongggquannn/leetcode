"""
Payment Invoice Reconciliation (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/1fbd1219-4a22-4925-9555-fc2bb2cd24b2
Reconstructed from: 1point3acres post 7379560 + interviewexperiences.in

Match standalone payments to open invoices for a customer. Each payment carries
a memo line that names the invoice it pays off.

================================================================================
INPUT FORMATS
================================================================================

Payment string (CSV):
    "<payment_id>,<amount_cents>,Paying off: <invoice_id>"
    e.g. "payment5,1000,Paying off: invoiceC"

Invoice string (CSV):
    "<invoice_id>,<due_date YYYY-MM-DD>,<amount_due_cents>"
    e.g. "invoiceC,2023-01-30,1000"

Amounts are integer minor units ($1.00 = 100).

================================================================================
PART 1: Single Payment Lookup
================================================================================

Function: f(payment: str, invoices: list[str]) -> str

Parse the payment, find the invoice named in the memo, return a formatted
string describing the reconciliation, e.g.:
    "payment5 pays off 1000 for invoiceC due on 2023-01-30"

Example:
    f("payment5,1000,Paying off: invoiceC",
      ["invoiceA,2024-01-01,100",
       "invoiceB,2024-02-01,200",
       "invoiceC,2023-01-30,1000"])
    == "payment5 pays off 1000 for invoiceC due on 2023-01-30"

================================================================================
PART 2 / PART 3 (typical follow-ups, exact wording paywalled)
================================================================================

Likely extensions seen in the wild:
- Multiple payments → multiple invoices; handle missing/unknown invoice IDs.
- Partial payments: amount may be less than invoice amount; track remaining
  balance per invoice across many payments.
- Overpayments / split payments across several invoices.
- Sort output by invoice due date or by payment processing order.

Write your own test cases (Stripe expects you to generate at least 2-3).
"""


def reconcile_part1(payment: str, invoices: list[str]) -> str:
    pass


def reconcile_part2(payments: list[str], invoices: list[str]):
    pass


def reconcile_part3(payments: list[str], invoices: list[str]):
    pass


if __name__ == "__main__":
    pass
