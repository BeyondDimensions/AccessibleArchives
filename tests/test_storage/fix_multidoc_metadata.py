"""Take a folder of MultiPageDoc JOSN files where the pages field has
Page IDs instead of Page-Metada IDs and correct those."""
import _load_src
import json
import ipfs_api
import os
import shutil
from utils.utils import ensure_dir_exists
bad_multipagedoc_json_dir = "/media/llearuin/EXT/curated_files/BadMPD-Files"
fixed_multipagedoc_json_dir = ensure_dir_exists(
    "/media/llearuin/EXT/curated_files/BadMPD-Files-FIXED"
)
pages_dir = "/media/llearuin/EXT/curated_files/Pages"
fixed_count = 0
skipped_count = 0

for filename in os.listdir(bad_multipagedoc_json_dir):
    metadata_path = os.path.join(bad_multipagedoc_json_dir, filename)
    with open(metadata_path, "r") as file:
        metadata = json.loads(file.read())
    new_metadata_ids = []
    for ipfs_id in metadata["pages"]:
        print(ipfs_id)
        page_path = os.path.join(pages_dir, ipfs_id+".png")
        if os.path.exists(page_path):
            fixed_count += 1
            new_metadata_ids.append(ipfs_api.publish(page_path))
        else:
            new_metadata_ids.append(ipfs_id)
            skipped_count += 1
    metadata["pages"] = new_metadata_ids
    with open(os.path.join(fixed_multipagedoc_json_dir, filename), "w+") as file:
        file.write(json.dumps(metadata))


print("fixed_count:", fixed_count)
print("skipped_count:", skipped_count)
