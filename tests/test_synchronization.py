# Created by seroney
# Date: 13/08/2023
# Time: 17:40
# Purpose: 
# Implementation:
# TestData:

import os
import shutil
import random
import string
import time

import pytest

from src.synchronizer import sync_folders
from tqdm import tqdm


def random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@pytest.fixture
def setup_folders(tmpdir, large=False):
    source = tmpdir.mkdir("source")
    replica = tmpdir.mkdir("replica")

    file_count = 1000 if large else 5
    for _ in range(file_count):
        file = source.join(random_string() + ".txt")
        file.write("content")

    return str(source), str(replica)


def test_sync_folders_basic(setup_folders):
    source, replica = setup_folders

    sync_folders(source, replica)
    source_files = {f.basename for f in source.listdir()}
    replica_files = {f.basename for f in replica.listdir()}

    assert source_files == replica_files, "Files in source and replica should match after synchronization."


def test_sync_folders_removal(setup_folders):
    source, replica = setup_folders

    # Remove a file from the source
    file_to_remove = random.choice(source.listdir())
    os.remove(file_to_remove)

    sync_folders(source, replica)

    assert not replica.join(
        file_to_remove.basename).check(), "Removed file from source should not be present in replica."


def test_parallel_sync_performance(setup_folders):
    source, replica = setup_folders(large=True)

    # Synchronization without parallelism
    start_time = time.time()
    sync_folders(source, replica, max_workers=1)
    non_parallel_duration = time.time() - start_time

    # Clear replica and synchronize with parallelism
    shutil.rmtree(replica)
    os.makedirs(replica)
    start_time = time.time()
    sync_folders(source, replica)
    parallel_duration = time.time() - start_time

    assert parallel_duration < non_parallel_duration, "Parallel synchronization should be faster."
