import heapq

def q5(arr, damage_dealt):
    res = []
    max_heap = []

    for idx, health in enumerate(arr):
        heapq.heappush(max_heap, (-health, idx))

    while max_heap:
        current_health, current_idx = heapq.heappop(max_heap) # (-3, 2)
        current_health = -current_health # 3
        updated_health = current_health - damage_dealt #1
        # Check there is health left
        if updated_health <= 0:
            res.append(current_idx + 1)
            continue
        else:
            heapq.heappush(max_heap, (-updated_health, current_idx)) # (-1, 2)

    return " ".join(map(str, res))

if __name__ == "__main__":
    # Read number of test cases
    t = int(input().strip())

    # Process each test case
    for _ in range(t):
        # Read the number of arrays in the current test case
        n, damage_dealt = map(int, input().split())
        arr = list(map(int, input().split()))
        # Process test case and print result
        result = q5(arr, damage_dealt)
        print(result)
