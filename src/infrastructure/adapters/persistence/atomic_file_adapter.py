"""
AtomicFileAdapter - Safe Concurrent File Access with Locking

Provides atomic file operations using fcntl locking and temp file patterns.
This adapter ensures data integrity during concurrent access and crash recovery.

Implementation Notes:
    - Uses fcntl.lockf for POSIX-compliant file locking
    - Lock files are stored in a centralized lock directory (.jerry/local/locks/)
    - Atomic writes use tempfile + os.replace for crash safety
    - Locks auto-release on process termination (OS-level guarantee)

References:
    - WI-012: Atomic File Adapter work item
    - PROJ-004-e-002: Runtime Collision Avoidance research
    - PAT-ADP-002: Persistence Adapter pattern
"""

from __future__ import annotations

import fcntl
import hashlib
import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class AtomicFileAdapter:
    """Adapter for atomic file operations with POSIX file locking.

    This adapter provides thread-safe and process-safe file operations
    using fcntl.lockf for locking and tempfile + os.replace for atomic writes.

    Attributes:
        lock_dir: Directory for storing lock files

    Example:
        >>> adapter = AtomicFileAdapter()
        >>> content = adapter.read_with_lock(Path("config.toml"))
        >>> adapter.write_atomic(Path("config.toml"), "new content")
    """

    def __init__(self, lock_dir: Path | None = None) -> None:
        """Initialize the adapter with a lock directory.

        Args:
            lock_dir: Directory for lock files. Defaults to .jerry/local/locks/
        """
        self._lock_dir = lock_dir or Path(".jerry/local/locks")

    @property
    def lock_dir(self) -> Path:
        """Get the lock directory path."""
        return self._lock_dir

    def _get_lock_path(self, path: Path) -> Path:
        """Get the lock file path for a given data file.

        Uses SHA-256 hash of the absolute path to create a unique lock file name.
        This avoids issues with path length and special characters.

        Args:
            path: Path to the data file

        Returns:
            Path to the corresponding lock file
        """
        self._lock_dir.mkdir(parents=True, exist_ok=True)
        # Use SHA-256 hash for consistent, safe filename
        path_hash = hashlib.sha256(str(path.absolute()).encode()).hexdigest()[:16]
        lock_name = f"{path_hash}.lock"
        return self._lock_dir / lock_name

    def read_with_lock(self, path: Path) -> str:
        """Read file content with a shared (read) lock.

        Acquires a shared lock before reading to allow concurrent reads
        but block writes during the read operation.

        Args:
            path: Path to the file to read

        Returns:
            File content as string, or empty string if file doesn't exist

        Raises:
            PermissionError: If lock cannot be acquired
            OSError: If file cannot be read
        """
        lock_path = self._get_lock_path(path)
        lock_path.touch(exist_ok=True)

        with open(lock_path, "r+") as lock_file:
            fcntl.lockf(lock_file.fileno(), fcntl.LOCK_SH)
            try:
                if path.exists():
                    return path.read_text(encoding="utf-8")
                return ""
            finally:
                fcntl.lockf(lock_file.fileno(), fcntl.LOCK_UN)

    def write_atomic(self, path: Path, content: str) -> None:
        """Write content atomically with an exclusive (write) lock.

        Uses the following pattern for crash-safe writes:
        1. Acquire exclusive lock on lock file
        2. Write content to a temporary file in the same directory
        3. Flush and fsync to ensure data is on disk
        4. Atomically replace the target file with os.replace
        5. Release the lock

        Args:
            path: Path to the file to write
            content: Content to write

        Raises:
            PermissionError: If lock cannot be acquired or file cannot be written
            OSError: If write operation fails
        """
        lock_path = self._get_lock_path(path)
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path.touch(exist_ok=True)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(lock_path, "r+") as lock_file:
            fcntl.lockf(lock_file.fileno(), fcntl.LOCK_EX)
            try:
                # Create temp file in same directory for atomic replace
                fd, temp_path = tempfile.mkstemp(
                    dir=path.parent,
                    prefix=f".{path.name}.",
                    suffix=".tmp",
                )
                try:
                    with os.fdopen(fd, "w", encoding="utf-8") as f:
                        f.write(content)
                        f.flush()
                        os.fsync(f.fileno())
                    # Atomic replace - this is a single syscall
                    os.replace(temp_path, path)
                except Exception:
                    # Clean up temp file on failure
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                    raise
            finally:
                fcntl.lockf(lock_file.fileno(), fcntl.LOCK_UN)

    def exists(self, path: Path) -> bool:
        """Check if a file exists.

        Args:
            path: Path to check

        Returns:
            True if the file exists, False otherwise
        """
        return path.exists() and path.is_file()

    def delete_with_lock(self, path: Path) -> bool:
        """Delete a file with exclusive lock.

        Args:
            path: Path to the file to delete

        Returns:
            True if file was deleted, False if it didn't exist

        Raises:
            PermissionError: If lock cannot be acquired or file cannot be deleted
            OSError: If delete operation fails
        """
        lock_path = self._get_lock_path(path)
        lock_path.touch(exist_ok=True)

        with open(lock_path, "r+") as lock_file:
            fcntl.lockf(lock_file.fileno(), fcntl.LOCK_EX)
            try:
                if path.exists():
                    path.unlink()
                    return True
                return False
            finally:
                fcntl.lockf(lock_file.fileno(), fcntl.LOCK_UN)
