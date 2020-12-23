"""
Advent of Code 2020 :: Day 23: Crab Cups
"""
import sys
from collections import deque
from itertools import islice, dropwhile
import tqdm
import pyperclip

def number_to_deque(number):
    """Turn number into a deque."""
    return deque(int(c) for c in str(number))

def number_to_list(number):
    """Turn number into a list."""
    return [int(c) for c in str(number)]

def play_round(current_cup, cups, min_label, max_label):
    """Play one round of the game."""
    current_label = cups[current_cup]
    print('current cup', current_label)

    # The crab picks up the three cups that are immediately clockwise of the
    # current cup. They are removed.
    picked_cups = []
    i = (current_cup + 1) % len(cups)
    for _ in range(3):
        picked_cups.append(cups[i])
        i = (i + 1) % len(cups)
    print('picked cups', picked_cups)

    # The crab selects a destination cup: the cup with a label equal to the
    # current cup's label minus one. If this would select one of the cups that
    # was just picked up, the crab will keep subtracting one until it finds a
    # cup that wasn't just picked up. If at any point in this process the value
    # goes below the lowest value on any cup's label, it wraps around to the
    # highest value on any cup's label instead.
    destination_label = current_label - 1
    if destination_label < min_label:
        destination_label = max_label
    while destination_label in picked_cups:
        destination_label -= 1
        if destination_label < min_label:
            destination_label = max_label
    print('destination cup', destination_label)

    # The crab places the cups it just picked up so that they are immediately
    # clockwise of the destination cup. They keep the same order as when they
    # were picked up.

    # Move left up to the destination cup
    i = (current_cup + 1) % len(cups)
    while cups[(i + 3) % len(cups)] != destination_label:
        cups[i] = cups[(i + 3) % len(cups)]
        i = (i + 1) % len(cups)
    cups[i] = cups[(i + 3) % len(cups)]
    i = (i + 1) % len(cups)
    
    # Copy picked cups into next three slots
    for j in range(3):
        cups[i] = picked_cups[j]
        i = (i + 1) % len(cups)


def solve1(number, moves):
    cups = number_to_list(number)
    min_label = min(cups)
    max_label = max(cups)
    for i in range(0, moves):
        print('round', i + 1)
        print(" ".join(str(c) for c in cups))
        play_round(i % len(cups), cups, min_label, max_label)
        print()

    # Find the 1.
    i = 0
    while cups[i] != 1:
        i = (i + 1) % len(cups)
    i = (i + 1) % len(cups)
    result = []
    for _ in range(len(cups) - 1):
        result.append(cups[i])
        i = (i + 1) % len(cups)
    # print("".join(str(c) for c in result))
    return "".join(str(c) for c in result)


def solve2(number, moves, fill_to):
    cups = number_to_deque(number)
    min_label = min(cups)
    max_label = max(cups)
    next_label = max_label + 1
    while len(cups) < fill_to:
        cups.append(next_label)
        next_label += 1
    for i in tqdm.tqdm(range(0, moves)):
        play_round(i % len(cups), cups, min_label, max_label)



def main():
    """Main program."""
    test_input = 389125467
    assert solve1(test_input, 10) == "92658374"
    assert solve1(test_input, 100) == "67384529"
    puzzle_input = 158937462
    soln1 = solve1(puzzle_input, 100)
    print(f"The solution to part 1 is {soln1}")
    assert soln1 == "69473825"

    fill_to = 1000000
    moves = 10000000
    solve2(test_input, moves, fill_to)


if __name__ == '__main__':
    main()
