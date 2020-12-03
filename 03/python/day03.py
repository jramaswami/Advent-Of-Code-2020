"""
Advent of Code 2020 :: Day 3: Toboggan Trajectory
"""
import sys
from operator import mul
from functools import reduce
import pyperclip


def main():
    slope_tree_cells = [[0 for _ in range(8)] for _ in range(3)]
    slope_col_indices = [[0 for _ in range(8)] for _ in range(3)]

    for row_index, row in enumerate(sys.stdin):
        col_count = len(row.strip())
        for slope_col in range(8):
            # Count the trees.
            for k in range(1,3):
                if row_index % k == 0:
                    slope_col_index = slope_col_indices[k][slope_col]
                    slope_tree_cells[k][slope_col] += (row[slope_col_index] == '#')

            # Update the index.
            for k in range(1,3):
                if row_index % k == 0:
                    slope_col_indices[k][slope_col] = (slope_col_indices[k][slope_col] + slope_col) % col_count

    soln1 = slope_tree_cells[1][3]
    print('Solution to part 1 is', soln1)
    assert soln1 == 232

    soln2 = reduce(mul, (slope_tree_cells[1][i] for i in (1, 3, 5, 7)), slope_tree_cells[2][1])
    print('Solution to part 2 is', soln2)
    assert soln2 == 3952291680
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()
