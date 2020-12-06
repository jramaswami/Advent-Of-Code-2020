"""
Advent of Code 2020 :: Day 6: Custom Customs
"""
import sys
import string
import pyperclip


def main():
    """Main program."""
    group1 = set()
    group2 = set(string.ascii_lowercase)
    soln1 = 0
    soln2 = 0
    for line in sys.stdin:
        line = line.strip()
        answered = set()
        if line:
            for c in line:
                group1.add(c)
                answered.add(c)
            group2.intersection_update(answered)
        else:
            soln1 += len(group1)
            soln2 += len(group2)
            group1 = set()
            group2 = set(string.ascii_lowercase)
    soln1 += len(group1)
    soln2 += len(group2)
    print('The solution to part 1 is', soln1)
    assert soln1 == 6437
    print('The solution to part 2 is', soln2)
    assert soln2 == 3229
    pyperclip.copy(soln2)



if __name__ == '__main__':
    main()
