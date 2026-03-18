# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Security tests for tool_exec_commands.py CLI handler.

Tests FINDING-001 (CWE-22, High): --evidence-dir path traversal remediation.
The _validate_evidence_dir() function must canonicalize the user-supplied path
via .resolve() and enforce project-root containment before any directory is
created or written to.

References:
    - FINDING-001: eng-security-phase2-review.md
    - ASVS V5.1.2 (Input validation, file paths)
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.interface.cli.tool_exec_commands import _validate_evidence_dir


class TestValidateEvidenceDirFinding001:
    """Tests for FINDING-001 (CWE-22, High): _validate_evidence_dir containment check.

    Verifies that _validate_evidence_dir() rejects paths that escape the project
    root and accepts paths that are legitimately within it. Without this check,
    an operator could pass --evidence-dir ../../tmp/exfil to redirect evidence
    writes outside the engagement isolation boundary, bypassing the 0o700 quarantine
    permission protections and the engagement directory model.
    """

    def test_path_within_project_root_accepted(self, tmp_path: Path) -> None:
        """Absolute path inside project root is accepted and returned as resolved Path."""
        project_root = tmp_path / "project"
        project_root.mkdir()
        # Use an absolute path so .resolve() resolves relative to the filesystem,
        # not relative to cwd (which may be the repo root in test runs).
        evidence_subdir = project_root / "work" / "engagements" / "eng-001" / "evidence"

        result = _validate_evidence_dir(str(evidence_subdir), project_root)

        assert result == evidence_subdir.resolve()

    def test_absolute_path_within_project_root_accepted(self, tmp_path: Path) -> None:
        """Absolute path inside project root is accepted."""
        project_root = tmp_path / "project"
        project_root.mkdir()
        evidence_dir = project_root / "work" / "evidence"

        result = _validate_evidence_dir(str(evidence_dir), project_root)

        assert result == evidence_dir.resolve()

    def test_relative_dotdot_path_rejected(self, tmp_path: Path) -> None:
        """Relative path with .. that escapes project root is rejected (FINDING-001)."""
        project_root = tmp_path / "project"
        project_root.mkdir()

        with pytest.raises(ValueError, match="outside the project root"):
            _validate_evidence_dir("../../tmp/exfil", project_root)

    def test_absolute_out_of_tree_path_rejected(self, tmp_path: Path) -> None:
        """Absolute path outside project root is rejected (FINDING-001)."""
        project_root = tmp_path / "project"
        project_root.mkdir()

        # Use /tmp which is guaranteed to be outside the project root in tmp_path
        with pytest.raises(ValueError, match="outside the project root"):
            _validate_evidence_dir("/tmp/world-readable", project_root)

    def test_sibling_directory_rejected(self, tmp_path: Path) -> None:
        """Sibling directory of project root is rejected (FINDING-001)."""
        project_root = tmp_path / "project"
        project_root.mkdir()
        sibling = tmp_path / "sibling"

        with pytest.raises(ValueError, match="outside the project root"):
            _validate_evidence_dir(str(sibling), project_root)

    def test_parent_directory_rejected(self, tmp_path: Path) -> None:
        """Parent directory of project root is rejected (FINDING-001)."""
        project_root = tmp_path / "project"
        project_root.mkdir()

        with pytest.raises(ValueError, match="outside the project root"):
            _validate_evidence_dir(str(tmp_path), project_root)

    def test_dotdot_that_stays_in_tree_accepted(self, tmp_path: Path) -> None:
        """Path with .. that resolves within the project root is accepted."""
        project_root = tmp_path / "project"
        sub_a = project_root / "sub" / "a"
        sub_a.mkdir(parents=True)
        # work/../work resolves to project_root/work -- still inside
        in_tree_path = project_root / "sub" / "a" / ".." / "b"

        # Should be accepted (resolves to project_root/sub/b)
        result = _validate_evidence_dir(str(in_tree_path), project_root)

        assert result == (project_root / "sub" / "b").resolve()
        # And the resolved path is still under project_root
        result.relative_to(project_root.resolve())  # should not raise

    def test_error_message_includes_override_and_root(self, tmp_path: Path) -> None:
        """Error message names the rejected path and the project root boundary."""
        project_root = tmp_path / "project"
        project_root.mkdir()
        bad_dir = "/tmp/leaked"

        with pytest.raises(ValueError) as exc_info:
            _validate_evidence_dir(bad_dir, project_root)

        error_text = str(exc_info.value)
        assert bad_dir in error_text
        assert str(project_root) in error_text

    def test_returns_resolved_path_not_raw(self, tmp_path: Path) -> None:
        """Return value is the .resolve()d absolute Path, not the raw input string."""
        project_root = tmp_path / "project"
        project_root.mkdir()
        # Use an absolute path inside the project root; the return must be absolute.
        evidence_dir = project_root / "work" / "evidence"

        result = _validate_evidence_dir(str(evidence_dir), project_root)

        assert result.is_absolute()
        assert result == evidence_dir.resolve()
