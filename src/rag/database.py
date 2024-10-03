import os
import shutil
from utils import logger
from config import CHROMA_WORKING_PATH, CHROMA_BACKUP_PATH
from .common import get_embedding_function
from .chunker import split_documents, assign_chunk_ids
from langchain_chroma import Chroma
from langchain.schema.document import Document
from langchain_community.document_loaders import DirectoryLoader
from tqdm import tqdm

# it might be beneficial to return a boolean value indicating whether the database was newly initialized or skipped.
# This could be useful for downstream logic that depends on database initialization.


def initialize_database(data_path, load_files=True):
    """Initialize the document database. Reset if needed."""
    try:
        if os.path.exists(CHROMA_BACKUP_PATH) and not load_files:
            return

        logger.info("✨ Initializing Database")
        documents = load_documents(data_path)
        if documents:
            chunks = split_documents(documents)
            save_chunks_to_chroma(chunks)
            logger.success("Successfully initialized database")
        else:
            logger.warning("No documents found to process.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")


def reset_database():
    """Clear the existing database."""
    try:
        if os.path.exists(CHROMA_WORKING_PATH):
            shutil.rmtree(CHROMA_WORKING_PATH)
            logger.success(f"Cleared existing database at {CHROMA_WORKING_PATH}")
    except Exception as e:
        logger.error(f"Error clearing database: {e}")
        raise e


def load_documents(data_path):
    """Load documents from the specified directory."""
    try:
        # TODO: ask user to select a document collection
        logger.info(
            f"Loading documents from {data_path}")
        loader = DirectoryLoader(
            data_path, glob="*.md",
            show_progress=True,
        )
        documents = loader.load()
        logger.success(
            f"Loaded {len(documents)} documents from {data_path}")
        return documents
    except Exception as e:
        logger.error(f"Error loading documents: {e}")
        raise e


def split_array(arr, chunk_size=10):
    # Use list comprehension to split the array into chunks
    return [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]


def load_db() -> Chroma:
    return Chroma(
        persist_directory=CHROMA_WORKING_PATH,
        embedding_function=get_embedding_function()
    )


def backup_chroma_db():
    # Make sure the backup path exists
    os.makedirs(CHROMA_BACKUP_PATH, exist_ok=True)
    # Copy the entire directory tree to the backup location
    shutil.copytree(CHROMA_WORKING_PATH, CHROMA_BACKUP_PATH, dirs_exist_ok=True)


def restore_chroma_db():
    # Make sure the original chroma path exists
    os.makedirs(CHROMA_WORKING_PATH, exist_ok=True)
    # Copy the backup directory back to the original chroma path
    shutil.copytree(CHROMA_BACKUP_PATH, CHROMA_WORKING_PATH, dirs_exist_ok=True)


def save_chunks_to_chroma(chunks: list[Document]):
    """Save chunked documents to the Chroma database."""
    try:
        db = load_db()

        chunks_with_ids = assign_chunk_ids(chunks)

        existing_ids = set(db.get(include=[])["ids"])
        logger.info(f"Existing IDs: {len(existing_ids)}")

        new_chunks = [
            chunk
            for chunk in chunks_with_ids
            if chunk.metadata["id"] not in existing_ids
        ]
        if new_chunks:
            logger.info(
                f"👉 Adding {len(new_chunks)} new documents to the database."
            )
            new_chunk_batches = split_array(new_chunks, chunk_size=10)
            for batch in tqdm(new_chunk_batches):
                batch_chunk_ids = [chunk.metadata["id"] for chunk in batch]
                db.add_documents(batch, ids=batch_chunk_ids)
                backup_chroma_db()
                db = load_db()
            logger.success(
                f"👉 Added {len(new_chunks)} new documents to the database.")
        else:
            logger.success("No new documents to add.")
    except Exception as e:
        logger.error(f"Error saving documents to Chroma: {e}")
        raise e
