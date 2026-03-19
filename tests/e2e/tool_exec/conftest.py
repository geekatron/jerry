# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""E2E conftest for jerry tool exec tests.

TASK-029: Docker availability guard, project_root fixture, cli_run fixture.
TASK-030: Docker Compose session-scoped build+up+teardown fixture.
TASK-047: Extended to cover all 6 compose clusters with explicit opt-in fixtures.

Design constraints:
- No mocks. All CLI calls go through the real `uv run jerry` subprocess.
- Docker is required. Tests skip at session scope when Docker is unavailable.
- Cluster fixtures are NOT autouse — tests must request the cluster they need.
  This prevents spinning up all 6 clusters when running a single test file.
- Engagement directories are created under the real project root and cleaned up
  after each test that creates them.

Security notes:
- All engagement IDs are prefixed with E2E-TEST- to make cleanup deterministic.
- Subprocess calls use timeout=60 to prevent test suite hangs.
- No shell=True anywhere (CWE-78 mitigation).

Cluster-to-compose mapping:
    supply_chain_cluster  -> skills/rainbow-supply-chain/tests/docker/docker-compose.yml
    blue_team_cluster     -> skills/blue-team/tests/docker/docker-compose.yml
    cloud_cluster         -> skills/rainbow-cloud/tests/docker/docker-compose.yml
    recon_cluster         -> skills/rainbow-recon/tests/docker/docker-compose.yml
    exploit_cluster       -> skills/rainbow-exploit/tests/docker/docker-compose.yml
    runtime_cluster       -> skills/rainbow-runtime/tests/docker/docker-compose.yml

References:
    - TASK-029: conftest.py base structure
    - TASK-030: Docker Compose session fixture
    - TASK-047: All-cluster conftest extension
    - ADR-PROJ023-001: Behavioral Contract
