# Created by seroney
# Date: 12/08/2023
# Time: 14:50

import os
import logging
import shutil
import hashlib
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def compute_md5(file_path):
    """
    Computes and returns the MD5 hash of a given file.

    Args:
    - file_path (str): The path to the file for which the MD5 hash is computed.

    Returns:
    - str: MD5 hash of the file content.
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        # Read the file in chunks and update the hash.
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def copy_file(source_path, replica_path):
    """
    Copies a file from source to replica and then verifies its integrity using MD5 hash.

    Args:
    - source_path (str): The path to the source file.
    - replica_path (str): The destination path in the replica.
    """
    # Copy the file including its metadata.
    shutil.copy2(source_path, replica_path)

    # Verify that the source and replica files are identical.
    if compute_md5(source_path) != compute_md5(replica_path):
        logging.error(f"MD5 mismatch after copying {source_path} to {replica_path}.")
        raise ValueError("File integrity verification after copying failed!")


def count_deletions(source, replica):
    """
    Counts the number of items (files and directories) in the replica that don't exist in the source.

    Args:
    - source (str): Path to the source directory.
    - replica (str): Path to the replica directory.

    Returns:
    - int: Count of items in replica not present in source.
    """
    count = 0
    for dirpath, dirnames, filenames in os.walk(replica):
        for filename in filenames:
            replica_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(replica_path, replica)
            source_path = os.path.join(source, rel_path)
            if not os.path.exists(source_path):
                count += 1

        for dirname in dirnames:
            replica_dir_path = os.path.join(dirpath, dirname)
            rel_dir_path = os.path.relpath(replica_dir_path, replica)
            source_dir_path = os.path.join(source, rel_dir_path)
            if not os.path.exists(source_dir_path):
                count += 1
    return count


def sync_folders(source, replica, max_workers=None):
    """
    Synchronizes content of the source folder with the replica folder. If a file exists in the source but not
    in the replica, it is copied over. If a file exists in the replica but not in the source, it is deleted.

    Args:
    - source (str): Path to the source directory.
    - replica (str): Path to the replica directory.
    - max_workers (int, optional): Maximum number of worker threads for parallelism.
    """
    # Create the replica directory if it doesn't exist.
    if not os.path.exists(replica):
        os.makedirs(replica)

    # Calculate the number of files in the source for the progress bar.
    total_files = sum([len(files) for _, _, files in os.walk(source)])

    # Copying files from source to replica with a progress bar.
    with tqdm(total=total_files, desc="Syncing", unit="file") as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for dirpath, dirnames, filenames in os.walk(source):
                for filename in filenames:
                    source_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(source_path, source)
                    replica_path = os.path.join(replica, rel_path)
                    replica_dir = os.path.dirname(replica_path)

                    # Ensure the directory structure in the replica matches the source.
                    if not os.path.exists(replica_dir):
                        os.makedirs(replica_dir)

                    # If file doesn't exist in replica or is different, copy it.
                    if not os.path.exists(replica_path) or compute_md5(source_path) != compute_md5(replica_path):
                        executor.submit(copy_file, source_path, replica_path)
                        logging.info(f"Synced: {source_path} to {replica_path}")

                    pbar.update(1)

    # Removing files from replica not present in source with a progress bar.
    total_deletions = count_deletions(source, replica)
    with tqdm(total=total_deletions, desc="Deleting", unit="item") as pbar:
        for dirpath, dirnames, filenames in os.walk(replica, topdown=False):
            for filename in filenames:
                replica_path = os.path.join(dirpath, filename)
                rel_path = os.path.relpath(replica_path, replica)
                source_path = os.path.join(source, rel_path)

                # Remove files in replica that aren't in source.
                if not os.path.exists(source_path):
                    try:
                        os.remove(replica_path)
                        logging.info(f"Removed file: {replica_path}")
                        pbar.update(1)
                    except Exception as e:
                        logging.error(f"Failed to remove {replica_path}. Error: {e}")

            for dirname in dirnames:
                replica_dir_path = os.path.join(dirpath, dirname)
                rel_dir_path = os.path.relpath(replica_dir_path, replica)

                source_dir_path = os.path.join(source, rel_dir_path)

                # Remove empty directories in replica that aren't in source.
                if not os.path.exists(source_dir_path) and not os.listdir(replica_dir_path):
                    try:
                        os.rmdir(replica_dir_path)
                        logging.info(f"Removed directory: {replica_dir_path}")
                        pbar.update(1)
                    except Exception as e:
                        logging.error(f"Failed to remove directory {replica_dir_path}. Error: {e}")


