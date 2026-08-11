import math
import functools

def q2(arr_size, k ,arr):
    res = float('inf')
    # Check for multiples
    for num in arr:
        remainder = num % k
        if remainder == 0:
            res = 0
        else:
            res = min(res, k - remainder) 
    
    # Check for 4
    if k == 4 and arr_size > 1:
        num_evens = 0
        for num in arr:
            if num % 2 == 0:
                num_evens += 1
        min_ops_two_even_num = max(0, 2 - num_evens)
        res = min(res, min_ops_two_even_num)
    
    return res

if __name__ == "__main__":
    # Read number of test cases
    t = int(input().strip())
    
    # Process each test case
    for _ in range(t):
        n, k = map(int, input().split())
        arr = list(map(int, input().split()))
        # Process test case and print result
        result = q2(n, k, arr)
        print(result)