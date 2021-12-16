"""
--- Day 16: Packet Decoder ---
https://adventofcode.com/2021/day/16
"""
from typing import Tuple, List
from abc import ABC, abstractmethod

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
        self.packet_version = int(binary_input[:3], 2)
        self.packet_type_id = int(binary_input[3:6], 2)

    def __str__(self):
        return f"Packet Version: {self.packet_version} Packet Type ID: {self.packet_type_id}"


class Packet(ABC):
    def __init__(self, packet_header: PacketHeader, binary_input: str):
        self.packet_header = packet_header
        self.binary_input = binary_input

    @abstractmethod
    def parse(self) -> Tuple[int, str, List[int]]:
        pass

    def __str__(self):
        return (
            f"Packet Type: {self.__class__.__name__} \n"
            f"Header: {self.packet_header} \n"
            f"Binary String: {self.binary_input}"
        )


class LiteralValuePacket(Packet):
    def parse(self) -> Tuple[int, str, List[int]]:
        binary_representation = ""
        start_index, end_index = 6, 11
        group = self.binary_input[start_index:end_index]
        binary_representation += group[1:]
        while group.startswith("1"):
            start_index += 5
            end_index += 5
            group = self.binary_input[start_index:end_index]
            binary_representation += group[1:]
        return (
            int(binary_representation, 2),
            self.binary_input[end_index:],
            [self.packet_header.packet_version],
        )


class OperatorValuePacket(Packet):
    def __init__(self, packet_header: PacketHeader, binary_input: str):
        super().__init__(packet_header, binary_input)
        self.length_type_id = int(binary_input[6], 2)

    def parse(self) -> Tuple[int, str, List[int]]:
        if self.length_type_id == 0:
            return self.parse_bit_length_type()
        if self.length_type_id == 1:
            return self.parse_packet_length_type()
        raise Exception(f"Invalid length type id: {self.length_type_id}")

    def parse_bit_length_type(self) -> Tuple[int, str, List[int]]:
        bit_length = int(self.binary_input[7:22], 2)
        remaining_input = self.binary_input[22:]
        results = []
        pack_versions = [self.packet_header.packet_version]
        while int(remaining_input, 2) != 0:
            sub_packet = PacketFactory().fetch_packet_type(remaining_input)
            result, remaining_input, new_pack_versions = sub_packet.parse()
            pack_versions.extend(new_pack_versions)
            results.append(result)
        return sum(pack_versions), remaining_input, pack_versions

    def parse_packet_length_type(self) -> Tuple[int, str, List[int]]:
        num_sub_packets = int(self.binary_input[7:18], 2)
        results = []
        pack_versions = [self.packet_header.packet_version]
        remaining_input = self.binary_input[18:]
        while num_sub_packets != 0 and int(remaining_input, 2) != 0:
            sub_packet = PacketFactory().fetch_packet_type(remaining_input)
            result, remaining_input, new_pack_versions = sub_packet.parse()
            pack_versions.extend(new_pack_versions)
            results.append(result)
            num_sub_packets -= 1
        return sum(pack_versions), remaining_input, pack_versions


class PacketFactory:
    PACKET_TYPE_ID_LITERAL = 4

    def fetch_packet_type(self, binary_input: str) -> Packet:
        packet_header = PacketHeader(binary_input)
        if packet_header.packet_type_id == self.PACKET_TYPE_ID_LITERAL:
            return LiteralValuePacket(packet_header, binary_input)
        return OperatorValuePacket(packet_header, binary_input)


def create_binary_string_from_input(input_string: str) -> str:
    binary_string = ""
    for char in input_string:
        binary_string += hex_to_bin[char]
    return binary_string


with open("input.txt", "r") as file:
    binary_string = create_binary_string_from_input(file.readline().strip())

packet_factory = PacketFactory()
packet = packet_factory.fetch_packet_type(binary_string)
print(packet)
print(packet.parse())
