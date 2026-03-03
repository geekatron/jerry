# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Integration tests for `jerry ci detect-bump-type` CLI command.

Tests the full CLI path via subprocess to verify argument parsing,
output format, and exit codes.

References:
    - BUG-002: Version bump regex rejects uppercase scopes
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

pytestmark = [
    pytest.mark.integration,
    pytest.mark.subprocess,
]


@pytest.fixture()
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


class TestCliDetectBumpTypeHappy:
    """Happy path tests for CLI detect-bump-type."""

    @pytest.mark.happy_path
    def test_stdin_feat_returns_minor(self, project_root: Path) -> None:
        """feat commit via stdin returns 'minor'."""
        result = subprocess.run(
            ["uv", "run", "jerry", "ci", "detect-bump-type", "--commits-from-stdin"],
            input="feat(GH-122): add version detection\n",
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "minor"

    @pytest.mark.happy_path
    def test_stdin_fix_returns_patch(self, project_root: Path) -> None:
        """fix commit via stdin returns 'patch'."""
        result = subprocess.run(
            ["uv", "run", "jerry", "ci", "detect-bump-type", "--commits-from-stdin"],
            input="fix: correct edge case\n",
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "patch"

    @pytest.mark.happy_path
    def test_stdin_breaking_returns_major(self, project_root: Path) -> None:
        """Breaking change via stdin returns 'major'."""
        result = subprocess.run(
            ["uv", "run", "jerry", "ci", "detect-bump-type", "--commits-from-stdin"],
            input="feat(GH-122)!: breaking change\n",
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "major"

    @pytest.mark.happy_path
    def test_json_output_format(self, project_root: Path) -> None:
        """--json flag produces valid JSON output."""
        result = subprocess.run(
            ["uv", "run", "jerry", "--json", "ci", "detect-bump-type", "--commits-from-stdin"],
            input="feat: add feature\n",
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["bump_type"] == "minor"


class TestCliDetectBumpTypeNegative:
    """Negative tests for CLI detect-bump-type."""

    @pytest.mark.negative
    def test_stdin_docs_returns_none(self, project_root: Path) -> None:
        """Non-bumping commit type returns 'none'."""
        result = subprocess.run(
            ["uv", "run", "jerry", "ci", "detect-bump-type", "--commits-from-stdin"],
            input="docs: update README\n",
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "none"

    @pytest.mark.negative
    def test_stdin_empty_returns_none(self, project_root: Path) -> None:
        """Empty stdin returns 'none'."""
        result = subprocess.run(
            ["uv", "run", "jerry", "ci", "detect-bump-type", "--commits-from-stdin"],
            input="",
            capture_output=True,
            text=True,
            cwd=project_root,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "none"
