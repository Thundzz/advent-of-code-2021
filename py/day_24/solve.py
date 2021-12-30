from functools import lru_cache
from collections import defaultdict

def parse_input(filename):
    with open(filename) as file:
        return [l.strip().split() for l in file.readlines()]

def grouped(instructions):
    blocks = []
    block = []
    context = {}
    for instr, *rest in instructions:
        if instr == "inp":
            if block:
                blocks.append(block)
            block = [(instr, *rest)]
        else:
            block.append((instr, *rest))
    blocks.append(block)
    return blocks

@lru_cache(None)
def evaluate(instructions, input_value, z_val):
    context = defaultdict(lambda :0, {"z" : z_val})
    for instr, *rest in instructions:
        if instr == "inp":
            var, = rest
            context[var] = int(input_value)
        else:
            var, val = rest
            roperand = context[val] if val in {"w", "x", "y", "z" } else int(val)
            if instr == "add":
                context[var] += roperand
            if instr == "mul":
                context[var] *= roperand
            if instr == "div":
                context[var] //= roperand
            if instr == "mod":
                context[var] %= roperand
            if instr == "eql":
                context[var] = 1 if context[var] == roperand else 0
    # print(context)
    return context["z"]

def eval_all(grouped_instrs, number):
    z_val = 0
    for val, block in zip(str(number), grouped_instrs):
        z_val = evaluate(tuple(block), val, z_val)
    return z_val
def main():
    instructions = parse_input("input.txt")
    grouped_instrs = grouped(instructions)
    value = 51983999947999
    z_val = eval_all(grouped_instrs, value)
    print(z_val)
    value = 11211791111365
    z_val = eval_all(grouped_instrs, value)
    print(z_val)
if __name__ == '__main__':
    """
    when z % 26 + Xadd == w  then z // Zdiv , else 26*(z // Zdiv) + Yadd + w
    In the first case it seems that Zdiv should be 26 and in the second that it should be 1

    After some careful reading of the "assembly code", I came to these conclusions:
    The blocks where we have a "div z 1" instruction are equivalent to pushing "w + yAdd" to the stack. 
    The blocks where we have a "div z 26" instruction force us to have "w = last_pushed_value + xAdd"

    If we write the number we search ABCDEFGHIJKL, we have the following constraints on my input:

    D = C - 1
    F = E + 6
    G = B + 8
    I = H
    L = K + 2
    M = J + 5
    N = A + 4

    Since all digits have to be between 1 and 9, computing the correct values for each input is simple.
    For example in the case I = H, if we are maximizing, then I = H = 9
    For a harder example like D = C - 1:
        When we maximize, we want the largest MSD so, C = 9, and D = 8.
        When we minimize, we want the smallest MSD possible so, C = 2, and D = 1
               ABCDEFGHIJKLMN
    largest    51983999947999
    smallest   11211791111365

    If we suppose that all other inputs from this exercise follow the same pattern as mine,
    it should be possible to write an algorithm that computes and solves these rules automatically,
    but I am too lazy to do it and have spend enough time already on this.
    """
    main()