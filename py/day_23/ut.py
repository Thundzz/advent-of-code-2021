import unittest
from solve import GameState

class TestSnailFishOps(unittest.TestCase):

    def test_can_move_c_amphipod_to_destination(self):
        positions = {
            ("Bx", "A1"),
            ("Ax", "A2"),
            ("Cx", "B1"),
            ("Dx", "B2"),
            ("By", "H3"),
            ("Cy", "C2"),
            ("Dy", "D1"),
            ("Ay", "D2")
        }
        gs = GameState(positions)
        assert gs.can_move("Cx", "B1", "C1"), "Cx should be able to move from B1 to C1"

    def test_can_move_c_amphipod_to_destination_after_first_move(self):
        positions = {
            ("Bx", "A1"),
            ("Ax", "A2"),
            ("Cx", "B1"),
            ("Dx", "B2"),
            ("By", "C1"),
            ("Cy", "C2"),
            ("Dy", "D1"),
            ("Ay", "D2")
        }
        gs = GameState(positions)
        gs.play(("By", "C1", "H3"))
        assert gs.can_move("Cx", "B1", "C1"), "Cx should be able to move from B1 to C1"


    def test_can_move_c_amphipod_to_destination_after_first_move_2(self):
        positions = {
            ("Bx", "A1"),
            ("Ax", "A2"),
            ("Cx", "B1"),
            ("Dx", "B2"),
            ("By", "C1"),
            ("Cy", "C2"),
            ("Dy", "D1"),
            ("Ay", "D2")
        }
        gs = GameState(positions)
        gs.play(("By", "C1", "H3"))
        assert ("Cx", "B1", "C1") in gs.possible_moves(), 'move should be there'

if __name__ == '__main__':
    unittest.main()