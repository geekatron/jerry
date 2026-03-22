# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Unit tests for CLM-002: worktree-isolated compose project names.

Naming: test_{scenario}_when_{condition}_then_{expected}
Distribution: 60% happy / 30% negative / 10% edge
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.tool_exec.infrastructure.container_lifecycle.worktree_isolation import (
    derive_compose_project_name,
    session_state_path,
)


class TestDeriveComposeProjectName:
    """CLM-002: derive_compose_project_name function."""

    # --- Happy path (60%) ---

    def test_derive_name_when_explicit_root_given_then_returns_rainbow_hash_format(
        self,
    ) -> None:
        """Explicit project_root produces rainbow-{8-char-hex} format."""
        name = derive_compose_project_name(Path("/some/worktree/path"))
        assert name.startswith("rainbow-")
        assert len(name) == len("rainbow-") + 8

    def test_derive_name_when_same_path_called_twice_then_returns_identical_name(
        self,
    ) -> None:
        """Deterministic: same input always produces same output."""
        path = Path("/consistent/worktree")
        assert derive_compose_project_name(path) == derive_compose_project_name(path)

    def test_derive_name_when_claude_project_dir_set_then_uses_env_var(self) -> None:
        """CLAUDE_PROJECT_DIR env var is the primary source."""
        with patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": "/env/path"}, clear=False):
            name = derive_compose_project_name(None)
            expected = derive_compose_project_name(Path("/env/path"))
            assert name == expected

    def test_derive_name_when_env_empty_and_git_available_then_uses_git(self) -> None:
        """Falls back to git rev-parse when CLAUDE_PROJECT_DIR is empty."""
        with (
            patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": ""}, clear=False),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0, stdout="/git/toplevel\n")
            name = derive_compose_project_name(None)
            expected = derive_compose_project_name(Path("/git/toplevel"))
            assert name == expected

    def test_derive_name_when_explicit_root_then_never_returns_bare_rainbow(
        self,
    ) -> None:
        """With explicit root, name always includes hash suffix."""
        assert derive_compose_project_name(Path("/any/path")) != "rainbow"

    def test_derive_name_when_hash_computed_then_contains_only_hex_chars(self) -> None:
        """Hash suffix is lowercase hexadecimal."""
        name = derive_compose_project_name(Path("/test"))
        suffix = name.replace("rainbow-", "")
        assert all(c in "0123456789abcdef" for c in suffix)

    # --- Negative (30%) ---

    def test_derive_name_when_different_paths_then_returns_different_names(
        self,
    ) -> None:
        """Two different worktree paths produce different project names."""
        name_a = derive_compose_project_name(Path("/worktree/a"))
        name_b = derive_compose_project_name(Path("/worktree/b"))
        assert name_a != name_b

    def test_derive_name_when_git_unavailable_then_returns_bare_rainbow(self) -> None:
        """Returns fallback 'rainbow' when neither env var nor git works."""
        with (
            patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": ""}, clear=False),
            patch("subprocess.run", side_effect=FileNotFoundError),
        ):
            assert derive_compose_project_name(None) == "rainbow"

    def test_derive_name_when_git_times_out_then_returns_bare_rainbow(self) -> None:
        """Returns fallback 'rainbow' when git times out."""
        with (
            patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": ""}, clear=False),
            patch(
                "subprocess.run",
                side_effect=subprocess.TimeoutExpired("git", 10),
            ),
        ):
            assert derive_compose_project_name(None) == "rainbow"

    def test_derive_name_when_git_fails_then_returns_bare_rainbow(self) -> None:
        """Returns fallback 'rainbow' when git rev-parse exits non-zero."""
        with (
            patch.dict("os.environ", {"CLAUDE_PROJECT_DIR": ""}, clear=False),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=128, stdout="")
            assert derive_compose_project_name(None) == "rainbow"

    # --- Edge (10%) ---

    def test_derive_name_when_path_has_special_chars_then_hashes_safely(self) -> None:
        """Paths with spaces and special characters hash without error."""
        name = derive_compose_project_name(Path("/path with spaces/and-dashes/"))
        assert name.startswith("rainbow-")
        assert len(name) == len("rainbow-") + 8


class TestSessionStatePath:
    """CLM-002: session_state_path function."""

    # --- Happy path ---

    def test_state_path_when_root_given_then_returns_work_subdir(self) -> None:
        """State file lives under work/ directory."""
        root = Path("/test/project")
        path = session_state_path(root)
        assert path.parent == root / "work"

    def test_state_path_when_root_given_then_has_yaml_extension(self) -> None:
        """State file is a YAML file."""
        assert session_state_path(Path("/root")).suffix == ".yaml"

    def test_state_path_when_root_given_then_is_dotfile(self) -> None:
        """State file is a dotfile (hidden, gitignored)."""
        path = session_state_path(Path("/root"))
        assert path.name.startswith(".")

    # --- Negative ---

    def test_state_path_when_different_roots_then_returns_different_paths(self) -> None:
        """Different project roots produce different state file paths."""
        assert session_state_path(Path("/root/a")) != session_state_path(Path("/root/b"))
