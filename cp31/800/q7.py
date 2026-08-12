def q7(len_x, len_s, str_x, str_s):
    if any(c not in str_x for c in str_s):
        return -1

    curr = str_x
    for ops in range(6):
        if str_s in curr:
            return ops
        curr = curr + curr

    return -1


if __name__ == "__main__":
    t = int(input().strip())
    for _ in range(t):
        len_x, len_s = map(int, input().split())
        str_x = input().strip()
        str_s = input().strip()
        print(q7(len_x, len_s, str_x, str_s))