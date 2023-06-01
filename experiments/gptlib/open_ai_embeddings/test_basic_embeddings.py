#!/usr/bin/env python
"""

uses the OpenAI embedding generator. Here is their example:

```python
response = openai.Embedding.create(
    input="Your text string goes here",
    model="text-embedding-ada-002"
)
embeddings = response['data'][0]['embedding']
```

Output:

```
{
  "data": [
    {
      "embedding": [
        -0.006929283495992422,
        -0.005336422007530928,
        ...
        -4.547132266452536e-05,
        -0.024047505110502243
      ],
      "index": 0,
      "object": "embedding"
    }
  ],
  "model": "text-embedding-ada-002",
  "object": "list",
  "usage": {
    "prompt_tokens": 5,
    "total_tokens": 5
  }
}
```

I want the script to be called basic_embeddings.py and it should have a generate_embedding(text: str) -> List[float]: function that takes an input string, and calls the openai.Embedding.create endpoint with that input string.
"""
import asyncio
import unittest
from unittest.mock import patch
from typing import List

from experiments.gptlib.open_ai_embeddings.basic_embeddings import generate_embedding


# Mock response for the OpenAI API call
mock_response = {
    "data": [{"embedding": [0.1, 0.2, 0.3, 0.4], "index": 0, "object": "embedding"}],
    "model": "text-embedding-ada-002",
    "object": "list",
    "usage": {"prompt_tokens": 5, "total_tokens": 5},
}


# Mock function to replace the actual API call
async def mock_create(*args, **kwargs) -> dict:
    return mock_response


class TestGenerateEmbedding(unittest.TestCase):
    """
    A class that tests the generate_embedding function.
    """

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    @patch("openai.Embedding.acreate", side_effect=mock_create)
    def test_generate_embedding(self, mock_create_function):
        # Call the generate_embedding function with sample text
        text = "Sample input text for testing."
        embedding = self.loop.run_until_complete(generate_embedding(text))

        # Ensure the output is a list of floats
        self.assertIsInstance(embedding, List)
        self.assertEqual(embedding, [0.1, 0.2, 0.3, 0.4])

        # Check if the mocked API function was called with the correct parameters
        mock_create_function.assert_called_once_with(input=text, model="text-embedding-ada-002")


if __name__ == "__main__":
    unittest.main()
