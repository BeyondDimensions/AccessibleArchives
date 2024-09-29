from _load_src import SRC_PATH
import shutil
import os
from datetime import datetime, UTC
from utils.utils import ensure_dir_exists
from storage.storage_api import MultiPageDoc, DocumentCollection, Page, Transcript, PageSource
from storage.ipfs_localfs_interop import read_file, get_ipfs_cid
TEST_COLLECTION_PATH = "/tmp/MyTemp/AccessibleArchive"
PAGES_DIR = os.path.join(TEST_COLLECTION_PATH, "Pages")
PAGES_METADATA_DIR = os.path.join(TEST_COLLECTION_PATH, "PageMetadata")
UNTRANSCRIBED_DIR = ensure_dir_exists(os.path.join(TEST_COLLECTION_PATH, "Untrasncribed"))

for filename in os.listdir(PAGES_DIR):
    metadata_path = os.path.join(PAGES_METADATA_DIR, filename.split(".")[0]+".json")
    if not os.path.exists(metadata_path):
        shutil.copy(os.path.join(PAGES_DIR, filename), UNTRANSCRIBED_DIR)
collection = DocumentCollection(TEST_COLLECTION_PATH)

len(collection.get_page_ids())

len(collection.get_multipagedoc_ids())
doc = collection.get_multipagedocs().send(None)
doc.get_page_from_page_number(4)
doc.pages[2]
