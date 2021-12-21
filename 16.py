#!python3
"""
Day 16 of Advent of Code 2021
See: https://adventofcode.com/2021/day/16
"""

from __future__ import annotations
import bitstring
import logging
logging.basicConfig(level=logging.INFO)


IMPORT_FILE = '16.input'

PACKET_TYPE_SUM = 0
PACKET_TYPE_PRODUCT = 1
PACKET_TYPE_MIN = 2
PACKET_TYPE_MAX = 3
PACKET_TYPE_LITERAL = 4
PACKET_TYPE_GT = 5
PACKET_TYPE_LT = 6
PACKET_TYPE_EQ = 7

VERSION_BITS = slice(0, 3)
PACKET_ID_BITS = slice(3, 6)
LENGTH_ID_TYPE_BITS = slice(6, 7)
OPERATOR_VALUE_START = 6
LENGTH_ID_0_IDX = 7 + 15
LENGTH_ID_0_BITS = slice(7, LENGTH_ID_0_IDX)
LENGTH_ID_1_IDX = 7 + 11
LENGTH_ID_1_BITS = slice(7, LENGTH_ID_1_IDX)


class BITS_packet:
    bitarray: bitarray.BitArray = None
    remainder: bitarray.BitArray = None
    version: int = None
    packetid: int = None
    length_type_id: int = None
    length_value: int = None
    literal_value: int = None
    nested_packets: list[BITS_packet] = None

    def __init__(self) -> None:
        pass

    def _process_literal(self) -> None:
        val_str: str = ''
        for idx in range(OPERATOR_VALUE_START, len(self.bitarray), 5):
            val_str += self.bitarray[idx + 1: idx + 5].bin
            if not self.bitarray[idx]:
                # Stop looping if the first bit is 0
                break

        # Save the literal value
        self.literal_value = int(val_str, 2)

        # Save the remainder of the bit array
        self.remainder = self.bitarray[idx + 5:]

    def _get_data_from_bitarray(self) -> None:
        # Process header
        self.version = self.bitarray[VERSION_BITS].uint
        self.packetid = self.bitarray[PACKET_ID_BITS].uint

        logging.debug(f'Parsed: {self.version=} and {self.packetid=}')

        # Process literal
        if self.packetid == PACKET_TYPE_LITERAL:
            self._process_literal()
            logging.debug(f'Parsed literal: {self.literal_value}')
            return

        # Process operator
        self.length_type_id = self.bitarray[LENGTH_ID_TYPE_BITS].uint
        len_idx = LENGTH_ID_1_BITS if self.length_type_id else LENGTH_ID_0_BITS
        self.length_value = self.bitarray[len_idx].uint
        self.nested_packets = []

        logging.debug(f'Parsed operator: {self.length_type_id=} '
                      f'{self.length_value=}')

        # process length_type_id 1, number of sub packets is known
        if self.length_type_id:
            self.remainder = self.bitarray[LENGTH_ID_1_IDX:]
            for i in range(self.length_value):
                logging.debug(f'*** Getting package {i} for {str(self)}')
                package = BITS_packet.from_string(self.remainder.bin, 'bin')

                logging.debug(f'Parsed {self.remainder=} into {str(package)}')

                self.nested_packets.append(package)
                self.remainder = package.remainder
            return

        # process lenth_type_id 0, process a fixed number of bits
        self.remainder = self.bitarray[LENGTH_ID_0_IDX:]
        initial_bits = len(self.remainder)
        while initial_bits - len(self.remainder) < self.length_value:
            package = BITS_packet.from_string(self.remainder.bin, 'bin')

            logging.debug(f'Parsed {self.remainder=} into {str(package)}')

            self.nested_packets.append(package)
            self.remainder = package.remainder
        return

    def version_sum(self) -> int:
        sub_sum = 0
        if self.nested_packets:
            sub_sum = sum(p.version_sum() for p in self.nested_packets)
        return self.version + sub_sum

    def calculate(self) -> int:
        if self.packetid == PACKET_TYPE_SUM and self.nested_packets:
            return sum(p.calculate() for p in self.nested_packets)

        elif self.packetid == PACKET_TYPE_PRODUCT and self.nested_packets:
            prod = 1
            for p in self.nested_packets:
                prod *= p.calculate()
            return prod

        elif self.packetid == PACKET_TYPE_MIN and self.nested_packets:
            return min(p.calculate() for p in self.nested_packets)

        elif self.packetid == PACKET_TYPE_MAX and self.nested_packets:
            return max(p.calculate() for p in self.nested_packets)

        elif self.literal_value and self.packetid == PACKET_TYPE_LITERAL:
            return self.literal_value

        elif self.packetid == PACKET_TYPE_GT and self.nested_packets:
            values = [p.calculate() for p in self.nested_packets]
            return values[0] > values[1]

        elif self.packetid == PACKET_TYPE_LT and self.nested_packets:
            values = [p.calculate() for p in self.nested_packets]
            return values[0] < values[1]

        elif self.packetid == PACKET_TYPE_EQ and self.nested_packets:
            values = [p.calculate() for p in self.nested_packets]
            return values[0] == values[1]

        else:
            raise ValueError(f'Unknown packet id in packet: {str(self)}')

    def __str__(self):
        if self.literal_value:
            real_value = self.literal_value
            typestr = '(literal type)'
        else:
            real_value = ('Sub packet: - ' +
                          '\n -'.join(str(p) for p in self.nested_packets))
            typestr = '(nested package)'

        rem = self.remainder.bin if self.remainder else 'no remainder'

        return (f'Packet {typestr}: {self.bitarray.bin} -> {self.version=}, '
                f'{self.packetid=}, {rem}. Value: {real_value}')

    @classmethod
    def from_string(cls, string: str, type='hex') -> BITS_packet:
        result = cls()
        result.bitarray = bitstring.BitArray(**{type: str(string)})

        logging.debug(f'Parsed {type} {string} to {result.bitarray.bin}')

        result._get_data_from_bitarray()
        return result

    @classmethod
    def from_file(self, filename: str) -> BITS_packet:
        with open(filename, 'rt') as f:
            line = f.readline().strip()
            return BITS_packet.from_string(line)


def main():
    BITSmsg = BITS_packet.from_file(IMPORT_FILE)

    print('*** First part of the assignment ***')
    print(f'Sum of versions: {BITSmsg.version_sum()}')

    print('\n*** Second part of the assignment ***')
    print(f'Minimized risk: {BITSmsg.calculate()}')


if __name__ == "__main__":
    main()
