"""
Advent of Code 2020 :: Day 24: Lobby Layout
"""
import sys
from collections import defaultdict
import pyperclip


def parse_tile_reference(tile_reference):
    """Parse tile reference in tokens."""
    index = 0
    while index < len(tile_reference):
        if tile_reference[index] == 'e':
            yield 'e'
            index += 1
        elif tile_reference[index] == 'w':
            yield 'w'
            index += 1
        elif tile_reference[index] == 's':
            yield tile_reference[index:index+2]
            index += 2
        elif tile_reference[index] == 'n':
            yield tile_reference[index:index+2]
            index += 2
        else:
            t = tile_reference[index]
            m = "Parse error, {index}, {t}, {tile_reference}"
            raise Exception(m)


def get_posn(tile_reference):
    """Return the position of the tile referred to relative to (0, 0)."""
    # Use axial coordinate system
    # REF: https://www.redblobgames.com/grids/hexagons/
    offsets = {'e': (1, 0), 'ne': (1, -1), 'nw': (0, -1), 
               'w': (-1, 0), 'sw': (-1, 1), 'se': (0, 1)}
    posn = (0, 0)
    for dirn in parse_tile_reference(tile_reference):
        off = offsets[dirn]
        posn = (posn[0] + off[0], posn[1] + off[1])
    return posn


def solve1(tile_references):
    """Solve part 1 of puzzzle."""
    tiles = defaultdict(lambda: False)
    for ref in tile_references:
        posn = get_posn(ref)
        tiles[posn] = not tiles[posn]
    return sum(tiles.values())


def tick(live_tiles):
    """One unit of time for our game of life.  Return live cells."""
    living_neighbors = defaultdict(int)
    offsets = {'e': (1, 0), 'ne': (1, -1), 'nw': (0, -1), 
               'w': (-1, 0), 'sw': (-1, 1), 'se': (0, 1)}
    for posn in live_tiles:
        for off in offsets.values():
            neighbor = (posn[0] + off[0], posn[1] + off[1])
            living_neighbors[neighbor] += 1

    next_live_tiles = set()
    for posn in living_neighbors:
        # Any live tile with zero or more than 2 live tiles immediately
        # adjacent to it is flipped to dead.
        if posn in live_tiles and (living_neighbors[posn] == 1 or living_neighbors[posn] == 2):
            next_live_tiles.add(posn)
        # Any dead tile with exactly 2 live tiles immediately adjacent to
        # it is flipped to live.
        if posn not in live_tiles and living_neighbors[posn] == 2:
            next_live_tiles.add(posn)
    return next_live_tiles
    

def solve2(tile_references, ticks):
    """Solve part2 of puzzle."""
    tiles = defaultdict(lambda: False)
    for ref in tile_references:
        posn = get_posn(ref)
        tiles[posn] = not tiles[posn]
    live_tiles = set(posn for posn, state in tiles.items() if state)

    for t in range(1, ticks+1):
        live_tiles = tick(live_tiles)
    return len(live_tiles)


def main():
    """Main program."""
    tile_references = [line.strip() for line in sys.stdin if line.strip()]
    soln1 = solve1(tile_references)
    print(f"The solution to part 1 is {soln1}")
    assert soln1 == 293
    soln2 = solve2(tile_references, 100)
    print(f"The solution to part 2 is {soln2}")
    assert soln2 == 3967
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()
