import unittest
import pathfinding
from node import Node
from grid import Grid

class TestPathfinding(unittest.TestCase):
    
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
        self.board_grid = Grid(11, 11)

    def test_get_distance(self):
        self.assertEqual(1, pathfinding.get_distance(self.node_a, self.node_b))
        self.assertEqual(1, pathfinding.get_distance(self.node_a, self.node_c))
        self.assertEqual(2, pathfinding.get_distance(self.node_a, self.node_d))
        self.assertEqual(5, pathfinding.get_distance(self.node_a, self.node_g))
        self.assertEqual(0, pathfinding.get_distance(self.node_a, self.node_a))

    def test_retrace_path(self):
        path = pathfinding.retrace_path(self.node_a, self.node_g)
        self.assertEqual([self.node_a, self.node_b, self.node_d, self.node_e, self.node_f, self.node_g], path)

    def test_find_path(self):
        path = pathfinding.find_path(self.board_grid, self.node_a, self.node_g)
        self.assertEqual([self.node_a, self.node_b, self.node_d, self.node_e, self.node_f, self.node_g], path)
        self.board_grid.insert_path(path)

if __name__ == '__main__':
    unittest.main()