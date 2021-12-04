"""
Day 4 of Advent of Code 2021
See: https://adventofcode.com/2021/day/4
"""


import numpy
import logging
logging.basicConfig(level=logging.DEBUG)


IMPORT_FILE = '04.input'
BOARD_SIZE = 5


def read_data():
    boards = []
    with open(IMPORT_FILE, 'rt') as filehandler:
        draws = numpy.array(filehandler.readline().strip().split(','),
                            dtype=int)

        while filehandler.readline() != '':
            boards.append(
                [list(map(int, filehandler.readline().strip().split()))
                 for _ in range(BOARD_SIZE)])

    return draws, numpy.array(boards)


def main():
    draws, boards = read_data()
    logging.debug(f'{draws=}')
    logging.debug(f'{boards=}')

    winning_boards = []
    boardsum = 0
    for round, draw in enumerate(draws):
        # Set all drawn numbers to -1
        boards[boards == draw] = -1

        logging.debug(f'Round: {round}. {draw=}. '
                      f'Matched numers: {(boards == -1).sum()}')

        # If a column / row is full, its sum is -BOARD_SIZE
        for ax in [1, 2]:
            if -BOARD_SIZE in boards.sum((ax,)):
                for board in numpy.where(boards.sum((ax,)) == -BOARD_SIZE)[0]:
                    if board not in winning_boards:
                        winning_boards.append(board)

        # Save the data for the first winning board
        if winning_boards and boardsum == 0:
            win_board = winning_boards[0]
            boardsum1 = boards[win_board][boards[win_board] > 0].sum()
            winning_draw = draw

            logging.debug(f'Winning board is board {win_board}:\n'
                          f'{boards[win_board]}.\n'
                          f'Sum is: {boardsum1}.\n'
                          f'Last draw was: {draw}.')

        # Stop when all boards have won
        if len(winning_boards) == len(boards):
            break

    print('*** First part of the assignment ***')
    print(f'Final score = {boardsum1 * winning_draw}')

    last_board = winning_boards[-1]
    boardsum2 = boards[last_board][boards[last_board] > 0].sum()
    last_draw = draw

    print('\n*** Second part of the assignment ***')
    print(f'Final score = {boardsum2 * last_draw}')


if __name__ == "__main__":
    main()
