import streamlit as st
from gui.chat_view import chat_view
from gui.pdf_view import pdf_view
from gui.ocr_view import ocr_view


def main_view():
    st.title('Accessible Archives')

    # Tabs setup
    st.sidebar.title("Navigation")
    tabs = ['Chatbot', 'Document Viewer', 'OCR Processing']
    choice = st.sidebar.selectbox('Select Tab', tabs)

    if choice == 'Chatbot':
        chat_view()
    elif choice == 'Document Viewer':
        pdf_view()
    elif choice == 'OCR Processing':
        ocr_view()
