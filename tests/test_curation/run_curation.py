import os
from _load_src import SRC_PATH
from curation.curation import curate_pngs


input_dir = "/Users/marvinkirsch/DocumentsOB/ScansnapHome/Curation_Folder"
original_medium = "Photocopy of Folder from BSTU"
# pdf_path = "/Users/marvinkirsch/DocumentsOB/ScansnapHome/Curation_Folder"
output_dir = os.path.abspath(os.path.join(
    __file__, "..", "..", "..", "curated_files"))
for file_name in os.listdir(input_dir):
    if file_name.endswith('.pdf'):  # check if the file is a PDF
        pdf_path = os.path.join(input_dir, file_name)
        dirname = file_name.strip(".pdf")
        png_dir = os.path.join(input_dir, "PNGs", dirname)

        curate_pngs(png_dir, output_dir, original_medium, pdf_path)
