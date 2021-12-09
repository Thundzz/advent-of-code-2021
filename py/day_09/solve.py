import numpy as np
import heapq

def neighbours(i, j, n, m):
    full_list = [
        (i - 1, j),
        (i, j - 1),
        (i + 1, j),
        (i, j + 1)
    ]
    return [(ii, jj) for ii, jj in full_list if 0 <= ii < n and 0 <= jj < m ]

def parse_input(filename):
    with open(filename) as file:
        ls = file.readlines()
    n, m = len(ls), len(ls[0].strip())
    mat = np.zeros((n, m))
    for i, l in enumerate(ls):
        mat[i, :] = [int(c) for c in l.strip()]
    return (mat, n, m)

def low_point_risk_levels(mat, n, m):
    mask = np.zeros_like(mat)
    low_points = []
    for i in range(n):
        for j in range(m):
            if all(mat[i, j] < mat[ii, jj] for ii, jj in neighbours(i, j, n, m)):
                mask[i, j] = mat[i, j] + 1
                low_points.append((i, j))
    return np.sum(mask), low_points

def explore_basin(mat, n, m, i, j):
    queue = [(i, j)]
    basin = []
    visited = np.zeros_like(mat)
    while queue:
        ci, cj = queue.pop()
        if not visited[ci, cj]:
            visited[ci, cj] = 1
            basin.append((ci, cj))
            for ii, jj in neighbours(ci, cj, n, m):
                if not mat[ii, jj] == 9 and not visited[ii, jj]:
                    queue.append((ii, jj))
    return len(basin), basin

def find_largest_basins(mat, low_points, n, m):
    basin_sizes = []
    for i, j in low_points:
        l, b = explore_basin(mat, n, m, i, j)
        heapq.heappush(basin_sizes, l)
    largest_basins =  heapq.nlargest(3, basin_sizes)
    return largest_basins

def main():
    mat, n, m = parse_input("input.txt")
    # import matplotlib.pyplot as plt
    # plt.imshow(mat)
    # plt.show()
    c, low_points = low_point_risk_levels(mat, n, m)
    print(c)
    largest_basins = find_largest_basins(mat, low_points, n, m)
    print(np.prod(largest_basins))

if __name__ == '__main__':
    main()

