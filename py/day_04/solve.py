from collections import Counter
import numpy as np
def parse_ints(l):
    return [int(c) for c in l.strip().split()]

def parse_input(filename):
    with open(filename) as file:
        draw_numbers =  [int(i) for i in  file.readline().strip().split(",")]
        file.readline()
        grids = []
        current = np.zeros((5, 5))
        lines = file.readlines()
        while lines:
            for i in range(5):
                l = parse_ints(lines.pop(0))
                current[i,:] = l
            grids.append(current)
            current = np.zeros((5, 5))
            lines.pop(0)
        return draw_numbers, grids

def is_finished(mask):
    for i in range(5):
        if mask[i,:].all() or mask[:, i].all():
            return True
    return False

def compute_score(grid, mask):
    # for i in range(5):
    #     for j in range(5):
    #         mask[i, j] = 1 - mask[i, j]
    arr =  np.ma.masked_array(grid, mask)
    # print(arr)
    # print(arr.sum())
    return arr.sum()

def compute_bingo(draw_numbers, grid):
    mask = np.zeros((5,5))
    draw_nums_reversed = list(reversed(draw_numbers))
    cnt = 0
    while True:
        cnt += 1
        last_drawn = draw_nums_reversed.pop()
        mask += (grid == last_drawn)
        if is_finished(mask):
            return cnt, last_drawn, compute_score(grid, mask)

def pick_best_min(sols):
    mini = min([cnt for cnt, _, _ in sols])
    return next(ld * s for cnt, ld, s in sols if cnt == mini)


def pick_best_max(sols):
    maxi = max([cnt for cnt, _, _ in sols])
    return next(ld * s for cnt, ld, s in sols if cnt == maxi)

def main():
    draw_numbers, grids = parse_input("input.txt")
    print(draw_numbers)
    sols = [compute_bingo(draw_numbers, grid) for grid in grids]
    print(pick_best_min(sols))
    print(pick_best_max(sols))
if __name__ == '__main__':
    main()
