from io import BytesIO
from storage import DocumentCollection
import os
import streamlit as st
from utils import encode_data_base64
from utils import ensure_directories_exist
from utils import PROCESSED_FOLDER


def list_pdfs_in_folder(folder_path):
    files = os.listdir(folder_path)
    pdf_files = [file for file in files if file.endswith('.pdf')]
    return pdf_files


def display_pdf(pdf_data: bytes, page_number: int):
    base64_pdf = encode_data_base64(pdf_data)

    # TODO: scroll to page number
    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{
        base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


# TODO: ask user to select a document collection
CURRENT_DOCUMENT_COLLECTION = DocumentCollection(
    "/ipfs/QmZ75y9EkkVEpRKhWZn4Ba2E9yNAxbkqGjEFkKdmCUkL5h")


def pdf_view():
    st.header("Document Viewer")

    pdf_files = DocumentCollection.get_multipagedoc_ids()

    if not pdf_files:
        st.write("No PDF files found in the folder.")
    else:
        selected_pdf = st.selectbox('Select a PDF file', pdf_files)

        if selected_pdf:
            document = CURRENT_DOCUMENT_COLLECTION.get_multipagedoc(selected_pdf)
            pdf_data = document.compilations[0].get_data()
            # Create two columns for layout
            col1, col2 = st.columns([4, 1])  # Adjust the ratio as needed

            with col1:
                st.write(f"### Previewing PDF: {selected_pdf}")
                try:
                    display_pdf(pdf_data)
                except Exception as e:
                    st.error(
                        f"An error occurred while displaying the PDF: {e}")

            with col2:
                # Add a button to download the PDF
                # with open(pdf_path, "rb") as pdf_file:
                virtual_pdf_file = BytesIO(pdf_data)

                st.download_button(
                    label="Download PDF",
                    data=virtual_pdf_file,
                    file_name=selected_pdf,
                    mime="application/pdf"
                )
