# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Contract tests for container lifecycle adapter API surface.

Verifies that DockerComposeAdapter exposes the method signatures
consumed by ContainerLifecycleManager. No formal Protocol/ABC exists
for this adapter (it is a concrete infrastructure dependency), so these
tests verify structural stability of the public API.

Naming: test_{scenario}_when_{condition}_then_{expected}

References:
    - ADR-PROJ023-007: Container lifecycle architecture
    - H-07: Hexagonal architecture layer isolation
    - CLM-001 through CLM-005: Critical findings requiring adapter methods
"""

from __future__ import annotations

import inspect

from src.tool_exec.infrastructure.container_lifecycle.docker_compose_adapter import (
    DockerComposeAdapter,
)
from src.tool_exec.infrastructure.container_lifecycle.service_status import ServiceStatus


class TestDockerComposeAdapterContract:
    """Contract: DockerComposeAdapter API surface required by CLM."""

    def test_adapter_when_inspected_then_has_is_docker_available_method(self) -> None:
        """CLM calls is_docker_available() -> bool before any operation."""
        method = getattr(DockerComposeAdapter, "is_docker_available", None)
        assert method is not None
        sig = inspect.signature(method)
        # from __future__ import annotations makes return annotation a string
        assert sig.return_annotation in (bool, "bool")

    def test_adapter_when_inspected_then_has_get_running_services_method(self) -> None:
        """CLM-001 calls get_running_services(compose_file) -> list[ServiceStatus]."""
        method = getattr(DockerComposeAdapter, "get_running_services", None)
        assert method is not None
        sig = inspect.signature(method)
        params = list(sig.parameters.keys())
        assert "compose_file" in params

    def test_adapter_when_inspected_then_has_compose_build_method(self) -> None:
        """CLM calls compose_build(compose_file) during startup."""
        method = getattr(DockerComposeAdapter, "compose_build", None)
        assert method is not None
        sig = inspect.signature(method)
        assert "compose_file" in sig.parameters

    def test_adapter_when_inspected_then_has_compose_up_method(self) -> None:
        """CLM calls compose_up(compose_file) during startup."""
        method = getattr(DockerComposeAdapter, "compose_up", None)
        assert method is not None
        sig = inspect.signature(method)
        assert "compose_file" in sig.parameters

    def test_adapter_when_inspected_then_has_compose_down_method(self) -> None:
        """CLM-003 calls compose_down(compose_file) during teardown."""
        method = getattr(DockerComposeAdapter, "compose_down", None)
        assert method is not None
        sig = inspect.signature(method)
        assert "compose_file" in sig.parameters

    def test_adapter_when_inspected_then_has_wait_for_health_method(self) -> None:
        """CLM calls wait_for_health(compose_file, service, max_wait) -> bool."""
        method = getattr(DockerComposeAdapter, "wait_for_health", None)
        assert method is not None
        sig = inspect.signature(method)
        assert "compose_file" in sig.parameters
        assert "service" in sig.parameters
        assert "max_wait" in sig.parameters
        assert sig.return_annotation in (bool, "bool")

    def test_adapter_when_inspected_then_has_remove_volumes_method(self) -> None:
        """CLM-005 calls remove_volumes(volume_names) -> list[str]."""
        method = getattr(DockerComposeAdapter, "remove_volumes", None)
        assert method is not None
        sig = inspect.signature(method)
        assert "volume_names" in sig.parameters

    def test_adapter_when_inspected_then_has_list_project_volumes_method(self) -> None:
        """CLM-005 calls list_project_volumes() -> list[str]."""
        method = getattr(DockerComposeAdapter, "list_project_volumes", None)
        assert method is not None

    def test_adapter_when_inspected_then_has_project_name_property(self) -> None:
        """CLM reads adapter.project_name for compose project isolation."""
        assert isinstance(getattr(DockerComposeAdapter, "project_name", None), property)


class TestServiceStatusContract:
    """Contract: ServiceStatus fields required by CLM."""

    def test_service_status_when_created_then_has_name_field(self) -> None:
        """CLM reads svc.name to identify services."""
        svc = ServiceStatus(name="test", state="running", health="healthy")
        assert hasattr(svc, "name")
        assert svc.name == "test"

    def test_service_status_when_created_then_has_state_field(self) -> None:
        """CLM-001 checks svc.state == 'running' for Docker reality."""
        svc = ServiceStatus(name="test", state="running", health="healthy")
        assert hasattr(svc, "state")
        assert svc.state == "running"

    def test_service_status_when_created_then_has_health_field(self) -> None:
        """CLM reads svc.health for health check evaluation."""
        svc = ServiceStatus(name="test", state="running", health="healthy")
        assert hasattr(svc, "health")
        assert svc.health == "healthy"
