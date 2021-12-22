#!python3
"""
Day 17 of Advent of Code 2021
See: https://adventofcode.com/2021/day/17
"""

from __future__ import annotations
import logging
import itertools
from pathlib import Path
logging.basicConfig(level=logging.INFO)


IMPORT_FILE = '17.input'


def import_target_zone(filename: str) -> list:
    """Import file from filename into a list with min/max x/y pairs

    Args:
        filename (str): name of the file to be read

    Returns:
        list[tuple]: [(min_x, max_x), (min_y, max_y)]
    """
    # Get the path of this Python file
    path = Path(__file__).with_name(filename)

    # Open file in the same path as this Python file
    with path.open('rt') as f:
        s = f.readline().strip()
        x = tuple(int(v) for v in s.split('x=')[1].split(',')[0].split('..'))
        y = tuple(int(v) for v in s.split('y=')[1].split(',')[0].split('..'))
        return [x, y]


def distance(start_v, end_v):
    return int(1/2 * (start_v + end_v) * (start_v - end_v + 1))


def find_xy(min_x, max_x, min_y, max_y) -> list:
    x_solutions = set()
    for begin_vx in range(max_x + 1):
        pos = 0
        vx = begin_vx
        while pos <= max_x and vx > 0:
            pos += vx
            vx = max(vx - 1, 0)
            if min_x <= pos <= max_x:
                # Store result: begin speed, speed at pos, steps and pos
                x_solutions.add((begin_vx, vx, begin_vx - vx, pos))

    logging.debug(f'Found all x solutions: {sorted(x_solutions)}')

    y_solutions = set()
    for begin_vy in range(min_y - 1, max(-min_y, max_y) + 1):
        pos = 0
        vy = begin_vy
        while pos > min_y:
            pos += vy
            vy -= 1
            if min_y <= pos <= max_y:
                # Store result: begin speed, speed at pos, steps and pos
                y_solutions.add((begin_vy, vy, begin_vy - vy, pos))

    logging.debug(f'Found all y solutions: {sorted(y_solutions)}')

    valid_xy = set()
    for x_solution, y_solution in itertools.product(x_solutions, y_solutions):
        # There are two conditions: the index is equal OR the y index is
        # bigger and the x-speed had reached zero.
        if ((x_solution[2] == y_solution[2]) or
                (y_solution[2] > x_solution[2] and x_solution[1] == 0)):
            valid_xy.add((x_solution[0], y_solution[0]))

    logging.debug(f'Matching (x, y) solutions: {sorted(valid_xy)}')

    return sorted(valid_xy)


def main():
    target_zone = import_target_zone(IMPORT_FILE)
    logging.debug(f'{target_zone=}')

    # If start_y = -min_y + 1, it maximizes height; it lands exactly
    # at the bottom of the target area (coordinate y_min).
    # It's height = 1/2 * (-min_y+1) * -min_y
    max_height = target_zone[1][0] * (target_zone[1][0] + 1) // 2

    """ This code is now obsolete (but works!):
    start_vy = find_y(*target_zone[1])
    max_height = distance(*start_vy[-1])
    """

    print('*** First part of the assignment ***')
    print(f'Sum of versions: {max_height}')

    valid_xy = find_xy(*target_zone[0], *target_zone[1])

    print('\n*** Second part of the assignment ***')
    print(f'Found {len(valid_xy)} solutions.')


if __name__ == "__main__":
    main()
