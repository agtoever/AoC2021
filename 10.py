#!python3
"""
Day 10 of Advent of Code 2021
See: https://adventofcode.com/2021/day/10
"""

from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)


IMPORT_FILE = '10.input'
ERROR_SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
AUTOCOMPLETE_SCORES = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}
CHUNK__START_CHARACTERS = list('([{<')
CHUNK_END_CHARACTERS = list(')]}>')
CHUNK_CHARACTER_PAIRS = dict(zip(CHUNK__START_CHARACTERS,
                                 CHUNK_END_CHARACTERS))


def import_lines(filename: str) -> list:
    """Import file from filename into a list

    Args:
        filename (str): name of the file to be read

    Returns:
        list: List of lines from the file
    """
    # Get the path of this Python file
    path = Path(__file__).with_name(filename)

    # Open file in the same path as this Python file
    with path.open('rt') as f:
        return [line.strip() for line in f]


def score_syntax_errors(line: str) -> int:
    """Checks the syntax of line and returns its score if it has an error

    Args:
        line (str): line to be parsed

    Raises:
        ValueError: if an invalid character is encountered

    Returns:
        int: score if a syntax error is found
    """
    stack = []
    for c in line:
        if c in CHUNK__START_CHARACTERS:
            stack.append(CHUNK_CHARACTER_PAIRS[c])
        elif c in CHUNK_END_CHARACTERS:
            if c != stack.pop():
                return ERROR_SCORES[c]
        else:
            raise ValueError(f'Invalid character in line {line}: {c}')
    return 0


def score_autocomplete(line: str) -> int:
    """Checks the completeness of line and returns its score if incomplete

    Args:
        line (str): line to be parsed

    Raises:
        ValueError: if an invalid character is encountered

    Returns:
        int: score if an incomplete line is found; 0 if line with syntax error
    """
    stack = []
    for c in line:
        if c in CHUNK__START_CHARACTERS:
            stack.append(CHUNK_CHARACTER_PAIRS[c])
        elif c in CHUNK_END_CHARACTERS:
            if c != stack.pop():
                return 0  # line with syntax error; return 0
        else:
            raise ValueError(f'Invalid character in line {line}: {c}')

    return sum(5 ** n * AUTOCOMPLETE_SCORES[c] for n, c in enumerate(stack))


def main():
    lines = import_lines(IMPORT_FILE)
    sum_syntax_score = sum([score_syntax_errors(line) for line in lines])

    print('*** First part of the assignment ***')
    print(f'Sum of error scores is: {sum_syntax_score}')

    autocomplete_scores = [score for score in
                           [score_autocomplete(line) for line in lines]
                           if score > 0]
    median_score = sorted(autocomplete_scores)[len(autocomplete_scores) // 2]

    print('\n*** Second part of the assignment ***')
    print(f'Median score of autocomplete scores is: {median_score}')


if __name__ == "__main__":
    main()
