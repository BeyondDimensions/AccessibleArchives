import PyPDF2
from io import BytesIO


def extract_pages(pdf_data: bytes, pages: list):
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
    return (pdf_output.read(), num_pages, start_page, end_page)
