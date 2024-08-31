import os
import fitz  # PyMuPDF for PDF to image conversion
import json
import shutil
import base64
import tempfile
import subprocess
import streamlit as st
from openai import OpenAI
from config.config import OPENAI_API_KEY, ORIGINAL_FOLDER, TEMP_FOLDER
from config.config import TRANSCRIPTS_FOLDER

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def ensure_directories_exist(*dirs):
    """Ensure that all directories in the list exist."""
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)


def convert_pdf_to_images(pdf_path):
    """Convert each page of a PDF to an image using fitz (PyMuPDF) and return a list of image paths."""
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    temp_folder = os.path.join(TEMP_FOLDER, pdf_name)
    ensure_directories_exist(temp_folder)

    doc = fitz.open(pdf_path)
    image_paths = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load a page from the PDF
        pix = page.get_pixmap()  # Render page to an image
        image_path = os.path.join(temp_folder, f"page_{page_num + 1}.jpg")
        pix.save(image_path)  # Save the image to the output folder
        image_paths.append(image_path)

    return image_paths, temp_folder


def get_pdf_input_from_user(input_option):
    """Handle PDF input based on user selection."""
    if input_option == 'Folder of PDFs':
        folder_path = st.text_input("Enter the folder path containing PDFs:")
        if not os.path.isdir(folder_path):
            st.warning("Invalid folder path.")
            return None, None

        pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        if not pdf_files:
            st.warning("No PDF files found in the specified folder.")
            return None, None

        return folder_path, pdf_files
    else:
        uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
        if uploaded_file is not None:
            ensure_directories_exist(ORIGINAL_FOLDER)
            pdf_path = os.path.join(ORIGINAL_FOLDER, uploaded_file.name)
            with open(pdf_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            return ORIGINAL_FOLDER, [uploaded_file.name]
        else:
            st.warning("Please upload a PDF file.")
            return None, None


def load_transcription_log():
    """Load the transcription log from a JSON file."""
    log_path = os.path.join(TRANSCRIPTS_FOLDER, 'transcription_log.json')
    if os.path.exists(log_path):
        with open(log_path, 'r') as log_file:
            return json.load(log_file)
    return {}


def save_transcription_log(log):
    """Save the transcription log to a JSON file."""
    log_path = os.path.join(TRANSCRIPTS_FOLDER, 'transcription_log.json')
    with open(log_path, 'w') as log_file:
        json.dump(log, log_file, indent=4)


def update_transcription_log(log, pdf_name, page_key, success):
    """Update the transcription log with the status of each page."""
    if pdf_name not in log:
        log[pdf_name] = {}
    log[pdf_name][page_key] = success
    save_transcription_log(log)


def extract_markdown_from_response(response_content):
    """Extract markdown content from the GPT model response."""
    start_idx = response_content.find("```markdown")
    if start_idx != -1:
        start_idx += len("```markdown")
        end_idx = response_content.find("```", start_idx)
        if end_idx != -1:
            return response_content[start_idx:end_idx].strip()
        else:
            return response_content[start_idx:].strip()
    else:
        return response_content.strip()


def generate_transcripts_from_images(images, pdf_name, gpt_version, log, temp_folder):
    """Process images using the GPT model and save the results."""
    if images:
        all_pages_processed = True  # Assume all pages will be processed

        # Ensure directory exists for Markdown files
        markdown_folder = os.path.join(
            TRANSCRIPTS_FOLDER, 'markdown', pdf_name)
        ensure_directories_exist(markdown_folder)

        for idx, image_path in enumerate(images):
            page_key = f"page_{idx + 1}"
            page_status = log.get(pdf_name, {}).get(page_key, None)

            # Check if the page is marked as false (need reprocessing) or not processed yet
            if page_status is True:
                st.info(f"Skipping page {idx+1} - already processed.")
                continue
            elif page_status is False:
                st.info(f"Reprocessing page {idx+1} - previously failed.")
            else:
                st.info(f"Processing page {idx+1} for the first time.")

            with st.spinner(f"Processing image {idx+1}/{len(images)}..."):
                try:
                    with open(image_path, 'rb') as image_file:
                        image_base64 = base64.b64encode(
                            image_file.read()).decode('utf-8')

                    response = client.chat.completions.create(
                        model=gpt_version,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": (
                                            "Please extract and transcribe all visible text and formatting from the following image and save it into a markdown file. "
                                            "Use appropriate markdown syntax to represent headings, tables, lists, and any other formatting present in the image. "
                                            "If you can not transcribe the image say that I should refer to the original document. Don't comment anything by yourself, "
                                            "just give me the extracted and transcribed text."
                                        )
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{image_base64}"
                                        }
                                    }
                                ]
                            }
                        ]
                    )

                    if response and response.choices:
                        message_content = response.choices[0].message.content
                        markdown_content = extract_markdown_from_response(
                            message_content)

                        md_filename = os.path.join(
                            markdown_folder, f"page_{idx + 1}.md")

                        with open(md_filename, 'w') as file:
                            file.write(markdown_content)

                        st.success(f"Image {idx+1} processed successfully.")
                        update_transcription_log(log, pdf_name, page_key, True)

                    else:
                        st.error(f"Failed to process image {idx+1}.")
                        all_pages_processed = False  # Mark that not all pages were processed
                        update_transcription_log(
                            log, pdf_name, page_key, False)

                except Exception as e:
                    format_and_display_error(e, idx)
                    all_pages_processed = False  # Mark that not all pages were processed
                    update_transcription_log(log, pdf_name, page_key, False)

        # After all images are processed, delete the output folder if all pages were processed
        if all_pages_processed:
            shutil.rmtree(temp_folder)
        else:
            st.error(
                "Some images could not be processed. Temporary files retained for review.")
    else:
        st.warning("No images to process.")


