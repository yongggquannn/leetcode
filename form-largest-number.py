from typing import List
from functools import cmp_to_key

def compare_val(a, b):
    updated_a = a
    updated_b = b
    min_length = min(len(a), len(b))
    if len(a) != min_length:
        updated_a = a[-min_length:]
    if len(b) != min_length:
        updated_b = b[-min_length:]
    if updated_a > updated_b:
        return -1
    else:
        return 1


def form_largest_number(nums: List[int]) -> str:
    nums = [str(num) for num in nums]
    sorted_nums = sorted(nums, key=cmp_to_key(compare_val))
    res = "".join(sorted_nums)
    return res

nums = [8, 80, 89]
form_largest_number(nums)
"""
Example 1:

Input: [10,2]
Output: "210"
Example 2:

Input: [3,30,34,5,9]
Output: "9534330"

3637 > 36 > 3634

3637363634

9, 5

9534330
"""