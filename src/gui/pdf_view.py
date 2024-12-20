from . import state_data
from utils import logger
from io import BytesIO
import streamlit as st
from utils import encode_data_base64
from formatting.pdf_pagination import extract_pages

# how many PDF pages to display at once
PAGES_PER_CHUNK = 1


def display_pdf(pdf_data: bytes, page_number: int):
    """Display the given PDF file at the specified page."""
    # extract the next few pages
    pdf_data_chunk, num_pages, start_page, end_page = extract_pages(
        pdf_data, [page_number])
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
            height: calc(100vh - 330px);  /* Adjust based on your layout */
        }}
        #pdf-iframe {{
            width: 75%;  /* Adjust width as needed */
            height: 100%;
            border: none;  /* Remove border */
        }}
    </style>
    <div id="pdf-container">
        <iframe id="pdf-iframe" src="data:application/pdf;base64,{base64_pdf}#zoom=58" type="application/pdf"></iframe>
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

    # Display the PDF file
    st.markdown(pdf_display, unsafe_allow_html=True)



def display_page_navigation(num_pages):
    """Display a label showing which page number(s) is/are currently loaded."""
    # Create two columns for layout
    _, last_col, page_num_col, next_col, _ = st.columns([2, 2, 1, 2, 2])  # Layout for buttons and spacing

    # Display navigation buttons

    with last_col:
        label = state_data.get_language_config().gui_text.LAST_PAGE
        # Ensure we don't go below the first page
        if st.button(label):
            if st.session_state['current_page'] > 0:

                st.session_state['current_page'] -= PAGES_PER_CHUNK

    # "Next" button
    with next_col:
        label = state_data.get_language_config().gui_text.NEXT_PAGE
        
        # Ensure we don't exceed the total pages
        if st.button(label=label, key=2345):
            if st.session_state['current_page'] < num_pages-1:
                st.session_state['current_page'] += PAGES_PER_CHUNK
            # Add a button to download the PDF
            # with open(pdf_path, "rb") as pdf_file:
    with page_num_col:
        label = state_data.get_language_config().gui_text.PAGE
        text = f"{label}  {st.session_state['current_page']+1}/{num_pages}"

        st.markdown(text)
    


def pdf_view():
    """Display a PDF viewer with a document selector, download button etc."""
    # st.header("Document Viewer")
    
    if "current_doc_collection" in st.session_state:
        selected_doc_collection = st.session_state["current_doc_collection"]
        pdf_files = selected_doc_collection.get_multipagedoc_ids()
    else:
        pdf_files = None
    if not pdf_files:
        st.write("No PDF files to display.")
    else:

        label_col, selector_col, download_col = st.columns([1, 3, 1])
        with label_col:
            label = state_data.get_language_config().gui_text.DOCUMENT
            
            st.html(f'<b style="font-size: 2em">{label}:</b>')

        with selector_col:
            label = state_data.get_language_config().gui_text.PAGE
            selected_pdf = st.selectbox(
                label, pdf_files, label_visibility="collapsed"
            )
        if st.session_state["llm-recommended-pdf"]:
            # try:
            doc = selected_doc_collection.get_page_docs(
                st.session_state["llm-recommended-pdf"])[0]
            selected_pdf = doc.ipfs_id
            page_num = doc.get_page_number(
                st.session_state["llm-recommended-pdf"])
            st.session_state['current_page'] = page_num
            logger.info(
                f"Recommended PDF: {st.session_state['llm-recommended-pdf']} {st.session_state['current_page']}")
            # except Exception as e:
            #     logger.error(e)
        if not selected_pdf:
            return
        if 'current_page' not in st.session_state:
            st.session_state['current_page'] = 0
        document = selected_doc_collection.get_multipagedoc(
            selected_pdf)
        
        
        
        # let user choose the page
        display_page_navigation(len(document.get_page_ids()))
        
        # get text data
        page = document.get_page_from_page_number(st.session_state['current_page'])
        st.session_state["transcript_text"] = page.transcripts[0].get_text()
        
        # get PDF dta
        st.session_state["pdf_data"] = document.compilations[0].get_data()
        virtual_pdf_file = BytesIO(st.session_state["pdf_data"])
        
        with download_col:
            label = state_data.get_language_config().gui_text.DOWNLOAD_DOCUMENT
            
            st.download_button(
                label=label,
                data=virtual_pdf_file,
                file_name=selected_pdf + ".pdf",
                mime="application/pdf"
            )
        txt_col = None
        if st.session_state['display_txt'] and st.session_state['display_pdf']:
            pdf_col, txt_col = st.columns([1, 1])
        else:
            pdf_col, = st.columns([1])
        with pdf_col:
            with st.container(height=600, border=False):
                    
                # Display the current chunk of the PDF based on the current page
                display_pdf(st.session_state["pdf_data"],
                            st.session_state['current_page'])
        if txt_col:
            with txt_col:
                with st.container(height=600, border=False):
                    
                    st.markdown(st.session_state["transcript_text"])
            