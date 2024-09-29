import os
from datetime import datetime, UTC
from _load_src import SRC_PATH
from storage.storage_api import MultiPageDoc, DocumentCollection, Page, Transcript, PageSource
from storage.ipfs_localfs_interop import read_file, get_ipfs_cid

TEST_COLLECTION_PATH = os.path.join(
    SRC_PATH, "..", "tests", "test_storage", "demo_docs"
)
PAGE_ID = "QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2"
DOC_ID = "Qmb4yZQxAaWkrR2hNKcBBnxvEyvewGXqpQtBZHziAWaZov"
COMPILATION_ID = "Qmb8bSRLULw4nsCjQ959cLAxsbuBib2KZpHhS6fxBgvF4y"
# Utility function to load a page from a file


def load_page_metadata(PAGE_ID: str) -> Page:
    """Load a Page from its metadata JSON file."""
    page_path = os.path.join(TEST_COLLECTION_PATH,
                             "PageMetadata", f"{PAGE_ID}.json")
    return Page.from_json(read_file(page_path))


# Utility function to load transcript text
def read_transcript(PAGE_ID: str) -> str:
    transcript_path = os.path.join(
        TEST_COLLECTION_PATH, "Transcripts", f"{PAGE_ID}.md")
    return read_file(transcript_path).decode()


# Utility function to load a MultiPageDoc from a file
def load_multipagedoc(DOC_ID: str) -> MultiPageDoc:
    """Load a MultiPageDoc from its metadata JSON file."""
    doc_path = os.path.join(TEST_COLLECTION_PATH,
                            "MultiPageDocs", f"{DOC_ID}.json")
    return MultiPageDoc.from_json(read_file(doc_path))


def test_page():
    """Run tests for the Page class."""
    page = load_page_metadata(PAGE_ID)

    # Assert that the IPFS ID matches
    assert page.ipfs_id == PAGE_ID

    # Check if transcript text matches the expected content
    transcript_text = read_transcript(PAGE_ID)
    assert page.transcripts[0].get_text() == transcript_text


# Test for the MultiPageDoc object
def test_multipagedoc():
    """Run tests for the MultiPageDoc class."""

    doc = load_multipagedoc(DOC_ID)
    page = load_page_metadata(PAGE_ID)

    # Assert that the page is linked to the document
    assert page in doc.get_pages()
    assert PAGE_ID in doc.get_page_ids()

    # Assert that the compilation format and IPFS ID match
    assert doc.compilations[0].format == "pdf"
    assert doc.compilations[0].ipfs_id == COMPILATION_ID
    page_metadata_path = os.path.join(TEST_COLLECTION_PATH,
                                      "PageMetadata", f"{PAGE_ID}.json")
    assert page.ipfs_id == doc.get_page_id_from_metadata_id(get_ipfs_cid(page_metadata_path))
    assert doc.get_page_from_page_number(0) == page
    assert doc.get_page_number(page.ipfs_id) == 0

# Test for the DocumentCollection object


def test_document_collection():
    """Run tests for the DocumentCollection class."""

    collection = DocumentCollection(TEST_COLLECTION_PATH)
    page = load_page_metadata(PAGE_ID)
    doc = load_multipagedoc(DOC_ID)

    # Assert that the page is in the collection
    assert page in collection.get_pages()
    assert PAGE_ID in collection.get_page_ids()
    assert page == collection.get_page(page.ipfs_id)

    # Assert that the MultiPageDoc is in the collection
    assert doc in collection.get_multipagedocs()

    assert doc in collection.get_page_docs(page.ipfs_id)
    page_metadata_path = os.path.join(TEST_COLLECTION_PATH,
                                      "PageMetadata", f"{PAGE_ID}.json")
    assert page.ipfs_id == collection.get_page_id_from_metadata_id(get_ipfs_cid(page_metadata_path))


def run_tests():
    test_page()
    test_multipagedoc()
    test_document_collection()


if __name__ == "__main__":
    run_tests()
