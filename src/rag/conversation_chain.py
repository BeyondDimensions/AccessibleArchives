from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.llms.ollama import Ollama
from config import DEFAULT_LLM_MODEL
from utils import logger
import streamlit as st
# Chat prompt for LangChain conversation

from config.rag_config import DB_QUERY_GEN_PROMPT, PROMPT_WRAPPER, PROMPT_SOURCES_WRAPPER


def initialise_conversation_chain(llm_model=DEFAULT_LLM_MODEL,):
    """Create a conversation chain with memory."""
    logger.info("Creating conversation chain...")
    memory = ConversationBufferMemory(
        memory_key="history", input_key="input", output_key="response"
    )
    prompt_template = ChatPromptTemplate.from_template(PROMPT_WRAPPER)

    # Initialize the conversation chain with the prompt and memory
    chain = ConversationChain(
        llm=Ollama(model=llm_model),
        prompt=prompt_template,
        memory=memory,
        verbose=True
    )
    st.session_state["conversation_chain"] = chain


def get_conversation_chain():
    if "conversation_chain" not in st.session_state:
        initialise_conversation_chain()
    return st.session_state["conversation_chain"]


def get_conversation_sources_chain(memory, context_text, llm_model=DEFAULT_LLM_MODEL):
    prompt_template = ChatPromptTemplate.from_template(
        PROMPT_SOURCES_WRAPPER.replace("{relevant_documents}", context_text))
    return ConversationChain(
        llm=Ollama(model=llm_model),
        prompt=prompt_template,
        memory=memory.copy(),
        verbose=True
    )


def get_query_chain(memory, llm_model=DEFAULT_LLM_MODEL):
    prompt_template = ChatPromptTemplate.from_template(DB_QUERY_GEN_PROMPT)
    return ConversationChain(
        llm=Ollama(model=llm_model),
        prompt=prompt_template,
        memory=memory.copy(),
        verbose=True
    )
