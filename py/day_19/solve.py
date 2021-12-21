from itertools import product
from functools import lru_cache
from operator import itemgetter
from collections import Counter, defaultdict
import numpy as np
import heapq

def totuple(m):
    if m.shape == (1, 3):
        return tuple(np.array(m).reshape(-1))
    return (
        tuple(np.array(m[0]).reshape(-1)),
        tuple(np.array(m[1]).reshape(-1)),
        tuple(np.array(m[2]).reshape(-1))
    )
@lru_cache
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

def sub(tupl1, tupl2):
    return tuple(np.array(tupl1) - np.array(tupl2))

def find_offset(coords1, coords2):
    n = len(coords1)
    m = len(coords2)
    diffs = []
    for i, j in product(range(n), range(m)):
        diff = sub(coords1[i], coords2[j])
        diffs.append(diff)

    c = Counter(diffs)
    most_common, count = c.most_common(1)[0]
    if count >= 12:
        print("found offset", most_common, count)
        return (most_common, count)
    else:
        return None, None

def try_find_match(sc1, sc2):
    rotations = all_rotations()
    for rot in rotations:
        rotsc2 = [totuple(rot.dot(coord)) for coord in sc2]
        offset, count = find_offset(sc1, rotsc2)
        if offset:
            return rot, offset
    return None, None

def dijkstra(graph, st):
    distances = {v: float('inf') for v in graph}
    distances[st] = 0
    parents = {st: st}
    pq = [(0, st)]
    while len(pq) > 0:
        d, current = heapq.heappop(pq)
        if d > distances[current]:
            continue
        for neighbor, weight in graph[current].items():
            distance = d + weight
            if distance < distances[neighbor]:
                parents[neighbor] = current
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))

    return distances, parents

def as_graph(transforms):
    graph = defaultdict(lambda: {})
    for (s, d) in transforms.keys():
        graph[s][d] = 1
    return dijkstra(graph, 0)

def find_path(parents, start, target):
    path = []
    current = target
    while current != start:
        path.append(current)
        current = parents[current]
    path.append(start)
    return path

def displace(coords, rot, offset):
    return [
        totuple(rot.dot(coord) + np.array(offset))
        for coord in coords
    ]

def compute_absolute_coords(scanners, transforms, paths):
    all_beacons = set()
    all_scanners = set()
    for scid, sc in scanners.items():
        path = paths[scid]
        steps = [(path[i], path[i+1]) for i in range(len(path)-1)]
        coords = sc
        scanner = [(0,0,0)]
        for step in steps:
            i, j = step
            rot, offset = transforms[j, i]
            coords = displace(coords, rot, offset)
            scanner = displace(scanner, rot, offset)

        all_beacons = all_beacons | set(coords)
        all_scanners = all_scanners | set(scanner)
    return all_beacons, all_scanners

def manhattan(t1, t2):
    x1, y1, z1 = t1
    x2, y2, z2 = t2
    return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)

def solve(scanners):
    transforms = {}
    n = len(scanners)
    for sci1 in range(n):
        for sci2 in range(n):
            if sci1 != sci2:
                sc1 = scanners[sci1]
                sc2 = scanners[sci2]
                rot, offset = try_find_match(sc1, sc2)
                if offset:
                    transforms[(sci1, sci2)] = (rot, offset)
    graph, parents = as_graph(transforms)
    paths = { i: find_path(parents,0, i) for i in range(n) }
    all_coords, all_scanners = compute_absolute_coords(scanners, transforms, paths)
    print(len(all_coords))
    print("max distance", max([manhattan(sc1, sc2) for sc1, sc2 in product(all_scanners, repeat=2)]))


def main():
    scanners = parse_input("input.txt")
    solve(scanners)

if __name__ == '__main__':
    main()


