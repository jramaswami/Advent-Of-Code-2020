"""
Advent of Code 2020 :: Day 16: Ticket Translation
"""
import sys
import re
from itertools import chain
import pyperclip


def apply_rule(rule, ticket_value):
    """Return True if ticket value is valid for this rule."""
    for min_value, max_value in rule:
        if ticket_value >= min_value and ticket_value <= max_value:
            return True
    return False


def check_value(value, rules):
    """Return True if the value is ok for any ticket rules."""
    return any(apply_rule(rule, value) for rule in rules.values())


def main():
    """Main program."""
    # Parse input
    rule_pattern = re.compile(r"([^:]+):\s(\d+)-(\d+) or (\d+)-(\d+)")
    line = sys.stdin.readline().strip()
    rules = dict()
    field_names = []
    while line:
        groups = rule_pattern.findall(line)[0]
        line = sys.stdin.readline().strip()
        rules[groups[0]] = ((int(groups[1]), int(groups[2])), (int(groups[3]), int(groups[4])))
        field_names.append(groups[0])

    tickets = []
    line = sys.stdin.readline().strip()  # read "your ticket:"
    line = sys.stdin.readline().strip() # ticket
    tickets.append(tuple(int(i) for i in line.split(',')))
    line = sys.stdin.readline().strip() # read empty line
    line = sys.stdin.readline().strip() # read "nearby tickets:"
    line = sys.stdin.readline().strip()
    while line:
        tickets.append(tuple(int(i) for i in line.split(',')))
        line = sys.stdin.readline().strip()

    # Compute solution 1
    soln1 = sum(v for v in chain(*tickets) if not check_value(v, rules))
    # assert soln1 == 27911
    print(f"The solution to part 1 is {soln1}")
    pyperclip.copy(soln1)

    # Determine for each ticket's values which field it could be.  Then
    # subtract out any fields that it cannot be from the previous set of 
    # possible fields.
    valid_tickets = [t for t in tickets if all(check_value(v, rules) for v in t)]
    field_order = [set(field_names) for _ in field_names]
    for ticket in valid_tickets:
        for field_index, value in enumerate(ticket):
            possible_fields = set()
            for name, rule in rules.items():
                if apply_rule(rule, value):
                    possible_fields.add(name)
            field_order[field_index].intersection_update(possible_fields)

    # Loop over the possible fields and find where a value can only be a
    # certain field.  Then remove that certain field from the possible fields
    # for the rest of the ticket values.
    still_updating = True
    while still_updating:
        still_updating = False
        for s0 in field_order:
            if len(s0) == 1:
                for s1 in field_order:
                    if s0 == s1:
                        continue
                    if len(s1) > 1:
                        s1.difference_update(s0)
                        still_updating = True
    
    # Compute solution 2.
    soln2 = 1
    for i, ticket_value in enumerate(tickets[0]):
        field_name = next(iter(field_order[i]))
        if field_name.startswith('departure'):
            soln2 *= ticket_value
    print(f"The solution to part 2 is {soln2}")
    pyperclip.copy(soln2)
    assert soln2 == 737176602479


if __name__ == '__main__':
    main()
