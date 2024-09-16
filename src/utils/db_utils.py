import os
import shutil
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
# from config.config import MARKDOWN_FOLDER

CHROMA_PATH = "chroma"
DATA_PATH = "data/transcripts/markdown/dutschke"
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def initialize_database(reset=False):
    if reset or not os.path.exists(CHROMA_PATH):
        print("✨ Initializing Database")
        clear_database()
        documents = load_documents()
        chunks = split_text(documents)
        save_to_chroma(chunks)


def save_to_chroma(chunks: list[Document]):
    db = Chroma(persist_directory=CHROMA_PATH,
                embedding_function=get_embedding_function())
    chunks_with_ids = calculate_chunk_ids(chunks)

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("✅ No new documents to add")


def query_database(query_text: str):
    # initialize_database()  # Ensure the database is initialized before querying

    # Step 1: Query the database
    db = Chroma(persist_directory=CHROMA_PATH,
                embedding_function=get_embedding_function())
    results = db.similarity_search_with_score(query_text, k=5)

    # Step 2: Prepare the context from the results
    context_text = "\n\n---\n\n".join(
        [doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Step 3: Generate the response using the language model
    model = Ollama(model="qwen2:7b")
    response_text = model.invoke(prompt)

    # Step 4: Extract source information
    sources = [doc.metadata.get("id", None) for doc, _score in results]

    return response_text, sources


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


def load_documents():
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents


def get_embedding_function():
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    return embeddings


def split_text(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=100,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks


def calculate_chunk_ids(chunks):
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
