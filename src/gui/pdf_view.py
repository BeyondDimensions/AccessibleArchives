import base64
import PyPDF2
from io import BytesIO
from storage import DocumentCollection
import os
import streamlit as st
from utils import encode_data_base64
from utils import ensure_directories_exist
from storage import get_known_docs
from formatting.pdf_pagination import extract_pages

# Set the number of pages per chunk
pages_per_chunk = 1


def list_pdfs_in_folder(folder_path):
    files = os.listdir(folder_path)
    pdf_files = [file for file in files if file.endswith('.pdf')]
    return pdf_files


def display_pdf(pdf_data: bytes, page_number: int):
    # Extract the next 3 pages (or adjust to your needs)
    page_numbers = list(range(page_number, page_number+pages_per_chunk))
    pdf_data_chunk, start_page, end_page = extract_pages(pdf_data, page_numbers)
    print(len(pdf_data_chunk))
    base64_pdf = encode_data_base64(pdf_data_chunk)

    # Embedding PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{
        base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'

    display_page_label(start_page+1, end_page+1)

    # Display the PDF file
    st.markdown(pdf_display, unsafe_allow_html=True)


def display_page_label(start_page, end_page):
    if start_page == end_page:
        text = f"Page  {start_page}"
    else:
        text = f"Pages {start_page} - {end_page}"

    st.markdown(text)


def pdf_view():
    st.header("Document Viewer")

    # TODO: ask user to select a document collection
    selected_doc_collection = get_known_docs()[0]
    pdf_files = selected_doc_collection.get_multipagedoc_ids()

    if not pdf_files:
        st.write("No PDF files found in the folder.")
    else:
        col1, col2 = st.columns([5, 1])  # Layout for buttons and spacing

        with col1:
            selected_pdf = st.selectbox('Select a PDF file', pdf_files)

        if selected_pdf:
            document = selected_doc_collection.get_multipagedoc(selected_pdf)

            st.session_state["pdf_data"] = document.compilations[0].get_data()
            virtual_pdf_file = BytesIO(st.session_state["pdf_data"])

            with col2:
                st.download_button(
                    label="Download PDF",
                    data=virtual_pdf_file,
                    file_name=selected_pdf+".pdf",
                    mime="application/pdf"
                )

            # Create two columns for layout
            col1, col2, col3 = st.columns([1, 6, 1])  # Layout for buttons and spacing

            num_pages = len(PyPDF2.PdfReader(BytesIO(st.session_state["pdf_data"])).pages)

            # Display navigation buttons
            if not 'current_page' in st.session_state:
                st.session_state['current_page'] = 0
            with col1:
                if st.button("last"):
                    # Ensure we don't go below the first page
                    if st.session_state['current_page'] >= pages_per_chunk:
                        st.session_state['current_page'] -= pages_per_chunk

            # "Next" button
            with col3:
                if st.button("next"):
                    # Ensure we don't exceed the total pages
                    if st.session_state['current_page'] + pages_per_chunk < num_pages:
                        st.session_state['current_page'] += pages_per_chunk
                    # Add a button to download the PDF
                    # with open(pdf_path, "rb") as pdf_file:

            # Display the current chunk of the PDF based on the current page
            display_pdf(st.session_state["pdf_data"], st.session_state['current_page'])
