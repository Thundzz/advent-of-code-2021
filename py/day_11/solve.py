
import numpy as np
import itertools

def parse_input(filename):
    cavern = np.zeros((10, 10))
    with open(filename) as file:
        for idx, line in enumerate(file.readlines()):
            cavern[idx, :] = [int(c) for c in line.strip()]
        return cavern

def neighbours(i, j, max_size):
    raw_neighbours = [
      (x + i, y + j)
      for x, y in itertools.product([-1, 0, 1],[-1, 0, 1])
      if not(x == 0 and y == 0)
    ]
    return [
        (ii, jj) for ii, jj in raw_neighbours
        if 0 <= ii < max_size and 0 <= jj < max_size
    ]

def update_flashed(new_state, flashed_octopi):
    newly_flashed = [
        (i, j) for i, j in np.argwhere(new_state > 9)
        if flashed_octopi[i, j] == 0
    ]
    for i, j in newly_flashed:
        flashed_octopi[i, j] = 1
    return newly_flashed, flashed_octopi

def step(cavern):
    new_state = cavern + 1
    flashed_octopi = np.zeros_like(cavern)
    newly_flashed, flashed_octopi = update_flashed(new_state, flashed_octopi)
    while newly_flashed:
        to_update = []
        for i, j in newly_flashed:
            to_update.extend(neighbours(i, j, 10))
        for i, j in to_update:
            new_state[i, j] += 1
        newly_flashed, flashed_octopi = update_flashed(new_state, flashed_octopi)

    for i, j in np.argwhere(flashed_octopi):
        new_state[i, j] = 0

    return new_state, len(np.argwhere(flashed_octopi))

def synchronized_flash(cavern):
    return (cavern == 0).all()

def main():
    cavern = parse_input("input.txt")
    count = 0
    for i in range(1000):
        cavern, c = step(cavern)
        count += c
        if synchronized_flash(cavern):
            print("First synchronization is at", i +1)
            break
        if i == 99:
            print("Number of flashes at 100 iterations is", count)

if __name__ == '__main__':
    main()

