import typing
import logging


def _default_critical_msg(e: Exception, context: str = 'Unknown') -> str:
    return f'Got {e.__class__.__name__}: "{e}" in context {context}.'


def parse_input(filehandler: typing.TextIO,
                type_mapping: typing.Iterable[type],
                separator: str = None) -> list:
    """Returns a list of parsed and type mapped values from filehandler

    Args:
        filehandler (typing.TextIO): input file handler
        separator (str): separator string used for splitting elements in lines
        type_mapping (list[type]): mapping of datatypes for each line

    Returns:
        list: list of tuples with values
    """
    logging.debug(f'Parsing input file {filehandler.name}.')

    result = []
    for line in filehandler:

        # Strip and split line to lineitems
        if separator:
            try:
                lineitems = line.strip().split(separator)
            except Exception as e:
                logging.critical(_default_critical_msg(e), filehandler.name)
        else:
            lineitems = [line.strip()]

        logging.debug(f'Split line {line.strip()} into: {lineitems}')

        # map to the corresponding type and add to result
        try:
            result.append(tuple(
                type_map(element)
                for type_map, element in zip(type_mapping, lineitems)))
            logging.debug(f'Added parsed line as: {result[-1]}')

        except Exception as e:
            logging.critical(_default_critical_msg(e), filehandler.name)

    logging.info(f'Parsed {len(result)} values from {filehandler.name}.')

    return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()
