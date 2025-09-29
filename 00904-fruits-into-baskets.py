from typing import List
from collections import defaultdict

def totalFruit(fruits: List[int]) -> int:
    res = 0
    left = 0
    type_to_count = collections.defaultdict(int)

    
    # Use sliding window approach to solve the problem
    for right in range(len(fruits)):
        type_to_count[fruits[right]] += 1
        # Check if basket is holding more than 2 types of fruit
        while len(type_to_count) > 2:
            type_to_count[fruits[left]] -= 1
            if type_to_count[fruits[left]] == 0:
                del type_to_count[fruits[left]]
            left += 1 
        res = max(res, right - left + 1)
    
    return res


"""

res = 2 (right - left + 1)

fruits = [1,2,3,2,2]
l         ^
r             ^

type_to_count = {1: 1, 2: 1, 3: 1}

=> When len of baskets excced 2, decrement the type of fruit in left until it is not in basket
=> Update left pointer aftwards to the next type of fruit

"""