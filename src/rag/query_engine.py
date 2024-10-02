from utils import logger
from config import CHROMA_PATH
from config import RAG_CONFIG
from langchain_chroma import Chroma
from .database import initialize_database
from .common import get_embedding_function
from .conversation_chain import create_conversation_chain


def generate_response(query_text: str):
    """Generate a response using retrieved documents."""
    try:
        # Ensure the database is initialized
        initialize_database()

        # Create the conversation chain
        conversation_chain = create_conversation_chain()

        # Retrieve relevant documents
        context_text, sources = query_database(query_text)

        # Use conversation chain to generate a final response, adding the new user query and context
        response = conversation_chain.run(
            input=f"{context_text}\n\n{query_text}")

        return response, sources
    except Exception as e:
        logger.error(f"Failed to generate response: {e}")
        raise e


def query_database(query_text: str):
    """Query the database for similar documents and generate a response."""
    try:
        db = Chroma(persist_directory=CHROMA_PATH,
                    embedding_function=get_embedding_function())

        results = db.similarity_search_with_score(
            query_text, k=RAG_CONFIG['number_of_contexts'])

        if not results:
            logger.warning("No relative documents found.")
            raise Exception("No relative documents found.")

        context_text = "\n\n---\n\n".join(
            doc.page_content for doc, _score in results)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        return context_text, sources  # You can keep this if needed elsewhere
    except Exception as e:
        logger.error(f"Error querying database: {e}")
        raise e
