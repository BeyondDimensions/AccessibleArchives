import os
import shutil

# Define the source and target directories
source_dir = '/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/Transcripts'
english_dir = '/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/Failed_Transcripts'

# Ensure the target directory exists
os.makedirs(english_dir, exist_ok=True)

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
        
        # Check if the file is in English
        if content.strip().startswith("I'm"):
            # Move the file to the English directory
            shutil.move(file_path, os.path.join(english_dir, filename))
            print(f"Moved {filename} to {english_dir}")
        else:
            print(f"{filename} is not in English, skipping.")