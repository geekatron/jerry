# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Persistence adapters for file I/O operations.

Provides adapters for safe concurrent file access with locking and atomic writes.
"""

from src.infrastructure.adapters.persistence.atomic_file_adapter import AtomicFileAdapter
from src.infrastructure.adapters.persistence.filesystem_local_context_adapter import (
    FilesystemLocalContextAdapter,
)

__all__ = ["AtomicFileAdapter", "FilesystemLocalContextAdapter"]
