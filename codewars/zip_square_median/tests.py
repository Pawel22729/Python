import unittest
from zip_square_median import solution

class TestMain(unittest.TestCase):
    def test(self):
        self.assertEqual(solution([1,2,3], [4,5,6]), 9)
        self.assertEqual(solution([10, 20, 10, 2], [10, 25, 5, -2]), 16.5)
        self.assertEqual(solution([-1, 0], [0, -1]), 1)

if __name__ == '__main__':
    unittest.main()
