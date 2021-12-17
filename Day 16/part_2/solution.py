"""
--- Day 16: Packet Decoder ---
--- Part 2 ---
https://adventofcode.com/2021/day/16
"""
from typing import List, Dict, Type
from abc import ABC, abstractmethod
import math

hex_to_bin = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


class PacketHeader:
    def __init__(self, binary_input: str):
        self.packet_version: int = int(binary_input[:3], 2)
        self.packet_type_id: int = int(binary_input[3:6], 2)

    def __str__(self):
        return f"Packet Version: {self.packet_version} Packet Type ID: {self.packet_type_id}"


class Packet(ABC):

    PACKET_HEADER_LENGTH = 6

    def __init__(self, packet_header: PacketHeader, binary_input: str):
        self.packet_header: PacketHeader = packet_header
        self.binary_input: str = binary_input
        self.bit_len: int = self.PACKET_HEADER_LENGTH

    @abstractmethod
    def parse(self) -> int:
        pass

    def __str__(self):
        return (
            f"Packet Type: {self.__class__.__name__} \n"
            f"Header: {self.packet_header} \n"
            f"Binary String: {self.binary_input}"
        )


class LiteralValuePacket(Packet):

    LITERAL_PART_BIT_LENGTH = 5

    def parse(self) -> int:
        binary_representation = ""
        start_index, end_index = self.PACKET_HEADER_LENGTH, 11
        group = self.binary_input[start_index:end_index]
        binary_representation += group[1:]
        self.bit_len += self.LITERAL_PART_BIT_LENGTH
        while group.startswith("1"):
            start_index += self.LITERAL_PART_BIT_LENGTH
            end_index += self.LITERAL_PART_BIT_LENGTH
            self.bit_len += self.LITERAL_PART_BIT_LENGTH
            group = self.binary_input[start_index:end_index]
            # Remove leading 1 or 0 since it's not part of the number.
            binary_representation += group[1:]
        return int(binary_representation, 2)


class OperatorValuePacket(Packet, ABC):

    LENGTH_TYPE_INDEX = 7
    BIT_LENGTH_TYPE_END_INDEX = 22
    PACKET_COUNT_TYPE_END_INDEX = 18

    LENGTH_TYPE_BIT = 0
    LENGTH_TYPE_SUBPACKET_COUNT = 1

    def __init__(self, packet_header: PacketHeader, binary_input: str):
        super().__init__(packet_header, binary_input)
        self.length_type_id = int(binary_input[self.bit_len], 2)
        self.bit_len = self.LENGTH_TYPE_INDEX

    def parse(self) -> int:
        if self.length_type_id == self.LENGTH_TYPE_BIT:
            return self.parse_bit_length_type()
        if self.length_type_id == self.LENGTH_TYPE_SUBPACKET_COUNT:
            return self.parse_packet_length_type()
        raise Exception(f"Invalid length type id: {self.length_type_id}")

    def parse_bit_length_type(self) -> int:
        # Parse out the binary value representing how many bits are left in this packet.
        remaining_bit_length = int(
            self.binary_input[self.LENGTH_TYPE_INDEX : self.BIT_LENGTH_TYPE_END_INDEX],
            2,
        )
        # Now we know our total bit length for this packet.
        self.bit_len = self.BIT_LENGTH_TYPE_END_INDEX + remaining_bit_length

        # Get the rest of the packet less the header/length info.
        remaining_input = self.binary_input[
            self.BIT_LENGTH_TYPE_END_INDEX : self.bit_len
        ]

        results = []
        while len(remaining_input) != 0:
            # Get the first sub-packet.
            sub_packet = PacketFactory.fetch_packet_type(remaining_input)
            # Parse it, this will also parse the sub-packets of the sub-packet.
            results.append(sub_packet.parse())
            # Figure out what we have left to parse out now that we know the bit length of the sub-packet.
            remaining_input = remaining_input[sub_packet.bit_len :]
        # Apply this packets operator on the results.
        return self.operation(results)

    def parse_packet_length_type(self) -> int:
        # Parse out the binary value representing how many sub packets are in this packet.
        num_sub_packets = int(
            self.binary_input[
                self.LENGTH_TYPE_INDEX : self.PACKET_COUNT_TYPE_END_INDEX
            ],
            2,
        )
        # We know our bit length is AT LEAST the header plus the packet count value.
        self.bit_len = self.PACKET_COUNT_TYPE_END_INDEX

        # Remove the header and packet count value and parse sub-packets.
        remaining_input = self.binary_input[self.PACKET_COUNT_TYPE_END_INDEX :]

        sub_packets_parsed = 0
        results = []
        while sub_packets_parsed < num_sub_packets:
            # Get the first sub-packet.
            sub_packet = PacketFactory.fetch_packet_type(remaining_input)
            # Parse it, this will also parse the sub-packets of the sub-packet.
            results.append(sub_packet.parse())
            # Figure out what we have left to parse out now that we know the bit length of the sub-packet.
            remaining_input = remaining_input[sub_packet.bit_len :]
            # Now that we know the sub-packet length, add it to the total length of this packet.
            self.bit_len += sub_packet.bit_len
            sub_packets_parsed += 1
        # Apply this packets operator on the results.
        return self.operation(results)

    @abstractmethod
    def operation(self, results: List[int]) -> int:
        pass


