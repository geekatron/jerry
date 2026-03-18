# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Shared pytest fixtures for tool_exec BDD tests.

All fixtures used across UC-TOOLEXEC-001 through UC-TOOLEXEC-006 live here.
Step-file-specific helpers are colocated with those step files.

Security note: No literal credential-format strings appear in this file.
Canary credential values are loaded at test runtime from the generated
canary fixture files under skills/rainbow/tests/credential-fixtures/.
"""

from __future__ import annotations

import argparse
import subprocess
import textwrap
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.tool_exec.domain.services.credential_filter import CredentialFilterService
from src.tool_exec.domain.services.engagement_initializer import EngagementInitializer

# ---------------------------------------------------------------------------
# Canary fixture support
# ---------------------------------------------------------------------------

FIXTURE_BASE = Path("skills/rainbow/tests/credential-fixtures")

REQUIRED_CATEGORIES = [
    "aws-key",
    "api-token",
    "ssh-key",
    "ntlm-hash",
    "kerberos",
    "connection-string",
    "plaintext-password",
    "github-pat",
    "jwt-token",
]


@pytest.fixture(scope="session", autouse=True)
def ensure_canaries_generated() -> None:
    """Regenerate canary fixtures if any category canary.txt is missing."""
    if not FIXTURE_BASE.exists():
        return
    missing = [
        cat for cat in REQUIRED_CATEGORIES if not (FIXTURE_BASE / cat / "canary.txt").exists()
    ]
    if missing:
        subprocess.run(
            [
                "uv",
                "run",
                "python",
                str(FIXTURE_BASE / "generate_canaries.py"),
            ],
            check=True,
        )


def load_canary(category: str) -> str:
    """Return the full text of a canary fixture file.

    Args:
        category: Subdirectory name under credential-fixtures/.

    Returns:
        File content as a string.
    """
    canary_path = FIXTURE_BASE / category / "canary.txt"
    if not canary_path.exists():
        pytest.skip(f"Canary fixture missing: {canary_path}. Run generate_canaries.py first.")
    return canary_path.read_text(encoding="utf-8")


def load_canary_line(category: str, test_label: str) -> str:
    """Extract a single test line from a canary fixture by its section label.

    Canary files use '# --- Test N: {label} ---' section headers.
    Returns the first non-comment, non-blank line after the matching header.

    Args:
        category: Subdirectory name under credential-fixtures/.
        test_label: Substring to match in the section header (case-sensitive).

    Returns:
        The first content line in that section.

    Raises:
        KeyError: If no section matching test_label is found.
    """
    lines = load_canary(category).splitlines()
    found = False
    for line in lines:
        if found:
            if line.strip() and not line.startswith("#"):
                return line.strip()
        elif test_label in line and line.startswith("# --- Test"):
            found = True
    raise KeyError(f"Section '{test_label}' not found in {category}/canary.txt")


# ---------------------------------------------------------------------------
# Tool families YAML content helper
# ---------------------------------------------------------------------------


def _build_minimal_tool_exec_yaml() -> str:
    """Build a minimal tool-exec.yaml content for test instantiation.

    Returns:
        YAML content string covering Zone 1, 2, and 3 tools.
    """
    return textwrap.dedent(
        """\
        default_mode: local
        tool_resolution:
          # Zone 1 supply-chain scanners
          - prefix: syft
            zone: "1"
            service: supply-chain
            compose_file: docker/supply-chain/docker-compose.yml
            sub_skill: rainbow-supply-chain

          - prefix: checkov
            zone: "1"
            service: supply-chain
            compose_file: docker/supply-chain/docker-compose.yml
            sub_skill: rainbow-supply-chain

          - prefix: grype
            zone: "1"
            service: supply-chain
            compose_file: docker/supply-chain/docker-compose.yml
            sub_skill: rainbow-supply-chain

          # Zone 2 reconnaissance
          - prefix: nuclei
            zone: "2"
            service: recon-pipeline
            compose_file: docker/recon/docker-compose.yml
            sub_skill: rainbow-recon

          - prefix: subfinder
            zone: "2"
            service: recon-pipeline
            compose_file: docker/recon/docker-compose.yml
            sub_skill: rainbow-recon

          # Zone 3 exploitation
          - prefix: msfconsole
            zone: "3"
            service: exploit-ops
            compose_file: docker/exploit/docker-compose.yml
            sub_skill: rainbow-exploit

          - prefix: "impacket-*"
            zone: "3"
            service: exploit-ops
            compose_file: docker/exploit/docker-compose.yml
            sub_skill: rainbow-exploit
        """
    )


# ---------------------------------------------------------------------------
# Core fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the repository root directory.

    Returns:
        Absolute path to the repository root.
    """
    # Walk up from this file until we find .git or pyproject.toml
    current = Path(__file__).parent
    while current != current.parent:
        if (current / ".git").exists() or (current / "pyproject.toml").exists():
            return current
        current = current.parent
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture
def tool_families_yaml_content() -> str:
    """Return minimal tool_families.yaml content for test isolation.

    Returns:
        YAML content string for a registry containing the rainbow family only.
    """
    return textwrap.dedent(
        """\
        families:
          - name: rainbow
            description: "Rainbow cybersecurity tool suite"
            resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
            resolver_class: RainbowToolResolver
            config_path: test-tool-exec.yaml
            enabled: true
            priority: 10
        """
    )


