import os

HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

DEFAULT_MODEL = ''

MODELS = {
    'llama': {
        'path': 'meta-llama/Llama-2-7b-chat-hf',
        'type': 'causal'
    }
}

LLM_MODELS = {
    "Ollama Llama3": "llama3.1:8b",
    "Ollama Mistral": "mistral:7b",
    "Ollama Qwen": "qwen2:7b",
}

EMBEDDING_MODELS = {
    "Ollama Mxbai Embed Large": "mxbai-embed-large",
    "Ollama Nomic Embed Text": "nomic-embed-text",
    "Ollama All MiniLM": "all-minilm"
}

# Base data folder
DATA_FOLDER = 'data'

# Subfolders
ORIGINAL_FOLDER = os.path.join(DATA_FOLDER, 'pdfs')
TEMP_FOLDER = os.path.join(DATA_FOLDER, '.temp')
TRANSCRIPTS_FOLDER = os.path.join(DATA_FOLDER, 'transcripts')
PROCESSED_FOLDER = os.path.join(TRANSCRIPTS_FOLDER, 'pdfs')
MARKDOWN_FOLDER = os.path.join(TRANSCRIPTS_FOLDER, 'markdown')

ALLOWED_VERSIONS = ['gpt-4o-2024-08-06', 'chatgpt-4o-latest', 'gpt-4o-mini']
