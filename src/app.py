from storage import load_known_docs
from gui import main_view
from utils import logger
import streamlit as st

st.set_page_config(
    page_title="Accessible Archives",
    page_icon="../release/icon.png",  # Use a path to your favicon file
    layout="wide"
)

load_known_docs()


def main():
    logger.streamlit_logger()
    main_view()


if __name__ == "__main__":
    main()
