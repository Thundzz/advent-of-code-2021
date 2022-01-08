import numpy as np
import itertools

def parse_input(filename):
    mapping = { "v" : 1, ">" : 2, "." : 0 }
    with open(filename) as file:
        return np.matrix([
            [mapping[c] for c in l.strip()]
            for  l in file.readlines()
        ])

def where_to_move(cucumber_type, i, j, m, n):
    if cucumber_type == 1:
        return ((i + 1) % m, j)
    elif cucumber_type == 2:
        return (i, (j + 1) % n)
    else:
        return None

def pprint(grid):
    if grid is not None:
        m, n = grid.shape
        mapping = { 1 : "v", 2 : ">", 0 : "." }
        for i in range(m):
            for j in range(n):
                print(mapping[grid[i, j]], end="")
            print()
        print("----------")

def iterate(grid):
    m, n = grid.shape
    horizontal_guys = np.argwhere(grid == 2)
    vertical_guys = np.argwhere(grid == 1)
    for critters in [horizontal_guys, vertical_guys]:
        copy = grid.copy()
        for i, j in critters:
            ii, jj = where_to_move(grid[i, j], i, j, m, n)
            if grid[ii, jj] == 0:
                copy[i, j] = 0
                copy[ii, jj] = grid[i, j]
        grid = copy
    return copy

def main():
    m = parse_input("input.txt")
    # while not (m == m_prev).all():
    for i in itertools.count(1):
        previous = m
        m = iterate(m)
        if (previous == m).all():
            print(f"Converged after {i} iterations.")
            break
    pprint(m)
if __name__ == '__main__':
    main()