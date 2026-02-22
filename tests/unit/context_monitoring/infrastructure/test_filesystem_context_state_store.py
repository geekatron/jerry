# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Tests for FilesystemContextStateStore infrastructure adapter.

BDD scenarios from EN-011:
    - Load returns None when no state file exists
    - Save creates state file and load reads it back
    - State round-trips through JSON correctly
    - Save overwrites previous state
    - Save creates parent directory if missing
    - Atomic write: temp file cleaned up on failure
    - Satisfies IContextStateStore protocol

References:
    - EN-011: Infrastructure Adapter (FilesystemContextStateStore)
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from src.context_monitoring.application.ports.context_state import ContextState
from src.context_monitoring.application.ports.context_state_store import (
    IContextStateStore,
)
from src.context_monitoring.infrastructure.adapters.filesystem_context_state_store import (
    FilesystemContextStateStore,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def state_dir(tmp_path: Path) -> Path:
    """Temporary directory for state file storage."""
    return tmp_path / "jerry-local"


@pytest.fixture()
def store(state_dir: Path) -> FilesystemContextStateStore:
    """FilesystemContextStateStore using temporary directory."""
    return FilesystemContextStateStore(state_dir=state_dir)


def _make_state(
    *,
    previous_tokens: int = 150000,
    previous_session_id: str = "sess-abc",
    last_tier: str = "warning",
    last_rotation_action: str = "log_warning",
) -> ContextState:
    return ContextState(
        previous_tokens=previous_tokens,
        previous_session_id=previous_session_id,
        last_tier=last_tier,
        last_rotation_action=last_rotation_action,
    )


# =============================================================================
# Protocol compliance
# =============================================================================


class TestProtocolCompliance:
    """FilesystemContextStateStore satisfies IContextStateStore protocol."""

    def test_is_runtime_checkable(self, store: FilesystemContextStateStore) -> None:
        """Store instance passes isinstance check for IContextStateStore."""
        assert isinstance(store, IContextStateStore)


# =============================================================================
# Load behavior
# =============================================================================


class TestLoad:
    """Test state loading from filesystem."""

    def test_load_returns_none_when_no_file(self, store: FilesystemContextStateStore) -> None:
        """Load returns None when state file does not exist."""
        assert store.load() is None

    def test_load_returns_saved_state(
        self, store: FilesystemContextStateStore, state_dir: Path
    ) -> None:
        """Load returns ContextState when valid state file exists."""
        state_dir.mkdir(parents=True, exist_ok=True)
        state_file = state_dir / "context-state.json"
        state_file.write_text(
            json.dumps(
                {
                    "previous_tokens": 180000,
                    "previous_session_id": "sess-xyz",
                    "last_tier": "critical",
                    "last_rotation_action": "checkpoint",
                }
            ),
            encoding="utf-8",
        )

        result = store.load()

        assert result is not None
        assert result.previous_tokens == 180000
        assert result.previous_session_id == "sess-xyz"
        assert result.last_tier == "critical"
        assert result.last_rotation_action == "checkpoint"

    def test_load_raises_on_invalid_json(
        self, store: FilesystemContextStateStore, state_dir: Path
    ) -> None:
        """Load raises JSONDecodeError on corrupted file."""
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "context-state.json").write_text("not json", encoding="utf-8")

        with pytest.raises(json.JSONDecodeError):
            store.load()

    def test_load_raises_on_missing_fields(
        self, store: FilesystemContextStateStore, state_dir: Path
    ) -> None:
        """Load raises KeyError when required fields are missing."""
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "context-state.json").write_text(
            json.dumps({"previous_tokens": 100}), encoding="utf-8"
        )

        with pytest.raises(KeyError):
            store.load()


# =============================================================================
# Save behavior
# =============================================================================


class TestSave:
    """Test state saving to filesystem."""

    def test_save_creates_file(self, store: FilesystemContextStateStore, state_dir: Path) -> None:
        """Save creates the state file in the expected location."""
        store.save(_make_state())

        state_file = state_dir / "context-state.json"
        assert state_file.exists()

    def test_save_creates_parent_directory(
        self, store: FilesystemContextStateStore, state_dir: Path
    ) -> None:
        """Save creates parent directory if it doesn't exist."""
        assert not state_dir.exists()

        store.save(_make_state())

        assert state_dir.exists()
        assert (state_dir / "context-state.json").exists()

    def test_save_writes_valid_json(
        self, store: FilesystemContextStateStore, state_dir: Path
    ) -> None:
        """Saved file contains valid JSON with expected fields."""
        store.save(_make_state(previous_tokens=99000, last_tier="emergency"))

        data = json.loads((state_dir / "context-state.json").read_text(encoding="utf-8"))
        assert data["previous_tokens"] == 99000
        assert data["previous_session_id"] == "sess-abc"
        assert data["last_tier"] == "emergency"
        assert data["last_rotation_action"] == "log_warning"

    def test_save_overwrites_previous(self, store: FilesystemContextStateStore) -> None:
        """Subsequent save overwrites previous state."""
        store.save(_make_state(previous_tokens=100000))
        store.save(_make_state(previous_tokens=200000))

        result = store.load()
        assert result is not None
        assert result.previous_tokens == 200000


# =============================================================================
# Round-trip
# =============================================================================


class TestRoundTrip:
    """Test save-then-load round-trip preserves all fields."""

    def test_full_round_trip(self, store: FilesystemContextStateStore) -> None:
        """All ContextState fields survive save -> load cycle."""
        original = _make_state(
            previous_tokens=175432,
            previous_session_id="session-round-trip-test",
            last_tier="critical",
            last_rotation_action="checkpoint",
        )

        store.save(original)
        loaded = store.load()

        assert loaded == original


# =============================================================================
# Atomic write safety
# =============================================================================


class TestAtomicWrite:
    """Test atomic write guarantees."""

    def test_temp_file_cleaned_on_failure(
        self, store: FilesystemContextStateStore, state_dir: Path
    ) -> None:
        """Temp file is cleaned up when json.dump fails."""
        state_dir.mkdir(parents=True, exist_ok=True)

        with (
            patch("json.dump", side_effect=OSError("disk full")),
            pytest.raises(OSError, match="disk full"),
        ):
            store.save(_make_state())

        # No temp files left behind
        tmp_files = list(state_dir.glob("*.tmp"))
        assert tmp_files == []

    def test_original_preserved_on_failure(
        self, store: FilesystemContextStateStore, state_dir: Path
    ) -> None:
        """Original state file preserved when save fails mid-write."""
        store.save(_make_state(previous_tokens=100000))

        with (
            patch("json.dump", side_effect=OSError("disk full")),
            pytest.raises(OSError, match="disk full"),
        ):
            store.save(_make_state(previous_tokens=999999))

        # Original state should still be readable
        result = store.load()
        assert result is not None
        assert result.previous_tokens == 100000
