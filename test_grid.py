import unittest
from grid import Grid
from node import Node
import copy

class TestGrid(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.node_a = Node(True, 0, 0)
        self.node_b = Node(True, 1, 0)
        self.node_b.parent = self.node_a
        self.node_c = Node(True, 0, 1)
        self.node_d = Node(True, 1, 1)
        self.node_d.parent = self.node_b
        self.node_e = Node(True, 1, 2)
        self.node_e.parent = self.node_d
        self.node_f = Node(True, 1, 3)
        self.node_f.parent = self.node_e
        self.node_g = Node(True, 1, 4)
        self.node_g.parent = self.node_f
        self.board = {
            "height": 11,
            "width": 11,
            "food": [
                {"x": 5, "y": 5}, 
                {"x": 9, "y": 0}, 
                {"x": 2, "y": 6}
            ],
            "snakes": [
                {
                    "id": "snake-508e96ac-94ad-11ea-bb37",
                    "name": "My Snake",
                    "health": 54,
                    "body": [
                    {"x": 0, "y": 0}, 
                    {"x": 1, "y": 0}, 
                    {"x": 2, "y": 0}
                    ],
                    "head": {"x": 0, "y": 0},
                    "length": 3,
                    "shout": "why are we shouting??"
                }, 
                {
                    "id": "snake-b67f4906-94ae-11ea-bb37",
                    "name": "Another Snake",
                    "health": 16,
                    "body": [
                    {"x": 5, "y": 4}, 
                    {"x": 5, "y": 3}, 
                    {"x": 6, "y": 3},
                    {"x": 6, "y": 2}
                    ],
                    "head": {"x": 5, "y": 4},
                    "length": 4,
                    "shout": "I'm not really sure..."
                }
            ]
        }
        self.board_grid = Grid(self.board["width"], self.board["height"])

    def test_insert_snakes(self):
        result = copy.deepcopy(self.board_grid)
        expected = copy.deepcopy(self.board_grid)
        expected.grid[0][0].safe = False
        expected.grid[0][0].certainty = -100
        expected.grid[0][1].safe = False
        expected.grid[0][1].certainty = -100
        expected.grid[4][5].safe = False
        expected.grid[4][5].certainty = -100
        expected.grid[3][5].safe = False
        expected.grid[3][5].certainty = -100
        expected.grid[3][6].safe = False
        expected.grid[3][6].certainty = -100
        result.insert_snakes(self.board["snakes"])
        self.assertEqual(expected, result)

    def test_get_neighbours(self):
        neighbours = self.board_grid.get_neighbours(Node(True, 0, 0))
        self.assertEqual([Node(True, 0, 1), Node(True, 1, 0)], neighbours)
        neighbours = self.board_grid.get_neighbours(Node(True, 5, 5))
        self.assertEqual([Node(True, 4, 5), Node(True, 5, 4), Node(True, 5, 6), Node(True, 6, 5)], neighbours)

    def test_insert_path(self):
        result = copy.deepcopy(self.board_grid)
        expected = copy.deepcopy(self.board_grid)
        expected.grid[0][0].certainty = 0.5/3
        expected.grid[1][0].certainty = 0.5/3
        expected.grid[2][0].certainty = 0.5/3
        result.insert_path([Node(True, 0, 0), Node(True, 0, 1), Node(True, 0, 2)])
        self.assertEqual(expected, result)

    def test_insert_rooms(self):
        result = copy.deepcopy(self.board_grid)
        expected = copy.deepcopy(self.board_grid)
        expected.grid[0][0].certainty = 0.2
        expected.grid[1][0].certainty = 0.2
        expected.grid[1][1].certainty = 0.2
        expected.grid[0][1].certainty = 0.2
        result.insert_rooms([[Node(True, 0, 0), Node(True, 0, 1), Node(True, 1, 1), Node(True, 1, 0)], [Node(True, 1, 2), Node(True, 1, 3)]])
        result.printGridCertainty()
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()