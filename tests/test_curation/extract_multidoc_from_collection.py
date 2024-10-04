import shutil
from _load_src import SRC_PATH
from tqdm import tqdm
from utils import ensure_dir_exists
from storage import DocumentCollection, Page
import os
from rag import initialize_database
import ipfs_api
DOCUMENTS_PATH = os.path.abspath(os.path.join(
    SRC_PATH, "..", ".data2"
))

docs_clxn = DocumentCollection(DOCUMENTS_PATH)
longest_doc = None
MAX_DOC_SEARCH_COUNT = 20
for i, doc in enumerate(tqdm(docs_clxn.get_multipagedocs())):
    if i > MAX_DOC_SEARCH_COUNT:
        break
    if longest_doc is None:
        longest_doc = doc
        continue
    if len(doc.pages) > len(longest_doc.pages):
        longest_doc = doc
longest_doc = docs_clxn.get_multipagedoc("QmPjudoU1LuKkA65Xw1aC6qJHhqon5iicUdr5AcA63QpjE")
len(longest_doc.pages)
len(longest_doc.get_pages())
OUTPUT_DIR = ".output"
OUTPUT_PAGES_DIR = ensure_dir_exists(os.path.join(OUTPUT_DIR, "Pages"))
OUTPUT_PAGES_METADAT_DIR = ensure_dir_exists(os.path.join(OUTPUT_DIR, "PageMetadata"))
OUTPUT_TRANSCRIPTS_DIR = ensure_dir_exists(os.path.join(OUTPUT_DIR, "Transcripts"))
OUTPUT_MULTI_DOC_DIR = ensure_dir_exists(os.path.join(OUTPUT_DIR, "MultiPageDocs"))
longest_doc
# p = longest_doc.get_page("QmSm2ar5iaCUTXULRPR9TdrjJiHE5YNtLkyLHiVSZz4dFD")
# p.transcripts[0].get_text()
for page in tqdm(longest_doc.get_pages()):
    print(page.ipfs_id, "Page")
    page_path = os.path.join(OUTPUT_PAGES_DIR, page.ipfs_id+"."+page.format)
    if not os.path.exists(page_path):
        # with open(page_path, "wb+") as file:
        #     file.write(page.get_data())
        shutil.copy(
            os.path.join(docs_clxn.pages_dir, page.ipfs_id+f".{page.format}"),
            page_path
        )
    print(page.ipfs_id, "Metadata")
    metadata_path = os.path.join(OUTPUT_PAGES_METADAT_DIR, page.ipfs_id+".json")
    if not os.path.exists(metadata_path):
        # with open(metadata_path, "w+") as file:
        #     file.write(page.to_json())
        shutil.copy(
            os.path.join(docs_clxn.pagemetadata_dir, page.ipfs_id+".json"),
            metadata_path
        )

        assert ipfs_api.predict_cid(metadata_path) in longest_doc._metadata_ids
    print(page.ipfs_id, "Transcrip")
    transcript_path = os.path.join(OUTPUT_TRANSCRIPTS_DIR, page.ipfs_id+".md")
    if not os.path.exists(transcript_path):
        print("Writing...")
        # with open(transcript_path, "w+") as file:
        #     transcript = page.transcripts[0]
        #     print(page.transcripts[0].ipfs_id)
        #     if page.transcripts[0].ipfs_id == "QmbFMke1KXqnYyBBWxB74N4c5SBnJMVAiMNRcGu6x1AwQH":
        #         file.write("")
        #     else:
        #         try:
        #             file.write(page.transcripts[0].get_text())
        #         except:
        #             file.write("")
        shutil.copy(os.path.join(docs_clxn.transcripts_dir, page.ipfs_id+".md"), transcript_path)
    print(page.ipfs_id, "Done!")

with open(os.path.join(OUTPUT_MULTI_DOC_DIR, longest_doc.ipfs_id+".json"), "w+") as file:
    file.write(longest_doc.to_json())
with open(os.path.join(OUTPUT_MULTI_DOC_DIR, longest_doc.ipfs_id+".pdf"), "wb+") as file:
    file.write(longest_doc.compilations[0].get_data())
