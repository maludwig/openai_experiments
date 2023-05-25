#!/usr/bin/env python
"""
Please write me a python class which will implement an on-disk cache. The DiskCache object should have a `get(key,getter_fn)` function that will return the data saved onto the disk, in the event that the data exists. If it does not exist, then it should call the getter_fn, and write down the result to disk. the getter_fn always returns a JSON serializable dict. The data from each key should be stored in a separate file.
"""
import os
import json
import tempfile
import shutil
from unittest import TestCase

from disk_cache import DiskCache


class TestDiskCache(TestCase):
    def setUp(self):
        # Create a temporary directory for the cache.
        self.temp_dir = tempfile.mkdtemp()
        self.cache = DiskCache(cache_dir=self.temp_dir)

    def tearDown(self):
        # Remove the temporary directory after the test.
        shutil.rmtree(self.temp_dir)

    def test_get_cache_path(self):
        # Test that the cache path is generated correctly.
        cache_path = self.cache._get_cache_path("test_key")
        expected_path = os.path.join(self.temp_dir, "test_key.json")
        self.assertEqual(expected_path, cache_path)

    def test_get_cached_data(self):
        # Create a sample cache file.
        test_key = "test_key"
        test_data = {"value": 42}
        cache_path = self.cache._get_cache_path(test_key)
        with open(cache_path, "w") as cache_file:
            json.dump(test_data, cache_file)

        # Test that the get method returns the correct cached data.
        getter_fn = lambda: {"value": "should_not_be_returned"}
        result = self.cache.get(test_key, getter_fn)
        self.assertEqual(test_data, result)

    def test_get_non_cached_data(self):
        # Test that the get method calls the getter_fn and saves the result when the data is not in the cache.
        test_key = "test_key"
        test_data = {"value": 42}

        def getter_fn():
            return test_data

        cache_path = self.cache._get_cache_path(test_key)
        self.assertFalse(os.path.exists(cache_path))

        result = self.cache.get(test_key, getter_fn)
        self.assertEqual(test_data, result)

        # Test that the data was saved to the cache.
        self.assertTrue(os.path.exists(cache_path))
        with open(cache_path, "r") as cache_file:
            saved_data = json.load(cache_file)
        self.assertEqual(test_data, saved_data)
