import re
from functools import cache

def parse_line(content):
    pattern = r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)'
    xs, xe, ys, ye = re.match(pattern, content).groups()
    return tuple(map(int, (xs, xe, ys, ye)))

def parse_input(filename):
    with open(filename) as file:
        return parse_line(file.read().strip())

@cache
def fy(vy0, n):
    """
    Computed by hand
    """
    return n*(2*vy0 + 1 -n) / 2

@cache
def fx(vx0, n):
    """
    Computed by hand
    """
    if n>= vx0:
        return vx0*(vx0+1)/2
    else:
        return n*(2*vx0 + 1 -n) / 2

def solve_second_star(xs, xe, ys, ye):
    vel = set()
    for n in range(200):
        for vx in range(300):
            for vy in range(-100, 200):
                if xs <= fx(vx,n) <= xe  and ys <= fy(vy, n) <= ye:
                    vel.add((vx, vy))
    return len(vel)

def main():
    """
    First star solved using the following Desmos graph:
    https://www.desmos.com/calculator/pd8rlbrut3

    Second star limits guessed using the same desmos graph.
    """
    xs, xe, ys, ye = parse_input("input.txt")
    num = solve_second_star(xs, xe, ys, ye)
    print(num)

if __name__ == '__main__':
    main()


