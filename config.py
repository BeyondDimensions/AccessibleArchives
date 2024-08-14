# config
import os
from dotenv import load_dotenv

load_dotenv('credentials.env')

HF_API_KEY = os.getenv('HF_API_KEY')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

DEFAULT_MODEL = ''

MODELS = {
    'llama': {
        'path': 'meta-llama/Llama-2-7b-chat-hf',
        'type': 'causal'
    }
}
