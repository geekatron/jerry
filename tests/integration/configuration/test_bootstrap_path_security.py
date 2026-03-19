# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Security tests for bootstrap.get_project_data_path() boundary enforcement.

Tests cover:
    - SRR-FIND-001 (CWE-22): Path traversal via '../' in output.base_path
    - SRR-FIND-002 (CWE-73): Symlink escape outside project root

References:
    - GitHub Issue #192: Configurable output base path
    - Security Review: FIND-001 (CVSS 7.1), FIND-002 (CVSS 6.3)
    - Gate Discharge Criteria: code-review-gate.md
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch

import pytest


class TestPathTraversalPrevention:
    """SRR-FIND-001: CWE-22 path traversal via '../' sequences."""

    def test_path_traversal_via_dotdot_raises_value_error(self, tmp_path: Path) -> None:
        """Config with '../' that escapes project root must raise ValueError."""
        from src.bootstrap import get_project_data_path

        config_file = tmp_path / ".jerry" / "config.toml"
        config_file.parent.mkdir(parents=True)
        config_file.write_text('[output]\nbase_path = "../../escape-attempt"\n')

        env = {
            "CLAUDE_PROJECT_DIR": str(tmp_path),
            "JERRY_OUTPUT__BASE_PATH": "../../escape-attempt",
        }
        # Remove JERRY_PROJECT so config takes priority
        env_clean = {k: v for k, v in os.environ.items() if k != "JERRY_PROJECT"}
        env_clean.update(env)

        with patch.dict(os.environ, env_clean, clear=True):
            with pytest.raises(ValueError, match="escapes project root"):
                get_project_data_path()

    def test_deeply_nested_path_traversal_raises_value_error(self, tmp_path: Path) -> None:
        """Deeply nested '../' sequences must also be caught."""
        from src.bootstrap import get_project_data_path

        env = {
            "CLAUDE_PROJECT_DIR": str(tmp_path),
            "JERRY_OUTPUT__BASE_PATH": "a/b/c/../../../../escape",
        }
        env_clean = {k: v for k, v in os.environ.items() if k != "JERRY_PROJECT"}
        env_clean.update(env)

        with patch.dict(os.environ, env_clean, clear=True):
            with pytest.raises(ValueError, match="escapes project root"):
                get_project_data_path()

    def test_relative_path_within_root_succeeds(self, tmp_path: Path) -> None:
        """Path with '..' that stays within project root must succeed."""
        from src.bootstrap import get_project_data_path

        # Create the directory so resolve() works correctly
        nested = tmp_path / "a" / "b"
        nested.mkdir(parents=True)

        env = {
            "CLAUDE_PROJECT_DIR": str(tmp_path),
            "JERRY_OUTPUT__BASE_PATH": "a/b/../c",
        }
        env_clean = {k: v for k, v in os.environ.items() if k != "JERRY_PROJECT"}
        env_clean.update(env)

        with patch.dict(os.environ, env_clean, clear=True):
            result = get_project_data_path()

        assert result is not None
        resolved_root = tmp_path.resolve()
        assert str(result.resolve()).startswith(str(resolved_root))


class TestSymlinkEscapePrevention:
    """SRR-FIND-002: CWE-73 symlink escape outside project root."""

    def test_symlink_to_outside_directory_raises_value_error(self, tmp_path: Path) -> None:
        """Symlink pointing outside project root must raise ValueError."""
        from src.bootstrap import get_project_data_path

        # Create an outside directory
        outside_dir = tmp_path / "outside"
        outside_dir.mkdir()

        # Create project root
        project_root = tmp_path / "project"
        project_root.mkdir()

        # Create symlink inside project pointing outside
        symlink_path = project_root / "evil-link"
        symlink_path.symlink_to(outside_dir)

        env = {
            "CLAUDE_PROJECT_DIR": str(project_root),
            "JERRY_OUTPUT__BASE_PATH": "evil-link",
        }
        env_clean = {k: v for k, v in os.environ.items() if k != "JERRY_PROJECT"}
        env_clean.update(env)

        with patch.dict(os.environ, env_clean, clear=True):
            with pytest.raises(ValueError, match="escapes project root"):
                get_project_data_path()

    def test_symlink_within_project_root_succeeds(self, tmp_path: Path) -> None:
        """Symlink pointing to a directory within project root must succeed."""
        from src.bootstrap import get_project_data_path

        # Create target inside project root
        target = tmp_path / "actual-output"
        target.mkdir()

        # Create symlink to target (both inside tmp_path)
        symlink_path = tmp_path / "output-link"
        symlink_path.symlink_to(target)

        env = {
            "CLAUDE_PROJECT_DIR": str(tmp_path),
            "JERRY_OUTPUT__BASE_PATH": "output-link",
        }
        env_clean = {k: v for k, v in os.environ.items() if k != "JERRY_PROJECT"}
        env_clean.update(env)

        with patch.dict(os.environ, env_clean, clear=True):
            result = get_project_data_path()

        assert result is not None
        resolved_root = tmp_path.resolve()
        assert str(result.resolve()).startswith(str(resolved_root))


class TestLegitimatePathsUnaffected:
    """Verify the security fix does not break legitimate use cases."""

    def test_jerry_project_fallback_still_works(self, tmp_path: Path) -> None:
        """JERRY_PROJECT fallback (projects/{id}/) must still work."""
        from src.bootstrap import get_project_data_path

        env = {
            "CLAUDE_PROJECT_DIR": str(tmp_path),
            "JERRY_PROJECT": "PROJ-001",
        }
        # Remove any output base path env vars
        env_clean = {
            k: v
            for k, v in os.environ.items()
            if "OUTPUT__BASE_PATH" not in k and k != "JERRY_PROJECT"
        }
        env_clean.update(env)

        with patch.dict(os.environ, env_clean, clear=True):
            result = get_project_data_path()

        assert result is not None
        assert "projects" in str(result)
        assert "PROJ-001" in str(result)

    def test_terminal_fallback_returns_none_without_project(self, tmp_path: Path) -> None:
        """work/ fallback without JERRY_PROJECT returns None (backward compat)."""
        from src.bootstrap import get_project_data_path

        env = {"CLAUDE_PROJECT_DIR": str(tmp_path)}
        env_clean = {
            k: v
            for k, v in os.environ.items()
            if "OUTPUT__BASE_PATH" not in k and k != "JERRY_PROJECT" and k != "CLAUDE_PROJECT_DIR"
        }
        env_clean.update(env)

        with patch.dict(os.environ, env_clean, clear=True):
            result = get_project_data_path()

        assert result is None
