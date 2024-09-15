import streamlit as st
from utils.db_utils import query_database, initialize_database
from config.config import ALLOWED_VERSIONS

def chat_view():
    st.header("Ask me a question!")

    # Model selection
    # model_name = st.selectbox('Select Model', list(LLM_MODELS.keys()))
    with st.spinner("Initializing database..."):
        try:
            initialize_database()
        except Exception as e:
            st.error(f"Error initializing database: {e}")

    # Initialize session state variables if they don't exist
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    # if 'previous_model' not in st.session_state:
    #     st.session_state.previous_model = model_name

    # Clear messages if the selected model has changed
    # if st.session_state.previous_model != model_name:
    #     st.session_state.messages = []
    #     st.session_state.previous_model = model_name

    # Display chat messages
    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    # Input for the prompt
    prompt = st.chat_input('Pass your prompt here')

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        with st.chat_message("assistant"):
            response_placeholder = st.empty()

            # Generate the response
            with st.spinner("Generating response..."):
                response, sources = query_database(prompt)
                response_text = response + \
                    "\n\nSources:\n" + "\n".join(sources)
                response_placeholder.markdown(response_text)
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': response_text})
