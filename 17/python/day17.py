"""
Advent of Code 2020 :: Day 17: Conway Cubes
"""
import sys
from collections import defaultdict
from itertools import product
import pyperclip


def add_v(left, right):
    """Add two vectors (tuples) together."""
    return tuple(a + b for a, b in zip(left, right))


def neighborhood(posn):
    """Return all the neighbors of the given position."""
    offsets = [tuple(p) for p in product([-1, 0, 1], repeat=len(posn))]
    for off in offsets:
        posn0 = add_v(posn, off)
        if posn0 == posn:
            continue
        yield posn0


def tick(live_cells):
    """Return the active cells after the given tick."""
    # Compute number of living neighbor cells for all neighbors
    # that will have a living neighbor.
    live_neighbors = defaultdict(int)
    for posn in live_cells:
        for neighbor in neighborhood(posn):
            live_neighbors[neighbor] += 1

    next_live_cells = set()
    for cell in live_neighbors:
        # If a cube is active and exactly 2 or 3 of its neighbors are also
        # active, the cube remains active. Otherwise, the cube becomes
        # inactive.
        living_neighbors = live_neighbors[cell]
        cell_is_alive = (cell in live_cells)
        if cell_is_alive and (living_neighbors == 2 or living_neighbors == 3):
            next_live_cells.add(cell)
        # If a cube is inactive but exactly 3 of its neighbors are active, the
        # cube becomes active. Otherwise, the cube remains inactive.
        if not cell_is_alive and living_neighbors == 3:
            next_live_cells.add(cell)
        
    return next_live_cells


def main():
    """Main program."""
    live_cells3 = set()
    live_cells4 = set()
    for y, line in enumerate(sys.stdin):
        for x, char in enumerate(line.strip()):
            if char == '#':
                live_cells3.add((x, -y, 0))
                live_cells4.add((x, -y, 0, 0))

    for _ in range(6):
        live_cells3 = tick(live_cells3)
        live_cells4 = tick(live_cells4)

    soln1 = len(live_cells3)
    print(f"The solution to part 1 is {soln1}")
    # assert soln1 == 362
    
    soln2 = len(live_cells4)
    print(f"The solution to part 2 is {soln2}")
    # assert soln2 == 362
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()
