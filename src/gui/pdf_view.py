from io import BytesIO
import streamlit as st
from utils import encode_data_base64
from storage import get_known_docs
from formatting.pdf_pagination import extract_pages

# how many PDF pages to display at once
PAGES_PER_CHUNK = 1


def display_pdf(pdf_data: bytes, page_number: int):
    """Display the given PDF file at the specified page."""
    # extract the next few pages
    page_numbers = list(range(page_number, page_number + PAGES_PER_CHUNK))
    pdf_data_chunk, num_pages, start_page, end_page = extract_pages(
        pdf_data, page_numbers)
    base64_pdf = encode_data_base64(pdf_data_chunk)

    # Embedding PDF in HTML
    pdf_display = f'''
    <style>
        body {{
            overflow: hidden;  /* Hide scrollbar */
        }}
        #pdf-container {{
            display: flex;
            justify-content: center;  /* Center horizontally */
            align-items: center;  /* Center vertically if needed */
            height: calc(100vh - 250px);  /* Adjust based on your layout */
        }}
        #pdf-iframe {{
            width: 75%;  /* Adjust width as needed */
            height: 100%;
            border: none;  /* Remove border */
        }}
    </style>
    <div id="pdf-container">
        <iframe id="pdf-iframe" src="data:application/pdf;base64,{base64_pdf}" type="application/pdf"></iframe>
    </div>
    <script>
        // Function to resize the iframe on window resize
        function resizeIframe() {{
            const iframe = document.getElementById('pdf-iframe');
            iframe.style.height = window.innerHeight + 'px';
        }}

        window.addEventListener('resize', resizeIframe);
        // Initial call to set the height
        resizeIframe();
    </script>
'''

    display_page_navigation(num_pages, start_page + 1, end_page + 1)

    # Display the PDF file
    st.markdown(pdf_display, unsafe_allow_html=True)


def display_page_navigation(num_pages, start_page, end_page=None):
    """Display a label showing which page number(s) is/are currently loaded."""
    # Create two columns for layout
    last_col, _, col2, _, next_col = st.columns(
        [1, 4, 1, 4, 1])  # Layout for buttons and spacing

    # Display navigation buttons

    with last_col:
        if st.button("Last"):
            # Ensure we don't go below the first page
            if st.session_state['current_page'] >= PAGES_PER_CHUNK:
                st.session_state['current_page'] -= PAGES_PER_CHUNK

    # "Next" button
    with next_col:
        if st.button("Next"):
            # Ensure we don't exceed the total pages
            if st.session_state['current_page'] + PAGES_PER_CHUNK < num_pages:
                st.session_state['current_page'] += PAGES_PER_CHUNK
            # Add a button to download the PDF
            # with open(pdf_path, "rb") as pdf_file:
    with col2:
        if end_page is None or start_page == end_page:
            text = f"Page  {start_page}"
        else:
            text = f"Pages {start_page} - {end_page}"

        st.markdown(text)


def pdf_view():
    """Display a PDF viewer with a document selector, download button etc."""
    # st.header("Document Viewer")
    with st.container(height=850, border=False):
        # TODO: ask user to select a document collection
        selected_doc_collection = get_known_docs()[0]
        pdf_files = selected_doc_collection.get_multipagedoc_ids()

        if not pdf_files:
            st.write("No PDF files found in the folder.")
        else:
            selector_col, download_col = st.columns(
                [5, 1])  # Layout for buttons and spacing

            with selector_col:
                selected_pdf = st.selectbox(
                    'Select Document', pdf_files, label_visibility="collapsed")

            if selected_pdf:
                if 'current_page' not in st.session_state:
                    st.session_state['current_page'] = 0
                document = selected_doc_collection.get_multipagedoc(
                    selected_pdf)

                st.session_state["pdf_data"] = document.compilations[0].get_data()
                virtual_pdf_file = BytesIO(st.session_state["pdf_data"])

            with download_col:
                st.download_button(
                    label="Download PDF",
                    data=virtual_pdf_file,
                    file_name=selected_pdf+".pdf",
                    mime="application/pdf"
                )

            # Display the current chunk of the PDF based on the current page
            display_pdf(st.session_state["pdf_data"],
                        st.session_state['current_page'])
