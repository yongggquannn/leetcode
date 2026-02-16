"""
Given an array of terrain heights, V droplets are poured one by one at index K 
and each droplet greedily rolls to the leftmost lowest reachable position (otherwise to the right) before settling; 
return the final heights after all drops.
The core challenge is correctly simulating these local greedy flows (left-then-right scan) and updating heights efficiently.

Input: heights = [3, 2, 2], V = 3, K = 1
Output: [3, 4, 3]

[3, 3, 2] -> First drop
[3, 3, 3] -> Second drop
[3, 4, 3] -> Third drop

"""

from turtle import right


def pourWater(heights, v, k):
    droplets, pourIdx = v, k
    
    for _ in range(droplets):
        print(heights)
        # Check for left scan
        leftPos = pourIdx

        for pos in range(leftPos - 1, -1, -1):
            # Go to the next position
            if heights[pos] < heights[leftPos]:
                leftPos = pos
            else:
                break
        
        # Update height of left position if diff
        if leftPos != pourIdx:
            heights[leftPos] += 1
            continue
        
        # Did not manage to find left, check for right
        rightPos = pourIdx

        for pos in range(rightPos + 1, len(heights)):
            if heights[pos] < heights[rightPos]:
                rightPos = pos
            else:
                break
        
        # Update regardless (2 cases: No changes to right position -> update pourIdx, Changes to right position)
        heights[rightPos] += 1

    return heights


heights = [3, 2, 2]
V = 3
K = 1

print(pourWater(heights, V, K))
