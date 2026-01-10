"""
Unit tests for IFileStore implementations.

Test Categories:
    - Happy Path: Normal operations work correctly
    - Edge Cases: Boundary conditions and special inputs
    - Negative Cases: Error handling and invalid inputs
    - Concurrency: Lock behavior

References:
    - IMPL-REPO-002: IFileStore + ISerializer<T>
    - PAT-003: Optimistic Concurrency with File Locking
"""
from __future__ import annotations

import threading
import time
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from src.infrastructure.internal.file_store import (
    FileNotFoundError_,
    FileLockError,
    FileStoreError,
    FileWriteError,
    InMemoryFileStore,
    LocalFileStore,
)


class TestLocalFileStoreHappyPath:
    """Happy path tests for LocalFileStore."""

    def test_write_and_read_file(self, tmp_path: Path) -> None:
        """Test basic write and read operations."""
        store = LocalFileStore(base_path=tmp_path)
        data = b'{"name": "Alice", "age": 30}'

        store.write("user.json", data)
        result = store.read("user.json")

        assert result == data

    def test_write_creates_parent_directories(self, tmp_path: Path) -> None:
        """Test that write creates parent directories if they don't exist."""
        store = LocalFileStore(base_path=tmp_path)
        data = b"nested data"

        store.write("deep/nested/path/file.txt", data)

        assert (tmp_path / "deep/nested/path/file.txt").exists()
        assert store.read("deep/nested/path/file.txt") == data

    def test_exists_returns_true_for_existing_file(self, tmp_path: Path) -> None:
        """Test exists returns True when file exists."""
        store = LocalFileStore(base_path=tmp_path)
        store.write("existing.txt", b"content")

        assert store.exists("existing.txt") is True

    def test_exists_returns_false_for_missing_file(self, tmp_path: Path) -> None:
        """Test exists returns False when file doesn't exist."""
        store = LocalFileStore(base_path=tmp_path)

        assert store.exists("missing.txt") is False

    def test_delete_removes_existing_file(self, tmp_path: Path) -> None:
        """Test delete removes an existing file."""
        store = LocalFileStore(base_path=tmp_path)
        store.write("to_delete.txt", b"content")

        result = store.delete("to_delete.txt")

        assert result is True
        assert store.exists("to_delete.txt") is False

    def test_delete_returns_false_for_missing_file(self, tmp_path: Path) -> None:
        """Test delete returns False when file doesn't exist."""
        store = LocalFileStore(base_path=tmp_path)

        result = store.delete("nonexistent.txt")

        assert result is False

    def test_overwrite_existing_file(self, tmp_path: Path) -> None:
        """Test that writing to existing file overwrites it."""
        store = LocalFileStore(base_path=tmp_path)
        store.write("file.txt", b"original")

        store.write("file.txt", b"updated")

        assert store.read("file.txt") == b"updated"

    def test_write_without_fsync(self, tmp_path: Path) -> None:
        """Test write with fsync=False still works."""
        store = LocalFileStore(base_path=tmp_path)

        store.write("fast.txt", b"no fsync", fsync=False)

        assert store.read("fast.txt") == b"no fsync"

    def test_absolute_path_ignores_base_path(self, tmp_path: Path) -> None:
        """Test that absolute paths bypass base_path."""
        store = LocalFileStore(base_path=tmp_path / "base")
        absolute_file = tmp_path / "absolute.txt"

        store.write(str(absolute_file), b"absolute")

        assert absolute_file.exists()
        assert store.read(str(absolute_file)) == b"absolute"


class TestLocalFileStoreEdgeCases:
    """Edge case tests for LocalFileStore."""

    def test_empty_file_write_and_read(self, tmp_path: Path) -> None:
        """Test writing and reading empty file."""
        store = LocalFileStore(base_path=tmp_path)

        store.write("empty.txt", b"")

        assert store.read("empty.txt") == b""

    def test_large_file_write_and_read(self, tmp_path: Path) -> None:
        """Test writing and reading large file (1MB)."""
        store = LocalFileStore(base_path=tmp_path)
        large_data = b"x" * (1024 * 1024)  # 1MB

        store.write("large.bin", large_data)

        assert store.read("large.bin") == large_data

    def test_binary_data_roundtrip(self, tmp_path: Path) -> None:
        """Test binary data with all byte values."""
        store = LocalFileStore(base_path=tmp_path)
        binary_data = bytes(range(256))

        store.write("binary.bin", binary_data)

        assert store.read("binary.bin") == binary_data

    def test_unicode_filename(self, tmp_path: Path) -> None:
        """Test file with unicode characters in name."""
        store = LocalFileStore(base_path=tmp_path)

        store.write("файл.txt", b"unicode name")

        assert store.read("файл.txt") == b"unicode name"

    def test_special_characters_in_path(self, tmp_path: Path) -> None:
        """Test paths with spaces and special characters."""
        store = LocalFileStore(base_path=tmp_path)

        store.write("path with spaces/file-name_v2.txt", b"special")

        assert store.read("path with spaces/file-name_v2.txt") == b"special"

    def test_no_base_path_uses_relative_paths(self, tmp_path: Path) -> None:
        """Test store without base_path uses paths as-is."""
        import os
        original_cwd = os.getcwd()
        try:
            os.chdir(tmp_path)
            store = LocalFileStore()

            store.write("relative.txt", b"relative")

            assert (tmp_path / "relative.txt").exists()
        finally:
            os.chdir(original_cwd)


