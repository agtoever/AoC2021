#!python3
"""
Day 13 of Advent of Code 2021
See: https://adventofcode.com/2021/day/13
"""

import numpy as np
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)


# IMPORT_FILE = '13.example.01.input'
IMPORT_FILE = '13.input'
SHAPE = (1311, 895)


def import_sheet(filename: str) -> tuple:
    """Import sheet points and fold instructions from filename into a tuple

    Args:
        filename (str): name of the file to be read

    Returns:
        tuple: (numpy.array with dots, list of tuples with fold instructions)
    """
    # Get the path of this Python file
    path = Path(__file__).with_name(filename)

    # Open file in the same path as this Python file
    with path.open('rt') as f:
        # First process coordinates
        coords = []
        for line in f:
            if len(line.strip()) == 0:
                break  # end of coordinates
            coords.append(tuple([int(c) for c in line.strip().split(',')]))

        # Create array of bools and set point at coordinates to True
        arr = np.zeros(shape=SHAPE, dtype=bool)
        # arr = np.zeros(shape=np.array(coords).max(axis=0) + 1, dtype=bool)
        arr[tuple(zip(*coords))] = True

        # Next process folding instructions from the input file
        folds = []
        for line in f:
            axis, value = line.strip().split('=')
            folds.append((axis[-1], int(value)))

        return (arr, folds)


def split_and_fold(arr: np.array, axis: str, value: int) -> np.array:
    """Split and fold arr at the given axis and position

    Args:
        arr (np.array): array to be split and folded
        axis (str): axis: 'x' or 'y'
        value (int): value of the axis where to fold

    Returns:
        np.array: new split and folded array
    """
    if axis == 'x':
        arr1 = arr[:value, :]
        arr2 = arr[:value:-1, :]
    else:  # axis == 'y'
        arr1 = arr[:, :value]
        arr2 = arr[:, :value:-1]
    return arr1 | arr2


def bool_print(arr: np.array) -> str:
    """Pretty print a boolean 2d array

    Args:
        arr (np.array): 2d boolean array

    Returns:
        str: string representation of the bool array
    """
    return '\n'.join(f"{''.join('#' if c else ' ' for c in row)}"
                     for row in arr.T)


def main():
    sheet, folding = import_sheet(IMPORT_FILE)
    sheet = split_and_fold(sheet, *folding[0])

    print('*** First part of the assignment ***')
    print(f'Found {len(sheet[sheet])} dots after 1 fold')

    for fold in folding[1:]:
        logging.debug(f'Next fold: {fold=}; shape before fold: {sheet.shape}')
        sheet = split_and_fold(sheet, *fold)

    print('\n*** Second part of the assignment ***')
    print('Found the following sheet with dots:\n')
    print(bool_print(sheet))


if __name__ == "__main__":
    main()
