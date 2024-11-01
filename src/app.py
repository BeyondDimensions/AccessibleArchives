from gui import main_view, initialise_st_session
from utils import logger
import streamlit as st


def main():
    initialise_st_session()
    main_view()
    logger.streamlit_logger()


if __name__ == "__main__":
    main()
