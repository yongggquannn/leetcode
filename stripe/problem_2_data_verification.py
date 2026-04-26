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
Check that full_statement_descriptor must satisfy length >= 5 and <= 31 
Violators are NOT VERIFIED even when all fields are present.

================================================================================
PART 3: Blocklist Validation
================================================================================

Add rule: full_statement_descriptor must NOT match any blocklisted generic
descriptor. Blocklist (case-insensitive, exact match):
    {"ONLINE STORE", "ECOMMERCE", "RETAIL", "SHOP", "GENERAL MERCHANDISE"}

Accounts using a blocklisted descriptor are NOT VERIFIED.
"""
import collections
import csv
import io

def verify_part1(csv_input: str) -> dict[str, str]:
    name_to_verification_status = collections.defaultdict(str)
    # Read string input
    reader = csv.DictReader(io.StringIO(csv_input))
    header = reader.fieldnames
    for row in reader:
        name = row['business_name']
        # Handle invalid names
        if not name:
            continue
        # Default will always be verified
        name_to_verification_status[name] = 'VERIFIED'
        for field in header:
            if row[field] == '':
                name_to_verification_status[name] = 'NOT VERIFIED'
                break
    return name_to_verification_status


def verify_part2(csv_input: str) -> dict[str, str]:
    name_to_verification_status = collections.defaultdict(str)
    # Read string input
    reader = csv.DictReader(io.StringIO(csv_input))
    header = reader.fieldnames
    for row in reader:
        name = row['business_name']
        # Handle invalid names
        if not name:
            continue
        descriptor = row['full_statement_descriptor']
        # Part 2
        if not descriptor or not (5 <= len(descriptor) <= 31):
            name_to_verification_status[name] = 'NOT VERIFIED'
            continue
        # Default will always be verified
        name_to_verification_status[name] = 'VERIFIED'
        for field in header:
            if row[field] == '':
                name_to_verification_status[name] = 'NOT VERIFIED'
                break
    return name_to_verification_status

BLOCK_LIST = {"ONLINE STORE", "ECOMMERCE", "RETAIL", "SHOP", "GENERAL MERCHANDISE"}

def check_verification_status(descriptor):
    if not descriptor:
        return 'NOT VERIFIED'
    if not 5 <= len(descriptor) <= 31:
        return 'NOT VERIFIED'
    for word in BLOCK_LIST:
        if descriptor.lower() == word.lower():
            return 'NOT VERIFIED'
    return 'VERIFIED'

def verify_part3(csv_input: str) -> dict[str, str]:
    name_to_verification_status = collections.defaultdict(str)
    # Read string input
    reader = csv.DictReader(io.StringIO(csv_input))
    header = reader.fieldnames
    for row in reader:
        name = row['business_name']
        # Handle invalid names
        if not name:
            continue
        descriptor = row['full_statement_descriptor']
        verification_status_from_descriptor = check_verification_status(descriptor)
        if verification_status_from_descriptor == 'NOT VERIFIED':
            name_to_verification_status[name] = verification_status_from_descriptor
            continue
        # Default will always be verified
        name_to_verification_status[name] = 'VERIFIED'
        for field in header:
            if row[field] == '':
                name_to_verification_status[name] = 'NOT VERIFIED'
                break
    return name_to_verification_status


if __name__ == "__main__":
    # Write test cases to test the different output
    csv_input_1 = (
        "business_name,business_profile_name,full_statement_descriptor,"
        "short_statement_descriptor,url,product_description\n"
        "AcmeCo,Acme,ACME PURCHASE,ACME,https://acme.com,Widgets\n"
        "GapsLLC,Gaps,,GAPS,https://gaps.com,\n"
    )
    assert verify_part1(csv_input_1) == {"AcmeCo": "VERIFIED", "GapsLLC": "NOT VERIFIED"}
    
    csv_input_2 = (
        "business_name,business_profile_name,full_statement_descriptor,"
        "short_statement_descriptor,url,product_description\n"
        "AcmeCo,Acme,ACMEE,ACME,https://acme.com,Widgets\n"
        "GapsLLC,Gaps,,GAPS,https://gaps.com,\n"
    )

    assert verify_part2(csv_input_2) == {"AcmeCo": "VERIFIED", "GapsLLC": "NOT VERIFIED"}

    csv_input_3 = (
        "business_name,business_profile_name,full_statement_descriptor,"
        "short_statement_descriptor,url,product_description\n"
        "AcmeCo,Acme,ACME,ACME,https://acme.com,Widgets\n"
        "GapsLLC,Gaps,online STORE,GAPS,https://gaps.com,\n"
    )
    assert verify_part3(csv_input_3) == {"AcmeCo": "NOT VERIFIED", "GapsLLC": "NOT VERIFIED"}
