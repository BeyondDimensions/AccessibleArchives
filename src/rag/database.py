import os
import shutil
from utils import logger
from .common import get_embedding_function
from .chunker import split_documents, assign_chunk_ids, load_documents, split_array
from langchain_chroma import Chroma
from langchain.schema.document import Document
from tqdm import tqdm
from utils.utils import ensure_dir_exists
from config import RAG_CONFIG
# it might be beneficial to return a boolean value indicating whether the database was newly initialized or skipped.
# This could be useful for downstream logic that depends on database initialization.

from config import DOC_EMBEDDINGS_PATH


class DocsEmbedding:
    def __init__(self, name, data_path):
        self.data_path = data_path
        self.working_dir = os.path.join(DOC_EMBEDDINGS_PATH, name, "current")

        self.backup_dir = os.path.join(DOC_EMBEDDINGS_PATH, name, "backup")

        self.initialize_database()

    def initialize_database(self, load_files=False):
        """Initialize the document database. Reset if needed."""
        try:
            if os.path.exists(self.backup_dir) and not load_files:
                logger.info("Skipping loading DocsEmbedding from files.")
                return

            logger.info("✨ Initializing Database")
            documents = load_documents(self.data_path)
            if documents:
                chunks = split_documents(documents)
                self._embed_chunks(chunks)
                logger.success("Successfully initialized database")
            else:
                logger.warning("No documents found to process.")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

    def reset_database(self, ):
        """Clear the existing database."""
        try:
            if os.path.exists(self.working_dir):
                shutil.rmtree(self.working_dir)
                logger.success(f"Cleared existing database at {self.working_dir}")
        except Exception as e:
            logger.error(f"Error clearing database: {e}")
            raise e

    def query_database(self, query_text: str) -> dict[str, str]:
        """Query the database for similar documents and generate a response."""
        try:
            db = self._load_db()

            results = db.similarity_search_with_score(
                query_text, k=RAG_CONFIG['number_of_contexts'])

            if not results:
                logger.warning("No relevant documents found.")
                return dict()
                raise Exception("No relevant documents found.")

            # sort results by score
            results.sort(key=lambda result: result[1], reverse=True)

            return dict([
                (doc.metadata["id"], doc.page_content)
                for doc, score in results if doc.metadata.get("id", None)
            ])
        except Exception as e:
            logger.error(f"Error querying database: {e}")
            raise e

    def _load_db(self, ) -> Chroma:
        return Chroma(
            persist_directory=self.working_dir,
            embedding_function=get_embedding_function()
        )

    def _backup_chroma_db(self, ):
        # Make sure the backup path exists
        os.makedirs(self.backup_dir, exist_ok=True)
        # Copy the entire directory tree to the backup location
        shutil.copytree(self.working_dir, self.backup_dir, dirs_exist_ok=True)

    def _restore_chroma_db(self, ):
        # Make sure the original chroma path exists
        os.makedirs(self.working_dir, exist_ok=True)
        # Copy the backup directory back to the original chroma path
        shutil.copytree(self.backup_dir, self.working_dir, dirs_exist_ok=True)

    def _embed_chunks(self, chunks: list[Document]):
        """Save chunked documents to the Chroma database."""
        try:
            db = self._load_db()

            chunks_with_ids = assign_chunk_ids(chunks)

            existing_ids = set(db.get(include=[])["ids"])
            logger.info(f"Existing IDs: {len(existing_ids)}")
            # print(list(existing_ids)[0:10])
            # print([chunk.metadata["id"] for chunk in chunks_with_ids])
            new_chunks = [
                chunk
                for chunk in chunks_with_ids
                if chunk.metadata["id"] not in existing_ids
            ]
            logger.info(f"Skipping existing chunks: {len(chunks_with_ids) - len(new_chunks)}")
            if new_chunks:
                logger.info(
                    f"👉 Adding {len(new_chunks)} new documents to the database."
                )
                new_chunk_batches = split_array(new_chunks, chunk_size=10)
                for batch in tqdm(new_chunk_batches):
                    batch_chunk_ids = [chunk.metadata["id"] for chunk in batch]
                    db.add_documents(batch, ids=batch_chunk_ids)
                    self._backup_chroma_db()
                    db = self._load_db()
                logger.success(
                    f"👉 Added {len(new_chunks)} new documents to the database.")
            else:
                logger.success("No new documents to add.")
        except Exception as e:
            logger.error(f"Error saving documents to Chroma: {e}")
            raise e
