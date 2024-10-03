import os
import json
import shutil

# Define the paths
json_folder = "/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/MultiPageDocsFull"
multipage_folder = "/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/MultiPageDocs"

#source folders
png_folder = "/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/PagesFull"  # The folder where the files are located
md_folder = "/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/TranscriptsFull"
json_files_folder = "/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/PageMetadataFull"

# destination folders
png_destination_folder = "/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/Pages"  # Where you want to move the files
md_destination_folder = "/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/Transcripts"
json_destination_folder = "/Users/marvinkirsch/Programming/AccessibleArchives/curated_files/PageMetadata"

# Create directories if they don't exist
os.makedirs(multipage_folder, exist_ok=True)
os.makedirs(png_destination_folder, exist_ok=True)
os.makedirs(md_destination_folder, exist_ok=True)
os.makedirs(json_destination_folder, exist_ok=True)

# Step 1: Find the 3 .json files with the longest 'pages' lists and move them to MultiPageDocs
def find_top_3_json_files(json_folder, multipage_folder):
    # Check if the folder already contains files
    moved_files = os.listdir(multipage_folder)
    if moved_files:
        print("Step 1: Files have already been moved to MultiPageDocs. Skipping step 1.")
        return [os.path.join(multipage_folder, file) for file in moved_files]

    json_files = [f for f in os.listdir(json_folder) if f.endswith('.json')]
    file_lengths = []

    for file in json_files:
        file_path = os.path.join(json_folder, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            if 'pages' in data and isinstance(data['pages'], list):
                file_lengths.append((file, len(data['pages'])))

    # Sort files by the length of 'pages' in descending order and take the top 3
    top_3_files = sorted(file_lengths, key=lambda x: x[1], reverse=True)[:3]

    # Move the top 3 files to the 'MultiPageDocs' folder
    for file, length in top_3_files:
        print(f"Moving file {file} to {multipage_folder}")
        shutil.move(os.path.join(json_folder, file), os.path.join(multipage_folder, file))

    return [os.path.join(multipage_folder, file[0]) for file in top_3_files]

# Step 2: Move the files listed in the 'pages' list to their respective destination folders
def move_files_from_json(pages_list, folder_map):
    for file_name in pages_list:
        file_found = False  # Track if the file is found

        for extension, paths in folder_map.items():
            file_with_extension = file_name + extension
            source_folder = paths["source"]
            destination_folder = paths["destination"]

            print(f"Looking for {file_with_extension} in {source_folder}")

            # Search for the file in the source folder
            for root, dirs, files in os.walk(source_folder):
                if file_with_extension in files:
                    source_path = os.path.join(root, file_with_extension)
                    print(f"Found and moving {file_with_extension} to {destination_folder}")
                    shutil.move(source_path, os.path.join(destination_folder, file_with_extension))
                    file_found = True
                    break  # Break out of the loop once the file is found

            if file_found:
                break  # Stop checking other extensions if the file is found

        if not file_found:
            print(f"File {file_name} with any known extension was not found.")

# Define the source and destination folders for different file types
folder_map = {
    '.png': {
        "source": png_folder,
        "destination": png_destination_folder
    },
    '.md': {
        "source": md_folder,
        "destination": md_destination_folder
    },
    '.json': {
        "source": json_files_folder,
        "destination": json_destination_folder
    }
}
from _load_src import SRC_PATH

from storage.ipfs_localfs_interop import list_dir
# Main execution
top_3_json_files = find_top_3_json_files(json_folder, multipage_folder)

# Step 2: For each of the top 3 files, move the files listed in 'pages' to their respective folders
for json_file in top_3_json_files:
    print(f"Reading file: {json_file}")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if 'pages' in data and isinstance(data['pages'], list):
            print(f"Processing pages list in {json_file}: {data['pages']}")
            png_ids = list_dir(f"/ipfs/{data['ipfs_id']}")

            move_files_from_json(png_ids, folder_map)
        else:
            print(f"No 'pages' list found in {json_file}")