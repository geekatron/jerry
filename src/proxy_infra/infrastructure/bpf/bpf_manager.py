# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BPF program lifecycle manager for eBPF transparent Envoy redirect.

Manages the full lifecycle of 3 BPF cgroup programs (connect4, sockops, getsockopt):
  - Load compiled BPF objects and pin to bpffs atomically
  - Detach stale root cgroup BPF before per-container attachment (EN-023-001 F-2)
  - Attach to container-specific cgroup (NOT root cgroup)
  - Create jerry-intercept cgroup as CHILD of container cgroup (EN-023-001 F-8)
  - Pin all 3 programs to bpffs to prevent fail-open on process exit (OPSEC-F5 CRITICAL)
  - Verify all 3 pins before declaring ready
  - Detach and clean up all 3 programs on teardown

Design constraints:
  H-10:  One public class per file.
  H-11:  All public methods have type annotations.
  H-07:  Infrastructure layer — subprocess and pathlib use is permitted here.
  OPSEC-F5: BPF programs MUST be pinned; unpinned programs cause fail-open.
  C5:    NEVER leave fewer than 3 programs loaded during ACTIVE engagement.
  B3:    NEVER leave programs attached/pinned after teardown.
  F-8:   jerry-intercept cgroup MUST be a CHILD of the container cgroup.

References:
  EN-023-010   -- Envoy unified traffic path with 3-program BPF
  EN-023-009   -- 3-program BPF architecture (connect4, sockops, getsockopt)
