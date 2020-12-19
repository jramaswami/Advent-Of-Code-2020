"""
Advent of Code 2020 :: Day 19: Monster Messages
"""
import sys
import pyperclip
from lark import Lark


def translate(t):
    """Translate token for use in grammar."""
    if t.isdigit():
        return f"RULE_{t}"
    return t


def main():
    """Main program."""
    line = sys.stdin.readline().strip()
    rules = dict()
    rule_max = 0
    while line:
        tokens = line.split(': ')
        rules[tokens[0]] = tokens[1].strip().split()
        line = sys.stdin.readline().strip()
        rule_max = max(int(tokens[0]), rule_max)

    messages = []
    for line in sys.stdin:
        messages.append(line.strip())

    # Part 1
    grammar_rules = ["" for _ in range(rule_max+1)]
    for r, t in rules.items():
        rule_max = max(int(r), rule_max)
        if '|' in t:
            i = t.index('|')
            tl, tr = t[:i], t[i+1:]
            t0 = ("(" + " ".join(translate(e) for e in tl) + ") | (" 
                 + " ".join(translate(e) for e in tr) + ")")
        else:
            t0 = " ".join(translate(e) for e in t)
        if r == '0':
            grammar_rules[int(r)] = f"start: {t0}"
        else:
            grammar_rules[int(r)] = f"RULE_{r}: {t0}"

    parser1 = Lark("\n".join(t for t in grammar_rules if t))
    soln1 = 0
    for m in messages:
        try:
            parser1.parse(m)
            soln1 += 1
        except: 
            pass
    print(f"The solution to part 1 is {soln1}.")
    assert soln1 == 124

    # Part 2
    grammar_rules[0] = "start: rule_8 rule_11"
    grammar_rules[8] = "rule_8: [rule_8] RULE_42"
    grammar_rules[11] = "rule_11: RULE_42 [rule_11] RULE_31"
    parser2 = Lark("\n".join(t for t in grammar_rules if t))
    soln2 = 0
    for m in messages:
        try:
            parser2.parse(m)
            soln2 += 1
        except: 
            pass
    print(f"The solution to part 2 is {soln2}.")
    assert soln2 == 228
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()
