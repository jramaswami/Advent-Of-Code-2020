"""
Advent of Code 2020 :: Day 9: Encoding Error
"""
import sys
from itertools import combinations
import pyperclip

# 45 is wrong

def solve1(preamble_length, numbers):
    """Solve first part of the puzzle."""
    soln1 = 0
    for i in range(preamble_length, len(numbers)):
        n = numbers[i]
        if all(a + b != n for a, b in combinations(numbers[i - preamble_length:i], 2)):
            return n
    return None


def test_1():
    """First sample test."""
    numbers = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182,
               127, 219, 299, 277, 309, 576]
    assert solve1(5, numbers) == 127


def find_contiguous_set(numbers, target):
    """Find a subarray that sums to target."""
    left = 0
    ssum = 0
    for right, n in enumerate(numbers):
        ssum += n
        while ssum > target:
            ssum -= numbers[left]
            left += 1

        if ssum == target:
            return numbers[left:right+1]

    return None


def solve2(numbers, target):
    """Solve second part of the puzzle."""
    contiguous_set = find_contiguous_set(numbers, target)
    return min(contiguous_set) + max(contiguous_set)


def test_2():
    """Test find_contigous_set()."""
    numbers = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182,
               127, 219, 299, 277, 309, 576]
    assert find_contiguous_set(numbers, 127) == [15, 25, 47, 40]


def test_3():
    """Second sample test."""
    numbers = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182,
               127, 219, 299, 277, 309, 576]
    assert solve2(numbers, 127) == 62


def main():
    """Main program."""
    numbers = [int(i) for i in sys.stdin]
    soln1 = solve1(25, numbers)
    print('The solution to part 1 is', soln1)
    assert soln1 == 776203571
    soln2 = solve2(numbers, soln1)
    print('The solution to part 2 is', soln2)
    assert soln2 == 104800569
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()