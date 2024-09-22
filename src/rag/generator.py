from langchain.prompts import ChatPromptTemplate
from database import initialize_database

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def generate_response(query_text: str):
    initialize_database()  # Ensure the database is initialized
    from retriever import query_database
    response_text, sources = query_database(query_text)
    return response_text, sources


def format_prompt(context_text: str, question: str):
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    return prompt_template.format(context=context_text, question=question)
