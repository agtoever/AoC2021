"""
Day 5 of Advent of Code 2021
See: https://adventofcode.com/2021/day/5
"""

import numpy
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


def main():
    lines = read_data()

    graph = lines_to_graph(lines, only_straight=True)
    num_overlap = len(graph[graph >= 2])

    print('*** First part of the assignment ***')
    print(f'Number of overlaps >= 2 is: {num_overlap}')

    graph = lines_to_graph(lines, only_straight=False)
    num_overlap = len(graph[graph >= 2])

    print('\n*** Second part of the assignment ***')
    print(f'Number of overlaps >= 2 is: {num_overlap}')


if __name__ == "__main__":
    main()
