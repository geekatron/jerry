# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for EngagementInitializer."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.tool_exec.domain.services.engagement_initializer import (
    EngagementInitializer,
)


class TestEngagementInitializer:
    """Tests for engagement directory creation and validation."""

    def test_initialize_creates_all_dirs(self, tmp_path: Path) -> None:
        """Initialize creates evidence, reports, and quarantine directories."""
        init = EngagementInitializer(base_dir=tmp_path)
        result = init.initialize("ENG-001")

        assert (result / "evidence").is_dir()
        assert (result / "reports").is_dir()
        assert (result / ".credential-quarantine").is_dir()

    def test_initialize_writes_metadata(self, tmp_path: Path) -> None:
        """Initialize writes .engagement-meta.json."""
        init = EngagementInitializer(base_dir=tmp_path)
        result = init.initialize("ENG-002")

        meta_path = result / ".engagement-meta.json"
        assert meta_path.exists()

        meta = json.loads(meta_path.read_text())
        assert meta["engagement_id"] == "ENG-002"
        assert "initialized_at" in meta
        assert "directories" in meta

    def test_initialize_is_idempotent(self, tmp_path: Path) -> None:
        """Calling initialize twice does not fail or destroy content."""
        init = EngagementInitializer(base_dir=tmp_path)
        init.initialize("ENG-003")

        # Write a file in evidence dir
        evidence_file = tmp_path / "ENG-003" / "evidence" / "test.txt"
        evidence_file.write_text("evidence data")

        # Re-initialize
        init.initialize("ENG-003")

        # File should still exist
        assert evidence_file.exists()
        assert evidence_file.read_text() == "evidence data"

    def test_is_initialized_true(self, tmp_path: Path) -> None:
        """is_initialized returns True after successful initialization."""
        init = EngagementInitializer(base_dir=tmp_path)
        init.initialize("ENG-004")
        assert init.is_initialized("ENG-004") is True

    def test_is_initialized_false(self, tmp_path: Path) -> None:
        """is_initialized returns False for non-existent engagement."""
        init = EngagementInitializer(base_dir=tmp_path)
        assert init.is_initialized("NONEXISTENT") is False

    def test_is_initialized_partial(self, tmp_path: Path) -> None:
        """is_initialized returns False if only some dirs exist."""
        init = EngagementInitializer(base_dir=tmp_path)
        # Create only the evidence dir
        (tmp_path / "ENG-PARTIAL" / "evidence").mkdir(parents=True)
        assert init.is_initialized("ENG-PARTIAL") is False

    def test_evidence_dir_path(self, tmp_path: Path) -> None:
        """evidence_dir returns the correct path."""
        init = EngagementInitializer(base_dir=tmp_path)
        expected = tmp_path / "ENG-005" / "evidence"
        assert init.evidence_dir("ENG-005") == expected

    def test_quarantine_dir_path(self, tmp_path: Path) -> None:
        """quarantine_dir returns the correct path."""
        init = EngagementInitializer(base_dir=tmp_path)
        expected = tmp_path / "ENG-006" / ".credential-quarantine"
        assert init.quarantine_dir("ENG-006") == expected


class TestEngagementInitializerValidation:
    """Tests for engagement ID validation."""

    def test_empty_id_raises(self, tmp_path: Path) -> None:
        """Empty engagement ID raises ValueError."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="must not be empty"):
            init.initialize("")

    def test_whitespace_only_id_raises(self, tmp_path: Path) -> None:
        """Whitespace-only engagement ID raises ValueError."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="must not be empty"):
            init.initialize("   ")

    def test_path_traversal_dotdot_raises(self, tmp_path: Path) -> None:
        """Engagement ID with .. raises ValueError."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="path-traversal"):
            init.initialize("../escape")

    def test_path_traversal_slash_raises(self, tmp_path: Path) -> None:
        """Engagement ID with / raises ValueError."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="path-traversal"):
            init.initialize("dir/subdir")

    def test_path_traversal_backslash_raises(self, tmp_path: Path) -> None:
        """Engagement ID with backslash raises ValueError."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="path-traversal"):
            init.initialize("dir\\subdir")
