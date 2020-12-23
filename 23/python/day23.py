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


def play_round(current_cup, cups, min_label, max_label):
    """Play one round of the game."""
    current_label = cups[current_cup]
    # print('current cup', current_label)
    # Place the current cup at the back
    while cups[-1] != current_label:
        cups.rotate(-1)

    # The crab picks up the three cups that are immediately clockwise of the
    # current cup. They are removed.
    picked_cups = []
    for _ in range(3):
        picked_cups.append(cups.popleft())
    # print('picked cups', picked_cups)

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

    # print('destination cup', destination_label)

    # Place the destination cup at the front
    while cups[0] != destination_label:
        cups.rotate(-1)

    # The crab places the cups it just picked up so that they are immediately
    # clockwise of the destination cup. They keep the same order as when they
    # were picked up.
    cups.popleft()
    while picked_cups:
        cups.appendleft(picked_cups.pop())
    cups.appendleft(destination_label)

    # Rotate back to current cup at the right position
    while cups[current_cup] != current_label:
        cups.rotate()


def solve1(number, moves):
    cups = number_to_deque(number)
    min_label = min(cups)
    max_label = max(cups)
    for i in range(0, moves):
        # print('round', i + 1)
        # print("".join(str(c) for c in cups))
        play_round(i % len(cups), cups, min_label, max_label)
        # print()
    # print("".join(str(c) for c in cups))

    while cups[-1] != 1:
        cups.rotate()
    cups.pop()
    return "".join(str(c) for c in cups)


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
    # assert solve1(test_input, 10) == "92658374"
    # assert solve1(test_input, 100) == "67384529"
    puzzle_input = 158937462
    soln1 = solve1(puzzle_input, 100)
    # print(f"The solution to part 1 is {soln1}")
    assert soln1 == "69473825"

    # fill_to = 1000000
    # moves = 10000000
    # solve2(test_input, moves, fill_to)


if __name__ == '__main__':
    main()
