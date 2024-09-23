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
    os.path.dirname(os.path.abspath(__file__)
                    ), "json_schemas", "MultiPageDoc.json"
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

    def get_text(self):
        return ipfs_api.read(self.ipfs_id).decode()


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
    """Represents a single page of source material."""

    ipfs_id: str    # the IPFS content ID of this page
    # metadata of different versions of transcripts of this page
    transcripts: list[Transcript]
    content: dict   # description of this page's content
    source: PageSource  # information of this page's source
    format: str     # the digital file format of this page, expressed by file-name extension


@dataclass_json
@dataclass
class CompiledDoc:
    """A file, based on a MultiPageDoc, in which pages and/or transcripts
    have been compiled into a more complex format."""

    ipfs_id: str    # the IPFS ID of the file
    format: str  # the digital file format, expressed by file-name extension
    compilation_method: str  # how this document was compiled from source
    compilation_date: datetime = field(
        default_factory=datetime.now,  # You can set default_factory for datetimes if needed
        metadata=config(
            encoder=datetime_encoder,
            decoder=datetime_decoder
        )
    )  # Specify the custom encoder/decoder for datetime


@dataclass_json
@dataclass
class MultiPageDoc:
    """Represents a folder comprising multiple pages"""
    # IPFS CID of the folder containing the Pages included in this document
    ipfs_id: str
    # IPFS CIDs of the pages and their metadata files, ordered by page number
    pages: list[str]
    content: dict
    source: dict
    compilations: list[CompiledDoc]

    def get_page_from_ipfs_id(
        self,
        ipfs_id: str,
    ) -> Page:
        """Get a Page from this document, given its IPFS content ID.
        Args:
            ipfs_id: the IPFS content ID of the 
        """
        if ipfs_id not in self.pages:
            raise ValueError(
                "This IPFS ID does not belong to any page in this MultiPageDoc.")
        return ipfs_api.read()

    def _load_page_metadata(self,) -> None:
        pages: dict[str, Page] = {}
        for metadata_ipfs_id in self.pages:

            # load page from metadata
            page = Page.from_json(bytes.decode(ipfs_api.read(metadata_ipfs_id)))
            ipfs_id = page.ipfs_id
            # ensure no duplicate pages
            if ipfs_id in pages.keys():
                raise InvalidDocumentCollectionError(
                    "This MultiPageDoc refers to the same page multiple times!"
                )
            pages.update({ipfs_id: page})
        self._pages = pages

    def get_pages(self) -> list[Page]:
        # if we haven't yet loaded our pages and their metadata, do so
        if not hasattr(self, "_pages") or not self._pages:
            self._load_page_metadata()
        return list(self._pages.values())

    def get_page_transcripts(self) -> list[Transcript]:
        return [page.transcripts[0] for page in self.get_pages()]

    def get_page_ids(self) -> list[str]:
        # if we haven't yet loaded our pages and their metadata, do so
        if not hasattr(self, "_pages") or not self._pages:
            self._load_page_metadata()
        return list(self._pages.keys())

    def get_page_from_page_number(self, page_number: int) -> Page:
        return self.get_page_from_ipfs_id(self.pages[page_number])


