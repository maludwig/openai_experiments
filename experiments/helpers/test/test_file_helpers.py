import json
import os
import shutil
import tempfile
from random import randint
from unittest import TestCase

from experiments.constants import ASSETS_DIR
from experiments.helpers.file_helpers import (
    get_fs_safe_timestamp,
    get_safe_filepath,
    generate_run_dir,
    load_text_asset,
    is_jupyter_script,
    load_json,
    save_json,
)


class TestFileHelpers(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_generate_run_dir(self):
        parent_dir = self.temp_dir
        run_dir = generate_run_dir(parent_dir)
        self.assertTrue(run_dir.startswith(parent_dir))

    def test_load_text_asset(self):
        expected_content = "This is a test text file."
        random_num = randint(0, 1000000)
        filename = get_fs_safe_timestamp() + f"_{random_num}_test_file.txt"
        file_path = get_safe_filepath(filename, ".txt", ASSETS_DIR)
        with open(file_path, "w") as f:
            f.write(expected_content)
        actual_content = load_text_asset(filename)
        self.assertEqual(actual_content, expected_content)
        os.remove(file_path)

    def test_get_fs_safe_timestamp(self):
        timestamp = get_fs_safe_timestamp()
        self.assertRegex(timestamp, r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}Z$")

    def test_get_safe_filepath(self):
        filename = "test+file:example.txt"
        expected_extension = ".txt"
        run_dir = os.path.join(self.temp_dir, "test")
        expected_filepath = os.path.join(run_dir, "test_file_example.txt")
        actual_filepath = get_safe_filepath(filename, expected_extension, run_dir)
        self.assertEqual(actual_filepath, expected_filepath)

    def test_is_jupyter_script(self):
        jupyter_script = "import matplotlib.pyplot as plt\nimport pandas as pd"
        non_jupyter_script = "import math"
        self.assertTrue(is_jupyter_script(jupyter_script))
        self.assertFalse(is_jupyter_script(non_jupyter_script))

    def test_save_json(self):
        data = {"key": "value"}
        file_path = os.path.join(self.temp_dir, "test.json")
        save_json(data, file_path)

        with open(file_path, "r") as f:
            loaded_data = json.load(f)

        self.assertEqual(data, loaded_data)

    def test_load_json(self):
        data = {"key": "value"}
        file_path = os.path.join(self.temp_dir, "test.json")
        with open(file_path, "w") as f:
            json.dump(data, f)

        loaded_data = load_json(file_path)
        self.assertEqual(data, loaded_data)
