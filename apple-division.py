"""
There are n apples with known weights. 
Your task is to divide the apples into two groups so that the difference between the weights of the groups is minimal

Input:

5
3 2 7 4 1
Output:

1
Explanation: Group 1 has weights 2, 3 and 4 (total weight 9), and group 2 has weights 1 and 7 (total weight 8).

Approach:

res = float('inf')
firstSum = 9
secondSum = 8
isPopLeft -> boolean 


[2, 3, 4]

Time Complexity: O (n log n) -> Sorting of array


"""
from functools import cache

def appleDivision(arr):

    @cache
    def dp(currIdx, sumArr1, sumArr2):
        if currIdx == len(arr):
            return abs(sumArr1 - sumArr2)
        # 2 decisions
        addElementToFirst = dp(currIdx + 1, sumArr1 + arr[currIdx], sumArr2)
        addElementToSecond = dp(currIdx + 1, sumArr1, sumArr2 + arr[currIdx])
        return min(addElementToFirst, addElementToSecond)


    return dp(0, 0, 0) # currIdx, sumOfArr1, sumArr2

arr = [3, 2, 7, 4, 1]
print(appleDivision(arr))

# Time complexity: O(n )