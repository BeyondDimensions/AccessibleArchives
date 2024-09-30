from typing import Iterator, List
from jsonschema import validate
import jsonschema
import json
import os
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime, UTC
import ipfs_api
from .ipfs_localfs_interop import is_ipfs_path, path_exists, is_dir, is_file, join_paths, read_file, list_dir, get_ipfs_cid
from utils import logger
from .exceptions import InvalidDocumentCollectionError
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


def encode_datetime_to_str(dt: datetime) -> str:
    return dt.isoformat()


def decode_datetime_from_str(dt_str: str) -> datetime:
    return dateutil.parser.isoparse(dt_str)


def load_json_file(filepath):
    """Load a json file, return its contents as a dictionary."""
    if is_ipfs_path(filepath):
        return json.loads(ipfs_api.read(filepath).decode())
    else:
        with open(filepath, 'r') as file:
            return json.load(file)


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
            encoder=encode_datetime_to_str,
            decoder=decode_datetime_from_str
        )
    )  # Specify the custom encoder/decoder for datetime

    def get_text(self):
        return ipfs_api.read(self.ipfs_id).decode()


@dataclass_json
@dataclass
class PageSource:
    """Represents the metadata about a Page's origin."""
    original_medium: str
    digitiser: str
    digitisation_date: datetime = field(
        default_factory=datetime.now,  # You can set default_factory for datetimes if needed
        metadata=config(
            encoder=encode_datetime_to_str,
            decoder=decode_datetime_from_str
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
    """A file comprised of a MultiPageDoc's pages and transcripts."""

    ipfs_id: str    # the IPFS ID of the file
    format: str  # the digital file format, expressed by file-name extension
    compilation_method: str  # how this document was compiled from source
    compilation_date: datetime = field(
        default_factory=datetime.now,  # You can set default_factory for datetimes if needed
        metadata=config(
            encoder=encode_datetime_to_str,
            decoder=decode_datetime_from_str
        )
    )  # Specify the custom encoder/decoder for datetime

    def get_data(self):
        return ipfs_api.read(self.ipfs_id)


@dataclass_json
@dataclass
class MultiPageDoc:
    """Represents a document comprising multiple pages."""
    # IPFS CID of the folder containing the Pages included in this document
    ipfs_id: str
    # IPFS CIDs of the pages and their metadata files, ordered by page number
    pages: list[str]
    content: dict
    source: dict
    compilations: list[CompiledDoc]

    def get_page(
        self,
        page_id: str,
    ) -> Page:
        """Get a Page from this document, given its IPFS content ID.
        Args:
            page_id: the IPFS content ID of the 
        """
        if not hasattr(self, "_pages") or not self._pages:
            self._load_page_metadata()

        try:
            return self._pages[page_id][0]
        except KeyError:
            raise ValueError(
                "This IPFS ID does not belong to any page in this MultiPageDoc."
            )

    def get_page_id_from_metadata_id(self, metadata_id: str) -> str:
        if not hasattr(self, "_metadata_ids") or not self._metadata_ids:
            self._load_page_metadata()
        return self._metadata_ids[metadata_id]

    def get_metadata_id_from_page_id(self, page_id: str) -> str:
        if not hasattr(self, "_pages") or not self._pages:
            self._load_page_metadata()
        return self._pages[page_id][1]

    def get_pages(self) -> list[Page]:
        # if we haven't yet loaded our pages and their metadata, do so
        if not hasattr(self, "_pages") or not self._pages:
            self._load_page_metadata()
        return [page for page, metadata_id in self._pages.values()]

    def get_page_transcripts(self) -> list[Transcript]:
        return [page.transcripts[0] for page in self.get_pages()]

    def get_page_ids(self) -> list[str]:
        # if we haven't yet loaded our pages and their metadata, do so
        if not hasattr(self, "_pages") or not self._pages:
            self._load_page_metadata()
        return list(self._pages.keys())

    def get_page_from_page_number(self, page_number: int) -> Page:
        """Get a Page, given its page number in this document."""
        return self.get_page(self.get_page_id_from_metadata_id(self.pages[page_number]))

    def get_page_number(self, page_id: str) -> int:
        return self.pages.index(self.get_metadata_id_from_page_id(page_id))

    def _read_metadata_file(self, metadata_id: str) -> str:
        """May be overridden to provide independence from IPFS daemon."""
        return ipfs_api.read(metadata_id)

    def _load_page_metadata(self,) -> None:
        """Read and validate this MultiPageDoc's Pages' metadata files."""
        pages: dict[str, tuple[Page, str]] = {}
        metadata_ids: dict[str, str] = {}
        for metadata_id in self.pages:

            # load page from metadata
            page = Page.from_json(self._read_metadata_file(metadata_id))
            page_id = page.ipfs_id
            # ensure no duplicate pages
            if page_id in pages.keys():
                raise InvalidDocumentCollectionError(
                    "This MultiPageDoc refers to the same page multiple times!"
                )
            pages.update({page_id: (page, metadata_id)})
            metadata_ids.update({metadata_id: page_id})
        self._pages = pages
        self._metadata_ids = metadata_ids


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
        self.pages_dir = join_paths(self.path, self.pages_dirname)
        self.pagemetadata_dir = join_paths(
            self.path, self.pagemetadata_dirname
        )
        self.transcripts_dir = join_paths(
            self.path, self.transcripts_dirname
        )
        self.multipagedocs_dir = join_paths(
            self.path, self.multipagedocs_dirname
        )

        _page_ids: list[str] | None = None
        _multipagedoc_ids: list[str] | None = None
        self.check_collection_integrity()

    def get_multipagedoc_ids(self) -> list[str]:
        """Get the IDs of the MultiPageDocs in this DocumentCollection."""
        if not self._multipagedoc_ids:
            self._load_multipagedocs()
        return self._multipagedoc_ids

    def get_multipagedoc(self, multipagedoc_id: str) -> MultiPageDoc:
        multipagedoc = MultiPageDoc.from_json(read_file(join_paths(
            self.multipagedocs_dir, f"{multipagedoc_id}.json"
        )))
        multipagedoc._load_page_metadata()
        self.make_multipagedoc_ipfs_independent(multipagedoc)
        return multipagedoc

    def get_multipagedocs(self) -> Iterator[MultiPageDoc]:
        """Get an iterator over the MultiPageDocs in this DocumentCollection."""
        for doc_id in self.get_multipagedoc_ids():

            yield self.get_multipagedoc(doc_id)

    def make_multipagedoc_ipfs_independent(self, multipagedoc: MultiPageDoc) -> MultiPageDoc:
        """Edit the MultiPageDoc method that reads an IPFS file to use
        the file from this DocumentCollection's path instead, allowing it to
        function without the IPFS daemon running."""
        multipagedoc._read_metadata_file = lambda x: read_file(
            self.get_page_metadata_path(self.get_page_id_from_metadata_id(x)))
        return multipagedoc

    def get_page_ids(self) -> list[str]:
        """Get the IDs of the Pages in this DocumentCollection."""

        if not self._page_ids:
            self._load_pages()
        return self._page_ids

    def get_page(self, page_id: str) -> Page:
        """Get a Page from this collection, given the IPFS ID of its source."""
        if page_id not in self.get_page_ids():
            raise ValueError(
                "The given IPFS ID does not belong to any of this DocumentCollection's pages."
            )

        return Page.from_json(read_file(self.get_page_metadata_path(page_id)))

    def get_pages(self) -> Iterator[Page]:
        """Get an iterator over the Pages in this DocumentCollection."""
        for page_ipfs_id in self.get_page_ids():
            yield self.get_page(page_ipfs_id)

    def get_page_path(self, page_id: str) -> str:
        page = self.get_page(page_id)
        page_path = join_paths(self.pages_dirname, page_id, page.format)
        if not path_exists(page_path):
            raise Exception(
                "Bug: The expected path for this page doesn't exist!"
            )
        return page_path

    def get_page_id_from_metadata_id(self, metadata_id: str) -> str:
        return self._metadata_ids[metadata_id]

    def get_page_metadata_path(self, page_id: str) -> str:
        return join_paths(self.pagemetadata_dir, page_id+".json")

    def get_page_docs(self, page_id: str) -> list[MultiPageDoc]:
        """Given the ID of a Page, get the documents which include it."""
        page_metadata_path = self.get_page_metadata_path(page_id)
        page_metadata_ipfs_id = get_ipfs_cid(page_metadata_path)
        multi_page_docs: list[MultiPageDoc] = []
        for multi_page_doc in self.get_multipagedocs():
            if page_metadata_ipfs_id in multi_page_doc.pages:
                multi_page_docs.append(multi_page_doc)
        return multi_page_docs

    def check_collection_integrity(self, ):
        """Ensure the data in this DocumentCollection is consistent."""
        if not path_exists(self.path):
            error_message = f"Can't find the path {self.path}"
            raise InvalidDocumentCollectionError(error_message)
        for subfolder_path in {
            self.pages_dir,
            self.transcripts_dir,
            self.multipagedocs_dir,
            self.pagemetadata_dir
        }:
            if not path_exists(subfolder_path):
                error_message = (
                    f"Collection doesn't have the subfolder {subfolder_path}"
                )
                raise InvalidDocumentCollectionError(error_message)
            if is_file(subfolder_path):
                error_message = (
                    f"This path should be a folder, not a file: {subfolder_path}"
                )
                raise InvalidDocumentCollectionError(error_message)

        # verify the integrity of pages and their metadata files
        self._load_pages()
        self._load_multipagedocs()

    def _load_pages(self) -> list[str]:
        page_ids: list[str] = []
        metadata_ids: dict[str, str] = {}
        # check the Pages subfolder, ensuring correct file-naming
        # and existence of metadata files
        for filename in list_dir(self.pages_dir):
            page_filepath = join_paths(self.pages_dir, filename)
            expected_ipfs_id = filename.split(".")[0]
            try:
                page_id = get_ipfs_cid(page_filepath)
                if not page_id == expected_ipfs_id:
                    raise InvalidDocumentCollectionError(
                        "This Page's filename is not its IPFS ID"
                    )
            except ipfs_api.ipfshttpclient.exceptions.ConnectionError:
                print("Warning: IPFS isn't running, can't verify ID")
                page_id = expected_ipfs_id

                # read the metadata file
            metadata_filepath = join_paths(
                self.pagemetadata_dir, f"{page_id}.json"
            )

            page_metadata = load_json_file(metadata_filepath)
            validate(page_metadata, PAGE_SCHEMA)

            # extract the Page IPFS ID from the metadata
            if not page_metadata["ipfs_id"] == page_id:
                raise InvalidDocumentCollectionError(
                    "This metadata file's filename is not its encoded IPFS ID"
                )

            if not filename == f"{page_id}.{page_metadata['format']}":
                raise InvalidDocumentCollectionError(
                    "This page's filename is not its IPFS ID and extension"
                )
            page_ids.append(page_id)
            metadata_ids.update({get_ipfs_cid(metadata_filepath): page_id})
        # double check metadata files
        for filename in list_dir(self.pages_dir):
            # ignore non-JSON files
            if not filename.endswith(".json"):
                continue
            page_id = filename.strip(".json")
            if page_id not in page_ids:
                raise InvalidDocumentCollectionError(
                    "This metadata file refers to a page which is not under pages."
                )

        self._page_ids = page_ids
        self._metadata_ids = metadata_ids
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

            doc_id = doc_metadata["ipfs_id"]
            if filename != f"{doc_id}.json":
                raise InvalidDocumentCollectionError(
                    "This MultiPageDoc's filename is not its ID"
                )
            if not doc_metadata["pages"]:
                continue
            doc_ids.append(doc_id)

        self._multipagedoc_ids = doc_ids
        return doc_ids
