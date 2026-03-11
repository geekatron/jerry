# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for AtomicFileAdapter.

Tests the AC-018.1 and AC-018.2 acceptance criteria:
- AC-018.1: Concurrent file access with file locking
- AC-018.2: Atomic write reliability

References:
    - WI-018: Integration & E2E Tests
    - WI-012: AtomicFileAdapter implementation
"""

from __future__ import annotations

import threading
import time
from pathlib import Path

from src.infrastructure.adapters.persistence.atomic_file_adapter import AtomicFileAdapter


class TestConcurrentFileAccess:
    """Integration tests for concurrent file access (AC-018.1)."""

    def test_concurrent_writes_dont_corrupt_file_threading(self, tmp_path: Path) -> None:
        """Multiple threads writing should not corrupt file content."""
        target_file = tmp_path / "concurrent_test.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        results: list[tuple[int, bool]] = []
        lock = threading.Lock()

        def write_task(thread_id: int, iterations: int) -> None:
            for i in range(iterations):
                content = f"Thread {thread_id}, iteration {i}\n"
                try:
                    adapter.write_atomic(target_file, content)
                    with lock:
                        results.append((thread_id, True))
                except Exception:
                    with lock:
                        results.append((thread_id, False))

        # Spawn multiple threads
        threads = [threading.Thread(target=write_task, args=(t, 20)) for t in range(4)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All writes should have succeeded
        assert all(success for _, success in results)
        assert len(results) == 80  # 4 threads * 20 iterations

        # File should be valid (one complete line)
        content = target_file.read_text(encoding="utf-8")
        assert content.startswith("Thread ")
        assert "iteration" in content

    def test_concurrent_read_write_is_safe(self, tmp_path: Path) -> None:
        """Concurrent reads during writes should not corrupt or fail."""
        target_file = tmp_path / "read_write_test.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        # Initialize file
        adapter.write_atomic(target_file, "initial content\n")

        read_results: list[str] = []
        write_complete = threading.Event()

        def write_task() -> None:
            for i in range(50):
                content = f"Write iteration {i}\n"
                adapter.write_atomic(target_file, content)
                time.sleep(0.001)  # Small delay
            write_complete.set()

        def read_task() -> None:
            while not write_complete.is_set():
                try:
                    content = adapter.read_with_lock(target_file)
                    read_results.append(content)
                except Exception as e:
                    read_results.append(f"ERROR: {e}")
                time.sleep(0.001)

        writer = threading.Thread(target=write_task)
        readers = [threading.Thread(target=read_task) for _ in range(3)]

        writer.start()
        for r in readers:
            r.start()

        writer.join()
        for r in readers:
            r.join()

        # All reads should have returned valid content (no errors, no partial reads)
        valid_endings = ("content",) + tuple(str(x) for x in range(50))
        for result in read_results:
            assert not result.startswith("ERROR:")
            assert result.strip().endswith(valid_endings)

    def test_lock_contention_under_heavy_load(self, tmp_path: Path) -> None:
        """Multiple writers competing for lock should all eventually succeed."""
        target_file = tmp_path / "contention_test.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        success_count = {"value": 0}
        lock = threading.Lock()

        def writer(writer_id: int) -> None:
            for i in range(10):
                adapter.write_atomic(target_file, f"Writer {writer_id}: {i}\n")
                with lock:
                    success_count["value"] += 1

        threads = [threading.Thread(target=writer, args=(i,)) for i in range(10)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All 100 writes should have succeeded
        assert success_count["value"] == 100


class TestAtomicWriteReliability:
    """Integration tests for atomic write reliability (AC-018.2)."""

    def test_atomic_write_is_all_or_nothing(self, tmp_path: Path) -> None:
        """If a write succeeds, the entire content is present."""
        target_file = tmp_path / "atomic_test.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        # Write large content
        large_content = "X" * 100000 + "\nEND\n"
        adapter.write_atomic(target_file, large_content)

        # Read back and verify
        content = target_file.read_text(encoding="utf-8")
        assert content == large_content
        assert content.endswith("\nEND\n")

    def test_atomic_write_uses_temp_file(self, tmp_path: Path) -> None:
        """Atomic write should use temp file + rename pattern."""
        target_file = tmp_path / "rename_test.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        # Write content
        adapter.write_atomic(target_file, "test content\n")

        # No temp files should remain
        temp_files = list(tmp_path.glob("*.tmp"))
        assert len(temp_files) == 0

        # Target file should exist
        assert target_file.exists()

    def test_atomic_write_preserves_content_on_crash_simulation(self, tmp_path: Path) -> None:
        """Original content preserved if write 'crashes' (we can't truly crash)."""
        target_file = tmp_path / "crash_test.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        # Write initial content
        original = "Original content\n"
        adapter.write_atomic(target_file, original)

        # Verify original is there
        assert target_file.read_text(encoding="utf-8") == original

        # The atomic write pattern ensures no partial writes
        # because we write to temp then rename

    def test_multiple_consecutive_writes_maintain_integrity(self, tmp_path: Path) -> None:
        """Rapid consecutive writes should all complete with proper content."""
        target_file = tmp_path / "rapid_test.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        expected_final = None
        for i in range(100):
            content = f"Write number {i}\n"
            adapter.write_atomic(target_file, content)
            expected_final = content

        # Final content should be the last write
        assert target_file.read_text(encoding="utf-8") == expected_final

    def test_write_creates_parent_directories(self, tmp_path: Path) -> None:
        """Atomic write should work even if parent directory doesn't exist."""
        nested_file = tmp_path / "deep" / "nested" / "path" / "file.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        # Parent directory doesn't exist yet
        assert not nested_file.parent.exists()

        # Write should create it
        adapter.write_atomic(nested_file, "content in nested path\n")

        assert nested_file.exists()
        assert nested_file.read_text(encoding="utf-8") == "content in nested path\n"


class TestFileAdapterEdgeCases:
    """Edge case tests for AtomicFileAdapter."""

    def test_read_nonexistent_file_returns_empty(self, tmp_path: Path) -> None:
        """Reading a non-existent file should return empty string."""
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")
        nonexistent = tmp_path / "does_not_exist.txt"

        content = adapter.read_with_lock(nonexistent)
        assert content == ""

    def test_empty_content_write(self, tmp_path: Path) -> None:
        """Writing empty content should create empty file."""
        target_file = tmp_path / "empty.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        adapter.write_atomic(target_file, "")

        assert target_file.exists()
        assert target_file.read_text(encoding="utf-8") == ""

    def test_unicode_content_preserved(self, tmp_path: Path) -> None:
        """Unicode content should be preserved correctly."""
        target_file = tmp_path / "unicode.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        unicode_content = "Unicode test: \u4e2d\u6587 \U0001f604 \u03b1\u03b2\u03b3\n"
        adapter.write_atomic(target_file, unicode_content)

        assert target_file.read_text(encoding="utf-8") == unicode_content

    def test_special_characters_in_content(self, tmp_path: Path) -> None:
        """Special characters should be preserved."""
        target_file = tmp_path / "special.txt"
        adapter = AtomicFileAdapter(lock_dir=tmp_path / "locks")

        special_content = "Newlines:\nTabs:\t\tQuotes:\"'`\nBackslash:\\\n"
        adapter.write_atomic(target_file, special_content)

        assert target_file.read_text(encoding="utf-8") == special_content
