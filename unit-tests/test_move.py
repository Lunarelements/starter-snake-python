import unittest
from move import Move

class TestMove(unittest.TestCase):

    def setUp(self):
        self.move = Move("up", 1, 0)

    def test_coordinates(self):
        self.assertEqual(self.move.coordinates(), {'x': 1, 'y': 0})
        self.assertIn(self.move.coordinates(), [{'x': 1, 'y': 0}, [{'x': 0, 'y': 1}]])
        self.assertNotIn(self.move.coordinates(), [{'x': 1, 'y': 1}, [{'x': 1, 'y': 2}]])

if __name__ == '__main__':
    unittest.main()