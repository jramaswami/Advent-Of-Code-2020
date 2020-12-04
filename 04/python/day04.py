"""
Advent of Code 2020 :: Day 4: Passport Processing
"""
import sys
import pyperclip


def parse(iterable):
    """
    Parse input.  Records are separated by two newlines.  Returns a dictionary
    with the data fields.
    """
    record = dict()
    for line in iterable:
        if line == '\n':
            yield record
            record = dict()
        else:
            tokens = line.split()
            for token in tokens:
                key, value = token.split(':')
                record[key] = value
    yield record


def is_valid(record):
    """
    Valid record requires 8 fields.  We are temporarily allowing the
    cid field to be missing.
    """
    eight_fields = set(("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"))
    seven_fields = set(("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"))
    return set(record.keys()) == eight_fields or set(record.keys()) == seven_fields


def is_number_between(field, start, end):
    """Return True if field is a number between [start, end]."""
    if not field.isdigit():
        return False
    number = int(field)
    if number < start or number > end:
        return False
    return True


def is_hex(field):
    """Return True if field is a hexidecimal number."""
    if field[0] != '#':
        return False
    for c in field[1:]:
        if not (c.isdigit() or c in ['a', 'b', 'c', 'd', 'e', 'f']):
            return False
    return True


def is_very_valid(record):
    """
    Additional rules:
    - byr (Birth Year) - four digits; at least 1920 and at most 2002.
    - iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    - eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    - hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    - hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    - ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    - pid (Passport ID) - a nine-digit number, including leading zeroes.
    - cid (Country ID) - ignored, missing or not.
    """
    if not is_valid(record):
        return False
    if not is_number_between(record['byr'], 1920, 2002):
        return False
    if not is_number_between(record['iyr'], 2010, 2020):
        return False
    if not is_number_between(record['eyr'], 2020, 2030):
        return False

    # For the height there must be at least 2 digits and 2 characters.
    if len(record['hgt']) < 4:
        return False
    value, units = record['hgt'][:-2], record['hgt'][-2:]
    if units == 'cm': 
        if not is_number_between(value, 150, 193):
            return False
    elif units == 'in': 
        if not is_number_between(value, 59, 76):
            return False
    else:
        return False
    if not is_hex(record['hcl']):
        return False
    if record['ecl'] not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return False
    if not (record['pid'].isdigit() and len(record['pid']) == 9):
        return False

    return True


def main():
    """Main program."""
    records = list(parse(sys.stdin))
    soln1 = sum(is_valid(r) for r in records)
    assert soln1 == 233
    print('The solution to part 1 is', soln1)
    soln2 = sum(is_very_valid(r) for r in records)
    assert soln2 == 111
    print('The solution to part 2 is', soln2)
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()

