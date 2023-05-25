#!/usr/bin/env python
"""
Please write me a python class which will implement an on-disk cache. The DiskCache object should have a `get(key,getter_fn)` function that will return the data saved onto the disk, in the event that the data exists. If it does not exist, then it should call the getter_fn, and write down the result to disk. the getter_fn always returns a JSON serializable dict. The data from each key should be stored in a separate file.
"""
import os
import json
from os.path import realpath


class DiskCache:
    """
    A Python class that implements an on-disk cache.
    Each cached value will be stored in a separate file.
    """

    def __init__(self, cache_dir: str = "cache"):
        """
        Initialize the DiskCache object.
        :param cache_dir: cache directory where the cached files will be stored.
        """
        self.cache_dir = realpath(cache_dir)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

    def _get_cache_path(self, key: str) -> str:
        """
        Get the cache file path for the given key.
        :param key: the key to get the cache file path for.
        :return: the cache file path.
        """
        return os.path.join(self.cache_dir, f"{key}.json")

    def get(self, key: str, getter_fn) -> dict:
        """
        Return the data from the disk cache if it exists.
        If it does not exist, call the getter_fn, save the result to disk, and return the result.
        :param key: the key to look up in the cache.
        :param getter_fn: the function to call if the data does not exist in the cache.
        :return: the data.
        """
        cache_path = self._get_cache_path(key)

        if os.path.exists(cache_path):
            with open(cache_path, "r") as cache_file:
                return json.load(cache_file)
        else:
            data = getter_fn()
            with open(cache_path, "w") as cache_file:
                json.dump(data, cache_file)
            return data


if __name__ == "__main__":
    # Example usage of the DiskCache class:
    cache = DiskCache()

    # Define a simple getter function that returns a JSON serializable dictionary.
    def example_getter():
        return {"example": "data"}

    # Get the data from the disk cache using the "example_key".
    cached_data = cache.get("example_key", example_getter)
    print(cached_data)
