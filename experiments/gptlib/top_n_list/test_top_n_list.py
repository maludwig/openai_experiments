#!/usr/bin/env python
"""
extracts the concept of a top_n item list from the code below. I want it to be based on a given lambda function named "key", and a max_length integer n. The class should be called "TopNList" and should have an "addItem" function that takes in a new item to possibly add to the list, if the item happens to be in the top "n" based on the "key" function. The code I have currently works, but I want to make it generic. I also want an "addItems" and "asSortedList" function. Here is my current code:

"""
import unittest

from top_n_list import TopNList


class TestTopNList(unittest.TestCase):
    """
    A class that tests the TopNList.
    """

    def test_addItem(self):
        # Create a TopNList instance with a simple key function and max_length 3.
        top_n_list = TopNList(lambda x: x, 3)

        # Add some test items and check the top 3.
        test_items = [1, 2, 5, 3, 4]
        for item in test_items:
            top_n_list.addItem(item)

        result = top_n_list.asSortedList()
        self.assertEqual(result, [(3, 3), (4, 4), (5, 5)])

    def test_addItems(self):
        # Create a TopNList instance with a custom key function and max_length 4.
        similarity_to_5 = lambda x: -abs(x - 5)
        top_n_list = TopNList(similarity_to_5, 5)

        # Add a list of test items at once and check the top 4.
        test_items = [9, 8, 7, 6, 5, 4, 3, 2, 1]
        top_n_list.addItems(test_items)

        result = top_n_list.asSortedList()
        expected = [(-2, 3), (-2, 7), (-1, 4), (-1, 6), (0, 5)]
        self.assertEqual(expected, result)

    def test_asSortedList(self):
        # Create a TopNList instance with a simple key function and max_length 5.
        top_n_list = TopNList(lambda x: x, 5)

        # Add some test items and get the sorted top 5 list.
        test_items = [4, 8, 12, 4, 6, 1]
        for item in test_items:
            top_n_list.addItem(item)

        result = top_n_list.asSortedList()
        self.assertEqual(result, [(4, 4), (4, 4), (6, 6), (8, 8), (12, 12)])

    def test_edge_case(self):
        # Create a TopNList instance with a simple key function and max_length 0.
        top_n_list = TopNList(lambda x: x, 0)

        # Add some test items.
        test_items = [1, 2, 3, 4]
        for item in test_items:
            top_n_list.addItem(item)

        # Expect an empty result because max_length is 0.
        result = top_n_list.asSortedList()
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