"""

from __future__ import annotations

import dataclasses
import logging
import shlex
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

# Canonical bpffs mount point
_BPFFS_ROOT = Path("/sys/fs/bpf")

# Default path where bpffs maps are pinned (shared across all 3 programs)
_DEFAULT_MAP_DIR = _BPFFS_ROOT / "rainbow_maps"

# Cgroup v2 docker hierarchy root
_CGROUP_DOCKER_ROOT = Path("/sys/fs/cgroup/docker")

# Name of the child intercept cgroup under the container cgroup (F-8)
_INTERCEPT_CGROUP_NAME = "jerry-intercept"


@dataclasses.dataclass(frozen=True)
class _BpfProgramDef:
    """Definition of a BPF program to load, pin, and attach."""

    name: str
    object_suffix: str
    pin_name: str
    attach_type: str


# The 3 programs that make up the unified Envoy architecture (EN-023-009).
# Order matters: connect4 must be loaded first (provides dst_lookup map),
# sockops second (provides port_cookie map), getsockopt third (reads both).
_PROGRAMS: tuple[_BpfProgramDef, ...] = (
    _BpfProgramDef(
        name="connect4",
        object_suffix="connect4.bpf.o",
        pin_name="rainbow_connect4",
        attach_type="connect4",
    ),
    _BpfProgramDef(
        name="sockops",
        object_suffix="sockops.bpf.o",
        pin_name="rainbow_sockops",
        attach_type="sock_ops",
    ),
    _BpfProgramDef(
        name="getsockopt",
        object_suffix="getsockopt.bpf.o",
        pin_name="rainbow_getsockopt",
        attach_type="getsockopt",
    ),
)


class BpfManager:
    """Manages 3-program BPF lifecycle for transparent Envoy redirect.

    All bpftool interactions are performed via subprocess. Tests should mock
    subprocess.run to avoid requiring kernel BPF capabilities.

    EN-023-010 lifecycle:
        1. load_and_attach(container_id)  -- load all 3 programs atomically
        2. is_ready()  -- verify all 3 pins + Envoy listening on port 15001
        3. detach_and_cleanup()  -- unpin and detach all 3 programs

    Args:
        bpf_object_path: Path to the directory containing compiled .bpf.o files.
            If a file path is given, the parent directory is used.
        bridge_port: TCP port for readiness check (default 15001, Envoy transparent TCP).
        pin_path: Deprecated; pin paths are derived from _PROGRAMS definitions.
        map_dir: bpffs directory for pinning shared maps (default /sys/fs/bpf/rainbow_maps).
    """

    def __init__(
        self,
        bpf_object_path: str,
        bridge_port: int = 15001,
        pin_path: str | None = None,
        map_dir: str | None = None,
    ) -> None:
        """Initialise the BPF manager.

        Args:
            bpf_object_path: Path to compiled BPF object file or directory.
                If a file, the parent directory is used to find all 3 .bpf.o files.
            bridge_port: Listening port for readiness check (default 15001).
            pin_path: Deprecated; ignored. Pin paths derived from program definitions.
            map_dir: Override bpffs map directory; defaults to /sys/fs/bpf/rainbow_maps.
        """
        obj_path = Path(bpf_object_path)
        self._bpf_object_dir = (
            obj_path.parent if obj_path.is_file() or obj_path.suffix else obj_path
        )
        self._bridge_port = bridge_port
        self._map_dir = Path(map_dir) if map_dir else _DEFAULT_MAP_DIR
        self._attached_cgroup: str | None = None
        self._envoy_cgroup: str | None = None
        self._loaded_programs: list[_BpfProgramDef] = []

    # ------------------------------------------------------------------
    # Public lifecycle API
    # ------------------------------------------------------------------

    def load_and_attach(
        self,
        container_id: str,
        envoy_container_id: str | None = None,
    ) -> None:
        """Load all 3 BPF programs and attach to appropriate cgroups.

        BPF cgroup programs fire only for processes in the attached cgroup.
        Split-cgroup attachment (BUG-023-004):
          - connect4 + sockops: attached to TOOL container cgroup
            (intercept tool process connect() and TCP ESTABLISHED events)
          - getsockopt: attached to ENVOY container cgroup
            (intercept Envoy's getsockopt(SO_ORIGINAL_DST) calls)

        Maps (dst_lookup, port_cookie) are pinned on bpffs and shared across
        all 3 programs regardless of cgroup attachment.

        If envoy_container_id is None, all 3 programs attach to the tool
        container cgroup (sidecar mode: Envoy runs inside tool container).

        Steps:
          1. Load all 3 BPF objects and pin programs + maps to bpffs (C5).
             If any program fails, rollback all previously loaded programs.
          2. Detach any stale BPF from root cgroup (EN-023-001 F-2).
          3. Find container cgroup paths (tool + optional envoy).
          4. Create jerry-intercept as CHILD of tool container cgroup (F-8).
          5. Attach connect4 + sockops to tool container cgroup.
          6. Attach getsockopt to envoy container cgroup (or tool cgroup if sidecar).

        Args:
            container_id: Tool container Docker ID (short or full).
            envoy_container_id: Envoy container Docker ID. If None, getsockopt
                attaches to tool container cgroup (sidecar mode).

        Raises:
            RuntimeError: If any BPF load, pin, or attachment fails.
        """
        self._loaded_programs = []

        for prog in _PROGRAMS:
            try:
                self._load_and_pin_program(prog)
                self._loaded_programs.append(prog)
            except RuntimeError:
                logger.error(
                    "Failed to load %s — rolling back %d loaded programs",
                    prog.name,
                    len(self._loaded_programs),
                )
                self._rollback_loaded()
                raise

        logger.info("All 3 BPF programs loaded and pinned")

        self._detach_root_cgroup()

        tool_cgroup = self.get_container_cgroup(container_id)
        logger.info("Tool container cgroup resolved: %s", tool_cgroup)

        self.create_intercept_cgroup(tool_cgroup)

        # Determine getsockopt cgroup: Envoy container or tool container (sidecar)
        if envoy_container_id:
            envoy_cgroup = self.get_container_cgroup(envoy_container_id)
            logger.info("Envoy container cgroup resolved: %s", envoy_cgroup)
        else:
            envoy_cgroup = tool_cgroup
            logger.info("Sidecar mode: getsockopt attaches to tool cgroup")

        # Attach connect4 + sockops to tool container cgroup
        logger.info("Attaching connect4 + sockops to tool cgroup %s", tool_cgroup)
        self._attach_program_to_cgroup(
            tool_cgroup,
            _PROGRAMS[0],  # connect4
        )
        self._attach_program_to_cgroup(
            tool_cgroup,
            _PROGRAMS[1],  # sockops
        )

        # Attach getsockopt to envoy cgroup (or tool cgroup in sidecar mode)
        logger.info(
            "Attaching getsockopt to %s cgroup %s",
            "envoy" if envoy_container_id else "tool (sidecar)",
            envoy_cgroup,
        )
        self._attach_program_to_cgroup(
            envoy_cgroup,
            _PROGRAMS[2],  # getsockopt
        )

        # Track both cgroups for cleanup
        self._attached_cgroup = tool_cgroup
        self._envoy_cgroup = envoy_cgroup

    def detach_and_cleanup(self) -> None:
        """Detach and unpin all 3 BPF programs from cgroup and bpffs.

        Safe to call even if attach was never completed. Logs warnings for
        any cleanup steps that fail rather than raising.
        Constraint B3: NEVER leave programs attached/pinned after teardown.
        """
        if self._attached_cgroup:
            # Detach connect4 + sockops from tool cgroup
            for prog in _PROGRAMS[:2]:  # connect4, sockops
                logger.info("Detaching %s from tool cgroup %s", prog.name, self._attached_cgroup)
                self._detach_program_from_cgroup(self._attached_cgroup, prog)
            # Detach getsockopt from envoy cgroup (or tool cgroup in sidecar mode)
            getsockopt_cgroup = self._envoy_cgroup or self._attached_cgroup
            logger.info("Detaching getsockopt from cgroup %s", getsockopt_cgroup)
            self._detach_program_from_cgroup(getsockopt_cgroup, _PROGRAMS[2])
            self._attached_cgroup = None
            self._envoy_cgroup = None
        else:
            logger.debug("No attached cgroup recorded; skipping detach")

        for prog in _PROGRAMS:
            pin_path = _BPFFS_ROOT / prog.pin_name
            logger.info("Unpinning %s from %s", prog.name, pin_path)
            self._unpin_program(pin_path)

        self._loaded_programs = []

    def get_container_cgroup(self, container_id: str) -> str:
        """Locate container cgroup via hostname-to-cgroup pattern (EN-023-001 F-3).

        Args:
            container_id: Short or full Docker container ID.

        Returns:
            Absolute path string to the container's cgroup directory.

        Raises:
            RuntimeError: If the cgroup directory cannot be found.
        """
        result = self._run(
            [
                "find",
                str(_CGROUP_DOCKER_ROOT),
                "-maxdepth",
                "1",
                "-name",
                f"{container_id}*",
                "-type",
                "d",
            ],
            check=False,
        )
        paths = [p.strip() for p in result.stdout.splitlines() if p.strip()]
        if not paths:
            raise RuntimeError(
                f"Container cgroup not found for '{container_id}' under {_CGROUP_DOCKER_ROOT}"
            )
        return paths[0]

    def create_intercept_cgroup(self, container_cgroup: str) -> str:
        """Create jerry-intercept as a CHILD of the container cgroup (F-8).

        Args:
            container_cgroup: Absolute path to the container's cgroup directory.

        Returns:
            Absolute path string to the jerry-intercept cgroup.

        Raises:
            RuntimeError: If the child cgroup cannot be created.
        """
        intercept_path = Path(container_cgroup) / _INTERCEPT_CGROUP_NAME
        self._run(["mkdir", "-p", str(intercept_path)], check=True)
        logger.info("Created intercept child cgroup at %s", intercept_path)
        return str(intercept_path)

    def is_ready(self) -> bool:
        """Check that all 3 BPF programs are pinned and Envoy is listening.

        Verifies:
          1. All 3 pin paths exist on bpffs (OPSEC-F5, C5).
          2. Envoy port 15001 is in LISTEN state (C8).

        Returns:
            True if all 3 pins and Envoy are confirmed ready.
        """
        for prog in _PROGRAMS:
            pin_path = _BPFFS_ROOT / prog.pin_name
            if not self._is_program_pinned(pin_path):
                logger.warning("BPF %s pin not found at %s", prog.name, pin_path)
                return False
        if not self._is_port_listening():
            logger.warning("Envoy not listening on port %d", self._bridge_port)
            return False
        return True

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _load_and_pin_program(self, prog: _BpfProgramDef) -> None:
        """Load a single BPF object and pin to bpffs.

        Args:
            prog: Program definition with object suffix and pin name.

        Raises:
            RuntimeError: If bpftool prog load fails.
        """
        object_path = self._bpf_object_dir / prog.object_suffix
        pin_path = _BPFFS_ROOT / prog.pin_name
        self._run(
            [
                "bpftool",
                "prog",
                "load",
                str(object_path),
                str(pin_path),
                "pinmaps",
                str(self._map_dir),
            ],
            check=True,
        )
        logger.info("BPF %s pinned at %s", prog.name, pin_path)

    def _rollback_loaded(self) -> None:
        """Unpin all successfully loaded programs (rollback on partial failure)."""
        for prog in reversed(self._loaded_programs):
            pin_path = _BPFFS_ROOT / prog.pin_name
            logger.info("Rolling back: unpinning %s from %s", prog.name, pin_path)
            self._unpin_program(pin_path)
        self._loaded_programs = []

    def _detach_root_cgroup(self) -> None:
        """Attempt to detach stale BPF from root cgroup (EN-023-001 F-2).

        Non-fatal: root cgroup may already be clean.
        """
        result = self._run(
            [
                "bpftool",
                "cgroup",
                "detach",
                "/sys/fs/cgroup",
                "connect4",
                "pinned",
                str(_BPFFS_ROOT / "rainbow_connect4"),
            ],
            check=False,
        )
        if result.returncode != 0:
            logger.debug(
                "Root cgroup detach returned non-zero (may be clean): %s",
                result.stderr.strip(),
            )

    def _attach_program_to_cgroup(
        self,
        cgroup_path: str,
        prog: _BpfProgramDef,
    ) -> None:
        """Attach a single pinned BPF program to a specific cgroup.

        BUG-023-004: Programs are attached to different cgroups based on
        where they need to fire. connect4+sockops go to the tool container
        cgroup; getsockopt goes to the Envoy container cgroup.

        Args:
            cgroup_path: Absolute path to the target cgroup directory.
            prog: Program definition specifying attach_type and pin_name.

        Raises:
            RuntimeError: If bpftool cgroup attach fails.
        """
        self._run(
            [
                "bpftool",
                "cgroup",
                "attach",
                cgroup_path,
                prog.attach_type,
                "pinned",
                str(_BPFFS_ROOT / prog.pin_name),
            ],
            check=True,
        )

    def _detach_program_from_cgroup(self, cgroup_path: str, prog: _BpfProgramDef) -> None:
        """Detach a BPF program from the specified cgroup. Non-fatal on error.

        Args:
            cgroup_path: Absolute path to the cgroup to detach from.
            prog: Program definition specifying attach_type and pin_name.
        """
        pin_path = _BPFFS_ROOT / prog.pin_name
        result = self._run(
            [
                "bpftool",
                "cgroup",
                "detach",
                cgroup_path,
                prog.attach_type,
                "pinned",
                str(pin_path),
            ],
            check=False,
        )
        if result.returncode != 0:
            logger.warning(
                "Detach %s from %s returned non-zero: %s",
                prog.name,
                cgroup_path,
                result.stderr.strip(),
            )

    def _unpin_program(self, pin_path: Path) -> None:
        """Remove a program pin from bpffs. Non-fatal on error."""
        result = self._run(["unlink", str(pin_path)], check=False)
        if result.returncode != 0:
            logger.warning("Unpin of %s returned non-zero: %s", pin_path, result.stderr.strip())

    def _is_program_pinned(self, pin_path: Path) -> bool:
        """Return True if the program pin path exists on bpffs."""
        result = self._run(
            ["bpftool", "prog", "show", "pinned", str(pin_path)],
            check=False,
        )
        return result.returncode == 0

    def _is_port_listening(self) -> bool:
        """Return True if the Envoy port is in LISTEN state."""
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
            raise RuntimeError(f"BpfManager command timed out: {shlex.join(cmd)}") from exc
        except FileNotFoundError as exc:
            raise RuntimeError(f"BpfManager command not found: {cmd[0]!r}") from exc

        if check and result.returncode != 0:
            raise RuntimeError(
                f"BpfManager command failed (exit {result.returncode}): "
                f"{shlex.join(cmd)}\nstderr: {result.stderr.strip()}"
            )
        return result
