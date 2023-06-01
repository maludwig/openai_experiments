#!/usr/bin/env python
"""
has a function that takes a markdown document in as a string, and removes any whitespace from any lines that are not inside a code block tag "```" or "```python" etc. If the whitespace is in a code block tag, it leave it alone. It should only remove leading whitespace from the start of the line.
"""
import unittest

from experiments.gptlib.whitespace_trimmer.remove_whitespace import remove_leading_whitespace


class TestRemoveWhitespace(unittest.TestCase):
    """
    A class that tests the remove_leading_whitespace function.
    """

    def test_basic_example(self):
        # Define a sample markdown document.
        sample_markdown = """\
## Example Markdown

This is a sample markdown document.

    This line has leading whitespace.
"""

        # Define the expected output without leading whitespace.
        expected_output = """\
## Example Markdown

This is a sample markdown document.

This line has leading whitespace.
"""
        # Test if the function works as expected.
        self.assertEqual(remove_leading_whitespace(sample_markdown), expected_output)

    def test_empty_input(self):
        # Test an empty input string
        self.assertEqual(remove_leading_whitespace(""), "")

    def test_no_whitespace(self):
        # Test an input string without leading whitespace
        sample_markdown = """\
Markdown without leading whitespace.
Another line without leading whitespace.

            This is a code block
            with leading whitespace
        ```"""
        expected_output = """Markdown without leading whitespace.
Another line without leading whitespace.

This is a code block
with leading whitespace
```"""
        # The function should not modify the input in this case.
        self.assertEqual(remove_leading_whitespace(sample_markdown), expected_output)

    def test_nested_code_blocks(self):
        # Test an input string with nested code blocks.
        sample_markdown = """\
        Line 1
        Line 2

            This is a code block
            ```
            This is a nested code block
            ```
            Back to the outer code block
        ```"""
        expected_output = """Line 1
Line 2

This is a code block
```
            This is a nested code block
```
Back to the outer code block
```"""
        self.assertEqual(remove_leading_whitespace(sample_markdown), expected_output)

    if __name__ == "__main__":
        unittest.main()
