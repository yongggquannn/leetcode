"""
Return a rotation table without overlapping periods representing who are on call during that time. 
Return "Start time", "End time" and list of names:

1 5 Abby
5 6 Abby, Ben
6 7 Abby, Ben, Carla
7 10 Abby, Carla
10 12 Carla
15 17 David

onCallTimings = [1, 5, 6, 7, 10, 12, 15, 17]

listNames = [[Abby], [Abby], [Abby], [Abby, Carla], [Carla], [], []] 

# Time Complexity: O(n log n + n x k) -> n is the number of schedule entries and k is unique boundaries
# Space complexity: O (n + kj) 

"""

import bisect

def rotationTable(schedule):
    # Prevent duplicate timings and sort timings  O (n log n)
    onCallTimings = set()
    for _, start, end in schedule:
        onCallTimings.add(start)
        onCallTimings.add(end)
    onCallTimings = sorted(list(onCallTimings)) # [1, 5, 6, 7, 10, 12, 15, 17]

    listNames = [[] for _ in range(len(onCallTimings) - 1)]

    for name, start, end in schedule:
        leftIdx = bisect.bisect_left(onCallTimings, start)
        rightIdx = bisect.bisect_left(onCallTimings, end) - 1
        for i in range(leftIdx, rightIdx + 1):
            listNames[i].append(name)
    
    intervalToNames = {}

    for j in range(len(onCallTimings) - 1):
        # Do not display anybody that is not on call during interval
        if len(listNames[j]) == 0:
            continue
        intervalToNames[f"{onCallTimings[j]} - {onCallTimings[j + 1]}"] = listNames[j]
    
    return intervalToNames
    

    

schedule = [
    ("Abby", 1, 10),
    ("Ben", 5, 7),
    ("Carla", 6, 12),
    ("David", 15, 17),
]

print(rotationTable(schedule))

