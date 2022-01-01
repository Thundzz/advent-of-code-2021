import helper as hlp
from collections import defaultdict
from functools import lru_cache
import heapq

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
def amphipod_color_rooms(rooms, amphipod):
        return [s for s in rooms if amphipod[0] == s[0]]

class GameState:
    hallway = list(map(lambda x: "H" + str(x), range(0,10))) + ["HA"]
    hallway_tuple = tuple(hallway)
    rooms = tuple([
        "A1", "A2", "A3", "A4",
        "B1", "B2", "B3", "B4",
        "C1", "C2", "C3", "C4",
        "D1", "D2", "D3", "D4"
    ])
    slots = frozenset(hallway + list(rooms))
    cost_by_type = { "A" : 1, "B" : 10, "C" : 100, "D" : 1000 }
    allowed_dests = set(slots) - {"H2", "H4", "H6", "H8"} # CONST

    def clone(self):
        return GameState([(v, k) for k, v in self.map.items() if v is not None], self.paths)

    def __lt__(self, other):
        return False

    def __init__(self, positions, paths):
        _, position_values = zip(*positions)
        self.paths = paths
        self.currently_empty = self.slots - set(position_values)
        self.map = defaultdict(lambda: None, { v: k for k, v in positions})

    def signature(self):
        return tuple((r, self.map[r]) for r in list(self.rooms) + self.hallway if self.map[r])
        # return tuple(sorted([(k, v) for k, v in self.map.items() if v]))


    def possible_moves(self):
        moves = []
        for curloc in self.slots:
            amphipod = self.map[curloc]
            if amphipod:
                if curloc[0] in {"A", "B", "C", "D"}:
                    target_rooms = self.hallway
                else:
                    target_rooms = amphipod_color_rooms(self.rooms, amphipod)
                for tarloc in target_rooms:
                    if self.can_move(amphipod, curloc, tarloc):
                        moves.append((amphipod, curloc, tarloc))
        return moves

    def move_cost(self, move):
        amphipod, start, dest = move
        return self.cost_by_type[amphipod] * (len(self.paths[(start, dest)]) - 1)

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
                all(self.map[c] is None for c in self.paths[(curloc, tarloc)][1:]) # path is free
                and not self.should_stay_locked(amphipod, curloc, tarloc)
                and self.room_is_good(amphipod, curloc, tarloc)
            )
        return False

    def play(self, move):
        amphipod, curloc, tarloc = move
        self.map[tarloc] = amphipod
        self.map[curloc] = None


def dijkstra(st, tar):
    distances = defaultdict(lambda: float('inf'))
    distances[st.signature()] = 0
    parents = {st.signature(): st.signature()}
    pq = [(0, st)]
    maxi_dist = 0
    found_dist = None
    while len(pq) > 0:
        # print(len(pq), maxi_dist)
        d, state = heapq.heappop(pq)
        state_sign = state.signature()
        if d > distances[state_sign]:
            continue
        for move in state.possible_moves():
            neighbor = state.clone()
            weight = state.move_cost(move)
            neighbor.play(move)
            distance = d + weight
            # print(maxi_dist, distance)
            next_sign = neighbor.signature()
            # print(tar, next_sign)
            if tar == next_sign:
                print(f"Found one path to target. Distance: {distance}")
                found_dist = distance if not found_dist else min(distance, found_dist)
            if distance > 60000 or (found_dist and distance >= found_dist):
                continue
            if distance < distances[next_sign]:
                parents[next_sign] = state.signature()
                distances[next_sign] = distance
                maxi_dist = max(maxi_dist, distance)
                heapq.heappush(pq, (distance, neighbor))
    return distances, parents

def main():
    # inpt = {
    #     ("B", "A1"),
    #     ("A", "A4"),
    #     ("C", "B1"),
    #     ("D", "B4"),
    #     ("B", "C1"),
    #     ("C", "C4"),
    #     ("D", "D1"),
    #     ("A", "D4"),
    #     ("D", "A2"),
    #     ("D", "A3"),
    #     ("C", "B2"),
    #     ("B", "B3"),
    #     ("B", "C2"),
    #     ("A", "C3"),
    #     ("A", "D2"),
    #     ("C", "D3")
    # }

    inpt = (
        ('C', 'A1'),
        ('B', 'A2'),
        ('D', 'B1'),
        ('A', 'B2'),
        ('A', 'C1'),
        ('D', 'C2'),
        ('B', 'D1'),
        ('C', 'D2'),
        ##
        ("D", "A2"),
        ("D", "A3"),
        ("C", "B2"),
        ("B", "B3"),
        ("B", "C2"),
        ("A", "C3"),
        ("A", "D2"),
        ("C", "D3"),
    )
    wanted_position = (
        ("A1", "A"),
        ("A2", "A"),
        ("A3", "A"),
        ("A4", "A"),
        ("B1", "B"),
        ("B2", "B"),
        ("B3", "B"),
        ("B4", "B"),
        ("C1", "C"),
        ("C2", "C"),
        ("C3", "C"),
        ("C4", "C"),
        ("D1", "D"),
        ("D2", "D"),
        ("D3", "D"),
        ("D4", "D")
    )
    res = dijkstra(GameState(inpt, hlp.large_graph_paths), wanted_position)



if __name__ == '__main__':
    main()



