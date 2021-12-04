"""
Day 1 of Advent of Code 2021
See: https://adventofcode.com/2021/day/1
"""

import numpy
import logging
logging.basicConfig(level=logging.INFO)


IMPORT_FILE = '01.input'


def count_increasing(data: list) -> int:
    """Returns the number of items that are increasing

    Args:
        data (list): list of values

    Returns:
        int: number of consequtive inceasing items in list

    Example:
    >>> count_increasing([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])
    7
    >>> count_increasing(sliding_window( \
        [199, 200, 208, 210, 200, 207, 240, 269, 260, 263], 3))
    5
    """
    return sum(data[n] > data[n - 1] for n in range(1, len(data)))


def sliding_window(data: list, window_size=1, operation=sum) -> list:
    """Smoooths the data by applying operations on a sliding window

    Args:
        data (list): list of values
        window_size (int, optional): sliding window size. Defaults to 1.

    Returns:
        list: new list with operation appliesd to a sliding window

    Example:
    >>> sliding_window([199, 200, 208, 210, 200, 207, 240, 269, 260, 263], 3)
    [607, 618, 618, 617, 647, 716, 769, 792]
    """
    return [operation(data[i:i + window_size])
            for i in range(len(data) - window_size + 1)]


def main():
    depths = numpy.loadtxt(INPUTFILE, dtype='int')

    print('*** First part of the assignment ***')
    print(f'{count_increasing(depths)=}')

    print('\n*** Second part of the assignment ***')
    smooth_depths = sliding_window(depths, 3)
    print(f'{count_increasing(smooth_depths)=}')


if __name__ == "__main__":
    main()
