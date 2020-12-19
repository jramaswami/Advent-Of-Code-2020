"""
Advent of Code 2020 :: Day 19: Monster Messages
"""
import sys
import re
from collections import defaultdict, deque
import pyperclip


def parenthisize(rule):
    """Convert into parenthisized expression."""
    s = []
    for t in rule:
        if type(t) is list:
            s.append('(')
            s.append(parenthisize(t))
            s.append(')')
        else:
            s.append(t)
    return "".join(s)


def compile_rules(rules):
    """Compile the rules into regexes."""
    # Determine which rules require which
    for r, t in rules.items():
        print(r, t)

    adj = defaultdict(set)
    leaf_nodes = []
    for rule_id, rule in rules.items():
        if rule[0][0] == '"':
            # Terminal node
            leaf_nodes.append(rule_id)
        else:
            for token in rule:
                if token.isdigit():
                    adj[token].add(rule_id)
    # Strip off quotes
    for rule_id in leaf_nodes:
        rules[rule_id] = rules[rule_id][0][1:-1]

    # Do replacements
    queue = deque(leaf_nodes)
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            rules[neighbor] = [rules[node] if t == node else t for t in rules[neighbor]]
            queue.append(neighbor)

    for r, t in rules.items():
        print(r, t)

    # Make into regexes, return rule 0
    for r, t in rules.items():
        p = rules[r]
        rules[r] = parenthisize(t)

    print(rules['0'])
    return re.compile(rules['0']+"$")


def main():
    """Main program."""
    line = sys.stdin.readline().strip()
    rules = dict()
    while line:
        tokens = line.split(': ')
        rules[tokens[0]] = tokens[1].strip().split()
        line = sys.stdin.readline().strip()
    pattern = compile_rules(rules)

    soln1 = 0
    for line in sys.stdin:
        if pattern.match(line):
            soln1 += 1
    print(f"The solution to part 1 is {soln1}.")
    pyperclip.copy(soln1)


if __name__ == '__main__':
    main()
