"""
HTTP Request Language Preference (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/c86912d8-30d3-4585-b791-444a4d157200
Reconstructed from: Glassdoor "Parsing the HTTP Accept-Language header" + linkjob.ai

Parse the HTTP Accept-Language header. Given the header value and the set of
languages your service supports, return the supported languages in descending
order of the requester's preference.

================================================================================
PART 1: Order-based Preference
================================================================================

Function: parse_accept_language(header: str, supported: list[str]) -> list[str]

Header is a comma-separated list of language tags, e.g. "en-US, fr-CA, fr-FR".
Earlier = more preferred. Return the subset of `supported` that appears in the
header, in the header's order.

Examples:
    parse_accept_language("en-US, fr-CA, fr-FR", ["fr-FR", "en-US"])
        == ["en-US", "fr-FR"]
    parse_accept_language("fr-CA, fr-FR",         ["en-US", "fr-FR"])
        == ["fr-FR"]
    parse_accept_language("en-US",                ["en-US", "fr-CA"])
        == ["en-US"]

================================================================================
PART 2: q-factors (Quality Values)
================================================================================

Header entries can carry an explicit numeric weight ("q-factor") between 0 and
1, e.g. "en-US;q=0.9, fr-FR;q=0.8, de;q=0".

Rules:
- Default q is 1.0 when omitted.
- q=0 means NOT acceptable - exclude even if supported.
- Sort the result by q descending. Ties broken by header order.

Examples:
    parse_accept_language("en-US;q=0.9, fr-FR;q=1.0, de;q=0",
                          ["en-US", "fr-FR", "de"])
        == ["fr-FR", "en-US"]

================================================================================
PART 3 (typical follow-up - paywalled, expect one of)
================================================================================

- Wildcard "*" entries acting as a catch-all preference.
- Language-prefix matching ("en" matches "en-US" and "en-GB").
- Multiple supported tags share the same q-factor: stable ordering.
- Reject malformed header entries.
"""


def parse_accept_language_part1(header: str, supported: list[str]) -> list[str]:
    pass


def parse_accept_language_part2(header: str, supported: list[str]) -> list[str]:
    pass


def parse_accept_language_part3(header: str, supported: list[str]) -> list[str]:
    pass


if __name__ == "__main__":
    pass
