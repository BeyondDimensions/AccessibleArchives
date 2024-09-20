"""
Use ChatGPT to transcribe images to markdown.

# Usage
```py
from transcription import transcribe_image

transcribe_image("/home/Programming/test.jpg", "/home/Programming/tmp/test-output.md")
```
"""

import os
import base64
import logging
import requests
from utils import OPENAI_API_KEY

# Initialize logging
logging.basicConfig(level=logging.INFO)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


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


def openai_api_prompt(api_key, gpt_version, image_base64):
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
      "model": gpt_version,
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Please extract and transcribe all visible text and formatting from the following image and save it into a markdown file. "
                      "Use appropriate markdown syntax to represent headings, tables, lists, and any other formatting present in the image. "
                      # "If you can not transcribe the image, say: \"I'm unable to transcribe the text from the image. Please refer to the original "
                      # "document for accurate information.\". Don't comment anything by yourself, just give me the extracted and transcribed text."
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}",
                "detail": "high"
              }
            }
          ]
        }
      ]
    }

    return requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)


def transcribe_image(image_path, md_filepath=None, api_key=OPENAI_API_KEY, gpt_version="gpt-4o-2024-08-06"):
    """Process a single image and save the markdown file next to it."""
    try:
        logging.info(f"Processing {image_path}...")

        if not api_key:
            raise Exception("Couldn't load API Key for OpenAI")

        # Send the image to GPT
        image_base64 = encode_image(image_path)
        response = openai_api_prompt(api_key, gpt_version, image_base64)

        # Check if the response is successful
        if response.status_code == 200:
            message_content = response.json(
            )['choices'][0]['message']['content']
            markdown_content = extract_markdown_from_response(message_content)

            # Save the markdown file next to the image
            if not md_filepath:
                md_filepath = f"{os.path.splitext(image_path)[0]}.md"

            with open(md_filepath, 'w') as file:
                file.write(markdown_content)

            logging.info(
                f"Successfully processed {image_path} and saved {md_filepath}.")
        else:
            error_message = f"Failed to process {image_path}. No response received."
            logging.error(error_message)
            raise Exception(error_message)
    except Exception as e:
        error_message = f"Error processing {image_path}: {str(e)}"
        logging.error(error_message)
        raise Exception(error_message)

    return md_filepath
