"""
Advent of Code 2020 :: Day 5: Binary Boarding
"""
import sys
from itertools import count, dropwhile
import pyperclip


def binary_search(boarding_pass):
    """Binary search for the row/col from a boarding pass."""
    # Count the number of FB and LR
    row_bits = 0
    col_bits = 0
    for c in boarding_pass:
        if c == 'F' or c == 'B':
            row_bits += 1
        elif c == 'L' or c == 'R':
            col_bits += 1

    ptr = 0
    low_row = 0
    high_row = pow(2, row_bits) - 1
    row = 0
    while boarding_pass[ptr] == 'F' or boarding_pass[ptr] == 'B':
        row = (low_row + high_row) // 2
        if boarding_pass[ptr] == 'F':
            high_row = row
        else:
            low_row = row + 1
        ptr += 1
    assert low_row == high_row
    row = low_row

    low_col = 0
    high_col = pow(2, col_bits) - 1
    col = 0
    while ptr < len(boarding_pass):
        col = (low_col + high_col) // 2
        if boarding_pass[ptr] == 'L':
            high_col = col
        else:
            low_col = col + 1
        ptr += 1
    assert low_col == high_col
    col = low_col

    return row, col


def binary_bp(boarding_pass):
    """
    Alternate (better) solution to convert convert boarding pass to row, col.
    """
    row = 0
    col = 0
    for c in boarding_pass:
        if c == 'F':
            row = row << 1
        elif c == 'B':
            row = (row << 1) | 1
        elif c == 'L':
            col = (col << 1)
        elif c == 'R':
            col = (col << 1) | 1
    return row, col


def seat_id(boarding_pass):
    """Return unique seat id for boarding pass."""
    row, col = binary_bp(boarding_pass)
    return (row * 8) + col


def main():
    """Main program."""
    boarding_passes = [line.strip() for line in sys.stdin]
    seat_ids = [seat_id(bp) for bp in boarding_passes]
    seat_ids.sort()
    soln1 = seat_ids[-1]
    print('The solution to part 1 is', soln1)
    assert soln1 == 842
    # Look for the first pair where the seat_id does not match the index,
    # starting with the index of the first seat.  The index of the first
    # mismatch is my seat.
    idx0 = seat_ids[0]
    soln2 = next(dropwhile(lambda t: t[0] == t[1], zip(seat_ids, count(idx0))))[1]
    print('The solution to part 2 is', soln2)
    pyperclip.copy(soln2)
    assert soln2 == 617


def test_binary_search():
    """Test binary_search() function."""
    assert binary_search("FBFBBFFRLR") == (44, 5)
    assert binary_search("BFFFBBFRRR") == (70, 7)
    assert binary_search("FFFBBBFRRR") == (14, 7)
    assert binary_search("BBFFBBFRLL") == (102, 4)


def test_binary_bp():
    """Test binary_bp() function."""
    assert binary_bp("FBFBBFFRLR") == (44, 5)
    assert binary_bp("BFFFBBFRRR") == (70, 7)
    assert binary_bp("FFFBBBFRRR") == (14, 7)
    assert binary_bp("BBFFBBFRLL") == (102, 4)

def test_seat_id():
    """Test seat_id() function."""
    assert seat_id("FBFBBFFRLR") == 357
    assert seat_id("BFFFBBFRRR") == 567
    assert seat_id("FFFBBBFRRR") == 119
    assert seat_id("BBFFBBFRLL") == 820


if __name__ == '__main__':
    main()