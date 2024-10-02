import os
import base64


def encode_file_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')


def encode_data_base64(data: bytes) -> str:
    return base64.b64encode(data).decode('utf-8')


def ensure_directories_exist(*dirs):
    """Ensure that all directories in the list exist."""
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)


def ensure_dir_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path
