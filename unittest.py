import unittest
from math_function import add_numbers

# define the unit tests
class my_unit_tests(unittest.TestCase):
    def test_add(self):

        # test adding negative integers
        self.assertEqual(add_numbers(4,5),9)

        # test adding floats"
        self.assertEqual(add_numbers(3,2),5)

# run the tests
if __name__ == "__main__":
    unittest.main()
