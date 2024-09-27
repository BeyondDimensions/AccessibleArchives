import os
import shutil
from langdetect import detect

# Define the source and target directories
source_dir = '/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/Transcripts'
english_dir = '/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/Failed_Transcripts'

# Ensure the target directory exists
os.makedirs(english_dir, exist_ok=True)

# Function to check if the file is in English
def is_english(text):
    try:
        # Detect the language of the text
        language = detect(text)
        return language == 'en'
    except LangDetectException:  # Handle cases where detection fails
        return False

# Process the files in the source directory
for filename in os.listdir(source_dir):
    if filename.lower().endswith('.md'):  # Case-insensitive .md check
        file_path = os.path.join(source_dir, filename)
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Check if the file is in English
        if is_english(content):
            # Move the file to the English directory
            shutil.move(file_path, os.path.join(english_dir, filename))
            print(f"Moved {filename} to {english_dir}")
        else:
            print(f"{filename} is not in English, skipping.")