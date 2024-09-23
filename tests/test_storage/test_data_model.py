from datetime import datetime, UTC
from _load_src import SRC_PATH
from storage.storage_api import MultiPageDoc, DocumentCollection, Page, Transcript, PageSource
from storage.ipfs_localfs_interop import read_file
import os
import ipfs_api
TEST_COLLECTION_PATH = os.path.join(
    SRC_PATH, "..", "tests", "test_storage", "docs_template"
)

page_id = "QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2"
page = Page.from_json(read_file(os.path.join(
    TEST_COLLECTION_PATH, "PageMetadata", f"{page_id}.json"
)))

assert page.ipfs_id == "QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2"

transcript_text = read_file(os.path.join(
    TEST_COLLECTION_PATH, "Transcripts", f"{page_id}.md"
)).decode()
assert page.transcripts[0].get_text() == transcript_text

doc = MultiPageDoc.from_json(read_file(os.path.join(
    TEST_COLLECTION_PATH, "MultiPageDocs", "Qmb4yZQxAaWkrR2hNKcBBnxvEyvewGXqpQtBZHziAWaZov.json")))


assert page in doc.get_pages()
assert page_id in doc.get_page_ids()

collection = DocumentCollection(TEST_COLLECTION_PATH)
assert page in collection.get_pages()
assert page_id in collection.get_page_ids()
assert doc in collection.get_multipagedocs()


# p = Page(
#     "QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2",
#     [
#         Transcript(
#             "QmbHXuQmaEKaZqRmtBvGXxDSLvGJL1KG7fq1qKFAhwR4v2",
#             "ChatGPT",
#             datetime.now(UTC))
#     ],
#     {},
#     PageSource(
#         "PhotoCopy of BStU archive document", digitisation_date=datetime.now(UTC), digitiser="anonymoys"
#     )
# )
# p.source.digitisation_date
# with open("/mnt/Uverlin/CLAN/AccessibleArchives/tests/test_storage/docs_template/PageMetadata/QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2.json", "w+")as file:
#     file.write(p.to_json())
# pages_dir = os.path.join(TEST_COLLECTION_PATH, "Pages")
# mpd_ipfs_id = ipfs_api.publish(pages_dir)
#
# pages = [
#     (
#         page_name.split(".")[0],
#         ipfs_api.publish(os.path.join(
#             TEST_COLLECTION_PATH,
#             "PageMetadata", page_name.replace("png", "json")
#         ))
#     )
#     for page_name in os.listdir(pages_dir)
# ]
# doc = MultiPageDoc(mpd_ipfs_id, pages, {}, {})
# doc.to_json()
