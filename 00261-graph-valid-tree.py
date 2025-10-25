from typing import List
from collections import defaultdict

def validTree(n: int, edges: List[List[int]]) -> bool:
    node_to_neigh = defaultdict(list)
    for edge in edges:
        u, v = edge[0], edge[1]
        node_to_neigh[u].append(v)
        node_to_neigh[v].append(u)
    
    visited = set()
    def dfs(node, parent):
        visited.add(node)
        for neigh in node_to_neigh[node]:
            if neigh not in visited:
                # Visit unvisted neigh
                if not dfs(neigh, node):
                    return False
            # Check for cycles (Found a visited node that is not parent)
            elif neigh != parent:
                return False
        return True
    if not dfs(0, -1):
        return False
    return len(visited) == n 

n = 5
edges = [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]
print(validTree(n, edges))