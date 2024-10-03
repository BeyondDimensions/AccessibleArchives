from utils import logger
from config import CHROMA_WORKING_PATH
from config import RAG_CONFIG
from config.rag_config import SOURCE_DOC_FORMATTING
from langchain_chroma import Chroma
from .common import get_embedding_function
from .conversation_chain import get_conversation_chain, get_query_chain, get_conversation_sources_chain
from storage import DocumentCollection, Page


def flatten(xss):
    return [x for xs in xss for x in xs]


def generate_response(query_text: str, docs_clxn: DocumentCollection):
    """Generate a response using retrieved documents."""
    try:

        # Create the conversation chain
        conversation_chain = get_conversation_chain()

        query_chain = get_query_chain(conversation_chain.memory.copy())

        database_query = query_chain.run(
            input=f"{query_text}")
        logger.info(f"Database query: {database_query}")
        logger.info("Querying database...")
        # Retrieve relevant documents
        sources = query_database(database_query)
        logger.success("Queried database.")

        if sources:  # if we found relevant documents:
            source_files: dict[str, str] = {}
            most_relevant_source: Page | None = None
            for id, text in list(sources.items()):
                _ipfs_id = [
                    s for s in flatten([
                        seg.split(".") for seg in flatten([
                            segment.split("/") for segment in id.split(":")
                        ])
                    ]) if s.startswith("Qm")
                ]
                if not _ipfs_id:
                    logger.error(f"Couldn't extract IPFS ID from {id}")
                    continue
                else:
                    ipfs_id = _ipfs_id[0]
                try:
                    page = docs_clxn.get_page(ipfs_id)
                    full_text = page.transcripts[0].get_text()
                    if not most_relevant_source:
                        most_relevant_source = page
                except ValueError:  # page isn't in our document collection
                    logger.error(
                        "Retrieved a page from ChromaDB which isn't in our "
                        f"document collection: {ipfs_id}")
                    full_text = text
                    continue
                if ipfs_id not in source_files:
                    source_files.update({
                        ipfs_id: full_text
                    })

            formatted_sources = "\n".join([
                SOURCE_DOC_FORMATTING.replace(
                    "{id}", id).replace("{text}", text)
                for id, text in list(source_files.items())
            ])

            # Use conversation chain to generate a final response, adding the new user query and context
            response = get_conversation_sources_chain(
                conversation_chain.memory, formatted_sources).run(query_text)
        else:   # we found no relevant documents
            response = conversation_chain.run(input=f"{query_text}")
        logger.success(f"Got final response: {response}")
        return response, sources
    except Exception as e:
        logger.error(f"Failed to generate response: {e}")
        raise e


def query_database(query_text: str) -> dict[str, str] | None:
    """Query the database for similar documents and generate a response."""
    try:
        db = Chroma(persist_directory=CHROMA_WORKING_PATH,
                    embedding_function=get_embedding_function())

        results = db.similarity_search_with_score(
            query_text, k=RAG_CONFIG['number_of_contexts'])

        if not results:
            logger.warning("No relevant documents found.")
            return None
            raise Exception("No relevant documents found.")

        # sort results by score
        results.sort(key=lambda result: result[1], reverse=True)

        return dict([
            (doc.metadata["id"], doc.page_content)
            for doc, score in results if doc.metadata.get("id", None)
        ])

        context_text = "\n\n---\n\n".join(
            doc.page_content for doc, _score in results)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        return context_text, sources  # You can keep this if needed elsewhere
    except Exception as e:
        logger.error(f"Error querying database: {e}")
        raise e
