from unittest import TestCase

from .fibonacci import FibonacciMemoizer


class TestFibonacci(TestCase):
    """
    A class that tests the FibonacciMemoizer.
    """

    def test_fibonacci_5(self):
        """
        Test the fibonacci memoizer.
        First, we will calculate the first 5 fibonacci numbers.
        Then, we will ensure that the numbers are correct.
        :return:
        """
        # Create a fibonacci memoizer.
        fibonacci_memoizer = FibonacciMemoizer()
        # Calculate the first 5 fibonacci numbers.
        fibonacci_memoizer.fibonacci(5)
        # Ensure that the numbers are correct
        expected = [1, 1, 2, 3, 5, 8]
        self.assertEqual(expected, fibonacci_memoizer.fibonacci_numbers)

    def test_fibonacci_0(self):
        """
        Test the 0 edge case.
        :return:
        """
        # Create a fibonacci memoizer.
        fibonacci_memoizer = FibonacciMemoizer()
        # Calculate the 0th fibonacci number.
        fibonacci_memoizer.fibonacci(0)
        # Ensure that the numbers are correct
        expected = [1]
        self.assertEqual(expected, fibonacci_memoizer.fibonacci_numbers)

    def test_fibonacci_1(self):
        """
        Test the 1 edge case.
        :return:
        """
        # Create a fibonacci memoizer.
        fibonacci_memoizer = FibonacciMemoizer()
        # Calculate 2 fibonacci numbers.
        fibonacci_memoizer.fibonacci(1)
        # Ensure that the numbers are correct
        expected = [1, 1]
        self.assertEqual(expected, fibonacci_memoizer.fibonacci_numbers)
