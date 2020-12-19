"""
Advent of Code 2020 :: Day 19: Monster Messages
"""
import sys
import pyperclip
from parsimonious import Grammar
from parsimonious.exceptions import ParseError


def peg_translate(t):
    """Translate token for use in PEG grammar."""
    if t == "|":
        return "/"
    if t.isdigit():
        return f"RULE_{t}"
    return t

def main():
    """Main program."""
    line = sys.stdin.readline().strip()
    rules = dict()
    while line:
        tokens = line.split(': ')
        rules[tokens[0]] = tokens[1].strip().split()
        line = sys.stdin.readline().strip()

    messages = []
    for line in sys.stdin:
        messages.append(line.strip())

    peg_rules1 = []
    peg_rules2 = []
    for r, t in rules.items():
        if '|' in t:
            i = t.index('|')
            tl, tr = t[:i], t[i+1:]
            t0 = "(" + " ".join(peg_translate(e) for e in tl) + ") / (" + " ".join(peg_translate(e) for e in tr) + ")"
        else:
            t0 = " ".join(peg_translate(e) for e in t)
        peg_rules1.append(f"RULE_{r} = {t0}")

        # Part 2
        if r == '8':
            t0 = "RULE_42 / (RULE_42 RULE_8)"
        if r == '11':
            t0 = "(RULE_42 RULE_31) / (RULE_42 RULE_11 RULE_31)"
        peg_rules2.append(f"RULE_{r} = {t0}")

    print('part 1')
    print("\n".join(peg_rules1))
    grammar1 = Grammar("\n".join(peg_rules1))
    grammar2 = Grammar("\n".join(peg_rules2))
    
    soln1 = 0
    for m in messages:
        try:
            grammar1['RULE_0'].parse(m)
            soln1 += 1
        except ParseError as pe:
            pass
    print(f"The solution to part 1 is {soln1}.")

    print('part 2')
    print("\n".join(peg_rules2))
    soln2 = 0
    for m in messages:
        try:
            grammar2['RULE_0'].parse(m)
            print('ok', m)
            soln2 += 1
        except ParseError as pe2:
            print('bad', m, print(pe2))
            pass

    print(f"The solution to part 2 is {soln2}.")
    pyperclip.copy(soln1)


if __name__ == '__main__':
    main()
