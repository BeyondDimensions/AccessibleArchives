import os
import shutil
from langchain_community.document_loaders import DirectoryLoader
from langchain_chroma import Chroma
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain.schema.document import Document

CHROMA_PATH = "chroma"
DATA_PATH = "data/transcripts/markdown/dutschke"


def initialize_database(reset=False):
    if reset or not os.path.exists(CHROMA_PATH):
        print("✨ Initializing Database")
        clear_database()
        documents = load_documents()
        chunks = split_documents(documents)
        save_chunks_to_chroma(chunks)


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    return loader.load()


def save_chunks_to_chroma(chunks: list[Document]):
    db = Chroma(persist_directory=CHROMA_PATH,
                embedding_function=get_embedding_function())
    chunks_with_ids = assign_chunk_ids(chunks)

    existing_ids = {item["id"] for item in db.get(include=[])}
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = [
        chunk for chunk in chunks_with_ids if chunk.metadata["id"] not in existing_ids]

    if new_chunks:
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")


def get_embedding_function():
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    return embeddings


def split_documents(documents: list[Document]):
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks


def assign_chunk_ids(chunks):
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
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

    return chunks
