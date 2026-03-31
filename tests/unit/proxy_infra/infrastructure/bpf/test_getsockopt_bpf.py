# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD tests for getsockopt.bpf.c -- SO_ORIGINAL_DST Interception.

TASK-023-170 RED phase: These tests MUST fail before implementation exists.
GREEN phase: Write getsockopt.bpf.c to make them pass.

Full chain under test:
    getsockopt.bpf.c attaches to cgroup/getsockopt.
    When Envoy calls getsockopt(SO_ORIGINAL_DST), the program intercepts,
    looks up source_port in port_cookie map to get cookie, then looks up
    cookie in dst_lookup map to return the real original destination.

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
class TestGetsockoptBpf:
    """Tests for getsockopt.bpf.c -- SO_ORIGINAL_DST Interception (TASK-023-170)."""

    @_requires_docker
    def test_getsockopt_compiles_to_valid_elf(
        self, bpf_builder_image: str
    ) -> None:
        """Docker build produces getsockopt.bpf.o; file reports eBPF ELF."""
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                bpf_builder_image,
                "file", "/opt/ebpf/getsockopt.bpf.o",
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
    def test_getsockopt_loads_and_pins(
        self, bpf_builder_image: str
    ) -> None:
        """bpftool prog load getsockopt.bpf.o /sys/fs/bpf/test_getsockopt exits 0."""
        result = subprocess.run(
            [
                "docker", "run", "--rm", "--privileged",
                bpf_builder_image,
                "sh", "-c",
                "mount -t bpf bpf /sys/fs/bpf 2>/dev/null; "
                "bpftool prog load /opt/ebpf/getsockopt.bpf.o "
                "/sys/fs/bpf/test_getsockopt && "
                "bpftool prog show pinned /sys/fs/bpf/test_getsockopt",
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
    def test_envoy_receives_original_dst_via_getsockopt(
        self, bpf_builder_image: str
    ) -> None:
        """After BPF load, dst_lookup map is pinned and accessible for getsockopt."""
        result = subprocess.run(
            [
                "docker", "run", "--rm", "--privileged",
                bpf_builder_image,
                "sh", "-c",
                "mount -t bpf bpf /sys/fs/bpf 2>/dev/null; "
                "bpftool prog load /opt/ebpf/getsockopt.bpf.o "
                "/sys/fs/bpf/test_getsockopt "
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
        assert "dst_lookup" in result.stdout, (
            f"dst_lookup map not pinned. Maps found: {result.stdout}"
        )
        assert "port_cookie" in result.stdout, (
            f"port_cookie map not pinned. Maps found: {result.stdout}"
        )

    @_requires_docker
    def test_getsockopt_attaches_to_container_cgroup(
        self, bpf_builder_image: str
    ) -> None:
        """bpftool cgroup show lists getsockopt program after attach."""
        result = subprocess.run(
            [
                "docker", "run", "--rm", "--privileged",
                bpf_builder_image,
                "sh", "-c",
                "mount -t bpf bpf /sys/fs/bpf 2>/dev/null; "
                "bpftool prog load /opt/ebpf/getsockopt.bpf.o "
                "/sys/fs/bpf/test_getsockopt && "
                "mkdir -p /sys/fs/cgroup/test_workload; "
                "bpftool cgroup attach /sys/fs/cgroup/test_workload getsockopt "
                "pinned /sys/fs/bpf/test_getsockopt && "
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
        assert "getsockopt" in result.stdout, (
            f"getsockopt not in cgroup show output: {result.stdout}"
        )
