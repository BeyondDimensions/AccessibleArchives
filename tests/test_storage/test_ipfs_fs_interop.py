from _load_src import SRC_PATH
from storage.ipfs_localfs_interop import is_file, is_dir, path_exists, join_paths, list_dir, read_file, get_ipfs_cid


import ipfs_api
import os
fs_path = "docs_template"
collection_id = ipfs_api.publish(fs_path)
ipfs_path = f"/ipfs/{collection_id}"
print(collection_id)
assert path_exists("docs_template")
assert path_exists(ipfs_path)

assert not path_exists("false_dir")
# assert not path_exists("/ipfs/QmbHXuQmaEKaZqRmtBvGXxDSLvGJL1KG7fq1qKFAhwR4v3")

assert path_exists(f"{ipfs_path}/Pages")
assert path_exists(f"{ipfs_path}/Pages/QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2.png")

assert path_exists(f"{ipfs_path}/Pages")
assert path_exists(f"{ipfs_path}/Pages/QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2.png")

assert path_exists(os.path.join(fs_path, "Pages"))
assert path_exists(os.path.join(
    fs_path, "Pages", "QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2.png"
))

assert not path_exists(f"{ipfs_path}/Pagess")
assert not path_exists(f"{ipfs_path}/Pages/QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ3.png")

assert not path_exists(os.path.join(fs_path, "Pagess"))
assert not path_exists(os.path.join(
    fs_path, "Pages", "QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ3.png"
))


assert is_dir(ipfs_path)
assert is_file(f"{ipfs_path}/Pages/QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2.png")


assert join_paths("/ipfs/QmUUPdYEPa1wn5SaptPBx3nz9P8aXzbHVTupXNRqsLXZwL/", "Pages",
                  "QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ3.png") == "/ipfs/QmUUPdYEPa1wn5SaptPBx3nz9P8aXzbHVTupXNRqsLXZwL/Pages/QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ3.png"
print(list_dir(fs_path))
print(list_dir(ipfs_path))
assert list_dir(fs_path) == list_dir(ipfs_path)
assert (
    read_file(
        f"{ipfs_path}/Pages/QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2.png"
    ) ==
    read_file(os.path.join(
        fs_path, "Pages", "QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2.png"
    ))
)


assert is_file(f"{ipfs_path}/Pages/QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2.png")
assert get_ipfs_cid(ipfs_path) == collection_id
assert get_ipfs_cid(
    f"{ipfs_path}/Pages/QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2.png") == "QmYZWkFRHWWDV1L98bj7aoWdi6ucz3j1SFZqgFgCtUHuJ2"
