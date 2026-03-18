# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Evidence hasher service for SLSA chain-of-custody integrity.

Provides portable SHA-256 hashing using Python's hashlib, avoiding
external dependencies like sha256sum that may not exist on all platforms.

References:
    - ADR-PROJ023-001: Evidence Persistence (SLSA chain of custody)
    - TASK-007: EvidenceHasher
"""

from __future__ import annotations

import hashlib


class EvidenceHasher:
    """Computes SHA-256 hashes for evidence integrity verification.

    Uses Python's hashlib.sha256 for portable, cross-platform hashing.
    This replaces the bash `sha256sum` dependency from the original
    rainbow-tool-exec script, ensuring consistent behavior across
    macOS and Linux.
    """

    ALGORITHM = "sha256"

    def hash_string(self, content: str) -> str:
        """Compute the SHA-256 hex digest of a string.

        Encodes the string as UTF-8 before hashing, matching the behavior
        of `echo "$content" | sha256sum` in the bash implementation.

        Args:
            content: The string content to hash.

        Returns:
            Lowercase hex-encoded SHA-256 digest (64 characters).
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def hash_bytes(self, content: bytes) -> str:
        """Compute the SHA-256 hex digest of raw bytes.

        Args:
            content: The raw bytes to hash.

        Returns:
            Lowercase hex-encoded SHA-256 digest (64 characters).
        """
        return hashlib.sha256(content).hexdigest()

    def hash_file(self, file_path: str) -> str:
        """Compute the SHA-256 hex digest of a file's contents.

        Reads the file in binary mode and computes the hash incrementally
        to support large files without excessive memory consumption.

        Args:
            file_path: Path to the file to hash.

        Returns:
            Lowercase hex-encoded SHA-256 digest (64 characters).

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the file cannot be read.
        """
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
