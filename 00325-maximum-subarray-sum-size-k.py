import collections

def maximum_subarray_sum_size_k(nums, k):
    sumToIdx = collections.defaultdict(int)
    sumToIdx[0] = -1 # {0: -1}
    res = 0
    prefixSum = 0

    for idx in range(len(nums)):
        prefixSum += nums[idx]
        # Check if there is target within subarray
        if (prefixSum - k) in sumToIdx:
            res = max(res, idx - sumToIdx[prefixSum - k])
        
        # Check if prefix sum in map
        if prefixSum not in sumToIdx:
            sumToIdx[prefixSum] = idx
    return res

nums = [1, -1, 5, -2, 3]
k = 3
print(maximum_subarray_sum_size_k(nums, k))


"""
You are given an integer array nums and an integer k. 
Your task is to find the maximum length of a contiguous subarray whose elements sum to exactly k.
If no such subarray exists, return 0.

Example 1:
nums = [1, -1, 5, -2, 3]
k = 3
Ans: 4

Prefix Sum approach

sumToIdx = {0 : -1, 1: 0, 5: 2}
prefixSum = 3

[1, -1, 5, -2, 3]
            ^

3 - (-1)

"""