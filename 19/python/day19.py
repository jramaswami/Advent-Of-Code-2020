"""
Advent of Code 2020 :: Day 19: Monster Messages
"""
import sys
import re
from collections import defaultdict, deque
import pyperclip
from parsimonious import Grammar
from parsimonious.exceptions import ParseError


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
    done = set()
    depends_on = defaultdict(set)
    leaf_nodes = []
    for rule_id, rule in rules.items():
        if rule[0][0] == '"':
            # Terminal node
            leaf_nodes.append(rule_id)
            rules[rule_id] = rule[0][1:-1]
            done.add(rule_id)
        else:
            for token in rule:
                if token.isdigit():
                    depends_on[rule_id].add(token)

    # Do replacements
    while len(done) < len(rules):
        for r in rules:
            if r in done:
                continue
            if all((pr in done) for pr in depends_on[r]):
                rules[r] = [rules[t] if t != '|' else t for t in rules[r]]
                done.add(r)

    # Make into regexes, return rule 0
    for r, t in rules.items():
        p = rules[r]
        rules[r] = parenthisize(t)
    return re.compile(rules['0']+"$")


def peg_translate(t):
    if t == "|":
        return "/"
    if t.isdigit():
        return f"RULE_{t}"
    return t

def main():
    """Main program."""
    line = sys.stdin.readline().strip()
    rules = dict()
    rules0 = dict()
    while line:
        tokens = line.split(': ')
        rules0[tokens[0]] = tokens[1].strip().split()
        rules[tokens[0]] = tokens[1].strip().split()
        line = sys.stdin.readline().strip()
    pattern = compile_rules(rules)

    soln1 = 0
    messages = []
    for line in sys.stdin:
        messages.append(line.strip())
        if pattern.match(line):
            soln1 += 1
    print(f"The solution to part 1 is {soln1}.")
    # assert soln1 == 124

    peg_rules = []
    for r, t in rules0.items():
        if '|' in t:
            i = t.index('|')
            tl, tr = t[:i], t[i+1:]
            t0 = "(" + " ".join(peg_translate(e) for e in tl) + ") / (" + " ".join(peg_translate(e) for e in tr) + ")"
        else:
            t0 = " ".join(peg_translate(e) for e in t)
        peg_rules.append(f"RULE_{r} = {t0}")
    grammar = Grammar("\n".join(peg_rules))
    
    soln1 = 0
    for m in messages:
        try:
            grammar['RULE_0'].parse(m)
            soln1 += 1
        except ParseError as pe:
            pass

    print(f"The solution to part 1 is {soln1}.")
    pyperclip.copy(soln1)


if __name__ == '__main__':
    main()
