import sys

def solve() -> None:
    inputData = list(map(int, sys.stdin.buffer.read().split()))
    iterator = iter(inputData)

    testCases = next(iterator)
    results = []

    for _ in range(testCases):
        numElements = next(iterator)
        numOperations = next(iterator)
        limit = next(iterator)

        initialVals = [next(iterator) for _ in range(numElements)]
        currVals = [0] * numElements
        # Keep track of position that was last modified
        lastUpdateTime = [-1] * numElements
        # Keep track of operation number when last reset happened
        lastResetTime = -1

        for opIdx in range(numOperations):
            currIdx = next(iterator) - 1
            incrementVal = next(iterator)

            # Check for laze evaluation: update currVals if position has not been updated since last reset
            if lastUpdateTime[currIdx] <= lastResetTime:
                currVals[currIdx] = initialVals[currIdx]

            lastUpdateTime[currIdx] = opIdx
            currVals[currIdx] += incrementVal

            # Check if reached limit: Reset arr and update last reset time
            if currVals[currIdx] > limit:
                currVals[currIdx] = initialVals[currIdx]
                lastResetTime = opIdx
            
        finalState = []

        for idx in range(numElements):
            # Position was updated -> Use curr val
            if lastUpdateTime[idx] > lastResetTime:
                finalState.append(str(currVals[idx]))
            # Position was not update -> Needs to reset to initial val
            else:
                finalState.append(str(initialVals[idx]))


        results.append(" ".join(finalState))

    sys.stdout.write("\n".join(results) + "\n")


if __name__ == "__main__":
    solve()
