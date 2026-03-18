# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""E2E conftest for jerry tool exec tests.

TASK-029: Docker availability guard, project_root fixture, cli_run fixture.
TASK-030: Docker Compose session-scoped build+up+teardown fixture.

Design constraints:
- No mocks. All CLI calls go through the real `uv run jerry` subprocess.
- Docker is required. Tests skip at session scope when Docker is unavailable.
- Compose containers are built and started once per session, torn down at end.
- Engagement directories are created under the real project root and cleaned up
  after each test that creates them.

Security notes:
- All engagement IDs are prefixed with E2E-TEST- to make cleanup deterministic.
- Subprocess calls use timeout=60 to prevent test suite hangs.
- No shell=True anywhere (CWE-78 mitigation).

References:
    - TASK-029: conftest.py base structure
    - TASK-030: Docker Compose session fixture
    - ADR-PROJ023-001: Behavioral Contract
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Internal helpers (not fixtures)
# ---------------------------------------------------------------------------


def _docker_available() -> bool:
    """Return True when docker daemon is reachable.

    Uses `docker info` which returns non-zero when the daemon is not running
    or the socket is not accessible. Timeout is 10 s to avoid blocking CI.
    """
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


# ---------------------------------------------------------------------------
# pytest hooks
# ---------------------------------------------------------------------------


def pytest_configure(config: pytest.Config) -> None:
    """Register the e2e marker so pytest does not warn about unknown markers."""
    config.addinivalue_line(
        "markers",
        "e2e: end-to-end tests requiring Docker and real CLI invocation",
    )


# ---------------------------------------------------------------------------
# Session-scoped fixtures
# ---------------------------------------------------------------------------

_COMPOSE_FILE = "skills/rainbow-supply-chain/tests/docker/docker-compose.yml"


