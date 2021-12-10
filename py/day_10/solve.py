from collections import deque


def parse_input(filename):
    with open(filename) as file:
        return [l.strip() for l in file.readlines()]

def illegal_char_score(c):
    return {
        ")" : 3, "]": 57, "}": 1197, ">": 25137
    }[c] if c else 0


def get_mappings():
    oc = {
        "(" : ")",
        "<" : ">",
        "[" : "]",
        "{" : "}"
    }
    co = { v : k for k, v in oc.items() }
    return oc, co

def parse(pattern):
    s = []
    oc, co = get_mappings()
    for c in pattern:
        if c in oc.keys():
            s.append(c)
        else:
            mb = s.pop()
            if co[c] != mb:
                return c, None
    return None, s


def parse_all(patterns):
    return [parse(p) for p in patterns]

def compute_parsing_score(parsed):
    return sum([illegal_char_score(res) for res, _ in parsed if res])

def autocomplete(stack):
    oc, co = get_mappings()
    full_map = { **oc, **co }
    return [ full_map[c] for c in reversed(stack) ]



def compute_score(completion):
    values = { ")": 1, "]": 2, "}": 3, ">": 4 }
    score = 0
    for c in completion:
        score = (score * 5) + values[c]
    return score

def compute_autocomplete_score(parsed):
    scores = [compute_score(autocomplete(s)) for _, s in parsed if s]
    n = len(scores)
    return list(sorted(scores))[n // 2 ]

def main():
    patterns = parse_input("input.txt")
    parsed = parse_all(patterns)
    score = compute_parsing_score(parsed)
    print(score)
    score = compute_autocomplete_score(parsed)
    print(score)

if __name__ == '__main__':
    main()

