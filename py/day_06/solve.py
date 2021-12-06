from collections import Counter
from itertools import groupby
from operator import itemgetter

def parse_input(filename):
    with open(filename) as file:
        return [int(i) for i in file.readline().split(",")]

def flatten(t):
    return [item for sublist in t for item in sublist]

def tick(fish_count):
    fish_ttl, count = fish_count
    NEW_FISH_TTL = 8
    RESET_TTL = 6
    REPRODUCTION_TIME = 0
    if fish_ttl == 0:
        return [(NEW_FISH_TTL, count), (RESET_TTL, count)]
    else:
        return [(fish_ttl - 1, count)]

def increment_school(school):
    next_counts = flatten(map(tick, school.items()))
    new_items = []
    for key, items in groupby(sorted(next_counts), key=itemgetter(0)):
        total_count = sum(map(itemgetter(1), items))
        new_items.append((key, total_count))
    return dict(new_items)

def simulate_fishes_first(fishes, days):
    fish_school = dict(Counter(fishes))
    for i in range(days):
        fish_school = increment_school(fish_school)
    return fish_school

def main():
    fishes = parse_input("input.txt")
    state = simulate_fishes_first(fishes, 80)
    print(sum(state.values()))
    state = simulate_fishes_first(fishes, 256)
    print(sum(state.values()))

if __name__ == '__main__':
    main()

