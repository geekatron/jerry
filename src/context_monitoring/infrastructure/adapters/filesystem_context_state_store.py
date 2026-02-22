# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
FilesystemContextStateStore - Filesystem implementation of IContextStateStore.

Persists cross-invocation context monitoring state as a JSON file in
the ``.jerry/local/`` directory. Uses atomic writes (write-to-temp +
rename) to prevent corruption from concurrent status line invocations.

File location: ``$HOME/.jerry/local/context-state.json``

References:
    - FEAT-002: Status Line / Context Monitoring Unification
    - EN-011: Infrastructure Adapter (FilesystemContextStateStore)
    - DEC-004 D-004: Cross-invocation state via port
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
import logging
import tempfile
from pathlib import Path

from src.context_monitoring.application.ports.context_state import ContextState

logger = logging.getLogger(__name__)

_STATE_FILENAME = "context-state.json"


class FilesystemContextStateStore:
    """Filesystem-backed implementation of IContextStateStore.

    Reads and writes a small JSON state file that bridges the gap
    between separate CLI invocations (status line, hooks). Uses
    atomic writes to prevent corruption.

    Attributes:
        _state_path: Path to the state JSON file.

    Example:
        >>> store = FilesystemContextStateStore(state_dir=Path.home() / ".jerry" / "local")
        >>> state = store.load()
        >>> store.save(ContextState(previous_tokens=150000, ...))
    """

    def __init__(self, state_dir: Path) -> None:
        """Initialize with the directory for state file storage.

        The directory is created if it does not exist.

        Args:
            state_dir: Directory where the state file will be stored.
        """
        self._state_path = state_dir / _STATE_FILENAME

    def load(self) -> ContextState | None:
        """Load the persisted context state from disk.

        Returns:
            The saved ContextState, or None if no state file exists.

        Raises:
            OSError: If the file exists but cannot be read.
            json.JSONDecodeError: If the file contains invalid JSON.
            KeyError: If required fields are missing from the JSON.
        """
        if not self._state_path.exists():
            return None

        data = json.loads(self._state_path.read_text(encoding="utf-8"))
        return ContextState(
            previous_tokens=data["previous_tokens"],
            previous_session_id=data["previous_session_id"],
            last_tier=data["last_tier"],
            last_rotation_action=data["last_rotation_action"],
        )

    def save(self, state: ContextState) -> None:
        """Save context state atomically to disk.

        Uses write-to-temp + rename for atomic writes, preventing
        corruption from concurrent invocations.

        Args:
            state: The state to persist.

        Raises:
            OSError: If the file cannot be written.
        """
        data = {
            "previous_tokens": state.previous_tokens,
            "previous_session_id": state.previous_session_id,
            "last_tier": state.last_tier,
            "last_rotation_action": state.last_rotation_action,
        }

        # Ensure directory exists
        self._state_path.parent.mkdir(parents=True, exist_ok=True)

        # Atomic write: temp file in same directory, then rename
        fd, tmp_path = tempfile.mkstemp(
            dir=self._state_path.parent,
            suffix=".tmp",
        )
        try:
            with open(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
                f.write("\n")
            Path(tmp_path).replace(self._state_path)
        except BaseException:
            # Clean up temp file on any failure
            Path(tmp_path).unlink(missing_ok=True)
            raise
