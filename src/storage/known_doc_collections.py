from typing import TypeVar
from time import sleep
import streamlit as st
from storage import DocumentCollection
import os
import ipfs_api
from utils import logger
from config import DOC_COLLECTIONS_PATH


class NotLoaded:
    pass


class Loading:
    pass


DocColxn = TypeVar('DocColxn', NotLoaded, Loading, DocumentCollection)

AUTO_LOAD_ALL = False  # load all document collections on startup


def load_known_docs():

    known_doc_collections: dict[str, DocColxn] = {}
    logger.info("Loading known docs...")
    for name in os.listdir(DOC_COLLECTIONS_PATH):
        abs_path = os.path.join(DOC_COLLECTIONS_PATH, name)
        if os.path.isdir(abs_path):
            doc_colxn = NotLoaded()
            if AUTO_LOAD_ALL:
                doc_colxn = DocumentCollection(abs_path)
            known_doc_collections.update({name: doc_colxn})
    logger.success("Loaded known docs!")
    st.session_state["known_doc_collections"] = known_doc_collections


def doc_colxns() -> dict[str, DocColxn]:
    """Get a dictionary of DocumentCollection objects"""
    if "known_doc_collections" not in st.session_state:
        load_known_docs()
    return st.session_state["known_doc_collections"]


def get_doc_colxns_names() -> list[str]:
    """Get the names of the document collections we have."""
    names = list(doc_colxns().keys())
    names.sort()
    return names


def get_doc_colxn(doc_colxn_name: str) -> DocumentCollection:
    """Get a DocumentCollection given its name."""
    doc_colxn = doc_colxns()[doc_colxn_name]
    if isinstance(doc_colxn, NotLoaded):
        logger.info(f"Loading DocumentCollection {doc_colxn_name}")
        doc_colxns()[doc_colxn_name] = Loading()
        abs_path = os.path.join(DOC_COLLECTIONS_PATH, doc_colxn_name)
        doc_colxn = DocumentCollection(abs_path)
        doc_colxns()[doc_colxn_name] = doc_colxn
    while isinstance(doc_colxn, Loading):
        sleep(0.1)
    return doc_colxn
