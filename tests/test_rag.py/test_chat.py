from _load_src import SRC_PATH
from storage import DocumentCollection
import os
from rag import DocsEmbedding
from config.languages import get_language_config


from rag.query_engine import generate_response
from rag.query_engine import format_history

# path to the DocumentCollection to use for this test
DOCUMENTS_PATH = os.path.abspath(os.path.join(
    SRC_PATH, "..", ".data", "Demo"
))

# select a language
chat_config = get_language_config("de-de").chat_config

# load DocumentCollection
docs_clxn = DocumentCollection(DOCUMENTS_PATH)

# load embeddings for this DocumentCollection
docs_embedding = DocsEmbedding(
    "Demo",
    docs_clxn.transcripts_dir
)

print(format_history(chat_config.INITIAL_CHAT_HISTORY, chat_config))
# generate_response("WasK
response, sources = generate_response(
    "ChatGPT",
    "Was wissen wir über die Zusammenarbeit zwischen Johannes Weinrich und Beatrix Odenal?",
    chat_config.INITIAL_CHAT_HISTORY,
    docs_clxn,
    docs_embedding,
    chat_config
)
print(response)
for source in sources:
    print(source)

chat_config = get_language_config("en-gb").chat_config

    
response, sources = generate_response(
    "ChatGPT",
    "What do we know about the collaboration between Johannes Weinrich and Beatrix Odenal?",
    chat_config.INITIAL_CHAT_HISTORY,
    docs_clxn,
    docs_embedding,
    chat_config
)
