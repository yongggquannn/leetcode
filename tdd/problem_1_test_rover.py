from problem_1_rover import Position, Rover, Heading, Plateau

PLATEAU = Plateau(5, 5)

def test_rover_turns_left_from_north_to_west():
    r = Rover(Position(2, 2), Heading("N"))
    r.heading.rotate_left()
    assert r.heading.direction == "W"

def test_rover_moves_north():
    r = Rover(Position(1, 1), Heading("N")).move(PLATEAU)
    assert r.position == Position(1, 2)

def test_rover_ignore_move_out_of_bounds():
    r = Rover(Position(5, 5), Heading("N")).move(PLATEAU)
    assert r.position == Position(5, 5)

def test_case_one():
    r = Rover(Position(1, 2), Heading("N")).execute("LMLMLMLMM", PLATEAU)
    assert r.position == Position(1, 3)

def test_case_two():
    r = Rover(Position(3, 3), Heading("E")).execute("MMRMMRMRRM", PLATEAU)
    assert r.position == Position(5, 1)

def test_collision():
    occupied_pos = Position(1, 2)
    # Move by (0, 1) for rover, but since occupied, remains in position
    r = Rover(Position(1, 1), Heading("N")).move(PLATEAU, {occupied_pos})
    assert r.position == Position(1, 1)

"""
Test Cases to consider:
1. turn left from north to west
2. rover moves north
3. rover ignores move out of bounds
4. execute one of the moves
5. Collision 

"""