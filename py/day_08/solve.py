from collections import Counter, defaultdict

def parse_line(l):
    lhs, rhs = l.split(" | ")
    inpt = tuple(lhs.strip().split())
    output = tuple(rhs.strip().split())
    return (inpt, output)

def parse_input(filename):
    with open(filename) as file:
        return dict([parse_line(l) for l in file.readlines()])

def flatten(t):
    return [item for sublist in t for item in sublist]

def count_easy_letters(info):
    x = map(len, flatten(info.values()))
    c = Counter(x)
    return c[2] + c[4] + c[7] + c[3]  # lengths of 1, 4, 8 and 7

def extract(s):
    return next(iter(s))

def by_length(inputs, length):
    return next(i for i in inputs if len(i) == length)

def decode_one(inputs, output):
    concatenated = "".join(flatten(inputs))
    counter = defaultdict(lambda: set())
    for k, v in  Counter(concatenated).items():
        counter[v].add(k)

    one, four, seven, eight = [by_length(inputs, l) for l in [2, 4, 3, 7]]
    f, e = extract(counter[9]), extract(counter[4])
    # d appears 7 times in the concat and is in the number 4 which g is not
    d = extract(counter[7] & set(four)) 
    c = extract(set(one) - { f })
    a = extract(set(seven) - set(one))
    b = extract(set(four) - {c, d, f})
    g = extract(set(eight) - {a, b, c, d, e, f})
    translation = str.maketrans(f"{a}{b}{c}{d}{e}{f}{g}", "abcdefg")
    to_digit = {
        tuple("abcefg") : "0",
        tuple("cf") : "1",
        tuple("acdeg") : "2",
        tuple("acdfg") : "3",
        tuple("bcdf") : "4",
        tuple("abdfg") : "5",
        tuple("abdefg") : "6",
        tuple("acf") : "7",
        tuple("abcdefg") : "8",
        tuple("abcdfg") : "9"
    }
    digits = [ to_digit[tuple(sorted(o.translate(translation)))] for o in output ]
    return int("".join(digits))


def solve(info):
    return sum([decode_one(inputs, output) for inputs, output in info.items()])

def helper():
    mapping = [
       "abcefg", "cf", "acdeg", "acdfg", "bcdf",
       "abdfg", "abdefg", "acf", "abcdefg", "abcdfg"
    ]

    print(Counter("".join(mapping)))

def main():
    info = parse_input("input.txt")
    c = count_easy_letters(info)
    print(c)
    s = solve(info)
    print(s)

if __name__ == '__main__':
    main()

