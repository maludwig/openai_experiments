from typing import List

import tiktoken

from experiments.constants import MODEL_NAME
from experiments.helpers.terminal_color_helper import BG_DEFAULT_COLOR, FG_DEFAULT_COLOR, fg

TOKENIZER = tiktoken.encoding_for_model(MODEL_NAME)
PRICES_USD = {
    "gpt-4": 0.03,
}


def count_tokens(text: str) -> int:
    return len(TOKENIZER.encode(text))


def tokenize(text: str) -> List[int]:
    return TOKENIZER.encode(text)


def print_pricing_message(token_count: int):
    print(fg(1, 1, 0) + f"Token count: {token_count}, price at this context: ${(token_count / 1000) * 0.03:0.2f} USD" + BG_DEFAULT_COLOR + FG_DEFAULT_COLOR)
