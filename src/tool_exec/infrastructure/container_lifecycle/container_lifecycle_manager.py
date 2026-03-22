# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Container lifecycle manager for the /rainbow skill orchestrator.

Implements ADR-PROJ023-007 Option D (Hybrid: Zone 1 eager, Zone 2/3 lazy
with scope gate). Domain layer: orchestrates startup, health checks,
teardown, and session state via the DockerComposeAdapter.

Addresses critical findings:
- CLM-001: Always verify against Docker reality, never trust state file alone
- CLM-002: Derive COMPOSE_PROJECT_NAME from worktree path hash
- CLM-003: Verify containers down BEFORE deleting state file
- CLM-005: Volume cleanup on teardown with verification
"""

from __future__ import annotations

import logging
import os
import subprocess
import time
from pathlib import Path
from typing import Any

import yaml

from src.tool_exec.infrastructure.container_lifecycle.cluster_state import ClusterState
from src.tool_exec.infrastructure.container_lifecycle.cluster_status import ClusterStatus
from src.tool_exec.infrastructure.container_lifecycle.docker_compose_adapter import (
    DockerComposeAdapter,
)
from src.tool_exec.infrastructure.container_lifecycle.session_state import SessionState
from src.tool_exec.infrastructure.container_lifecycle.teardown_result import TeardownResult
from src.tool_exec.infrastructure.container_lifecycle.worktree_isolation import (
    derive_compose_project_name,
    session_state_path,
)

logger = logging.getLogger(__name__)


class ContainerLifecycleManager:
    """Manages Docker Compose cluster lifecycle for /rainbow.

    Implements ADR-PROJ023-007 Option D with critical finding mitigations:
    - CLM-001: Docker reality check before trusting state file
    - CLM-002: Worktree-isolated compose project names
    - CLM-003: Verify containers down before deleting state file
    - CLM-005: Explicit volume cleanup on teardown
    """

    def __init__(
        self,
        project_root: Path,
        config_path: Path | None = None,
        adapter: DockerComposeAdapter | None = None,
    ) -> None:
        """Initialize the lifecycle manager.

        Args:
            project_root: Absolute path to the repository root.
            config_path: Path to tool-exec.yaml. Defaults to
                ``skills/rainbow/config/tool-exec.yaml``.
            adapter: Docker Compose adapter. Auto-created if None.
        """
        self._project_root = project_root
        self._config_path = config_path or (
            project_root / "skills" / "rainbow" / "config" / "tool-exec.yaml"
        )
        self._compose_project_name = derive_compose_project_name(project_root)
        self._adapter = adapter or DockerComposeAdapter(project_root, self._compose_project_name)
        self._state_path = session_state_path(project_root)
        self._config: dict[str, Any] = {}

    @property
    def compose_project_name(self) -> str:
        """Return the worktree-isolated compose project name."""
        return self._compose_project_name

    def _load_config(self) -> dict[str, Any]:
        """Load tool-exec.yaml configuration."""
        if not self._config:
            with self._config_path.open() as f:
                self._config = yaml.safe_load(f) or {}
        return self._config

    def _get_compose_files(self) -> dict[str, str]:
        """Get cluster name -> compose file path mapping from config."""
        config = self._load_config()
        return config.get("zone_compose_files", {})

    def _load_state(self) -> SessionState | None:
        """Load session state from file, if it exists."""
        if self._state_path.exists():
            try:
                with self._state_path.open() as f:
                    data = yaml.safe_load(f)
                if isinstance(data, dict):
                    return SessionState.from_dict(data)
            except (yaml.YAMLError, OSError) as e:
                logger.warning("Failed to load session state from %s: %s", self._state_path, e)
        return None

    def _save_state(self, state: SessionState) -> None:
        """Persist session state to file."""
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        with self._state_path.open("w") as f:
            yaml.dump(state.to_dict(), f, default_flow_style=False)

    def _delete_state(self) -> bool:
        """Delete the session state file. Returns True if deleted."""
        if self._state_path.exists():
            try:
                self._state_path.unlink()
                return True
            except OSError as e:
                logger.warning("Failed to delete state file %s: %s", self._state_path, e)
                return False
        return True

    def _verify_cluster_running(self, cluster_name: str, compose_file: str) -> bool:
        """CLM-001: Verify cluster is actually running via Docker reality check.

        Never trust the state file alone. Always ask Docker.

        Args:
            cluster_name: Name of the cluster.
            compose_file: Path to docker-compose.yml.

        Returns:
            True if all services in the cluster report State=running.
        """
        services = self._adapter.get_running_services(compose_file)
        if not services:
            logger.info(
                "CLM-001: Docker reports no services for cluster %s — state file stale",
                cluster_name,
            )
            return False

        for svc in services:
            if svc.state != "running":
                logger.info(
                    "CLM-001: Service %s in cluster %s is %s, not running",
                    svc.name,
                    cluster_name,
                    svc.state,
                )
                return False
        return True

    def ensure_clusters_running(
        self,
        required_clusters: list[str],
        *,
        health_check_timeout: int | None = None,
    ) -> list[ClusterStatus]:
        """Ensure the specified clusters are running.

        For each cluster:
        1. Check Docker reality (CLM-001) — not just state file
        2. If already running per Docker, skip startup
        3. If not running, build (if needed) and start
        4. Wait for health checks

        Args:
            required_clusters: List of cluster names (keys from
                zone_compose_files in tool-exec.yaml).
            health_check_timeout: Override health check timeout in seconds.

        Returns:
            List of ClusterStatus for each requested cluster.
        """
        if not self._adapter.is_docker_available():
            return [
                ClusterStatus(
                    cluster_name=c,
                    compose_file="",
                    state=ClusterState.ERROR,
                    error="Docker daemon is not available",
                )
                for c in required_clusters
            ]

        compose_files = self._get_compose_files()
        config = self._load_config()
        timeout = health_check_timeout or config.get("container", {}).get(
            "health_check_timeout", 30
        )

        # Load or create session state
        state = self._load_state() or SessionState(
            pid=os.getpid(),
            compose_project_name=self._compose_project_name,
            created_at=time.time(),
        )

        results: list[ClusterStatus] = []

        for cluster_name in required_clusters:
            compose_file = compose_files.get(cluster_name)
            if not compose_file:
                results.append(
                    ClusterStatus(
                        cluster_name=cluster_name,
                        compose_file="",
                        state=ClusterState.ERROR,
                        error=f"Unknown cluster: {cluster_name}. "
                        f"Available: {', '.join(compose_files.keys())}",
                    )
                )
                continue

            # CLM-001: Always verify Docker reality
            if self._verify_cluster_running(cluster_name, compose_file):
                services = self._adapter.get_running_services(compose_file)
                state.clusters[cluster_name] = "running"
                results.append(
                    ClusterStatus(
                        cluster_name=cluster_name,
                        compose_file=compose_file,
                        state=ClusterState.RUNNING,
                        services=services,
                    )
                )
                logger.info("Cluster %s already running (Docker verified)", cluster_name)
                continue

            # Need to start — build first, then up
            logger.info("Starting cluster %s from %s", cluster_name, compose_file)
            try:
                self._adapter.compose_build(compose_file)
                self._adapter.compose_up(compose_file)

                # Wait for health on all services
                services = self._adapter.get_running_services(compose_file)
                all_healthy = True
                for svc in services:
                    if not self._adapter.wait_for_health(compose_file, svc.name, max_wait=timeout):
                        all_healthy = False
                        logger.warning(
                            "Service %s in cluster %s did not become healthy within %ds",
                            svc.name,
                            cluster_name,
                            timeout,
                        )

                final_services = self._adapter.get_running_services(compose_file)
                cluster_state = ClusterState.RUNNING if all_healthy else ClusterState.UNHEALTHY
                state.clusters[cluster_name] = "running"

                results.append(
                    ClusterStatus(
                        cluster_name=cluster_name,
                        compose_file=compose_file,
                        state=cluster_state,
                        services=final_services,
                    )
                )

            except subprocess.CalledProcessError as e:
                state.clusters[cluster_name] = "error"
                results.append(
                    ClusterStatus(
                        cluster_name=cluster_name,
                        compose_file=compose_file,
                        state=ClusterState.ERROR,
                        error=f"Failed to start: {e}",
                    )
                )
            except subprocess.TimeoutExpired:
                state.clusters[cluster_name] = "error"
                results.append(
                    ClusterStatus(
                        cluster_name=cluster_name,
                        compose_file=compose_file,
                        state=ClusterState.ERROR,
                        error="Startup timed out",
                    )
                )

        # Persist updated state
        state.pid = os.getpid()
        self._save_state(state)

        return results

    def teardown(self, engagement_id: str | None = None) -> TeardownResult:
        """Tear down all running clusters.

        CLM-003 sequence:
        1. Call docker compose down --volumes --remove-orphans
        2. Verify zero containers remain via docker compose ps
        3. Only then delete the session state file
        4. If verification fails, keep state file for retry

        CLM-005: Explicitly remove named volumes and verify removal.

        Args:
            engagement_id: Optional engagement ID for scoped teardown.

        Returns:
            TeardownResult with details of what was torn down.
        """
        compose_files = self._get_compose_files()
        state = self._load_state()

        clusters_to_tear_down: list[str] = []
        if state and state.clusters:
            clusters_to_tear_down = [
                name for name, status in state.clusters.items() if status in ("running", "error")
            ]
        else:
            clusters_to_tear_down = list(compose_files.keys())

        torn_down: list[str] = []
        all_volumes_removed: list[str] = []
        errors: list[str] = []
        all_verified = True

        for cluster_name in clusters_to_tear_down:
            compose_file = compose_files.get(cluster_name)
            if not compose_file:
                continue

            # Step 1: docker compose down --volumes --remove-orphans
            try:
                self._adapter.compose_down(compose_file)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                errors.append(f"compose down failed for {cluster_name}: {e}")
                all_verified = False
                continue

            # Step 2: CLM-003 — verify zero containers remain
            remaining = self._adapter.get_running_services(compose_file)
            if remaining:
                running = [s for s in remaining if s.state == "running"]
                if running:
                    errors.append(
                        f"CLM-003: Cluster {cluster_name} still has {len(running)} "
                        f"running containers after teardown: "
                        f"{', '.join(s.name for s in running)}"
                    )
                    all_verified = False
                    continue

            torn_down.append(cluster_name)

        # CLM-005: Remove named volumes
        project_volumes = self._adapter.list_project_volumes()
        if project_volumes:
            removed = self._adapter.remove_volumes(project_volumes)
            all_volumes_removed.extend(removed)
            remaining_volumes = set(project_volumes) - set(removed)
            if remaining_volumes:
                errors.append(f"CLM-005: Failed to remove volumes: {', '.join(remaining_volumes)}")

        # Step 3: CLM-003 — only delete state file if all clusters verified down
        state_deleted = False
        if all_verified:
            state_deleted = self._delete_state()
            if not state_deleted:
                errors.append("CLM-003: Failed to delete session state file")
        else:
            logger.warning("CLM-003: Keeping state file for retry — not all clusters verified down")

        return TeardownResult(
            clusters_torn_down=torn_down,
            volumes_removed=all_volumes_removed,
            errors=errors,
            state_file_deleted=state_deleted,
        )
