"""
Advent of Code 2020 :: Day 25: Combo Breaker
"""
import random
import tqdm
import pyperclip


MOD = 20201227


def solve(card_pk, door_pk):
    """Solve puzzle."""
    card_loop = 0
    door_loop = 0
    s = 7
    max_l = 20000000
    card_pk_solved = False
    door_pk_solved = False
    for l in tqdm.tqdm(range(1, max_l)):
        if card_pk == pow(s, l, MOD):
            card_pk_solved = True
            card_loop = l
        if door_pk == pow(s, l, MOD):
            door_pk_solved = True
            door_loop = l
        if door_pk_solved and card_pk_solved:
            return s, card_loop, door_loop

    return -1


def main():
    """Main program."""
    test_card_pk = 5764801
    test_door_pk = 17807724

    print('Running tests ...')
    subject_number, test_card_loop, test_door_loop = solve(test_card_pk, test_door_pk)
    test_card_encryption_key = pow(test_door_pk, test_card_loop, MOD)
    test_door_encryption_key = pow(test_card_pk, test_door_loop, MOD)

    assert test_card_encryption_key == test_door_encryption_key
    assert test_card_encryption_key == 14897079
    print("... tests ok.\n")

    print('Solving puzzle ...')
    puzzle_door_pk = 13233401
    puzzle_card_pk = 6552760
    subject_number, puzzle_card_loop, puzzle_door_loop = solve(puzzle_card_pk, puzzle_door_pk)
    # print('card', subject_number, puzzle_card_loop)
    # print('door', subject_number, puzzle_door_loop)

    assert pow(subject_number, puzzle_card_loop, MOD) == puzzle_card_pk
    assert pow(subject_number, puzzle_door_loop, MOD) == puzzle_door_pk

    puzzle_card_encryption_key = pow(puzzle_door_pk, puzzle_card_loop, MOD)
    puzzle_door_encryption_key = pow(puzzle_card_pk, puzzle_door_loop, MOD)
    assert puzzle_card_encryption_key == puzzle_door_encryption_key

    print(f"The solution to part 1 is {puzzle_door_encryption_key}")
    assert puzzle_door_encryption_key == 17673381
    pyperclip.copy(puzzle_door_encryption_key)


if __name__ == '__main__':
    main()

