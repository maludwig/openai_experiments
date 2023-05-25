#!/usr/bin/env python
import argparse
from os.path import basename, dirname, join
from typing import Tuple

import re

import openai

from experiments.config import OPEN_AI_KEY
from experiments.constants import MODEL_NAME, SCRIPT_WRITER_DIR

ALL_COMPLETIONS_PATH = join(SCRIPT_WRITER_DIR, "all_completions.json")
from experiments.gptlib.dictdict.dictdict import DictDict
from experiments.gptlib.whitespace_trimmer.remove_whitespace import remove_leading_whitespace
from experiments.helpers.file_helpers import load_text_asset, generate_run_dir, is_jupyter_script, save_notebook, save_python_script
from experiments.helpers.io_helpers import multiline_input
from experiments.helpers.openai_api_helpers import backoff_completion, merge_completion_stream
from experiments.helpers.terminal_color_helper import fg, BG_DEFAULT_COLOR, FG_DEFAULT_COLOR

openai.api_key = OPEN_AI_KEY

FIBONACCI_EXAMPLE_SCRIPT = load_text_asset("fibonacci.py")
FIBONACCI_EXAMPLE_TEST_SCRIPT = load_text_asset("test_fibonacci.py")


def find_functions(full_text: str):
    function_names = []
    function_regex = re.compile(r"def ([a-zA-Z0-9_]+)\(")
    for match in function_regex.finditer(full_text):
        function_names.append(match.group(1))
    return function_names


def extract_python_scripts(completion_text: str):
    scripts = {}
    completion_lines = completion_text.split("\n")
    is_python_script = False
    script_name = "script_1"
    script_lines = []
    for idx in range(len(completion_lines)):
        line = completion_lines[idx]
        if not is_python_script:
            match = re.match(r"^#+ (.*)(\.py|\.ipynb)$", line)
            if match:
                script_name = match.group(1)
            elif line in ["```python", "```"]:
                is_python_script = True
        else:
            if line == "```":
                is_python_script = False
                script_name = script_name.replace(".py", "")
                script_name = script_name.replace(".ipynb", "")
                if script_name in scripts:
                    script_suffix = 2
                    while f"script_name_{script_suffix}" in scripts:
                        script_suffix += 1
                    script_name = f"script_name_{script_suffix}"
                scripts[script_name] = "\n".join(script_lines)
                script_lines = []
                script_name = f"script_{len(scripts) + 1}"
            else:
                script_lines.append(line)
    return scripts


def save_scripts(full_text, user_prompt, run_dir: str):
    scripts = extract_python_scripts(full_text)
    function_names_by_script = {}
    for script_name, script_text in scripts.items():
        if is_jupyter_script(script_text):
            save_notebook(user_prompt, script_name, script_text, run_dir)
        else:
            save_python_script(user_prompt, script_name, script_text, run_dir)
        new_function_names = find_functions(script_text)
        if len(new_function_names) > 0:
            function_names_by_script[script_name] = new_function_names
    return scripts, function_names_by_script


def get_user_prompt() -> Tuple[str, str]:
    user_prompt = multiline_input("I want you to implement a python script that...\n> ")
    full_prompt = f"""I want you to implement a python script that {user_prompt}
    Can you respond with the full script, and if you want to explain things, explain 
    with comments in the code? I already have numpy, matplotlib, tensorflow, keras, and jupyter installed and running. 
    Please format your response in markdown, and right before the script, with a header of a script filename.
    Also, for each function definition, please add a docstring description in reStructuredText format.
    Please include parameter and return types in the function definitions.
    Please include a docstring for classes.
    Before writing the script, describe your plan for the script, and what you are trying to accomplish.
    Be sure to describe your plan for the main() function, which should provide an example of how to use the script.
    For example, if you were writing a script to calculate the first 100 fibonacci numbers,
    you would write something like this:

    # fibonacci.py

    ### Plan

    In this script, we will calculate the first 100 fibonacci numbers, however, if we have already calculated
    a fibonacci number, we will not recalculate it, we will just use the previously calculated value.
    This is important, to ensure that we do not waste time recalculating the same fibonacci numbers over and over.

    ```python\n{FIBONACCI_EXAMPLE_SCRIPT}```
    """

    return user_prompt, remove_leading_whitespace(full_prompt)


known_completions = DictDict()


def load_previous_completions():
    global known_completions
    try:
        known_completions = DictDict.load(ALL_COMPLETIONS_PATH)
    except FileNotFoundError:
        print("No previous completions found")


load_previous_completions()


def add_completion_to_previous_completions(prompt, initial_messages, completion):
    key = {"prompt": prompt, "initial_messages": initial_messages}
    known_completions[key] = {"prompt": prompt, "initial_messages": initial_messages, "completion": completion}
    known_completions.save(ALL_COMPLETIONS_PATH)


