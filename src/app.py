from rag.database import initialize_database
from storage import load_known_docs, get_known_docs
from gui import main_view
from utils import logger
import streamlit as st


def load_data():
    load_known_docs()
    st.session_state["current_doc_collection"] = get_known_docs()[0]
    initialize_database(
        st.session_state["current_doc_collection"].transcripts_dir, load_files=False)


def main():
    main_view()
    logger.streamlit_logger()


if __name__ == "__main__":
    main()
