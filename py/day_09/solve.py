import numpy as np

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
    print(n, m)
    mat = np.zeros((n, m))
    for i, l in enumerate(ls):
        mat[i, :] = [int(c) for c in l.strip()]
    return (mat, n, m)

def low_point_risk_levels(mat, n, m):
    mask = np.zeros_like(mat)
    for i in range(n):
        for j in range(m):
            if all(mat[i, j] < mat[ii, jj] for ii, jj in neighbours(i, j, n, m)):
                mask[i, j] = mat[i, j] + 1

    return np.sum(mask)

def main():
    mat, n, m = parse_input("input.txt")
    import matplotlib.pyplot as plt
    plt.imshow(mat)
    plt.show()
    c = low_point_risk_levels(mat, n, m)
    print(c)

if __name__ == '__main__':
    main()

