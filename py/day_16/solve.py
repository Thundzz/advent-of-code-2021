from dataclasses import dataclass
from enum import Enum
from operator import mul
from functools import reduce

@dataclass
class Packet:
    version: int
    packet_type: int
    subpackets: list
    value: int

class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GT = 5
    LT = 6
    EQ = 7

def parse_input(filename):
    with open(filename) as file:
        return file.read().strip()

def hex_to_bin(h):
    mapping = { "0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101", "6": "0110", "7": "0111", "8": "1000", "9": "1001", "A": "1010", "B": "1011", "C": "1100", "D": "1101", "E": "1110", "F": "1111"}
    return flatten(map(lambda c: list(mapping[c]), h))

def parse_version(vbits):
    assert(len(vbits) == 3)
    return to_int(vbits)

def parse_type(vbits):
    assert(len(vbits) == 3)
    return to_int(vbits)

def to_int(bits):
    return int("".join(bits), 2)

def flatten(t):
    return [item for sublist in t for item in sublist]

def parse_literal(binmsg):
    # print("parse_literal", binmsg)
    accumulator = []
    STOP_READING_BIT = "0"
    while True:
        chunk = binmsg[:5]
        binmsg = binmsg[5:]
        accumulator.append(list(chunk)[1:])
        if chunk[0] == STOP_READING_BIT:
            break
    # print("--> parse_literal", binmsg)
    return to_int(flatten(accumulator)), binmsg

def parse_length(binmsg, length):
    # print("parse_length", binmsg)
    tmpbinmsg = binmsg[:length]
    binmsg = binmsg[length:]
    packets = []
    while tmpbinmsg:
        packet, tmpbinmsg = parse_packet(tmpbinmsg)
        packets.append(packet)
    return packets, binmsg

def parse_packet_number(binmsg, length):
    accumulator = []
    for i in range(length):
        packet, binmsg = parse_packet(binmsg)
        accumulator.append(packet)
    return accumulator, binmsg


def parse_operator(binmsg):
    # print("parse_operator", binmsg)
    length_type_id = binmsg[0]
    binmsg = binmsg[1:]
    TOTAL_LENGTH_LENGTH_TYPE = "0"
    if length_type_id == TOTAL_LENGTH_LENGTH_TYPE:
        parsing_function, LENGTH_SIZE = parse_length, 15
    else:
        parsing_function, LENGTH_SIZE = parse_packet_number, 11
    chunk = binmsg[:LENGTH_SIZE]
    binmsg = binmsg[LENGTH_SIZE:]
    length = to_int(chunk)
    # print("length", length)
    subpackets, binmsg = parsing_function(binmsg, length)
    return subpackets, binmsg


def parse_packet(binmsg):
    # print("parse_packet", binmsg)
    MSG_TYPE_LITERAL=4
    version = parse_version(binmsg[:3])
    binmsg = binmsg[3:]
    msgtype = parse_type(binmsg[:3])
    binmsg = binmsg[3:]
    # print("parse_packet", version, msgtype)
    if msgtype == PacketType.LITERAL.value:
        literal, binmsg = parse_literal(binmsg)
        return Packet(version=version, packet_type=PacketType(msgtype), subpackets=[], value=literal), binmsg
    else:
        subpackets, binmsg = parse_operator(binmsg)
        return Packet(version=version, packet_type=PacketType(msgtype), subpackets=subpackets, value=None), binmsg


def get_version_sum(packet):
    s = packet.version
    for p in packet.subpackets:
        s += get_version_sum(p)
    return s

def product(l):
    return reduce(mul, l)

def evaluate(packet):
    if packet.packet_type == PacketType.LITERAL:
        return packet.value

    comp_funcs = {
        PacketType.GT: lambda x, y: 1 if x > y else 0,
        PacketType.LT: lambda x, y: 1 if x < y else 0,
        PacketType.EQ: lambda x, y: 1 if x == y else 0
    }

    evaluated_children = list(map(evaluate, packet.subpackets))
    if packet.packet_type in comp_funcs:
        lhs, rhs = evaluated_children
        return comp_funcs[packet.packet_type](lhs, rhs)

    if packet.packet_type == PacketType.SUM:
        return sum(evaluated_children)

    if packet.packet_type == PacketType.PRODUCT:
        return product(evaluated_children)

    if packet.packet_type == PacketType.MIN:
        return min(evaluated_children)

    if packet.packet_type == PacketType.MAX:
        return max(evaluated_children)

def main():
    message = parse_input("input.txt")
    binmsg = hex_to_bin(message)
    p, _ = parse_packet(list(binmsg))
    s = get_version_sum(p)
    print(s)
    e = evaluate(p)
    print(e)


if __name__ == '__main__':
    main()


