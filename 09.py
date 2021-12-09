"""
Day 9 of Advent of Code 2021
See: https://adventofcode.com/2021/day/9
"""

import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG)


IMPORT_FILE = '09.input'


def fill_count(heights: np.array) -> np.array:
    """Fills each 9-enclodes areas with an unique, consecutive number

    Args:
        heights (np.array): 2d numpy area with values 0-9

    Returns:
        np.array: 2d numpy area with 0 as border and 1, 2, 3... as area's
    
    Example:
    >>> import numpy as np
    >>> 
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

        # Go to the next area
        area_counter += 1

    # Finally, set border to 0 (was: -1)
    h[h == -1] = 0

    return h


def main():
    # Import data into numpy array
    with open(IMPORT_FILE, 'rt') as f:
        heights = np.array([[int(c) for c in list(s.strip())] for s in f])

    # Pad heights with 10's
    padded_heights = np.pad(heights, pad_width=1,
                            mode='constant', constant_values=10)

    # Min heights = True if cell is lower than all of the adjacent cells
    min_heights = np.array(
        [[all(padded_heights[r, c] < padded_heights[r + dr, c + dc]
              for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)])
          for c in range(1, heights.shape[1] + 1)]
         for r in range(1, heights.shape[0] + 1)])

    # Sum the points where heigt == min_height + 1
    sum_lows = sum(heights[min_heights] + 1)

    print('*** First part of the assignment ***')
    print(f'Sum of lows is {sum_lows}')

    marked = fill_count(heights)
    area_counts = dict(zip(*np.unique(marked, return_counts=True)))
    del area_counts[0]  # remove the border itself from the counts
    product_largest_3 = np.prod(sorted(area_counts.values())[-3:])

    print('\n*** Second part of the assignment ***')
    print(f'Sum of all digit outputs {product_largest_3}')


if __name__ == "__main__":
    main()
