import helper as hlp
from collections import defaultdict
from functools import lru_cache
import heapq
import sys
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
        return sorted([s for s in rooms if amphipod[0] == s[0]], reverse=True)

class GameState:
    hallway = list(map(lambda x: "H" + str(x), range(0,10))) + ["HA"]
    hallway_tuple = tuple(hallway)
    rooms = tuple([
        "A1", "A2", "A3", "A4",
        "B1", "B2", "B3", "B4",
        "C1", "C2", "C3", "C4",
        "D1", "D2", "D3", "D4"
    ])
    rooms_list = list(rooms)
    slots = frozenset(hallway + list(rooms))
    cost_by_type = { "A" : 1, "B" : 10, "C" : 100, "D" : 1000 }
    allowed_dests = set(slots) - {"H2", "H4", "H6", "H8"} # CONST
    amphipod_mapping = defaultdict(lambda : 255, { "A": 0, "B": 1, "C": 2, "D": 3 })

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
        # t = tuple((r, self.map[r]) for r in self.rooms_list + self.hallway if self.map[r])
        t = bytes(bytearray([self.amphipod_mapping[self.map[r]] for r in self.rooms_list + self.hallway]))
        # print(sys.getsizeof(t))
        return t

    def next_available_spot(self, curloc):
        amphipod = self.map[curloc]
        if amphipod:
            amphi_rooms = amphipod_color_rooms(self.rooms, amphipod)
            try:
                chosen_room =  next(r for r in amphi_rooms if self.map[r] is None or self.map[r][0] != r[0])
                return chosen_room
            except StopIteration:
                return curloc
        else:
            return curloc

    def approx_cost(self):
        cost = 0
        for curloc in self.slots:
            amphipod = self.map[curloc]
            if amphipod and not self.should_stay_locked(amphipod, curloc):
                dest = self.next_available_spot(curloc)
                cost_mod = len(self.paths[(curloc, dest)]) - 1
                cost += self.cost_by_type[amphipod] * cost_mod
        return cost

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

    def should_stay_locked(self, amphipod, curloc):
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
                and not self.should_stay_locked(amphipod, curloc)
                and self.room_is_good(amphipod, curloc, tarloc)
            )
        return False

    def play(self, move):
        amphipod, curloc, tarloc = move
        self.map[tarloc] = amphipod
        self.map[curloc] = None


def astar(st, tar):
    tar_sign = tar.signature()
    distances = defaultdict(lambda: float('inf'))
    fdist_estimate = defaultdict(lambda: float('inf'))
    st_sign = st.signature()
    distances[st_sign] = 0
    fdist_estimate[st_sign] = st.approx_cost()
    # parents = {st.signature(): st.signature()}
    pq = [(fdist_estimate[st_sign], st)]
    pqset = set([st_sign])
    while len(pq) > 0:
        _, state = heapq.heappop(pq)
        # print(pqset)
        state_sign = state.signature()
        pqset.remove(state_sign)
        for move in state.possible_moves():
            neighbor = state.clone()
            neighbor_distance = neighbor.move_cost(move)
            neighbor.play(move)
            distance = distances[state_sign] + neighbor_distance
            next_sign = neighbor.signature()
            if tar_sign == next_sign:
                print(f"Found one path to target. Distance: {distance}")
            if distance < distances[next_sign]:
                distances[next_sign] = distance
                fdist_estimate[next_sign] = distance + neighbor.approx_cost()
                # if not neighbor in pqset:
                if not next_sign in pqset:
                    heapq.heappush(pq, (fdist_estimate[next_sign], neighbor))
                    pqset.add(next_sign)
    return distances

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
        ('B', 'A4'),
        ('D', 'B1'),
        ('A', 'B4'),
        ('A', 'C1'),
        ('D', 'C4'),
        ('B', 'D1'),
        ('C', 'D4'),
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
        ("A", "A1"),
        ("A", "A2"),
        ("A", "A3"),
        ("A", "A4"),
        ("B", "B1"),
        ("B", "B2"),
        ("B", "B3"),
        ("B", "B4"),
        ("C", "C1"),
        ("C", "C2"),
        ("C", "C3"),
        ("C", "C4"),
        ("D", "D1"),
        ("D", "D2"),
        ("D", "D3"),
        ("D", "D4")
    )
    res = astar(GameState(inpt, hlp.large_graph_paths), GameState(wanted_position, hlp.large_graph_paths))



if __name__ == '__main__':
    main()



