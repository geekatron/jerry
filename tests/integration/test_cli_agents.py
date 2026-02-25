# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for the ``jerry agents`` CLI commands via subprocess.

Executes the real CLI through ``uv run jerry agents ...`` to validate:
- Discovery (list), schema validation (validate), and inspection (show)
- Exit codes, output content, and error handling
- Filter and raw-mode flags

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - EN-006: Integration test suite for CLI commands
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

# Mark entire module as integration + subprocess tests
pytestmark = [
    pytest.mark.integration,
    pytest.mark.subprocess,
]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def repo_root() -> Path:
    """Locate the repository root by finding pyproject.toml."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    msg = "Could not find repository root (no pyproject.toml in parent directories)"
    raise FileNotFoundError(msg)


@pytest.fixture
def env_with_pythonpath(repo_root: Path) -> dict[str, str]:
    """Create environment with PYTHONPATH set to project root."""
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{repo_root}:{existing}" if existing else str(repo_root)
    return env


def run_jerry(
    args: list[str],
    repo_root: Path,
    env: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    """Execute ``jerry`` CLI via ``uv run``.

    Args:
        args: Command arguments after ``jerry`` (e.g. ``["agents", "list"]``).
        repo_root: Repository root used as working directory.
        env: Environment variables.

    Returns:
        CompletedProcess with stdout, stderr, and returncode.
    """
    return subprocess.run(
        ["uv", "run", "jerry", *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(repo_root),
    )


# =============================================================================
# Tests
# =============================================================================


class TestAgentsList:
    """Tests for ``jerry agents list``."""

    def test_agents_list_returns_all_agents(
        self,
        repo_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """``jerry agents list`` exits 0 and reports 58 agents."""
        result = run_jerry(
            ["agents", "list"],
            repo_root=repo_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        assert "58 agents" in result.stdout, (
            f"Expected '58 agents' in output, got:\n{result.stdout}"
        )

    def test_agents_list_filter_by_skill(
        self,
        repo_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """``jerry agents list --skill nasa-se`` shows only nasa-se agents."""
        result = run_jerry(
            ["agents", "list", "--skill", "nasa-se"],
            repo_root=repo_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        # All listed agents should be from the nasa-se skill
        lines = result.stdout.strip().splitlines()
        # Skip the header line and separator, and the summary line at the end
        data_lines = [
            ln
            for ln in lines
            if ln.strip()
            and not ln.startswith("-")
            and not ln.startswith("Name")
            and "agents found" not in ln
        ]
        assert len(data_lines) > 0, "Expected at least one nasa-se agent in output"
        for line in data_lines:
            assert "nasa-se" in line, f"Expected 'nasa-se' in every data row, but got: {line}"


class TestAgentsValidate:
    """Tests for ``jerry agents validate``."""

    def test_agents_validate_all_pass(
        self,
        repo_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """``jerry agents validate`` exits 0 and reports 58 passed, 0 failed."""
        result = run_jerry(
            ["agents", "validate"],
            repo_root=repo_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        assert "58 passed, 0 failed" in result.stdout, (
            f"Expected '58 passed, 0 failed' in output, got:\n{result.stdout}"
        )

    def test_agents_validate_single_agent(
        self,
        repo_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """``jerry agents validate ps-researcher`` exits 0."""
        result = run_jerry(
            ["agents", "validate", "ps-researcher"],
            repo_root=repo_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )


class TestAgentsShow:
    """Tests for ``jerry agents show``."""

    def test_agents_show_composed(
        self,
        repo_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """``jerry agents show ps-researcher`` exits 0 and outputs merged config."""
        result = run_jerry(
            ["agents", "show", "ps-researcher"],
            repo_root=repo_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        # The composed output should contain both agent-specific and default fields
        assert "ps-researcher" in result.stdout
        assert "constitution" in result.stdout, (
            "Composed output should include 'constitution' from defaults"
        )

    def test_agents_show_raw(
        self,
        repo_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """``jerry agents show ps-researcher --raw`` exits 0."""
        result = run_jerry(
            ["agents", "show", "ps-researcher", "--raw"],
            repo_root=repo_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        assert "ps-researcher" in result.stdout

    def test_agents_show_invalid_agent(
        self,
        repo_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """``jerry agents show nonexistent-agent`` exits 1."""
        result = run_jerry(
            ["agents", "show", "nonexistent-agent"],
            repo_root=repo_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 1, (
            f"Expected exit 1, got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )


class TestAgentsHelp:
    """Tests for ``jerry agents --help``."""

    def test_agents_help(
        self,
        repo_root: Path,
        env_with_pythonpath: dict[str, str],
    ) -> None:
        """``jerry agents --help`` exits 0."""
        result = run_jerry(
            ["agents", "--help"],
            repo_root=repo_root,
            env=env_with_pythonpath,
        )

        assert result.returncode == 0, (
            f"Expected exit 0, got {result.returncode}.\n"
            f"stderr: {result.stderr}\nstdout: {result.stdout}"
        )
        assert "agents" in result.stdout.lower()
