import streamlit as st
from utils.chat_interface import chat_interface
from utils.doc_viewer import doc_viewer
from utils.process_files import process_files
# from config.config import LLM_MODELS


# Main Streamlit app
def main():
    st.title('Lighthouse')

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


if __name__ == "__main__":
    main()
