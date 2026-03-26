# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BPF program lifecycle manager for eBPF transparent SOCKS routing.

Manages the full lifecycle of a BPF cgroup/connect4 program:
  - Load compiled BPF object from bpffs
  - Detach stale root cgroup BPF before per-container attachment (EN-023-001 F-2)
  - Attach to container-specific cgroup (NOT root cgroup)
  - Create jerry-intercept cgroup as CHILD of container cgroup (EN-023-001 F-8)
  - Populate bypass_ips map with proxy pool IPs and Envoy IP (EN-023-001 F-4, OPSEC-F3)
  - Pin program to bpffs to prevent fail-open on process exit (OPSEC-F5 CRITICAL)
  - Verify pin before declaring ready
  - Detach and clean up on teardown

Design constraints:
  H-10:  One public class per file.
  H-11:  All public methods have type annotations.
  H-07:  Infrastructure layer — subprocess and pathlib use is permitted here.
  OPSEC-F5: BPF program MUST be pinned; unpinned programs cause fail-open (real IP leak).
  F-8:   jerry-intercept cgroup MUST be a CHILD of the container cgroup, not a sibling.

References:
  EN-023-001 PoC  -- src/proxy_infra/ebpf_poc/
  TASK-023-017    -- BPF C program requirements
  TASK-023-018    -- CLM attach requirements
