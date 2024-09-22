import json
import os


def ensure_directories_exist(*dirs):
    """Ensure that all directories in the list exist."""
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)


def load_json_file(filepath):
    """Load a json file, return its contents as a dictionary."""
    with open(filepath, 'r') as file:
        return json.load(file)
