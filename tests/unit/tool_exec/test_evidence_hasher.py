# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for EvidenceHasher."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from src.tool_exec.domain.services.evidence_hasher import EvidenceHasher


class TestEvidenceHasher:
    """Tests for SHA-256 hashing operations."""

    def setup_method(self) -> None:
        """Create a fresh hasher."""
        self.hasher = EvidenceHasher()

    def test_hash_string_deterministic(self) -> None:
        """Same string always produces the same hash."""
        content = "hello world"
        h1 = self.hasher.hash_string(content)
        h2 = self.hasher.hash_string(content)
        assert h1 == h2

    def test_hash_string_correct_value(self) -> None:
        """Hash matches Python's hashlib directly."""
        content = "test content"
        expected = hashlib.sha256(content.encode("utf-8")).hexdigest()
        assert self.hasher.hash_string(content) == expected

    def test_hash_string_is_64_hex_chars(self) -> None:
        """SHA-256 hex digest is always 64 characters."""
        h = self.hasher.hash_string("any content")
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)

    def test_hash_bytes(self) -> None:
        """Bytes hashing matches expected value."""
        data = b"binary data"
        expected = hashlib.sha256(data).hexdigest()
        assert self.hasher.hash_bytes(data) == expected

    def test_hash_file(self, tmp_path: Path) -> None:
        """File hashing matches content hashing."""
        content = "file content for hashing"
        file_path = tmp_path / "test.txt"
        file_path.write_text(content, encoding="utf-8")

        file_hash = self.hasher.hash_file(str(file_path))
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        assert file_hash == content_hash

    def test_hash_file_not_found(self) -> None:
        """Missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            self.hasher.hash_file("/nonexistent/path/file.txt")

    def test_hash_empty_string(self) -> None:
        """Empty string produces the known SHA-256 empty hash."""
        expected = hashlib.sha256(b"").hexdigest()
        assert self.hasher.hash_string("") == expected

    def test_different_content_different_hash(self) -> None:
        """Different content produces different hashes."""
        h1 = self.hasher.hash_string("content A")
        h2 = self.hasher.hash_string("content B")
        assert h1 != h2