def get_completion(prompt, initial_messages=None):
    print(fg(0, 1, 0) + "Prompt:\n    " + prompt + BG_DEFAULT_COLOR + FG_DEFAULT_COLOR)
    if initial_messages is None:
        initial_messages = []
    messages = initial_messages + [{"role": "user", "content": prompt}]
    key = {"prompt": prompt, "initial_messages": initial_messages}
    if key in known_completions:
        completion = known_completions[key]["completion"]
    else:
        completion = backoff_completion(
            model=MODEL_NAME,
            messages=messages,
            stream=True,
        )
    full_completion, full_text = merge_completion_stream(completion)

    if key not in known_completions:
        add_completion_to_previous_completions(prompt, initial_messages, full_completion)

    messages.append({"role": "assistant", "content": full_text})
    return full_text, messages


def load_prewritten_script(script_path):
    with open(script_path) as f:
        content = f.read()
    return content


def prompt_to_improve_script(args):
    script_content = load_prewritten_script(args.script)
    basic_script_content = load_text_asset("fibonacci_basic.py")
    improved_script_content = load_text_asset("fibonacci.py")
    prompt = "Can you please read over this script, and then write a description for it?"
    user_prompt = "Auto-comment-and-document"
    if args.comment_lines:
        prompt += " And could you please add a comment for each non-trivial line of code."
    if args.add_docstrings:
        prompt += """
        Also, for each function, please add a docstring description in reStructuredText format.
        Please include parameter and return types in the function definitions.
        Please include a docstring for classes as well.

        For example, if I gave you this basic script as input:

        # fibonacci.py
        """
        prompt += f"\n```python\n{basic_script_content}\n```\n"
        prompt += """
        I would expect this output:

        # fibonacci.py
        """
        prompt += f"\n```python\n{improved_script_content}\n```\n"
        prompt += """
        Ok, that's the example, now, here is the real script, please improve it as described above:
        """
    prompt += f"""# {basename(args.script)}"""
    full_prompt = prompt + f"\n```python\n{script_content}\n```\n"

    full_text, messages = get_completion(remove_leading_whitespace(full_prompt))
    return user_prompt, full_prompt, full_text, messages


def main():
    parser = argparse.ArgumentParser(description="Generate embeddings for a text file.")
    parser.add_argument("--script", help="Path to the script file to generate a test for.")
    parser.add_argument("--comment-lines", action="store_true", help="Write a comment for every line of code.")
    parser.add_argument("--add-docstrings", action="store_true", help="Write a docstring for every class and function.")

    args = parser.parse_args()
    if args.script:
        run_dir = generate_run_dir(dirname(args.script))
        user_prompt, full_prompt, full_text, messages = prompt_to_improve_script(args)
    else:
        run_dir = generate_run_dir(SCRIPT_WRITER_DIR)
        user_prompt, full_prompt = get_user_prompt()

        full_text, messages = get_completion(full_prompt)

    print("=" * 60)
    scripts, function_names_by_script = save_scripts(full_text, user_prompt, run_dir)

    if len(function_names_by_script) > 0:
        test_file_name_list = list([f"test_{script_name}" for script_name in function_names_by_script.keys()])
        if len(test_file_name_list) == 1:
            test_file_names_prompt = f"Please make 1 test file and call it " + test_file_name_list[0]
        else:
            test_file_names_prompt = (
                f"Please make {len(function_names_by_script)} test files and call them "
                + ", ".join(test_file_name_list[:-1])
                + ", and "
                + test_file_name_list[-1]
            )
        prompt = f"""
        Can you please write unit tests for each of the functions above?
        Please use the unittest module, and write the tests in a new script.
        The first argument to an assertion should be the expected value, and the second argument should be the actual value.
        For example: `self.assertEqual(2, addNumbers(1,1))`
        Try to cover as many edge cases as you can think of.
        {test_file_names_prompt}
        """
        if args.script:
            prompt += f"""
            As an example, for this script:

            # fibonacci.py

            ```python\n{FIBONACCI_EXAMPLE_SCRIPT}\n```
            Your output could look like this:
            """

        else:
            prompt += f"""
            As an example, for the script earlier, fibonacci.py, your output could look like this:
            """
        prompt += f"""
            # test_fibonacci.py
            
            ### Plan
            
            #### fibonacci
            
            ##### Edge Cases
            
            - fibonacci(0) should return [1]
            - fibonacci(1) should return [1, 1]
            
            ##### General Cases
            
            - We will test the FibonacciMemoizer.fibonacci function by testing the first few numbers in the sequence.
                
            ```python\n{FIBONACCI_EXAMPLE_TEST_SCRIPT}\n```
        """
        next_full_text, next_messages = get_completion(prompt, messages)

        scripts, function_names_by_script = save_scripts(next_full_text, user_prompt, run_dir)


if __name__ == "__main__":
    main()
