"""
Data Verification - Business Account KYC (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/cfcd7f33-5ac5-4465-8d13-235477921cd3
Reconstructed from: 1point3acres KYC Conundrum + linkjob.ai write-ups

Goal: Build a KYC (Know Your Customer) verification system that decides whether
each business account in a CSV is VERIFIED or NOT VERIFIED, under progressively
stricter rules.

Required fields per business:
    business_name, business_profile_name,
    full_statement_descriptor, short_statement_descriptor,
    url, product_description

================================================================================
PART 1: Required Fields Present
================================================================================

Rule: Account is VERIFIED iff every required field is present and non-empty.
      Otherwise NOT VERIFIED.

Input:  CSV string (header + N rows).
Output: List/dict mapping business_name -> "VERIFIED" or "NOT VERIFIED",
        in input order.

Example:
    csv = (
        "business_name,business_profile_name,full_statement_descriptor,"
        "short_statement_descriptor,url,product_description\\n"
        "AcmeCo,Acme,ACME PURCHASE,ACME,https://acme.com,Widgets\\n"
        "GapsLLC,Gaps,,GAPS,https://gaps.com,\\n"
    )
    verify_part1(csv) == {"AcmeCo": "VERIFIED", "GapsLLC": "NOT VERIFIED"}

================================================================================
PART 2: Descriptor Length Validation
================================================================================

Add rule: full_statement_descriptor must be 5..31 characters (inclusive).
Violators are NOT VERIFIED even when all fields are present.

================================================================================
PART 3: Blocklist Validation
================================================================================

Add rule: full_statement_descriptor must NOT match any blocklisted generic
descriptor. Blocklist (case-insensitive, exact match):
    {"ONLINE STORE", "ECOMMERCE", "RETAIL", "SHOP", "GENERAL MERCHANDISE"}

Accounts using a blocklisted descriptor are NOT VERIFIED.
"""


def verify_part1(csv_input: str) -> dict[str, str]:
    pass


def verify_part2(csv_input: str) -> dict[str, str]:
    pass


def verify_part3(csv_input: str) -> dict[str, str]:
    pass


if __name__ == "__main__":
    pass
