"""
Day 8 of Advent of Code 2021
See: https://adventofcode.com/2021/day/8
"""

import numpy as np
import logging
logging.basicConfig(level=logging.INFO)


IMPORT_FILE = '08.input'


def _l147_score(digit: str, digit147: list) -> tuple:
    """Returns the length of digit and the number of sement matches with 1,4,7

    Args:
        digit (str): the digit to be scored
        digit147 (list): list of segments for digits 1, 4 and 7

    Returns:
        tuple: (length, matching segments with 1, idem with 4, idem with 7)
    """
    logging.debug(f'{digit147=}')
    return tuple([len(digit)] +
                 [len(set(digit) & set(num)) for num in digit147])


def create_mapping(observed: np.array) -> dict:
    """Create a mapping from 10 observed segments to the numbers 0-9

    Args:
        observed (np.array): observed segments as string

    Returns:
        dict: mapping from string value to number (0-9)
    """
    mapping = {}

    # First do the mapping of 1, 4, 7 and 8
    # Those have unique length of 2, 4, 3 and 7 segments
    mapping1 = {2: 1, 4: 4, 3: 7, 7: 8}
    for code in observed:
        if len(code) in mapping1:
            mapping[code] = mapping1[len(code)]

    # If we look at the length *AND* at the number of overlapping characters
    # for the digits 1, 4 and 7, we get unique matches. So we can create
    # a mapping for the tuple(length, match with 1, match with 4, match with 7)
    # to an unique digit
    mapping2 = {
        (5, 1, 2, 2): 2,
        (5, 2, 3, 3): 3,
        (5, 1, 3, 2): 5,
        (6, 1, 3, 2): 6,
        (6, 2, 4, 3): 9,
        (6, 2, 3, 3): 0
    }
    digit147 = sorted(mapping, key=mapping.get)[:3]
    for code in observed:
        l147_score = _l147_score(code, digit147)
        if l147_score in mapping2:
            mapping[code] = mapping2[l147_score]

    logging.debug(f'Mapping complete: {mapping}')
    assert len(mapping) == 10

    return mapping


def main():
    entries = np.loadtxt(IMPORT_FILE, dtype=str)

    count = 0       # count of digits 2,3,4 and 7 in the digits (assignment 1)
    sum_digits = 0  # sum of the digits (assignment 2)

    # Loop over all entries in the input file
    for entry in entries:
        entry = np.fromiter([''.join(sorted(e))
                             for e in entry], dtype=entry.dtype)

        # Split in observed segments and the digit readout
        observed, digits = entry[: 10], entry[11:]

        # Assignment 1
        count += sum([len(digit) in (2, 3, 4, 7)
                     for digit in digits])

        # Assignment 2
        mapping = create_mapping(observed)
        sum_digits += int(''.join(str(mapping[d]) for d in digits))

    print('*** First part of the assignment ***')
    print(f'Number of digits with length 1, 4, 7 or 8: {count}')

    print('\n*** Second part of the assignment ***')
    print(f'Sum of all digit outputs {sum_digits}')


if __name__ == "__main__":
    main()
