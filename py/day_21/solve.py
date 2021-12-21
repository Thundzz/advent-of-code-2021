import re
from itertools import cycle

def parse_line(l):
    pattern = r'Player (\d+) starting position: (\d+)'
    player_id, pos = re.match(pattern, l.strip()).groups()
    return tuple(map(int, (player_id, pos)))

def parse_input(filename):
    with open(filename) as file:
        return dict([parse_line(l.strip()) for l in file.readlines()])

def deterministic_dice(n):
    return cycle(map(lambda x:x+1, range(n)))

def roll(n, dice):
    l = []
    for _ in range(n):
        l.append(next(dice))
    return l

def play(positions, dice):
    pos = { k: v-1 for k, v in positions.items() }
    scores = { player_id: 0 for player_id in positions }
    total_rolls = 0
    for player in cycle([1, 2]):
        rolls = roll(3, dice)
        print(player, rolls, )
        total_rolls += 3
        pos[player] += sum(rolls)
        pos[player] = pos[player] % 10
        scores[player] += (pos[player] + 1)
        if scores[player] >= 1000:
            break
    print(player, total_rolls, rolls, scores)
    losing_player = 2 if player == 1 else 1
    print("answer = ", scores[losing_player], total_rolls, scores[losing_player] * total_rolls)


def main():
    positions = parse_input("input.txt")
    dice = deterministic_dice(100)
    play(positions, dice)
    # print(positions)

if __name__ == '__main__':
    main()



