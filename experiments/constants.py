from os import makedirs
from os.path import dirname, join, realpath

CURRENT_DIR = realpath(dirname(__file__))
REPO_ROOT = dirname(CURRENT_DIR)
ASSETS_DIR = join(REPO_ROOT, "assets")

DATA_DIR = join(REPO_ROOT, "data")

CHATS_DIR = join(DATA_DIR, "chats")
makedirs(CHATS_DIR, exist_ok=True)


SCRIPT_WRITER_DIR = join(DATA_DIR, "script_writer")
makedirs(SCRIPT_WRITER_DIR, exist_ok=True)

# See: https://platform.openai.com/docs/models/model-endpoint-compatibility
MODEL_NAME = "gpt-4"  # Basic 8k token context
# MODEL_NAME = "gpt-4-32k" # Larger 32k token context
