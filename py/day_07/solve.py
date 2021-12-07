import statistics
import math

def parse_input(filename):
    with open(filename) as file:
        return [int(i) for i in file.readline().split(",")]

def fuel_cost_assumption(positions, target):
    return sum(map(lambda p: abs(p - target), positions))

def min_fuel_assumption(positions):
    m = statistics.median(positions)
    ceil, floor= math.ceil(m), math.floor(m)
    ceilc = fuel_cost_assumption(positions, ceil)
    floorc = fuel_cost_assumption(positions, floor)
    print(m, ceil, floor, ceilc, floorc)
    return min(ceilc, floorc)


def fuel_cost_crab_eng(positions, target):
    return sum(map(lambda p: ((abs(p - target) * (abs(p - target) + 1)) / 2), positions))

def bruteforce(positions):
    # TODO : There certainly should be a better way to do this.
    mini, maxi = min(positions), max(positions)
    costs = { pos :  fuel_cost_crab_eng(positions, pos) for pos in range(mini, maxi+1)}
    minv = min(costs.values())
    # mink = next(k for k in costs if costs[k] == minv)
    return minv

def main():
    positions = parse_input("input.txt")
    minf = min_fuel_assumption(positions)
    print(minf)
    minf = bruteforce(positions)
    print(minf)

if __name__ == '__main__':
    main()

