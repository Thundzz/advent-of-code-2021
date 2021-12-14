import numpy as np
from operator import itemgetter
import re

def parse_input(filename):
    with open(filename) as file:
        base_raw, rules_raw = file.read().split("\n\n")
    base_molecule =  base_raw.strip()

    rules =[]
    for line in rules_raw.split("\n"):
        block, insertion = map(lambda x: x.strip(), line.split("->"))
        rules.append((block, insertion))
    return base_molecule, rules

def insert(st, c, pos):
    return st[:pos] + c + st[pos:]

def insertion_points(polymer, rules):
    insertions = []
    for pattern, inserted_c in rules:
        locations = [m.start() for m in re.finditer(rf"(?=({pattern}))", polymer)] # lookahed
        for loc in locations:
            insertions.append((loc + 1, inserted_c))
    for idx, c in sorted(insertions, key=itemgetter(0), reverse=True):
        polymer = insert(polymer, c, idx)

    return polymer


def polymerize(base_molecule, rules, increments):
    polymer = base_molecule
    for i in range(increments):
        print(i)
        polymer = insertion_points(polymer, rules)
    return polymer

def main():
    base_molecule, rules = parse_input("input.txt")
    polymer = polymerize(base_molecule, rules, 10)
    from collections import Counter
    c = Counter(polymer)
    _, counts = zip(*c.most_common())
    print(counts[0]  - counts[-1])

if __name__ == '__main__':
    main()

