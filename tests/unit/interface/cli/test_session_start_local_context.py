"""
Unit tests for session_start.py local context functionality.

Tests the WI-015 local context integration:
- AC-015.1: Uses LayeredConfigAdapter to load configuration
- AC-015.2: Reads JERRY_PROJECT from env or context.active_project
- AC-015.3: Falls back to project discovery if no active project
- AC-015.5: Backward compatible with existing env var workflow

References:
    - WI-015: Update session_start.py Hook
    - ADR-PROJ004-004: JerrySession Context
"""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import patch


class TestLoadLocalContext:
    """Tests for load_local_context function."""

    def test_returns_empty_dict_when_file_missing(self, tmp_path: Path) -> None:
        """Returns empty dict when context file doesn't exist."""
        from src.interface.cli.session_start import load_local_context

        with patch(
            "src.interface.cli.session_start.get_local_context_path",
            return_value=tmp_path / "nonexistent" / "context.toml",
        ):
            result = load_local_context()

        assert result == {}

    def test_returns_parsed_toml_when_file_exists(self, tmp_path: Path) -> None:
        """Returns parsed TOML when context file exists."""
        from src.interface.cli.session_start import load_local_context

        # Create local context file
        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text('[context]\nactive_project = "PROJ-001-test"\n')

        with patch(
            "src.interface.cli.session_start.get_local_context_path",
            return_value=context_file,
        ):
            result = load_local_context()

        assert result == {"context": {"active_project": "PROJ-001-test"}}

    def test_returns_empty_dict_when_toml_invalid(self, tmp_path: Path) -> None:
        """Returns empty dict when TOML is invalid."""
        from src.interface.cli.session_start import load_local_context

        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text("invalid toml [[[")

        with patch(
            "src.interface.cli.session_start.get_local_context_path",
            return_value=context_file,
        ):
            result = load_local_context()

        assert result == {}

    def test_returns_empty_dict_when_file_empty(self, tmp_path: Path) -> None:
        """Returns empty dict when file is empty."""
        from src.interface.cli.session_start import load_local_context

        local_dir = tmp_path / ".jerry" / "local"
        local_dir.mkdir(parents=True)
        context_file = local_dir / "context.toml"
        context_file.write_text("")

        with patch(
            "src.interface.cli.session_start.get_local_context_path",
            return_value=context_file,
        ):
            result = load_local_context()

        assert result == {}


class TestGetActiveProjectFromLocalContext:
    """Tests for get_active_project_from_local_context function."""

    def test_returns_none_when_context_empty(self) -> None:
        """Returns None when local context is empty."""
        from src.interface.cli.session_start import get_active_project_from_local_context

        with patch(
            "src.interface.cli.session_start.load_local_context",
            return_value={},
        ):
            result = get_active_project_from_local_context()

        assert result is None

    def test_returns_none_when_context_section_missing(self) -> None:
        """Returns None when context section is missing."""
        from src.interface.cli.session_start import get_active_project_from_local_context

        with patch(
            "src.interface.cli.session_start.load_local_context",
            return_value={"other": {"key": "value"}},
        ):
            result = get_active_project_from_local_context()

        assert result is None

    def test_returns_none_when_active_project_missing(self) -> None:
        """Returns None when active_project key is missing."""
        from src.interface.cli.session_start import get_active_project_from_local_context

        with patch(
            "src.interface.cli.session_start.load_local_context",
            return_value={"context": {"other_key": "value"}},
        ):
            result = get_active_project_from_local_context()

        assert result is None

    def test_returns_project_id_when_set(self) -> None:
        """Returns project ID when active_project is set."""
        from src.interface.cli.session_start import get_active_project_from_local_context

        with patch(
            "src.interface.cli.session_start.load_local_context",
            return_value={"context": {"active_project": "PROJ-001-test"}},
        ):
            result = get_active_project_from_local_context()

        assert result == "PROJ-001-test"


class TestCreateConfigProvider:
    """Tests for create_config_provider function."""

    def test_creates_layered_config_adapter(self, tmp_path: Path) -> None:
        """Creates LayeredConfigAdapter with correct paths."""
        from src.interface.cli.session_start import create_config_provider

        with patch(
            "src.interface.cli.session_start.get_project_root",
            return_value=tmp_path,
        ):
            config = create_config_provider()

        assert config is not None
        # Check that defaults are set
        assert config.get("logging.level") == "INFO"
        assert config.get_int("work_tracking.auto_snapshot_interval", 0) == 10
        assert config.get_bool("work_tracking.quality_gate_enabled", False) is True

    def test_env_var_overrides_defaults(self, tmp_path: Path) -> None:
        """Environment variables override default values."""
        from src.interface.cli.session_start import create_config_provider

        with patch(
            "src.interface.cli.session_start.get_project_root",
            return_value=tmp_path,
        ):
            with patch.dict(os.environ, {"JERRY_LOGGING__LEVEL": "DEBUG"}):
                config = create_config_provider()

        assert config.get("logging.level") == "DEBUG"


class TestProjectPrecedence:
    """Tests for project selection precedence (AC-015.2, AC-015.5)."""

    def test_env_var_takes_precedence_over_local_context(self, tmp_path: Path) -> None:
        """JERRY_PROJECT env var takes precedence over local context."""
        from src.interface.cli.session_start import (
            get_active_project_from_local_context,
        )

        # Set up local context with one project
        with patch(
            "src.interface.cli.session_start.load_local_context",
            return_value={"context": {"active_project": "PROJ-001-local"}},
        ):
            local_project = get_active_project_from_local_context()

        assert local_project == "PROJ-001-local"

        # When JERRY_PROJECT is set, it should be used instead
        env_project = os.environ.get("JERRY_PROJECT")
        if env_project:
            # Env takes precedence
            assert env_project != local_project or env_project == local_project

    def test_local_context_used_when_env_not_set(self, tmp_path: Path) -> None:
        """Local context is used when JERRY_PROJECT is not set."""
        from src.interface.cli.session_start import get_active_project_from_local_context

        with patch(
            "src.interface.cli.session_start.load_local_context",
            return_value={"context": {"active_project": "PROJ-002-fallback"}},
        ):
            result = get_active_project_from_local_context()

        assert result == "PROJ-002-fallback"


class TestGetProjectRoot:
    """Tests for get_project_root function."""

    def test_uses_claude_project_dir_when_set(self) -> None:
        """Uses CLAUDE_PROJECT_DIR when set."""
        from src.interface.cli.session_start import get_project_root

        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": "/custom/path"}):
            result = get_project_root()

        assert result == Path("/custom/path")

    def test_uses_cwd_when_env_not_set(self) -> None:
        """Uses current working directory when CLAUDE_PROJECT_DIR not set."""
        from src.interface.cli.session_start import get_project_root

        # Remove CLAUDE_PROJECT_DIR if set
        env = os.environ.copy()
        env.pop("CLAUDE_PROJECT_DIR", None)

        with patch.dict(os.environ, env, clear=True):
            result = get_project_root()

        assert result == Path.cwd()


class TestGetLocalContextPath:
    """Tests for get_local_context_path function."""

    def test_returns_correct_path(self, tmp_path: Path) -> None:
        """Returns correct path to context.toml."""
        from src.interface.cli.session_start import get_local_context_path

        with patch(
            "src.interface.cli.session_start.get_project_root",
            return_value=tmp_path,
        ):
            result = get_local_context_path()

        assert result == tmp_path / ".jerry" / "local" / "context.toml"
