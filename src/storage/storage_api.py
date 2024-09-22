from typing import Iterator, List
from jsonschema import validate
import jsonschema
import json
import os
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime, UTC
import ipfs_api
from .ipfs_localfs_interop import path_exists, is_dir, is_file, join_paths, read_file, list_dir
from utils import logging
from .exceptions import InvalidDocumentCollectionError
from utils.utils import load_json_file
from dataclasses import dataclass
from dataclasses_json import dataclass_json, config
from datetime import datetime
from typing import List
import dateutil.parser
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from datetime import datetime
from typing import List
import dateutil.parser
# Custom encoder and decoder for datetime to use strings (ISO 8601 format)


def datetime_encoder(dt: datetime) -> str:
    return dt.isoformat()


def datetime_decoder(dt_str: str) -> datetime:
    return dateutil.parser.isoparse(dt_str)


PAGE_SCHEMA = load_json_file(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "json_schemas", "Page.json"
))
MULTI_PAGE_DOC_SCHEMA = load_json_file(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "json_schemas", "MultiPageDoc.json"
))


@dataclass_json
@dataclass
class Transcript:
    """Represents a file containing the transcript of a Page object."""
    ipfs_id: str    # IPFS CID of the markdown file containing the transcript
    transcriber: str
    timestamp: datetime = field(
        default_factory=datetime.now,  # You can set default_factory for datetimes if needed
        metadata=config(
            encoder=datetime_encoder,
            decoder=datetime_decoder
        )
    )  # Specify the custom encoder/decoder for datetime


@dataclass_json
@dataclass
class PageSource:
    original_medium: str
    digitiser: str
    digitisation_date: datetime = field(
        default_factory=datetime.now,  # You can set default_factory for datetimes if needed
        metadata=config(
            encoder=datetime_encoder,
            decoder=datetime_decoder
        )
    )  # Specify the custom encoder/decoder for datetime


@dataclass_json
@dataclass
class Page:
    """Represents a single page of a document."""

    ipfs_id: str
    transcripts: list[Transcript]
    content: dict
    source: PageSource


@dataclass_json
@dataclass
class MultiPageDoc:
    """Represents a folder comprising multiple pages"""
    ipfs_id: str  # the IPFS CID of the json document representing this MultiPageDoc
    pages: list[str]  # the IPFS CIDs of all the pages of this document
    content: dict
    source: dict
    doc_col: 'DocumentCollection'

    def get_page_from_ipfs_id(self, ipfs_id: str) -> Page:
        if ipfs_id not in self.pages:
            raise ValueError("This IPFS ID does not belong to any page in this MultiPageDoc.")
        return self.doc_col.get_page_from_ipfs_id(ipfs_id)

    def get_page_from_page_number(self, page_number: int) -> Page:
        return self.get_page_from_ipfs_id(self.pages[page_number])

    def get_pages(self) -> Iterator[Page]:
        """Returns an iterator over the Page objects linked to this MultiPageDoc."""
        for page_ipfs_id in self.pages:
            yield self.get_page_from_ipfs_id(page_ipfs_id)


@dataclass_json
@dataclass
class DocumentCollection:
    """Represents a collection of documents."""
    path: str
    multi_page_docs: list[MultiPageDoc]

    pages_dir = "Pages"
    pagemetadata_dirname = "PageMetadata"
    transcripts_dirname = "Transcripts"
    multipagedocs_dirname = "MultiPageDocs"
    _page_ids: list[str] | None = None

    def __init__(self, collection_path: str):
        self.path = collection_path
        self.pagemetadata_dir = os.path.join(self.path, self.pagemetadata_dirname)
        self.transcripts_dir = os.path.join(self.path, self.transcripts_dirname)
        self.multipagedocs_dir = os.path.join(self.path, self.multipagedocs_dirname)

        self.check_path_integrity()

    def _load_pages(self) -> list[str]:
        page_ids: list[str] = []
        for item in list_dir(self.pages_dir):

            ipfs_id = ipfs_api.predict_cid(join_paths(self.pages_dir, item))
            if not item.split(".")[0] == ipfs_id:
                raise InvalidDocumentCollectionError(
                    "This page's filename is not its IPFS ID"
                )
            # read the metadata file
            metadata_filepath = join_paths(self.path, self.pagemetadata_dir, f"{ipfs_id}.json")
            page_metadata = json.loads(read_file(metadata_filepath).decode())
            validate(load_json_file(metadata_filepath), PAGE_SCHEMA)
            # extract the Page IPFS ID from the metadata
            if not page_metadata["ipfs_id"] == ipfs_id:
                raise InvalidDocumentCollectionError(
                    "This metadata file's filename is not its encoded IPFS ID"
                )
        # double check metadata files
        for item in list_dir(self.pages_dir):
            # ignore non-JSON files
            if not item.endswith(".json"):
                continue
            ipfs_id = item.strip(".json")
            if ipfs_id not in page_ids:
                raise InvalidDocumentCollectionError(
                    "This metadata file refers to a page which is not under pages."
                )

        self._page_ids_cache = page_ids
        return page_ids

    def get_page_ids(self) -> list[str]:
        if not self._page_ids_cache:
            self._load_pages()
        return self._page_ids_cache

    def get_page_from_ipfs_id(self, ipfs_id: str) -> Page:
        if ipfs_id not in self.get_page_ids():
            raise ValueError("This IPFS ID does not belong to any page in this MultiPageDoc.")
        return Page.from_json(
            bytes.decode(read_file(join_paths(self.pagemetadata_dir, ipfs_id+".json")))
        )

    def get_pages(self) -> Iterator[Page]:
        """Returns an iterator over the Page objects linked to this MultiPageDoc."""
        for page_ipfs_id in self.get_page_ids():
            yield self.get_page_from_ipfs_id(page_ipfs_id)

    def get_doc_ids(self) -> list[str]:
        doc_ids: list[str] = []
        for item in list_dir(self.multipagedocs_dir):
            # ignore non-json files
            if not item.endswith(".json"):
                continue

            # read the metadata file
            metadata_filepath = join_paths(self.path, self.multipagedocs_dir, item)
            docs_metadata = json.loads(read_file(metadata_filepath).decode())

            # extract the Page IPFS ID from the metadata
            doc_ids.append(docs_metadata["ipfs_id"])
        return doc_ids

    def check_path_integrity(self, ):
        if not path_exists(self.path):
            error_message = f"Can't find the path {self.path}"
            raise InvalidDocumentCollectionError(error_message)
        for subfolder in {
            self.pages_dir,
            self.transcripts_dir,
            self.multipagedocs_dir,
            self.pagemetadata_dir
        }:
            full_path = join_paths(self.path, subfolder)
            if not path_exists(full_path):
                error_message = f"Collection doesn't have the subfolder {
                    full_path}"
                raise InvalidDocumentCollectionError(error_message)
            if is_file(full_path):
                error_message = f"This path should be a folder, not a file: {
                    full_path}"
                raise InvalidDocumentCollectionError(error_message)

        # verify the integrity of pages and their metadata files
        self._load_pages()
        for metadata_filename in os.listdir(self.multipagedocs_dir):
            metadata_filepath = os.path.join(
                self.multi_page_docs, metadata_filename
            )
            validate(load_json_file(metadata_filepath), MULTI_PAGE_DOC_SCHEMA)
