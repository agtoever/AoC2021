#!python3
"""
Day 15 of Advent of Code 2021
See: https://adventofcode.com/2021/day/15
"""

from __future__ import annotations
from skimage import graph
import numpy as np
from pathlib import Path
import logging
logging.basicConfig(level=logging.DEBUG)


IMPORT_FILE = '15.input'


def import_risk_lvl(filename: str) -> np.array:
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


def expand_riskmap(riskmap: np.array, copies: int = 1) -> np.array:
    result = np.copy(riskmap)
    for axis in range(len(riskmap.shape)):  # loop over axis
        riskmap_cpy = np.copy(result)
        for cpy in range(copies):
            riskmap_cpy = np.copy(riskmap_cpy) + 1
            riskmap_cpy[riskmap_cpy > 9] = 1
            result = np.concatenate((result, riskmap_cpy), axis=axis)
    return result


def minimize_risk(risk_lvls: np.array) -> int:
    cost = graph.MCP(risk_lvls, fully_connected=False)
    rows, cols = risk_lvls.shape
    endpt = (rows - 1, cols - 1)
    cum_costs, _ = cost.find_costs(starts=[(0, 0)], ends=[endpt])
    return int(cum_costs[-1, -1] - risk_lvls[0, 0])


def main():
    risk_lvls = import_risk_lvl(IMPORT_FILE)
    end_risk = minimize_risk(risk_lvls)

    print('*** First part of the assignment ***')
    print(f'Minimized risk: {end_risk}')

    risk_lvls = expand_riskmap(risk_lvls, 4)
    end_risk = minimize_risk(risk_lvls)

    print('\n*** Second part of the assignment ***')
    print(f'Minimized risk: {end_risk}')


if __name__ == "__main__":
    main()
