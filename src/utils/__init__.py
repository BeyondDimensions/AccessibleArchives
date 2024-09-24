# src/utils/__init__.py
from .config import OPENAI_API_KEY, DEFAULT_OPENAI_MODEL, ALLOWED_OPENAI_MODELS
from .config import ORIGINAL_FOLDER, CHROMA_PATH, DATA_FOLDER, PROCESSED_FOLDER
from .logger import success, info, important, warning, error
from .error_handling import openai_api_error
from .utils import encode_file_base64, ensure_directories_exist
