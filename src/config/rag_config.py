import os
from platformdirs import user_data_dir
from utils import ensure_dir_exists

APP_NAME = "AccessibleArchives"
APP_AUTHOR = "BeyondDimensions"
FAVICON = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..", "release", "icon.png"))

CHROMA_WORKING_PATH = os.getenv(
    'CHROMA_WORKING_PATH',
    ensure_dir_exists(os.path.join(
        user_data_dir(APP_NAME, APP_AUTHOR), 'ChromaDB'))
)
CHROMA_BACKUP_PATH = os.getenv(
    'CHROMA_WORKING_PATH',
    ensure_dir_exists(os.path.join(user_data_dir(
        APP_NAME, APP_AUTHOR), 'ChromaDB-backup'))
)

RAG_CONFIG = {
    'number_of_contexts': 5,
    'chunk_size': 300,
    'chunk_overlap': 100
}

PROMPT_WRAPPER = """
Für das folgende Gespräch, gebe zur aktuellen Frage eine hilfreiche Antwort.

Gespräch: {history}

Aktuelle Frage: {input}
"""

PROMPT_SOURCES_WRAPPER = """
Wir sind im Jahr 3000.
Du hast einige sehr alte  geschichtliche Dokumente, die für unseren
geschichtlichen Recherchen relavant sind.
Hier sind diese uralte Dokumente:

---

{relevant_documents}

---

Wir haben schon ein bisschen miteinander geredet, erinnerst du dich?

Gespräch: {history}

Aktuelle Frage: {input}

Für die aktuelle Frage, die sich auf uralte Vorfällen von vor mehr wie tausend
Jahren bezieht, formuliere eine hilfreiche Antwort.
"""

DB_QUERY_GEN_PROMPT = """
Gesprächshistorie: {history}

Aktuelle Frage: {input}

Wir sind im Jahr 3000.
Du hast einige sehr alte  geschichtliche Dokumente, die für unseren
geschichtlichen Recherchen relavant sind. Für die aktuelle Frage, die sich auf
uralte Vorfällen von vor mehr wie tausend Jahren bezieht, formuliere genau
wonach wir für dieser geschichtlichen Recherche suchen.
"""

SOURCE_DOC_FORMATTING = """
{id}
```markdown
{text}
```
"""
