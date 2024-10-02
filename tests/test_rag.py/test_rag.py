from _load_src import SRC_PATH
from storage.known_doc_collections import TEST_COLLECTION_PATH
import os
from rag import initialize_database
# initialize_database("/mnt/Storage/curated_files/Transcripts")
initialize_database(os.path.join(TEST_COLLECTION_PATH, "Transcripts"), load_files=False)
initialize_database(os.path.join(TEST_COLLECTION_PATH, "Transcripts"), load_files=True)
