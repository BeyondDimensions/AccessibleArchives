"""This script demonstrates how the RAG system might access document storage."""
import os
from _load_src import SRC_PATH
from storage.storage_api import MultiPageDoc, DocumentCollection

TEST_COLLECTION_PATH = os.path.join(
    SRC_PATH, "..", "tests", "test_storage", "demo_docs"
)

collection = DocumentCollection(TEST_COLLECTION_PATH)

# this is the directory with the transcripts MD files
collection.transcripts_dir

# given a transcript file, get it's page's ID
transcript_1_filename = os.listdir(collection.transcripts_dir)[0]
page_id = transcript_1_filename.strip(".md")

# get the first document associated with this page
docs: list[MultiPageDoc] = collection.get_page_docs(page_id)
doc = docs[0]

# get the PDF file
pdf_content: bytes = doc.compilations[0].get_data()

# get the page number (counting starts at 0)
page_number = doc.get_page_number(page_id)
