"""
Currency Exchange Rate Converter (Stripe)
Source (paywalled): https://darkinterview.com/collections/t4y7u1i8/questions/95228763-4222-41ce-a073-8f867227280f
Reconstructed from: bigtechexperts.com Q1 Stripe Currency Conversion Problem

Model currencies as nodes and exchange rates as bidirectional weighted edges.
Three progressive parts.

Input format throughout: string of rates "C1:C2:rate,C3:C4:rate,..."
Rates are bidirectional: "USD:CAD:1.3" implies CAD->USD = 1/1.3.

================================================================================
PART 1: Direct Conversion (~10 min)
================================================================================

Convert amount only if a direct edge exists between from_currency and
to_currency. Return -1 if no direct rate.

Function:
    convert_currency(input_str: str, from_currency: str,
                     to_currency: str, amount: float) -> float

Examples:
    convert_currency("USD:CAD:1.3", "USD", "CAD", 100.0) == 130.0
    convert_currency("USD:CAD:1.3,EUR:USD:1.1", "USD", "GBP", 100.0) == -1

================================================================================
PART 2: Any Multi-hop Path (~20 min)
================================================================================

Allow conversion through intermediate currencies. Return route + rate +
converted_value. Return None / -1 if unreachable.

Function:
    find_conversion_path(input_str: str, from_currency: str,
                         to_currency: str, amount: float) -> dict

Expected return:
    {
        "route": "USD -> CAD -> AUD",
        "rate": 1.76,
        "converted_value": 176.0,
    }

================================================================================
PART 3: Shortest Path (~25 min)
================================================================================

Find the path with the MINIMUM number of hops (BFS), guaranteeing the fewest
intermediate conversions.

Function:
    find_shortest_conversion_path(input_str: str, from_currency: str,
                                  to_currency: str, amount: float) -> dict

Same return shape as Part 2.
"""


def convert_currency(input_str: str, from_currency: str,
                     to_currency: str, amount: float) -> float:
    pass


def find_conversion_path(input_str: str, from_currency: str,
                         to_currency: str, amount: float) -> dict:
    pass


def find_shortest_conversion_path(input_str: str, from_currency: str,
                                  to_currency: str, amount: float) -> dict:
    pass


if __name__ == "__main__":
    pass
