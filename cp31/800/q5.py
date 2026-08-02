def q5(arr_size, arr):
    if arr[0] != 1:
        return 'NO'
    return 'YES'

if __name__ == "__main__":
    # Read number of test cases
    t = int(input().strip())
    
    # Process each test case
    for _ in range(t):
        n = map(int, input().split())
        
        # Read the array of n integers
        arr = list(map(int, input().split()))
        
        # Process test case and print result
        result = q5(n, arr)
        print(result)