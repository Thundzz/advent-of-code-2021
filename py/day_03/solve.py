from collections import Counter
def parse_line(l):
    return [c for c in l.strip()]

def parse_input(filename):
    with open(filename) as file:
        return [parse_line(l) for l in file.readlines()]

def stringify(arr):
    return "".join(arr)

def compute_rates(diagnostic):
    n = len(diagnostic[0])
    gamma = [
        Counter([d[pos] for d in diagnostic]).most_common()[0][0]
        for pos in range(n)
    ]
    epsilon = [
        Counter([d[pos] for d in diagnostic]).most_common()[-1][0]
        for pos in range(n)
    ]

    return stringify(gamma), stringify(epsilon)

def bit_criteria(counter, default, index):
    if counter["1"] == counter["0"]:
        return default
    else:
        return counter.most_common()[index][0]

def o2_bit_criteria(counter):
    return bit_criteria(counter, "1", 0)

def co2_bit_criteria(counter):
    return bit_criteria(counter, "0", -1)

def o2_co2_ratings(diagnostic):
    n = len(diagnostic[0])
    o2l = list(diagnostic)
    co2l = list(diagnostic)
    for i in range(n):
        o2criteria = o2_bit_criteria(Counter([d[i] for d in o2l]))
        co2criteria = co2_bit_criteria(Counter([d[i] for d in co2l]))
        o2l = [d for d in o2l if d[i] == o2criteria]
        co2l = [d for d in co2l if d[i] == co2criteria]
    return stringify(o2l[0]), stringify(co2l[0])

def main():
    diagnostic = parse_input("input.txt")
    gamma, epsilon = compute_rates(diagnostic)
    gamma_i, epsilon_i = int(gamma, 2), int(epsilon, 2)
    print(gamma, epsilon, gamma_i, epsilon_i, gamma_i * epsilon_i)
    gamma, epsilon = o2_co2_ratings(diagnostic)
    gamma_i, epsilon_i = int(gamma, 2), int(epsilon, 2)
    print(gamma, epsilon, gamma_i, epsilon_i, gamma_i * epsilon_i)
if __name__ == '__main__':
    main()
