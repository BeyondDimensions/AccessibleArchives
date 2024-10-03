import streamlit as st
from rag import generate_response
from rag.database import initialize_database, reset_database
from config import TEMP_MODELS


def update_model(model_name):
    """Update the model and clear messages if changed."""
    if 'previous_model' not in st.session_state:
        st.session_state.previous_model = model_name
    if st.session_state.previous_model != model_name:
        st.session_state.messages = []  # Clear messages
        st.session_state.previous_model = model_name  # Update the model

    # TODO it should initialize the conversation chain


def chat_view():
    with st.container(height=900, border=False):
        st.markdown(
            "<h4 style='text-align: center;'>Select a model</h4>", unsafe_allow_html=True)
        # st.header("Ask me a question!")

        # Model selection
        model_name = st.selectbox('Select Model', list(
            TEMP_MODELS.keys()), label_visibility="collapsed")

        update_model(model_name)

        # Input for the prompt
        output_container = st.container(height=705, border=False)
        input_container = st.container(height=50, border=False)

        with input_container:
            prompt = st.chat_input('Pass your prompt here')
        with output_container:
            # Initialize session state variables if they don't exist
            if 'messages' not in st.session_state:
                st.session_state.messages = []
            # Display chat messages
            for message in st.session_state.messages:
                st.chat_message(message['role']).markdown(message['content'])

            if prompt:
                st.chat_message('user').markdown(prompt)
                st.session_state.messages.append(
                    {'role': 'user', 'content': prompt})

                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    if prompt == "/reset_db":
                        reset_database()
                        return
                    if prompt == "/load_files":
                        initialize_database(
                            st.session_state["current_doc_collection"].transcripts_dir, load_files=True)
                        return
                    # Generate the response
                    with st.spinner("Generating response..."):
                        response, sources = generate_response(prompt)
                        response_text = response + \
                            "\n\nSources:\n" + "\n".join(sources)
                        response_placeholder.markdown(response_text)
                        st.session_state.messages.append(
                            {'role': 'assistant', 'content': response_text})
