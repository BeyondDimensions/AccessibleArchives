import os


def ensure_directories_exist(*dirs):
    """Ensure that all directories in the list exist."""
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
