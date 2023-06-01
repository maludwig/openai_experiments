#!/usr/bin/env python
"""
Auto-comment-and-document
"""
import unittest
from unittest.mock import patch
from io import StringIO

from experiments.helpers.io_helpers import multiline_input


class TestIOHelpers(unittest.TestCase):
    """
    A class to test the IO helper functions.
    """

    @patch("sys.stdin", StringIO("hello\n"))
    def test_multiline_input_single_line(self):
        """
        Test the multiline_input function for a single line of input.
        """
        # Call multiline_input with mocked input
        user_response = multiline_input()

        # Check that the input is correct
        expected = "hello"
        self.assertEqual(expected, user_response)

    @patch("sys.stdin", StringIO("hello<<EOF\nworld\nEOF\n"))
    def test_multiline_input_multiple_lines(self):
        """
        Test the multiline_input function for multiple lines of input.
        """
        # Call multiline_input with mocked input
        user_response = multiline_input()

        # Check that the input is a combination of both lines separated by a newline
        expected = "hello\nworld"
        self.assertEqual(expected, user_response)

    @patch("sys.stdin", StringIO("exit\n"))
    def test_multiline_input_exit(self):
        """
        Test the multiline_input function for the 'exit' command.
        """
        # Call multiline_input with mocked input
        user_response = multiline_input()

        # Check that the input is "exit"
        expected = "exit"
        self.assertEqual(expected, user_response)

    @patch("sys.stdin", StringIO(""))
    def test_multiline_input_EOFError(self):
        """
        Test the multiline_input function for the EOFError.
        """

        def fake_input(prompt):
            raise EOFError

        # Call multiline_input with mocked input
        user_response = multiline_input("> ", input_fn=fake_input)

        # Check that the input is "exit" to handle EOFError properly
        expected = "exit"
        self.assertEqual(expected, user_response)


if __name__ == "__main__":
    unittest.main()
