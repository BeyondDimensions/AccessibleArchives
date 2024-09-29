import os
import shutil
from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException

# Define the source and target directories
source_dir = '/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/Transcripts'
english_dir = '/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/Failed_Transcripts'

# Ensure the target directory exists
os.makedirs(english_dir, exist_ok=True)

# Function to create an empty Markdown file with the same name in the source directory
def create_empty_markdown(filename):
    empty_file_path = os.path.join(source_dir, filename)
    with open(empty_file_path, 'w', encoding='utf-8') as empty_file:
        # Writing nothing to the file, thus keeping it empty
        pass
    print(f"Created empty file: {empty_file_path}")

# Function to check if the text contains both English and German
def contains_german(text):
    try:
        languages = detect_langs(text)  # Returns a list of detected languages with probabilities
        for lang in languages:
            if lang.lang == 'de':
                return True
        return False # No German detected
    except LangDetectException:
        return False

# Process the files in the source directory
for filename in os.listdir(source_dir):
    if filename.lower().endswith('.md'):  # Case-insensitive .md check
        file_path = os.path.join(source_dir, filename)
        
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Skip the file if it is empty
        if not content.strip():  # Strip to ignore whitespace-only files
            print(f"{filename} is empty, skipping.")
            continue

        # Check if the content contains German
        if contains_german(content):
            print(f"{filename} contains German, skipping")
            continue # Do not move files, contains German
        
        # Check if the file start with "I'm"
        if content.strip().startswith("I'm"):
            # Move the file to the English directory
            shutil.move(file_path, os.path.join(english_dir, filename))
            print(f"Moved {filename} to {english_dir}")
            create_empty_markdown(filename)  # Only create empty file for "I'm" files
        else:
            print(f"{filename} is not in English, skipping.")