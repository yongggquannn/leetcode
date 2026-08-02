def q2(num_gas_stations, end, gas_stations):    
    min_fuel_required = float('-inf')
    
    if num_gas_stations == 0:
        return end * 2
    # Determine fuel from starting to first gas station
    min_fuel_required = max(min_fuel_required, gas_stations[0])

    for idx in range(1, num_gas_stations):
        prev_idx = idx - 1
        min_fuel_required = max(min_fuel_required, gas_stations[idx]- gas_stations[prev_idx])
    
    # Determine fuel based on the U-Turn from last gas station to endpoint
    min_fuel_required = max(min_fuel_required, (end - gas_stations[-1]) * 2)

    return min_fuel_required


if __name__ == "__main__":
    # Read number of test cases
    num_test_cases = int(input().strip())
    
    # Process each test case
    for _ in range(num_test_cases):
        # Read n and k
        n, x = map(int, input().split())
        
        # Read the array of n integers
        arr = list(map(int, input().split()))
        
        # Process test case and print result
        result = q2(n, x, arr)
        print(result)