class SumOperatorPacket(OperatorValuePacket):
    def operation(self, results: List[int]) -> int:
        return sum(results)


class ProductOperatorPacket(OperatorValuePacket):
    def operation(self, results: List[int]) -> int:
        return math.prod(results)


class MinimumOperatorPacket(OperatorValuePacket):
    def operation(self, results: List[int]) -> int:
        return min(results)


class MaximumOperatorPacket(OperatorValuePacket):
    def operation(self, results: List[int]) -> int:
        return max(results)


class GreaterThanOperatorPacket(OperatorValuePacket):
    def operation(self, results: List[int]) -> int:
        return 1 if results[0] > results[1] else 0


class LessThanOperatorPacket(OperatorValuePacket):
    def operation(self, results: List[int]) -> int:
        return 1 if results[0] < results[1] else 0


class EqualToOperatorPacket(OperatorValuePacket):
    def operation(self, results: List[int]) -> int:
        return 1 if results[0] == results[1] else 0


class PacketFactory:
    PACKET_TYPE_ID_SUM = 0
    PACKET_TYPE_ID_PRODUCT = 1
    PACKET_TYPE_ID_MINIUMUM = 2
    PACKET_TYPE_ID_MAXIMUM = 3
    PACKET_TYPE_ID_LITERAL = 4
    PACKET_TYPE_ID_GREATER_THAN = 5
    PACKET_TYPE_ID_LESS_THAN = 6
    PACKET_TYPE_ID_EQUAL_TO = 7

    factory: Dict[int, Type[Packet]] = {
        PACKET_TYPE_ID_SUM: SumOperatorPacket,
        PACKET_TYPE_ID_PRODUCT: ProductOperatorPacket,
        PACKET_TYPE_ID_MINIUMUM: MinimumOperatorPacket,
        PACKET_TYPE_ID_MAXIMUM: MaximumOperatorPacket,
        PACKET_TYPE_ID_LITERAL: LiteralValuePacket,
        PACKET_TYPE_ID_GREATER_THAN: GreaterThanOperatorPacket,
        PACKET_TYPE_ID_LESS_THAN: LessThanOperatorPacket,
        PACKET_TYPE_ID_EQUAL_TO: EqualToOperatorPacket,
    }

    @staticmethod
    def fetch_packet_type(binary_input: str) -> Packet:
        packet_header = PacketHeader(binary_input)
        if packet_header.packet_type_id not in PacketFactory.factory:
            raise TypeError(f"Invalid packet type id: {packet_header.packet_type_id}")
        return PacketFactory.factory[packet_header.packet_type_id](
            packet_header, binary_input
        )


def create_binary_string_from_input(input_string: str) -> str:
    binary_string = ""
    for char in input_string:
        binary_string += hex_to_bin[char]
    return binary_string


with open("input.txt", "r") as file:
    binary_string = create_binary_string_from_input(file.readline().strip())

packet = PacketFactory.fetch_packet_type(binary_string)
print(packet.parse())
