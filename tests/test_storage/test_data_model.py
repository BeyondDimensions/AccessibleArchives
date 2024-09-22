from datetime import datetime, UTC
from _load_src import SRC_PATH
from storage.storage_api import MultiPageDoc, DocumentCollection, Page, Transcript, PageSource

import os
TEST_COLLECTION_PATH = os.path.join(
    SRC_PATH, "..", "tests", "test_storage", "docs_template"
)

collection = DocumentCollection(TEST_COLLECTION_PATH)
[page for page in collection.get_pages()]

collection.get_page_ids()
multipage_doc[0] = collection.get_multipage_docs()
multipage_doc.get_pages()

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