def format_and_display_error(exception, idx):
    """Handle and format errors."""
    if hasattr(exception, 'response') and exception.response and exception.response.text:
        try:
            error_info = json.loads(exception.response.text)
            error_code = error_info.get(
                "error", {}).get("code", "unknown_code")
            error_message = error_info.get("error", {}).get(
                "message", "An unknown error occurred.")
            http_status_code = exception.response.status_code if hasattr(
                exception.response, 'status_code') else 'unknown_status_code'
            formatted_error_message = (
                f"Error Code {http_status_code}: {error_code}\n\n"
                f"Error Message: {error_message}"
            )
        except json.JSONDecodeError:
            formatted_error_message = f"Error: {str(exception)}"
    else:
        formatted_error_message = f"Error: {str(exception)}"

    st.error(f"Error processing image {idx+1}: {formatted_error_message}")


def convert_markdown_to_pdf(markdown_folder, pdf_output_path):
    """Convert all Markdown files in a folder to a single PDF using Pandoc with each file on a separate page."""
    markdown_files = [os.path.join(markdown_folder, f) for f in sorted(
        os.listdir(markdown_folder)) if f.endswith('.md')]

    if not markdown_files:
        st.warning("No Markdown files found to convert.")
        return

    try:
        # Create a temporary file to store the combined Markdown content
        with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as temp_md_file:
            temp_md_path = temp_md_file.name

            with open(temp_md_path, 'w') as outfile:
                for md_file in markdown_files:
                    with open(md_file, 'r') as infile:
                        outfile.write(infile.read())
                        # Add a page break between files
                        outfile.write('\n\n\\newpage\n\n')

        # Build the Pandoc command with margin options
        pandoc_command = [
            'pandoc', '-s', '--pdf-engine=xelatex', '--variable', 'geometry:margin=1in',
            temp_md_path, '-o', pdf_output_path
        ]

        # Execute Pandoc command
        subprocess.run(pandoc_command, check=True)

        st.success(f"PDF generated successfully: {pdf_output_path}")

    except subprocess.CalledProcessError as e:
        st.error(f"Failed to convert Markdown to PDF: {e}")

    finally:
        # Clean up the temporary file
        if temp_md_path and os.path.exists(temp_md_path):
            os.remove(temp_md_path)


def process_and_transcribe_pdf(pdf_path, pdf_name, gpt_version):
    """Convert PDF to images, generate transcripts, and create a PDF from Markdown files."""
    st.write(f"Processing {pdf_name}.pdf...")

    # Load transcription log
    log = load_transcription_log()

    # Convert PDF to images
    images, temp_folder = convert_pdf_to_images(pdf_path)

    # Generate transcripts from the images
    generate_transcripts_from_images(
        images, pdf_name, gpt_version, log, temp_folder)

    # Convert Markdown files to a single PDF
    markdown_folder = os.path.join(TRANSCRIPTS_FOLDER, 'markdown', pdf_name)
    pdf_output_path = os.path.join(
        TRANSCRIPTS_FOLDER, 'pdfs', f"{pdf_name}.pdf")
    ensure_directories_exist(os.path.dirname(pdf_output_path))
    convert_markdown_to_pdf(markdown_folder, pdf_output_path)
