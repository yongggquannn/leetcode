from typing import List
import collections

def numMatchingSubseq(self, s: str, words: List[str]) -> int:
    # O(n) -> Total Characters in string
    letterToOccurrences = collections.defaultdict(list)
    for idx in range(len(s)):
        letterToOccurrences[s[idx]].append(idx)
    res = 0
    # Use binary search O(log m) -> m is length of characters in each word
    def findIdx(lst, temp):
        if not temp:
            return lst[0]
        minIdx = temp[-1]
        left, right = 0, len(lst) - 1
        while left < right:
            mid = (left + right) // 2
            # Reach condition
            if lst[mid] <= minIdx:
                left = mid + 1
            else:
                right = mid
        if lst[left] > minIdx:
            return lst[left]
        return -1

    # O(k) -> Length of words array
    for word in words:
        temp = []
        for char in word:
            if char in letterToOccurrences:
                nextIdx = findIdx(letterToOccurrences[char], temp)
                if not temp or nextIdx != -1:
                    temp.append(nextIdx)
        if len(temp) == len(word):
            res += 1
    return res


"""
Optimal Approach:
- Store in HashMap
- Use binary search to determine index

Time Complexity: O(n + k log m)
Space Complexity: O(n * m) -> Hashmap with values of list

"""