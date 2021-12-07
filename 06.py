"""
Day 6 of Advent of Code 2021
See: https://adventofcode.com/2021/day/6
"""

import numpy as np
import logging
logging.basicConfig(level=logging.INFO)


IMPORT_FILE = '06.input'
JUV_TIMER = 8
SIMULATION_LENGTH1 = 80
SIMULATION_LENGTH2 = 256
TRANSITION_MATRIX = np.array([
    # 0  1  2  3  4  5  6  7  8
    [0, 1, 0, 0, 0, 0, 0, 0, 0],  # 0; from 1 to 0
    [0, 0, 1, 0, 0, 0, 0, 0, 0],  # 1; from 2 to 1
    [0, 0, 0, 1, 0, 0, 0, 0, 0],  # 2; from 3 to 2
    [0, 0, 0, 0, 1, 0, 0, 0, 0],  # 3; from 4 to 3
    [0, 0, 0, 0, 0, 1, 0, 0, 0],  # 4; from 5 to 4
    [0, 0, 0, 0, 0, 0, 1, 0, 0],  # 5; from 6 to 5
    [1, 0, 0, 0, 0, 0, 0, 1, 0],  # 6; from 7 to 6 AND from 0 to 6
    [0, 0, 0, 0, 0, 0, 0, 0, 1],  # 7; from 8 to 7
    [1, 0, 0, 0, 0, 0, 0, 0, 0],  # 8; from 0 to 8
])

"""
Old simulation approach.
Works for the first part of the question, but is way too slow 
for the second part...


INITIAL_TIMER = 6


def simulate_fish(timers: np.array,
                  sim_length: int) -> np.array:
    logging.debug(f'Day 0: {len(timers)} fish. '
                  f'Simulating for {sim_length} days.')

    for day in range(1, sim_length + 1):
        # Progress timers
        timers -= 1

        # Index those fish with timer == -1 (previous cycle: 0)
        reset_idx = np.where(timers == -1)
        logging.debug(f'Resetting {len(reset_idx)}fish.')

        # Reset the timer for those fish
        timers[reset_idx] = INITIAL_TIMER

        # Create new fish for those fish who timer was 0
        new_fish = np.array([JUV_TIMER] * len(reset_idx[0]), dtype=int)
        timers = np.append(timers, new_fish)

        logging.debug(f'After day {day}: {len(timers)}.')

    return timers
"""


def calculate_fish(timers: np.array,
                   sim_length: int) -> int:
    """Calculates how many fish there are after sim_length of time

    Args:
        timers (np.array): list of timers. One element for each fish
        sim_length (int): duration of the simulation

    Returns:
        int: total number of fish at the end of the simulation
    """
    vector = np.array([sum(timers == age) for age in range(JUV_TIMER + 1)])
    logging.debug(f'Converted {timers=} to {vector} counts.')

    trans_matrix = np.linalg.matrix_power(TRANSITION_MATRIX, sim_length)
    end_counts = trans_matrix.dot(vector)
    logging.debug(f'After {sim_length=}, {timers=} is: {end_counts=}.')

    return end_counts.sum()


def main():
    timers = np.loadtxt(IMPORT_FILE, dtype=int, delimiter=',')
    fish_count = calculate_fish(timers, SIMULATION_LENGTH1)

    print('*** First part of the assignment ***')
    print(f'Number of fish after {SIMULATION_LENGTH1} days: {fish_count}.')

    fish_count = calculate_fish(timers, SIMULATION_LENGTH2)
    print('\n*** Second part of the assignment ***')
    print(f'Number of fish after {SIMULATION_LENGTH2} days: {fish_count}.')


if __name__ == "__main__":
    main()
