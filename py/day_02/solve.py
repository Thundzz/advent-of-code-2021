def parse_line(l):
    instr, count = l.split()
    return instr, int(count)

def parse_input(filename):
    with open(filename) as file:
        return [parse_line(l) for l in file.readlines()]

def eval_displ(instr, arg):
    displacement = {
        "forward": complex(1),
        "down": complex(0, 1),
        "up": complex(0, -1)
    }
    return arg * displacement[instr]

def compute_final_pos_simple(instuctions):
    return sum([eval_displ(instr, count) for instr, count in instuctions])


def compute_final_pos_real(instuctions):
    aim = 0
    pos = complex(0, 0)
    for inst, count in instuctions:
        if inst == "up":
            aim -= count
        elif inst == "down":
            aim += count
        else:
            pos += count * complex(1, aim)
    return pos

def main():
    inputs = parse_input("input.txt")
    s = compute_final_pos_simple(inputs)
    print(s.real * s.imag)
    s = compute_final_pos_real(inputs)
    print(s.real * s.imag)

if __name__ == '__main__':
    main()
