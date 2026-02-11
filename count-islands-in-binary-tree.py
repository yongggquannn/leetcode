"""
Given a binary tree where nodes have values (typically 0 or 1), analyze the 'islands' (connected components of similar values) within the tree.
Tasks include counting the total number of islands, identifying unique island types based on their structure and size, and analyzing different patterns of island formations. 
An island is defined as a connected group of nodes with the same value.


nodes = [1, 1, 0, 1, 1, null, 0]

2 islands total: 1 island of value 1, 1 island of value 0

Tree structure:

      1
     / \
    1   0
   / \   \
  1   1   0
All 1s are connected through parent–child links, forming a single island of value 1 (size 4). 
The two 0s are connected to each other and form a single island of value 0 (size 2). Therefore, the tree has 2 islands total.


"""
import collections

class TreeNode:
    

    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def countIslandsBinaryTree(root):
    # No root
    if not root:
        return 0
    islandsToCount = collections.defaultdict(int)

    # Take into account root node
    totalIslands = 1
    islandsToCount[root.val] += 1

    # Preorder DFS to process number of islands and map
    def dfs(node, parentVal):
        nonlocal totalIslands
        if not node:
            return
        # Detect change of islands
        if node.val != parentVal:
            totalIslands += 1
            islandsToCount[node.val] += 1

        dfs(node.left, node.val)
        dfs(node.right, node.val)


    # Process left and right nodes recursively
    dfs(root.left, root.val)
    dfs(root.right, root.val)
    
    print(islandsToCount)
    return totalIslands


# Examples are generated using LLM 

def build_example_1():
    """Example from problem: 2 islands (one of 1s size 4, one of 0s size 2)."""
    #       1
    #      / \
    #     1   0
    #    / \   \
    #   1   1   0
    root = TreeNode(1)
    root.left = TreeNode(1)
    root.right = TreeNode(0)
    root.left.left = TreeNode(1)
    root.left.right = TreeNode(1)
    root.right.right = TreeNode(0)
    return root


def build_example_2():
    """Single node: 1 island."""
    return TreeNode(1)


def build_example_3():
    """All same value: 1 island (size 5)."""
    #   1
    #  / \
    # 1   1
    #    / \
    #   1   1
    root = TreeNode(1)
    root.left = TreeNode(1)
    root.right = TreeNode(1)
    root.right.left = TreeNode(1)
    root.right.right = TreeNode(1)
    return root


def build_example_4():
    """Root differs from both children: 3 islands (one 0, two separate 1s)."""
    #     0
    #    / \
    #   1   1
    root = TreeNode(0)
    root.left = TreeNode(1)
    root.right = TreeNode(1)
    return root


def build_example_5():
    """Alternating path: 3 islands (1, 0, 1)."""
    #   1
    #    \
    #     0
    #      \
    #       1
    root = TreeNode(1)
    root.right = TreeNode(0)
    root.right.right = TreeNode(1)
    return root


def build_example_6():
    """More fragmented: 4 islands."""
    #     0
    #    / \
    #   1   0
    #  / \   \
    # 0   1   1
    root = TreeNode(0)
    root.left = TreeNode(1)
    root.right = TreeNode(0)
    root.left.left = TreeNode(0)
    root.left.right = TreeNode(1)
    root.right.right = TreeNode(1)
    return root


if __name__ == "__main__":
    examples = [
        ("Example 1 (problem)", build_example_1()),
        ("Example 2 (single node)", build_example_2()),
        ("Example 3 (all 1s)", build_example_3()),
        ("Example 4 (root 0, children 1,1)", build_example_4()),
        ("Example 5 (alternating 1-0-1)", build_example_5()),
        ("Example 6 (fragmented)", build_example_6()),
    ]
    for name, root in examples:
        print(f"{name}: {countIslandsBinaryTree(root)} islands")
