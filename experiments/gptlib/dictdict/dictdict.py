#!/usr/bin/env python
"""
I want to write a class called "DictDict" that subclasses collections.UserDict, uses "self.data", but accepts keys that are themselves dictionaries, and the key might be huge, more than 12KB. I also want the DictDict class to have a function "DictDict.load(file_path:str)" that loads a saved DictDict from a file into a new DictDict object, and also a save(file_path:str) function that saves the self dictdict to the specified file.
"""
import collections
import hashlib
import json


class DictDict(collections.UserDict):
    """
    A dictionary-like class that subclasses collections.UserDict.
    This class accepts keys that are dictionaries.
    """

    def __getitem__(self, key: dict) -> any:
        """
        Get the value associated with the given key (which is a dictionary)
        :param key: The dictionary key
        :return: The value associated with the key
        """
        hashed_key = DictDict.generate_hash(key)
        return self.data[hashed_key]

    def __setitem__(self, key: dict, value: any) -> None:
        """
        Set the value associated with the given key (which is a dictionary)
        :param key: The dictionary key
        :param value: The value to be set
        :return: None
        """
        hashed_key = DictDict.generate_hash(key)
        self.data[hashed_key] = value

    def __delitem__(self, key: dict) -> None:
        """
        Delete the item with the given key (which is a dictionary)
        :param key: The dictionary key
        :return: None
        """
        hashed_key = DictDict.generate_hash(key)
        del self.data[hashed_key]

    def __contains__(self, key: dict) -> bool:
        """
        Checks if a key is in the dictionary
        :param key: The dictionary key
        :return: True if the key is in the dictionary, False otherwise
        """
        hashed_key = DictDict.generate_hash(key)
        return hashed_key in self.data

    def save(self, file_path: str) -> None:
        """
        Save the DictDict to a file
        :param file_path: The path to the file where the DictDict will be saved
        :return: None
        """
        with open(file_path, "w") as f:
            json.dump(self.data, f)

    @staticmethod
    def generate_hash(d: dict) -> str:
        """
        Generate a hash for the given dictionary.
        :param d: The dictionary to generate a hash for.
        :return: The generated hash as a string.
        """
        try:
            json_data = json.dumps(d, sort_keys=True).encode("utf-8")
        except ValueError as e:
            # Dictionary is not serializable
            raise TypeError(str(e))
        return hashlib.sha256(json_data).hexdigest()

    @classmethod
    def load(cls, file_path: str) -> "DictDict":
        """
        Load the DictDict from a file
        :param file_path: The path to the file where the DictDict has been saved
        :return: The loaded DictDict object
        """
        d = DictDict()
        with open(file_path, "r") as f:
            d.data = json.load(f)
        return d
