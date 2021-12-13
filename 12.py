#!python3
"""
Day 12 of Advent of Code 2021
See: https://adventofcode.com/2021/day/12
"""

import collections
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)


IMPORT_FILE = '12.input'


def import_graph(filename: str, directed=False) -> dict:
    """Import directed graph from filename into a dict

    The file is assumed to contain 'from'-'to'-pairs per line

    Args:
        filename (str): name of the file to be read
        directed: indicates if edges are directed (True) or bi-directional
                  (False). The default is False = bi-directional edges.

    Returns:
        dict(list): dict with nodes as keys and a list of nodes for edges
    """
    # Get the path of this Python file
    path = Path(__file__).with_name(filename)

    graph = dict()
    # Open file in the same path as this Python file
    with path.open('rt') as f:
        for line in f:
            node1, node2 = line.strip().split('-')
            if node1 in graph:
                graph[node1].append(node2)
            else:
                graph[node1] = [node2]
            if node2 in graph:
                graph[node2].append(node1)
            else:
                graph[node2] = [node1]

        return graph


def _node_allowed(path: tuple,
                  node: str,
                  start_node: str = 'start',
                  end_node: str = 'end',
                  extra_visit_rule: bool = False) -> bool:
    # Can't add anything if the path already has an end
    if end_node in path:
        return False

    # Start node can't be revisited
    if node == start_node:
        return False

    # No restrictions on uppercase nodes
    if node.isupper():
        return True

    # End node can only be visited once
    if node == end_node:
        if end_node in path:
            return False
        else:
            return True

    # Count nodes *after* adding node
    node_count = collections.Counter(n for n in path if n.islower())
    node_count[node] += 1

    if extra_visit_rule:
        max_visits = max(node_count.values())
        if max_visits > 2:
            return False
        elif max_visits == 2:
            return list(node_count.values()).count(max_visits) == 1
    else:  # not exra_visit_rule
        return all(ct <= 1 for ct in node_count.values())

    return True


def find_unique_paths(graph: dict,
                      start: str = 'start',
                      end: str = 'end',
                      extra_visit_rule: bool = False) -> list:
    paths = set([(start,)])

    while any(path[-1] != end for path in paths):
        for path in [path for path in paths if path[-1] != end]:
            for node in graph[path[-1]]:
                if _node_allowed(path, node, start, end, extra_visit_rule):
                    paths.add(path + (node,))
            paths.remove(path)
        logging.debug(f'{paths=}')

    return paths


def main():
    graph = import_graph(IMPORT_FILE)
    logging.debug(f'{graph=}')

    paths = find_unique_paths(graph, extra_visit_rule=False)

    print('*** First part of the assignment ***')
    print(f'Found {len(paths)} unique paths')

    paths = find_unique_paths(graph, extra_visit_rule=True)

    print('\n*** Second part of the assignment ***')
    print(f'Found {len(paths)} unique paths')


if __name__ == "__main__":
    main()
