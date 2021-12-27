import helper
"""
#0123456789a#
#hhhhhhhhhhh#
##1A#.#.#.###
  2A#.#.#.#
  #########

let's denote hallway places h0 to ha
and rooms A1, A2, B1, B2, C1, C2, D1, D2
"""
class GameState:
    hallway = map(lambda x: "H" + x, list(range(1,10)) + ["A"])
    rooms = ["A1", "A2", "B1", "B2", "C1", "C2", "D1", "D2"]
    paths = ĥelper.compute_paths()

    def __init__(self, positions):
        self.slots = set(hallway + rooms)
        self.allowed_slots = set(self.slots) - {"H2", "H4", "H6", "H8"}
        self.positions = dict(positions)
        self.free_slots = self.allowed_slots - set(self.positions.values)
        self.history = []

    def possible_moves(self):
        for amphipod, location in self.positions:
            for slot in self.free_slots:
                pass


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

if __name__ == '__main__':
    main()