@dataclass_json
@dataclass
class DocumentCollection:
    """Represents a collection of documents."""
    path: str
    multi_page_docs: list[MultiPageDoc]

    pages_dirname = "Pages"
    pagemetadata_dirname = "PageMetadata"
    transcripts_dirname = "Transcripts"
    multipagedocs_dirname = "MultiPageDocs"

    def __init__(self, collection_path: str):
        self.path = collection_path
        self.pages_dir = os.path.join(self.path, self.pages_dirname)
        self.pagemetadata_dir = os.path.join(
            self.path, self.pagemetadata_dirname
        )
        self.transcripts_dir = os.path.join(
            self.path, self.transcripts_dirname
        )
        self.multipagedocs_dir = os.path.join(
            self.path, self.multipagedocs_dirname
        )

        _page_ids: list[str] | None = None
        _multipagedoc_ids: list[str] | None = None
        self.check_path_integrity()

    def _load_pages(self) -> list[str]:
        page_ids: list[str] = []

        # check the Pages subfolder, ensuring correct file-naming
        # and existence of metadata files
        for filename in list_dir(self.pages_dir):
            page_filepath = join_paths(self.pages_dir, filename)
            expected_ipfs_id = filename.split(".")[0]
            try:
                ipfs_id = ipfs_api.predict_cid(page_filepath)
                if not ipfs_id == expected_ipfs_id:
                    raise InvalidDocumentCollectionError(
                        "This Page's filename is not its IPFS ID"
                    )
            except ipfs_api.ipfshttpclient.exceptions.ConnectionError:
                print("Warning: IPFS isn't running, can't verify ID")
                ipfs_id = expected_ipfs_id

                # read the metadata file
            metadata_filepath = join_paths(
                self.path, self.pagemetadata_dir, f"{ipfs_id}.json"
            )

            page_metadata = load_json_file(metadata_filepath)
            validate(page_metadata, PAGE_SCHEMA)

            # extract the Page IPFS ID from the metadata
            if not page_metadata["ipfs_id"] == ipfs_id:
                raise InvalidDocumentCollectionError(
                    "This metadata file's filename is not its encoded IPFS ID"
                )

            if not filename == f"{ipfs_id}.{page_metadata['format']}":
                raise InvalidDocumentCollectionError(
                    "This page's filename is not its IPFS ID and extension"
                )
            page_ids.append(ipfs_id)
        # double check metadata files
        for filename in list_dir(self.pages_dir):
            # ignore non-JSON files
            if not filename.endswith(".json"):
                continue
            ipfs_id = filename.strip(".json")
            if ipfs_id not in page_ids:
                raise InvalidDocumentCollectionError(
                    "This metadata file refers to a page which is not under pages."
                )

        self._page_ids = page_ids
        return page_ids

    def _load_multipagedocs(self) -> list[str]:
        doc_ids: list[str] = []

        # check the Pages subfolder, ensuring correct file-naming
        # and existence of metadata files
        for filename in list_dir(self.multipagedocs_dir):
            # only process JSON files
            if not filename.endswith(".json"):
                continue
            # read the metadata file
            metadata_filepath = join_paths(
                self.path, self.multipagedocs_dir, filename
            )

            doc_metadata = load_json_file(metadata_filepath)
            validate(doc_metadata, MULTI_PAGE_DOC_SCHEMA)
            # extract the Page IPFS ID from the metadata

            ipfs_id = doc_metadata["ipfs_id"]
            if filename != f"{ipfs_id}.json":
                raise InvalidDocumentCollectionError(
                    "This MultiPageDoc's filename is not its ID"
                )

            doc_ids.append(ipfs_id)

        self._multipagedoc_ids = doc_ids
        return doc_ids

    def get_multipagedoc_ids(self):
        if not self._multipagedoc_ids:
            self._load_multipagedocs()
        return self._multipagedoc_ids

    def get_multipagedocs(self) -> Iterator[MultiPageDoc]:
        """Get an iterator over the Page objects linked to this MultiPageDoc."""
        for doc_id in self.get_multipagedoc_ids():
            yield MultiPageDoc.from_json(read_file(join_paths(
                self.multipagedocs_dir, f"{doc_id}.json"
            )))

    def get_page_ids(self) -> list[str]:
        if not self._page_ids:
            self._load_pages()
        return self._page_ids

    def get_pages(self) -> Iterator[Page]:
        """Get an iterator over the Page objects linked to this MultiPageDoc."""
        for page_ipfs_id in self.get_page_ids():
            yield self.get_page_from_ipfs_id(page_ipfs_id)

    def get_page_from_ipfs_id(self, ipfs_id: str) -> Page:
        if ipfs_id not in self.get_page_ids():
            raise ValueError(
                "This IPFS ID does not belong to any page in this MultiPageDoc."
            )
        return Page.from_json(
            bytes.decode(read_file(join_paths(
                self.pagemetadata_dir, ipfs_id + ".json"
            )))
        )

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
                error_message = (
                    f"Collection doesn't have the subfolder {full_path}"
                )
                raise InvalidDocumentCollectionError(error_message)
            if is_file(full_path):
                error_message = (
                    f"This path should be a folder, not a file: {full_path}"
                )
                raise InvalidDocumentCollectionError(error_message)

        # verify the integrity of pages and their metadata files
        self._load_pages()
        self._load_multipagedocs()
