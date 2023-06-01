#!/usr/bin/env python
from typing import List

import tiktoken

from experiments.constants import MODEL_NAME
from experiments.helpers.terminal_color_helper import BG_DEFAULT_COLOR, FG_DEFAULT_COLOR, fg

# Initialize the tokenizer using the specified model name.
TOKENIZER = tiktoken.encoding_for_model(MODEL_NAME)
# Define the per-token prices in USD for each model.
PRICES_USD = {
    "gpt-4": 0.03,
}


def count_tokens(text: str) -> int:
    """
    Count the number of tokens in the given text.
    :param text: The input text to tokenize.
    :return: The number of tokens in the text.
    """
    return len(TOKENIZER.encode(text))


def tokenize(text: str) -> List[int]:
    """
    Encode the given text to a list of integers representing tokens.
    :param text: The input text to tokenize.
    :return: A list of integers representing tokens.
    """
    return TOKENIZER.encode(text)


def print_pricing_message(token_count: int):
    """
    Print the cost of generating text with the given token count.
    :param token_count: The number of tokens for which to calculate the cost.
    """
    # Calculate the cost in USD and print a formatted message.
    print(fg(1, 1, 0) + f"Token count: {token_count}, price at this context: ${(token_count / 1000) * 0.03:0.2f} USD" + BG_DEFAULT_COLOR + FG_DEFAULT_COLOR)
