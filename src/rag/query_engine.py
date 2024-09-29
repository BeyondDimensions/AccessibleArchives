from utils import logger
from utils import CHROMA_PATH
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from .database import initialize_database
from .common import get_embedding_function

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def generate_response(query_text: str):
    """Generate a response using retrieved documents."""
    try:
        initialize_database()  # Ensure the database is initialized
        response_text, sources = query_database(query_text)
        return response_text, sources
    except Exception as e:
        logger.error(f"Failed to generate response: {e}")
        raise e


def format_prompt(context_text: str, question: str):
    """Format the prompt with the given context and question."""
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    return prompt_template.format(context=context_text, question=question)


def query_database(query_text: str):
    """Query the database for similar documents and generate a response."""
    try:
        db = Chroma(persist_directory=CHROMA_PATH,
                    embedding_function=get_embedding_function())

        results = db.similarity_search_with_score(query_text, k=5)

        if not results:
            logger.warning("No relative documents found.")
            raise Exception("No relative documents found.")

        context_text = "\n\n---\n\n".join(
            doc.page_content for doc, _score in results)
        prompt = format_prompt(context_text, query_text)

        model = Ollama(model="llama3.1:8b")
        response_text = model.invoke(prompt)

        sources = [doc.metadata.get("id", None) for doc, _score in results]
        return response_text, sources
    except Exception as e:
        logger.error(f"Error querying database: {e}")
        raise e
