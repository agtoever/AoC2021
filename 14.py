#!python3
"""
Day 14 of Advent of Code 2021
See: https://adventofcode.com/2021/day/14
"""

import collections
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)


# IMPORT_FILE = '14.example.input'
IMPORT_FILE = '14.input'


def import_polymer(filename: str) -> tuple:
    """Import polymer template and reactions from filename into a tuple

    Args:
        filename (str): name of the file to be read

    Returns:
        tuple: (template: str, dict) with template, reactions
    """
    # Get the path of this Python file
    path = Path(__file__).with_name(filename)

    # Open file in the same path as this Python file
    with path.open('rt') as f:
        # First get the template
        template = f.readline().strip()
        f.readline()  # empty line

        # Now get the reactions
        reactions = {}
        for line in f:
            key, value = line.strip().split(' -> ')
            reactions[key] = value

        return (template, reactions)


def iterate(poly_counter: dict, reactions: dict) -> dict:
    """Apply one iteration of reactions to poly_counter

    Args:
        poly_counter (dict): counter with 2 poly characters as key
        reactions (dict): reaction from poly character duo to one charcter

    Returns:
        dict: new version of poly_counter with reactions applied
    """
    result = collections.defaultdict(int)

    for base, count in poly_counter.items():
        if base in reactions:
            result[base[0] + reactions[base]] += count
            result[reactions[base] + base[1]] += count
        else:
            result[base] += count

    return result


def count_poly_char(poly_counter: dict) -> dict:
    """Counts polymer character in a poly_counter dict

    Args:
        poly_counter (dict): counter with 2 poly characters as key

    Returns:
        dict: poly base character with counts
    """
    result = collections.Counter()

    for base, count in poly_counter.items():
        for base_char in base:
            result[base_char] += count

    for base_char in result:
        result[base_char] = result[base_char] // 2 + result[base_char] % 2

    return result


def main():
    template, reactions = import_polymer(IMPORT_FILE)

    # Convert template to a counter of polymer duo characters
    poly_counter = {key: template.count(key)
                    for key in set([template[i:i+2]
                                    for i in range(len(template) - 1)])}
    logging.debug(f'{template=}\n{reactions=}\n{poly_counter=}')

    for i in range(10):
        poly_counter = iterate(poly_counter, reactions)
    logging.debug(f'Task 1: {poly_counter=} = {count_poly_char(poly_counter)}')
    counts = count_poly_char(poly_counter).values()

    print('*** First part of the assignment ***')
    print(f'Max counts - min counts = {max(counts) - min(counts)}')

    # Add another 30 steps (40 - 10 = 30)
    for i in range(30):
        poly_counter = iterate(poly_counter, reactions)
    logging.debug(f'Task 2: {poly_counter=} = {count_poly_char(poly_counter)}')
    counts = count_poly_char(poly_counter).values()

    print('\n*** Second part of the assignment ***')
    print(f'Max counts - min counts = {max(counts) - min(counts)}')


if __name__ == "__main__":
    main()
