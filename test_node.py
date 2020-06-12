import unittest
from node import Node

class TestNode(unittest.TestCase):

     def test_get_direction(self):
        node = Node(True, 0, 1)
        direction = node.get_direction({"x" : 0, "y" : 0})
        self.assertEqual("up", direction)

if __name__ == '__main__':
    unittest.main()