@pytest.fixture
def tool_families_registry_path(tmp_path: Path, tool_families_yaml_content: str) -> Path:
    """Write tool_families.yaml to a temp file and return its path.

    Args:
        tmp_path: pytest-provided temporary directory.
        tool_families_yaml_content: YAML content to write.

    Returns:
        Path to the written registry file.
    """
    registry_file = tmp_path / "tool_families.yaml"
    registry_file.write_text(tool_families_yaml_content, encoding="utf-8")
    return registry_file


@pytest.fixture
def minimal_rainbow_config_path(tmp_path: Path) -> Path:
    """Write a minimal tool-exec.yaml for RainbowToolResolver test instantiation.

    Args:
        tmp_path: pytest-provided temporary directory.

    Returns:
        Path to the written config file.
    """
    content = _build_minimal_tool_exec_yaml()
    config_file = tmp_path / "test-tool-exec.yaml"
    config_file.write_text(content, encoding="utf-8")
    return config_file


@pytest.fixture
def engagement_dir(tmp_path: Path) -> tuple[EngagementInitializer, str]:
    """Initialize a test engagement directory and return (initializer, engagement_id).

    Args:
        tmp_path: pytest-provided temporary directory.

    Returns:
        Tuple of (EngagementInitializer instance, engagement_id string).
    """
    engagement_id = "pentest-2026-001"
    initializer = EngagementInitializer(base_dir=tmp_path / "work" / "engagements")
    initializer.initialize(engagement_id, created_by="test-runner")
    return initializer, engagement_id


@pytest.fixture
def engagement_initializer(tmp_path: Path) -> EngagementInitializer:
    """Return an EngagementInitializer with no engagements created.

    Args:
        tmp_path: pytest-provided temporary directory.

    Returns:
        EngagementInitializer instance pointing at tmp_path.
    """
    return EngagementInitializer(base_dir=tmp_path / "work" / "engagements")


@pytest.fixture
def credential_filter() -> CredentialFilterService:
    """Return a real CredentialFilterService with the base 15 patterns.

    Returns:
        CredentialFilterService instance.
    """
    return CredentialFilterService()


