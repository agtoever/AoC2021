#!python3
"""
Day 11 of Advent of Code 2021
See: https://adventofcode.com/2021/day/11
"""

from pathlib import Path
import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG)


IMPORT_FILE = '11.input'
FLASH_THRESHOLD = 9
ADJACENT_OFFSETS = [(-1, -1), (-1, 0), (-1, 1),
                    (0, -1), (0, 1),
                    (1, -1), (1, 0), (1, 1)]


def import_energy(filename: str) -> np.array:
    """Import file from filename into a numpy array

    The file is assumed to contain values from 0-9 without separators.

    Args:
        filename (str): name of the file to be read

    Returns:
        np.array: Numpy array with the data from the file
    """
    # Get the path of this Python file
    path = Path(__file__).with_name(filename)

     # Open file in the same path as this Python file
    with path.open('rt') as f:
        return np.array([[int(c) for c in list(s.strip())] for s in f])


def process_step(energy: np.array) -> np.array:
    # Increase energy by 1
    energy += 1

    # Let all with energy > threshold flash and increase adjacent
    # Continue until there are not more cascasing flashes
    flashed = []
    while len(energy[energy > FLASH_THRESHOLD]) > len(flashed):
        for r, c in zip(*np.where(energy > FLASH_THRESHOLD)):
            if (r, c) not in flashed:
                flashed.append((r, c))
                for dr, dc in ADJACENT_OFFSETS:
                    if (0 <= r + dr < energy.shape[0] and
                            0 <= c + dc < energy.shape[1]):
                        energy[r + dr, c + dc] += 1

    # Last past of a step: all that flashed are reset to energy 0
    energy[energy > FLASH_THRESHOLD] = 0

    return energy


def main():
    energy = import_energy(IMPORT_FILE)

    energy1 = np.copy(energy)
    num_flashes = 0
    for step in range(100):
        energy1 = process_step(energy1)
        num_flashes += len(energy1[energy1 == 0])

    print('*** First part of the assignment ***')
    print(f'Number of flashes in 100 steps: {num_flashes}')

    energy2 = np.copy(energy)
    step = 0
    while energy2.sum() > 0:
        energy2 = process_step(energy2)
        step += 1

    print('\n*** Second part of the assignment ***')
    print(f'All flashed after {step} steps')


if __name__ == "__main__":
    main()
