from utils import logger
from config import CHROMA_PATH
from config import RAG_CONFIG
from config import SOURCE_DOC_FORMATTING
from langchain_chroma import Chroma
from .database import initialize_database, reset_database
from .common import get_embedding_function
from .conversation_chain import get_conversation_chain, get_query_chain, get_conversation_sources_chain


def generate_response(query_text: str):
    """Generate a response using retrieved documents."""
    try:
        # Ensure the database is initialized
        if query_text == "/reset_db":
            reset_database()
            return
        # initialize_database(get_known_docs()[0].transcripts_dir)

        # Create the conversation chain
        conversation_chain = get_conversation_chain()

        query_chain = get_query_chain(conversation_chain.memory.copy())

        database_query = query_chain.run(
            input=f"{query_text}")
        logger.info(f"Database query: {database_query}")
        logger.info("Querying database...")
        # Retrieve relevant documents
        context_text, sources = query_database(database_query)
        logger.success("Queried database.")

        # TODO
        # st.session_state["history"]

        if sources:  # if we found relevant documents:
            formatted_sources = "\n".join([
                SOURCE_DOC_FORMATTING.replace(
                    "{id}", id).replace("{text}", text)
                for id, text in list(sources.items())
            ])

            # Use conversation chain to generate a final response, adding the new user query and context
            response = get_conversation_sources_chain(
                conversation_chain.memory, context_text).run(query_text)
        else:   # we found no relevant documents
            response = conversation_chain.run(input=f"{query_text}")
        logger.success(f"Got final response: {response}")
        return response, sources
    except Exception as e:
        logger.error(f"Failed to generate response: {e}")
        raise e


def query_database(query_text: str) -> tuple[str | None, list[str] | None]:
    """Query the database for similar documents and generate a response."""
    try:
        db = Chroma(persist_directory=CHROMA_PATH,
                    embedding_function=get_embedding_function())

        results = db.similarity_search_with_score(
            query_text, k=RAG_CONFIG['number_of_contexts'])

        if not results:
            logger.warning("No relative documents found.")
            return None, None
            raise Exception("No relative documents found.")

        context_text = "\n\n---\n\n".join(
            doc.page_content for doc, _score in results)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        return context_text, sources  # You can keep this if needed elsewhere
    except Exception as e:
        logger.error(f"Error querying database: {e}")
        raise e
