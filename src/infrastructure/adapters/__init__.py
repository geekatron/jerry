# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Infrastructure adapters for repository pattern.

Provides concrete implementations of domain repository ports.

Adapters:
    - FileRepository: Generic file-based repository
    - AtomicFileAdapter: Safe concurrent file I/O with locking
    - EnvConfigAdapter: Environment variable configuration
    - LayeredConfigAdapter: Layered configuration with precedence
"""

from src.infrastructure.adapters.configuration.env_config_adapter import (
    EnvConfigAdapter,
)
from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)
from src.infrastructure.adapters.file_repository import FileRepository
from src.infrastructure.adapters.persistence.atomic_file_adapter import (
    AtomicFileAdapter,
)

__all__ = [
    "AtomicFileAdapter",
    "EnvConfigAdapter",
    "FileRepository",
    "LayeredConfigAdapter",
]
