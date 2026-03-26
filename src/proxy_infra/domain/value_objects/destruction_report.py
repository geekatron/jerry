# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""DestructionReport value object — aggregate result of a credential destruction sweep.

References:
    - TASK-023-035: Credential destruction specification
    - STORY-023-005: Ephemeral Credential Lifecycle
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.destruction_entry import DestructionEntry


@dataclass
class DestructionReport:
    """Aggregate result of a destroy_all() credential sweep.

    Attributes:
        destroyed_files: Entries for files successfully overwritten and unlinked.
        failed_files: Pairs of (file_path, error_message) for files that could
            not be destroyed.
    """

    destroyed_files: list[DestructionEntry] = field(default_factory=list)
    failed_files: list[tuple[str, str]] = field(default_factory=list)
