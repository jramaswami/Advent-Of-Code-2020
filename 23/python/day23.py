"""
Advent of Code 2020 :: Day 23: Crab Cups
"""
import sys
from math import inf
import tqdm
import pyperclip

class Cup:
    """Represent a cup in the circular array of cups."""
    def __init__(self, lbl, pr=None, nx=None):
        self.label = lbl
        self.pr = pr
        self.nx = nx

    def __repr__(self):
        return str(self.label)

class Cups:
    """Represent the cups as a circular array."""
    def __init__(self):
        self.head = None
        self.my_cups = dict()
        self.min_label = inf
        self.max_label = -inf
        self.length = 0

    def insert_end(self, label):
        """Insert new cup at the end."""
        new_cup = Cup(label)
        if self.head is None:
            new_cup.nx = new_cup.pr = new_cup
            self.head = new_cup
        else:
            last = self.head.pr

            last.nx = new_cup
            new_cup.pr = last

            new_cup.nx = self.head
            self.head.pr = new_cup

        self.my_cups[label] = new_cup
        self.min_label = min(self.min_label, label)
        self.max_label = max(self.max_label, label)
        self.length += 1

    def move_after(self, cup, first_picked_cup, last_picked_cup):
        """Move the group of nodes [first picked cup, last picked cup] after given cup."""
        # Remove [first_node, last_node].
        before = first_picked_cup.pr
        after = last_picked_cup.nx
        before.nx = after
        after.pr = before

        # Insert them after node.
        before = cup
        after = cup.nx
        before.nx = first_picked_cup
        first_picked_cup.pr = before
        last_picked_cup.nx = after
        after.pr = last_picked_cup

    def __len__(self):
        return self.length

    def __repr__(self):
        if self.head == None:
            return str([])
        labels = [self.head.label]
        cup = self.head.nx
        while cup != self.head:
            labels.append(cup.label)
            cup = cup.nx
        return str(labels)


def play_round(current_cup, cups):
    """Play one round of the game."""
    current_label = current_cup.label

    # The crab picks up the three cups that are immediately clockwise of the
    # current cup. They are removed.
    first_picked_cup = current_cup.nx
    last_picked_cup = current_cup.nx.nx.nx
    cup = first_picked_cup
    picked_labels = []
    for _ in range(3):
        picked_labels.append(cup.label)
        cup = cup.nx

    # The crab selects a destination cup: the cup with a label equal to the
    # current cup's label minus one. If this would select one of the cups that
    # was just picked up, the crab will keep subtracting one until it finds a
    # cup that wasn't just picked up. If at any point in this process the value
    # goes below the lowest value on any cup's label, it wraps around to the
    # highest value on any cup's label instead.
    destination_label = current_label - 1
    if destination_label < cups.min_label:
        destination_label = cups.max_label
    while destination_label in picked_labels:
        destination_label -= 1
        if destination_label < cups.min_label:
            destination_label = cups.max_label

    # The crab places the cups it just picked up so that they are immediately
    # clockwise of the destination cup. They keep the same order as when they
    # were picked up.
    destination_cup = cups.my_cups[destination_label]
    cups.move_after(destination_cup, first_picked_cup, last_picked_cup)
    

def solve1(number, moves):
    """Solve part 1 of puzzle."""
    len_n = 0
    cups = Cups()
    for n in (int(i) for i in str(number)):
        cups.insert_end(n)
        len_n += 1

    current_cup = cups.head
    for i in range(0, moves):
        play_round(current_cup, cups)
        current_cup = current_cup.nx

    one_cup = cups.my_cups[1]
    result = []
    cup = one_cup.nx
    while cup != one_cup:
        result.append(cup.label)
        cup = cup.nx
    return "".join(str(c) for c in result)


def solve2(number, moves, fill_to):
    """Solve part 2 of puzzle."""
    print('Laying out cards ...')
    cups = Cups()
    for n in (int(i) for i in str(number)):
        cups.insert_end(n)
    next_label = cups.max_label + 1
    while next_label <= fill_to:
        cups.insert_end(next_label)
        next_label += 1

    print('Playing game ...')
    current_cup = cups.head
    for i in tqdm.tqdm(range(0, moves)):
        play_round(current_cup, cups)
        current_cup = current_cup.nx

    one_cup = cups.my_cups[1]
    print(one_cup.nx, one_cup.nx.nx)
    return one_cup.nx.label * one_cup.nx.nx.label


def main():
    """Main program."""
    print('Part 1 ... greased lightning!')
    test_input = 389125467
    print('Testing ...')
    assert solve1(test_input, 10) == "92658374"
    assert solve1(test_input, 100) == "67384529"
    print('Tests passed.')
    print('Running puzzle input ...')
    puzzle_input = 158937462
    soln1 = solve1(puzzle_input, 100)
    print(f"The solution to part 1 is {soln1}")
    assert soln1 == "69473825"
    print("\n")

    fill_to = 1000000
    moves = 10000000
    print('Part 2 ... this one takes a little bit of time.')
    print('Testing ...')
    assert solve2(test_input, moves, fill_to) == 149245887792
    print('Test passed.')
    print('Running puzzle input ...')
    soln2 = solve2(puzzle_input, moves, fill_to)
    print(f"The solution to part 2 is {soln2}")
    pyperclip.copy(soln2)
    assert soln2 == 96604396189


if __name__ == '__main__':
    main()
