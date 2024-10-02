import streamlit as st
from rag import generate_response


def chat_view():
    with st.container(height=850, border=False):
        st.markdown(
            "<h3 style='text-align: center;'>Ask me a question!</h3>", unsafe_allow_html=True)
        # st.header("Ask me a question!")

        # Model selection
        # model_name = st.selectbox('Select Model', list(LLM_MODELS.keys()))
        # # Initialize session state variables if they don't exist
        # if 'messages' not in st.session_state:
        #     st.session_state.messages = []
        # if 'previous_model' not in st.session_state:
        #     st.session_state.previous_model = model_name
        #
        # # Clear messages if the selected model has changed
        # if st.session_state.previous_model != model_name:
        #     st.session_state.messages = []
        #     st.session_state.previous_model = model_name

        # Input for the prompt
        output_container = st.container(height=725, border=False)
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

                    # Generate the response
                    with st.spinner("Generating response..."):
                        response, sources = generate_response(prompt)
                        response_text = response + \
                            "\n\nSources:\n" + "\n".join(sources)
                        response_placeholder.markdown(response_text)
                        st.session_state.messages.append(
                            {'role': 'assistant', 'content': response_text})
