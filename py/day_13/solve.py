import numpy as np
from operator import itemgetter

def parse_input(filename):
    with open(filename) as file:
        coords_raw, folds_raw = file.read().split("\n\n")
    coords = []
    for line in coords_raw.split("\n"):
        x, y = map(int, line.strip().split(","))
        coords.append((x, y))
    folds =[]
    for line in folds_raw.split("\n"):
        direction, index = line.split()[-1].split("=")
        folds.append((direction, int(index)))
    return coords, folds

def fill_grid(coords):
    maxi = max(map(itemgetter(0), coords)) + 1
    maxj = max(map(itemgetter(1), coords)) + 1
    mat = np.zeros((maxj, maxi))
    for i, j in coords:
        mat[j, i] = 1
    return mat


def fold_once(matrix, fold):
    direction, index = fold
    if direction == "x":
        left = matrix[:, 0:index]
        right = matrix[:, index+1:]
        slx, sly = left.shape
        srx, sry = right.shape
        sx, sy = srx, max(sly, sry)
        folded = np.zeros((sx, sy))
        folded[:, sy-sly:] = folded[:, sy-sly:] + left
        folded[:, sy-sry:] = folded[:, sy-sry:] + np.fliplr(right)
    if direction == "y":
        top = matrix[0:index,:]
        bottom = matrix[index+1:,:]
        stx, sty = top.shape
        sbx, sby = bottom.shape
        sx, sy = max(stx, sbx), sby
        folded = np.zeros((sx, sy))
        folded[sx-stx:, :] = folded[sx-stx:, :] + top 
        folded[sx-sbx:, :] = folded[sx-sbx:, :] + np.flipud(bottom)
    return folded

def main():
    coords, folds = parse_input("input.txt")
    mat = fill_grid(coords)
    mat = fold_once(mat, folds[0])
    print(len(np.argwhere(mat != 0)))
    for f in folds[1:]:
        mat = fold_once(mat, f)

    code = np.zeros_like(mat)
    for i, j in np.argwhere(mat != 0):
        code[i, j] = 1

    import matplotlib.pyplot as plt
    plt.imshow(code)
    plt.show()

if __name__ == '__main__':
    main()

