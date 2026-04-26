"""
Shipping Cost Calculator (DarkInterview)
Source: https://darkinterview.com/collections/t4y7u1i8/questions/2a15f417-c9bb-4ab2-b606-24568b9f30c7

Build a shipping cost calculation system for e-commerce that computes total
shipping based on country and product type across three progressive complexity
levels.

Function signature (all parts):
    def calculate_shipping_cost(order, shipping_cost) -> int

================================================================================
PART 1: Fixed Rate Shipping
================================================================================

Input:
    order_us = {
        "country": "US",
        "items": [
            {"product": "mouse",  "quantity": 20},
            {"product": "laptop", "quantity": 5},
        ],
    }

    shipping_cost = {
        "US": [
            {"product": "mouse",  "cost": 550},
            {"product": "laptop", "cost": 1000},
        ],
        "CA": [
            {"product": "mouse",  "cost": 750},
            {"product": "laptop", "cost": 1100},
        ],
    }

Expected:
    calculate_shipping_cost(order_us, shipping_cost) == 16000
        # (20 * 550) + (5 * 1000) = 11,000 + 5,000
    calculate_shipping_cost(order_ca, shipping_cost) == 20500
        # (20 * 750) + (5 * 1100) = 15,000 + 5,500

Requirements:
    - Support multiple products per order
    - Handle country-specific pricing
    - Return total as integer

================================================================================
PART 2: Tiered Incremental Pricing
================================================================================

Input:
    shipping_cost = {
        "US": [
            {
                "product": "mouse",
                "costs": [
                    {"minQuantity": 0, "maxQuantity": None, "cost": 550},
                ],
            },
            {
                "product": "laptop",
                "costs": [
                    {"minQuantity": 0, "maxQuantity": 2,    "cost": 1000},
                    {"minQuantity": 3, "maxQuantity": None, "cost": 900},
                ],
            },
        ],
        # CA mirrors with mouse=750, laptop tiers (0,2)=1100 and (3,None)=1000
    }

Expected:
    calculate_shipping_cost(order_us, shipping_cost) == 15700
        # Mouse:  20 * 550 = 11,000
        # Laptop: (2 * 1000) + (3 * 900) = 2,000 + 2,700 = 4,700
        # Total:  15,700
    calculate_shipping_cost(order_ca, shipping_cost) == 20200
        # Mouse:  20 * 750 = 15,000
        # Laptop: (2 * 1100) + (3 * 1000) = 2,200 + 3,000 = 5,200
        # Total:  20,200

Requirements:
    - Process quantity tiers sequentially from lowest to highest
    - maxQuantity of None indicates unlimited quantity
    - Quantity ranges are half-open intervals: [minQuantity, maxQuantity)
    - Sum costs across all applicable tiers

================================================================================
PART 3: Mixed Pricing Models (Fixed + Incremental)
================================================================================

Input:
    shipping_cost = {
        "US": [
            {
                "product": "mouse",
                "costs": [
                    {"type": "incremental", "minQuantity": 0, "maxQuantity": None, "cost": 550},
                ],
            },
            {
                "product": "laptop",
                "costs": [
                    {"type": "fixed",       "minQuantity": 0, "maxQuantity": 2,    "cost": 1000},
                    {"type": "incremental", "minQuantity": 3, "maxQuantity": None, "cost": 900},
                ],
            },
        ],
        # CA mirrors with mouse incremental=750, laptop fixed=1100, incremental=1000
    }

Expected:
    calculate_shipping_cost(order_us, shipping_cost) == 14700
        # Mouse:  20 * 550 = 11,000 (incremental)
        # Laptop: 1,000 (fixed) + (3 * 900) = 1,000 + 2,700 = 3,700
        # Total:  14,700
    calculate_shipping_cost(order_ca, shipping_cost) == 19100
        # Mouse:  20 * 750 = 15,000 (incremental)
        # Laptop: 1,100 (fixed) + (3 * 1000) = 1,100 + 3,000 = 4,100
        # Total:  19,100

Requirements:
    - Support "fixed" and "incremental" pricing types
    - Fixed: apply cost directly regardless of quantity in that tier
    - Incremental: multiply quantity in that tier by cost
    - Handle alternating pricing patterns
"""

