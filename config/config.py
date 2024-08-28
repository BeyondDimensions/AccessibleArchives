# config
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='config/credentials.env')

HF_API_KEY = os.getenv('HF_API_KEY')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

DEFAULT_MODEL = ''

MODELS = {
    'llama': {
        'path': 'meta-llama/Llama-2-7b-chat-hf',
        'type': 'causal'
    }
}

# Base data folder
DATA_FOLDER = 'data'

# Subfolders
ORIGINAL_FOLDER = os.path.join(DATA_FOLDER, 'pdfs')
TEMP_FOLDER = os.path.join(DATA_FOLDER, 'temp')
TRANSCRIPTS_FOLDER = os.path.join(DATA_FOLDER, 'transcripts')
PROCESSED_FOLDER = os.path.join(TRANSCRIPTS_FOLDER, 'pdfs')

ALLOWED_VERSIONS = ['gpt-4o-2024-08-06', 'chatgpt-4o-latest',
                    'gpt-4o-mini', 'gpt-4o']
