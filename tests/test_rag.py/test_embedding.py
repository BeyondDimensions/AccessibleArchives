from _load_src import SRC_PATH
from storage import DocumentCollection
import os
from rag import DocsEmbedding


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

# query the embeddings using keywords
print(docs_embedding.query_database("Johannes Weinrich Beatrix Odenal"))
