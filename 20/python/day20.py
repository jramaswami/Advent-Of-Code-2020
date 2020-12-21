"""
Advent of Code 2020 :: Day 20: Jurassic Jigsaw
"""
import sys
from collections import defaultdict, deque
from itertools import combinations
from math import sqrt, inf
import numpy as np
import pyperclip

def search(grid):
    s1 = "                  # "
    s2 = "#    ##    ##    ###"
    s3 = " #  #  #  #  #  #   "

    p1 = [i for i, c in enumerate(s1) if c == '#']
    p2 = [i for i, c in enumerate(s2) if c == '#']
    p3 = [i for i, c in enumerate(s3) if c == '#']

    max_off = len(s1)

    result = False
    strings = ["".join(row) for row in grid]
    for r, row in enumerate(grid):
        if r + 2 > len(grid):
            break
        for c, _ in enumerate(row):
            if c + max_off > len(row):
                break

            if (all(grid[r][c + i] == '#' for i in p1) and
                all(grid[r+1][c+i] == '#' for i in p2) and
                all(grid[r+2][c+i] == '#' for i in p3)):

                for i in p1:
                    grid[r][c+i] = 'O'
                for i in p2:
                    grid[r+1][c+i] = 'O'
                for i in p3:
                    grid[r+2][c+i] = 'O'
                result = True
    return result


class Tile:
    def __init__(self, tid, grid):
        self.tid = tid
        self.grid = grid
        self.neighbors = set()
        self.sides = dict()
        self.do_sides()

        self.up = None
        self.down = None
        self.left = None
        self.right = None

    def __repr__(self):
        return "\n".join("".join(row) for row in self.grid)

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)

    def match(self, other):
        for side_m in self.sides:
            for side_o in other.sides:
                if self.sides[side_m] == other.sides[side_o]:
                    self.neighbors.add(other.tid)
                    other.neighbors.add(self.tid)

    def do_sides(self):
        self.sides['top'] = list(self.grid[0])
        self.sides['top_r'] = list(reversed(self.sides['top']))
        # self.sides['left'] = [self.grid[r][0] for r, _ in enumerate(self.grid)]
        self.sides['left'] = [row[0] for r, row in enumerate(self.grid)]
        self.sides['left_r'] = list(reversed(self.sides['left']))
        # self.sides['right'] = [self.grid[r][-1] for r, _ in enumerate(self.grid)]
        self.sides['right'] = [row[-1] for r, row in enumerate(self.grid)]
        self.sides['right_r'] = list(reversed(self.sides['right']))
        self.sides['bottom'] = list(self.grid[-1])
        self.sides['bottom_r'] = list(reversed(self.sides['bottom']))

    def match_right(self, other):
        return self.sides['right'] == other.sides['left']

    def match_bottom(self, other):
        return self.sides['bottom'] == other.sides['top']

    def match_left(self, other):
        return self.sides['right'] == other.sides['bottom']

    def match_top(self, other):
        return self.sides['bottom'] == other.sides['top']


def read_tile():
    """Read Tile from stdin"""
    tile_name = sys.stdin.readline().strip()
    if not tile_name:
        return None, True
    tile_id = int(tile_name[len('Tile '):-1])
    # There are eleven lines in each tile.
    grid = np.array([[c for c in sys.stdin.readline().strip()] for _ in range(10)])
    # Read trailing newline
    if sys.stdin:
        sys.stdin.readline()
    else:
        return Tile(tile_id, grid), True
    return Tile(tile_id, grid), False


