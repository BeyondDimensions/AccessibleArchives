import json
import os
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime, UTC
import ipfs_api
from .ipfs_localfs_interop import path_exists, is_dir, is_file, join_paths, read_file
from utils import logging
from .exceptions import InvalidDocumentCollectionError


@dataclass_json
@dataclass
class Transcript:
    """Represents a file containing the transcript of a Page object."""
    ipfs_id: str    # IPFS CID of the markdown file containing the transcript
    transcriber: str
    date: datetime


@dataclass_json
@dataclass
class Page:
    """Represents a single page of a document."""
    ipfs_id: str
    transcripts: list[Transcript]


@dataclass_json
@dataclass
class MultiPageDoc:
    """Represents a folder comprising multiple pages"""
    ipfs_id: str  # the IPFS CID of the json document representing this MultiPageDoc
    pages: list[str]  # the IPFS CIDs of all the pages of this document

    def get_page(self, page_number: int) -> Page:
        return Page.from_json(ipfs_api.read(self.pages[page_number]))


@dataclass_json
@dataclass
class DocumentCollection:
    """Represents a collection of documents."""
    path: str
    multi_page_docs: list[MultiPageDoc]

    pages_dir = "Pages"
    pagemetadata_dir = "PageMetadata"
    transcripts_dir = "Transcripts"
    multipagedocs_dir = "MultiPageDocs"

    def __init__(self, collection_path: str):
        self.path = collection_path
        self.check_path_integrity()

    def get_page_ids(self) -> list[str]:
        page_ids: list[str] = []
        for item in join_paths(self.path, self.pagemetadata_dir):
            # ignore non-json files
            if not item.endswith(".json"):
                continue

            # read the metadata file
            page_metadata_bytes = read_file(join_paths(self.path, self.pages_dir, item))
            page_metadata = json.loads(page_metadata_bytes.decode())

            # extract the Page IPFS ID from the metadata
            page_ids.append(page_metadata["ipfs_id"])
        return page_ids

    def check_path_integrity(self, ):
        if not path_exists(self.path):
            error_message = f"Can't find the path {self.path}"
            raise InvalidDocumentCollectionError(error_message)
        for subfolder in {self.pages_dir, self.transcripts_dir, self.multipagedocs_dir, self.pagemetadata_dir}:
            full_path = join_paths(self.path, subfolder)
            if not path_exists(full_path):
                error_message = f"Collection doesn't have the subfolder {full_path}"
                raise InvalidDocumentCollectionError(error_message)
            if is_file(full_path):
                error_message = f"This path should be a folder, not a file: {full_path}"
                raise InvalidDocumentCollectionError(error_message)
