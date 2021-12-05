"""
Day 5 of Advent of Code 2021
See: https://adventofcode.com/2021/day/5
"""

import numpy
import collections
import logging
logging.basicConfig(level=logging.INFO)


IMPORT_FILE = '05.input'


def str_to_coord(string: str) -> list:
    return list(map(int, string.strip().split(',')))


def read_data():
    lines = []
    with open(IMPORT_FILE, 'rt') as filehandler:
        for line in filehandler:
            from_to = line.strip().split('->')
            lines.append([str_to_coord(string) for string in from_to])

    logging.debug(f'{len(lines)} read from {IMPORT_FILE}')
    return numpy.array(lines)


def _is_straight(from_xy: numpy.array, to_xy: numpy.array) -> bool:
    return any(from_xy[ax] == to_xy[ax] for ax in range(len(from_xy)))


def lines_to_graph(lines: numpy.array,
                   only_straight: bool = True) -> numpy.array:
    # Create a map based on the max x, y values
    graph = numpy.zeros(lines.max((0,)).max((0,)) + 1, dtype=int)
    logging.debug(f'Created map of size {graph.shape}')

    for from_xy, to_xy in lines:
        if _is_straight(from_xy, to_xy):
            minx, maxx = sorted([from_xy[0], to_xy[0]])
            miny, maxy = sorted([from_xy[1], to_xy[1]])
            graph[minx:maxx + 1, miny:maxy + 1] += 1

        elif not only_straight:
            dx = 1 if from_xy[0] < to_xy[0] else -1
            dy = 1 if from_xy[1] < to_xy[1] else -1
            for x, y in zip(range(from_xy[0], to_xy[0] + dx, dx),
                            range(from_xy[1], to_xy[1] + dy, dy)):
                graph[x, y] += 1

        logging.debug(f'{from_xy} -> {to_xy} '
                      f'straight line: {_is_straight(from_xy, to_xy)}; '
                      f'after drawing, {len(graph[graph > 0])} points on map; '
                      f'max lines crossings: {graph.max()} '
                      f'crossings count: {len(graph[graph > 1])}')

    return graph


def lines_to_pointdict(lines: numpy.array,
                       only_straight: bool = True) -> dict:
    points = collections.defaultdict(int)

    for from_xy, to_xy in lines:
        assert ((from_xy[0] == to_xy[0]) or  # vertical line
                (from_xy[1] == to_xy[1]) or  # horizontal line
                (abs(to_xy[0] - from_xy[0]) == abs(to_xy[1] - from_xy[1])))
                # diagnonal line

        dx = 1 if from_xy[0] <= to_xy[0] else -1
        dy = 1 if from_xy[1] <= to_xy[1] else -1

        if _is_straight(from_xy, to_xy) or not only_straight:
            x_range = list(range(from_xy[0], to_xy[0] + dx, dx))
            y_range = list(range(from_xy[1], to_xy[1] + dy, dy))
            if len(x_range) == 1:
                x_range = x_range * len(y_range)
            elif len(y_range) == 1:
                y_range = y_range * len(x_range)

            for x, y in zip(x_range, y_range):
                points[tuple([x, y])] += 1

    return points


def main():
    lines = read_data()

    points = lines_to_pointdict(lines, True)
    num_overlap = sum(1 for ct in points.values() if ct >= 2)

    print('*** First part of the assignment ***')
    print(f'Number of overlaps >= 2 is: {num_overlap}')

    points = lines_to_pointdict(lines, False)
    num_overlap = sum(1 for ct in points.values() if ct >= 2)

    print('\n*** Second part of the assignment ***')
    print(f'Number of overlaps >= 2 is: {num_overlap}')


if __name__ == "__main__":
    main()
