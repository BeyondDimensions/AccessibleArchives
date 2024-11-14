from _load_src import SRC_PATH
from storage import DocumentCollection
import os
from rag import DocsEmbedding
from config.rag_config import INITIAL_CHAT_HISTORY


from rag.query_engine import generate_response
from rag.query_engine import format_history

# path to the DocumentCollection to use for this test
DOCUMENTS_PATH = os.path.abspath(os.path.join(
    SRC_PATH, "..", ".data", "Demo"
))

# load DocumentCollection
docs_clxn = DocumentCollection(DOCUMENTS_PATH)

# load embeddings for this DocumentCollection
docs_embedding = DocsEmbedding(
    "Demo",
    docs_clxn.transcripts_dir
)

print(format_history(INITIAL_CHAT_HISTORY))
# generate_response("WasK
response, sources = generate_response(
    "ChatGPT",
    "Was wissen wir über die Zusammenarbeit zwischen Johannes Weinrich und Beatrix Odenal?",
    INITIAL_CHAT_HISTORY,
    docs_clxn,
    docs_embedding,
)
print(response)
for source in sources:
    print(source)
