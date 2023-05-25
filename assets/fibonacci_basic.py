class FibonacciMemoizer:
    def __init__(self):
        self.fibonacci_numbers = [1, 1, 2]

    def fibonacci(self, n):
        if len(self.fibonacci_numbers) <= n:
            # Calculate the nth fibonacci number by adding the previous two fibonacci numbers.
            self.fibonacci_numbers.append(self.fibonacci(n - 1) + self.fibonacci(n - 2))
        # Return the nth fibonacci number.
        return self.fibonacci_numbers[n]


def main():
    fibonacci_memoizer = FibonacciMemoizer()
    # Calculate the first 100 fibonacci numbers.
    fibonacci_memoizer.fibonacci(100)
    print(fibonacci_memoizer.fibonacci_numbers)


if __name__ == "__main__":
    main()
