"""
Advent of Code 2020 :: Day 15: Rambunctious Recitation
"""
import pyperclip
import tqdm


def play_game(starting_numbers, stop_turn):
    """Simulate the game."""
    current_turn = 0
    recent_number = 0
    previous_numbers = dict()

    for current_turn in tqdm.tqdm(range(stop_turn)):
        current_number = None
        if current_turn < len(starting_numbers):
            current_number = starting_numbers[current_turn]
        else:
            if len(previous_numbers[recent_number]) < 2:
                current_number = 0
            else:
                current_number = previous_numbers[recent_number][1] - previous_numbers[recent_number][0]
        if current_number not in previous_numbers:
            previous_numbers[current_number] = (current_turn, )
        elif len(previous_numbers[current_number]) == 1:
            previous_numbers[current_number] = (previous_numbers[current_number][0], current_turn)
        else:
            previous_numbers[current_number] = (previous_numbers[current_number][1], current_turn)
        recent_number = current_number
    return current_number


def test_play_game():
    """Test play_game() with sample tests given."""
    assert play_game([0,3,6], 2020) == 436
    assert play_game([1,3,2], 2020) == 1
    assert play_game([2,1,3], 2020) == 10
    assert play_game([1,2,3], 2020) == 27
    assert play_game([2,3,1], 2020) == 78
    assert play_game([3,2,1], 2020) == 438
    assert play_game([3,1,2], 2020) == 1836

    assert play_game([0,3,6], 30000000) == 175594
    assert play_game([1,3,2], 30000000) == 2578
    assert play_game([2,1,3], 30000000) == 3544142
    assert play_game([1,2,3], 30000000) == 261214
    assert play_game([2,3,1], 30000000) == 6895259
    assert play_game([3,2,1], 30000000) == 18
    assert play_game([3,1,2], 30000000) == 362


def main():
    """Main program."""
    puzzle_input = [0,13,16,17,1,10,6]
    soln1 = play_game(puzzle_input, 2020)
    print(f"The solution to part 1 is {soln1}")
    assert soln1 == 276
    soln2 = play_game(puzzle_input, 30000000)
    print(f"The solution to part 1 is {soln2}")
    pyperclip.copy(soln2)
    assert soln2 == 31916


if __name__ == '__main__':
    main()