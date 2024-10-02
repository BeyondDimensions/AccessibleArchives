from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_community.llms.ollama import Ollama

# Chat prompt for LangChain conversation
CHAIN_PROMPT_TEMPLATE = """
Given the following conversation history and current user input, generate a helpful response using the context of provided documents:

Conversation history: {history}

Current question: {input}

If the history contains sufficient information, respond to the question. Otherwise, ask follow-up questions or provide additional information based on document knowledge.
"""


def create_conversation_chain(llm_model="qwen2:7b", memory_key="history"):
    """Create a conversation chain with memory."""
    memory = ConversationBufferMemory(
        memory_key=memory_key, input_key="input", output_key="response"
    )
    prompt_template = ChatPromptTemplate.from_template(CHAIN_PROMPT_TEMPLATE)

    # Initialize the conversation chain with the prompt and memory
    chain = ConversationChain(
        llm=Ollama(model=llm_model),
        prompt=prompt_template,
        memory=memory,
        verbose=True
    )
    return chain
