#!/usr/bin/env python
"""
Auto-comment-and-document
"""
# test_openai_api_helpers.py

import unittest
from unittest.mock import patch

from experiments.helpers.openai_api_helpers import count_messages_tokens, merge_completion_stream, backoff_completion


class TestOpenaiApiHelpers(unittest.TestCase):
    def test_count_messages_tokens(self):
        messages = [{"content": "Hello, how are you?"}, {"content": "I'm fine, thank you!"}]
        expected_token_count = 13
        actual_token_count = count_messages_tokens(messages)
        self.assertEqual(expected_token_count, actual_token_count)

    def test_count_messages_tokens_empty(self):
        messages = []
        expected_token_count = 0
        actual_token_count = count_messages_tokens(messages)
        self.assertEqual(expected_token_count, actual_token_count)

    def test_merge_completion_stream(self):
        completion = [
            {"choices": [{"delta": {"content": "Hello"}}]},
            {"choices": [{"delta": {"content": ", How"}}]},
            {"choices": [{"delta": {"content": " are"}}]},
            {"choices": [{"delta": {"content": " you?"}}]},
        ]

        expected_merged_completion = [{"choices": [{"delta": {"content": "Hello, How are you?"}}]}]

        expected_full_text = "Hello, How are you?"
        actual_merged_completion, actual_full_text = merge_completion_stream(completion)
        self.assertEqual(expected_merged_completion, actual_merged_completion)
        self.assertEqual(expected_full_text, actual_full_text)

    def test_merge_completion_stream_empty(self):
        completion = []
        expected_merged_completion = []
        expected_full_text = ""
        actual_merged_completion, actual_full_text = merge_completion_stream(completion)
        self.assertEqual(expected_merged_completion, actual_merged_completion)
        self.assertEqual(expected_full_text, actual_full_text)

    @patch("openai.ChatCompletion.create")
    def test_backoff_completion(self, mocked_completion_create):
        completion_response = "Completion response"
        mocked_completion_create.return_value = completion_response

        actual_response = backoff_completion()

        self.assertEqual(completion_response, actual_response)
        mocked_completion_create.assert_called_once()


if __name__ == "__main__":
    unittest.main()