import collections
# ---------- Part 1: Fixed Rate Shipping ----------

def calculate_shipping_cost_part1(order: dict, shipping_cost: dict) -> int:
    order_country = order["country"]
    product_to_unit_cost = collections.defaultdict(int)

    shipping_details = shipping_cost[order_country]
    for detail in shipping_details:
        product = detail["product"]
        unit_cost = detail["cost"]
        product_to_unit_cost[product] = unit_cost
    
    item_details = order["items"]
    total = 0
    for item in item_details:
        curr_product = item["product"]
        curr_qty = item["quantity"]
        unit_cost = product_to_unit_cost[curr_product]
        total += unit_cost * curr_qty
    return total

'''
- fetch the country
- build a map of product_to_unitCost 
- iterate through each item
- determine quantity and product
- increment based on qty and unitCost (retrieved from map)
- return total

order_country = order["country"]
'''


# ---------- Part 2: Tiered Incremental Pricing ----------
"""
Assumption: costs is sorted by minQuantity
"""
def calculate_required_cost(product_to_cost_details, curr_product, curr_qty):
    res = 0
    cost_details = product_to_cost_details[curr_product]
    for detail in cost_details:
        unit_cost = detail["cost"]
        min_qty, max_qty = detail["minQuantity"], detail["maxQuantity"]
        # Do not take into account no qty for calculation
        if min_qty == 0:
            min_qty = 1
        if max_qty is not None and curr_qty >= max_qty:
            res += (max_qty - min_qty + 1) * unit_cost
            if curr_qty == max_qty:
                break
        else:
            res += (curr_qty - min_qty + 1) * unit_cost
            break
    return res

def calculate_shipping_cost_part2(order: dict, shipping_cost: dict) -> int:
    order_country = order["country"]
    product_to_cost_details = collections.defaultdict(list)

    shipping_details = shipping_cost[order_country]
    for detail in shipping_details:
        product = detail["product"]
        cost_details = detail["costs"]
        product_to_cost_details[product] = cost_details
    
    item_details = order["items"]
    total = 0
    for item in item_details:
        curr_product = item["product"]
        curr_qty = item["quantity"]
        required_cost = calculate_required_cost(product_to_cost_details, curr_product, curr_qty)
        total += required_cost
    return total

'''
- fetch the country
- build a map of product_to_unitCost
- iterate through each item
- determine quantity and product
- calculation logic (helper function)
-> If current quanity is more than or eq to maxQty => price increment by (maxQty - minQty) * cost
-> Else, (currQty - minQty) * cost

    #     "US": [
    #         {"product": "mouse",  "costs": [{"minQuantity": 0, "maxQuantity": None, "cost": 550}]},
    #         {"product": "laptop", "costs": [
    #             {"minQuantity": 0, "maxQuantity": 2,    "cost": 1000},
    #             {"minQuantity": 3, "maxQuantity": 5, "cost": 900},
                  {"minQuanitity": 6, "maxQuanitity": None, "cost": 800}
    #         ]},
    #     ],



- return total

order_country = order["country"]
'''

def calculate_required_cost_model(product_to_cost_details, curr_product, curr_qty):
    res = 0
    cost_details = product_to_cost_details[curr_product]
    for detail in cost_details:
        type = detail["type"]
        unit_cost = detail["cost"]
        if type == "fixed":
            res += unit_cost
            continue
        min_qty, max_qty = detail["minQuantity"], detail["maxQuantity"]
        # Do not take into account no qty for calculation
        if min_qty == 0:
            min_qty = 1
        if max_qty is not None and curr_qty >= max_qty:
            res += (max_qty - min_qty + 1) * unit_cost
            if curr_qty == max_qty:
                break
        else:
            res += (curr_qty - min_qty + 1) * unit_cost
            break
    return res

# ---------- Part 3: Mixed Pricing Models (Fixed + Incremental) ----------

