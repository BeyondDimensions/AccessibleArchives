from gui.main_view import main_view
from utils import logger


def main():
    logger.streamlit_logger()
    main_view()


if __name__ == "__main__":
    main()
