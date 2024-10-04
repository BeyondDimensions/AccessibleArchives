from _load_src import SRC_PATH
from storage import DocumentCollection
import os
from rag import initialize_database
from config.rag_config import INITIAL_CHAT_HISTORY, AI_NAME, USER_NAME


from rag.query_engine import generate_response
from rag.query_engine import format_history
TEST_COLLECTION_PATH = os.path.abspath(os.path.join(
    SRC_PATH, "..", "tests", "test_storage", "demo_docs"
))
DOCUMENTS_PATH = os.path.abspath(os.path.join(
    SRC_PATH, "..", ".data5"
))
docs_clxn = DocumentCollection(DOCUMENTS_PATH)
# initialize_database("/mnt/Storage/curated_files/Transcripts")
initialize_database(docs_clxn.transcripts_dir, load_files=False)
# initialize_database(os.path.join(TEST_COLLECTION_PATH, "Transcripts"), load_files=True)

print(format_history(INITIAL_CHAT_HISTORY))
# generate_response("Was weist du über den RAF extremisten, Peter-Jürgen Boock?", docs_clxn)
generate_response("Llama3", "Was war die Carlos Gruppe?", INITIAL_CHAT_HISTORY, docs_clxn)
