from collections import Counter
from itertools import cycle, product
from functools import lru_cache
from dataclasses import dataclass
import numpy as np
import re

@dataclass(init=True, repr=True, eq=True, frozen=True)
class Player:
    position: int
    score: int

    def wins(self):
        return self.score >= 21 # Quantum variant

    def after_mvmt(self, total_mvmt):
        position = (self.position + total_mvmt) % 10
        score = self.score + position + 1
        return Player(position, score)

@dataclass(init=True, repr=True, eq=True, frozen=True)
class GameState:
    player1: Player
    player2: Player
    turn : 0
    def current_player(self):
        return self.player1 if self.turn == 0 else self.player2

    def after_mvmt(self, total_mvmt):
        if self.turn == 0:
            p1, p2 = self.player1.after_mvmt(total_mvmt), self.player2
        else:
            p1, p2 = self.player1, self.player2.after_mvmt(total_mvmt)

        return GameState(p1, p2, 1 - self.turn)

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

@lru_cache
def possible_dice_rolls():
    l = list(product((1, 2, 3), repeat=3))
    print(l)
    c = Counter([sum(roll) for roll in l])
    print(c)
    return c

@lru_cache(maxsize=None)
def play_quantum(gs):
    if gs.current_player().wins():
        return (1, 0) if gs.turn == 0 else (0, 1)

    p1wcnt, p2wcnt= 0, 0
    for total_mvmt, multiplier in possible_dice_rolls().items():
        updated_gs = gs.after_mvmt(total_mvmt)
        p1mod, p2mod = play_quantum(updated_gs)
        p1wcnt += multiplier * p1mod
        p2wcnt += multiplier * p2mod

    return (p1wcnt, p2wcnt)

def main():
    positions = parse_input("input.txt")
    dice = deterministic_dice(100)
    play(positions, dice)
    possible_dice_rolls()
    gs = GameState(Player(positions[1] - 1, 0), Player(positions[2] - 1, 0), 0)
    p1wins, p2wins = play_quantum(gs)
    print(p1wins, p2wins)
    print(p1wins / 27, p2wins / 27) # No idea why

    # print(positions)

if __name__ == '__main__':
    main()



