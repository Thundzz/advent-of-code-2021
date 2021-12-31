import unittest
from solve import GameState

class TestDay23(unittest.TestCase):

    def test_can_move_c_amphipod_to_destination(self):
        positions = {
            ("B", "A1"),
            ("A", "A2"),
            ("C", "B1"),
            ("D", "B2"),
            ("B", "H3"),
            ("C", "C2"),
            ("D", "D1"),
            ("A", "D2")
        }
        gs = GameState(positions)
        assert gs.can_move("Cx", "B1", "C1"), "Cx should be able to move from B1 to C1"

    def test_can_move_c_amphipod_to_destination_after_first_move(self):
        positions = {
            ("B", "A1"),
            ("A", "A2"),
            ("C", "B1"),
            ("D", "B2"),
            ("B", "C1"),
            ("C", "C2"),
            ("D", "D1"),
            ("A", "D2")
        }
        gs = GameState(positions)
        gs.play(("By", "C1", "H3"))
        assert gs.can_move("Cx", "B1", "C1"), "Cx should be able to move from B1 to C1"


    def test_can_move_c_amphipod_to_destination_after_first_move_2(self):
        positions = {
            ("B", "A1"),
            ("A", "A2"),
            ("C", "B1"),
            ("D", "B2"),
            ("B", "C1"),
            ("C", "C2"),
            ("D", "D1"),
            ("A", "D2")
        }
        gs = GameState(positions)
        gs.play(("B", "C1", "H3"))
        assert ("C", "B1", "C1") in gs.possible_moves(), 'move should be there'

    def test_c_wont_move_after_being_fully_positioned(self):
        positions = {
            ("B", "A1"),
            ("A", "A2"),
            ("C", "B1"),
            ("D", "B2"),
            ("B", "C1"),
            ("C", "C2"),
            ("D", "D1"),
            ("A", "D2")
        }
        gs = GameState(positions)
        gs.play(("B", "C1", "H3"))
        gs.play(("C", "B1", "C1"))
        for amphipod, source, dest in gs.possible_moves():
            print(amphipod, source, dest)
            assert amphipod != "C"


if __name__ == '__main__':
    unittest.main()