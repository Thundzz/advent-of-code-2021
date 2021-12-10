from collections import deque


def parse_input(filename):
    with open(filename) as file:
        return [l.strip() for l in file.readlines()]

def illegal_char_score(c):
    return {
        ")" : 3, "]": 57, "}": 1197, ">": 25137
    }[c] if c else 0


def parse(pattern):
    s = []
    oc = {
        "(" : ")",
        "<" : ">",
        "[" : "]",
        "{" : "}"
    }
    co = { v : k for k, v in oc.items() }
    for c in pattern:
        if c in oc.keys():
            s.append(c)
        else:
            mb = s.pop()
            if co[c] != mb:
                return c

def compute_score(patterns):
    return sum([illegal_char_score(parse(p)) for p in patterns if parse(p)])

def main():
    patterns = parse_input("input.txt")
    score = compute_score(patterns)
    print(score)


if __name__ == '__main__':
    main()

