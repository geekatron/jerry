# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for the shared CLI project-root resolution helper (BUG-010, GH #337).

The helper anchors path-containment and configuration lookups to the USER'S
project root (``CLAUDE_PROJECT_DIR`` env var, else the current working
directory) — never to the Jerry installation's own directory tree.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.interface.cli.project_root import get_project_root


class TestGetProjectRoot:
    """Resolution order: CLAUDE_PROJECT_DIR env var, then cwd."""

    def test_get_project_root_when_claude_project_dir_set_then_returns_it(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """CLAUDE_PROJECT_DIR takes precedence over the working directory."""
        # Arrange
        project_dir = tmp_path / "user-project"
        project_dir.mkdir()
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", str(project_dir))

        # Act
        root = get_project_root()

        # Assert
        assert root == project_dir

    def test_get_project_root_when_env_absent_then_returns_cwd(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """Without the env var, the current working directory is the root."""
        # Arrange
        monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
        monkeypatch.chdir(tmp_path)

        # Act
        root = get_project_root()

        # Assert
        assert root == tmp_path

    def test_get_project_root_when_env_empty_string_then_returns_cwd(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """An empty CLAUDE_PROJECT_DIR is treated as unset, not as a valid root."""
        # Arrange
        monkeypatch.setenv("CLAUDE_PROJECT_DIR", "")
        monkeypatch.chdir(tmp_path)

        # Act
        root = get_project_root()

        # Assert
        assert root == tmp_path

    def test_get_project_root_never_resolves_to_install_tree(
        self, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
    ) -> None:
        """The resolver must not anchor to the Jerry source tree (the BUG-010 defect)."""
        # Arrange: simulate running from a user project unrelated to the install tree
        monkeypatch.delenv("CLAUDE_PROJECT_DIR", raising=False)
        monkeypatch.chdir(tmp_path)
        install_tree = Path(__file__).resolve().parents[4]

        # Act
        root = get_project_root()

        # Assert
        assert root != install_tree
