"""
IFileStore - File Operations Abstraction.

Internal abstraction for file operations used by repository adapters.
Provides read/write/lock operations with proper error handling.

References:
    - PAT-003: Optimistic Concurrency with File Locking
    - PAT-010: Composed Infrastructure Adapters
    - ADR-006: File Locking Strategy
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Protocol, TypeVar

if TYPE_CHECKING:
    from collections.abc import Iterator

try:
    from filelock import FileLock
    from filelock import Timeout as FileLockTimeout

    HAS_FILELOCK = True
except ImportError:
    HAS_FILELOCK = False
    FileLock = None
    FileLockTimeout = Exception


T = TypeVar("T")


class FileStoreError(Exception):
    """Base exception for file store operations."""


class FileNotFoundError_(FileStoreError):
    """File does not exist."""

    def __init__(self, path: str | Path) -> None:
        super().__init__(f"File not found: {path}")
        self.path = path


class FileWriteError(FileStoreError):
    """Failed to write file."""

    def __init__(self, path: str | Path, reason: str) -> None:
        super().__init__(f"Failed to write {path}: {reason}")
        self.path = path
        self.reason = reason


class FileLockError(FileStoreError):
    """Failed to acquire file lock."""

    def __init__(self, path: str | Path, timeout: float) -> None:
        super().__init__(f"Failed to acquire lock on {path} within {timeout}s")
        self.path = path
        self.timeout = timeout


class IFileStore(Protocol):
    """Protocol for file operations.

    This is an internal abstraction used by repository adapters.
    It provides atomic file operations with optional locking.

    Implementations:
        - LocalFileStore: Local filesystem with filelock
        - InMemoryFileStore: For testing

    Example:
        >>> store = LocalFileStore()
        >>> store.write("/tmp/data.json", b'{"key": "value"}')
        >>> data = store.read("/tmp/data.json")
        >>> print(data)
        b'{"key": "value"}'
    """

    def read(self, path: str | Path) -> bytes:
        """Read file contents as bytes.

        Args:
            path: Path to the file

        Returns:
            File contents as bytes

        Raises:
            FileNotFoundError_: If file does not exist
            FileStoreError: If read fails
        """
        ...

    def write(self, path: str | Path, data: bytes, *, fsync: bool = True) -> None:
        """Write data to file atomically.

        Uses write-to-temp-then-rename pattern for atomicity.

        Args:
            path: Path to the file
            data: Data to write
            fsync: Whether to fsync before rename (default True for durability)

        Raises:
            FileWriteError: If write fails
        """
        ...

    def exists(self, path: str | Path) -> bool:
        """Check if file exists.

        Args:
            path: Path to check

        Returns:
            True if file exists, False otherwise
        """
        ...

    def delete(self, path: str | Path) -> bool:
        """Delete file if it exists.

        Args:
            path: Path to delete

        Returns:
            True if file was deleted, False if it didn't exist
        """
        ...

    @contextmanager
    def locked(self, path: str | Path, *, timeout: float = 10.0) -> Iterator[None]:
        """Context manager for exclusive file lock.

        Args:
            path: Path to lock (uses path.lock as lock file)
            timeout: Seconds to wait for lock (default 10)

        Yields:
            None (lock is held for duration of context)

        Raises:
            FileLockError: If lock cannot be acquired within timeout
        """
        ...


class LocalFileStore:
    """Local filesystem implementation of IFileStore.

    Uses filelock library for cross-process locking.
    Falls back to no-op locking if filelock is not installed.

    Attributes:
        base_path: Optional base path prefix for all operations

    Example:
        >>> store = LocalFileStore(base_path="/data")
        >>> store.write("users/1.json", b'{"name": "Alice"}')
        >>> # Actually writes to /data/users/1.json
    """

    def __init__(self, base_path: str | Path | None = None) -> None:
        """Initialize LocalFileStore.

        Args:
            base_path: Optional base path to prefix all file operations
        """
        self._base_path = Path(base_path) if base_path else None

    def _resolve_path(self, path: str | Path) -> Path:
        """Resolve path, optionally prefixing with base_path."""
        p = Path(path)
        if self._base_path and not p.is_absolute():
            return self._base_path / p
        return p

    def read(self, path: str | Path) -> bytes:
        """Read file contents as bytes."""
        resolved = self._resolve_path(path)
        if not resolved.exists():
            raise FileNotFoundError_(resolved)
        try:
            return resolved.read_bytes()
        except OSError as e:
            raise FileStoreError(f"Failed to read {resolved}: {e}") from e

    def write(self, path: str | Path, data: bytes, *, fsync: bool = True) -> None:
        """Write data to file atomically using write-to-temp-then-rename."""
        resolved = self._resolve_path(path)

        # Ensure parent directory exists
        resolved.parent.mkdir(parents=True, exist_ok=True)

        # Write to temp file first
        temp_path = resolved.with_suffix(resolved.suffix + ".tmp")
        try:
            with open(temp_path, "wb") as f:
                f.write(data)
                if fsync:
                    f.flush()
                    os.fsync(f.fileno())

            # Atomic rename
            temp_path.replace(resolved)

        except OSError as e:
            # Clean up temp file on failure
            if temp_path.exists():
                temp_path.unlink()
            raise FileWriteError(resolved, str(e)) from e

    def exists(self, path: str | Path) -> bool:
        """Check if file exists."""
        return self._resolve_path(path).exists()

    def delete(self, path: str | Path) -> bool:
        """Delete file if it exists."""
        resolved = self._resolve_path(path)
        if resolved.exists():
            resolved.unlink()
            return True
        return False

    @contextmanager
    def locked(self, path: str | Path, *, timeout: float = 10.0) -> Iterator[None]:
        """Context manager for exclusive file lock."""
        resolved = self._resolve_path(path)
        lock_path = resolved.with_suffix(resolved.suffix + ".lock")

        # Ensure lock directory exists
        lock_path.parent.mkdir(parents=True, exist_ok=True)

        if HAS_FILELOCK and FileLock is not None:
            lock = FileLock(str(lock_path), timeout=timeout)
            try:
                with lock:
                    yield
            except FileLockTimeout as e:
                raise FileLockError(resolved, timeout) from e
        else:
            # Fallback: no-op locking (for environments without filelock)
            yield


class InMemoryFileStore:
    """In-memory implementation of IFileStore for testing.

    Stores files in a dictionary. Useful for unit tests where
    filesystem access should be avoided.

    Example:
        >>> store = InMemoryFileStore()
        >>> store.write("test.json", b'{"key": "value"}')
        >>> store.read("test.json")
        b'{"key": "value"}'
    """

    def __init__(self) -> None:
        """Initialize empty in-memory store."""
        self._files: dict[str, bytes] = {}
        self._locks: set[str] = set()

    def read(self, path: str | Path) -> bytes:
        """Read file contents from memory."""
        key = str(path)
        if key not in self._files:
            raise FileNotFoundError_(path)
        return self._files[key]

    def write(self, path: str | Path, data: bytes, *, fsync: bool = True) -> None:
        """Write data to memory (fsync is ignored)."""
        self._files[str(path)] = data

    def exists(self, path: str | Path) -> bool:
        """Check if file exists in memory."""
        return str(path) in self._files

    def delete(self, path: str | Path) -> bool:
        """Delete file from memory."""
        key = str(path)
        if key in self._files:
            del self._files[key]
            return True
        return False

    @contextmanager
    def locked(self, path: str | Path, *, timeout: float = 10.0) -> Iterator[None]:
        """Simulate file lock (no actual locking in memory)."""
        key = str(path)
        if key in self._locks:
            raise FileLockError(path, timeout)
        self._locks.add(key)
        try:
            yield
        finally:
            self._locks.discard(key)

    def clear(self) -> None:
        """Clear all files from memory."""
        self._files.clear()
        self._locks.clear()
