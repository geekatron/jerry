# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Docker Compose subprocess adapter for container lifecycle management.

Infrastructure layer: all Docker interaction is isolated here.
The ContainerLifecycleManager calls this adapter through well-defined
methods, never running subprocess commands directly.
"""

from __future__ import annotations

import json
import logging
import subprocess
import time
from pathlib import Path

from src.tool_exec.infrastructure.container_lifecycle.service_status import ServiceStatus

logger = logging.getLogger(__name__)


class DockerComposeAdapter:
    """Infrastructure adapter for Docker Compose subprocess calls."""

    def __init__(self, project_root: Path, compose_project_name: str) -> None:
        """Initialize the adapter.

        Args:
            project_root: Absolute path to the repository root.
            compose_project_name: Docker Compose project name
                (worktree-isolated per CLM-002).
        """
        self._project_root = project_root
        self._compose_project_name = compose_project_name

    @property
    def project_name(self) -> str:
        """Return the compose project name."""
        return self._compose_project_name

    def is_docker_available(self) -> bool:
        """Check if the Docker daemon is reachable."""
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10,
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False

    def get_running_services(self, compose_file: str) -> list[ServiceStatus]:
        """Query Docker for actual container state (CLM-001: Docker reality check).

        Args:
            compose_file: Path to docker-compose.yml relative to project root.

        Returns:
            List of ServiceStatus for each service Docker reports.
        """
        abs_compose = str(self._project_root / compose_file)
        try:
            result = subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    abs_compose,
                    "-p",
                    self._compose_project_name,
                    "ps",
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
                cwd=str(self._project_root),
                timeout=30,
            )
            if result.returncode != 0:
                logger.warning(
                    "docker compose ps failed for %s: %s",
                    compose_file,
                    result.stderr.strip(),
                )
                return []

            services: list[ServiceStatus] = []
            output = result.stdout.strip()
            if not output:
                return []

            # docker compose ps --format json may output one JSON object per
            # line or a JSON array depending on Docker Compose version.
            for line in output.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        services.append(
                            ServiceStatus(
                                name=item.get("Service", item.get("Name", "")),
                                state=item.get("State", "unknown"),
                                health=item.get("Health", "none"),
                            )
                        )
                except json.JSONDecodeError:
                    logger.warning("Failed to parse docker compose ps output line: %s", line)
            return services

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            logger.warning("Failed to query Docker state for %s: %s", compose_file, e)
            return []

    def compose_build(self, compose_file: str, *, timeout: int = 600) -> None:
        """Build images for a compose file.

        Args:
            compose_file: Path to docker-compose.yml relative to project root.
            timeout: Build timeout in seconds.
        """
        abs_compose = str(self._project_root / compose_file)
        subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                abs_compose,
                "-p",
                self._compose_project_name,
                "build",
            ],
            check=True,
            cwd=str(self._project_root),
            timeout=timeout,
        )

    def compose_up(self, compose_file: str, *, timeout: int = 120) -> None:
        """Start containers in detached mode.

        Args:
            compose_file: Path to docker-compose.yml relative to project root.
            timeout: Startup timeout in seconds.
        """
        abs_compose = str(self._project_root / compose_file)
        subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                abs_compose,
                "-p",
                self._compose_project_name,
                "up",
                "--detach",
            ],
            check=True,
            cwd=str(self._project_root),
            timeout=timeout,
        )

    def compose_down(self, compose_file: str) -> None:
        """Stop and remove containers, volumes, and orphans.

        Args:
            compose_file: Path to docker-compose.yml relative to project root.
        """
        abs_compose = str(self._project_root / compose_file)
        subprocess.run(
            [
                "docker",
                "compose",
                "-f",
                abs_compose,
                "-p",
                self._compose_project_name,
                "down",
                "--volumes",
                "--remove-orphans",
            ],
            capture_output=True,
            cwd=str(self._project_root),
            timeout=60,
        )

    def remove_volumes(self, volume_names: list[str]) -> list[str]:
        """Explicitly remove named Docker volumes (CLM-005).

        Args:
            volume_names: List of volume names to remove.

        Returns:
            List of volume names that were successfully removed.
        """
        removed: list[str] = []
        for vol in volume_names:
            try:
                result = subprocess.run(
                    ["docker", "volume", "rm", vol],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode == 0:
                    removed.append(vol)
                else:
                    logger.warning("Failed to remove volume %s: %s", vol, result.stderr.strip())
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                logger.warning("Failed to remove volume %s: %s", vol, e)
        return removed

    def list_project_volumes(self) -> list[str]:
        """List all Docker volumes belonging to this compose project.

        Returns:
            List of volume names matching the compose project name prefix.
        """
        try:
            result = subprocess.run(
                [
                    "docker",
                    "volume",
                    "ls",
                    "--filter",
                    f"name={self._compose_project_name}",
                    "--format",
                    "{{.Name}}",
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                return []
            return [v.strip() for v in result.stdout.strip().splitlines() if v.strip()]
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return []

    def wait_for_health(
        self,
        compose_file: str,
        service: str,
        *,
        max_wait: int = 30,
    ) -> bool:
        """Poll a service until healthy or running.

        Args:
            compose_file: Path to docker-compose.yml relative to project root.
            service: Name of the compose service.
            max_wait: Maximum seconds to wait.

        Returns:
            True if the service reached a healthy/running state.
        """
        deadline = time.monotonic() + max_wait
        while time.monotonic() < deadline:
            services = self.get_running_services(compose_file)
            for svc in services:
                if svc.name == service:
                    if svc.state == "running" and svc.health in ("healthy", "none", ""):
                        return True
            time.sleep(1)
        return False
