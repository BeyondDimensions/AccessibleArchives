from langchain_chroma import Chroma
from langchain_community.llms.ollama import Ollama
from generator import format_prompt
from database import CHROMA_PATH, get_embedding_function


def query_database(query_text: str):
    db = Chroma(persist_directory=CHROMA_PATH,
                embedding_function=get_embedding_function())
    results = db.similarity_search_with_score(query_text, k=5)

    context_text = "\n\n---\n\n".join(doc.page_content for doc,
                                      _score in results)
    prompt = format_prompt(context_text, query_text)

    model = Ollama(model="qwen2:7b")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]

    return response_text, sources
