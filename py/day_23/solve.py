import helper as hlp
from collections import defaultdict
from functools import lru_cache
"""
#0123456789a#
#hhhhhhhhhhh#
##1A#.#.#.###
  2A#.#.#.#
  #########

let's denote hallway places h0 to ha
and rooms A1, A2, B1, B2, C1, C2, D1, D2
"""
@lru_cache(maxsize=None)
def amphipod_color_rooms(slots, amphipod):
        return [s for s in slots if amphipod[0] == s[0]]

class GameState:
    hallway = list(map(lambda x: "H" + str(x), range(1,10))) + ["HA"]
    rooms = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]
    paths = hlp.compute_paths()
    slots = frozenset(hallway + rooms)
    cost_by_type = { "A" : 1, "B" : 10, "C" : 100, "D" : 1000 }

    def clone(self):
        return GameState([(v, k) for k, v in self.map.items() if v is not None])

    def __init__(self, positions):
        _, position_values = zip(*positions)
        self.allowed_dests = set(self.slots) - {"H2", "H4", "H6", "H8"} # CONST
        self.currently_empty = self.slots - set(position_values)
        self.history = []
        self.map = defaultdict(lambda: None, { v: k for k, v in positions})

    def signature(self):
        return tuple(sorted([(k, v) for k, v in self.map.items() if v]))

    def possible_moves(self):
        moves = []
        for curloc in self.slots:
            amphipod = self.map[curloc]
            if amphipod:
                for tarloc in self.slots:
                    if tarloc != curloc and self.can_move(amphipod, curloc, tarloc):
                        moves.append((amphipod, curloc, tarloc))
        return moves

    def is_complete(self):
        to_check = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]
        return all(self.map[loc] == loc[0] for loc in to_check)

    def move_cost(self, move):
        amphipod, start, dest = move
        return self.cost_by_type[amphipod] * (len(self.paths[(start, dest)]) - 1)

    def total_cost(self):
        cost = 0
        for amphi, curloc, tarloc in self.history:
            cost += self.cost_by_type[amphi[0]] * (len(self.paths[(curloc, tarloc)]) - 1)
        return cost

    def should_stay_locked(self, amphipod, curloc, tarloc):
        correct_rooms = amphipod_color_rooms(self.slots, amphipod)
        return (
            curloc[0] == amphipod
            and all(self.map[room] == room[0] for room in correct_rooms if room[1] > curloc[1])
        )

    def room_is_good(self, amphipod, curloc, tarloc):
        correct_rooms = amphipod_color_rooms(self.slots, amphipod)
        empty_correct_rooms = [r[1] for r in correct_rooms if self.map[r] is None]
        return tarloc[0] == "H" or (
            tarloc[0] == amphipod[0]
            and tarloc[1] == "?" if not empty_correct_rooms else max(empty_correct_rooms)
            and all(self.map[room] is None or self.map[room] == room[0] for room in correct_rooms)
        )

    def can_move(self, amphipod, curloc, tarloc):
        if tarloc in self.allowed_dests and curloc[0] != tarloc[0]:
            return (
                not self.should_stay_locked(amphipod, curloc, tarloc)
                and all(self.map[c] is None for c in self.paths[(curloc, tarloc)][1:]) # path is free
                and self.room_is_good(amphipod, curloc, tarloc)
            )
        return False
    def play(self, move):
        amphipod, curloc, tarloc = move
        self.map[tarloc] = amphipod
        self.map[curloc] = None
        self.history.append(move)
    def unplay(self, move):
        assert self.history[-1] == move
        amphipod, curloc, tarloc = move
        self.map[tarloc] = None
        self.map[curloc] = amphipod
        self.history.pop()

def solve(positions):
    game_state = GameState(positions)
    seen_positions = { }
    def recurse():
        print(len(seen_positions))
        if game_state.history[:2] == [("By", "C1", "H3"), ("Cx", "B1", "C1")]:
            print(game_state.total_cost(), game_state.positions, game_state.history)
        if game_state.total_cost() >= 14000 or len(game_state.history) >= 10:
            return

        for move in game_state.possible_moves():
            game_state.play(move)
            current_cost = game_state.total_cost()
            signature = game_state.signature()
            # print(signature)
            if signature in seen_positions and seen_positions[signature] < current_cost:
                game_state.unplay(move)
                continue
            if game_state.is_complete():
                print("solution found, cost:", game_state.total_cost())
                print(game_state.history)
                print(game_state.positions)
            if current_cost >= 14000:
                game_state.unplay(move)
                continue

            seen_positions[signature] = current_cost
            recurse()
            game_state.unplay(move)
    recurse()

def gen_all_states(initial_state):
    q = [initial_state]
    seen = set()
    transitions = defaultdict(lambda :{})
    i = 0
    while q:
        i += 1
        state = q.pop()
        state_sign = state.signature()
        # print(i, len(transitions), len(q), len(seen))
        if state_sign not in seen:
            for move in state.possible_moves():
                state.play(move)
                next_sign = state.signature()
                if not next_sign in seen:
                    q.append(state.clone())
                transitions[state_sign][next_sign] = state.move_cost(move)
                transitions[next_sign][state_sign] = state.move_cost(move)
                state.unplay(move)
            seen.add(state_sign)
    return transitions

def main():
    inpt = {
        ("B", "A1"),
        ("A", "A2"),
        ("C", "B1"),
        ("D", "B2"),
        ("B", "C1"),
        ("C", "C2"),
        ("D", "D1"),
        ("A", "D2")
    }

    inpt = (('C', 'A1'), ('B', 'A2'), ('D', 'B1'), ('A', 'B2'), ('A', 'C1'), ('D', 'C2'), ('B', 'D1'), ('C', 'D2'))
    print("--- computing transitions between all states ---")
    initial_gs = GameState(inpt)
    initial_gs_sign = initial_gs.signature()
    transitions = gen_all_states(initial_gs)

    # print("--- print graph ---")
    # for source, edges in transitions.items():
    #     for dest, distance in edges.items():
    #         print(source, dest, distance)
    print("--- dijkstra ---")
    wanted_position = (
        ("A1", "A"),
        ("A2", "A"),
        ("B1", "B"),
        ("B2", "B"),
        ("C1", "C"),
        ("C2", "C"),
        ("D1", "D"),
        ("D2", "D")
    )
    distances, parents = hlp.dijkstra(transitions, initial_gs_sign)
    print(distances[wanted_position])
    # print(moves)

if __name__ == '__main__':
    main()



