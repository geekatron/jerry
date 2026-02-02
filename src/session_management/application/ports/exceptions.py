"""
Repository Exceptions - Infrastructure Error Types

These exceptions are raised by repository adapters when
infrastructure operations fail (I/O errors, permission issues, etc.).
"""

from __future__ import annotations


class RepositoryError(Exception):
    """Base exception for repository errors.

    Raised when infrastructure operations fail (I/O errors, permission issues, etc.).
    """

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        self.message = message
        self.cause = cause
        super().__init__(message)
