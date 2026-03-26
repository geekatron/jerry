# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""DestructionEntry value object — record of a single file's destruction operation.

References:
    - TASK-023-035: Credential destruction specification
    - STORY-023-005: Ephemeral Credential Lifecycle
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DestructionEntry:
    """Immutable record of a single credential file's destruction.

    Attributes:
        file_path: Absolute path of the file that was processed.
        overwrite_confirmed: True if the urandom overwrite succeeded before
            the file was unlinked.
    """

    file_path: str
    overwrite_confirmed: bool
