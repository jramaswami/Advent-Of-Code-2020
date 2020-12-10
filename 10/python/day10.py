"""
Advent of Code 2020 :: Day 10: Adapter Array
"""
import sys
import pyperclip

def main():
    """Main program."""
    adapters = [int(line) for line in sys.stdin]
    adapters.sort()
    device = 3 + adapters[-1]
    adapters = [0] + adapters + [device]
    delta3 = 0
    delta1 = 0
    for a, b in zip(adapters[:-1], adapters[1:]):
        if b - a == 1:
            delta1 += 1
        elif b - a == 3:
            delta3 += 1
    soln1 = delta1 * delta3
    assert soln1 == 2775
    print('The solution to part 1 is', soln1)

    dp = [0 for _ in range(device+1)]
    dp[0] = 1
    for adapter in adapters:
        # This adapter can reach the next 3
        for i in range(1, 4):
            if adapter + i < len(dp):
                dp[adapter+i] += dp[adapter]
    soln2 = dp[device]
    assert soln2 == 518344341716992
    print('The solution to part 2 is', soln2)
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()