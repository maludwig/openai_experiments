#!/usr/bin/env python
import sys
import unittest
from io import StringIO
from unittest.mock import patch

from experiments.helpers.token_helpers import count_tokens, tokenize, print_pricing_message


class TestTokenHelpers(unittest.TestCase):
    """
    A class that tests the token_helpers module functions.
    """

    def test_count_tokens(self):
        """
        Test the count_tokens function with various inputs.
        """

        # Test empty string
        self.assertEqual(0, count_tokens(""))

        # Test string with one token
        self.assertEqual(1, count_tokens("Hello"))

        # Test string with multiple tokens
        self.assertEqual(4, count_tokens("Hello, World!"))

    def test_tokenize(self):
        """
        Test the tokenize function with various inputs.
        """

        # Test empty string
        self.assertEqual([], tokenize(""))

        # Test string with one token
        self.assertEqual([9906], tokenize("Hello"))

        # Test string with multiple tokens
        self.assertEqual([9906, 11, 4435, 0], tokenize("Hello, World!"))

    @patch("builtins.print")
    def test_print_pricing_message(self, mock_print):
        """
        Test the print_pricing_message function with a known token count to ensure correct output format.
        """

        test_token_count = 1000
        # Test print_pricing_message
        print_pricing_message(test_token_count)

        # Ensure that the output is correct
        mock_print.assert_called_once_with("\x1b[38;2;255;255;0mToken count: 1000, price at this context: $0.03 USD\x1b[49m\x1b[39m")


if __name__ == "__main__":
    unittest.main()
