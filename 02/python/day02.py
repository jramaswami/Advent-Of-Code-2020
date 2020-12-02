"""
Advent of Code 2020 :: Day 2: Password Philosophy
https://adventofcode.com/2020/day/2
"""
import sys
import pyperclip

# 382 is too low.

def main():
    """Main program."""
    soln1 = 0
    soln2 = 0
    for line in sys.stdin:
        tokens = line.split(" ")

        min_freq, max_freq = (int(i) for i in tokens[0].split('-'))
        letter = tokens[1][:-1]
        freq = sum(1 if c == letter else 0 for c in tokens[-1])
        if freq >= min_freq and freq <= max_freq:
            soln1 += 1

        left = tokens[-1][min_freq-1]
        right = tokens[-1][max_freq-1]
        if left != right and (left == letter or right == letter):
            soln2 += 1

    print('The solution to part 1 is', soln1)
    print('The solution to part 2 is', soln2)
    assert soln1 == 467
    assert soln2 == 441
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()
