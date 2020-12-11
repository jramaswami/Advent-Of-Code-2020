"""
Advent of Code 2020 :: Day 11: Seating System
https://adventofcode.com/2020/day/11
"""
import sys
import pyperclip


def eight_neighbors(row, col, seats):
    """Return the eight neighbors adjacent to the cell at (row, col)."""
    offsets = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for row_off, col_off in offsets:
        row0 = row + row_off
        col0 = col + col_off
        if row0 < 0 or row0 >= len(seats):
            continue
        if col0 < 0 or col0 >= len(seats[0]):
            continue
        yield seats[row0][col0]


def visible_neighbors(row, col, seats):
    """Return the visible neighbors in the eight directions fromthe cell at (row, col)."""
    offsets = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for row_off, col_off in offsets:
        keep_looking = True
        row0, col0 = row, col
        while keep_looking:
            row0, col0 = row0 + row_off, col0 + col_off
            if row0 < 0 or row0 >= len(seats):
                keep_looking = False
            elif col0 < 0 or col0 >= len(seats[0]):
                keep_looking = False
            elif seats[row0][col0] != '.':
                yield seats[row0][col0]
                keep_looking = False


def next_state(row, col, seats, neighbor_fn, seat_death):
    """Return the next state of the cell at (row, col)."""
    occupied_neighbors = sum(neighbor == '#' for neighbor
                                 in neighbor_fn(row, col, seats))

    # If a seat is empty (L) and there are no occupied seats adjacent to it,
    # the seat becomes occupied.
    if seats[row][col] == 'L' and occupied_neighbors == 0:
        return '#'

    # If a seat is occupied (#) and four or more seats adjacent to it are also
    # occupied, the seat becomes empty.  This rule is changed in part to to
    # five or more seats.
    if seats[row][col] == '#' and occupied_neighbors >= seat_death:
        return 'L'

    # Otherwise, the seat's state does not change.
    return seats[row][col]


def find_stabilization(seats, neighbor_fn, seat_death):
    """Find the stabilization point."""
    stable = False

    while not stable:
        stable = True
        next_seats = [list(row) for row in seats]
        for r, row in enumerate(seats):
            for c, seat in enumerate(row):
                next_seats[r][c] = next_state(r, c, seats, neighbor_fn, seat_death)
                if seat != next_seats[r][c]:
                    stable = False
        seats = next_seats

    return seats


def solve(seats, neighbor_fn, seat_death):
    """Find the number of occupied seats at the stabilization point."""
    stable_seats = find_stabilization(seats, neighbor_fn, seat_death)
    return sum(sum(seat == '#' for seat in row) for row in stable_seats)


def main():
    """Main program."""
    seats = [[c for c in line.strip()] for line in sys.stdin]
    soln1 = solve([list(row) for row in seats], eight_neighbors, 4)
    print('The solution to part 1 is', soln1)
    assert soln1 == 2265
    soln2 = solve([list(row) for row in seats], visible_neighbors, 5)
    print('The solution to part 2 is', soln2)
    pyperclip.copy(soln2)
    assert soln2 == 2045


if __name__ == '__main__':
    main()