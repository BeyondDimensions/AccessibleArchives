import streamlit as st
from .chat_view import chat_view
from .pdf_view import pdf_view
from .ocr_view import ocr_view


def set_page_style():
    st.html("<style> .main {overflow: hidden} </style>")


def main_view():
    # st.title('Accessible Archives')
    set_page_style()

    pdf_col, chat_col = st.columns([1, 1])  # Layout for buttons and spacing
    with pdf_col:
        pdf_view()
    with chat_col:
        chat_view()
