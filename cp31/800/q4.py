def q4(target_int):
    if target_int % 3 == 0:
        return 'Second'
    return 'First'


if __name__ == "__main__":
    t = int(input().strip())

    for _ in range(t):
        n = int(input().strip())
        print(q4(n))
