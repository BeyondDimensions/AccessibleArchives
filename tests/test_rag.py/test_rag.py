from _load_src import SRC_PATH
from storage import DocumentCollection
import os
from rag import initialize_database

from rag.query_engine import generate_response
TEST_COLLECTION_PATH = os.path.abspath(os.path.join(
    SRC_PATH, "..", "tests", "test_storage", "demo_docs"
))
DOCUMENTS_PATH = os.path.abspath(os.path.join(
    SRC_PATH, "..", ".data5"
))
docs_clxn = DocumentCollection(DOCUMENTS_PATH)
# initialize_database("/mnt/Storage/curated_files/Transcripts")
initialize_database(docs_clxn.transcripts_dir, load_files=True)
# initialize_database(os.path.join(TEST_COLLECTION_PATH, "Transcripts"), load_files=True)

# generate_response("Was weist du über den RAF extremisten, Peter-Jürgen Boock?", docs_clxn)
generate_response("Was war die Carlos Gruppe?", docs_clxn)
