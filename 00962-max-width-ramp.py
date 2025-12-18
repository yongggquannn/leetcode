from typing import List

def maxWidthRamp(nums: List[int]) -> int:
    stack = []
    # Form decreasing monotonic stack
    for idx in range(len(nums)):
        if not stack or nums[idx] < nums[stack[-1]]:
            stack.append(idx)
    
    res = 0
    # Traverse backwards to find the max value
    for idx in range(len(nums) - 1, -1, -1):
        while stack and nums[idx] >= nums[stack[-1]]:
            res = max(res, idx - stack.pop())
    return res

nums = [9,8,1,0,1,9,4,0,4,1]
print(maxWidthRamp(nums))

"""
- Next greater element/ next smaller element
- Monotonic stack

nums = [6,0,8,2,1,5]


"""