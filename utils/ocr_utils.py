import os
import fitz  # PyMuPDF for PDF to image conversion
import cv2  # OpenCV for image processing
import base64
import json
import streamlit as st
from openai import OpenAI
from config.config import OPENAI_API_KEY, PDFS_FOLDER, IMAGES_FOLDER
from config.config import COMPRESSED_FOLDER, TRANSCRIPTS_FOLDER

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def ensure_directories_exist(*dirs):
    """Ensure that all directories in the list exist."""
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)


def convert_pdf_to_images(pdf_path):
    """Convert each page of a PDF to an image using fitz (PyMuPDF) and return a list of image paths."""
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = os.path.join(IMAGES_FOLDER, pdf_name)
    ensure_directories_exist(output_folder)

    doc = fitz.open(pdf_path)
    image_paths = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)  # Load a page from the PDF
        pix = page.get_pixmap()  # Render page to an image
        image_path = os.path.join(output_folder, f"page_{page_num + 1}.jpg")
        pix.save(image_path)  # Save the image to the output folder
        image_paths.append(image_path)

    return image_paths


def compress_and_convert_image_to_grayscale(image_path):
    """Convert image to grayscale and compress it using OpenCV."""
    pdf_name = os.path.basename(os.path.dirname(image_path))
    compressed_folder = os.path.join(COMPRESSED_FOLDER, pdf_name)
    ensure_directories_exist(compressed_folder)

    compressed_path = os.path.join(
        compressed_folder, os.path.basename(image_path))

    # Load the image with OpenCV
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Compress and save the grayscale image
    cv2.imwrite(compressed_path, gray_img, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

    return compressed_path


def convert_and_preprocess_pdf(pdf_path):
    """Convert PDF to images, preprocess each image, and return the paths of the processed images."""
    # Convert PDF to images
    image_paths = convert_pdf_to_images(pdf_path)

    # Preprocess each image
    processed_image_paths = [compress_and_convert_image_to_grayscale(
        image_path) for image_path in image_paths]

    return processed_image_paths


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
            pdf_path = os.path.join(PDFS_FOLDER, uploaded_file.name)
            with open(pdf_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            return PDFS_FOLDER, [uploaded_file.name]
        else:
            st.warning("Please upload a PDF file.")
            return None, None


def process_single_pdf_file(pdf_path):
    """Process a single PDF file and return the processed image paths."""
    st.write(f"Processing {os.path.basename(pdf_path)}...")
    compressed_images = convert_and_preprocess_pdf(pdf_path)
    return compressed_images


def generate_transcripts_from_images(images, pdf_name, gpt_version):
    """Process images using the GPT model and save the results."""
    if images:
        for idx, image_path in enumerate(images):
            with st.spinner(f"Processing image {idx+1}/{len(images)}..."):
                with open(image_path, 'rb') as image_file:
                    image_base64 = base64.b64encode(
                        image_file.read()).decode('utf-8')

                try:
                    response = client.chat.completions.create(
                        model=gpt_version,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": "Provide a properly aligned markdown transcript containing everything visible in the image."},
                                    {"type": "image_url", "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}"}}
                                ]
                            }
                        ]
                    )

                    if response and response.choices:
                        message_content = response.choices[0].message.content
                        md_filename = os.path.join(
                            TRANSCRIPTS_FOLDER, pdf_name, f"page_{idx + 1}.md")

                        ensure_directories_exist(
                            os.path.join(TRANSCRIPTS_FOLDER, pdf_name))
                        with open(md_filename, 'w') as file:
                            file.write(message_content)

                        st.success(
                            f"Image {idx+1} processed successfully.")
                    else:
                        st.error(f"Failed to process image {idx+1}.")

                except Exception as e:
                    format_and_display_error(e, idx)
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


def process_and_transcribe_pdf(pdf_path, pdf_name, gpt_version):
    """Convert PDF to images, preprocess each image, and generate transcripts."""
    st.write(f"Processing {pdf_name}.pdf...")

    # Convert PDF to images and preprocess
    compressed_images = convert_and_preprocess_pdf(pdf_path)

    # Generate transcripts from the processed images
    generate_transcripts_from_images(compressed_images, pdf_name, gpt_version)
