def q1(n, k, arr):    
    isSorted= True

    # Check through each integers in array
    for idx in range(1, n):
        # Array is not sorted
        if arr[idx] < arr[idx - 1]:
            isSorted = False
            break
    # If k is more than 1, will always be able to reverse
    if isSorted or k > 1:
        return "YES"
    return "NO"


if __name__ == "__main__":
    # Read number of test cases
    t = int(input().strip())
    
    # Process each test case
    for _ in range(t):
        # Read n and k
        n, k = map(int, input().split())
        
        # Read the array of n integers
        arr = list(map(int, input().split()))
        
        # Process test case and print result
        result = q1(n, k, arr)
        print(result)

