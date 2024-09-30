from gui import main_view
from utils import logger

from storage import load_known_docs

load_known_docs()


def main():
    logger.streamlit_logger()
    main_view()


if __name__ == "__main__":
    main()
