from experiments.constants import MODEL_NAME
from experiments.helpers.openai_api_helpers import backoff_completion, merge_completion_stream


def get_completion(prompt, initial_messages=None, temperature=1.0):
    if initial_messages is None:
        initial_messages = []
    messages = initial_messages + [{"role": "user", "content": prompt}]
    completion = backoff_completion(model=MODEL_NAME, messages=messages, stream=True, temperature=temperature)
    full_completion, full_text = merge_completion_stream(completion)

    messages.append({"role": "assistant", "content": full_text})
    return full_text, messages


def get_valid_temperature(temp) -> float:
    if isinstance(temp, float):
        if temp < 0.0 or temp > 2.0:
            raise ValueError("Temperature must be a float between 0.0 and 2.0")
        return temp
    else:
        raise ValueError("Temperature must be a float between 0.0 and 2.0")
