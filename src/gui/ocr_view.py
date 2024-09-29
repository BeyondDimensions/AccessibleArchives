import os
import streamlit as st
from utils import logger
from utils import ensure_directories_exist
from ocr import transcribe_image
from utils import ALLOWED_OPENAI_MODELS, ORIGINAL_FOLDER, DATA_FOLDER


def get_pdf_input_from_user(input_option):
    """Handle PDF input based on user selection."""
    if input_option == 'Folder of PDFs':
        folder_path = st.text_input("Enter the folder path containing PDFs:")
        if not os.path.isdir(folder_path):
            logger.warning("Invalid folder path.", True)
            return None, None

        pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        if not pdf_files:
            logger.warning("No PDF files found in the specified folder.", True)
            return None, None

        return folder_path, pdf_files
    else:
        uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
        if uploaded_file is not None:
            ensure_directories_exist(ORIGINAL_FOLDER)
            pdf_path = os.path.join(ORIGINAL_FOLDER, uploaded_file.name)
            with open(pdf_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            return ORIGINAL_FOLDER, [uploaded_file.name]
        else:
            logger.warning("Please upload a PDF file.", True)
            return None, None


def ocr_view():
    st.header("OCR Processing")

    # Option to choose a single PDF or a folder
    input_option = st.radio('Input Option', ('Single PDF', 'Folder of PDFs'))

    folder_path, pdf_files = get_pdf_input_from_user(input_option)

    if not folder_path or not pdf_files:
        return

    gpt_version = st.selectbox('Select GPT Version', ALLOWED_OPENAI_MODELS)

    # Button to trigger the processing of selected PDFs
    if st.button('Start Processing PDFs'):
        pass
        # st.write(f"Processing {pdf_name}.pdf...")
        # for pdf_file in pdf_files:
        #     pdf_name = os.path.splitext(pdf_file)[0]
        #     pdf_path = os.path.join(folder_path, pdf_file)
        #
        #     # Process the PDF file when the button is clicked
        #     transcribe_image(os.path.join(DATA_FOLDER, 'test.jpg'),
        #                      os.path.join(DATA_FOLDER, 'test-output.md'),
        #                      gpt_version=gpt_version)
