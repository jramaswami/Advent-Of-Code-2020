"""
Advent of Code 2020 :: Day 1: Report Repair
"""
import sys
import pyperclip


def find_two_sum(arr, s):
    """Find two numbers in arr that sum to s."""
    freqs = dict()
    for n in arr:
        if n in freqs:
            freqs[n] += 1
        else:
            freqs[n] = 1

    for n, freq in freqs.items():
        m = s - n
        if m == n and freq[m] > 1:
            return m, n
        elif m in freqs:
            return min(n, m), max(n, m)


def solve1(arr, s):
    """Return the product of the two numbers in arr that sum to s."""
    n, m = find_two_sum(arr, s)
    return n * m


def test_1():
    """First sample test."""
    nums = [1721, 979, 366, 299, 675, 1456]
    n, m = find_two_sum(nums, 2020)
    assert n == 299 and m == 1721
    assert solve1(nums, 2020) == 514579


def find_three_sum(arr, s):
    """Find two numbers in arr that sum to s."""
    N = len(arr)
    for i in range(N):
        for j in range(i+1, N):
            for k in range(j+1, N):
                if arr[i] + arr[j] + arr[k] == s:
                    return arr[i], arr[j], arr[k]


def solve2(arr, s):
    """Return the product of the two numbers in arr that sum to s."""
    a, b, c = find_three_sum(arr, s)
    return a * b * c


def test_2():
    """First sample test."""
    nums = [1721, 979, 366, 299, 675, 1456]
    assert solve2(nums, 2020) == 241861950


def main():
    """Main program."""
    arr = [int(line.strip()) for line in sys.stdin]
    soln1 = solve1(arr, 2020)
    print('The solution to part 1 is', soln1)
    soln2 = solve2(arr, 2020)
    print('The solution to part 2 is', soln2)
    assert soln1 == 618144
    assert soln2 == 173538720


if __name__ == '__main__':
    main()
