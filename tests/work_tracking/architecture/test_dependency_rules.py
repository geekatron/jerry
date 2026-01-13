"""Architecture tests for dependency rules.

Enforces specific dependency rules within the work_tracking domain
to ensure proper separation of concerns and avoid circular dependencies.

Requires pytest-archon package. Tests are skipped if not installed.

References:
    - IMPL-010: Architecture Tests
    - Clean Architecture dependency rule
    - DDD Aggregate boundaries
"""

from __future__ import annotations

import pytest

# Skip module if pytest-archon is not installed
pytest.importorskip("pytest_archon", reason="pytest-archon not installed")

from pytest_archon import archrule

# =============================================================================
# Event Dependency Rules
# =============================================================================


class TestEventDependencyRules:
    """Tests for domain event dependency rules."""

    def test_events_no_aggregate_imports(self) -> None:
        """Events must not import aggregates (avoid cycles)."""
        (
            archrule("events_no_aggregates")
            .match("src.work_tracking.domain.events.*")
            .should_not_import("src.work_tracking.domain.aggregates.*")
            .check("src")
        )

    def test_events_no_service_imports(self) -> None:
        """Events must not import services."""
        (
            archrule("events_no_services")
            .match("src.work_tracking.domain.events.*")
            .should_not_import("src.work_tracking.domain.services.*")
            .check("src")
        )

    def test_events_may_import_shared_kernel(self) -> None:
        """Events may import from shared kernel (DomainEvent base)."""
        (
            archrule("events_use_shared_kernel")
            .match("src.work_tracking.domain.events.*")
            .may_import("src.shared_kernel.*")
            .check("src")
        )


# =============================================================================
# Infrastructure Dependency Rules
# =============================================================================


class TestInfrastructureDependencyRules:
    """Tests for infrastructure layer dependency rules."""

    def test_infrastructure_may_import_domain(self) -> None:
        """Infrastructure may import from domain (implements ports)."""
        (
            archrule("infra_uses_domain")
            .match("src.work_tracking.infrastructure.*")
            .may_import("src.work_tracking.domain.*")
            .check("src")
        )

    def test_infrastructure_may_import_shared_kernel(self) -> None:
        """Infrastructure may import from shared kernel."""
        (
            archrule("infra_uses_shared_kernel")
            .match("src.work_tracking.infrastructure.*")
            .may_import("src.shared_kernel.*")
            .check("src")
        )


# =============================================================================
# No Circular Dependencies
# =============================================================================


class TestNoCircularDependencies:
    """Tests to prevent circular dependencies."""

    def test_value_objects_no_mutual_imports(self) -> None:
        """Value objects should minimize mutual imports."""
        # Specific rule: priority should not import work_type and vice versa
        # This prevents value object entanglement
        (
            archrule("priority_independent")
            .match("src.work_tracking.domain.value_objects.priority")
            .should_not_import("src.work_tracking.domain.value_objects.work_type")
            .check("src")
        )

    def test_ports_no_cross_imports(self) -> None:
        """Ports should not import from each other."""
        (
            archrule("event_store_independent")
            .match("src.work_tracking.domain.ports.event_store")
            .should_not_import("src.work_tracking.domain.ports.repository")
            .check("src")
        )


# =============================================================================
# Shared Kernel Constraints
# =============================================================================


class TestSharedKernelConstraints:
    """Tests for shared kernel usage constraints."""

    def test_shared_kernel_no_work_tracking_imports(self) -> None:
        """Shared kernel must not import from work_tracking (it's shared!)."""
        (
            archrule("shared_kernel_independent")
            .match("src.shared_kernel.*")
            .should_not_import("src.work_tracking.*")
            .check("src")
        )

    def test_shared_kernel_no_external_domain_imports(self) -> None:
        """Shared kernel must not import from any bounded context."""
        (
            archrule("shared_kernel_no_contexts")
            .match("src.shared_kernel.*")
            .should_not_import("src.session_management.*")
            .check("src")
        )


# =============================================================================
# Test Module Constraints
# =============================================================================


class TestTestModuleConstraints:
    """Tests for test module organization."""

    def test_unit_tests_no_integration_imports(self) -> None:
        """Unit tests should not import from integration tests."""
        (
            archrule("unit_tests_independent")
            .match("tests.work_tracking.unit.*")
            .should_not_import("tests.work_tracking.integration.*")
            .check("tests")
        )


# =============================================================================
# Stdlib-Only Domain Tests
# =============================================================================


class TestStdlibOnlyDomain:
    """Tests that domain layer uses only stdlib (zero dependencies)."""

    def test_domain_no_third_party_libs(self) -> None:
        """Domain should not import third-party libraries."""
        # List of common third-party imports that should NOT appear in domain
        forbidden_imports = [
            "flask",
            "django",
            "fastapi",
            "sqlalchemy",
            "requests",
            "aiohttp",
            "redis",
            "celery",
            "pydantic",  # stdlib dataclasses preferred
        ]

        for lib in forbidden_imports:
            (
                archrule(f"domain_no_{lib}")
                .match("src.work_tracking.domain.*")
                .should_not_import(f"{lib}.*")
                .check("src")
            )

    def test_value_objects_stdlib_only(self) -> None:
        """Value objects should use stdlib only."""
        (
            archrule("vo_no_numpy")
            .match("src.work_tracking.domain.value_objects.*")
            .should_not_import("numpy.*")
            .check("src")
        )
