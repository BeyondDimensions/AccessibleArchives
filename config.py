# config
import os
from dotenv import load_dotenv

load_dotenv('credentials.env')

API_KEY = os.getenv('API_KEY')

DEFAULT_MODEL = ''

MODELS = {
    'llama': {
        'path': 'meta-llama/Llama-2-7b-chat-hf',
        'type': 'causal'
    }
}

OCR_MODEL_NAME = 'your-ocr-model-name'
