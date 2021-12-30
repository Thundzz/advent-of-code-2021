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



def main():
    instructions = parse_input("input.txt")
    grouped_instrs = grouped(instructions)
    value = int(14*"9")
    # while True:
    #     z_val = 0
    #     for val, block in zip(str(value), grouped_instrs):
    #         z_val = evaluate(tuple(block), val, z_val)
    #     if z_val == 0:
    #         print(value)
    #         break
    #     value -= 1

    for idx, block in enumerate(grouped_instrs):
        for z in range(1, 100):
            for w in range(1, 10):
                res = evaluate(tuple(block), str(w) , z)
                if res == 3:
                    print(w, z, res)
    # print(grouped_instrs)

if __name__ == '__main__':
    """
    when z % 26 + Xadd == w  then z // Zdiv , else 26*(z // Zdiv) + Yadd + w
    In the first case it seems that Zdiv should be 26 and in the second that it should be 1
    """
    main()