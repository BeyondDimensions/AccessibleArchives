import sys
from loguru import logger
st = None

logger.remove()

logger.add(
    sys.stdout,
    format="<cyan>{time:YYYY-MM-DD HH:mm:ss.SSS}</cyan> | <level>{level.icon}  {level: <9}</level>| <level>{message}</level>",
    colorize=True
)


def streamlit_logger():
    global st
    import streamlit as st


def success(message, log_to_gui=False):
    logger.success(message)
    if st and log_to_gui:
        st.success(message)


def info(message, log_to_gui=False):
    logger.info(message)
    if st and log_to_gui:
        st.info(message)


def important(message, log_to_gui=False):
    logger.important(message)
    if st and log_to_gui:
        st.warning(message)


def warning(message, log_to_gui=False):
    logger.warning(message)
    if st and log_to_gui:
        st.warning(message)


def error(message, log_to_gui=False):
    logger.error(message)
    if st and log_to_gui:
        st.error(message)


def debug(message):
    logger.debug(message)
