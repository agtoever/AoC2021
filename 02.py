"""
Day 2 of Advent of Code 2021
See: https://adventofcode.com/2021/day/2
"""


import AoC
import logging
import numpy
logging.basicConfig(level=logging.INFO)


IMPORT_FILE = '02.input'
INITIAL_POSITION = [0, 0, 0]  # horizontal, vertical, aim
DIRECTIONS_1 = {
    'forward': (1, 0, 0),
    'down': (0, 1, 0),
    'up': (0, -1, 0)
}
DIRECTIONS_2 = {
    'forward': (1, 0, 0),
    'down': (0, 0, 1),
    'up': (0, 0, -1)
}


def main():
    with open(IMPORT_FILE, 'rt') as filehandler:
        route = AoC.parse_input(filehandler, [str, int], ' ')

    position = numpy.array(INITIAL_POSITION)
    for step in route:
        position += numpy.array(DIRECTIONS_1[step[0]]) * step[1]
        logging.debug(f'Position after {step=} is: {position=}')

    print('*** First part of the assignment ***')
    print(f'Product of position coordinates: {numpy.prod(position[0:2])}')

    position = numpy.array(INITIAL_POSITION)
    for step in route:
        position += numpy.array(DIRECTIONS_2[step[0]]) * step[1]
        if step[0] == 'forward':
            position[1] += position[2] * step[1]
        logging.debug(f'Position after {step=} is: {position=}')

    print('\n*** Second part of the assignment ***')
    print(f'Product of position coordinates: {numpy.prod(position[0:2])}')


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    main()
