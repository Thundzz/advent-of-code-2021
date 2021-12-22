import re
from itertools import product

def parse_line(l):
    pattern = r'(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)'
    onoff, xmin, xmax, ymin, ymax, zmin, zmax = re.match(pattern, l.strip()).groups()
    return (
        True if onoff == "on" else False,
        int(xmin), int(xmax), int(ymin), int(ymax), int(zmin), int(zmax)
    )

def cubes(instruction):
    onoff, xmin, xmax, ymin, ymax, zmin, zmax = instruction
    return product(range(xmin, xmax+1), range(ymin, ymax+1), range(zmin, zmax+1))

def procedure(instructions):
    on_cubes = set()
    for idx, instr in enumerate(instructions):
        onoff, xmin, xmax, ymin, ymax, zmin, zmax = instr
        if xmin >= -50 and xmax <= 50 and ymin >= -50 and ymax <= 50 and zmin >= -50 and zmax <= 50:
            cs = cubes(instr)
            if onoff:
                on_cubes = on_cubes | set(cs)
            else:
                on_cubes = on_cubes - set(cs)
    return on_cubes

def parse_input(filename):
    with open(filename) as file:
        return [parse_line(l.strip()) for l in file.readlines()]

def main():
    instructions = parse_input("input.txt")
    cubes = procedure(instructions)
    print(len(cubes))
    # print(instructions)

if __name__ == '__main__':
    main()
    # c = cubes((True, -20,26,-36,17,-47,7))
    # for x in c:
    #     print(x)


