"""Infrastructure adapters for repository pattern.

Provides concrete implementations of domain repository ports.
"""

from src.infrastructure.adapters.file_repository import FileRepository

__all__ = ["FileRepository"]
