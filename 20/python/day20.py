"""
Advent of Code 2020 :: Day 20: Jurassic Jigsaw
"""
import sys
from collections import defaultdict
from itertools import combinations
from math import sqrt
import numpy as np
import pyperclip

class Tile:
    def __init__(self, tid, grid):
        self.tid = tid
        self.grid = grid

        self.neighbors = set()

        self.up = None
        self.down = None
        self.right = None
        self.left = None

    def get_sides(self):
        for s in ['top', 'top_r', 'left', 'left_r', 'right', 'right_r', 'bottom', 'bottom_r']:
            yield s

    def get_side(self, s):
        if s == 'top':
            return list(self.grid[0])
        if s == 'top_r':
            return list(reversed(self.get_side('top')))
        if s == 'left':
            return [self.grid[r][0] for r, _ in enumerate(self.grid)]
        if s == 'left_r':
            return list(reversed(self.get_side('left')))
        if s == 'right':
            return [self.grid[r][-1] for r, _ in enumerate(self.grid)]
        if s == 'right_r':
            return list(reversed(self.get_side('right')))
        if s == 'bottom':
            return list(self.grid[-1])
        if s == 'bottom_r':
            return list(reversed(self.get_side('bottom')))

    def __repr__(self):
        return "\n".join("".join(row) for row in self.grid)

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)

    def match(self, other):
        for side_m in self.get_sides():
            SM = self.get_side(side_m)
            for side_o in other.get_sides():
                SO = other.get_side(side_o)
                if SM == SO:
                    self.neighbors.add(other.tid)
                    other.neighbors.add(self.tid)

    def which_matches(self, other):
        for side_m in self.get_sides():
            for side_o in other.get_sides():
                if self.get_side(side_m) == other.get_side(side_o):
                    yield (side_m, side_o)


    def match_right(self, other):
        return self.get_side('right') == other.get_side('left')

    def match_bottom(self, other):
        return self.get_side('bottom') == other.get_side('top')

    def reorient(self):
        # Rotations
        for _ in range(4):
            yield
            self.grid = np.flipud(self.grid)
            yield
            self.grid = np.flipud(self.grid)
            self.grid = np.rot90(self.grid)


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


class Grid:
    def __init__(self, tiles):
        self.tiles = dict()
        for t in tiles:
            self.tiles[t.tid] = t

        self.dim = int(sqrt(len(tiles)))
        self.corner_tiles = [t.tid for t in tiles if len(t.neighbors) == 2]
        self.edge_tiles = [t.tid for t in tiles if len(t.neighbors) == 3]
        self.middle_tiles = [t.tid for t in tiles if len(t.neighbors) == 4]
        self.tile_grid = [[0 for _ in range(self.dim)] for _ in range(self.dim)]

    def is_corner(self, row, col):
        if row == 0 or row == self.dim - 1:
            if col == 0 or col == self.dim - 1:
                return True
        if col == 0 or col == self.dim - 1:
            if row == 0 or row == self.dim - 1:
                return True

    def is_edge(self, row, col):
        if self.is_corner(row, col):
            return False
        return row == 0 or row == self.dim - 1 or col == 0 or col == self.dim - 1

    def is_middle(self, row, col):
        return not self.is_edge(row, col) and not self.is_corner(row, col)

    def neighbors(self, row, col):
        offsets = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for off_row, off_col in offsets:
            row0 = row + off_row
            col0 = col + off_col
            if row0 < 0 or row0 >= self.dim or col0 < 0 or col0 >= self.dim:
                # Out of bounds
                continue
            if self.tile_grid[row0][col0] > 0:
                yield self.tile_grid[row0][col0]

    def posn_ok(self, r, c):
        curr_tile = self.tiles[self.tile_grid[r][c]]
        return all(n in curr_tile.neighbors for n in self.neighbors(r, c))

    def check_soln(self):
        for r, row in enumerate(self.tile_grid):
            for c, t in enumerate(row):
                if r < self.dim - 1:
                    # Make sure of match to bottom
                    if not self.tiles[t].match_bottom(self.tiles[self.tile_grid[r+1][c]]):
                        return False
                if c < self.dim - 1:
                    # Make sure of match to right
                    if not self.tiles[t].match_right(self.tiles[self.tile_grid[r][c+1]]):
                        return False
        return True

    def print_grid(self):
        # For row of grid.
        for r in range(self.dim):
            # For row of each tile.
            for r0 in range(len(self.tiles[self.tile_grid[r][0]].grid)):
                srow = []
                for c in range(len(self.tile_grid[r])):
                    tile = self.tiles[self.tile_grid[r][c]]
                    srow.append("".join(tile.grid[r0]))
                print(" ".join(srow))
            print()

    def arrange(self):
        ct = set(self.corner_tiles)
        et = set(self.edge_tiles)
        mt = set(self.middle_tiles)
        r = c = 0
        self._arrange0(r, c, ct, et, mt)

    def _arrange0(self, r, c, ct, et, mt):
        if r >= self.dim:
            return True

        elif c >= self.dim:
            if self._arrange0(r+1, 0, ct, et, mt):
                return True

        elif self.is_corner(r, c):
            assert ct
            for t in ct:
                ct.remove(t)
                self.tile_grid[r][c] = t
                if self.posn_ok(r, c):
                    if self._arrange0(r, c+1, ct, et, mt):
                        return True
                self.tile_grid[r][c] = 0
                ct.add(t)

        elif self.is_edge(r, c):
            assert et
            for t in et:
                et.remove(t)
                self.tile_grid[r][c] = t
                if self.posn_ok(r, c):
                    if self._arrange0(r, c+1, ct, et, mt):
                        return True
                self.tile_grid[r][c] = 0
                et.add(t)
        else:
            assert mt
            for t in mt:
                mt.remove(t)
                self.tile_grid[r][c] = t
                if self.posn_ok(r, c):
                    if self._arrange0(r, c+1, ct, et, mt):
                        return True
                self.tile_grid[r][c] = 0
                mt.add(t)

    def reorient(self):
        self._reorient0(0, 0)

    def _reorient0(self, r, c):
        if r >= self.dim:
            return self.check_soln()
        elif c >= self.dim:
            if self._reorient0(r+1, 0):
                return True
        else:
            result = False
            tid = self.tile_grid[r][c]
            tile = self.tiles[tid]
            for _ in tile.reorient():
                result = self._reorient0(r, c+1)
                if result == True:
                    break
            return result



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
    pyperclip.copy(soln1)

    grid = Grid(tiles)
    grid.arrange()
    grid.reorient()
    for row in grid.tile_grid:
        print(row)
    grid.print_grid()
    for r in range(grid.dim):
        for c in range(grid.dim):
            print(r, c, grid.tile_grid[r][c], grid.tiles[grid.tile_grid[r][c]].matchings)


if __name__ == '__main__':
    main()
