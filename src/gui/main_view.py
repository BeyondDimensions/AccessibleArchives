import streamlit as st
from .chat_view import chat_view
from .pdf_view import pdf_view
from .ocr_view import ocr_view
from config import APP_NAME, FAVICON


def set_page_style():
    st.html("<style> .main {overflow: hidden} </style>")


st.set_page_config(
    page_title=APP_NAME,
    page_icon=FAVICON,
    layout="wide"
)


def main_view():
    # st.title('Accessible Archives')
    set_page_style()
    with st.container(height=None):
        # Layout for buttons and spacing
        chat_col, pdf_col, = st.columns([1, 1])
        with chat_col:
            chat_view()
        with pdf_col:
            pdf_view()
