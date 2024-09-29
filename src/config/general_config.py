import os
from platformdirs import user_data_dir

# Defining app name and author
APP_NAME = "AccessibleArchives"
APP_AUTHOR = "BeyondDimensions"

CHROMA_PATH = os.getenv('CHROMA_PATH', os.path.join(
    user_data_dir(APP_NAME, APP_AUTHOR), 'chroma'))

HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Base data folder
DATA_FOLDER = '.data'

# Subfolders
ORIGINAL_FOLDER = os.path.join(DATA_FOLDER, 'pdfs')
TEMP_FOLDER = os.path.join(DATA_FOLDER, '.temp')
TRANSCRIPTS_FOLDER = os.path.join(DATA_FOLDER, 'transcripts')
PROCESSED_FOLDER = os.path.join(TRANSCRIPTS_FOLDER, 'pdfs')
MARKDOWN_FOLDER = os.path.join(DATA_FOLDER, 'markdown')
