"""Generate page metadata JSON for a page with an empty transcript"""
import json
from datetime import datetime, UTC

original_medium = "Photocopy of Folder from BSTU"
ipfs_id = "Qmbfr5UHN7SYmVxjYjEb6LbLsdaetshJyc12rWhShkgBh5"

empty_file_ipfs_id = "QmWunHCTcgMPYEDxvqogR6pyEDheKdKUbrc6hmRjv3H8w9"
transcript_id = empty_file_ipfs_id
metadata = {
    "ipfs_id": ipfs_id,
    "transcripts": [{
        "ipfs_id": transcript_id,
        "transcriber": "ChatGPT-4o-2024-08-06",
        "timestamp": datetime.now(UTC).isoformat()
    }],
    "content": {

    },
    "source": {
        "original_medium": original_medium,
        "digitisation_date": datetime.now(UTC).isoformat(),
        "digitiser": "anonymous"
    },
    "format": "png"
}
json.dumps(metadata)
