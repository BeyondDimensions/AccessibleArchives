import streamlit as st
from .chat_view import chat_view
from .pdf_view import pdf_view
from config import APP_NAME, FAVICON
from storage import get_doc_colxns_names, get_doc_colxn
from rag import DocsEmbedding

from utils import logger


def streamlit_config():
    st.set_page_config(
        page_title=APP_NAME,
        page_icon=FAVICON,
        layout="wide"
    )
    st.html("<style> .main {overflow: hidden} </style>")


def main_view():
    # st.title('APP_NAME')

    streamlit_config()

    with st.container(height=None):
        label_col, selector_col, = st.columns([1, 3])
        with label_col:
            st.html('<b style="font-size: 2em">Document Collection:</b>')
        with selector_col:
            doc_colxn_name = st.selectbox(
                'Select DocColxn', get_doc_colxns_names(),
                label_visibility="collapsed"
            )
            logger.info(f"Selected DocColxn: {doc_colxn_name}")
            st.session_state['current_doc_collection'] = get_doc_colxn(doc_colxn_name)
            st.session_state['current_doc_embeddings'] = DocsEmbedding(
                doc_colxn_name,
                st.session_state['current_doc_collection'].transcripts_dir
            )
        # # Layout for buttons and spacing
        chat_col, pdf_col, = st.columns([1, 1])
        with chat_col:
            chat_view()  # IMPORTANT: load chat view before PDF-View
        with pdf_col:
            pdf_view()  # IMPORTANT: load PDF-View after Chat view
