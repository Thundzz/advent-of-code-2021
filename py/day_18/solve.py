import json
import re
import math
import itertools

def replace_left(left_str, left_num):
    flipped = left_str[::-1]
    match = list(re.finditer(r'\d+', flipped))
    if match:
        fst_match = match[0]
        match_str = fst_match.group()
        match_int = int(match_str[::-1])
        replacement = str(left_num + match_int)[::-1]
        return re.sub(r'\d+', replacement, flipped, 1)[::-1]
    return left_str

def replace_right(right_str, right_num):
    match = list(re.finditer(r'\d+', right_str))
    if match:
        fst_match = match[0]
        match_str = fst_match.group()
        return re.sub(r'\d+', str(right_num + int(match_str)), right_str, 1)
    return right_str

def explode(sn):
    level = 0
    should_explode = False
    for idx, c in enumerate(sn):
        if c == "[":
            level +=1
        elif c == "]":
            level -=1
        if level == 5:
            should_explode = True
            break
    if should_explode:
        clos = sn[idx:].index("]")
        left_str = sn[:idx]
        exploding_num = sn[idx:idx+clos+1]
        right_str = sn[idx+clos+1:]
        left_comp, right_comp = json.loads(exploding_num)
        new_left_str = replace_left(left_str, left_comp)
        new_right_str = replace_right(right_str, right_comp)
        return True, new_left_str + "0" + new_right_str
    return False, sn


def split(sn):
    def aux(l):
        if isinstance(l, int):
            if l >= 10:
                return True, [math.floor(l/2), math.ceil(l/2)]
            else:
                return False, l
        left, right = l
        has_split, new_l = aux(left)
        if has_split:
            return has_split, [new_l, right]
        else:
            has_split, new_r = aux(right)
            return has_split, [left, new_r]
    l = json.loads(sn)
    has_split, expr = aux(l)
    return has_split, json.dumps(expr, separators=(',', ':'))


def reduce_sfn(sn):
    stop = False
    while not stop:
        has_exploded, sn = explode(sn)
        if has_exploded: continue
        has_split, sn = split(sn)
        if not has_split:
            stop = True
    return sn

def parse_input(filename):
    with open(filename) as file:
        lines = [l.strip() for l in file.readlines()]
    return lines

def add_sfn(sn1, sn2):
    return reduce_sfn( f"[{sn1},{sn2}]")

def magnitude_sfn(sn):
    def aux(l):
        if isinstance(l, int):
            return l
        else:
            left, right = l
            return 3*aux(left) + 2*aux(right)
    return aux(json.loads(sn))


def solve_addition(numbers):
    fst, snd, *others = numbers
    summ = add_sfn(fst, snd)
    for n in others:
        summ = add_sfn(summ, n)
    return summ

def bonus_question(numbers):
    p = list(itertools.permutations(numbers, 2))
    maxi = max([magnitude_sfn(add_sfn(i1, i2)) for i1, i2 in p])
    return maxi

def main():
    numbers = parse_input("input.txt")
    res = solve_addition(numbers)
    magnitude = magnitude_sfn(res)
    print(res, magnitude)
    maxi = bonus_question(numbers)
    print(maxi)

if __name__ == '__main__':
    main()


