"""Take a folder of MultiPageDoc JOSN files where the pages field has
Page IDs instead of Page-Metada IDs and correct those."""
import _load_src
import json
import ipfs_api
import os
import shutil
from utils.utils import ensure_dir_exists
bad_multipagedoc_json_dir = "/tmp/MyTemp/BadMPD-Files"
fixed_multipagedoc_json_dir = ensure_dir_exists(
    "/tmp/MyTemp/BadMPD-Files-FIXED"
)
pages_dir = "/tmp/MyTemp/Pages"
page_metadata_dir = "/tmp/MyTemp/PageMetadata"
fixed_count = 0
skipped_count = 0

for filename in os.listdir(bad_multipagedoc_json_dir):
    doc_json_path = os.path.join(bad_multipagedoc_json_dir, filename)
    with open(doc_json_path, "r") as file:
        metadata = json.loads(file.read())
    new_metadata_ids = []
    for ipfs_id in metadata["pages"]:
        print(ipfs_id)
        page_path = os.path.join(pages_dir, ipfs_id+".png")
        if os.path.exists(page_path):
            page_metadata_path = os.path.join(page_metadata_dir, ipfs_id+".json")
            fixed_count += 1
            new_metadata_ids.append(ipfs_api.predict_cid(page_metadata_path))
        else:
            new_metadata_ids.append(ipfs_id)
            skipped_count += 1
    metadata["pages"] = new_metadata_ids
    with open(os.path.join(fixed_multipagedoc_json_dir, filename), "w+") as file:
        file.write(json.dumps(metadata))


print("fixed_count:", fixed_count)
print("skipped_count:", skipped_count)
