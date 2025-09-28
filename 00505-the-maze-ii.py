"""
There is a ball in a maze with empty spaces and walls. The ball can go through empty spaces by rolling up, down, left or right, but it won't stop rolling until hitting a wall. When the ball stops, it could choose the next direction.

Given the ball's start position, the destination and the maze, find the shortest distance for the ball to stop at the destination. The distance is defined by the number of empty spaces traveled by the ball from the start position (excluded) to the destination (included). If the ball cannot stop at the destination, return -1.

The maze is represented by a binary 2D array. 1 means the wall and 0 means the empty space. You may assume that the borders of the maze are all walls. The start and destination coordinates are represented by row and column indexes.
"""

from typing import List
import heapq

def shortestDistance(maze: List[List[int]], start: List[int], destination: List[int]) -> int:
    ROWS, COLS = len(maze), len(maze[0])
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    start_row, start_col = start
    dest_row, dest_col = destination
    
    pq = [(0, start_row, start_col)]
    distances = [[float('inf')] * COLS for _ in range(ROWS)]
    distances[start_row][start_col] = 0

    while pq:
        curr_dist, curr_row, curr_col = heapq.heappop(pq)

        # Continue to traverse PQ if the shortest distance is more than existing one
        if curr_dist > distances[curr_row][curr_col]:
            continue
        
        for dx, dy in directions:
            updated_dist, updated_row, updated_col = curr_dist, curr_row, curr_col
            # Continue to iterate until it reaches wall and ensure that it is within boundary of the maze
            while (0 <= updated_row + dx <= ROWS - 1) and (0 <= updated_col + dy <= COLS - 1) and maze[updated_row + dx][updated_col + dy] == 0:
                updated_row += dx
                updated_col += dy
                updated_dist += 1
            # Update distance accordingly and use that to continue to traverse in maze
            if updated_dist < distances[updated_row][updated_col]:
                distances[updated_row][updated_col] = updated_dist
                heapq.heappush(pq, (updated_dist, updated_row, updated_col))


    return -1 if distances[dest_row][dest_col] == float('inf') else distances[dest_row][dest_col]


maze = [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,1,0],[1,1,0,1,1],[0,0,0,0,0]]
start = [0,4]
destination = [4,4]

print(shortestDistance(maze, start, destination))