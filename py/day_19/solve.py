
from scipy.spatial.transform import Rotation as R
from itertools import product
from functools import cache
import numpy as np
@cache
def all_rotations():
    axes = ["x", "y", "z"]
    angles = range(0,360, 90)
    matrices = []
    for axe, angle in product(axes, angles):
        mat = np.round(R.from_euler(axe, angle, degrees=True).as_matrix())
        print(mat)
        matrices.append(mat)
    return set([str(m) for m in matrices])


def parse_raw_scanner(raw_scanner):
    beacons = []
    for l in raw_scanner.split("\n"):
        if "--" in l: continue
        x, y, z = map(int, l.split(","))
        beacons.append((x, y, z))
    return beacons

def parse_input(filename):
    with open(filename) as file:
        content = file.read()
    raw_scanners = content.split("\n\n")
    scanners = {}
    for idx, raw_scanner in enumerate(raw_scanners):
        scanners[idx] = parse_raw_scanner(raw_scanner.strip())
    return scanners

def main():
    scanners = parse_input("input.txt")
    # print(scanners)

if __name__ == '__main__':
    main()
    matrices = all_rotations()
    print(len(matrices))