def main():
    """Main program."""
    tiles = []
    tile, eof = read_tile()
    while not eof:
        if tile:
            tiles.append(tile)
        tile, eof = read_tile()
    if tile:
        tiles.append(tile)

    for t1, t2 in combinations(tiles, 2):
        t1.match(t2)

    soln1 = 1
    for t in tiles:
        if len(t.neighbors) <= 2:
            soln1 *= t.tid
    print(f"The solution to part 1 is {soln1}")
    assert soln1 == 2699020245973
    pyperclip.copy(soln1)

    # Part 2.
    tilesd = {t.tid: t for t in tiles}
    queue = deque()
    queue.append(tiles[0])
    visited = set()
    visited.add(tiles[0].tid)
    tile_posns = dict()
    tile_posns[tiles[0].tid] = (0, 0)

    while queue:
        tile = queue.popleft()
        for tid0 in tile.neighbors:
            tile0 = tilesd[tid0]
            if tile0.tid in visited:
                continue
            visited.add(tile0.tid)
            queue.append(tile0)
            my_right = tile.sides['right']
            prev_posn = tile_posns[tile.tid]
            for side_o in tile0.sides:
                if my_right == tile0.sides[side_o]:
                    # She is to my left.
                    tile.left = tile0
                    tile0.right = tile
                    if side_o == 'left':
                        pass
                    elif side_o == 'left_r':
                        # She must reverse the left side, a flipud.
                        tile0.grid = np.flipud(tile0.grid)
                    elif side_o == 'right_r':
                        # She must flip l/r and u/d.
                        tile0.grid = np.flipud(tile0.grid)
                        tile0.grid = np.fliplr(tile0.grid)
                    elif side_o == 'top_r':
                        tile0.grid = np.rot90(tile0.grid)
                    elif side_o == 'bottom':
                        tile0.grid = np.rot90(tile0.grid, -1)
                    elif side_o == 'right':
                        tile0.grid = np.fliplr(tile0.grid)
                    elif side_o == 'bottom_r':
                        tile0.grid = np.rot90(tile0.grid, -1)
                        tile0.grid = np.flipud(tile0.grid)
                    elif side_o == 'top':
                        tile0.grid = np.rot90(tile0.grid)
                        tile0.grid = np.flipud(tile0.grid)
                    else:
                        assert False
                    tile0.do_sides()
                    # To the left
                    tile_posns[tile0.tid] = (prev_posn[0], prev_posn[1] - 1)
                    assert tile.sides['right'] == tile0.sides['left']

            my_left = tile.sides['left']
            for side_o in tile0.sides:
                if my_left == tile0.sides[side_o]:
                    # She is to my right.
                    tile.right = tile0
                    tile0.left = tile
                    if side_o == 'right':
                        pass
                    elif side_o == 'right_r':
                        tile0.grid = np.flipud(tile0.grid)
                    elif side_o == 'bottom':
                        tile0.grid = np.rot90(tile0.grid)
                        tile0.grid = np.flipud(tile0.grid)
                    elif side_o == 'left':
                        tile0.grid = np.fliplr(tile0.grid)
                    elif side_o == 'left_r':
                        tile0.grid = np.fliplr(tile0.grid)
                        tile0.grid = np.flipud(tile0.grid)
                    elif side_o == 'top':
                        tile0.grid = np.rot90(tile0.grid, -1)
                    elif side_o == 'top_r':
                        tile0.grid = np.rot90(tile0.grid, -1)
                        tile0.grid = np.flipud(tile0.grid)
                    elif side_o == 'bottom_r':
                        tile0.grid = np.rot90(tile0.grid)
                    else:
                        assert False
                    tile0.do_sides()
                    # To the right
                    tile_posns[tile0.tid] = (prev_posn[0], prev_posn[1] + 1)
                    assert tile.sides['left'] == tile0.sides['right']

            my_bottom = tile.sides['bottom']
            for side_o in tile0.sides:
                if my_bottom == tile0.sides[side_o]:
                    # My bottom matches her.  She is below me.
                    tile.down = tile0
                    tile0.up = tile
                    if side_o == 'top':
                        pass
                    elif side_o == 'top_r':
                        tile0.grid = np.fliplr(tile0.grid)
                    elif side_o == 'bottom':
                        tile0.grid = np.flipud(tile0.grid)
                    elif side_o == 'right':
                        tile0.grid = np.rot90(tile0.grid)
                    elif side_o == 'right_r':
                        tile0.grid = np.rot90(tile0.grid)
                        tile0.grid = np.fliplr(tile0.grid)
                    elif side_o == 'left_r':
                        tile0.grid = np.rot90(tile0.grid, -1)
                    elif side_o == 'left':
                        tile0.grid = np.rot90(tile0.grid, -1)
                        tile0.grid = np.fliplr(tile0.grid)
                    elif side_o == 'bottom':
                        tile0.grid = np.flipud(tile0.grid)
                    elif side_o == 'bottom_r':
                        tile0.grid = np.flipud(tile0.grid)
                        tile0.grid = np.fliplr(tile0.grid)
                    else:
                        assert False
                    tile0.do_sides()
                    # Downwards
                    tile_posns[tile0.tid] = (prev_posn[0] + 1, prev_posn[1])
                    assert tile.sides['bottom'] == tile0.sides['top']

            my_top = tile.sides['top']
            for side_o in tile0.sides:
                if my_top == tile0.sides[side_o]:
                    # She is on top of me.
                    tile.up = tile0
                    tile0.down = tile
                    if side_o == 'bottom':
                        pass
                    elif side_o == 'left':
                        # She must rotate the left to be the bottom
                        tile0.grid = np.rot90(tile0.grid)
                    elif side_o == 'top_r':
                        # She must rotate top to bottom.
                        tile0.grid = np.flipud(tile0.grid)
                        tile0.grid = np.fliplr(tile0.grid)
                    elif side_o == 'left_r':
                        tile0.grid = np.rot90(tile0.grid)
                        tile0.grid = np.fliplr(tile0.grid)
                    elif side_o == 'top':
                        tile0.grid = np.flipud(tile0.grid)
                    elif side_o == 'right':
                        tile0.grid = np.rot90(tile0.grid, -1)
                        tile0.grid = np.fliplr(tile0.grid)
                    elif side_o == 'bottom_r':
                        tile0.grid = np.fliplr(tile0.grid)
                    elif side_o == 'right_r':
                        tile0.grid = np.rot90(tile0.grid, -1)
                    else:
                        assert False
                    tile0.do_sides()
                    # Upwards
                    tile_posns[tile0.tid] = (prev_posn[0] - 1, prev_posn[1])
                    assert tile.sides['top'] == tile0.sides['bottom']

    min_row = inf
    max_row = -inf
    min_col = inf
    max_col = -inf
    for row, col in tile_posns.values():
        min_row = min(min_row, row)
        max_row = max(max_row, row)
        min_col = min(min_col, col)
        max_col = max(max_col, col)

    row_off = 0 - min_row
    col_off = 0 - min_col

    grid = [[None for _ in range(max_col + col_off + 1)] for _ in range(max_row + row_off + 1)]
    for tid, (row, col) in tile_posns.items():
        row0 = row + row_off
        col0 = col + col_off
        grid[row0][col0] = tilesd[tid]
        grid[row0][col0].grid = np.fliplr(grid[row0][col0].grid)  # Not sure why this has to be done but it does.

    for tile in tiles:
        tile.do_sides()

    for r, row in enumerate(grid):
        for c, _ in enumerate(row):
            # Check up
            if r > 0:
                assert grid[r-1][c].sides['bottom'] == grid[r][c].sides['top']
            # Check dn
            if r + 1< len(grid):
                assert grid[r+1][c].sides['top'] == grid[r][c].sides['bottom']
            # Check left
            if c > 0:
                assert grid[r][c-1].sides['right'] == grid[r][c].sides['left']
            # Check right
            if c + 1 < len(grid):
                assert grid[r][c+1].sides['left'] == grid[r][c].sides['right']


    # Build final grid
    for tile in tiles:
        tile.grid = tile.grid[1:-1, 1:-1]

    T = []
    for r in range(len(grid)):
        for r0 in range(8):
            S = []
            for c in range(len(grid)):
                S.append("".join(grid[r][c].grid[r0]))
            T.append("".join(S))

    # Search all the variations for sea monsters, stop when you find them.
    final_grid = np.array([[c for c in row] for row in T])
    result = False
    for _ in range(4):
        result = search(final_grid)
        if result:
            break
        final_grid = np.rot90(final_grid)
    if not result:
        final_grid = np.fliplr(final_grid)
        for _ in range(4):
            result = search(final_grid)
            if result:
                break
            final_grid = np.rot90(final_grid)

    # Count the number of #'s
    soln2 = 0
    for row in final_grid:
        for col in row:
            if col == '#':
                soln2 += 1
    print(f"The solution to part 2 is {soln2}")
    assert soln2 == 2012
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()
