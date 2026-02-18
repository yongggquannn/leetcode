"""
Given an undirected graph with n nodes and m edges,
find the minimum number of edges that need to be removed to disconnect
the graph into exactly k connected components

Example 1:
n = 4, edges = [(0,1), (1,2), (2,3)], k = 2

0 - 1 - 2 - 3

0 - 1   2 - 3  4

Example 2: (Cycles)
n = 5, edges = [(0, 1), (1,2), (2,3), (3,4), (4,0)], k = 2

0  1  2 - 3 - 4 - 0

[1, 0, 1, 1, 1]

Intuition: 
1. Count initial number of components 
2. Check for number of components and edges to determine answer
3. Put placeholder min cut -> NP Hard

"""
import collections


def removeEdges(n, edges, k):
    adjList = collections.defaultdict(list)
    
    for u, v in edges:
        adjList[u].append(v)
        adjList[v].append(u)
    
    # Count number of connected components
    visited = set()
    numComponents = 0

    def dfs(currNode):
        visited.add(currNode)
        for neigh in adjList[currNode]:
            if neigh not in visited:
                dfs(neigh)

    for node in range(n):
        if node not in visited:
            dfs(node)
            numComponents += 1
    # Invalid case
    if numComponents < k:
        return -1
    
    # No edges needed to remove
    if numComponents == k:
        return 0
    
    # All nodes are connected
    if numComponents == 1 and len(edges) == n - 1:
        return k - 1
    
    # Cycle detected
    if numComponents == 1 and len(edges) == n:
        return k
    # Assume that it has been implemented -> NP Hard
    return minKCut(n, edges, k)

