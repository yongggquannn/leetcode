class UnionFind:

    def __init__(self, size):
        self.parent = [idx for idx in range(size)]
        self.rank = [1 for _ in range(size)]
    

    def find(self, parent):
        if self.parent[parent] != parent:
            # Path compression
            self.parent[parent] = self.find(self.parent[parent])
        return self.parent[parent]

    def union(self, p, q):
        rootP, rootQ = self.find(p), self.find(q)
        if rootP != rootQ:
            # Check for rank 
            # Rank P higher than rank Q
            if self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
            elif self.rank[rootQ] > self.rank[rootP]:
                self.parent[rootP] = rootQ
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1
    