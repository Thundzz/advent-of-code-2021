import re

def sign(n):
    if n < 0:
        return -1
    if n == 0:
        return 0
    else:
        return 1

def parse_line(content):
    pattern = r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)'
    xs, xe, ys, ye = re.match(pattern, content).groups()
    return tuple(map(int, (xs, xe, ys, ye)))

def parse_input(filename):
    with open(filename) as file:
        return parse_line(file.read().strip())

def trajectory(vx, vy, bounds, steps=10000):
    x, y = 0, 0

    points = []
    for _ in range(steps):
        points.append((x, y))
        print(x, y)
        x += vx
        y += vy
        if vx > 0:
            vx -= 1
        elif vx < 0:
            vx += 1
        vy -= 1
    points.append((x, y))

    print(x, y, vx, vy)
    return False, points

def main():
    xs, xe, ys, ye = parse_input("test.txt")
    traj = trajectory()
    import matplotlib.pyplot as plt
    xs, ys = zip(*traj)
    plt.scatter(xs, ys)
    plt.show()
    print(xs, xe, ys, ye)

if __name__ == '__main__':
    main()


