import fitz  # pyMuPdf
import os

# Defining function to convert a single page of the:


def convert_pdf_page_to_png(pdf_document, page_number, pdf_output_folder):
    page = pdf_document.load_page(page_number)  # loading the page
    pix = page.get_pixmap()     # get the pixel map
    output_path = os.path.join(
        pdf_output_folder, f"page_{page_number + 1}.png")    # define output path
    pix.save(output_path)   # save the image as PNG
    print(f"Saved {output_path}")

# Defining the function for the entire PDF conversion:


def convert_pdf_to_png(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)  # open the PDF document
    # extract PDf name from file without extention
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    # create a folder with the file name
    pdf_output_folder = os.path.join(output_folder, pdf_name)

# create the output folder if it doesn't exist
    if os.path.exists(pdf_output_folder):
        return

    os.makedirs(pdf_output_folder)
    

    for page_number in range(len(pdf_document)):    # iterate through all pages
        convert_pdf_page_to_png(pdf_document, page_number, pdf_output_folder)

    print(f"PDF coversion complete for {pdf_path}!")


def convert_all_pdfs_in_folder(folder_path, output_folder):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.pdf'):  # check if the file is a PDF
            pdf_path = os.path.join(folder_path, file_name)
            convert_pdf_to_png(pdf_path, output_folder)


if __name__ == "__main__":
    folder_path = "/Users/marvinkirsch/DocumentsOB/ScansnapHome/Curation_Folder"
    output_folder = "/Users/marvinkirsch/DocumentsOB/ScansnapHome/Curation_Folder/PNGs"

    convert_all_pdfs_in_folder(folder_path, output_folder)
