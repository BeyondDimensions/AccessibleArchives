from tqdm import tqdm
from utils import logger
from config import RAG_CONFIG
from langchain.schema.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.text_splitter import CharacterTextSplitter

# def split_documents(documents: list[Document]):
#     """Split loaded documents into chunks."""
#     logger.info(
#         f"Splitting {len(documents)} documents into chunks...")
#     text_splitter = CharacterTextSplitter(
#         separator="\n",
#         chunk_size=RAG_CONFIG['chunk_size'],
#         chunk_overlap=RAG_CONFIG['chunk_overlap'],
#         length_function=len
#     )
#     chunks = text_splitter.split_documents(documents)
#     logger.success(
#     f"Split {len(documents)} documents into {len(chunks)} chunks.")
#     return chunks


def split_documents(documents: list[Document]):
    """Split loaded documents into chunks."""
    logger.info(
        f"Splitting {len(documents)} documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=RAG_CONFIG['chunk_size'],
        chunk_overlap=RAG_CONFIG['chunk_overlap'],
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    logger.success(
        f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks


def assign_chunk_ids(chunks):
    """Assign unique chunk IDs to each document chunk."""
    last_page_id = None
    current_chunk_index = 0

    logger.info(f"Assigning IDs to {len(chunks)} chunks...")
    for chunk in tqdm(chunks):
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

    logger.success(f"Assigned IDs to {len(chunks)} chunks.")
    return chunks
