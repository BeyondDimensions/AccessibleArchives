import os
import streamlit as st
from utils.pdf_utils import list_pdfs_in_folder, displayPDF
from utils.model_utils import generate_response
from utils.ocr_utils import ensure_directories_exist
from utils.ocr_utils import get_pdf_input_from_user, process_and_transcribe_pdf
from config.config import MODELS, ALLOWED_VERSIONS, PROCESSED_FOLDER


def chat_interface():
    st.header("Ask me a question!")

    # Model selection
    model_name = st.selectbox('Select Model', list(MODELS.keys()))

    # Initialize session state variables if they don't exist
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    # if 'previous_model' not in st.session_state:
    #     st.session_state.previous_model = model_name
    #
    # # Clear messages if the selected model has changed
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
                response_stream = generate_response(prompt, model_name)
                # Initialize with an empty string to avoid duplication
                current_response = ""
                for response in response_stream:
                    response_placeholder.markdown(response)
                    current_response = response
                # Update the session state with the latest complete response
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': current_response})


def doc_viewer():
    st.header("Document Viewer")

    ensure_directories_exist(PROCESSED_FOLDER)
    pdf_files = list_pdfs_in_folder(PROCESSED_FOLDER)

    if not pdf_files:
        st.write("No PDF files found in the folder.")
    else:
        selected_pdf = st.selectbox('Select a PDF file', pdf_files)

        if selected_pdf:
            pdf_path = os.path.join(PROCESSED_FOLDER, selected_pdf)

            # Create two columns for layout
            col1, col2 = st.columns([4, 1])  # Adjust the ratio as needed

            with col1:
                st.write(f"### Previewing PDF: {selected_pdf}")
                try:
                    displayPDF(pdf_path)
                except Exception as e:
                    st.error(
                        f"An error occurred while displaying the PDF: {e}")

            with col2:
                # Add a button to download the PDF
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_file,
                        file_name=selected_pdf,
                        mime="application/pdf"
                    )


def process_files():
    st.header("OCR Processing")

    # Option to choose a single PDF or a folder
    input_option = st.radio('Input Option', ('Single PDF', 'Folder of PDFs'))

    folder_path, pdf_files = get_pdf_input_from_user(input_option)

    if not folder_path or not pdf_files:
        return

    gpt_version = st.selectbox('Select GPT Version', ALLOWED_VERSIONS)

    # Button to trigger the processing of selected PDFs
    if st.button('Start Processing PDFs'):
        for pdf_file in pdf_files:
            pdf_name = os.path.splitext(pdf_file)[0]
            pdf_path = os.path.join(folder_path, pdf_file)

            # Process the PDF file when the button is clicked
            process_and_transcribe_pdf(pdf_path, pdf_name, gpt_version)


# Main Streamlit app
def main():
    st.title('Lighthouse')

    # Tabs setup
    st.sidebar.title("Navigation")
    tabs = ['Chatbot', 'Document Viewer', 'OCR Processing']
    choice = st.sidebar.selectbox('Select Tab', tabs)

    if choice == 'Chatbot':
        chat_interface()
    elif choice == 'Document Viewer':
        doc_viewer()
    elif choice == 'OCR Processing':
        process_files()


if __name__ == "__main__":
    main()
