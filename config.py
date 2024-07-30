# config
import os
from dotenv import load_dotenv

load_dotenv('credentials.env')

API_KEY = os.getenv('API_KEY')

MODELS = {
    'fastchat-t5-3b': 'lmsys/fastchat-t5-3b-v1.0',
    'another-model': 'another/model-name'
}

OCR_MODEL_NAME = 'your-ocr-model-name'
