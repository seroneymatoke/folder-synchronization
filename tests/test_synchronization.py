# Created by seroney
# Date: 13/08/2023
# Time: 17:40
# Purpose: 
# Implementation:
# TestData:

import os
import time

import pytest
from src.synchronizer import compute_md5, copy_file, sync_folders

# Basic tests

def test_compute_md5(tmp_path):
    content = "Hello, World!"
    file_path = tmp_path / "test.txt"
    file_path.write_text(content)
    known_md5 = "65a8e27d8879283831b664bd8b7f0ad4"
    assert compute_md5(file_path) == known_md5

def test_copy_file(tmp_path):
    source = tmp_path / "source.txt"
    replica = tmp_path / "replica.txt"
    source.write_text("Testing content")
    copy_file(source, replica)
    assert source.read_text() == replica.read_text()

# Comprehensive sync_folders tests

def test_sync_empty_replica(tmp_path):
    source = tmp_path / "source"
    replica = tmp_path / "replica"
    source.mkdir()
    (source / "file.txt").write_text("content")
    sync_folders(source, replica)
    assert (replica / "file.txt").exists()


def test_sync_additional_files_in_replica(tmp_path):
    source = tmp_path / "source"
    replica = tmp_path / "replica"
    source.mkdir()
    replica.mkdir()
    (source / "file1.txt").write_text("content")
    (replica / "file2.txt").write_text("additional content")
    sync_folders(source, replica)
    assert not (replica / "file2.txt").exists()


def test_sync_modified_files_in_source(tmp_path):
    source = tmp_path / "source"
    replica = tmp_path / "replica"
    source.mkdir()
    replica.mkdir()
    (source / "file.txt").write_text("new content")
    (replica / "file.txt").write_text("old content")
    sync_folders(source, replica)
    assert (replica / "file.txt").read_text() == "new content"


def test_sync_modified_files_in_replica(tmp_path):
    source = tmp_path / "source"
    replica = tmp_path / "replica"
    source.mkdir()
    replica.mkdir()
    (source / "file.txt").write_text("content")
    (replica / "file.txt").write_text("modified content")
    sync_folders(source, replica)
    assert (replica / "file.txt").read_text() == "content"


def test_sync_nested_directories(tmp_path):
    source = tmp_path / "source"
    replica = tmp_path / "replica"
    nested_dir = source / "dir1" / "dir2"
    nested_dir.mkdir(parents=True)
    (nested_dir / "file.txt").write_text("nested content")
    sync_folders(source, replica)
    assert (replica / "dir1" / "dir2" / "file.txt").exists()


def slow_copy_file(source_path, replica_path):
    """Artificially slowed down version of the copy_file function for testing purposes."""
    time.sleep(2)  # 2 seconds delay
    copy_file(source_path, replica_path)


def test_parallel_sync(tmp_path, monkeypatch):
    """Tests the parallel synchronization of the folders."""
    # Monkeypatch the slow copy_file function for this test
    monkeypatch.setattr('src.synchronizer.copy_file', slow_copy_file)

    source = tmp_path / "source"
    replica = tmp_path / "replica"
    source.mkdir()
    for i in range(4):  # Create 4 files
        (source / f"file{i}.txt").write_text(f"content{i}")

    start_time = time.time()

    # Synchronize with parallelism
    sync_folders(source, replica, max_workers=4)

    elapsed_time = time.time() - start_time

    # If the files were processed concurrently, the elapsed time should be roughly
    # the time of a single file copy (2 seconds) plus some overhead.
    # Let's assume overhead can be at most another 2 seconds.
    assert elapsed_time < 4



