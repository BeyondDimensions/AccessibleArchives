import os
import streamlit as st
from utils import encode_file_base64
from utils import ensure_directories_exist
from config.config import PROCESSED_FOLDER


def list_pdfs_in_folder(folder_path):
    files = os.listdir(folder_path)
    pdf_files = [file for file in files if file.endswith('.pdf')]
    return pdf_files


def display_pdf(file):
    base64_pdf = encode_file_base64()

    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


def pdf_view():
    st.header("Document Viewer")

    ensure_directories_exist(PROCESSED_FOLDER)
    pdf_files = list_pdfs_in_folder(PROCESSED_FOLDER)

    if not pdf_files:
        st.write("No PDF files found in the folder.")
    else:
        selected_pdf = st.selectbox('Select a PDF file', pdf_files)

        if selected_pdf:
            pdf_path = os.path.join(PROCESSED_FOLDER, selected_pdf)

            # Create two columns for layout
            col1, col2 = st.columns([4, 1])  # Adjust the ratio as needed

            with col1:
                st.write(f"### Previewing PDF: {selected_pdf}")
                try:
                    display_pdf(pdf_path)
                except Exception as e:
                    st.error(
                        f"An error occurred while displaying the PDF: {e}")

            with col2:
                # Add a button to download the PDF
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_file,
                        file_name=selected_pdf,
                        mime="application/pdf"
                    )
