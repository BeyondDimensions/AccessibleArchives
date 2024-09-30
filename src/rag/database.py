import os
import shutil
from utils import logger
from utils import CHROMA_PATH, DATA_FOLDER
from .common import get_embedding_function
from langchain_chroma import Chroma
from langchain.schema.document import Document
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from storage import known_doc_collections


def initialize_database(reset=False):
    """Initialize the document database. Reset if needed."""
    try:
        if reset or not os.path.exists(CHROMA_PATH):
            logger.info("✨ Initializing Database")
            reset_database()
            documents = load_documents()
            if documents:
                chunks = split_documents(documents)
                save_chunks_to_chroma(chunks)
                logger.success("Successfully initialized database")
            else:
                logger.warning("No documents found to process.")
        else:
            logger.info("Database already exists. Skipping initialization.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")


def reset_database():
    """Clear the existing database."""
    try:
        if os.path.exists(CHROMA_PATH):
            shutil.rmtree(CHROMA_PATH)
            logger.success(f"Cleared existing database at {CHROMA_PATH}")
    except Exception as e:
        logger.error(f"Error clearing database: {e}")
        raise e


# TODO: ask user to select a document collection


def load_documents():
    """Load documents from the specified directory."""
    try:
        loader = DirectoryLoader(known_doc_collections.transcripts_dir, glob="*.md")
        documents = loader.load()
        logger.info(
            f"Loaded {len(documents)} documents from {DATA_FOLDER}")
        return documents
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        raise e


def save_chunks_to_chroma(chunks: list[Document]):
    """Save chunked documents to the Chroma database."""
    try:
        db = Chroma(persist_directory=CHROMA_PATH,
                    embedding_function=get_embedding_function())

        chunks_with_ids = assign_chunk_ids(chunks)

        existing_ids = set(db.get(include=[])["ids"])

        new_chunks = [
            chunk
            for chunk in chunks_with_ids
            if chunk.metadata["id"] not in existing_ids
        ]

        if new_chunks:
            logger.info(
                f"👉 Adding {len(new_chunks)} new documents to the database.")
            new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
            db.add_documents(new_chunks, ids=new_chunk_ids)
        else:
            logger.success("No new documents to add.")
    except Exception as e:
        logger.error(f"Error saving documents to Chroma: {e}")
        raise e


def split_documents(documents: list[Document]):
    """Split loaded documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(
        f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks


def assign_chunk_ids(chunks):
    """Assign unique chunk IDs to each document chunk."""
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    logger.info(f"Assigned IDs to {len(chunks)} chunks.")
    return chunks
