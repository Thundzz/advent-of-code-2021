def parse_input(filename):
    with open(filename) as file:
        return [int(l.strip()) for l in file.readlines()]

def count_increases(depths):
    return len([i for i, n in zip(depths, depths[1:]) if i < n])


def count_sliding_window_increases(depths):
    n = len(depths)
    sliding_windows = [depths[i:i+3] for i in range(n-2)]
    sliding_sums = [ sum(w) for w in sliding_windows ]
    return count_increases(sliding_sums)

def main():
    inputs = parse_input("input.txt")
    s = count_increases(inputs)
    print(s)
    s = count_sliding_window_increases(inputs)
    print(s)

if __name__ == '__main__':
    main()
