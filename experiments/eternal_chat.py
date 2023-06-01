#!/usr/bin/env python

import argparse
from argparse import Namespace

import openai

from experiments.config import OPEN_AI_KEY
from experiments.helpers.io_helpers import multiline_input
from experiments.helpers.openai_api_helpers import count_messages_tokens
from experiments.helpers.file_helpers import (
    save_json,
    load_json,
    get_fs_safe_timestamp,
    generate_run_dir,
)
from experiments.constants import (
    CHATS_DIR,
)
from experiments.helpers.openai_completion_helpers import get_completion, get_valid_temperature

from experiments.helpers.terminal_color_helper import fg, BG_DEFAULT_COLOR, FG_DEFAULT_COLOR
from experiments.helpers.token_helpers import print_pricing_message

openai.api_key = OPEN_AI_KEY


def parse_args() -> Namespace:
    """
    Parse command line arguments.
    :return: The parsed arguments, as a Namespace object.
    """
    parser = argparse.ArgumentParser(description="Have an unlimited chat with ChatGPT")

    # Add the '--fresh' option as a boolean flag, which will be True when the option is specified, and False otherwise.
    parser.add_argument("--fresh", action="store_true", help="Indicates if the system should start from scratch.")
    parser.add_argument("--temperature", type=float, default=1.0, help="The temperature to use for the chat completion.")
    # Add the '--save-file-path' option, which requires a file path as its argument.
    # The 'default' value will be used if this option is not specified on the command line.
    defaultdir = generate_run_dir(CHATS_DIR)
    parser.add_argument(
        "--save-dir-path",
        type=str,
        default=defaultdir,
        help=f'Path to the save directory. Defaults to "{defaultdir}"',
    )

    return parser.parse_args()


SYSTEM_MESSAGE = """
SYSTEM MESSAGE, YOU ARE AN OPENAI LLM CHATBOT, AND HAVE A MAXIMUM TOKEN CONTEXT OF 8000 TOKENS.
THE END USER THAT YOU HAVE BEEN CHATTING WITH WANTS TO CONTINUE THE CONVERSATION, AND DOES NOT WANT TO LOSE THE
CONTEXT OF THE CONVERSATION.
PLEASE SUMMARIZE FOR YOURSELF THE CHAT SO FAR, AND INCLUDE INFORMATION THAT YOU BELIEVE THE END USER
WOULD FIND IMPORTANT.
THE RESPONSE YOU GENERATE WILL BE PASSED INTO THE NEXT ITERATION.
PREVIOUS MESSAGES WILL BE OMITTED.
GIVE YOURSELF AS MUCH RELEVANT CONTEXT AS POSSIBLE.
YOUR RESPONSE SHOULD BE LONG, AT LEAST 1000 WORDS.
INCLUDE ANY MATHEMATICAL CALCULATIONS IN DETAIL, BUT ONLY IF THEY ARE CORRECT.
THE END USER WILL NOT SEE THIS MESSAGE OR YOUR RESPONSE.
""".replace(
    "\n", " "
)


def main():
    args = parse_args()
    temperature = get_valid_temperature(args.temperature)
    try:
        all_messages = load_json(args.save_dir_path + "/messages.json")
    except FileNotFoundError:
        all_messages = []
    messages = all_messages
    for message in messages:
        if message["role"] == "user":
            print(fg(0, 1, 0) + message["content"] + BG_DEFAULT_COLOR + FG_DEFAULT_COLOR)
        elif message["role"] == "system":
            print(fg(0.5, 0.5, 0.9) + "SYSTEM: " + message["content"] + BG_DEFAULT_COLOR + FG_DEFAULT_COLOR)
        else:
            print(fg(0, 1, 1) + message["content"] + BG_DEFAULT_COLOR + FG_DEFAULT_COLOR)
    for idx, message in enumerate(all_messages):
        if message["role"] == "user" and message["content"] == SYSTEM_MESSAGE:
            messages = all_messages[max(idx - 4, 0) :]
    user_prompt = multiline_input()
    while user_prompt != "exit":
        token_count = count_messages_tokens(messages)
        print_pricing_message(token_count)
        if token_count > 6500:
            print("\n\n\n   ======== TRUNCATING CHAT =========  \n\n\n")
            full_text, messages = get_completion(SYSTEM_MESSAGE, messages, temperature=temperature)
            all_messages.append(messages[-2])
            all_messages.append(messages[-1])
            messages = messages[-6:]
        full_text, messages = get_completion(user_prompt, messages, temperature=temperature)
        all_messages.append(messages[-2])
        all_messages.append(messages[-1])
        json_filename = args.save_dir_path + f"/messages_{get_fs_safe_timestamp()}.json"
        save_json(all_messages, json_filename)
        save_json(all_messages, args.save_dir_path + "/messages.json")
        user_prompt = multiline_input()


if __name__ == "__main__":
    main()
