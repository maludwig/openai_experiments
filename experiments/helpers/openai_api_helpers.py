#!/usr/bin/env python
from time import sleep

import openai

from experiments.helpers.token_helpers import count_tokens

from experiments.constants import (
    MODEL_NAME,
)
from experiments.config import OPEN_AI_KEY

from experiments.helpers.terminal_color_helper import fg, BG_DEFAULT_COLOR, FG_DEFAULT_COLOR

openai.api_key = OPEN_AI_KEY


def backoff_completion(model=MODEL_NAME, messages=None, stream=True, retry_count=5, temperature=1):
    """
    Send a completion request to the OpenAI API with exponential backoff for rate limit errors.

    :param model: The name of the model to use for the completion.
    :param messages: A list of messages to process (optional).
    :param stream: A boolean, set to True if streaming the responses (default: True).
    :param retry_count: The number of retries to attempt upon rate limit errors (default: 5).
    :param temperature: The sampling temperature used by the model (default: 1).
    :return: The completion object returned by the API.
    """
    if messages is None:
        messages = []
    try:
        print(fg(1, 0, 1) + "Sending completion request..." + BG_DEFAULT_COLOR + FG_DEFAULT_COLOR)
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=stream,
            temperature=temperature,
        )
        return completion
    except openai.error.RateLimitError:
        if retry_count == 0:
            raise Exception("Rate limit error, giving up.")
        else:
            sleep(5 - retry_count)
            print("Rate limit error, retrying...")
            return backoff_completion(model=model, messages=messages, stream=stream, retry_count=retry_count - 1, temperature=temperature)


def count_messages_tokens(messages):
    """
    Count the number of tokens in a list of messages.

    :param messages: A list of messages.
    :return: The total number of tokens in the messages.
    """
    token_count = 0
    for message in messages:
        token_count += count_tokens(message["content"])
    return token_count


def merge_completion_stream(completion):
    """
    Merge a stream of completion chunks into a list of full completions and a concatenated text.

    :param completion: An iterable stream of completion chunks.
    :return: A tuple containing a list of full completions and the concatenated text from the chunks.
    """
    full_completion = []
    full_text_chunks = []
    for chunk in completion:
        delta = chunk["choices"][0]["delta"]
        if "content" in delta:
            text_content = delta["content"]
            full_text_chunks.append(text_content)
            msg = fg(0, 1, 1) + text_content + BG_DEFAULT_COLOR + FG_DEFAULT_COLOR
            print(msg, end="")
            if len(full_completion) > 0:
                last_chunk = full_completion[-1]
                last_delta = last_chunk["choices"][0]["delta"]
                if "content" in last_delta:
                    last_delta["content"] += text_content
                    chunk = None
        if chunk is not None:
            full_completion.append(chunk)
    full_text = "".join(full_text_chunks)

    return full_completion, full_text
