"""
In a social group, there are N people, with unique integer ids from 0 to N-1.

We have a list of logs, where each logs[i] = [timestamp, id_A, id_B] contains a non-negative integer timestamp, and the ids of two different people.

Each log represents the time in which two different people became friends.  Friendship is symmetric: if A is friends with B, then B is friends with A.

Let's say that person A is acquainted with person B if A is friends with B, or A is a friend of someone acquainted with B.

Return the earliest time for which every person became acquainted with every other person. Return -1 if there is no such earliest time.


Input: logs = [[20190101,0,1],[20190104,3,4],[20190107,2,3],[20190211,1,5],[20190224,2,4],[20190301,0,3],[20190312,1,2],[20190322,4,5]], N = 6
Output: 20190301
Explanation: 
The first event occurs at timestamp = 20190101 and after 0 and 1 become friends we have the following friendship groups [0,1], [2], [3], [4], [5].
The second event occurs at timestamp = 20190104 and after 3 and 4 become friends we have the following friendship groups [0,1], [2], [3,4], [5].
The third event occurs at timestamp = 20190107 and after 2 and 3 become friends we have the following friendship groups [0,1], [2,3,4], [5].
The fourth event occurs at timestamp = 20190211 and after 1 and 5 become friends we have the following friendship groups [0,1,5], [2,3,4].
The fifth event occurs at timestamp = 20190224 and as 2 and 4 are already friend anything happens.
The sixth event occurs at timestamp = 20190301 and after 0 and 3 become friends we have that all become friends.

Note:
2 <= N <= 100
1 <= logs.length <= 10^4
0 <= logs[i][0] <= 10^9
0 <= logs[i][1], logs[i][2] <= N - 1
It's guaranteed that all timestamps in logs[i][0] are different.
logs are not necessarily ordered by some criteria.
logs[i][1] != logs[i][2]

"""

    
class UnionFind:

    def __init__(self, size):
        self.parent = [idx for idx in range(size)]
        self.rank = [1 for _ in range(size)]
        self.latestTimeStamp = None
        self.numGroups = size
    
    def find(self, p):
        if self.parent[p] != p:
            # Path compression
            self.parent[p] = self.find(self.parent[p])
        return self.parent[p]

    def union(self, p, q, timeStamp):
        rootP, rootQ = self.find(p), self.find(q)
        # Belong to different group
        if rootP != rootQ:
            # Rank P higher than Q
            if self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
            elif self.rank[rootQ] > self.rank[rootP]:
                self.parent[rootP] = rootQ
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1
            self.latestTimeStamp = timeStamp
            self.numGroups -= 1
    
    def totalGroups(self):
        return self.numGroups



def earliestMoment(logs, n):
    uf = UnionFind(n)

    # Sort logs in timestamp order
    logs.sort(key=lambda x: x[0])

    for timeStamp, p, q in logs:
        uf.union(p, q, timeStamp)

        if uf.totalGroups() == 1:
            return uf.latestTimeStamp
            
    return -1

logs = [[20190101,0,1],[20190104,3,4],[20190107,2,3],[20190211,1,5],[20190224,2,4],[20190301,0,3],[20190312,1,2],[20190322,4,5]]
n = 6

print(earliestMoment(logs, n))

"""
- Use Union Find data structure to solve the problem
- Idea of path compression 

[[20190101,0,1],[20190104,3,4],[20190107,2,3],[20190211,1,5],[20190224,2,4],[20190301,0,3],[20190312,1,2],[20190322,4,5]]


"""