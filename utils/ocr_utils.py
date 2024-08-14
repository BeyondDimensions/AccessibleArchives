import os
import base64
import json
import streamlit as st
from openai import OpenAI
from config import OPENAI_API_KEY

# Define the directories
DATA_FOLDER = 'data'
UPLOAD_FOLDER = os.path.join(DATA_FOLDER, 'uploads')
TRANSCRIPT_FOLDER = os.path.join(DATA_FOLDER, 'transcripts')

# Ensure the directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)

allowed_versions = ['gpt-4o', 'gpt-4o-mini',
                    'gpt-4-turbo', 'gpt-4', 'gpt-3.5-turbo']

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def process_file():
    st.header("OCR")

    upload_option = st.radio(
        'Upload Option', ('Upload New File', 'Choose Existing File'))

    if upload_option == 'Upload New File':
        uploaded_file = st.file_uploader(
            "Choose a file", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            st.success("File uploaded successfully.")
            file_to_process = file_path
        else:
            file_to_process = None
    else:
        existing_files = os.listdir(UPLOAD_FOLDER)
        selected_file = st.selectbox('Select an existing file', existing_files)
        file_to_process = os.path.join(
            UPLOAD_FOLDER, selected_file) if selected_file else None

    if file_to_process:
        gpt_version = st.selectbox('Select GPT Version', allowed_versions)

        with open(file_to_process, 'rb') as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode('utf-8')

        if st.button("Process Image"):
            with st.spinner("Processing image..."):
                try:
                    response = client.chat.completions.create(
                        model=gpt_version,
                        response_format={"type": "json_object"},
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Provide JSON file that represents extracted text from this image."},
                                    {"type": "image_url", "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}"}}
                                ]
                            }
                        ]
                    )

                    if response and response.choices and response.choices[0].message:
                        json_data = json.loads(
                            response.choices[0].message['content'])
                        filename_without_extension = os.path.splitext(
                            os.path.basename(file_to_process))[0]
                        json_filename = os.path.join(
                            TRANSCRIPT_FOLDER, f"{filename_without_extension}.json")

                        with open(json_filename, 'w') as file:
                            json.dump(json_data, file, indent=4)

                        st.success("Image processed successfully.")
                        st.download_button("Download JSON", data=json.dumps(
                            json_data, indent=4), file_name=f"{filename_without_extension}.json", mime="application/json")

                        # Display the extracted text from JSON
                        st.subheader("Extracted Text:")
                        extracted_text = json_data.get(
                            'text', 'No text found.')
                        st.text_area("Extracted Text",
                                     value=extracted_text, height=300)
                    else:
                        st.error("Failed to process the image.")

                except Exception as e:
                    # Handle API error responses
                    if hasattr(e, 'response') and e.response and e.response.text:
                        try:
                            # Extract error information
                            error_info = json.loads(e.response.text)
                            error_code = error_info.get(
                                "error", {}).get("code", "unknown_code")
                            error_message = error_info.get("error", {}).get(
                                "message", "An unknown error occurred.")
                            # Display the HTTP status code if available
                            http_status_code = e.response.status_code if hasattr(
                                e.response, 'status_code') else 'unknown_status_code'
                            formatted_error_message = (
                                f"Error Code {http_status_code}: {error_code}\n\n"
                                f"Error Message: {error_message}"
                            )
                        except json.JSONDecodeError:
                            formatted_error_message = f"Error: {str(e)}"
                    else:
                        formatted_error_message = f"Error: {str(e)}"

                    st.error(formatted_error_message)
