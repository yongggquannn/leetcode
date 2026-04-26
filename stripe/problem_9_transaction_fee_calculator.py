"""
Transaction Fee Calculator (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/0d112b32-cb43-45d8-be8b-e22bc4c9fa75
Reconstructed from: prachub.com "compute-transaction-fees-from-a-csv-string"

Compute total fees per user from a CSV transaction log. Use HALF-UP rounding
to nearest cent before aggregating.

================================================================================
PART 1: Basic Fees by Status + Provider
================================================================================

Input CSV header: "user,status,payment_provider,amount"
amount is a decimal dollars value (e.g. "100.00").

Fee rules:
    payment_completed | payment_failed | payment_pending:
        fee = amount * provider_rate + $0.30
        provider_rate: card 2.9%, bank_transfer 1.0%, wallet 1.5%
    refund_completed:  fee = $0
    dispute_lost:      fee = $15.00 flat
    dispute_won:       fee = $0

Output: dict {user: total_fee_in_cents}

Example:
    csv = (
        "user,status,payment_provider,amount\\n"
        "alice,payment_completed,card,100.00\\n"
        "bob,payment_failed,bank_transfer,50.00\\n"
        "alice,refund_completed,card,20.00\\n"
        "bob,dispute_lost,wallet,80.00"
    )
    compute_fees_part1(csv) == {"alice": 320, "bob": 1580}

Edge cases:
    - Whitespace and blank lines must be tolerated.
    - Half-up rounding to nearest cent BEFORE summing.
    - Return all users seen, even if total fee is 0.
    - Empty input -> {}.

================================================================================
PART 2: Country-Specific Rates + Currency Conversion
================================================================================

Input CSV header: "user,status,payment_provider,buyer_country,currency,amount"
Plus an exchange_rates dict: {currency_code: rate_to_USD}.

Process: convert each amount to USD first:
    converted_usd = amount * exchange_rates[currency]

For payment_completed only (country-specific rates):
    card:           US/CA 2.9%, GB 2.5%, DE/FR/AT 2.3%, others 3.1%
    bank_transfer:  US/CA 1.2%, GB 1.1%, DE/FR/AT 1.0%, others 1.4%
    wallet:         all countries 1.8%
    fee = converted_usd * rate + $0.30

Other statuses: same rules as Part 1, applied on the converted USD amount.

Example:
    compute_fees_part2(
        "user,status,payment_provider,buyer_country,currency,amount\\n"
        "alice,payment_completed,card,DE,EUR,100.00\\n"
        "bob,payment_pending,bank_transfer,US,USD,50.00\\n"
        "alice,dispute_lost,wallet,GB,GBP,80.00",
        {"USD": 1.0, "EUR": 1.10, "GBP": 1.25},
    ) == {"alice": 1783, "bob": 80}
"""


def compute_fees_part1(csv_input: str) -> dict[str, int]:
    pass


def compute_fees_part2(csv_input: str, exchange_rates: dict[str, float]) -> dict[str, int]:
    pass


if __name__ == "__main__":
    pass
