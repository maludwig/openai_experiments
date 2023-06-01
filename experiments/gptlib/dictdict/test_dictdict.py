#!/usr/bin/env python
"""
I want to write a class called "DictDict" that subclasses collections.UserDict, uses "self.data", but accepts keys that are themselves dictionaries, and the key might be huge, more than 12KB. I also want the DictDict class to have a function "DictDict.load(file_path:str)" that loads a saved DictDict from a file into a new DictDict object, and also a save(file_path:str) function that saves the self dictdict to the specified file.
"""
import unittest
import os

from experiments.gptlib.dictdict.dictdict import DictDict


class TestDictDict(unittest.TestCase):
    def test_operations(self):
        dd = DictDict()

        # Test __setitem__ and __getitem__
        dd[{1: "a", 2: "b"}] = "test1"
        self.assertEqual("test1", dd[{1: "a", 2: "b"}])

        # Test unhashable key
        with self.assertRaises(TypeError):
            unhashable_dict = {"a": "b"}
            unhashable_dict["c"] = unhashable_dict
            dd[unhashable_dict] = "test2"

        # Test deletion of item
        key = {1: "a", 2: "b"}
        dd[key] = "test3"
        del dd[key]
        with self.assertRaises(KeyError):
            _ = dd[key]

    def test_save_load(self):
        dd1 = DictDict()

        dd1[{1: "a", 2: "b"}] = "test1"
        dd1[{3: "c", 4: "d"}] = "test2"

        # Save the DictDict instance to a file
        dd1.save("test_dictdict.pkl")

        # Load the saved DictDict instance from the file
        dd2 = DictDict.load("test_dictdict.pkl")

        # Delete the test file to clean up
        os.remove("test_dictdict.pkl")

        # Check if the loaded DictDict is equivalent to the original
        self.assertEqual(dd1.data, dd2.data)


if __name__ == "__main__":
    unittest.main()
