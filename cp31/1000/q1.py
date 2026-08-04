from collections import Counter

def q1(binary_str):
    min_cost = 0
    # Reverse and count the number of letters in reversed arr
    initial_letter_to_count = Counter(list(binary_str))

    for idx, letter in enumerate(binary_str):
        complement_letter = '0' if letter == '1' else '1'
        initial_letter_to_count[complement_letter] -= 1
        if initial_letter_to_count[complement_letter] < 0:
            min_cost = len(binary_str) - idx
            break
    return min_cost

if __name__ == "__main__":
    # Read number of test cases
    t = int(input().strip())
    
    # Process each test case
    for _ in range(t):
        s = str(input().strip())
    
        # Process test case and print result
        result = q1(s)
        print(result)