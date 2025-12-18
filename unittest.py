import unittest
from math_function import add_numbers

class TestAddNumbers(unittest.TestCase):

  def test_add_two_positive_numbers(self):
    self.assertEqual(add_numbers(2,3),5)

  def test_add_two_negative_and_positive(self):
    self.assertEqual(add_numbers(-1,4),3)

if __name__ == "__main__":
    unittest.main()
