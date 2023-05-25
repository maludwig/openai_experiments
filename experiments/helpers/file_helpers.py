import json
import re
from os import makedirs
from os.path import join, dirname, realpath

import arrow
import nbformat as nbf
from experiments.constants import ASSETS_DIR

# Compile a regular expression to match all characters that aren't safe for filenames
SAFE_CHARACTER_REGEX = re.compile(r"[^a-zA-Z0-9_\-.]")


def load_text_asset(filename: str) -> str:
    """
    Load a text asset from the ASSETS_DIR.
    :param filename: The name of the file to load.
    :return: The contents of the file as a string.
    """
    with open(join(ASSETS_DIR, filename)) as f:
        return f.read()


def get_fs_safe_timestamp() -> str:
    """
    Returns a timestamp that is safe to use on the filesystem.
    :return: A safe timestamp.
    """
    # Format the current UTC time as a filesystem-safe string
    return arrow.utcnow().format("YYYY-MM-DD_HH-mm-ss") + "Z"


def generate_run_dir(parent_dir: str) -> str:
    """
    Generate a run directory under the specified parent directory.
    :param parent_dir: The parent directory for the run directory.
    :return: The path of the created run directory.
    """
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
    # Replace unsafe characters in the filename with underscores
    safe_filename = SAFE_CHARACTER_REGEX.sub("_", filename)
    # Add the expected extension if it is not present
    if not safe_filename.endswith(expected_extension):
        safe_filename += expected_extension
    # Ensure the run directory exists, creating it if necessary
    makedirs(run_dir, exist_ok=True)
    # Return the full safe filepath
    return join(run_dir, safe_filename)


def save_notebook(user_prompt: str, script_name: str, script_text: str, run_dir: str):
    """
    Save the given script as an IPython notebook in the specified run directory.
    :param user_prompt: The user prompt associated with the script.
    :param script_name: The name of the script.
    :param script_text: The text of the script.
    :param run_dir: The directory to save the notebook in.
    """
    # Create a new IPython notebook
    nb = nbf.v4.new_notebook()

    text = f"""\
    # User Prompt:

    {user_prompt}
    """

    script_lines = script_text.split("\n")

    # Find the last import line in the script
    last_import_line = 0
    for idx in range(len(script_lines)):
        line = script_lines[idx]
        if re.match(r"^import ([a-zA-Z0-9_]+)(?: as ([a-zA-Z0-9_]+))?$", line):
            last_import_line = idx
        elif re.match(r"^from ([a-zA-Z0-9_]+) import .*", line):
            last_import_line = idx

    # Split the script into import and code lines
    import_lines = script_lines[: last_import_line + 1]
    code_lines = script_lines[last_import_line + 1 :]

    # Create the notebook's cells
    nb["cells"] = [
        nbf.v4.new_markdown_cell(text),
        nbf.v4.new_code_cell("\n".join(import_lines)),
        nbf.v4.new_code_cell("\n".join(code_lines)),
    ]

    # Set the notebook's metadata
    nb["metadata"]["language_info"] = {
        "codemirror_mode": {"name": "ipython", "version": 2},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython2",
        "version": "2.7.6",
    }

    # Save the notebook
    safe_filepath = get_safe_filepath(script_name, ".ipynb", run_dir)
    with open(safe_filepath, "w") as f:
        nbf.write(nb, f)


def save_python_script(user_prompt: str, script_name: str, script_text: str, run_dir: str):
    """
    Save the given script as a Python script in the specified run directory.
    :param user_prompt: The user prompt associated with the script.
    :param script_name: The name of the script.
    :param script_text: The text of the script.
    :param run_dir: The directory to save the script in.
    """
    # Get a safe filepath for the script
    safe_filepath = get_safe_filepath(script_name, ".py", run_dir)
    with open(safe_filepath, "w") as f:
        # Write the shebang line
        f.write("#!/usr/bin/env python\n")
        # If there is a user prompt, write it as a docstring
        if user_prompt != "":
            clean_user_prompt = user_prompt.replace('"""', "```")
            f.write(f'"""\n{clean_user_prompt}\n"""\n')
        # Write the script text
        f.write(script_text)


def is_jupyter_script(script_text: str) -> bool:
    """
    Determine if the given script is a Jupyter/IPython script.
    :param script_text: The text of the script.
    :return: True if the script is a Jupyter/IPython script, False otherwise.
    """
    if "import matplotlib.pyplot as plt" in script_text:
        return True
    elif "import pandas as pd" in script_text:
        return True
    else:
        return False


def save_json(o, file_path):
    """
    Save the given object as a JSON file.
    :param o: The object to save.
    :param file_path: The path of the file to save the object in.
    """
    real_filepath = realpath(file_path)
    # Ensure the file's directory exists, creating it if necessary
    makedirs(dirname(real_filepath), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(o, f, indent=2)


def load_json(file_path):
    """
    Load a JSON file into a Python object.
    :param file_path: The path of the JSON file to load.
    :return: The deserialized JSON object.
    """
    with open(file_path) as f:
        return json.load(f)
