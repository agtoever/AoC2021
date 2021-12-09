#!python3
"""
Day 9 of Advent of Code 2021
See: https://adventofcode.com/2021/day/9
"""

from pathlib import Path
import numpy as np
import logging
logging.basicConfig(level=logging.INFO)


IMPORT_FILE = '09.input'


def import_heights(filename: str) -> np.array:
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


def sum_lows(heights: np.array) -> int:
    """Find all low points in the heights array and add their values + 1

    Low points are point surrounded in horizontal and vertical directions
    with only higher values than themselves. Each low point is increased
    with 1 and then added together.

    Args:
        heights (np.array): 2d array with values

    Returns:
        int: sum of the low points

    Example:
    #  Low points are: 1, 0, 5 and 5. Each increased by 1 and summed is 15
    >>> sum_lows(np.array([ \
            [2, 1, 9, 9, 9, 4, 3, 2, 1, 0], \
            [3, 9, 8, 7, 8, 9, 4, 9, 2, 1], \
            [9, 8, 5, 6, 7, 8, 9, 8, 9, 2], \
            [8, 7, 6, 7, 8, 9, 6, 7, 8, 9], \
            [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]]))
    15
    """
    logging.debug(f'Finding low points for {heights}')
    # Pad heights with 10's
    padded_heights = np.pad(heights, pad_width=1,
                            mode='constant', constant_values=10)

    # Min heights = True if cell is lower than all of the adjacent cells
    min_heights = np.array(
        [[all(padded_heights[r, c] < padded_heights[r + dr, c + dc]
              for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)])
          for c in range(1, heights.shape[1] + 1)]
         for r in range(1, heights.shape[0] + 1)])

    logging.debug(f'Boolean array with True at Low points: {min_heights=}')

    # Sum the points where heigt == min_height + 1
    return sum(heights[min_heights] + 1)


def fill_count(heights: np.array) -> np.array:
    """Fills each 9-enclodes areas with an unique, consecutive number

    Args:
        heights (np.array): 2d numpy area with values 0-9

    Returns:
        np.array: 2d numpy area with 0 as border and 1, 2, 3... as area's

    Example:
    >>> areas = fill_count(np.array([ \
            [2, 1, 9, 9, 9, 4, 3, 2, 1, 0], \
            [3, 9, 8, 7, 8, 9, 4, 9, 2, 1], \
            [9, 8, 5, 6, 7, 8, 9, 8, 9, 2], \
            [8, 7, 6, 7, 8, 9, 6, 7, 8, 9], \
            [9, 8, 9, 9, 9, 6, 5, 6, 7, 8]]))

    >>> areas
    array([[1, 1, 0, 0, 0, 2, 2, 2, 2, 2],
           [1, 0, 3, 3, 3, 0, 2, 0, 2, 2],
           [0, 3, 3, 3, 3, 3, 0, 4, 0, 2],
           [3, 3, 3, 3, 3, 0, 4, 4, 4, 0],
           [0, 3, 0, 0, 0, 4, 4, 4, 4, 4]])

    # Now you can easily calculate the sizes of the area's.
    # Note that area 0 is the border.
    >>> dict(zip(*np.unique(areas, return_counts=True)))
    {0: 15, 1: 3, 2: 9, 3: 14, 4: 9}

    """
    # Create a copy of heights. Set border to -1 and fill area's to -2
    h = np.copy(heights)
    h[h == 9] = -1
    h[h != -1] = -2

    # Loop while there are still unindexed area's (elements with value -2)
    area_counter = 1
    while -2 in h:
        # init some book keeping
        area_size = 1
        old_area_size = 0
        indices = [list(zip(*np.where(h == -2)))[0]]
        h[indices[0]] = area_counter

        logging.debug(f'Filling area {area_counter}, '
                      f'starting at index {indices[0]}')

        # Keep going until the area can't be expanded anymore
        while area_size > old_area_size:
            old_area_size = area_size
            # Check all surrounding cells of the current marked area for -2's
            for r, c in indices:
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if (0 <= r + dr < h.shape[0] and
                        0 <= c + dc < h.shape[1] and
                            h[r + dr, c + dc] == -2):
                        # Found a -2 cell; add it to the area
                        h[r + dr, c + dc] = area_counter
                        indices.append(tuple([r + dr, c + dc]))
                        area_size += 1

        logging.debug(f'Filled area {area_counter} of size {area_size}')

        # Go to the next area
        area_counter += 1

    # Finally, set border to 0 (was: -1)
    h[h == -1] = 0

    return h


def main():
    heights = import_heights(IMPORT_FILE)
    low_sum = sum_lows(heights)

    print('*** First part of the assignment ***')
    print(f'Sum of lows is {low_sum}')

    # Mark all area's, count their sizes
    marked = fill_count(heights)
    area_counts = dict(zip(*np.unique(marked, return_counts=True)))
    del area_counts[0]  # remove the border itself from the counts

    logging.debug(f'Found areas (index: size): {area_counts}')

    # Multiply the largest 3 sizes for the answer
    product_largest_3 = np.prod(sorted(area_counts.values())[-3:])

    print('\n*** Second part of the assignment ***')
    print(f'Sum of all digit outputs {product_largest_3}')


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    main()
