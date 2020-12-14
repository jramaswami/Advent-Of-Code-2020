"""
Advent of Code 2020 :: Day 14: Docking Data
"""
import sys
from collections import defaultdict, deque
import pyperclip


def compute_value(mask, number):
    """Compute the value to be written using the mask and the number."""
    for i, mask_bit in enumerate(mask):
        bit = len(mask) - 1 - i
        if mask_bit == '0':
            # Clear bit at i
            number &= (~(1 << bit))
        elif mask_bit == '1':
            # Set bit
            number |= (1 << bit)
    return number


def test_compute_value():
    """Test compute_value() with sample tests given."""
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    assert compute_value(mask, 11) == 73
    assert compute_value(mask, 101) == 101
    assert compute_value(mask, 0) == 64


def bits_to_address(bits):
    """Turn bits into an address (number)."""
    result = 0
    for i, bit in enumerate(bits):
        bit_index = len(bits) - i - 1
        if bit:
            result |= (1 << bit_index)
    return result


def decode_memory_bit(mask, address, index):
    """Determine what the bit is for the memory address."""
    mask_bit = mask[index]
    bit_index = len(mask) - 1 - index
    address_bit = 1 if address & (1 << bit_index) else 0
    if mask_bit == '1':
        return 1
    if mask_bit == 'X':
        return 'X'
    return address_bit


def decode_memory_address(mask, address):
    """Return a list of decoded memory addresses."""
    result = []
    address0 = [decode_memory_bit(mask, address, i) for i, _ in enumerate(mask)]
    queue = [tuple(address0)]
    new_queue = []
    while queue:
        for address1 in queue:
            try:
                x_bit = address1.index('X')
                address2 = list(address1)
                address3 = list(address1)
                address2[x_bit] = 1
                address3[x_bit] = 0
                new_queue.append(tuple(address2))
                new_queue.append(tuple(address3))
            except ValueError:
                # There are no xs in this one, it is done.
                result.append(bits_to_address(address1))
        queue, new_queue = new_queue, []
    result.sort()
    return result


def test_decode_memory_address():
    """Test decode_memory_address() with sample tests given."""
    mask = "000000000000000000000000000000X1001X"
    assert decode_memory_address(mask, 42) == [26, 27, 58, 59]
    mask = "00000000000000000000000000000000X0XX"
    assert decode_memory_address(mask, 26) == [16, 17, 18, 19, 24, 25, 26, 27]


def main():
    """Main program."""
    memory1 = defaultdict(int)
    memory2 = defaultdict(int)
    for line in sys.stdin:
        tokens = line.split(' = ')
        if tokens[0] == 'mask':
            mask = tokens[1].strip()
        else:
            left_bracket = tokens[0].find('[')
            right_bracket = tokens[0].find(']', left_bracket)
            address = int(tokens[0][left_bracket + 1:right_bracket])
            number = int(tokens[1])
            value = compute_value(mask, number)
            memory1[address] = value
            for address0 in decode_memory_address(mask, address):
                memory2[address0] = number

    soln1 = sum(memory1.values())
    print(f"The solution to part 1 is {soln1}")
    assert soln1 == 11327140210986
    soln2 = sum(memory2.values())
    print(f"The solution to part 2 is {soln2}")
    assert soln2 == 2308180581795
    pyperclip.copy(soln2)



if __name__ == '__main__':
    main()
