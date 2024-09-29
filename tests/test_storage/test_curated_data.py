from _load_src import SRC_PATH
import shutil
import os
from datetime import datetime, UTC
from utils.utils import ensure_dir_exists
from storage.storage_api import MultiPageDoc, DocumentCollection, Page, Transcript, PageSource
from storage.ipfs_localfs_interop import read_file, get_ipfs_cid
TEST_COLLECTION_PATH = "/media/llearuin/EXT/curated_files"
PAGES_DIR = os.path.join(TEST_COLLECTION_PATH, "Pages")
PAGES_METADATA_DIR = os.path.join(TEST_COLLECTION_PATH, "PageMetadata")
UNTRANSCRIBED_DIR = ensure_dir_exists(os.path.join(TEST_COLLECTION_PATH, "Untrasncribed"))

print("Checking files...")
for filename in os.listdir(PAGES_DIR):
    metadata_path = os.path.join(PAGES_METADATA_DIR, filename.split(".")[0]+".json")
    if not os.path.exists(metadata_path):

        try:
            shutil.move(os.path.join(PAGES_DIR, filename), UNTRANSCRIBED_DIR)
        except shutil.Error as e:
            if "already exists" in str(e):
                os.remove(os.path.join(PAGES_DIR, filename))
            else:
                raise e
print("Initialising DocumentCollection")
collection = DocumentCollection(TEST_COLLECTION_PATH)
print("Inistialised DocumentCollection")

print(len(collection.get_page_ids()))
print(len(collection.get_multipagedoc_ids()))
doc = collection.get_multipagedocs().send(None)
for doc in collection.get_multipagedocs():
    print(len(doc.pages))

doc._load_page_metadata()
"QmYAQ5tgS4ci2Yisezihs28om4hLpVaHvNudfUBCJ9PJjM" in set(doc.pages)
print(doc.get_page_from_page_number(4))
print(doc.pages[2])
