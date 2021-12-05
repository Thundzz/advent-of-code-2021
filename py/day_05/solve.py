from collections import Counter
import numpy as np
import re

def parse_line(l):
    pattern = r'(\d+),(\d+) -> (\d+),(\d+)'
    xs, ys, xe, ye = re.match(pattern, l.strip()).groups()
    return tuple(map(int, (xs, ys, xe, ye)))

def parse_input(filename):
    with open(filename) as file:
        return [parse_line(l) for l in file.readlines()]

def offset(start, end):
    if start < end:
        return 1
    elif start > end:
        return -1
    else:
        return 0

def get_line(xs, ys, xe, ye):
    xoff, yoff = offset(xs, xe), offset(ys, ye)
    xcurrent, ycurrent = xs, ys
    l = []
    while not(xcurrent == xe and ycurrent == ye):
        l.append((xcurrent, ycurrent))
        xcurrent += xoff
        ycurrent += yoff
    l.append((xcurrent, ycurrent))
    assert xcurrent == xe
    assert ycurrent == ye, f"{xs=} {ys=} {xe=}, {ye=}, {xoff=}, {yoff=}"
    return l

def count_dangerous_spots(vents):
    maxi = max([max(v) for v in vents]) + 1
    ocean_floor = np.zeros((maxi, maxi))
    for xs, ys, xe, ye in vents:
        spots = get_line(xs, ys, xe, ye)
        for x, y in spots:
            ocean_floor[x, y] += 1
    # import matplotlib.pyplot as plt
    # plt.imshow(ocean_floor)
    # plt.show()
    dangerous_spots = np.argwhere(ocean_floor[:,:] >= 2)
    return len(dangerous_spots)

def main():
    vents = parse_input("input.txt")
    nb_dg_spots = count_dangerous_spots([(xs, ys, xe, ye) for xs, ys, xe, ye  in vents if xs == xe or ys == ye])
    print(nb_dg_spots)
    nb_dg_spots = count_dangerous_spots(vents)
    print(nb_dg_spots)

if __name__ == '__main__':
    main()

