from gui import main_view
from utils import logger
import streamlit as st


def main():
    main_view()
    logger.streamlit_logger()


if __name__ == "__main__":
    main()
