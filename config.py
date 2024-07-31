# config
import os
from dotenv import load_dotenv

load_dotenv('credentials.env')

API_KEY = os.getenv('API_KEY')

DEFAULT_MODEL = ''

MODELS = {
    'fastchat-t5-3b': {'path': 'lmsys/fastchat-t5-3b-v1.0', 'type': 'seq2seq'},
    'gpt-neo': {'path': 'EleutherAI/gpt-neo-2.7B', 'type': 'causal'},
    'bloom': {'path': 'bigscience/bloom-1b1', 'type': 'causal'},
    'llama': {'path': 'meta-llama/Llama-2-7b-chat-hf', 'type': 'seq2seq'}
}

OCR_MODEL_NAME = 'your-ocr-model-name'
