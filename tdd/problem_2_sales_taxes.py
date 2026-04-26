"""
Basic sales tax is 10% on all goods except books, food, and medical products 
(which are exempt). 
Import duty is an additional 5% on all imported goods, no exemptions.

Round tax up to the nearest 0.05 per item (not per line).

Given a shopping basket (list of lines like "1 book at 12.49" or 
"1 imported bottle of perfume at 27.99"), 
print a receipt showing each line, the total taxes, and the total price.

Potential Data Classes:

1. Item
-> original_price
-> is_import
-> final_price

2. ReceiptLine
-> Output is each line, total taxes and total price

Things to take note:
1. Rounding rule happens PER ITEM
-> Use Decimal import and not float

Helper functions of the file:
1. Parse in receipt line
2. Round up based on tax
3. Calculate unit tax

Main function to build receipt
"""

from decimal import Decimal, ROUND_UP
import re
import collections

NEAREST_VAL = Decimal("0.05")
IMPORT_TAX = Decimal("0.05")
BASIC_SALES_TAX = Decimal("0.1")
TAX_POLICY = {"IMPORT": IMPORT_TAX, "BASIC_SALES": BASIC_SALES_TAX}
EXEMPT_WORDS = {"book", "books", "food", "pill", "pills"}
NUMBER_ITEM_DISCOUNT = 3
# Check for regex of each line
LINE_RE = re.compile(r"^(\d+)\s+(.*?)\s+at\s+(\d+\.\d{2})$")


class Item:

    def __init__(self, description, quantity, unit_price):
        self.description = description
        self.qty = quantity
        self.unit_price = unit_price

    def is_imported(self):
        return "imported" in self.description.lower()
    
    def is_exempted(self):
        for word in EXEMPT_WORDS:
            if self.description.contains(word):
                return True
        return False

class ReceiptLine:

    def __init__(self, item, line_total):
        self.item = item
        self.line_total = line_total

class Basket:

    def __init__(self):
        self.item_to_qty = collections.defaultdict(int)
    
    def add_items(self, item, qty):
        self.item_to_qty[item] += qty
        return self.item_to_qty
    
    def _fetch_item_qty(self, item):
        return self.item_to_qty[item]
    
    def qty_of_items_bulk_discount_applied(self, item):
        return self._fetch_item_qty(item) // NUMBER_ITEM_DISCOUNT

def parse_receipt_line(line):
    is_matched = LINE_RE.match(line.strip())
    if not is_matched:
        raise ValueError("Malformed line detected")
    qty, desc, price = is_matched.groups()
    return Item(desc, int(qty), Decimal(price))

def round_up_price(price):
    return (price / NEAREST_VAL).quantize(Decimal("1"), rounding=ROUND_UP) * NEAREST_VAL

# Calculate unit tax
def calculate_unit_tax(item):
    res = Decimal("0")
    if item.is_imported():
        res += TAX_POLICY["IMPORT"]
    if not item.is_exempted():
        res += TAX_POLICY["BASIC_SALES"]
    return round_up_price(item.unit_price * res)

def build_receipt(lines):
    receipt = []
    basket = Basket()
    total_tax = Decimal("0")
    total_price = Decimal("0")
    for l in lines:
        item = parse_receipt_line(l)
        basket.add_items(item, item.qty)
        # Bulk discount
        unit_tax = calculate_unit_tax(item)
        line_total = item.qty * (item.unit_price + unit_tax)
        total_tax += item.qty * unit_tax
        total_price += line_total
        receipt.append(ReceiptLine(item.description, line_total))
    # Process bulk discount
    for i in basket.item_to_qty.keys():
        qty_of_items = basket.qty_of_items_bulk_discount_applied(i)
        total_price -= i.unit_price * qty_of_items
        unit_tax = calculate_unit_tax(i)
        total_tax -= unit_tax * qty_of_items
        price_deducted = i.unit_price * qty_of_items + unit_tax * qty_of_items
        receipt.append(ReceiptLine(f"Discount for {item.description} applied", -price_deducted))

    return receipt, total_tax, total_price
        
"""


"""