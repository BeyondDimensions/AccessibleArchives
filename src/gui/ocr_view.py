import os
import streamlit as st
from utils.ocr_utils import get_pdf_input_from_user, process_and_transcribe_pdf
from config.config import ALLOWED_VERSIONS

def ocr_view():
    st.header("OCR Processing")

    # Option to choose a single PDF or a folder
    input_option = st.radio('Input Option', ('Single PDF', 'Folder of PDFs'))

    folder_path, pdf_files = get_pdf_input_from_user(input_option)

    if not folder_path or not pdf_files:
        return

    gpt_version = st.selectbox('Select GPT Version', ALLOWED_VERSIONS)

    # Button to trigger the processing of selected PDFs
    if st.button('Start Processing PDFs'):
        for pdf_file in pdf_files:
            pdf_name = os.path.splitext(pdf_file)[0]
            pdf_path = os.path.join(folder_path, pdf_file)

            # Process the PDF file when the button is clicked
            process_and_transcribe_pdf(pdf_path, pdf_name, gpt_version)
