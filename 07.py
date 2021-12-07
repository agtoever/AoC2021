"""
Day 7 of Advent of Code 2021
See: https://adventofcode.com/2021/day/7
"""

import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG)


IMPORT_FILE = '07.input'


def distance_to_fuel(positions: np.array,
                     pos: int) -> int:
    """Returns fuel needed for all elements to travel from positions to pos
    For distance d, this is sum(range(d+1)) = d * (d + 1) / 2

    Args:
        positions (np.array): array of positions
        pos (int): position to travel to

    Returns:
        int: amount of fuel needed
    """
    distances = np.abs(positions - pos)
    return sum(map(lambda d: d * (d + 1) / 2, distances))


def find_optimal_position(positions: np.array) -> int:
    """Finds the optimal position by brute force

    Args:
        positions (np.array): positions

    Returns:
        int: optimal position
    """
    fuels = [distance_to_fuel(pos, positions)
             for pos in range(len(positions))]
    return fuels.index(min(fuels))


def main():
    positions = np.loadtxt(IMPORT_FILE, dtype=int, delimiter=',')

    opt_pos = np.median(positions)
    sum_dist = np.abs(positions - opt_pos).sum()
    print('*** First part of the assignment ***')
    print(f'Optimal position is {opt_pos}; sum distances = {sum_dist}')

    opt_pos = find_optimal_position(positions)
    sum_fuel = distance_to_fuel(positions, opt_pos)
    print('\n*** Second part of the assignment ***')
    print(f'Optimal position is {opt_pos}; sum distances = {sum_fuel}')


if __name__ == "__main__":
    main()
