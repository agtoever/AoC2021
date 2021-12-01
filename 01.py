"""
As the submarine drops below the surface of the ocean, it automatically performs a sonar sweep of the nearby sea floor. On a small screen, the sonar sweep report (your puzzle input) appears: each line is a measurement of the sea floor depth as the sweep looks further and further away from the submarine.

For example, suppose you had the following report:

199
200
208
210
200
207
240
269
260
263
This report indicates that, scanning outward from the submarine, the sonar sweep found depths of 199, 200, 208, 210, and so on.

The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with - you never know if the keys will get carried into deeper water by an ocean current or a fish or something.

To do this, count the number of times a depth measurement increases from the previous measurement. (There is no measurement before the first measurement.) In the example above, the changes are as follows:

199 (N/A - no previous measurement)
200 (increased)
208 (increased)
210 (increased)
200 (decreased)
207 (increased)
240 (increased)
269 (increased)
260 (decreased)
263 (increased)
In this example, there are 7 measurements that are larger than the previous measurement.

How many measurements are larger than the previous measurement?
"""

import AoC
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
    with open(IMPORT_FILE, 'rt') as filehandler:
        depths = [item[0] for item in AoC.parse_input(filehandler, [int])]

    print('*** First part of the assignment ***')
    print(f'{count_increasing(depths)=}')

    print('\n*** Second part of the assignment ***')
    smooth_depths = sliding_window(depths, 3)
    print(f'{count_increasing(smooth_depths)=}')


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    main()
