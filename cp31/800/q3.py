def q3(num_cells, string):
    # Check for substring
    if '...' in string:
        return 2
    return string.count('.')


if __name__ == "__main__":
    t = int(input().strip())

    for _ in range(t):
        n = int(input().strip())
        s = input().strip()
        print(q3(n, s))

"""
Filip has a row of cells, some of which are blocked, and some are empty. He wants all empty cells to have water in them. He has two actions at his disposal:

1
 — place water in an empty cell.
2
 — remove water from a cell and place it in any other empty cell.
If at some moment cell 𝑖
 (2≤𝑖≤𝑛−1
) is empty and both cells 𝑖−1
 and 𝑖+1
 contains water, then it becomes filled with water.

Find the minimum number of times he needs to perform action 1
 in order to fill all empty cells with water.

Note that you don't need to minimize the use of action 2
. Note that blocked cells neither contain water nor can Filip place water in them.

Thought process:
1. Can check if there is any substring '...' -> Can always use the middle grid water to replace other grid
2. If not, just count the number of '.' in the string
"""