"""

from __future__ import annotations

import os
import shutil
import subprocess
import time
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


def _compose_build(compose_path: str, *, cwd: str) -> None:
    """Build images for a compose file.

    Runs docker compose build --quiet to suppress verbose layer output while
    still surfacing build errors. Timeout is 600 s to allow for image pulls.

    Args:
        compose_path: Absolute path to the docker-compose.yml file.
        cwd: Working directory for the docker compose command.
    """
    subprocess.run(
        ["docker", "compose", "-f", compose_path, "build", "--quiet"],
        check=True,
        cwd=cwd,
        timeout=600,
    )


def _compose_up(compose_path: str, *, cwd: str) -> None:
    """Start containers for a compose file in detached mode.

    Args:
        compose_path: Absolute path to the docker-compose.yml file.
        cwd: Working directory for the docker compose command.
    """
    subprocess.run(
        ["docker", "compose", "-f", compose_path, "up", "--detach"],
        check=True,
        cwd=cwd,
        timeout=120,
    )


def _compose_down(compose_path: str, *, cwd: str) -> None:
    """Stop and remove containers, volumes, and orphan services.

    Best-effort: does not raise on failure so teardown always runs to
    completion even if containers were already removed.

    Args:
        compose_path: Absolute path to the docker-compose.yml file.
        cwd: Working directory for the docker compose command.
    """
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
        cwd=cwd,
        timeout=60,
        # No check=True: best-effort teardown should not fail the session.
    )


def _wait_for_health(
    compose_path: str,
    service: str,
    *,
    cwd: str,
    max_wait: int = 30,
) -> bool:
    """Poll a compose service until it is healthy or running.

    Uses ``docker compose ps --format json`` to inspect container status.
    Returns True when the service reaches a healthy or running state.
    Returns False when max_wait seconds elapse without a healthy state.

    Args:
        compose_path: Absolute path to the docker-compose.yml file.
        service: Name of the compose service to wait for.
        cwd: Working directory for the docker compose command.
        max_wait: Maximum number of seconds to poll.
    """
    for _ in range(max_wait):
        result = subprocess.run(
            ["docker", "compose", "-f", compose_path, "ps", service],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=10,
        )
        output = result.stdout.lower()
        # Docker compose ps reports "(healthy)" or "running" in the status column.
        if "healthy" in output or "running" in output:
            return True
        time.sleep(1)
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
# Session-scoped guards and root
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Cluster fixtures — NOT autouse. Tests must request the cluster they need.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def supply_chain_cluster(project_root: Path) -> str:  # type: ignore[misc]
    """Build and start the supply-chain compose cluster once per session.

    Yields the compose file path so tests can reference it for docker exec
    operations (e.g., TestEnvoyProxy tests that exec into scanner-net).

    Tears down containers, volumes, and orphan services on session exit.
    """
    compose = str(project_root / "skills/rainbow-supply-chain/tests/docker/docker-compose.yml")
    cwd = str(project_root)
    _compose_build(compose, cwd=cwd)
    _compose_up(compose, cwd=cwd)
    _wait_for_health(compose, "scanner", cwd=cwd)

    yield compose

    _compose_down(compose, cwd=cwd)


@pytest.fixture(scope="session")
def blue_team_cluster(project_root: Path) -> str:  # type: ignore[misc]
    """Build and start the blue-team compose cluster once per session.

    Yields the compose file path.
    """
    compose = str(project_root / "skills/blue-team/tests/docker/docker-compose.yml")
    cwd = str(project_root)
    _compose_build(compose, cwd=cwd)
    _compose_up(compose, cwd=cwd)
    _wait_for_health(compose, "detection", cwd=cwd)

    yield compose

    _compose_down(compose, cwd=cwd)


@pytest.fixture(scope="session")
def cloud_cluster(project_root: Path) -> str:  # type: ignore[misc]
    """Build and start the rainbow-cloud compose cluster once per session.

    Yields the compose file path.
    """
    compose = str(project_root / "skills/rainbow-cloud/tests/docker/docker-compose.yml")
    cwd = str(project_root)
    _compose_build(compose, cwd=cwd)
    _compose_up(compose, cwd=cwd)
    _wait_for_health(compose, "cloud-auditor", cwd=cwd)

    yield compose

    _compose_down(compose, cwd=cwd)


@pytest.fixture(scope="session")
def recon_cluster(project_root: Path) -> str:  # type: ignore[misc]
    """Build and start the rainbow-recon compose cluster once per session.

    Yields the compose file path so tests can reference it for docker exec
    operations (e.g., TestEnvoyFailClosed which stops/restarts envoy-z2).
    """
    compose = str(project_root / "skills/rainbow-recon/tests/docker/docker-compose.yml")
    cwd = str(project_root)
    _compose_build(compose, cwd=cwd)
    _compose_up(compose, cwd=cwd)
    _wait_for_health(compose, "recon-pipeline", cwd=cwd)

    yield compose

    _compose_down(compose, cwd=cwd)


@pytest.fixture(scope="session")
def exploit_cluster(project_root: Path) -> str:  # type: ignore[misc]
    """Build and start the rainbow-exploit compose cluster once per session.

    Yields the compose file path so tests can reference exploit container paths.
    """
    compose = str(project_root / "skills/rainbow-exploit/tests/docker/docker-compose.yml")
    cwd = str(project_root)
    _compose_build(compose, cwd=cwd)
    _compose_up(compose, cwd=cwd)
    _wait_for_health(compose, "exploit-ops", cwd=cwd)

    yield compose

    _compose_down(compose, cwd=cwd)


@pytest.fixture(scope="session")
def runtime_cluster(project_root: Path) -> str:  # type: ignore[misc]
    """Build and start the rainbow-runtime compose cluster once per session.

    Yields the compose file path.
    """
    compose = str(project_root / "skills/rainbow-runtime/tests/docker/docker-compose.yml")
    cwd = str(project_root)
    _compose_build(compose, cwd=cwd)
    _compose_up(compose, cwd=cwd)
    _wait_for_health(compose, "mitmproxy", cwd=cwd)

    yield compose

    _compose_down(compose, cwd=cwd)


# ---------------------------------------------------------------------------
# Session-scoped engagement init
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def engagement_init(project_root: Path):  # type: ignore[misc]
    """Initialize E2E-TEST-001 engagement once per session.

    Uses subprocess directly (not cli_run) because this is session-scoped
    and cli_run is function-scoped. ScopeMismatch fix.

    Creates the engagement directory that Zone 2/3 tools require.
    Cleans up E2E-TEST-* engagement dirs on session exit (F-003 mitigation).
    """
    eng_id = "E2E-TEST-001"
    eng_dir = project_root / "work" / "engagements" / eng_id

    # F-003: Clean stale engagement dirs from prior crashed sessions
    engagements_root = project_root / "work" / "engagements"
    if engagements_root.exists():
        for stale in engagements_root.glob("E2E-TEST-*"):
            shutil.rmtree(stale, ignore_errors=True)

    subprocess.run(
        ["uv", "run", "jerry", "tool", "exec", "_", "--init-engagement", eng_id],
        capture_output=True,
        cwd=str(project_root),
        timeout=30,
    )

    yield

    if eng_dir.exists():
        shutil.rmtree(eng_dir, ignore_errors=True)


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
