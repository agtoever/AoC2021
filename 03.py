"""
Day 3 of Advent of Code 2021
See: https://adventofcode.com/2021/day/3
"""


import AoC
import logging
import numpy
logging.basicConfig(level=logging.INFO)


IMPORT_FILE = '03.input'


def bitlist_to_int(bitlist: list) -> int:
    """Converts a list of Truthy values (bits) to an integer value

    Args:
        bitlist (list): list of truthy/falsy values (0/1, True/False, ...)

    Returns:
        int: integer value of the bitlist
    """
    return sum(i * 2 ** n for n, i in enumerate(bitlist[::-1]))


def _bit_criteria(report: list, select_func: callable = numpy.argmax) -> int:
    """Applies the bit criteria on report with selection criterium select_func

    Args:
        report (list): list of reported values
        select_func (callable, optional): Defaults to numpy.argmax.

    Returns:
        int: integer value of the filtered bitlist
    """
    filtered = numpy.copy(report)

    # Append a column of 1s for argmax for a tie in 1s and 0s
    # if select_func == numpy.argmax:
    #    filtered = numpy.c_[filtered, [1] * len(filtered)]

    column = 0
    while len(filtered) > 1:
        counts = numpy.bincount(filtered[:, column])
        if counts[0] == counts[1]:
            selected = select_func([0, 1])
        else:
            selected = select_func(counts)

        filtered = filtered[filtered[:, column] == selected, :]
        column += 1

        logging.debug(f'{len(filtered)} items left after filtering.')

    logging.debug(f'Bit criteria with {select_func.__name__}: {filtered[0]}')
    return bitlist_to_int(filtered[0])


def calculate_oxygen_generator_rating(report: list) -> int:
    """Calculate the oxygen generator rating

    Args:
        report (list): list of reported values

    Returns:
        int: Oxygen generator rating
    """
    oxy = _bit_criteria(report, numpy.argmax)
    logging.debug(f'Oxygen generator rating = {oxy}')
    return oxy


def calculate_co2_scrubber_rating(report: list) -> int:
    """Calculate the co2 scrubber rating

    Args:
        report (list): list of reported values

    Returns:
        int: co2 scrubber rating
    """
    co2scrub = _bit_criteria(report, numpy.argmin)
    logging.debug(f'CO2 scrubber rating = {co2scrub}')
    return co2scrub


def main():
    with open(IMPORT_FILE, 'rt') as filehandler:
        report = AoC.parse_input(filehandler, [list], '')

    # Convert to numpy array of integer values (0/1)
    report = numpy.array([list(map(int, item[0])) for item in report])

    # Transpose, do a bincount an get the argmax/argmin for each row
    report_t = numpy.copy(report).transpose()
    gamma_rate = bitlist_to_int(
        [numpy.bincount(column).argmax() for column in report_t])
    epsilon_rate = bitlist_to_int(
        [numpy.bincount(column).argmin() for column in report_t])

    print('*** First part of the assignment ***')
    print(f'Power consumtion = {gamma_rate * epsilon_rate}')

    oxy = calculate_oxygen_generator_rating(report)
    co2 = calculate_co2_scrubber_rating(report)

    print('\n*** Second part of the assignment ***')
    print(f'Life support rating = {oxy * co2}')


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    main()
