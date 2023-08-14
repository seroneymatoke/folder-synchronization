# Created by seroney
# Date: 12/08/2023
# Time: 14:50
# Purpose:
# Implementation:
# TestData:
import os
import logging
import shutil
import hashlib
from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm


def compute_md5(file_path):
    """
    Compute the MD5 hash of a file.

    Args:
    - file_path (str): Path to the file.

    Returns:
    - str: MD5 hash of the file content.
    """
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def copy_file(source_path, replica_path):
    """
    Copy a file from source to replica and verify its integrity using MD5.

    Args:
    - source_path (str): Path to the source file.
    - replica_path (str): Path to the destination in the replica.
    """
    shutil.copy2(source_path, replica_path)  # Using copy2 to also copy metadata
    if compute_md5(source_path) != compute_md5(replica_path):
        logging.error(f"MD5 mismatch after copying {source_path} to {replica_path}.")
        raise ValueError("File integrity verification after copying failed!")


def sync_folders(source, replica, max_workers=None):
    """
    Synchronize content of the source folder with the replica folder.

    Args:
        source (str): Path to the source directory.
        replica (str): Path to the replica directory.
        max_workers (int, optional): Maximum number of worker threads for parallelism.
    """
    if not os.path.exists(replica):
        os.makedirs(replica)

    # Calculate total files for progress bar
    total_files = sum([len(files) for _, _, files in os.walk(source)])

    with tqdm(total=total_files, desc="Syncing", unit="file") as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for dirpath, dirnames, filenames in os.walk(source):
                for filename in filenames:
                    source_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(source_path, source)
                    replica_path = os.path.join(replica, rel_path)

                    # Ensure parent directory exists in the replica
                    replica_dir = os.path.dirname(replica_path)
                    if not os.path.exists(replica_dir):
                        os.makedirs(replica_dir)

                    # Check if file exists and compare md5
                    # If they are different or file doesn't exist in replica, copy it
                    if not os.path.exists(replica_path) or compute_md5(source_path) != compute_md5(replica_path):
                        executor.submit(copy_file, source_path, replica_path)
                        logging.info(f"Synced: {source_path} to {replica_path}")

                    # Update progress bar after submitting a job
                    pbar.update(1)

            # Remove files/folders in replica not in source
            for dirpath, dirnames, filenames in os.walk(replica, topdown=False):
                for filename in filenames:
                    replica_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(replica_path, replica)
                    source_path = os.path.join(source, rel_path)

                    if not os.path.exists(source_path):
                        try:
                            os.remove(replica_path)
                            logging.info(f"Removed file: {replica_path}")
                        except Exception as e:
                            logging.error(f"Failed to remove {replica_path}. Error: {e}")

                for dirname in dirnames:
                    replica_dir_path = os.path.join(dirpath, dirname)
                    rel_dir_path = os.path.relpath(replica_dir_path, replica)
                    source_dir_path = os.path.join(source, rel_dir_path)

                    if not os.path.exists(source_dir_path) and not os.listdir(replica_dir_path):
                        try:
                            os.rmdir(replica_dir_path)
                            logging.info(f"Removed directory: {replica_dir_path}")
                        except Exception as e:
                            logging.error(f"Failed to remove directory {replica_dir_path}. Error: {e}")
