import streamlit as st
from rag import generate_response
from rag.database import DocsEmbedding
from config import TEMP_MODELS, OPENAI_API_KEY
from utils import logger
from . import state_data


def update_model(model_name):
    """Update the model and clear messages if changed."""
    if 'previous_model' not in st.session_state:
        st.session_state.previous_model = model_name
    if st.session_state.previous_model != model_name:
        st.session_state.messages = []  # Clear messages
        st.session_state.previous_model = model_name  # Update the model

    # TODO it should initialize the conversation chain


def display_sources(message: dict):
    if "sources" in message:
        for source in message["sources"]:
            st.markdown(source)


def chat_view():
    if 'llm-recommended-pdf' not in st.session_state:
        st.session_state["llm-recommended-pdf"] = ""
    
    with st.container(height=800, border=False):
        
        label_col, selector_col, = st.columns([1, 3])

        # Model selector
        with label_col:
            label = state_data.get_language_config().gui_text.LLM_MODEL

            st.html(f'<b style="font-size: 2em">{label}</b>')
        with selector_col:
            label = state_data.get_language_config().gui_text.SELECT_LLM_MODEL

            model_name = st.selectbox(
                label,
                list(TEMP_MODELS.keys()),
                label_visibility="collapsed"
            )

        update_model(model_name)
        
        
        
        
        # Containers for input and output
        output_container = st.container(height=505, border=False)
        input_container = st.container(height=50, border=False)

        openai_api_key_valid = True  # Flag to check API key validity

        with input_container:
            # Check if API key is missing for ChatGPT
            if model_name == 'ChatGPT' and not OPENAI_API_KEY:
                openai_api_key_valid = False
                prompt = None  # Set prompt to None to skip execution
            else:
                label = state_data.get_language_config().gui_text.PROMPT_BOX

                prompt = st.chat_input(label)

        with output_container:
            if not openai_api_key_valid:
                logger.warning(
                    "OPENAI_API_KEY is not set. You cannot use ChatGPT without it.", True)
                return  # Stop further execution if API key is invalid

            # Initialize session state variables if they don't exist
            if 'messages' not in st.session_state:
                st.session_state.messages = state_data.get_language_config(
                ).chat_config.INITIAL_CHAT_HISTORY
                st.session_state.messages = []

            # Display chat messages
            for message in st.session_state.messages:
                st.chat_message(message['role']).markdown(message['content'])
                display_sources(message)

            if prompt:
                # Add user message to chat
                st.chat_message(
                    state_data.get_language_config().chat_config.USER_NAME
                ).markdown(prompt)
                st.session_state.messages.append({
                    'role': state_data.get_language_config().chat_config.USER_NAME,
                    'content': prompt
                })

                with st.chat_message(
                    state_data.get_language_config().chat_config.AI_NAME
                ):
                    response_placeholder = st.empty()

                    # Handle commands like /reset_db or /load_files
                    if prompt == "/reset_db":
                        st.session_state["current_doc_embeddings"].reset_database(
                        )
                        return
                    if prompt == "/load_files":
                        st.session_state["current_doc_embeddings"].initialize_database(
                            load_files=True
                        )
                        return

                    # Generate the response
                    with st.spinner("Generating response..."):
                        try:
                            response, sources = generate_response(
                                model_name,
                                prompt,
                                st.session_state.messages,
                                st.session_state["current_doc_collection"],
                                st.session_state["current_doc_embeddings"],
                                state_data.get_language_config().chat_config
                            )
                            message = {
                                'role': state_data.get_language_config().chat_config.AI_NAME,
                                'content': response,
                                'sources': sources
                            }
                            st.session_state.messages.append(message)
                            response_placeholder.markdown(response)
                            display_sources(message)
                            st.session_state["llm-recommended-pdf"] = sources[0]
                        except Exception as e:
                            logger.error(str(e))
