import unittest
import battlesnake
from move import Move

class TestBattlesnake(unittest.TestCase):

    def setUp(self):
        self.body = [
            {"x": 0, "y": 0}, 
            {"x": 1, "y": 0}, 
            {"x": 2, "y": 0}
        ]
        self.board = {
            "height": 11,
            "width": 11,
            "food": [
                {"x": 5, "y": 5}, 
                {"x": 9, "y": 0}, 
                {"x": 2, "y": 6}
            ],
            "snakes": []
        }

    def test_generate_possible_moves(self):
        # Snake neck is on the right, so the only moves are up, down and left
        self.assertListEqual(battlesnake.generate_possible_moves(self.body),
            [Move("up", 0, 1), Move("down", 0, -1), Move("left", -1, 0)]
        )

    def test_can_avoid_wall(self):
        self.assertTrue(battlesnake.can_avoid_wall({"x": 0, "y" : 0}, self.board))
        self.assertFalse(battlesnake.can_avoid_wall({"x": -1, "y" : 0}, self.board))
        self.assertFalse(battlesnake.can_avoid_wall({"x": self.board["width"], "y" : 0}, self.board))
        self.assertFalse(battlesnake.can_avoid_wall({"x": 2, "y" : self.board["height"] + 4}, self.board))

if __name__ == '__main__':
    unittest.main()