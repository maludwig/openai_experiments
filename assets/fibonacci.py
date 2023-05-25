class FibonacciMemoizer:
    """
    A class that memoizes the fibonacci series, so that it does not need to be
    regenerated.
    """

    def __init__(self):
        """
        Initialize the fibonacci memoizer.
        """
        # Initialize the list of fibonacci numbers with the first three numbers.
        self.fibonacci_numbers = []

    def fibonacci(self, n: int) -> int:
        """
        Calculate the nth fibonacci number.
        :param n: The index of the fibonacci number to calculate.
        :return: The nth fibonacci number.
        """
        # If we have not previously calculated the nth fibonacci number, calculate it.
        if len(self.fibonacci_numbers) <= n:
            if n <= 1:
                if n == 1:
                    self.fibonacci_numbers.append(1)
                # The 0th and 1st fibonacci numbers are 1.
                self.fibonacci_numbers.append(1)
            else:
                # Calculate the nth fibonacci number by adding the previous two fibonacci numbers.
                # Store the result in the list of fibonacci numbers. Note that this will always append
                # the result to the end of the list, which will always be the correct location, because
                # we are calculating the fibonacci numbers in order.
                self.fibonacci_numbers.append(self.fibonacci(n - 2) + self.fibonacci(n - 1))
        # Return the nth fibonacci number.
        return self.fibonacci_numbers[n]


def main():
    """
    The main function for the fibonacci memoizer.
    This is called when the script is run directly.
    """
    # Create a fibonacci memoizer.
    fibonacci_memoizer = FibonacciMemoizer()
    # Calculate the first 100 fibonacci numbers.
    fibonacci_memoizer.fibonacci(100)
    # Print the result
    print(fibonacci_memoizer.fibonacci_numbers)


if __name__ == "__main__":
    main()