def calculate_shipping_cost_part3(order: dict, shipping_cost: dict) -> int:
    order_country = order["country"]
    product_to_cost_details = collections.defaultdict(list)

    shipping_details = shipping_cost[order_country]
    for detail in shipping_details:
        product = detail["product"]
        cost_details = detail["costs"]
        product_to_cost_details[product] = cost_details
    
    item_details = order["items"]
    total = 0
    for item in item_details:
        curr_product = item["product"]
        curr_qty = item["quantity"]
        required_cost = calculate_required_cost_model(product_to_cost_details, curr_product, curr_qty)
        total += required_cost
    return total


'''
Input:
    shipping_cost = {
        "US": [
            {
                "product": "mouse",
                "costs": [
                    {"type": "incremental", "minQuantity": 0, "maxQuantity": None, "cost": 550},
                ],
            },
            {
                "product": "laptop",
                "costs": [
                    {"type": "fixed",       "minQuantity": 0, "maxQuantity": 2,    "cost": 1000},
                    {"type": "incremental", "minQuantity": 3, "maxQuantity": None, "cost": 900},
                ],
            },
        ],
        # CA mirrors with mouse incremental=750, laptop fixed=1100, incremental=1000
'''

if __name__ == "__main__":
    # Uncomment the block for the part you're working on to sanity-check.

    # ----- Part 1 sample data -----
    order_us = {
        "country": "US",
        "items": [
            {"product": "mouse",  "quantity": 20},
            {"product": "laptop", "quantity": 5},
        ],
    }
    order_ca = {**order_us, "country": "CA"}
    shipping_cost_p1 = {
        "US": [
            {"product": "mouse",  "cost": 550},
            {"product": "laptop", "cost": 1000},
        ],
        "CA": [
            {"product": "mouse",  "cost": 750},
            {"product": "laptop", "cost": 1100},
        ],
    }
    assert calculate_shipping_cost_part1(order_us, shipping_cost_p1) == 16000
    assert calculate_shipping_cost_part1(order_ca, shipping_cost_p1) == 20500

    # ----- Part 2 sample data -----
    shipping_cost_p2 = {
        "US": [
            {"product": "mouse",  "costs": [{"minQuantity": 0, "maxQuantity": None, "cost": 550}]},
            {"product": "laptop", "costs": [
                {"minQuantity": 0, "maxQuantity": 2,    "cost": 1000},
                {"minQuantity": 3, "maxQuantity": None, "cost": 900},
            ]},
        ],
        "CA": [
            {"product": "mouse",  "costs": [{"minQuantity": 0, "maxQuantity": None, "cost": 750}]},
            {"product": "laptop", "costs": [
                {"minQuantity": 0, "maxQuantity": 2,    "cost": 1100},
                {"minQuantity": 3, "maxQuantity": None, "cost": 1000},
            ]},
        ],
    }
    assert calculate_shipping_cost_part2(order_us, shipping_cost_p2) == 15700
    assert calculate_shipping_cost_part2(order_ca, shipping_cost_p2) == 20200

    # ----- Part 3 sample data -----
    shipping_cost_p3 = {
        "US": [
            {"product": "mouse",  "costs": [
                {"type": "incremental", "minQuantity": 0, "maxQuantity": None, "cost": 550},
            ]},
            {"product": "laptop", "costs": [
                {"type": "fixed",       "minQuantity": 0, "maxQuantity": 2,    "cost": 1000},
                {"type": "incremental", "minQuantity": 3, "maxQuantity": None, "cost": 900},
            ]},
        ],
        "CA": [
            {"product": "mouse",  "costs": [
                {"type": "incremental", "minQuantity": 0, "maxQuantity": None, "cost": 750},
            ]},
            {"product": "laptop", "costs": [
                {"type": "fixed",       "minQuantity": 0, "maxQuantity": 2,    "cost": 1100},
                {"type": "incremental", "minQuantity": 3, "maxQuantity": None, "cost": 1000},
            ]},
        ],
    }
    assert calculate_shipping_cost_part3(order_us, shipping_cost_p3) == 14700
    assert calculate_shipping_cost_part3(order_ca, shipping_cost_p3) == 19100
