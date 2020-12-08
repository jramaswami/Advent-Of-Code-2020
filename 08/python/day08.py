"""
Advent of Code 2020 :: Day 8: Handheld Halting
"""
import sys
from collections import namedtuple
import pyperclip


Instruction = namedtuple('Instruction', ['index', 'cmd', 'arg'])


class VM:
    """Represents a VM to run the boot code."""

    def __init__(self, lines):
        self.accumulator = 0
        self.instructions = []
        self.instruction_pointer = 0
        for i, line in enumerate(lines):
            tokens = line.split(" ")
            self.instructions.append(Instruction(i, tokens[0], int(tokens[1])))
        self.instructions_executed = [False for _ in self.instructions]

    def run(self):
        """
        Run the boot code. 
        Returns False if any instruction is repeated.
        Returns True if code ran without infinite loop.
        """
        while self.instruction_pointer < len(self.instructions):
            instruction = self.instructions[self.instruction_pointer]
            if self.instructions_executed[instruction.index]:
                # Detect infinite loop.
                return False
            self.instructions_executed[instruction.index] = True
            if instruction.cmd == 'nop':
                self.instruction_pointer += 1
            elif instruction.cmd == 'acc':
                self.accumulator += instruction.arg
                self.instruction_pointer += 1
            elif instruction.cmd == 'jmp':
                self.instruction_pointer += instruction.arg

        return True

    def reset(self):
        """Reset machine."""
        self.accumulator = 0
        self.instruction_pointer = 0
        self.instructions_executed = [False for _ in self.instructions]

    def fix_corruption(self):
        """
        Fix corruption by changing each jmp and nop instruction.
        Returns True if successful.
        """
        for instruction in self.instructions:
            self.reset()
            if instruction.cmd == 'nop':
                instruction0 = Instruction(instruction.index, 'jmp', instruction.arg)
                self.instructions[instruction.index] = instruction0
                if self.run():
                    return True
                self.instructions[instruction.index] = instruction
            elif instruction.cmd == 'jmp':
                instruction0 = Instruction(instruction.index, 'nop', instruction.arg)
                self.instructions[instruction.index] = instruction0
                if self.run():
                    return True
                self.instructions[instruction.index] = instruction
        return False


def main():
    """Main program."""
    vm = VM(sys.stdin)
    vm.run()
    soln1 = vm.accumulator
    assert soln1 == 1867
    print('The solution to part 1 is', soln1)
    vm.fix_corruption()
    soln2 = vm.accumulator
    print('The solution to part 2 is', soln2)
    assert soln2 == 1303
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()
