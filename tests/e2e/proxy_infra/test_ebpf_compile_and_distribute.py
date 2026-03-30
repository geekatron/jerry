# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""BDD E2E tests for eBPF BPF object compilation and distribution.

Feature: eBPF BPF Object Compilation and Distribution
    EN-023-008 TASK-023-161: The BPF cgroup/connect4 program must be compiled
    inside Docker against LinuxKit-compatible headers and distributed to all
    Zone 2/3 tool containers as a read-only volume.

    Verifies:
        - BPF object compiles to valid ELF in Docker build
        - Compiled artifact available at /opt/ebpf/connect4.bpf.o in 4 clusters
        - bpftool is installed and executable in all tool containers

    Test pyramid (H-20):
        60% happy path  -- compile, distribute to 4 clusters (5 tests)
        30% edge        -- bpftool availability (2 tests)
        10% arch        -- ELF format verification (1 test)

BDD RED phase (H-20):
    These tests FAIL initially because no production Dockerfile.bpf-builder
    exists and no compose cluster has the bpf-objects volume. This is the
    correct initial state — write tests first, then implement.

No mocks. Real Docker builds. Real compose containers.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Production BPF builder Dockerfile (does not exist yet — RED phase)
_BPF_BUILDER_DOCKERFILE = str(
    _PROJECT_ROOT / "src/proxy_infra/infrastructure/bpf/Dockerfile.bpf-builder"
)
_BPF_BUILDER_CONTEXT = str(_PROJECT_ROOT / "src/proxy_infra/ebpf_poc")

# Zone 2/3 compose clusters and their primary tool service names
_ZONE23_CLUSTERS: list[tuple[str, str, str]] = [
    # (compose_file_relative, compose_cwd, service_name)
    (
        "skills/rainbow-cloud/tests/docker/docker-compose.yml",
        "skills/rainbow-cloud/tests/docker",
        "cloud-auditor",
    ),
    (
        "skills/rainbow-recon/tests/docker/docker-compose.yml",
        "skills/rainbow-recon/tests/docker",
        "recon-pipeline",
    ),
    (
        "skills/rainbow-exploit/tests/docker/docker-compose.yml",
        "skills/rainbow-exploit/tests/docker",
        "exploit-ops",
    ),
    (
        "skills/rainbow-runtime/tests/docker/docker-compose.yml",
        "skills/rainbow-runtime/tests/docker",
        "frida",
    ),
]

# Expected path inside containers
_BPF_OBJECT_PATH = "/opt/ebpf/connect4.bpf.o"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _docker_compose_exec(
    compose_file: str,
    cwd: str,
    service: str,
    cmd: list[str],
    *,
    timeout: int = 30,
) -> subprocess.CompletedProcess[str]:
    """Run a command inside a compose service container.

    Args:
        compose_file: Path to docker-compose.yml relative to project root.
        cwd: Working directory for docker compose (relative to project root).
        service: Docker Compose service name.
        cmd: Command to run inside the container.
        timeout: Command timeout in seconds.

    Returns:
        CompletedProcess with stdout/stderr.
    """
    full_compose = str(_PROJECT_ROOT / compose_file)
    full_cwd = str(_PROJECT_ROOT / cwd)
    return subprocess.run(
        ["docker", "compose", "-f", full_compose, "exec", "-T", service, *cmd],
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=full_cwd,
    )


# ---------------------------------------------------------------------------
# Tests — RED phase (H-20: all must FAIL initially)
# ---------------------------------------------------------------------------


@pytest.mark.e2e
class TestBpfObjectCompilesInDocker:
    """Verify the BPF object compiles inside Docker to a valid ELF."""

    def test_bpf_object_compiles_in_docker(self) -> None:
        """Given the production Dockerfile.bpf-builder, docker build succeeds
        and the output image contains a valid eBPF ELF at /opt/ebpf/connect4.bpf.o.

        RED: Fails because Dockerfile.bpf-builder does not exist yet.
        """
        result = subprocess.run(
            [
                "docker",
                "build",
                "-f",
                _BPF_BUILDER_DOCKERFILE,
                "-t",
                "bpf-builder:test",
                _BPF_BUILDER_CONTEXT,
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )
        assert result.returncode == 0, (
            f"Docker build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )

        # Verify the compiled artifact exists and is a valid eBPF ELF
        check = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "bpf-builder:test",
                "file",
                _BPF_OBJECT_PATH,
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert check.returncode == 0, f"file command failed: {check.stderr}"
        assert "ELF 64-bit LSB relocatable, eBPF" in check.stdout, (
            f"Expected eBPF ELF, got: {check.stdout}"
        )


@pytest.mark.e2e
class TestBpfObjectDistributed:
    """Verify the compiled BPF object is available in all Zone 2/3 tool containers."""

    @pytest.mark.parametrize(
        "compose_file,compose_cwd,service",
        _ZONE23_CLUSTERS,
        ids=["cloud", "recon", "exploit", "runtime"],
    )
    def test_bpf_object_available_in_tool_container(
        self,
        compose_file: str,
        compose_cwd: str,
        service: str,
    ) -> None:
        """Given a running Zone 2/3 compose cluster, the tool container has
        the compiled BPF object at /opt/ebpf/connect4.bpf.o.

        RED: Fails because compose clusters have no bpf-objects volume.
        """
        result = _docker_compose_exec(
            compose_file,
            compose_cwd,
            service,
            ["ls", "-la", _BPF_OBJECT_PATH],
        )
        assert result.returncode == 0, (
            f"BPF object not found in {service}:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )


@pytest.mark.e2e
class TestBpftoolAvailable:
    """Verify bpftool is installed and executable in all Zone 2/3 tool containers."""

    @pytest.mark.parametrize(
        "compose_file,compose_cwd,service",
        _ZONE23_CLUSTERS,
        ids=["cloud", "recon", "exploit", "runtime"],
    )
    def test_bpftool_available_in_tool_container(
        self,
        compose_file: str,
        compose_cwd: str,
        service: str,
    ) -> None:
        """Given a running Zone 2/3 compose cluster, bpftool is installed and
        reports its version.

        RED: Fails because bpftool is not installed in tool container images.
        """
        result = _docker_compose_exec(
            compose_file,
            compose_cwd,
            service,
            ["bpftool", "version"],
        )
        assert result.returncode == 0, (
            f"bpftool not available in {service}:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
        assert "bpftool" in result.stdout.lower(), f"Unexpected bpftool output: {result.stdout}"
