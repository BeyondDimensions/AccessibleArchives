from langchain_community.embeddings.ollama import OllamaEmbeddings
# from langchain.embeddings import HuggingFaceInstructEmbeddings
from utils import logger


def get_embedding_function():
    """Return the embedding function."""
    try:
        # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
        embeddings = OllamaEmbeddings(model="mxbai-embed-large")
        return embeddings
    except Exception as e:
        logger.error(f"Error initializing embedding function: {e}")
        raise e
