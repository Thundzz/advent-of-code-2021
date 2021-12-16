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
    print("parse_literal", binmsg)
    accumulator = []
    STOP_READING_BIT = "0"
    while True:
        chunk = binmsg[:5]
        # print(chunk)
        binmsg = binmsg[5:]
        accumulator.append(list(chunk)[1:])
        if chunk[0] == STOP_READING_BIT:
            break
    print("--> parse_literal", binmsg)
    return to_int(flatten(accumulator)), binmsg

def parse_length(binmsg, length):
    print("parse_length", binmsg)
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
    return packet, binmsg


def parse_operator(binmsg):
    print("parse_operator", binmsg)
    length_type_id = binmsg[0]
    binmsg = binmsg[1:]
    TOTAL_LENGTH_LENGTH_TYPE = "0"
    SUBPACKET_NUMBER_LENGTH_TYPE = "0"
    if length_type_id == TOTAL_LENGTH_LENGTH_TYPE:
        parsing_function, LENGTH_SIZE = parse_length, 15
    else:
        parsing_function, LENGTH_SIZE = parse_packet_number, 11
    chunk = binmsg[:LENGTH_SIZE]
    binmsg = binmsg[LENGTH_SIZE:]
    length = to_int(chunk)
    print("length", length)
    subpackets, binmsg = parsing_function(binmsg, length)
    return subpackets, binmsg


def parse_packet(binmsg):
    print("parse_packet", binmsg)
    MSG_TYPE_LITERAL=4
    version = parse_version(binmsg[:3])
    binmsg = binmsg[3:]
    msgtype = parse_type(binmsg[:3])
    binmsg = binmsg[3:]
    print("parse_packet", version, msgtype)
    if msgtype == MSG_TYPE_LITERAL:
        literal, binmsg = parse_literal(binmsg)
        print("literal", literal, binmsg),
        return literal, binmsg
    else:
        subpackets, binmsg = parse_operator(binmsg)
        return subpackets, binmsg


def main():
    message = parse_input("simple_literal.txt")
    message = "EE00D40C823060"
    binmsg = hex_to_bin(message)

    # binmsg = list("10010000010")
    parse_packet(list(binmsg))

if __name__ == '__main__':
    main()


