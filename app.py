import os
import streamlit as st
from utils.pdf_utils import list_pdfs_in_folder, displayPDF
from utils.model_utils import generate_response
from config import MODELS


def chat_interface():
    st.header("Ask me a question!")

    # Model selection
    model_name = st.selectbox('Select Model', list(MODELS.keys()))

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        st.chat_message(message['role']).markdown(message['content'])

    prompt = st.chat_input('Pass your prompt here')

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        response = generate_response(prompt, model_name)
        st.chat_message('assistant').markdown(response)
        st.session_state.messages.append(
            {'role': 'assistant', 'content': response})


def doc_viewer():
    st.header("Document Viewer")

    # Path to the folder containing PDFs
    pdf_folder = 'data/pdf_files'

    # List PDF files in the folder
    pdf_files = list_pdfs_in_folder(pdf_folder)

    if not pdf_files:
        st.write("No PDF files found in the folder.")
    else:
        selected_pdf = st.selectbox('Select a PDF file', pdf_files)

        if selected_pdf:
            pdf_path = os.path.join(pdf_folder, selected_pdf)
            st.write(f"### Previewing PDF: {selected_pdf}")

            # Display PDF using the defined function
            displayPDF(pdf_path)


# Main Streamlit app
def main():
    st.title('Lighthouse')

    # Tabs setup
    st.sidebar.title("Navigation")
    tabs = ['Chatbot', 'Document Viewer']
    choice = st.sidebar.selectbox('Select Tab', tabs)

    if choice == 'Chatbot':
        chat_interface()
    elif choice == 'Document Viewer':
        doc_viewer()


if __name__ == "__main__":
    main()
