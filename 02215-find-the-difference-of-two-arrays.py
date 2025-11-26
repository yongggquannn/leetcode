from collections import Counter
from typing import List

def findDifference(nums1: List[int], nums2: List[int]) -> List[List[int]]:
    num1_to_count = Counter(nums1)
    num2_to_count = Counter(nums2)

    diff_A , diff_B = [], []

    # Check for difference in A 
    for num in nums1:
        if num in num2_to_count:
            num2_to_count[num] -= 1
            if num2_to_count[num] == 0:
                del num2_to_count[num]
        else:
            diff_A.append(num)
    
    for num in nums2:
        if num in num1_to_count:
            num1_to_count[num] -= 1
            if num1_to_count[num] == 0:
                del num1_to_count[num]
        else:
            diff_B.append(num)
    
    return [diff_A, diff_B]


nums1 = [1,3,2,3,4]
nums2 = [1,2,3]
print(findDifference(nums1, nums2))


"""
Given two 0-indexed integer arrays nums1 and nums2, return a list answer of size 2 where:

answer[0] is a list of all distinct integers in nums1 which are not present in nums2.
answer[1] is a list of all distinct integers in nums2 which are not present in nums1.
Note that the integers in the lists may be returned in any order.


Follow-Up: Give those 2 arrays in an order they appeared.

Example 1:
A: [1,3,2,3,4] B:[1,2,3]
answer: [3,4] []

- Use a counter to keep track

{1: 1, 3: 1, 2: 0, 4: 1}
{1: 0, 2: 0, 3: 0}


[3, 4]
[]

"""