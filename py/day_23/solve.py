import helper as hlp
"""
#0123456789a#
#hhhhhhhhhhh#
##1A#.#.#.###
  2A#.#.#.#
  #########

let's denote hallway places h0 to ha
and rooms A1, A2, B1, B2, C1, C2, D1, D2
"""

def other_room(room):
    return room[0] + str((3 ^ int(room[1])))

def other_amphipod(amphipod):
    return amphipod[0] + ("x" if amphipod[1] == "y" else "y")

class GameState:
    hallway = list(map(lambda x: "H" + str(x), range(1,10))) + ["HA"]
    rooms = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]
    paths = hlp.compute_paths()

    def __init__(self, positions):
        self.slots = set(self.hallway + self.rooms) # CONST
        self.allowed_dests = set(self.slots) - {"H2", "H4", "H6", "H8"} # CONST
        self.positions = dict(positions)
        self.possible_empty_dests = self.allowed_dests - set(self.positions.values())
        self.currently_empty = self.slots - set(self.positions.values())
        self.history = []

    def signature(self):
        return tuple(sorted(self.positions.items()))

    def possible_moves(self):
        moves = []
        for amphipod, curloc in self.positions.items():
            for tarloc in self.possible_empty_dests:
                if self.can_move(amphipod, curloc, tarloc):
                    moves.append((amphipod, curloc, tarloc))
        return moves

    def is_complete(self):
        return all(loc[0] == amphi[0] for amphi, loc in self.positions.items())

    def total_cost(self):
        cost = 0
        cost_by_type = { "A" : 1, "B" : 10, "C" : 1000, "D" : 1000 }
        for amphi, curloc, tarloc in self.history:
            cost += cost_by_type[amphi[0]] * (len(self.paths[(curloc, tarloc)]) - 1)
        return cost

    def can_move(self, amphipod, curloc, tarloc):
        # TODO : finish this function. Cleanup. Fix logic.
        # if amphipod and target location are the same color:
        could_be_useful = (
            amphipod[0] != curloc[0]
            or (
                amphipod[0] == curloc[0] == tarloc[0] and tarloc[1] > curloc[1]
            )
            or (
                self.positions[other_amphipod(amphipod)][0] != amphipod[0]
            )
        )
        target_allowed = tarloc in self.possible_empty_dests
        in_hallway = curloc[0] == "H"
        path_is_free = all(c in self.currently_empty for c in self.paths[(curloc, tarloc)][1:])
        room_is_safe = tarloc[0] == "H" or (
            tarloc[0] == amphipod[0]
            and
            not any(loc == other_room(tarloc) for other, loc, in self.positions if other[0] != amphipod[0])
        )
        no_bis_repetita = (amphipod, curloc, tarloc) not in self.history
        return no_bis_repetita and target_allowed and could_be_useful and path_is_free and room_is_safe and (
            not in_hallway
            or (in_hallway and tarloc[0] == amphipod[0] )
            )

    def play(self, move):
        amphipod, curloc, tarloc = move
        self.positions[amphipod] = tarloc
        self.possible_empty_dests = self.allowed_dests - set(self.positions.values())
        self.currently_empty = self.slots - set(self.positions.values())
        self.history.append(move)
    def unplay(self, move):
        assert self.history[-1] == move
        amphipod, curloc, tarloc = move
        self.positions[amphipod] = curloc
        self.possible_empty_dests = self.allowed_dests - set(self.positions.values())
        self.currently_empty = self.slots - set(self.positions.values())
        self.history.pop()

def solve(positions):
    game_state = GameState(positions)
    seen_positions = { }
    def recurse():
        if game_state.total_cost() >= 14000:
            return
        for move in game_state.possible_moves():
            game_state.play(move)
            current_cost = game_state.total_cost()
            if game_state.is_complete():
                print("solution found, cost:", game_state.total_cost())
                print(game_state.history)
                print(game_state.positions)
            if current_cost >= 14000:
                game_state.unplay(move)
                continue
            signature = game_state.signature()
            if signature in seen_positions and seen_positions[signature] <= current_cost:
                game_state.unplay(move)
                continue
            seen_positions[signature] = current_cost
            recurse()
            game_state.unplay(move)
    recurse()



def main():
    inpt = {
        ("Bx", "A1"),
        ("Ax", "A2"),
        ("Cx", "B1"),
        ("Dx", "B2"),
        ("By", "C1"),
        ("Cy", "C2"),
        ("Dy", "D1"),
        ("Ay", "D2")
    }

    # gs = GameState(inpt)
    # moves = gs.possible_moves()
    solve(inpt)
    # print(moves)

if __name__ == '__main__':
    main()



