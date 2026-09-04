def q3(num_residents, cost_sharing, max_num_residents, cost_residents):
    # Group the cost to the min number of people sharing
    cost_max_num_residents = list(zip(cost_residents, max_num_residents))
    # Sort by cost in ascending order 
    cost_max_num_residents.sort(key=lambda x:x[0])
    
    # One direct notification to start
    min_cost = cost_sharing
    remaining = num_residents - 1

    for curr_cost, max_num in cost_max_num_residents:
        # Check for edge cases
        # Just do direct sharing since cost is lower
        if remaining <= 0 or curr_cost > cost_sharing:
            break
        residents_take = min(max_num, remaining)
        min_cost += curr_cost * residents_take
        remaining -= residents_take
    
    # Add the remainder cost based on the edge case
    min_cost += cost_sharing * remaining

    return min_cost


if __name__ == "__main__":
    # Read number of test cases
    t = int(input().strip())
    
    # Process each test case
    for _ in range(t):
        n, p = map(int, input().split())
        max_num_residents = list(map(int, input().split()))
        cost_residents = list(map(int, input().split()))
        # Process test case and print result
        result = q3(n, p, max_num_residents, cost_residents)
        print(result)