@pytest.fixture(scope="session", autouse=True)
def docker_guard() -> None:
    """Skip the entire E2E session when Docker is not available.

    Runs automatically for all tests in this package.  When Docker is absent
    (e.g., macOS without Docker Desktop, or a CI runner without Docker socket)
    the skip propagates through all tests so no false failures are recorded.
    """
    if not _docker_available():
        pytest.skip("Docker daemon not available -- skipping all E2E tool_exec tests")


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the absolute project root by walking up from this file.

    Looks for pyproject.toml as the canonical root marker so the fixture
    works regardless of cwd at test invocation time.
    """
    candidate = Path(__file__).resolve()
    while candidate != candidate.parent:
        if (candidate / "pyproject.toml").exists():
            return candidate
        candidate = candidate.parent
    pytest.fail("Could not locate pyproject.toml -- cannot determine project root")


@pytest.fixture(scope="session", autouse=True)
def docker_compose_up(project_root: Path) -> None:  # type: ignore[misc]
    """Build and start the supply-chain scanner container once per session.

    Yields after the containers are running so all tests in the session
    benefit from warm containers.  Tears down containers (including volumes
    and orphan services) on session exit.

    The build step is run with --quiet to suppress verbose layer output in CI
    while still surfacing build errors.  Timeout is 300 s for the build phase
    (image pulls can be slow) and 60 s for up/down.
    """
    compose_path = str(project_root / _COMPOSE_FILE)

    subprocess.run(
        ["docker", "compose", "-f", compose_path, "build", "--quiet"],
        check=True,
        cwd=str(project_root),
        timeout=300,
    )
    subprocess.run(
        ["docker", "compose", "-f", compose_path, "up", "--detach"],
        check=True,
        cwd=str(project_root),
        timeout=60,
    )

    yield

    subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            compose_path,
            "down",
            "--volumes",
            "--remove-orphans",
        ],
        cwd=str(project_root),
        timeout=60,
    )


# ---------------------------------------------------------------------------
# Per-test fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def cli_run(project_root: Path):  # type: ignore[return]
    """Return a callable that invokes `uv run jerry tool exec` via subprocess.

    The callable signature:
        _run(*args, env_override=None) -> tuple[int, str, str]

    Returns (exit_code, stdout, stderr).  All invocations run with cwd set
    to the project root so the CLI can find pyproject.toml and tool_families.yaml.

    Args are passed directly after `jerry tool exec`; callers must not shell-
    quote arguments — subprocess handles quoting via the list form (CWE-78).

    Argparse quirk: `tool_command` is a required positional argument on
    `jerry tool exec`.  The CLI handler for --list-families, --list-tools, and
    --init-engagement all return early before resolving the tool command, so
    argparse is the only thing that blocks them from running without a positional.
    This helper automatically appends a dummy placeholder ("_") when a
    management-only flag is detected and no real tool_command is present,
    so tests can call `cli_run("--list-families")` without injecting a spurious
    second positional in every test body.

    Management flag detection: any invocation that has --list-families,
    --list-tools, or --init-engagement as the first arg (and no other positional
    that looks like a tool command) receives the dummy.
    """

    # Management flags that cause the CLI handler to return before consuming
    # tool_command.  When an invocation uses ONLY these flags (plus their option
    # values), append a dummy positional so argparse does not reject the call.
    #
    # _MANAGEMENT_FLAGS_NO_VALUE: standalone boolean flags (no following value)
    _MANAGEMENT_FLAGS_NO_VALUE = frozenset({"--list-families"})
    # _MANAGEMENT_FLAGS_WITH_VALUE: flags that consume one following token as
    # their option value.  The value is NOT the tool_command positional.
    _MANAGEMENT_FLAGS_WITH_VALUE = frozenset({"--init-engagement", "--list-tools"})

    # All known jerry tool exec option flags that consume one following value.
    # Used to skip over option-value pairs when scanning for the tool_command.
    _JERRY_FLAGS_WITH_VALUE = frozenset(
        {
            "--mode",
            "--family",
            "--engagement-id",
            "--evidence-dir",
            "--init-engagement",
            "--list-tools",
            "--zone",
        }
    )
    # Known boolean flags that do NOT consume a following value.
    _JERRY_FLAGS_BOOL = frozenset(
        {
            "--no-filter",
            "--health-check",
            "--list-families",
            "-h",
            "--help",
        }
    )

    def _needs_dummy(args_seq: tuple[str, ...]) -> bool:
        """Return True when management flag is present and no tool_command is.

        Scans the arg list using explicit knowledge of jerry's own option
        schema to distinguish jerry flags from tool positionals.  Only tokens
        that survive flag-stripping and are not option-values are considered
        potential tool_command positionals.
        """
        has_management = False
        skip_next = False
        positional_count = 0

        for token in args_seq:
            if skip_next:
                skip_next = False
                continue
            if token in _MANAGEMENT_FLAGS_NO_VALUE:
                has_management = True
            elif token in _MANAGEMENT_FLAGS_WITH_VALUE:
                has_management = True
                skip_next = True  # next token is the option-value, not tool_command
            elif token in _JERRY_FLAGS_WITH_VALUE:
                skip_next = True  # next token is the option-value, not tool_command
            elif token in _JERRY_FLAGS_BOOL:
                pass  # consume no value
            elif token.startswith("-"):
                # Unknown option; assume it takes one value (conservative)
                skip_next = True
            else:
                # Non-flag token after accounting for all known options:
                # this is either tool_command or a tool_arg.
                positional_count += 1

        return has_management and positional_count == 0

    def _run(*args: str, env_override: dict[str, str] | None = None) -> tuple[int, str, str]:
        env = os.environ.copy()
        if env_override:
            env.update(env_override)

        # Inject dummy positional when the invocation is management-only.
        #
        # Argparse enforces that tool_command is present even for management
        # flags (--list-families, --list-tools, --init-engagement) that cause
        # the CLI handler to return early before consuming the positional.
        #
        # The dummy "_" is PREPENDED (not appended) because --list-tools uses
        # nargs="?" and greedily consumes the next positional token as its
        # optional FAMILY value.  Prepending ensures "_" is parsed as
        # tool_command, not as the --list-tools family filter.
        effective_args = list(args)
        if _needs_dummy(args):
            effective_args = ["_"] + effective_args

        result = subprocess.run(
            ["uv", "run", "jerry", "tool", "exec", *effective_args],
            capture_output=True,
            text=True,
            cwd=str(project_root),
            env=env,
            timeout=60,
        )
        return result.returncode, result.stdout, result.stderr

    return _run


@pytest.fixture()
def engagement_cleanup(project_root: Path):  # type: ignore[return]
    """Collect engagement IDs created during a test and remove them after.

    Usage:
        def test_something(engagement_cleanup, cli_run):
            engagement_cleanup.append("E2E-TEST-001")
            cli_run("--init-engagement", "E2E-TEST-001")
            ...  # engagement dir is removed after the test returns

    The fixture yields a mutable list.  Append the engagement ID string to
    register it for cleanup.  Cleanup is best-effort: if the directory does
    not exist, no error is raised.
    """
    created: list[str] = []
    yield created
    for eng_id in created:
        eng_dir = project_root / "work" / "engagements" / eng_id
        if eng_dir.exists():
            shutil.rmtree(eng_dir, ignore_errors=True)
