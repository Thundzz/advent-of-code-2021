import re
from itertools import product
from dataclasses import dataclass
from collections import Counter
from math import prod

@dataclass(init=True, repr=True, eq=True, frozen=True)
class Cuboid:
    xmin: int
    xmax: int
    ymin: int
    ymax: int
    zmin: int
    zmax: int

    def intersects(self, other):
        b = (
            self.xmin <= other.xmax and self.xmax >= other.xmin
            and self.ymin <= other.ymax and self.ymax >= other.ymin
            and self.zmin <= other.zmax and self.zmax >= other.zmin
        )
        return b

    def intersection(self, other):
        return Cuboid(
            max(self.xmin, other.xmin), min(self.xmax, other.xmax),
            max(self.ymin, other.ymin), min(self.ymax, other.ymax),
            max(self.zmin, other.zmin), min(self.zmax, other.zmax)
        )
    def volume(self):
        return prod([
            self.xmax - self.xmin + 1,
            self.ymax - self.ymin + 1,
            self.zmax - self.zmin + 1
        ])


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

def solve_large(instructions):
    """
    Keep track of intersections and their corresponding volume modifiers
    to compensate final volume
    """
    final_volumes = Counter()
    for idx, instr in enumerate(instructions):
        to_update = Counter()
        onoff, xmin, xmax, ymin, ymax, zmin, zmax = instr
        cuboid = Cuboid(xmin, xmax, ymin, ymax, zmin, zmax)
        if onoff:
            to_update[cuboid] += 1
        for other, volume_modifier in final_volumes.items():
            if cuboid.intersects(other):
                to_update[cuboid.intersection(other)] -= volume_modifier
        final_volumes.update(to_update)
    return final_volumes

def parse_input(filename):
    with open(filename) as file:
        return [parse_line(l.strip()) for l in file.readlines()]

def main():
    instructions = parse_input("input.txt")
    cubes = procedure(instructions)
    print(len(cubes))
    volumes = solve_large(instructions)
    s = sum(cuboid.volume() * mod for cuboid, mod in volumes.items())
    print(s)

if __name__ == '__main__':
    main()
    # c = cubes((True, -20,26,-36,17,-47,7))
    # for x in c:
    #     print(x)


