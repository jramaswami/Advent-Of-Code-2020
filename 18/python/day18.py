"""
Advent of Code 2020 :: Day 18: Operation Order
"""
import sys
from collections import deque
import pyperclip


class AdventNumber:
    """Class that will allow use of Python's eval to evaluate expression."""
    def __init__(self, value):
        self.value = value
    
    def __add__(self, other):
        return AdventNumber(self.value * other.value)
    
    def __mul__(self, other):
        return AdventNumber(self.value + other.value)


def parse(expression):
    """Parse expresssion."""
    tokens = []
    number = 0
    i = 0
    while i < len(expression):
        c = expression[i]
        if c.isdigit():
            j = i
            while j < len(expression) and expression[j].isdigit():
                j += 1
            tokens.append(int(expression[i:j]))
            i = j - 1
        elif c == ' ':
            pass
        else:
            tokens.append(c) 
        i += 1
    return tokens


def evaluate(expression):
    """Evaluate expression."""
    value_stack = []
    op_stack = []
    tokens = deque(parse(expression))
    while tokens:
        token = tokens.popleft()
        if token == '(':
            # Push onto op stack to signal the new subexpression
            op_stack.append('(')
        elif token == ')':
            # Place the completed subexpression value at front of tokens
            tokens.appendleft(value_stack.pop())
            # Remove '('
            op_stack.pop()
        elif token == '*':
            op_stack.append('*')
        elif token == '+':
            op_stack.append('+')
        else:
            if op_stack:
                if op_stack[-1] == '(':
                    value_stack.append(token)
                elif op_stack[-1] == '+':
                    a = value_stack.pop()
                    op_stack.pop()
                    value_stack.append(a + token)
                elif op_stack[-1] == '*':
                    a = value_stack.pop()
                    op_stack.pop()
                    value_stack.append(a * token)
            else:
                value_stack.append(token)
    assert len(value_stack) == 1
    return value_stack[-1]


def test_parse():
    """Test parse()."""
    expression = "2 * 3 + (4 * 5)"
    assert parse(expression) == [2, '*', 3, '+', '(', 4, '*', 5, ')']
    expression = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
    assert parse(expression) == [5, '+', '(', 8, '*', 3, '+', 9, '+', 3, '*', 4, '*', 3, ')']
    expression = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
    assert parse(expression) == ['(', '(', 2, '+', 4, '*', 9, ')', '*', '(', 6, '+', 9, '*', 8, '+', 6, ')', '+', 6, ')', '+', 2, '+', 4, '*', 2]


def test_evaluate():
    """Test evaluate()."""
    expression = "2 * 3 + (4 * 5)"
    assert evaluate(expression) == 26
    expression = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
    assert evaluate(expression) == 437
    expression = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
    assert evaluate(expression) == 12240
    expression = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
    assert evaluate(expression) == 13632


def adventize(tokens):
    """Transform numbers into AdventNumbers."""
    tokens0 = []
    for token in tokens:
        if token in ['(', ')']:
            tokens0.append(token)
        elif token == '*':
            tokens0.append('+')
        elif token == '+':
            tokens0.append('*')
        else:
            tokens0.append(f"AdventNumber({token})")
    return tokens0


def advent_evaluate(expression):
    """Evaluate according to advent rules."""
    return eval("".join(adventize(parse(expression)))).value


def test_advent_evaluate():
    """Test advent_evaluate()."""
    expression = "1 + (2 * 3) + (4 * (5 + 6))"
    assert advent_evaluate(expression) == 51
    expression = "2 * 3 + (4 * 5)"
    assert advent_evaluate(expression) == 46
    expression = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
    assert advent_evaluate(expression) == 1445
    expression = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
    assert advent_evaluate(expression) == 669060
    expression = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"
    assert advent_evaluate(expression) == 23340


def main():
    """Main program."""
    expressions = [line.strip() for line in sys.stdin]
    soln1 = sum(evaluate(e) for e in expressions)
    print(f"The solution to part 1 is {soln1}.")
    # Test file 1 soln1 == 26335
    assert soln1 == 131076645626
    soln2 = sum(advent_evaluate(e) for e in expressions)
    print(f"The solution to part 2 is {soln2}.")
    # Test file 2 soln2 == 693942
    assert soln2 == 109418509151782
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()
