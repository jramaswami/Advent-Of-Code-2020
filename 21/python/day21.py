"""
Advent of Code 2020 :: Day 21: Allergen Assessment
"""
import sys
from collections import defaultdict
import pyperclip


def parse_line(line):
    """
    Return a tuple containing (1) a list of ingredients, and 
    (2) a list of allergens.
    """
    line = line.strip()
    tokens = line.split()

    ingredients = []
    t = 0
    while tokens[t] != '(contains':
        ingredients.append(tokens[t])
        t += 1
    
    allergens = []
    t += 1
    while t < len(tokens):
        allergen = tokens[t].strip(',')
        allergen = allergen.strip(')')
        allergens.append(allergen)
        t += 1

    return ingredients, allergens
    


def main():
    """Main program."""
    data = list(sys.stdin)
    # Get the sets of all allergens and all ingredients.
    allergens = set()
    ingredients = set()
    for line in data:
        ingredients0, allergens0 = parse_line(line)
        allergens.update(allergens0)
        ingredients.update(ingredients0)

    # Compute which ingredients are allergens
    could_be = dict()
    for a in allergens:
        could_be[a] = ingredients.copy()

    for line in data:
        ingredients0, allergens0 = parse_line(line)
        for a in allergens0:
            could_be[a].intersection_update(ingredients0)

    # Compute which ingredients are not allergens
    nonallergens = [i for i in ingredients if not any(i in i0 for i0 in could_be.values())]

    # Count how many times they appear
    nonallergen_appearances = defaultdict(int)
    for line in data:
        ingredients0, _ = parse_line(line)
        for nonallergen in nonallergens:
            if nonallergen in ingredients0:
                nonallergen_appearances[nonallergen] += 1

    soln1 = sum(nonallergen_appearances.values())
    print(f"The solution to part 1 is {soln1}.")
    assert soln1 == 1930

    while any(len(s) > 1 for s in could_be.values()):
        for left_allergen, left_ingredients in could_be.items():
            if len(left_ingredients) == 1:
                for right_allergen, right_ingredients in could_be.items():
                    if left_allergen == right_allergen:
                        continue
                    could_be[right_allergen].difference_update(left_ingredients) 

    soln2 = ",".join(i for a, i in sorted((a, list(i)[0]) for a, i in could_be.items()))
    print(f"The solution to part 2 is {soln2}.")
    assert soln2 == 'spcqmzfg,rpf,dzqlq,pflk,bltrbvz,xbdh,spql,bltzkxx'
    pyperclip.copy(soln2)


if __name__ == '__main__':
    main()
