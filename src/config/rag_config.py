import os
from platformdirs import user_data_dir

# Defining app name and author
APP_NAME = "AccessibleArchives"
APP_AUTHOR = "BeyondDimensions"

CHROMA_PATH = os.getenv(
    'CHROMA_PATH',
    os.path.join(user_data_dir(APP_NAME, APP_AUTHOR), 'chroma')
)


RAG_CONFIG = {
    'number_of_contexts': 5,
    'chunk_size': 300,
    'chunk_overlap': 100
}

PROMPT_WRAPPER = """Für das folgende Gespräch, gebe zur aktuellen Frage eine hilfreiche Antwort.

Gespräch: {history}

Aktuelle Frage: {input}
"""
PROMPT_SOURCES_WRAPPER = """
Gespräch: {history}

Aktuelle Frage: {input}

Hier sind evtl. hilfreiche informationen:

{relevant_documents}
"""
DB_QUERY_GEN_PROMPT = """
Gesprächshistorie: {history}

Aktuelle Frage: {input}

Für die aktuelle Frage, formuliere, genau was wir suchen.
"""
