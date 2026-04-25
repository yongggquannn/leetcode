from dataclasses import dataclass, replace

@dataclass(frozen=True)
class Position:
    x: int
    y: int

@dataclass(frozen=True)
class Plateau:
    x: int
    y: int

    def within_boundary(self, position: Position):
        return 0 <= position.x <= self.x and 0 <= position.y <= self.y

_COMPASS_ORDER = ("N", "E", "S", "W")
_DIRECTION_TO_DELTA = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}

class Heading:

    def __init__(self, direction: str = "N"):
        self.direction = direction

    def move_delta(self):
        return _DIRECTION_TO_DELTA[self.direction]

    def rotate_left(self):
        i = _COMPASS_ORDER.index(self.direction)
        self.direction = _COMPASS_ORDER[(i - 1) % 4]

    def rotate_right(self):
        i = _COMPASS_ORDER.index(self.direction)
        self.direction = _COMPASS_ORDER[(i + 1) % 4]

class Rover:
    def __init__(self, position: Position, heading: Heading):
        self.position = position
        self.heading = heading

    def move(self, plateau: Plateau, occupied=None):
        dx, dy = self.heading.move_delta()
        new_pos = Position(self.position.x + dx, self.position.y + dy)
        # Out of bounds check
        if not plateau.within_boundary(new_pos):
            return self 

        # If the grid is occupied
        if occupied and new_pos in occupied:
            return self
        
        self.position = new_pos
        return self

    def execute(self, commands, plateau, occupied=None):
        rover = None
        # Check for commands
        for c in commands:
            if c == "L":
                rover = self.heading.rotate_left()
            elif c == "R":
                rover = self.heading.rotate_right()
            elif c == "M":
                rover = self.move(plateau, occupied)
            else:
                raise ValueError("Invalid Command")
        return rover
    
"""
A squad of rovers is being deployed on a rectangular plateau on Mars. The plateau is a grid; rovers must stay within it. 
Each rover has a position (x, y) and a heading in {N, E, S, W}.

Input is two lines per rover. The first gives position and heading, e.g. 1 2 N. The second is a string of commands from {L, R, M}:

L / R — rotate 90° left / right in place

M — move one grid square in the current heading

Print the final state of each rover on its own line.

5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM

1 3 N
5 1 E


Approach: 

1. Design Classes:

Position
x
y

Heading:
Store [N, E, S, W]
Fetch direction which the rover will be moving 

Rover:
position -> Position
heading -> N, S, E, W

Plateau:
x
y

Need a helper function to determine boundary of the grid
"""