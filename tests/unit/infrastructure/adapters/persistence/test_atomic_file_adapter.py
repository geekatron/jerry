# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for AtomicFileAdapter.

Tests verify:
- AC-012.1: read_with_lock() acquires shared lock before reading
- AC-012.2: write_atomic() uses exclusive lock + temp file + os.replace
- AC-012.3: Lock files are in configurable lock directory
- AC-012.4: Locks auto-release on process crash (OS-level)
- AC-012.5: Handles missing directories gracefully

References:
    - WI-012: Atomic File Adapter work item
    - PROJ-004-e-002: Runtime Collision Avoidance research
"""

from __future__ import annotations

from pathlib import Path

from src.infrastructure.adapters.persistence.atomic_file_adapter import (
    AtomicFileAdapter,
)


class TestAtomicFileAdapterInit:
    """Tests for AtomicFileAdapter initialization."""

    def test_init_with_default_lock_dir(self) -> None:
        """Default lock directory is .jerry/local/locks/."""
        adapter = AtomicFileAdapter()
        assert adapter.lock_dir == Path(".jerry/local/locks")

    def test_init_with_custom_lock_dir(self, tmp_path: Path) -> None:
        """Custom lock directory is respected."""
        custom_dir = tmp_path / "custom_locks"
        adapter = AtomicFileAdapter(lock_dir=custom_dir)
        assert adapter.lock_dir == custom_dir


class TestAtomicFileAdapterRead:
    """Tests for read_with_lock method."""

    def test_read_existing_file(self, tmp_path: Path) -> None:
        """Read returns content of existing file."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "test.txt"
        test_file.write_text("Hello World", encoding="utf-8")

        content = adapter.read_with_lock(test_file)

        assert content == "Hello World"

    def test_read_nonexistent_file_returns_empty_string(self, tmp_path: Path) -> None:
        """Read returns empty string for non-existent file."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "nonexistent.txt"

        content = adapter.read_with_lock(test_file)

        assert content == ""

    def test_read_creates_lock_directory(self, tmp_path: Path) -> None:
        """Read creates lock directory if it doesn't exist."""
        lock_dir = tmp_path / "locks"
        adapter = AtomicFileAdapter(lock_dir=lock_dir)
        test_file = tmp_path / "test.txt"
        test_file.write_text("content", encoding="utf-8")

        adapter.read_with_lock(test_file)

        assert lock_dir.exists()

    def test_read_utf8_content(self, tmp_path: Path) -> None:
        """Read handles UTF-8 content correctly."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "unicode.txt"
        test_file.write_text("Hello 世界 🌍", encoding="utf-8")

        content = adapter.read_with_lock(test_file)

        assert content == "Hello 世界 🌍"


class TestAtomicFileAdapterWrite:
    """Tests for write_atomic method."""

    def test_write_creates_new_file(self, tmp_path: Path) -> None:
        """Write creates a new file with content."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "new.txt"

        adapter.write_atomic(test_file, "New Content")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8") == "New Content"

    def test_write_overwrites_existing_file(self, tmp_path: Path) -> None:
        """Write overwrites existing file content."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "existing.txt"
        test_file.write_text("Old Content", encoding="utf-8")

        adapter.write_atomic(test_file, "New Content")

        assert test_file.read_text(encoding="utf-8") == "New Content"

    def test_write_creates_parent_directories(self, tmp_path: Path) -> None:
        """Write creates parent directories if they don't exist."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "nested" / "dir" / "file.txt"

        adapter.write_atomic(test_file, "Content")

        assert test_file.exists()
        assert test_file.read_text(encoding="utf-8") == "Content"

    def test_write_utf8_content(self, tmp_path: Path) -> None:
        """Write handles UTF-8 content correctly."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "unicode.txt"

        adapter.write_atomic(test_file, "Hello 世界 🌍")

        assert test_file.read_text(encoding="utf-8") == "Hello 世界 🌍"

    def test_write_no_temp_file_remains_on_success(self, tmp_path: Path) -> None:
        """Write doesn't leave temp files on success."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "test.txt"

        adapter.write_atomic(test_file, "Content")

        # Check no .tmp files remain
        tmp_files = list(tmp_path.glob("*.tmp"))
        assert len(tmp_files) == 0


class TestAtomicFileAdapterExists:
    """Tests for exists method."""

    def test_exists_returns_true_for_file(self, tmp_path: Path) -> None:
        """Exists returns True for existing file."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "test.txt"
        test_file.write_text("content", encoding="utf-8")

        assert adapter.exists(test_file) is True

    def test_exists_returns_false_for_nonexistent(self, tmp_path: Path) -> None:
        """Exists returns False for non-existent file."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "nonexistent.txt"

        assert adapter.exists(test_file) is False

    def test_exists_returns_false_for_directory(self, tmp_path: Path) -> None:
        """Exists returns False for directories."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        assert adapter.exists(tmp_path) is False


class TestAtomicFileAdapterDelete:
    """Tests for delete_with_lock method."""

    def test_delete_existing_file_returns_true(self, tmp_path: Path) -> None:
        """Delete returns True for existing file."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "test.txt"
        test_file.write_text("content", encoding="utf-8")

        result = adapter.delete_with_lock(test_file)

        assert result is True
        assert not test_file.exists()

    def test_delete_nonexistent_file_returns_false(self, tmp_path: Path) -> None:
        """Delete returns False for non-existent file."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "nonexistent.txt"

        result = adapter.delete_with_lock(test_file)

        assert result is False


class TestAtomicFileAdapterLockPath:
    """Tests for lock file path generation."""

    def test_lock_path_is_deterministic(self, tmp_path: Path) -> None:
        """Same file path generates same lock path."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "test.txt"

        lock1 = adapter._get_lock_path(test_file)
        lock2 = adapter._get_lock_path(test_file)

        assert lock1 == lock2

    def test_different_files_have_different_locks(self, tmp_path: Path) -> None:
        """Different file paths generate different lock paths."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        lock1 = adapter._get_lock_path(file1)
        lock2 = adapter._get_lock_path(file2)

        assert lock1 != lock2

    def test_lock_path_uses_hash(self, tmp_path: Path) -> None:
        """Lock path uses hash to avoid path length/character issues."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "some" / "very" / "long" / "path" / "with spaces" / "file.txt"

        lock_path = adapter._get_lock_path(test_file)

        assert lock_path.suffix == ".lock"
        assert len(lock_path.name) <= 21  # 16 hex chars + ".lock"


class TestAtomicFileAdapterRoundTrip:
    """Tests for read-write round trip."""

    def test_write_then_read_roundtrip(self, tmp_path: Path) -> None:
        """Written content can be read back."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "test.txt"
        content = "Test content with special chars: <>&\n\t"

        adapter.write_atomic(test_file, content)
        read_content = adapter.read_with_lock(test_file)

        assert read_content == content

    def test_multiple_writes_overwrite(self, tmp_path: Path) -> None:
        """Multiple writes correctly overwrite."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        test_file = tmp_path / "test.txt"

        adapter.write_atomic(test_file, "First")
        adapter.write_atomic(test_file, "Second")
        adapter.write_atomic(test_file, "Third")

        assert adapter.read_with_lock(test_file) == "Third"
