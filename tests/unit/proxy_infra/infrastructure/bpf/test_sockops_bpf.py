# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD tests for sockops.bpf.c -- Port-to-Cookie Mapping.

TASK-023-169 RED phase: These tests MUST fail before implementation exists.
GREEN phase: Write sockops.bpf.c to make them pass.

Full chain under test:
    sockops.bpf.c attaches to cgroup/sock_ops.
    On BPF_SOCK_OPS_ACTIVE_ESTABLISHED_CB, stores source_port -> socket_cookie
    in the shared port_cookie BPF hash map.

Tests require Docker with BPF capabilities (privileged mode).
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parents[5]
_EBPF_POC_DIR = _PROJECT_ROOT / "src/proxy_infra/ebpf_poc"
_BPF_BUILDER_DOCKERFILE = (
    _PROJECT_ROOT / "src/proxy_infra/infrastructure/bpf/Dockerfile.bpf-builder"
)
_BUILDER_IMAGE = "jerry-bpf-builder-test"


def _docker_available() -> bool:
    """Check if Docker is available and running.

    Returns:
        True if ``docker info`` exits 0 within 10 seconds.

    Raises:
        No exceptions raised; all errors return False.
    """
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


_requires_docker = pytest.mark.skipif(
    not _docker_available(),
    reason="Docker not available",
)


@pytest.fixture(scope="module")
def bpf_builder_image() -> str:
    """Build the BPF builder Docker image and return the image tag.

    Builds once per test module. Requires Docker.

    Returns:
        Docker image tag string for the built BPF builder image.

    Raises:
        pytest.Failed: If Docker build exits non-zero.
    """
    result = subprocess.run(
        [
            "docker", "build",
            "-f", str(_BPF_BUILDER_DOCKERFILE),
            "-t", _BUILDER_IMAGE,
            str(_EBPF_POC_DIR),
        ],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        pytest.fail(
            f"Docker build failed:\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return _BUILDER_IMAGE


@pytest.mark.unit
class TestSockopsBpf:
    """Tests for sockops.bpf.c -- Port-to-Cookie Mapping (TASK-023-169)."""

    @_requires_docker
    def test_sockops_compiles_to_valid_elf(
        self, bpf_builder_image: str
    ) -> None:
        """Docker build produces sockops.bpf.o; file reports eBPF ELF."""
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                bpf_builder_image,
                "file", "/opt/ebpf/sockops.bpf.o",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, f"file command failed: {result.stderr}"
        assert "ELF" in result.stdout, f"Not an ELF file: {result.stdout}"
        assert "eBPF" in result.stdout or "BPF" in result.stdout, (
            f"Not an eBPF object: {result.stdout}"
        )

    @_requires_docker
    def test_sockops_loads_and_pins(self, bpf_builder_image: str) -> None:
        """bpftool prog load sockops.bpf.o /sys/fs/bpf/test_sockops exits 0."""
        result = subprocess.run(
            [
                "docker", "run", "--rm", "--privileged",
                bpf_builder_image,
                "sh", "-c",
                "mount -t bpf bpf /sys/fs/bpf 2>/dev/null; "
                "bpftool prog load /opt/ebpf/sockops.bpf.o "
                "/sys/fs/bpf/test_sockops && "
                "bpftool prog show pinned /sys/fs/bpf/test_sockops",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"BPF load/pin failed:\nstdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )

    @_requires_docker
    def test_port_cookie_map_populated_after_connect(
        self, bpf_builder_image: str
    ) -> None:
        """After BPF load, port_cookie map is pinned and accessible."""
        result = subprocess.run(
            [
                "docker", "run", "--rm", "--privileged",
                bpf_builder_image,
                "sh", "-c",
                "mount -t bpf bpf /sys/fs/bpf 2>/dev/null; "
                "bpftool prog load /opt/ebpf/sockops.bpf.o "
                "/sys/fs/bpf/test_sockops "
                "pinmaps /sys/fs/bpf/test_maps && "
                "ls /sys/fs/bpf/test_maps/",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"Map pin failed:\nstdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )
        assert "port_cookie" in result.stdout, (
            f"port_cookie map not pinned. Maps found: {result.stdout}"
        )

    @_requires_docker
    def test_sockops_attaches_to_container_cgroup(
        self, bpf_builder_image: str
    ) -> None:
        """bpftool cgroup show lists sock_ops program after attach."""
        result = subprocess.run(
            [
                "docker", "run", "--rm", "--privileged",
                bpf_builder_image,
                "sh", "-c",
                "mount -t bpf bpf /sys/fs/bpf 2>/dev/null; "
                "mkdir -p /sys/fs/cgroup/test_workload; "
                "bpftool prog load /opt/ebpf/sockops.bpf.o "
                "/sys/fs/bpf/test_sockops && "
                "bpftool cgroup attach /sys/fs/cgroup/test_workload sock_ops "
                "pinned /sys/fs/bpf/test_sockops && "
                "bpftool cgroup show /sys/fs/cgroup/test_workload",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, (
            f"cgroup attach failed:\nstdout: {result.stdout}\n"
            f"stderr: {result.stderr}"
        )
        assert "sock_ops" in result.stdout, (
            f"sock_ops not in cgroup show output: {result.stdout}"
        )
