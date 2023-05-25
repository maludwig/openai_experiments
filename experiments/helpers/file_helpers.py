import json
import re
from os import makedirs
from os.path import join, dirname, realpath

import arrow
import nbformat as nbf

from experiments.constants import ASSETS_DIR

SAFE_CHARACTER_REGEX = re.compile(r"[^a-zA-Z0-9_\-.]")


def load_text_asset(filename: str) -> str:
    with open(join(ASSETS_DIR, filename)) as f:
        return f.read()


def get_fs_safe_timestamp() -> str:
    """
    Returns a timestamp that is safe to use on the filesystem.
    :return: A safe timestamp.
    """
    return arrow.utcnow().format("YYYY-MM-DD_HH-mm-ss") + "Z"


def generate_run_dir(parent_dir: str) -> str:
    run_timestamp = get_fs_safe_timestamp()
    run_dir = join(parent_dir, run_timestamp)
    return run_dir


def get_safe_filepath(filename: str, expected_extension: str, run_dir: str) -> str:
    """
    Returns a file path that is safe to use on the filesystem.
    :param filename: The filename to make safe.
    :param expected_extension: The expected extension of the file.
    :param run_dir: The directory to save the file in.
    :return: A safe file path.
    """
    safe_filename = SAFE_CHARACTER_REGEX.sub("_", filename)
    if not safe_filename.endswith(expected_extension):
        safe_filename += expected_extension
    makedirs(run_dir, exist_ok=True)
    return join(run_dir, safe_filename)


def save_notebook(user_prompt: str, script_name: str, script_text: str, run_dir: str):
    nb = nbf.v4.new_notebook()
    text = f"""\
    # User Prompt:

    {user_prompt}
    """

    script_lines = script_text.split("\n")

    last_import_line = 0
    for idx in range(len(script_lines)):
        line = script_lines[idx]
        if re.match(r"^import ([a-zA-Z0-9_]+)(?: as ([a-zA-Z0-9_]+))?$", line):
            last_import_line = idx
        elif re.match(r"^from ([a-zA-Z0-9_]+) import .*", line):
            last_import_line = idx

    import_lines = script_lines[: last_import_line + 1]
    code_lines = script_lines[last_import_line + 1 :]

    nb["cells"] = [
        nbf.v4.new_markdown_cell(text),
        nbf.v4.new_code_cell("\n".join(import_lines)),
        nbf.v4.new_code_cell("\n".join(code_lines)),
    ]
    nb["metadata"]["language_info"] = {
        "codemirror_mode": {"name": "ipython", "version": 2},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython2",
        "version": "2.7.6",
    }
    safe_filepath = get_safe_filepath(script_name, ".ipynb", run_dir)
    with open(safe_filepath, "w") as f:
        nbf.write(nb, f)


def save_python_script(user_prompt: str, script_name: str, script_text: str, run_dir: str):
    safe_filepath = get_safe_filepath(script_name, ".py", run_dir)
    with open(safe_filepath, "w") as f:
        f.write("#!/usr/bin/env python\n")
        if user_prompt != "":
            clean_user_prompt = user_prompt.replace('"""', "```")
            f.write(f'"""\n{clean_user_prompt}\n"""\n')
        f.write(script_text)


def is_jupyter_script(script_text: str) -> bool:
    if "import matplotlib.pyplot as plt" in script_text:
        return True
    elif "import pandas as pd" in script_text:
        return True
    else:
        return False


def save_json(o, file_path):
    real_filepath = realpath(file_path)
    makedirs(dirname(real_filepath), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(o, f, indent=2)


def load_json(file_path):
    with open(file_path) as f:
        return json.load(f)