# ---------------------------------------------------------------------------
# CLI invocation fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def cli_invoke(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]):
    """Return a helper that invokes handle_tool_exec with a patched project root.

    The helper patches _find_project_root() to return tmp_path, writes a
    minimal tool_families.yaml there, and calls handle_tool_exec(args).

    Args:
        tmp_path: pytest temporary directory (used as the project root).
        monkeypatch: pytest monkeypatch fixture.
        capsys: pytest capsys fixture for stdout/stderr capture.

    Returns:
        Callable that accepts an argparse.Namespace and optional kwargs, and
        returns {"exit_code": int, "stdout": str, "stderr": str}.
    """
    from src.interface.cli.tool_exec_commands import handle_tool_exec

    def _invoke(
        args: argparse.Namespace,
        *,
        families_yaml_content: str | None = None,
        rainbow_config_content: str | None = None,
        subprocess_run_side_effect: Any = None,
        subprocess_run_return: Any = None,
        strict_mode: str = "false",
        extra_env: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Invoke handle_tool_exec with a mocked project root.

        Args:
            args: Argparse Namespace with tool exec arguments.
            families_yaml_content: Optional custom tool_families.yaml content.
                Defaults to the minimal rainbow registry.
            rainbow_config_content: Optional custom tool-exec.yaml content.
                Defaults to the minimal tool config.
            subprocess_run_side_effect: Side effect for subprocess.run mock.
            subprocess_run_return: Return value for subprocess.run mock.
            strict_mode: JERRY_STRICT_MODE value (default "false").
            extra_env: Additional environment variables to set.

        Returns:
            Dict with keys: exit_code (int), stdout (str), stderr (str).
        """
        # Write tool_families.yaml
        yaml_content = families_yaml_content or textwrap.dedent(
            """\
            families:
              - name: rainbow
                description: "Rainbow cybersecurity tool suite"
                resolver_module: src.tool_exec.infrastructure.adapters.rainbow_tool_resolver
                resolver_class: RainbowToolResolver
                config_path: test-tool-exec.yaml
                enabled: true
                priority: 10
            """
        )
        (tmp_path / "tool_families.yaml").write_text(yaml_content, encoding="utf-8")

        # Write test-tool-exec.yaml (the rainbow family config)
        config_content = rainbow_config_content or _build_minimal_tool_exec_yaml()
        (tmp_path / "test-tool-exec.yaml").write_text(config_content, encoding="utf-8")

        # Set up environment
        monkeypatch.setenv("JERRY_STRICT_MODE", strict_mode)
        if extra_env:
            for k, v in extra_env.items():
                monkeypatch.setenv(k, v)

        # Patch project root
        monkeypatch.setattr(
            "src.interface.cli.tool_exec_commands._find_project_root",
            lambda: tmp_path,
        )

        # Set up subprocess mock
        # Note: subprocess.run is called with text=True so stdout/stderr are str, not bytes.
        if subprocess_run_return is not None:
            mock_result = subprocess_run_return
        else:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "mock tool output\n"
            mock_result.stderr = ""

        if subprocess_run_side_effect is not None:
            with patch("subprocess.run", side_effect=subprocess_run_side_effect):
                with patch("subprocess.check_output", side_effect=subprocess_run_side_effect):
                    exit_code = handle_tool_exec(args)
        else:
            with patch("subprocess.run", return_value=mock_result):
                with patch("subprocess.check_output", return_value=b""):
                    exit_code = handle_tool_exec(args)

        captured = capsys.readouterr()
        return {
            "exit_code": int(exit_code),
            "stdout": captured.out,
            "stderr": captured.err,
        }

    return _invoke


# ---------------------------------------------------------------------------
# Argparse namespace builder helper
# ---------------------------------------------------------------------------


def make_exec_args(**kwargs: Any) -> argparse.Namespace:
    """Build an argparse.Namespace for tool exec invocation.

    Provides sensible defaults for all known tool exec arguments.
    Pass keyword arguments to override specific fields.

    Args:
        **kwargs: Field overrides for the Namespace.

    Returns:
        argparse.Namespace with all tool exec fields populated.
    """
    defaults: dict[str, Any] = {
        "namespace": "tool",
        "command": "exec",
        "tool_command": None,
        "tool_args": [],
        "mode": None,
        "family": None,
        "engagement_id": None,
        "evidence_dir": None,
        "init_engagement": None,
        "zone": None,
        "no_filter": False,
        "health_check": False,
        "list_families": False,
        "list_tools": None,
        "verbose": False,
    }
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)


def make_tool_args(**kwargs: Any) -> argparse.Namespace:
    """Build an argparse.Namespace for jerry tool (non-exec) commands.

    Args:
        **kwargs: Field overrides.

    Returns:
        argparse.Namespace with tool command fields.
    """
    defaults: dict[str, Any] = {
        "namespace": "tool",
        "command": None,
        "tool_command": None,
        "tool_args": [],
        "mode": None,
        "family": None,
        "engagement_id": None,
        "evidence_dir": None,
        "init_engagement": None,
        "zone": None,
        "no_filter": False,
        "health_check": False,
        "list_families": False,
        "list_tools": None,
        "verbose": False,
    }
    defaults.update(kwargs)
    return argparse.Namespace(**defaults)
