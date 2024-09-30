import os
from platformdirs import user_data_dir

# Defining app name and author
APP_NAME = "AccessibleArchives"
APP_AUTHOR = "BeyondDimensions"

CHROMA_PATH = os.getenv('CHROMA_PATH', os.path.join(
    user_data_dir(APP_NAME, APP_AUTHOR), 'chroma'))


RAG_CONFIG = {
    'number_of_contexts': 5,
    'chunk_size': 300,
    'chunk_overlap': 100
}
