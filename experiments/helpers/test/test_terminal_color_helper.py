#!/usr/bin/env python
"""
Auto-comment-and-document
"""
import unittest
from experiments.helpers.terminal_color_helper import f_to_i, fg, bg, bias


class TestTerminalColorHelper(unittest.TestCase):
    def test_f_to_i(self):
        self.assertEqual((255, 255, 255), f_to_i(-0.5, -0.5, -0.5))
        self.assertEqual((0, 0, 0), f_to_i(1.5, 1.5, 1.5))
        self.assertEqual((0, 0, 0), f_to_i(0, 0, 0))
        self.assertEqual((255, 255, 255), f_to_i(1, 1, 1))
        self.assertEqual((63, 127, 191), f_to_i(0.25, 0.5, 0.75))

    def test_fg(self):
        self.assertEqual("\x1b[38;2;255;255;255m", fg(-0.5, -0.5, -0.5))
        self.assertEqual("\x1b[38;2;0;0;0m", fg(1.5, 1.5, 1.5))
        self.assertEqual("\x1b[38;2;0;0;0m", fg(0, 0, 0))
        self.assertEqual("\x1b[38;2;255;255;255m", fg(1, 1, 1))
        self.assertEqual("\x1b[38;2;63;127;191m", fg(0.25, 0.5, 0.75))

    def test_bg(self):
        self.assertEqual("\x1b[48;2;255;255;255m", bg(-0.5, -0.5, -0.5))
        self.assertEqual("\x1b[48;2;0;0;0m", bg(1.5, 1.5, 1.5))
        self.assertEqual("\x1b[48;2;0;0;0m", bg(0, 0, 0))
        self.assertEqual("\x1b[48;2;255;255;255m", bg(1, 1, 1))
        self.assertEqual("\x1b[48;2;63;127;191m", bg(0.25, 0.5, 0.75))

    def test_bias(self):
        self.assertEqual((0, 0, 0), bias(0, 0, 0, 0))
        self.assertEqual((1, 1, 1), bias(0, 0, 0, 1))
        self.assertEqual((-1, -1, -1), bias(0, 0, 0, -1))
        self.assertEqual((0.75, 0.5, 0.25), bias(0.5, 0.25, 0.0, 0.25))
        self.assertEqual((-0.25, -0.25, -0.25), bias(0, 0, 0, -0.25))


if __name__ == "__main__":
    unittest.main()
