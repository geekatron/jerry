# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for EngagementInitializer.

Security tests include:
- M-05 (T-08, DREAD 28): Engagement ID character-class allowlist enforcement.
- M-10 (T-21, DREAD 24): Quarantine directory permission restriction (0o700).
"""

from __future__ import annotations

import json
import stat
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
        # CV-010: Field names aligned with UC spec (id, created_at, created_by).
        assert meta["id"] == "ENG-002"
        assert "created_at" in meta
        assert "created_by" in meta

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
        """Engagement ID with .. raises ValueError (blocked by allowlist, M-05)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="invalid characters"):
            init.initialize("../escape")

    def test_path_traversal_slash_raises(self, tmp_path: Path) -> None:
        """Engagement ID with / raises ValueError (blocked by allowlist, M-05)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="invalid characters"):
            init.initialize("dir/subdir")

    def test_path_traversal_backslash_raises(self, tmp_path: Path) -> None:
        """Engagement ID with backslash raises ValueError (blocked by allowlist, M-05)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="invalid characters"):
            init.initialize("dir\\subdir")

    def test_special_char_dollar_raises(self, tmp_path: Path) -> None:
        """Engagement ID with shell-special $ char raises ValueError (M-05)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="invalid characters"):
            init.initialize("$(whoami)")

    def test_special_char_backtick_raises(self, tmp_path: Path) -> None:
        """Engagement ID with backtick raises ValueError (M-05)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="invalid characters"):
            init.initialize("`id`")

    def test_special_char_semicolon_raises(self, tmp_path: Path) -> None:
        """Engagement ID with semicolon raises ValueError (M-05)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="invalid characters"):
            init.initialize("id;rm -rf /")

    def test_valid_alphanumeric_id_accepted(self, tmp_path: Path) -> None:
        """Alphanumeric engagement ID with hyphens and underscores is accepted (M-05)."""
        init = EngagementInitializer(base_dir=tmp_path)
        # Should not raise
        result = init.initialize("PROJ-023-pentest-2026")
        assert result.is_dir()

    def test_valid_id_with_numbers_accepted(self, tmp_path: Path) -> None:
        """Engagement ID starting with digit is accepted (M-05 allowlist)."""
        init = EngagementInitializer(base_dir=tmp_path)
        result = init.initialize("20260317-engagement")
        assert result.is_dir()

    def test_id_exceeding_128_chars_raises(self, tmp_path: Path) -> None:
        """Engagement ID longer than 128 chars raises ValueError (M-05)."""
        init = EngagementInitializer(base_dir=tmp_path)
        long_id = "a" * 129  # 129 chars, over the 128-char limit
        with pytest.raises(ValueError, match="invalid characters"):
            init.initialize(long_id)

    def test_id_exactly_128_chars_accepted(self, tmp_path: Path) -> None:
        """Engagement ID of exactly 128 chars is accepted (boundary check, M-05)."""
        init = EngagementInitializer(base_dir=tmp_path)
        exact_id = "a" * 128  # 128 chars = 1 leading + 127 body chars
        result = init.initialize(exact_id)
        assert result.is_dir()


class TestEngagementInitializerFinding002:
    """Tests for FINDING-002 (CWE-22): _validate_id() called in all public methods.

    Verifies that is_initialized(), evidence_dir(), and quarantine_dir() reject
    engagement IDs with path-traversal characters -- not just initialize().
    Before the fix, these methods accepted raw strings and composed filesystem
    paths without validation, creating a defence-in-depth gap.
    """

    def test_is_initialized_rejects_path_traversal(self, tmp_path: Path) -> None:
        """is_initialized() raises ValueError for path-traversal ID (FINDING-002)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="invalid characters"):
            init.is_initialized("../../etc")

    def test_is_initialized_rejects_empty_id(self, tmp_path: Path) -> None:
        """is_initialized() raises ValueError for empty ID (FINDING-002)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="must not be empty"):
            init.is_initialized("")

    def test_is_initialized_rejects_slash_id(self, tmp_path: Path) -> None:
        """is_initialized() raises ValueError for ID containing / (FINDING-002)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="invalid characters"):
            init.is_initialized("dir/subdir")

    def test_evidence_dir_rejects_path_traversal(self, tmp_path: Path) -> None:
        """evidence_dir() raises ValueError for path-traversal ID (FINDING-002)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="invalid characters"):
            init.evidence_dir("../../etc")

    def test_evidence_dir_rejects_empty_id(self, tmp_path: Path) -> None:
        """evidence_dir() raises ValueError for empty ID (FINDING-002)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="must not be empty"):
            init.evidence_dir("")

    def test_quarantine_dir_rejects_path_traversal(self, tmp_path: Path) -> None:
        """quarantine_dir() raises ValueError for path-traversal ID (FINDING-002)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="invalid characters"):
            init.quarantine_dir("../../etc")

    def test_quarantine_dir_rejects_empty_id(self, tmp_path: Path) -> None:
        """quarantine_dir() raises ValueError for empty ID (FINDING-002)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with pytest.raises(ValueError, match="must not be empty"):
            init.quarantine_dir("")

    def test_valid_id_accepted_by_is_initialized(self, tmp_path: Path) -> None:
        """Valid IDs are still accepted by is_initialized() after the fix."""
        init = EngagementInitializer(base_dir=tmp_path)
        # Should not raise -- returns False because engagement not yet initialized
        assert init.is_initialized("valid-eng-001") is False

    def test_valid_id_accepted_by_evidence_dir(self, tmp_path: Path) -> None:
        """Valid IDs return the correct path from evidence_dir() after the fix."""
        init = EngagementInitializer(base_dir=tmp_path)
        expected = tmp_path / "valid-eng-002" / "evidence"
        assert init.evidence_dir("valid-eng-002") == expected

    def test_valid_id_accepted_by_quarantine_dir(self, tmp_path: Path) -> None:
        """Valid IDs return the correct path from quarantine_dir() after the fix."""
        init = EngagementInitializer(base_dir=tmp_path)
        expected = tmp_path / "valid-eng-003" / ".credential-quarantine"
        assert init.quarantine_dir("valid-eng-003") == expected


class TestEngagementInitializerQuarantinePermissions:
    """Tests for M-10: quarantine directory permission restriction (T-21, DREAD 24).

    Verifies that the .credential-quarantine directory is created with 0o700
    permissions (owner read/write/execute only), preventing other users on a
    shared system from reading quarantined credential-bearing output.
    """

    def test_quarantine_dir_permissions_restricted(self, tmp_path: Path) -> None:
        """Quarantine directory is created with 0o700 permissions (M-10)."""
        init = EngagementInitializer(base_dir=tmp_path)
        result = init.initialize("SEC-PERM-TEST")

        quarantine_dir = result / ".credential-quarantine"
        assert quarantine_dir.is_dir()

        # Check that permissions are 0o700 (owner rwx, group none, world none)
        mode = quarantine_dir.stat().st_mode
        # Extract the permission bits (mask out file type bits)
        permissions = stat.S_IMODE(mode)
        assert permissions == 0o700, (
            f"Quarantine directory permissions should be 0o700 (owner-only), got 0o{permissions:o}"
        )
