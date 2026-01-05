class TreeNode:

    def __init__(self,val=0, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right
        

class Solution:
    def maxSizeIsland(self, root):
        res = 0
        def dfs(currNode):
            nonlocal res
            if not currNode:
                return 0
            leftSize = dfs(currNode.left)
            rightSize = dfs(currNode.right)
            tempArea = 0
            # Curr Node is 1
            if currNode.val == 1:
                tempArea += 1 + leftSize + rightSize
                res = max(res, tempArea)
                return tempArea # Return temp area
            else:
                # Have to find the next max area again
                tempArea = max(leftSize, rightSize)
                res = max(res, tempArea)
                return 0 

        dfs(root) #node
        return res
        



"""
Given a tree having nodes with value 0 and 1. write a function to return the max size of island ?


DFS Approach (Post-Order) -> Return max area at that point
1. If not currNode, return 0 (Base Case)
2. compute Left and Right Subtree
3. increment size if currNode is 1

            1
                
        /       \
    0             0
    
/
1


Ans: 1



            1
                
        /       \
    1             0
    
/
1

Ans: 3
"""

# Test Cases
def test_maxSizeIsland():
    solution = Solution()
    
    # Test Case 1: Example from comments - single node with value 1
    #     1
    #   /   \
    #  0     0
    # /
    # 1
    root1 = TreeNode(1)
    root1.left = TreeNode(0)
    root1.right = TreeNode(0)
    root1.left.left = TreeNode(1)
    print(solution.maxSizeIsland(root1))
    
    # Test Case 2: Example from comments - connected island of 3
    #     1
    #   /   \
    #  1     0
    # /
    # 1
    root2 = TreeNode(1)
    root2.left = TreeNode(1)
    root2.right = TreeNode(0)
    root2.left.left = TreeNode(1)
    \

    

if __name__ == "__main__":
    test_maxSizeIsland()