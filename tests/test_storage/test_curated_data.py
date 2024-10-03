import json
from _load_src import SRC_PATH
import shutil
import os
from datetime import datetime, UTC
from utils.utils import ensure_dir_exists
from jsonschema import validate
import jsonschema
from storage.storage_api import (
    MultiPageDoc, DocumentCollection, Page, Transcript, PageSource,
    PAGE_SCHEMA,
    MULTI_PAGE_DOC_SCHEMA,
)
from storage.ipfs_localfs_interop import read_file, get_ipfs_cid
DOCUMENTS_PATH = os.path.abspath(os.path.join(
    SRC_PATH, "..", ".data5"
))
PAGES_DIR = os.path.join(DOCUMENTS_PATH, "Pages")
PAGES_METADATA_DIR = os.path.join(DOCUMENTS_PATH, "PageMetadata")
UNTRANSCRIBED_DIR = ensure_dir_exists(os.path.join(DOCUMENTS_PATH, "Untrasncribed"))

print("Checking files...")
# check that page metadata files exist and contain valid JSON
for filename in os.listdir(PAGES_DIR):
    metadata_path = os.path.join(PAGES_METADATA_DIR, filename.split(".")[0]+".json")
    # check that page metadata files exist
    if not os.path.exists(metadata_path):

        try:
            shutil.move(os.path.join(PAGES_DIR, filename), UNTRANSCRIBED_DIR)
        except shutil.Error as e:
            if "already exists" in str(e):
                os.remove(os.path.join(PAGES_DIR, filename))
            else:
                raise e
    else:
        # check the PAGES_METADATA_DIR contains valid JSON files
        try:
            with open(metadata_path) as file:
                data = file.read()
            metadata = json.loads(data)
            validate(metadata, PAGE_SCHEMA)
        except json.JSONDecodeError as e:
            print(f"Failed to load page metadata for {filename}")
            raise e

print("Initialising DocumentCollection")
collection = DocumentCollection(DOCUMENTS_PATH)
print("Inistialised DocumentCollection")

print(len(collection.get_page_ids()))
print(len(collection.get_multipagedoc_ids()))
doc = collection.get_multipagedocs().send(None)
# for doc in collection.get_multipagedocs():
#     print(len(doc.pages))


# doc._load_page_metadata()
"QmfMo8eELXbwvDgczDQA9BMpDYFarLuYrycYBHqxuj2DYb" in set(doc.get_page_ids())
print(doc.get_page_from_page_number(0))
print(doc.pages[2])
