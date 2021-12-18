import unittest
from solve import explode, split, reduce_sfn

class TestSnailFishOps(unittest.TestCase):

    def test_explode_1(self):
        _, res = explode("[[[[[9,8],1],2],3],4]")
        self.assertEqual(res, "[[[[0,9],2],3],4]")

    def test_explode_2(self):
        _, res = explode("[7,[6,[5,[4,[3,2]]]]]")
        self.assertEqual(res, "[7,[6,[5,[7,0]]]]")

    def test_explode_3(self):
        _, res = explode("[[6,[5,[4,[3,2]]]],1]")
        self.assertEqual(res, "[[6,[5,[7,0]]],3]")

    def test_explode_4(self):
        _, res = explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
        self.assertEqual(res, "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")

    def test_explode_5(self):
        _, res = explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
        self.assertEqual(res, "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")

    def test_explode_5(self):
        _, res = explode("[[3,[2,[8,0]]],[9,[5,[4,[6,2]]]]]")
        self.assertEqual(res, "[[3,[2,[8,0]]],[9,[5,[10,0]]]]")

    def test_split_1(self):
        _, res = split("[[[[0,7],4],[15,[0,13]]],[1,1]]")
        self.assertEqual(res, "[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")

    def test_split_2(self):
        _, res = split("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
        self.assertEqual(res, "[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]")

    def test_reduce_1(self):
        res = reduce_sfn("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
        self.assertEqual(res, "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

if __name__ == '__main__':
    unittest.main()