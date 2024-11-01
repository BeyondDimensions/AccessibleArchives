import streamlit as st
from storage import DocumentCollection
import os
import ipfs_api
from utils import logger
from config import DOC_COLLECTIONS_PATH

known_doc_collections: list[DocumentCollection] = []


@st.cache_data
def load_known_docs():
    logger.info("Loading known docs...")
    for name in os.listdir(DOC_COLLECTIONS_PATH):
        abs_path = os.path.join(DOC_COLLECTIONS_PATH, name)
        if os.path.isdir(abs_path):
            # ipfs_api.publish(DOCUMENTS_PATH)
            known_doc_collections.append(DocumentCollection(
                # "/ipfs/QmZ75y9EkkVEpRKhWZn4Ba2E9yNAxbkqGjEFkKdmCUkL5h"
                # "/mnt/Storage/curated_files"
                abs_path
            ))
    logger.success("Loaded known docs!")
    return known_doc_collections


@st.cache_data
def get_known_docs():
    return known_doc_collections