"""

from __future__ import annotations

import logging
import shlex
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

# Canonical bpffs mount point
_BPFFS_ROOT = Path("/sys/fs/bpf")

# Default path under bpffs where the production program is pinned
_DEFAULT_PIN_PATH = _BPFFS_ROOT / "rainbow_connect4"

# Default path where bpffs maps are pinned (mirrors PoC poc_maps pattern)
_DEFAULT_MAP_DIR = _BPFFS_ROOT / "rainbow_maps"

# Cgroup v2 docker hierarchy root
_CGROUP_DOCKER_ROOT = Path("/sys/fs/cgroup/docker")

# Name of the child intercept cgroup under the container cgroup (F-8)
_INTERCEPT_CGROUP_NAME = "jerry-intercept"


class BpfManager:
    """Manages BPF cgroup/connect4 program lifecycle for transparent SOCKS routing.

    All bpftool interactions are performed via subprocess. Tests should mock
    subprocess.run to avoid requiring kernel BPF capabilities.

    Lifecycle:
        1. load_and_attach(container_id)  -- load, detach stale root, attach to container
        2. populate_bypass(proxy_ips, envoy_ip)  -- fill bypass_ips map
        3. is_ready()  -- verify pin + bridge listening
        4. detach_and_cleanup()  -- unpin, detach from cgroup

    Args:
        bpf_object_path: Path to the compiled .bpf.o ELF file.
        bridge_port: TCP port the transparent bridge listens on (default 12345).
        pin_path: bpffs path for pinning the program (default /sys/fs/bpf/rainbow_connect4).
        map_dir: bpffs directory for pinning maps (default /sys/fs/bpf/rainbow_maps).
    """

    def __init__(
        self,
        bpf_object_path: str,
        bridge_port: int = 12345,
        pin_path: str | None = None,
        map_dir: str | None = None,
    ) -> None:
        """Initialise the BPF manager.

        Args:
            bpf_object_path: Path to compiled BPF object file (.bpf.o).
            bridge_port: Listening port of the transparent SOCKS bridge.
            pin_path: Override bpffs pin path; defaults to /sys/fs/bpf/rainbow_connect4.
            map_dir: Override bpffs map directory; defaults to /sys/fs/bpf/rainbow_maps.
        """
        self._bpf_object_path = Path(bpf_object_path)
        self._bridge_port = bridge_port
        self._pin_path = Path(pin_path) if pin_path else _DEFAULT_PIN_PATH
        self._map_dir = Path(map_dir) if map_dir else _DEFAULT_MAP_DIR
        self._attached_cgroup: str | None = None

    # ------------------------------------------------------------------
    # Public lifecycle API
    # ------------------------------------------------------------------

    def load_and_attach(self, container_id: str) -> None:
        """Load the BPF program, detach any stale root cgroup BPF, then attach to container.

        Steps:
          1. Load BPF object file and pin program + maps to bpffs (OPSEC-F5).
          2. Detach any stale BPF from root cgroup (EN-023-001 F-2 — prevents blocking).
          3. Find container cgroup path via hostname detection pattern (EN-023-001 F-3).
          4. Create jerry-intercept as CHILD of container cgroup (EN-023-001 F-8).
          5. Attach the pinned BPF program to the container cgroup.

        Args:
            container_id: Docker container ID (short or full). Used to locate cgroup.

        Raises:
            RuntimeError: If BPF load, pin, or attachment fails.
        """
        logger.info("Loading BPF object from %s", self._bpf_object_path)
        self._load_and_pin()

        logger.info("Detaching stale root cgroup BPF (F-2 mitigation)")
        self._detach_root_cgroup()

        container_cgroup = self.get_container_cgroup(container_id)
        logger.info("Container cgroup resolved: %s", container_cgroup)

        intercept_cgroup = self.create_intercept_cgroup(container_cgroup)
        logger.info("Intercept child cgroup created: %s", intercept_cgroup)

        logger.info("Attaching BPF to container cgroup %s", container_cgroup)
        self._attach_to_cgroup(container_cgroup)
        self._attached_cgroup = container_cgroup

    def populate_bypass(self, proxy_ips: list[str], envoy_ip: str) -> None:
        """Populate the bypass_ips BPF map to prevent redirect loops.

        Must be called AFTER load_and_attach so the pinned map exists.

        Adds:
          - All proxy pool IPs (bridge connects directly to these — EN-023-001 F-4)
          - Envoy container IP (HTTP_PROXY traffic must not be BPF-intercepted — OPSEC-F3)

        Args:
            proxy_ips: List of IPv4 addresses for all SOCKS5 proxy pool nodes.
            envoy_ip: IPv4 address of the local Envoy forward proxy container.

        Raises:
            RuntimeError: If any map update fails.
        """
        all_ips = list(proxy_ips) + [envoy_ip]
        for ip in all_ips:
            logger.info("Adding %s to bypass_ips BPF map", ip)
            self._map_update_bypass(ip)

    def detach_and_cleanup(self) -> None:
        """Detach the BPF program from the cgroup and unpin from bpffs.

        Safe to call even if attach was never completed. Logs warnings for
        any cleanup steps that fail rather than raising.
        """
        if self._attached_cgroup:
            logger.info("Detaching BPF from cgroup %s", self._attached_cgroup)
            self._detach_from_cgroup(self._attached_cgroup)
            self._attached_cgroup = None
        else:
            logger.debug("No attached cgroup recorded; skipping detach")

        logger.info("Unpinning BPF program from %s", self._pin_path)
        self._unpin()

    def get_container_cgroup(self, container_id: str) -> str:
        """Locate container cgroup via hostname-to-cgroup pattern (EN-023-001 F-3).

        Docker sets the container hostname to the short container ID. The cgroup
        is at /sys/fs/cgroup/docker/{full-container-id}. This method uses the
        provided container_id to locate the cgroup directory by prefix match.

        Args:
            container_id: Short or full Docker container ID.

        Returns:
            Absolute path string to the container's cgroup directory.

        Raises:
            RuntimeError: If the cgroup directory cannot be found.
        """
        result = self._run(
            ["find", str(_CGROUP_DOCKER_ROOT), "-maxdepth", "1",
             "-name", f"{container_id}*", "-type", "d"],
            check=False,
        )
        paths = [p.strip() for p in result.stdout.splitlines() if p.strip()]
        if not paths:
            raise RuntimeError(
                f"Container cgroup not found for '{container_id}' "
                f"under {_CGROUP_DOCKER_ROOT}"
            )
        return paths[0]

    def create_intercept_cgroup(self, container_cgroup: str) -> str:
        """Create jerry-intercept as a CHILD of the container cgroup (EN-023-001 F-8).

        BPF programs on a parent cgroup apply to all child cgroups. A sibling cgroup
        does NOT inherit the parent's BPF programs, so processes moved to a sibling
        would escape BPF coverage entirely. This method ensures the intercept cgroup
        is a child, preserving BPF inheritance.

        Args:
            container_cgroup: Absolute path to the container's cgroup directory.

        Returns:
            Absolute path string to the newly created jerry-intercept cgroup.

        Raises:
            RuntimeError: If the child cgroup cannot be created.
        """
        intercept_path = Path(container_cgroup) / _INTERCEPT_CGROUP_NAME
        self._run(["mkdir", "-p", str(intercept_path)], check=True)
        logger.info("Created intercept child cgroup at %s", intercept_path)
        return str(intercept_path)

    def is_ready(self) -> bool:
        """Check that the BPF program is pinned and the bridge is listening.

        Verifies:
          1. Pin path exists on bpffs (OPSEC-F5 readiness gate).
          2. Bridge port is in LISTEN state (ss -tlnp check).

        Returns:
            True if both the program pin and bridge are confirmed ready.
        """
        if not self._is_pinned():
            logger.warning("BPF program pin not found at %s", self._pin_path)
            return False
        if not self._is_bridge_listening():
            logger.warning("Bridge not listening on port %d", self._bridge_port)
            return False
        return True

    # ------------------------------------------------------------------
    # Private helpers — each wraps a single bpftool/system command
    # ------------------------------------------------------------------

    def _load_and_pin(self) -> None:
        """Load BPF object and pin program + maps to bpffs.

        Raises:
            RuntimeError: If bpftool prog load fails.
        """
        self._run([
            "bpftool", "prog", "load",
            str(self._bpf_object_path),
            str(self._pin_path),
            "pinmaps", str(self._map_dir),
        ], check=True)
        logger.info("BPF program pinned at %s", self._pin_path)

    def _detach_root_cgroup(self) -> None:
        """Attempt to detach stale BPF from root cgroup (EN-023-001 F-2).

        Non-fatal: root cgroup may already be clean. Logs warnings on failure.
        """
        result = self._run([
            "bpftool", "cgroup", "detach",
            "/sys/fs/cgroup", "connect4",
            "pinned", str(self._pin_path),
        ], check=False)
        if result.returncode != 0:
            logger.debug(
                "Root cgroup detach returned non-zero (may be clean): %s",
                result.stderr.strip(),
            )

    def _attach_to_cgroup(self, cgroup_path: str) -> None:
        """Attach the pinned BPF program to the specified cgroup path.

        Args:
            cgroup_path: Absolute path to the target cgroup directory.

        Raises:
            RuntimeError: If bpftool cgroup attach fails.
        """
        self._run([
            "bpftool", "cgroup", "attach",
            cgroup_path, "connect4",
            "pinned", str(self._pin_path),
        ], check=True)

    def _detach_from_cgroup(self, cgroup_path: str) -> None:
        """Detach BPF program from the specified cgroup. Non-fatal on error.

        Args:
            cgroup_path: Absolute path to the cgroup to detach from.
        """
        result = self._run([
            "bpftool", "cgroup", "detach",
            cgroup_path, "connect4",
            "pinned", str(self._pin_path),
        ], check=False)
        if result.returncode != 0:
            logger.warning(
                "Detach from %s returned non-zero: %s",
                cgroup_path, result.stderr.strip(),
            )

    def _unpin(self) -> None:
        """Remove the program pin from bpffs. Non-fatal on error."""
        result = self._run(["unlink", str(self._pin_path)], check=False)
        if result.returncode != 0:
            logger.warning("Unpin of %s returned non-zero: %s",
                           self._pin_path, result.stderr.strip())

    def _map_update_bypass(self, ip: str) -> None:
        """Add an IPv4 address to the bypass_ips BPF hash map.

        Converts the dotted-decimal IP to 4 hex bytes and uses bpftool map update.

        Args:
            ip: IPv4 address string to add to the bypass set.

        Raises:
            RuntimeError: If bpftool map update fails.
            ValueError: If the IP address format is invalid.
        """
        import socket as _socket
        try:
            ip_bytes = _socket.inet_aton(ip)
        except OSError as exc:
            raise ValueError(f"Invalid IPv4 address for bypass map: {ip!r}") from exc

        hex_key = " ".join(f"0x{b:02x}" for b in ip_bytes)
        map_pinned = str(self._map_dir / "bypass_ips")

        # bpftool map update pinned <path> key hex <b0> <b1> <b2> <b3> value hex 0x01
        cmd = (
            ["bpftool", "map", "update", "pinned", map_pinned, "key", "hex"]
            + hex_key.split()
            + ["value", "hex", "0x01"]
        )
        self._run(cmd, check=True)

    def _is_pinned(self) -> bool:
        """Return True if the program pin path exists on bpffs.

        Returns:
            True if bpftool prog show succeeds for the pinned path.
        """
        result = self._run(
            ["bpftool", "prog", "show", "pinned", str(self._pin_path)],
            check=False,
        )
        return result.returncode == 0

    def _is_bridge_listening(self) -> bool:
        """Return True if the bridge port is in LISTEN state.

        Uses 'ss -tlnp' to inspect TCP listening sockets without requiring root.

        Returns:
            True if the bridge port appears in ss output as a LISTEN socket.
        """
        result = self._run(["ss", "-tlnp"], check=False)
        port_str = f":{self._bridge_port}"
        return port_str in result.stdout

    def _run(
        self,
        cmd: list[str],
        *,
        check: bool,
    ) -> subprocess.CompletedProcess[str]:
        """Execute a subprocess command and return the result.

        Args:
            cmd: Command and arguments as a list of strings.
            check: If True, raise RuntimeError on non-zero exit code.

        Returns:
            CompletedProcess instance with stdout/stderr as strings.

        Raises:
            RuntimeError: If check=True and returncode != 0.
        """
        logger.debug("BpfManager exec: %s", shlex.join(cmd))
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(
                f"BpfManager command timed out: {shlex.join(cmd)}"
            ) from exc
        except FileNotFoundError as exc:
            raise RuntimeError(
                f"BpfManager command not found: {cmd[0]!r}"
            ) from exc

        if check and result.returncode != 0:
            raise RuntimeError(
                f"BpfManager command failed (exit {result.returncode}): "
                f"{shlex.join(cmd)}\nstderr: {result.stderr.strip()}"
            )
        return result