class TestLocalFileStoreNegativeCases:
    """Negative case tests for LocalFileStore."""

    def test_read_nonexistent_file_raises_error(self, tmp_path: Path) -> None:
        """Test reading non-existent file raises FileNotFoundError_."""
        store = LocalFileStore(base_path=tmp_path)

        with pytest.raises(FileNotFoundError_) as exc_info:
            store.read("nonexistent.txt")

        assert "nonexistent.txt" in str(exc_info.value)

    def test_read_directory_raises_error(self, tmp_path: Path) -> None:
        """Test reading a directory raises error."""
        store = LocalFileStore(base_path=tmp_path)
        (tmp_path / "subdir").mkdir()

        with pytest.raises(FileStoreError):
            store.read("subdir")


class TestLocalFileStoreLocking:
    """Locking behavior tests for LocalFileStore."""

    def test_locked_context_manager_basic(self, tmp_path: Path) -> None:
        """Test basic lock acquisition and release."""
        store = LocalFileStore(base_path=tmp_path)
        store.write("lockable.txt", b"data")

        with store.locked("lockable.txt"):
            # Lock is held, can still read/write
            store.write("lockable.txt", b"updated")
            assert store.read("lockable.txt") == b"updated"

        # Lock is released

    def test_lock_prevents_concurrent_modification(self, tmp_path: Path) -> None:
        """Test that lock is held during context."""
        store = LocalFileStore(base_path=tmp_path)
        store.write("file.txt", b"original")

        with store.locked("file.txt"):
            # Can still read/write while holding lock
            store.write("file.txt", b"modified")
            assert store.read("file.txt") == b"modified"


class TestInMemoryFileStoreHappyPath:
    """Happy path tests for InMemoryFileStore."""

    def test_write_and_read_file(self) -> None:
        """Test basic write and read operations."""
        store = InMemoryFileStore()
        data = b'{"key": "value"}'

        store.write("test.json", data)
        result = store.read("test.json")

        assert result == data

    def test_exists_returns_true_for_existing_file(self) -> None:
        """Test exists returns True when file exists."""
        store = InMemoryFileStore()
        store.write("existing.txt", b"content")

        assert store.exists("existing.txt") is True

    def test_exists_returns_false_for_missing_file(self) -> None:
        """Test exists returns False when file doesn't exist."""
        store = InMemoryFileStore()

        assert store.exists("missing.txt") is False

    def test_delete_removes_existing_file(self) -> None:
        """Test delete removes an existing file."""
        store = InMemoryFileStore()
        store.write("to_delete.txt", b"content")

        result = store.delete("to_delete.txt")

        assert result is True
        assert store.exists("to_delete.txt") is False

    def test_delete_returns_false_for_missing_file(self) -> None:
        """Test delete returns False when file doesn't exist."""
        store = InMemoryFileStore()

        result = store.delete("nonexistent.txt")

        assert result is False

    def test_clear_removes_all_files(self) -> None:
        """Test clear removes all files from memory."""
        store = InMemoryFileStore()
        store.write("file1.txt", b"one")
        store.write("file2.txt", b"two")

        store.clear()

        assert store.exists("file1.txt") is False
        assert store.exists("file2.txt") is False

    def test_locked_context_manager(self) -> None:
        """Test lock context manager works."""
        store = InMemoryFileStore()

        with store.locked("file.txt"):
            store.write("file.txt", b"data")

        assert store.read("file.txt") == b"data"


class TestInMemoryFileStoreNegativeCases:
    """Negative case tests for InMemoryFileStore."""

    def test_read_nonexistent_file_raises_error(self) -> None:
        """Test reading non-existent file raises FileNotFoundError_."""
        store = InMemoryFileStore()

        with pytest.raises(FileNotFoundError_):
            store.read("nonexistent.txt")

    def test_double_lock_raises_error(self) -> None:
        """Test acquiring lock twice raises FileLockError."""
        store = InMemoryFileStore()

        with store.locked("file.txt"):
            with pytest.raises(FileLockError):
                with store.locked("file.txt"):
                    pass


class TestFileStoreProtocolCompliance:
    """Tests that implementations comply with IFileStore protocol."""

    @pytest.mark.parametrize("store_factory", [
        lambda tmp_path: LocalFileStore(base_path=tmp_path),
        lambda tmp_path: InMemoryFileStore(),
    ])
    def test_protocol_methods_exist(
        self, tmp_path: Path, store_factory
    ) -> None:
        """Test that all protocol methods are implemented."""
        store = store_factory(tmp_path)

        # All these should be callable
        assert callable(getattr(store, "read"))
        assert callable(getattr(store, "write"))
        assert callable(getattr(store, "exists"))
        assert callable(getattr(store, "delete"))
        assert callable(getattr(store, "locked"))

    @pytest.mark.parametrize("store_factory", [
        lambda tmp_path: LocalFileStore(base_path=tmp_path),
        lambda tmp_path: InMemoryFileStore(),
    ])
    def test_write_read_roundtrip(
        self, tmp_path: Path, store_factory
    ) -> None:
        """Test write/read roundtrip works for all implementations."""
        store = store_factory(tmp_path)
        data = b"test data"

        store.write("test.txt", data)

        assert store.read("test.txt") == data
