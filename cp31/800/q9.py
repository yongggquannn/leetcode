def q9(num_teams, arr):
    # Determine sum of arr
    total_score = 0
    for num in arr:
        total_score += num
    # Remaining total score
    return -total_score


if __name__ == "__main__":
    t = int(input().strip())
    for _ in range(t):
        num_teams = int(input().strip())
        arr = list(map(int, input().split()))
        print(q9(num_teams, arr))