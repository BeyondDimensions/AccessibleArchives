import streamlit as st
from storage import DocumentCollection
import os
import ipfs_api
from utils import logger
SRC_PATH = os.path.abspath(os.path.join(__file__, "..", ".."))
TEST_COLLECTION_PATH = os.path.abspath(os.path.join(
    SRC_PATH, "..", "tests", "test_storage", "demo_docs"
))
# TEST_COLLECTION_PATH = os.path.abspath(os.path.join(
#     SRC_PATH, "..", ".data"
# ))


known_doc_collections: list[DocumentCollection] = []


@st.cache_data
def load_known_docs():
    logger.info("Loading known docs...")
    # TODO: replace with appdata memory of known collections
    ipfs_api.publish(TEST_COLLECTION_PATH)
    known_doc_collections.append(DocumentCollection(
        # "/ipfs/QmZ75y9EkkVEpRKhWZn4Ba2E9yNAxbkqGjEFkKdmCUkL5h"
        # "/mnt/Storage/curated_files"
        TEST_COLLECTION_PATH
    ))
    logger.success("Loaded known docs!")
    return known_doc_collections


@st.cache_data
def get_known_docs():
    return known_doc_collections
