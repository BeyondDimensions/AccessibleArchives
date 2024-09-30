from storage import DocumentCollection
import os
SRC_PATH = os.path.abspath(os.path.join(__file__, "..", ".."))
TEST_COLLECTION_PATH = os.path.abspath(os.path.join(
    SRC_PATH, "..", "tests", "test_storage", "demo_docs"
))

known_doc_collections: list[DocumentCollection] = []


def load_known_docs():
    # TODO: replace with appdata memory of known collections
    known_doc_collections.append(DocumentCollection(
        # "/ipfs/QmZ75y9EkkVEpRKhWZn4Ba2E9yNAxbkqGjEFkKdmCUkL5h"
        # "/mnt/Storage/curated_files"
        TEST_COLLECTION_PATH
    ))
