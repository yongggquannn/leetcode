from collections import Counter

def q6(arr_size, arr):
    counts = Counter(arr)
    # 1 distinct element
    if len(counts) == 1:
        return 'Yes'
    # More than 3 distinct elements
    elif len(counts) >= 3:
        return 'No'
    # Arr size is 2
    elif arr_size == 2:
        return 'Yes'
    c1, c2 = counts.values()
    return 'Yes' if abs(c1 - c2) <= 1 else 'No'

if __name__ == "__main__":
    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        arr = list(map(int, input().split()))
        print(q6(n, arr))