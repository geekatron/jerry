"""
E2E tests for CLI config commands.

Tests the WI-016 config command implementations:
- AC-016.1: jerry config show displays merged configuration
- AC-016.2: jerry config show --json outputs JSON format
- AC-016.3: jerry config get <key> retrieves specific value
- AC-016.4: jerry config set <key> <value> --scope writes to appropriate file
- AC-016.5: jerry config path shows config file locations

References:
    - WI-016: CLI Config Commands
    - ADR-PROJ004-004: JerrySession Context (5-level precedence)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

# Capture project root before any chdir happens
PROJECT_ROOT = Path(__file__).parent.parent.parent


class TestConfigShow:
    """Tests for jerry config show command."""

    def test_config_show_displays_defaults(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Config show displays default configuration values."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        result = subprocess.run(
            [sys.executable, "-m", "src.interface.cli.main", "config", "show"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
        )

        assert result.returncode == 0
        # Should show defaults
        assert "logging.level" in result.stdout or "KEY" in result.stdout

    def test_config_show_json_outputs_valid_json(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Config show --json outputs valid JSON."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        result = subprocess.run(
            [sys.executable, "-m", "src.interface.cli.main", "--json", "config", "show"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
        )

        assert result.returncode == 0
        # Output should be valid JSON
        data = json.loads(result.stdout)
        assert isinstance(data, dict)


class TestConfigGet:
    """Tests for jerry config get command."""

    def test_config_get_returns_default_value(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Config get returns default value for known key."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        result = subprocess.run(
            [sys.executable, "-m", "src.interface.cli.main", "config", "get", "logging.level"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
        )

        assert result.returncode == 0
        assert "INFO" in result.stdout

    def test_config_get_returns_error_for_unknown_key(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Config get returns error for unknown key."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        result = subprocess.run(
            [sys.executable, "-m", "src.interface.cli.main", "config", "get", "nonexistent.key"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
        )

        assert result.returncode == 1
        assert "not found" in result.stdout.lower() or "not found" in result.stderr.lower()

    def test_config_get_json_outputs_with_source(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Config get --json outputs value with source."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        result = subprocess.run(
            [sys.executable, "-m", "src.interface.cli.main", "--json", "config", "get", "logging.level"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
        )

        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["key"] == "logging.level"
        assert data["value"] == "INFO"
        assert data["source"] == "default"


class TestConfigPath:
    """Tests for jerry config path command."""

    def test_config_path_shows_paths(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Config path shows configuration file paths."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        result = subprocess.run(
            [sys.executable, "-m", "src.interface.cli.main", "config", "path"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
        )

        assert result.returncode == 0
        assert "Root:" in result.stdout
        assert "Local:" in result.stdout
        assert "config.toml" in result.stdout

    def test_config_path_shows_project_path_when_set(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Config path shows project path when JERRY_PROJECT is set."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("JERRY_PROJECT", "PROJ-001-test")

        result = subprocess.run(
            [sys.executable, "-m", "src.interface.cli.main", "config", "path"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT), "JERRY_PROJECT": "PROJ-001-test"},
        )

        assert result.returncode == 0
        assert "Project:" in result.stdout
        assert "PROJ-001-test" in result.stdout

    def test_config_path_json_outputs_all_paths(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Config path --json outputs all paths."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.setenv("JERRY_PROJECT", "PROJ-001-test")

        result = subprocess.run(
            [sys.executable, "-m", "src.interface.cli.main", "--json", "config", "path"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT), "JERRY_PROJECT": "PROJ-001-test"},
        )

        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "paths" in data
        assert "root" in data["paths"]
        assert "local" in data["paths"]
        assert "project" in data["paths"]
        assert data["active_project"] == "PROJ-001-test"


class TestConfigSet:
    """Tests for jerry config set command."""

    def test_config_set_requires_project_for_project_scope(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Config set with project scope requires JERRY_PROJECT."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        result = subprocess.run(
            [sys.executable, "-m", "src.interface.cli.main", "config", "set", "test.key", "value"],
            capture_output=True,
            text=True,
            cwd=tmp_path,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
        )

        assert result.returncode == 1
        assert "No active project" in result.stdout or "No active project" in result.stderr

    def test_config_set_writes_to_root_scope(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Config set with root scope writes to root config."""
        monkeypatch.chdir(tmp_path)
        monkeypatch.delenv("JERRY_PROJECT", raising=False)

        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "src.interface.cli.main",
                "config",
                "set",
                "test.key",
                "testvalue",
                "--scope",
                "root",
            ],
            capture_output=True,
            text=True,
            cwd=tmp_path,
            env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
        )

        assert result.returncode == 0
        assert "Set test.key" in result.stdout

        # Verify file was created
        config_path = tmp_path / ".jerry" / "config.toml"
        assert config_path.exists()
        content = config_path.read_text()
        assert "testvalue" in content
