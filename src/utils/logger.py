import loguru
st = None


def streamlit_logger():
    global st
    import streamlit as st


def success(message, log_to_gui=False):
    loguru.logger.success(message)
    if st and log_to_gui:
        st.success(message)


def info(message, log_to_gui=False):
    loguru.logger.info(message)
    if st and log_to_gui:
        st.info(message)


def important(message, log_to_gui=False):
    loguru.logger.important(message)
    if st and log_to_gui:
        st.warning(message)


def warning(message, log_to_gui=False):
    loguru.logger.warning(message)
    if st and log_to_gui:
        st.warning(message)


def error(message, log_to_gui=False):
    loguru.logger.error(message)
    if st and log_to_gui:
        st.error(message)
