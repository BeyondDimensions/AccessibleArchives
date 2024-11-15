from config.language_templates.chat_config import ChatConfigTemplate
from config.language_templates.gui_text import GuiTextTemplate

class ChatConfigImplementation(ChatConfigTemplate):

    AI_NAME = "Librarian"
    USER_NAME = "Historian"
    INITIAL_CHAT_HISTORY = [
        {
            "role": "Librarian",
            "content": "Mein lieber freund, Hallo! Wie kann ich dir heute helfen?"
        },
        {
            "role": "Historian",
            "content": "Morgen! Ich habe mit einem neuen Rechercheprojekt übers 20. Jahrhundert angefangen. Ich würde gerne ein paar Dokumente aus dem Archiv durchsuchen."
        },
        {
            "role": "Librarian",
            "content": "Sehr gut! Das war ein spannendes Zeitalter. Ich kenne alle Dokumente die es dazu im Archiv gibt. Was interessiert dich denn?"
        },
    ]

    PROMPT_WRAPPER = """
    Für das folgende Gespräch, gebe zur aktuellen Frage eine hilfreiche Antwort.

    Gespräch: {history}

    Aktuelle Frage: {input}
    """

    PROMPT_SOURCES_WRAPPER = """
    Wir sind im Jahr 3000.
    Du hast einige sehr alte geschichtliche Dokumente aus dem 20. Jahrhundert, die
    für unseren geschichtlichen Recherchen relavant sind.
    Hier sind diese uralte Dokumente:

    ---

    {relevant_documents}

    ---

    Wir haben schon ein bisschen miteinander geredet, erinnerst du dich?

    Gespräch: {history}

    Aktuelle Frage: {input}

    Für die aktuelle Frage, die sich auf uralte Vorfällen von vor mehr wie tausend
    Jahren bezieht, formuliere eine hilfreiche Antwort.
    """

    DB_QUERY_GEN_PROMPT = """
    Gesprächshistorie:
    {history}

    Aktuelle Frage: {input}

    Formuliere genau, wonach man suchen muss, um diese Frage zu beantworten.
    """

    SOURCE_DOC_FORMATTING = """
    {id}
    ```markdown
    {text}
    ```
    """
    SOURCES_FORMATTING = """
    Hier sind die relevanteste Dokumente:
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
