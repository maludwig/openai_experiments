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
import concurrent
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict

import openai


import logging
import asyncio
from aiohttp import ClientSession

from experiments.config import OPEN_AI_KEY

openai.api_key = OPEN_AI_KEY


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] (%(threadName)-10s) %(message)s",
)
sleep_seconds = 0.5


class EmbeddingsGenerator:
    """
    A class that generates word embeddings concurrently using multiple threads.
    """

    def __init__(self, num_workers: int = 10):
        """
        Initialize the EmbeddingsGenerator.
        :param num_workers: The number of worker threads to use.
        """
        self.num_workers = num_workers

    async def multi_generate_embeddings(self, words: List[str]) -> Dict[str, List[float]]:
        """
        Generate word embeddings for the list of words using the slow function in multiple threads.
        :param words: A list of words to generate embeddings for.
        :return: A dictionary where the key is the input word, and the value is the generated embedding.
        """

        # Semaphore to limit number of concurrent requests
        semaphore = asyncio.Semaphore(10)

        # Submit each word as a separate task, store a list of Future objects.
        openai.aiosession.set(ClientSession())

        # This is your worker function
        async def worker(word):
            global sleep_seconds
            async with semaphore:
                try:
                    embedding = await generate_embedding(word)
                    return word, embedding
                except Exception as e:  # Handle exceptions here
                    print(f"Failed to generate embedding for {word}: {e}")
                    sleep_seconds += 0.1
                    await asyncio.sleep(sleep_seconds)
                    return word, None

        # Start the tasks and collect the results
        results = await asyncio.gather(*(worker(word) for word in words))

        # Gather results from completed tasks, and build a dictionary of word -> embedding
        word_embeddings = {}
        for word, embedding in results:
            if embedding is not None:
                word_embeddings[word] = embedding
        await openai.aiosession.get().close()
        return word_embeddings


async def generate_embedding(text: str, model="text-embedding-ada-002") -> List[float]:
    """
    Generates an embedding for the given text using the OpenAI API.

    :param text: The input text for which to generate the embedding.
    :param model: The OpenAI model name
    :return: The generated embedding as a list of floats.
    """
    logging.debug(f"Creating embedding for: '{text}'...")

    response = await openai.Embedding.acreate(input=text, model=model)
    logging.debug(f"Done embedding for: '{text}'")
    embeddings = response["data"][0]["embedding"]
    return embeddings


async def main():
    """
    The main function for the basic_embeddings script.
    This is called when the script is run directly.
    """
    # Provide a sample input text
    text = "This is a sample text for generating an embedding."

    # Generate the embedding for the provided text
    embedding = await generate_embedding(text)

    # Print the generated embedding
    print(embedding)

    # Initialize the EmbeddingsGenerator with 10 worker threads
    generator = EmbeddingsGenerator()

    # Define a list of words for which to generate embeddings
    words = ["apple", "banana", "orange", "grape", "watermelon"]

    # Generate the embeddings using the defined list of words
    word_embeddings = await generator.multi_generate_embeddings(words)

    # Print the generated embeddings
    for word, embedding in word_embeddings.items():
        print(f"{word}: {embedding}")


if __name__ == "__main__":
    asyncio.run(main())
