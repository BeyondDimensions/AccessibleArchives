from config.language_templates.chat_config import ChatConfigTemplate
from config.language_templates.gui_text import GuiTextTemplate

class ChatConfigImplementation(ChatConfigTemplate):

    AI_NAME = "Librarian"
    USER_NAME = "Historian"
    INITIAL_CHAT_HISTORY = [
        {
            "role": "Librarian",
            "content": "My dear friend, hello! How can I help you today?"
        },
        {
            "role": "Historian",
            "content": "Good morning! I’ve started a new research project about the 20th century. I’d like to browse some documents from the archive."
        },
        {
            "role": "Librarian",
            "content": "Very good! That was an exciting era. I know all the documents that are available in the archive about it. What specifically interests you?"
        },
    ]

    PROMPT_WRAPPER = """
    For the following conversation, provide a helpful answer to the current question.

    Conversation: {history}

    Current question: {input}
    """

    PROMPT_SOURCES_WRAPPER = """
    We are in the year 3000.
    You have some very old historical documents from the 20th century that
    are relevant to our historical research.
    Here are these ancient documents:

    ---

    {relevant_documents}

    ---

    We’ve already talked a bit, do you remember?

    Conversation: {history}

    Current question: {input}

    For the current question, which refers to ancient events more than a thousand
    years ago, formulate a helpful answer.
    """

    DB_QUERY_GEN_PROMPT = """
    Conversation history:
    {history}

    Current question: {input}

    Precisely formulate what to search for in order to answer this question.
    """

    SOURCE_DOC_FORMATTING = """
    {id}
    ```markdown
    {text}
    ```
    """
    SOURCES_FORMATTING = """
    Here are the most relevant documents:
    {sources}
    """

    HISTORY_MESSAGE_FORMATTING = """{role}: {content}
    {sources}
    """

class GuiTextImplementation(GuiTextTemplate):
    DOCUMENT_COLLECTION="Document Collection"
    LLM_MODEL="LLM Model"
    DOCUMENT="Document"
    SELECT_DOC_COLXN="Select Document Collection"
    SELECT_DOCUMENT="Select Document"
    SELECT_LLM_MODEL="Choose an LLM"
    PROMPT_BOX="Write your prompt here"
    DOWNLOAD_DOCUMENT="download PDF"
    PAGE="page"
    PAGES="pages"
    LAST_PAGE="last"
    NEXT_PAGE="next"

language_code="en-gb"
language_icon="🇬🇧"
