import streamlit as st
import PyPDF2
from io import BytesIO
import base64

# Function to extract specific pages from PDF


def extract_pages(pdf_data: bytes, pages: list):
    # print(pages)
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_data))
    pdf_writer = PyPDF2.PdfWriter()

    # Ensure we don't exceed the total number of pages
    num_pages = len(pdf_reader.pages)
    start_page = None
    end_page = None
    for page_number in pages:
        if 0 <= page_number < num_pages:  # Ensure valid page numbers
            if start_page is None:
                start_page = page_number
            end_page = page_number
            pdf_writer.add_page(pdf_reader.pages[page_number])

    pdf_output = BytesIO()
    pdf_writer.write(pdf_output)
    pdf_output.seek(0)
    return (pdf_output.read(), start_page, end_page)

# Function to encode binary data to base64


def encode_data_base64(data: bytes) -> str:
    return base64.b64encode(data).decode("utf-8")

# Function to display PDF


def display_pdf(pdf_data: bytes, page_number: int):
    # Extract the next 3 pages (or adjust to your needs)
    page_numbers = list(range(page_number, page_number+pages_per_chunk))
    pdf_data_chunk, start_page, end_page = extract_pages(pdf_data, page_numbers)
    # print(len(pdf_data_chunk))
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


# PDF Data - (replace with actual data loading)
with open("sample.pdf", "rb") as f:
    pdf_data = f.read()

# Set the number of pages per chunk
pages_per_chunk = 1

# Initialize session state to track the current page
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 0

# Calculate total number of pages in the PDF
num_pages = len(PyPDF2.PdfReader(BytesIO(pdf_data)).pages)

# Display navigation buttons
col1, col2, col3 = st.columns([1, 6, 1])  # Layout for buttons and spacing

# "Previous" button
with col1:
    if st.button("last"):
        # Ensure we don't go below the first page
        if st.session_state['current_page'] >= pages_per_chunk:
            st.session_state['current_page'] -= pages_per_chunk

# Display currently displayed page numbers
start_page = st.session_state['current_page'] + 1  # Starting page (1-based index)
end_page = min(st.session_state['current_page'] + pages_per_chunk, num_pages)  # Ending page

# "Next" button
with col3:
    if st.button("next"):
        # Ensure we don't exceed the total pages
        if st.session_state['current_page'] + pages_per_chunk < num_pages:
            st.session_state['current_page'] += pages_per_chunk
# Display the current chunk of the PDF based on the current page
display_pdf(pdf_data, st.session_state['current_page'])
