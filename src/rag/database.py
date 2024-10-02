import os
import shutil
from utils import logger
from config import CHROMA_PATH
from .common import get_embedding_function
from .chunker import split_documents, assign_chunk_ids
from langchain_chroma import Chroma
from langchain.schema.document import Document
from langchain_community.document_loaders import DirectoryLoader
from storage import get_known_docs


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


def load_documents():
    """Load documents from the specified directory."""
    try:
        # TODO: ask user to select a document collection
        logger.info(
            f"Loading documents from {get_known_docs()[0].transcripts_dir}")
        loader = DirectoryLoader(
            get_known_docs()[0].transcripts_dir, glob="*.md",
            show_progress=True,
        )
        documents = loader.load()
        logger.success(
            f"Loaded {len(documents)} documents from {get_known_docs()[0].transcripts_dir}")
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
