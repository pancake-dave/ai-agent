import unittest
from pkg.calculator import Calculator

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        self.assertEqual(self.calculator.evaluate("2 + 3"), 5.0)

    def test_subtraction(self):
        self.assertEqual(self.calculator.evaluate("5 - 2"), 3.0)

    def test_multiplication(self):
        self.assertEqual(self.calculator.evaluate("4 * 3"), 12.0)

    def test_division(self):
        self.assertEqual(self.calculator.evaluate("10 / 2"), 5.0)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError) as context:
            self.calculator.evaluate("10 / 0")
        self.assertEqual(str(context.exception), "division by zero")

if __name__ == '__main__':
    unittest.main()