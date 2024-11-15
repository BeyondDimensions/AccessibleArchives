import platform
import os
from platformdirs import user_data_dir
from utils import ensure_dir_exists

APP_NAME = "AccessibleArchives"
APP_AUTHOR = "BeyondDimensions"
FAVICON = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "release", "icon.png"))

platform.system()
if platform.system().lower() == "linux":
    DOC_EMBEDDINGS_PATH = os.getenv(
        'DOC_EMBEDDINGS_PATH',
        ensure_dir_exists("/opt/AccessibleArchives/DocumentEmbeddings")
    )

else:
    DOC_EMBEDDINGS_PATH = os.getenv(
        'DOC_EMBEDDINGS_PATH',
        ensure_dir_exists(os.path.join(
            user_data_dir(APP_NAME, APP_AUTHOR), 'DocumentEmbeddings'))
    )


RAG_CONFIG = {
    'number_of_contexts': 5,
    'chunk_size': 300,
    'chunk_overlap': 100
}
