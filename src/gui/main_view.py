import streamlit as st
from .chat_view import chat_view
from .pdf_view import pdf_view
from config import APP_NAME, FAVICON
from rag.database import initialize_database
from storage import load_known_docs, get_known_docs


def load_data():
    load_known_docs()
    st.session_state["current_doc_collection"] = get_known_docs()[0]
    initialize_database(
        st.session_state["current_doc_collection"].transcripts_dir, load_files=False)


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

    load_data()

    with st.container(height=None):
        # Layout for buttons and spacing
        chat_col, pdf_col, = st.columns([1, 1])
        with chat_col:
            chat_view()  # IMPORTANT: load chat view before PDF-View
        with pdf_col:
            pdf_view()  # IMPORTANT: load PDF-View after Chat view
