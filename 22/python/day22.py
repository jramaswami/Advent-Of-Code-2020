"""
Advent of Code 2020 :: Day 22: Crab Combat
"""
import sys
from collections import deque
import pyperclip


def play_combat_round(player1_cards, player2_cards):
    """Play a round of combat."""
    p1 = player1_cards.popleft()
    p2 = player2_cards.popleft()
    if p1 < p2:
        player2_cards.append(p2)
        player2_cards.append(p1)
    else:
        player1_cards.append(p1)
        player1_cards.append(p2)


def compute_winner_score(player1_cards, player2_cards):
    """Compute the winning score."""
    winner_cards = player1_cards if player1_cards else player2_cards
    mulipliers = list(reversed(range(1, len(winner_cards)+1)))
    return sum(a * b for a, b in zip(winner_cards, mulipliers))


def play_combat_game(player1_cards, player2_cards):
    """Play game of combat until someone has no cards."""
    while player1_cards and player2_cards:
        play_combat_round(player1_cards, player2_cards)
    return compute_winner_score(player1_cards, player2_cards)


def play_recursive_round(player1_cards, player2_cards, previous_rounds):
    """Play a round of recursive combat."""
    # If both players have at least as many cards remaining in their deck as
    # the value of the card they just drew, the winner of the round is
    # determined by playing a new game of Recursive Combat
    p1 = player1_cards.popleft()
    p2 = player2_cards.popleft()
    if len(player1_cards) >= p1 and len(player2_cards) >= p2:
        # To play a sub-game of Recursive Combat, each player creates a new
        # deck by making a copy of the next cards in their deck (the quantity
        # of cards copied is equal to the number on the card they drew to
        # trigger the sub-game).
        player1_cards0 = deque(p for i, p in enumerate(player1_cards) if i < p1)
        player2_cards0 = deque(p for i, p in enumerate(player2_cards) if i < p2)
        # Previous rounds from other games are not considered.
        previous_rounds0 = set()
        winner = play_recursive_game0(player1_cards0, player2_cards0, previous_rounds0)
        if winner == 2:
            player2_cards.append(p2)
            player2_cards.append(p1)
        else:
            player1_cards.append(p1)
            player1_cards.append(p2)
    else:
        if p1 < p2:
            player2_cards.append(p2)
            player2_cards.append(p1)
        else:
            player1_cards.append(p1)
            player1_cards.append(p2)

        
def play_recursive_game0(player1_cards, player2_cards, previous_rounds):
    """Recursive function to play a game of recursive combat."""
    round_number = 1
    while player1_cards and player2_cards:
        # If there was a previous round in this game that had exactly the same
        # cards in the same order in the same players' decks, the game instantly
        # ends in a win for player 1
        config = (tuple(player1_cards), tuple(player2_cards))
        if config in previous_rounds:
            return 1
        previous_rounds.add(config)
        play_recursive_round(player1_cards, player2_cards, previous_rounds)
        round_number += 1
    if player1_cards:
        return 1
    else:
        return 2


def play_recursive_game(player1_cards, player2_cards):
    """Function to play a game of recursive combat."""
    previous_rounds = set()
    play_recursive_game0(player1_cards, player2_cards, previous_rounds)
    return compute_winner_score(player1_cards, player2_cards)


def main():
    """Main program."""
    sys.setrecursionlimit(pow(10, 9))

    player1_cards = []
    # Read "Player 1:"
    sys.stdin.readline()
    line = sys.stdin.readline().strip()
    while line:
        player1_cards.append(int(line))
        line = sys.stdin.readline().strip()

    player2_cards = []
    # Read "Player 2:"
    sys.stdin.readline()
    line = sys.stdin.readline().strip()
    while line:
        player2_cards.append(int(line))
        line = sys.stdin.readline().strip()

    soln1 = play_combat_game(deque(player1_cards), deque(player2_cards))
    print(f"The solution to part 1 is {soln1}")
    assert soln1 == 35370

    soln2 = play_recursive_game(deque(player1_cards), deque(player2_cards))
    print(f"The solution to part 2 is {soln2}")
    pyperclip.copy(soln2)
    assert soln2 == 36246


if __name__ == '__main__':
    main()
