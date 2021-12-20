from itertools import product
from functools import lru_cache
from operator import itemgetter
from collections import Counter
import numpy as np

def totuple(m):
    if m.shape == (1, 3):
        return tuple(np.array(m).reshape(-1))
    return (
        tuple(np.array(m[0]).reshape(-1)),
        tuple(np.array(m[1]).reshape(-1)),
        tuple(np.array(m[2]).reshape(-1))
    )

def all_rotations():
    xrot = np.matrix([[1, 0, 0], [0, 0,-1],[0,1,0]])
    yrot = np.matrix([[0, 0, 1], [0, 1, 0],[-1,0,0]])
    matrices = set()
    for p,q,r,s in product(range(4), repeat=4):
        m = (xrot**p).dot(yrot**q).dot(xrot**r).dot(yrot**s)
        matrices.add(totuple(m))
    return list(map(np.matrix, matrices))

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

def try_find_match(sc1, sc2):
    _, sc1 = sc1
    _, sc2 = sc2
    rotations = all_rotations()

    IIII = 0
    for rot in rotations:
        # print(sc2)
        n = len(sc1)
        m = len(sc2)
        # print(n, m)
        rotsc2 = [totuple(rot.dot(coords)) for coords in sc2]
        # print(rotsc2)
        xs1 = list(map(itemgetter(0), sc1))
        xs2 = list(map(itemgetter(0), rotsc2))
        # print(xs2)
        mat = np.zeros((n, m), dtype=int)
        diffs = []
        for i, j in product(range(n), range(m)):
            mat[i, j] =  xs1[i] - xs2[j]
            diffs.append(xs1[i] - xs2[j])
        c = Counter(diffs)
        if c.most_common(1)[0][1] >= 3:
            print("hi :)")
        # import matplotlib.pyplot as plt
        # plt.imshow(mat)
        # IIII +=1
        # plt.savefig(str(IIII) + ".jpg")
def diffprint(i, j, s1, s2):
    print(i, j)
    return s1[i]-s2[j]


def solve(scanners):
    sc1, sc2, *others = scanners.items()
    try_find_match(sc1, sc2)

def main():
    scanners = parse_input("input.txt")
    solve(scanners)
    # print(scanners)

if __name__ == '__main__':
    main()
    # matrices = all_rotations()
    # print(matrices)
    # print(len(matrices))


