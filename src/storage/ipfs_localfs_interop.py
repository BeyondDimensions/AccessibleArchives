"""Filesystem functions for both ordinary file systems and IPFS objects."""

import os
import ipfs_api


def is_ipfs_path(path) -> str | None:
    if path.startswith("/ipfs/"):
        return path.split("/")[1]
    return None


def path_exists(path: str):
    # print("Path:", path)
    ipfs_id = is_ipfs_path(path)

    if ipfs_id:

        # check if any specified subfolders/files exist
        try:
            ipfs_api.http_client.ls(path)
        except ipfs_api.ipfshttpclient.exceptions.TimeoutError:
            print(f"Couldn't find the IPFS object {ipfs_id}.")
            return False
        except ipfs_api.ipfshttpclient.exceptions.ErrorResponse as e:
            # if the error message is about a path not existing
            if "no link named" in str(e):
                print(f"The IPFS object {ipfs_id} doesn't have the path {path}.")
                return False
            else:
                # the error message is about something else
                raise e
        return True
    else:  # the path is from the local filesystem
        return os.path.exists(path)


def is_file(path):
    if not path_exists(path):
        raise FileNotFoundError()

    ipfs_id = is_ipfs_path(path)
    if ipfs_id:
        try:
            ipfs_api.read(path)
            return True
        except ipfs_api.ipfshttpclient.exceptions.ErrorResponse as e:
            # if the error message is about the path being a directory
            if "is a directory" in str(e):
                print(f"The IPFS object {ipfs_id} doesn't have the path {path}.")
                return False
            else:
                # the error message is about something else
                raise e
    else:  # the path is from the local filesystem
        return os.path.isfile(path)


def is_dir(path):
    return not is_file(path)


def join_paths(*args):
    if is_ipfs_path(args[0]):
        return "/".join(args).replace("//", "/")
    else:
        return os.path.join(*args)


def list_dir(path):
    if is_file(path):
        raise Exception(f"This path is a file, not a directory: {path}")
    ipfs_id = is_ipfs_path(path)
    if ipfs_id:
        return [item['Name'] for item in ipfs_api.http_client.ls(path)["Objects"][0]['Links']]
    else:
        return os.listdir(path)


def read_file(path):
    if is_dir(path):
        raise Exception(f"This path is a directory, not a file: {path}")
    ipfs_id = is_ipfs_path(path)
    if ipfs_id:
        return ipfs_api.read(path)
    else:
        with open(path, 'rb') as file:
            return file.read()
