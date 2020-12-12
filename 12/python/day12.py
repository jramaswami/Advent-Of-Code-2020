"""
Advent of Code 2020 :: Day 12: Rain Risk
"""
import sys
import math
import pyperclip


def round_nearest(fpn):
    """Round the floating point number to the nearest integer."""
    return int(math.floor(fpn + 0.5))


def turn(curr_dirn, turn_cmd, degrees):
    """Turn from current direction."""
    assert (degrees % 90 == 0)
    right_turns = [(1, 0), (0, -1), (-1, 0), (0, 1)]
    left_turns = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    # Find index of current heading.
    index = left_turns.index(curr_dirn) if turn_cmd == 'L' else right_turns.index(curr_dirn)
    new_index = (index + (degrees // 90)) % len(left_turns)
    new_dirn = left_turns[new_index] if turn_cmd == 'L' else right_turns[new_index]
    return new_dirn


def move(curr_posn, curr_dirn, mv_cmd, magnitude):
    """Return new position, direction will not change."""
    offsets = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0), 'F': curr_dirn}
    mv_offset = offsets[mv_cmd]
    new_posn = (curr_posn[0] + (magnitude * mv_offset[0]),
                curr_posn[1] + (magnitude * mv_offset[1]))
    return new_posn


def rotate_waypoint(wp_posn, rotate_cmd, degrees):
    """Rotate current position around the origin (the ship)."""
    if rotate_cmd == 'R':
        degrees *= -1
    rads = math.radians(degrees)
    new_posn = (round_nearest(wp_posn[0] * math.cos(rads) - wp_posn[1] * math.sin(rads)),
                round_nearest(wp_posn[0] * math.sin(rads) + wp_posn[1] * math.cos(rads)))
    return new_posn


def main():
    """Main program."""
    commands = [(line[:1], int(line[1:])) for line in sys.stdin]

    # Part 1
    ship_posn = (0, 0)
    ship_dirn = (1, 0)
    for cmd, magnitude in commands:
        if cmd in ['L', 'R']:
            ship_dirn = turn(ship_dirn, cmd, magnitude)
        elif cmd in ['N', 'S', 'E', 'W', 'F']:
            ship_posn = move(ship_posn, ship_dirn, cmd, magnitude)
    soln1 = abs(ship_posn[0]) + abs(ship_posn[1])
    print(f"The solution to part 1 is {soln1}")
    assert soln1 == 319

    # Part 2
    waypoint_rel_posn = (10, 1)
    ship_posn = (0, 0)
    for cmd, magnitude in commands:
        if cmd in ['L', 'R']:
            waypoint_rel_posn = rotate_waypoint(waypoint_rel_posn, cmd, magnitude)
        elif cmd in ['N', 'E', 'S', 'W']:
            waypoint_rel_posn = move(waypoint_rel_posn, None, cmd, magnitude)
        elif cmd == 'F':
            prev = ship_posn
            ship_posn = (ship_posn[0] + (magnitude * waypoint_rel_posn[0]),
                         ship_posn[1] + (magnitude * waypoint_rel_posn[1]))

    soln2 = abs(ship_posn[0]) + abs(ship_posn[1])
    print(f"The solution to part 2 is {soln2}")
    assert soln2 == 50157
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()