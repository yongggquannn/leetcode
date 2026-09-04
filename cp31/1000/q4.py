def q4(arr):
    second_elements = []
    lowest_first_minimum = float('inf') # 1

    for a in arr:
        a.sort()
        second_elements.append(a[1])
        lowest_first_minimum = min(lowest_first_minimum, a[0]) 

    # Sort the second smallest elements
    second_elements.sort() # [2, 4]
    sum_of_second_elements = sum(second_elements) # 6
    lowest_second_minimum = second_elements[0] # 2

    # Calculate the maximum beauty
    return lowest_first_minimum + sum_of_second_elements - lowest_second_minimum # 1 + 6 - 2


if __name__ == "__main__":
    # Read number of test cases
    t = int(input().strip())

    # Process each test case
    for _ in range(t):
        # Read the number of arrays in the current test case
        n = int(input().strip())
        arrays = []
        for _ in range(n):
            # Read the number of elements in the current array
            m = int(input().strip())
            a = list(map(int, input().split()))
            arrays.append(a)
        # Process test case and print result
        result = q4(arrays)
        print(result)
