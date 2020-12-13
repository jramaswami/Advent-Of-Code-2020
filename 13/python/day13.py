"""
Advent of Code 2020 :: Day 13: Shuttle Search
"""
import sys
import math
from functools import reduce
from operator import mul
import pyperclip


def solve2(buses):
    """
    Solve part 2 of puzzle.

    Use Chinese Remainder Theorem to solve modular equations.
    REF: Guide to Competitive Programming, A. Laaksonen, pp.155-156
    """
    # Equation: x = a mod m
    eqns = [(0 if i == 0 else b - i, b) for i, b in enumerate(buses) if b != 'x']
    # Product = m[1] * m[2] * ... * m[n]
    product = reduce(mul, (b for b in buses if b != 'x'), 1)
    # Solution is sum of a[i] * X[i] * inv[m[i]]](X[i])
    # where X[i] is m[1] * m[2] * ... * m[n] / m[i]
    # and inv[m[i]]] is the multiplicative inverse of X[i]  mod m[i]
    soln2 = 0
    # eqns = [(3, 5), (4, 7), (2, 3)]
    # product = 5 * 7 * 3
    for a, m in eqns:
        X = product // m
        soln2 += a * X * pow(X, m - 2, m)

    # This gives as *a* solution.  We want the lowest solution.
    # Solutions can be in the form of x + m[1]*m[2]* ... * m[n].
    # So find the most of m[1]*m[2]*...m[n] that can be removed
    # without dropping below zero.
    soln2 -= (product * (soln2 // product))
    return soln2


def test_solve2():
    """Test solve2() with the provided samples."""
    x = 'x'
    buses = [7,13,x,x,59,x,31,19]
    assert solve2(buses) == 1068781

    buses = [17,x,13,19]
    assert solve2(buses) == 3417

    buses = [67,7,59,61]
    assert solve2(buses) == 754018

    buses = [67,x,7,59,61]
    assert solve2(buses) == 779210

    buses = [67,7,x,59,61]
    assert solve2(buses) == 1261476

    buses = [1789,37,47,1889]
    assert solve2(buses) == 1202161486


def solve1(earliest, buses):
    """Solve part 1 of puzzle."""
    # Which bus has the lowest k * timestap >= earliest departure
    best_departure = math.inf
    best_bus = None
    for bus in buses:
        if bus == 'x':
            continue
        departing = int(math.ceil(earliest / bus)) * bus
        if departing < best_departure:
            best_departure = departing
            best_bus = bus
    return (best_departure - earliest) * best_bus


def main():
    """Main program."""
    earliest = int(sys.stdin.readline())
    buses = [i if i == 'x' else int(i) for i in sys.stdin.readline().split(',')]

    soln1 = solve1(earliest, buses)
    print(f"The solution to part 1 is {soln1}")
    assert soln1 == 138

    soln2 = solve2(buses)
    print(f"The solution to part 2 is {soln2}")
    assert soln2 == 226845233210288
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()