from config.rag_config import DB_QUERY_GEN_PROMPT, PROMPT_WRAPPER, PROMPT_SOURCES_WRAPPER, HISTORY_MESSAGE_FORMATTING, SOURCES_FORMATTING
from utils import logger
from config import SOURCE_DOC_FORMATTING
from storage import DocumentCollection, Page

from llm import prompt_llm
from .database import DocsEmbedding


def flatten(xss):
    return [x for xs in xss for x in xs]


def format_history(history: list[dict[str, str]]) -> str:
    formatted_history = ""
    for message in history:
        content = "\n    ".join([""]+[line.strip("\n") for line in message["content"].split("\n")])
        formatted_sources = ""
        if "sources" in message:
            formatted_sources = SOURCES_FORMATTING.replace(
                "{sources}",
                "\n- ".join([""]+[str(source) for source in message["sources"]])
            )
        formatted_history += HISTORY_MESSAGE_FORMATTING.replace(
            "{sources}", formatted_sources
        ).replace(
            "{role}", message["role"]
        ).replace(
            "{content}", content
        )
    return formatted_history


def generate_response(
        llm_name: str,
        prompt: str,
        history: list[dict[str, str]],
        docs_clxn: DocumentCollection,
        docs_embedding: DocsEmbedding
):
    """Generate a response using retrieved documents."""
    try:
        # Create the conversation chain
        formatted_history = format_history(history)
        db_query_prompt = DB_QUERY_GEN_PROMPT.replace(
            "{history}", formatted_history
        ).replace(
            "{input}", prompt
        )
        logger.info(f"Generating DB-Query: {db_query_prompt}")
        database_query = prompt_llm(db_query_prompt, llm_name)
        logger.info(f"Database query: {database_query}")
        logger.info("Querying database...")
        # Retrieve relevant documents
        sources = docs_embedding.query_database(database_query)
        logger.success("Queried database.")

        # TODO
        # st.session_state["history"]

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

                if ipfs_id in source_files:
                    continue
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
                source_files.update({
                    ipfs_id: full_text
                })

            formatted_sources = "\n".join([
                SOURCE_DOC_FORMATTING.replace(
                    "{id}", id).replace("{text}", text)
                for id, text in list(source_files.items())
            ])

            llm_prompt = PROMPT_SOURCES_WRAPPER.replace(
                "{relevant_documents}", formatted_sources
            ).replace(
                "{history}", formatted_history
            ).replace(
                "{input}", prompt
            )
            source_ids = list(source_files.keys())
        else:   # we found no relevant documents
            llm_prompt = PROMPT_WRAPPER.replace(
                "{history}", formatted_history
            ).replace(
                "{input}", prompt
            )
            source_ids = []
        logger.info(f"Generating final response: {llm_prompt}")

        response = prompt_llm(llm_prompt, llm_name)
        logger.success(f"Got final response: {response}")
        return response, source_ids
    except Exception as e:
        logger.error(f"Failed to generate response: {e}")
        raise e
