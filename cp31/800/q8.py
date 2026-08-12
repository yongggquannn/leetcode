def q8(arr_len, int_k, arr):
    num_set = set(arr)
    if int_k not in num_set:
        return 'No'
    return 'Yes'


if __name__ == "__main__":
    t = int(input().strip())
    for _ in range(t):
        arr_len, int_k = map(int, input().split())
        arr = list(map(int, input().split()))
        print(q8(arr_len, int_k, arr))
