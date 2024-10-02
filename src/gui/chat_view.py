import streamlit as st
from rag import generate_response


def chat_view():
    st.header("Ask me a question!")

    # Model selection
    # model_name = st.selectbox('Select Model', list(LLM_MODELS.keys()))
    # with st.spinner("Initializing database..."):
    #     initialize_database()

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

    response_placeholder = st.empty()
    # Input for the prompt
    prompt = st.chat_input('Pass your prompt here')

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        with st.chat_message("assistant"):

            # Generate the response
            with st.spinner("Generating response..."):
                response, sources = generate_response(prompt)
                if sources:
                    response_text = response + \
                        "\n\nSources:\n" + "\n".join(sources)
                else:
                    response_text = response
                response_placeholder.markdown(response_text)
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': response_text})
