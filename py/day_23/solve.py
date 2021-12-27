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

    def possible_moves(self):
        possible_moves = []
        for amphipod, curloc in self.positions.items():
            for tarloc in self.possible_empty_dests:
                print(amphipod, curloc, tarloc)
                if self.can_move(amphipod, curloc, tarloc):
                    possible_moves.append((amphipod, curloc, tarloc))
        return possible_moves

    def can_move(self, amphipod, curloc, tarloc):
        # TODO : finish this function. Cleanup. Fix logic.
        target_allowed = tarloc in self.possible_empty_dests
        in_hallway = curloc[0] == "H"
        path_is_free = all(c in self.currently_empty for c in self.paths[(curloc, tarloc)][1:])
        room_is_safe = tarloc[0] == "H" or (
            tarloc[0] == amphipod[0]
            and
            not any(loc == other_room(tarloc) for other, loc, in self.positions)
        )
        return target_allowed and path_is_free and room_is_safe and (
            not in_hallway
            or (in_hallway and tarloc[0] == amphipod[0] )
            )

def solve():
    game_state = GameState()
    def recurse():
        for move in possible_moves(game_state):
            game_state.play(move)
            if game.is_complete():
                print(game_state.total_cost())
                return
            if game.total_cost() >= 14000:
                return
            recurse()
            game_state.unplay(move)



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

    gs = GameState(inpt)
    moves = gs.possible_moves()
    print(moves)

if __name__ == '__main__':
    main()



