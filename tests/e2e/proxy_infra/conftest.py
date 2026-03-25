# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Conftest for eBPF transparent SOCKS5 proxy E2E tests.

EN-023-001: eBPF cgroup/connect4 transparent proxy PoC.

Design constraints:
- No mocks. All assertions go through real docker compose exec calls.
- Docker with privileged container support is required (eBPF needs CAP_BPF).
- The ebpf_poc_stack fixture is session-scoped: one build + up per session,
  then down on exit.  Building the eBPF image requires clang/llvm/libbpf in
  the builder image, which takes ~90 s on first run.
- Tests are annotated @pytest.mark.e2e and @pytest.mark.ebpf.  They are
  expected to be RED on a machine without Docker or without kernel eBPF
  support -- that is the intended BDD Red phase.
- No shell=True anywhere (CWE-78 mitigation).

References:
    EN-023-001 eBPF PoC: src/proxy_infra/ebpf_poc/
    docker-compose.yml:  src/proxy_infra/ebpf_poc/docker-compose.yml
    entrypoint.sh:       src/proxy_infra/ebpf_poc/entrypoint.sh
    bridge.py:           src/proxy_infra/ebpf_poc/bridge.py
    connect4.bpf.c:      src/proxy_infra/ebpf_poc/connect4.bpf.c
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_EBPF_COMPOSE = str(_PROJECT_ROOT / "src/proxy_infra/ebpf_poc/docker-compose.yml")
_EBPF_CWD = str(_PROJECT_ROOT / "src/proxy_infra/ebpf_poc")

# Service names defined in docker-compose.yml
_SVC_EBPF_TEST = "ebpf-test"
_SVC_PROXY_NODE = "proxy-node"
_SVC_TEST_TARGET = "test-target"


def _docker_available() -> bool:
    """Return True when the Docker daemon is reachable."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _compose_build(*, cwd: str) -> None:
    """Build images for the eBPF PoC compose file.

    Timeout is 900 s: clang + libbpf compilation takes ~90 s on first run;
    CI caches layers, but a full cold build on a fresh runner needs margin.

    Args:
        cwd: Working directory for the docker compose command.
    """
    subprocess.run(
        ["docker", "compose", "-f", _EBPF_COMPOSE, "build"],
        check=True,
        cwd=cwd,
        timeout=900,
    )


def _compose_up(*, cwd: str) -> None:
    """Start the eBPF PoC stack in detached mode.

    Args:
        cwd: Working directory for the docker compose command.
    """
    subprocess.run(
        ["docker", "compose", "-f", _EBPF_COMPOSE, "up", "--detach"],
        check=True,
        cwd=cwd,
        timeout=120,
    )


def _compose_down(*, cwd: str) -> None:
    """Stop and remove the eBPF PoC stack.

    Best-effort: does not raise on failure so teardown always completes.

    Args:
        cwd: Working directory for the docker compose command.
    """
    subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            _EBPF_COMPOSE,
            "down",
            "--volumes",
            "--remove-orphans",
        ],
        cwd=cwd,
        timeout=60,
        # No check=True: best-effort teardown.
    )


def _wait_for_service(
    service: str,
    *,
    cwd: str,
    max_wait: int = 60,
) -> bool:
    """Poll a compose service until it shows as running.

    The ebpf-test container runs entrypoint.sh which compiles + loads the BPF
    program before the bridge starts listening.  We poll docker compose ps
    for "running" status and additionally wait for the bridge log line.

    Args:
        service: Compose service name.
        cwd: Working directory for the docker compose command.
        max_wait: Maximum seconds to poll.
    """
    for _ in range(max_wait):
        result = subprocess.run(
            ["docker", "compose", "-f", _EBPF_COMPOSE, "ps", service],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=10,
        )
        if "running" in result.stdout.lower():
            return True
        time.sleep(1)
    return False


def _wait_for_bridge_ready(*, cwd: str, max_wait: int = 90) -> bool:
    """Poll docker logs for the bridge ready marker.

    entrypoint.sh prints "[OK]   Bridge PID=" once the bridge is listening.
    We need this before running any tests that exercise the full chain.

    Args:
        cwd: Working directory for the docker compose command.
        max_wait: Maximum seconds to poll.
    """
    for _ in range(max_wait):
        result = subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                _EBPF_COMPOSE,
                "logs",
                "--no-log-prefix",
                _SVC_EBPF_TEST,
            ],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=10,
        )
        if "Bridge PID=" in result.stdout or "bridge] Listening on" in result.stdout:
            return True
        time.sleep(1)
    return False


# ---------------------------------------------------------------------------
# pytest hooks
# ---------------------------------------------------------------------------


def pytest_configure(config: pytest.Config) -> None:
    """Register eBPF-specific markers so pytest does not warn about unknowns."""
    config.addinivalue_line(
        "markers",
        "ebpf: eBPF transparent SOCKS5 proxy E2E tests (requires privileged Docker + kernel BPF support)",
    )
    config.addinivalue_line(
        "markers",
        "e2e: end-to-end tests requiring Docker and real CLI invocation",
    )


# ---------------------------------------------------------------------------
# Session-scoped Docker guard
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def docker_guard() -> None:
    """Skip the entire session when Docker is unavailable.

    Propagates to all tests in this package automatically.  On macOS
    without Docker Desktop or a CI runner without a Docker socket the
    entire test module is skipped rather than failing.
    """
    if not _docker_available():
        pytest.skip(
            "Docker daemon not available -- skipping all eBPF proxy E2E tests"
        )


# ---------------------------------------------------------------------------
# Project root fixture
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the absolute project root located by pyproject.toml.

    Returns:
        Absolute path to the repository root containing pyproject.toml.
    """
    candidate = Path(__file__).resolve()
    while candidate != candidate.parent:
        if (candidate / "pyproject.toml").exists():
            return candidate
        candidate = candidate.parent
    pytest.fail("Could not locate pyproject.toml -- cannot determine project root")


# ---------------------------------------------------------------------------
# Primary stack fixture
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def ebpf_poc_stack() -> str:  # type: ignore[misc]
    """Build and start the eBPF PoC Docker Compose stack once per session.

    Three-service topology:
        ebpf-test  (172.30.0.2) -- BPF + bridge -- privileged container
        proxy-node (172.30.0.5) -- microsocks SOCKS5
        test-target(172.30.0.10) -- nginx

    Waits for:
        1. All three services to show "running" in docker compose ps.
        2. The bridge ready log line from entrypoint.sh.

    Yields:
        The absolute path to docker-compose.yml for use in _compose_exec calls.

    Tears down all containers, volumes, and orphan services on session exit.
    """
    cwd = _EBPF_CWD
    _compose_build(cwd=cwd)
    _compose_up(cwd=cwd)

    for svc in (_SVC_TEST_TARGET, _SVC_PROXY_NODE, _SVC_EBPF_TEST):
        _wait_for_service(svc, cwd=cwd)

    _wait_for_bridge_ready(cwd=cwd)

    yield _EBPF_COMPOSE

    _compose_down(cwd=cwd)
