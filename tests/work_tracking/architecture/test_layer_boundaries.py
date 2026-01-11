"""Architecture tests for layer boundaries.

Enforces the hexagonal architecture constraint that inner layers
(domain) cannot depend on outer layers (application, infrastructure).

Layer Hierarchy (inside → outside):
    domain → application → infrastructure → interface

Rules:
    1. Domain has NO imports from application, infrastructure, interface
    2. Application may import from domain only
    3. Infrastructure may import from domain and application
    4. Shared Kernel is accessible to all layers

References:
    - IMPL-010: Architecture Tests
    - Hexagonal Architecture (Alistair Cockburn)
    - ADR-003: Code Structure
"""

from __future__ import annotations

from pytest_archon import archrule

# =============================================================================
# Domain Layer Independence Tests
# =============================================================================


class TestDomainLayerIndependence:
    """Tests that domain layer has no dependencies on outer layers."""

    def test_domain_no_application_imports(self) -> None:
        """Domain layer must not import from application layer."""
        (
            archrule("domain_no_application")
            .match("src.work_tracking.domain.*")
            .should_not_import("src.work_tracking.application.*")
            .check("src")
        )

    def test_domain_no_infrastructure_imports(self) -> None:
        """Domain layer must not import from infrastructure layer."""
        (
            archrule("domain_no_infrastructure")
            .match("src.work_tracking.domain.*")
            .should_not_import("src.work_tracking.infrastructure.*")
            .check("src")
        )

    def test_domain_no_interface_imports(self) -> None:
        """Domain layer must not import from interface layer."""
        (
            archrule("domain_no_interface")
            .match("src.work_tracking.domain.*")
            .should_not_import("src.work_tracking.interface.*")
            .check("src")
        )

    def test_domain_may_import_shared_kernel(self) -> None:
        """Domain layer may import from shared kernel."""
        # This is a positive test - we verify shared_kernel imports work
        (
            archrule("domain_uses_shared_kernel")
            .match("src.work_tracking.domain.*")
            .may_import("src.shared_kernel.*")
            .check("src")
        )


# =============================================================================
# Value Object Purity Tests
# =============================================================================


class TestValueObjectPurity:
    """Tests that value objects are pure and independent."""

    def test_value_objects_no_aggregate_imports(self) -> None:
        """Value objects must not import from aggregates."""
        (
            archrule("vo_no_aggregates")
            .match("src.work_tracking.domain.value_objects.*")
            .should_not_import("src.work_tracking.domain.aggregates.*")
            .check("src")
        )

    def test_value_objects_no_service_imports(self) -> None:
        """Value objects must not import from services."""
        (
            archrule("vo_no_services")
            .match("src.work_tracking.domain.value_objects.*")
            .should_not_import("src.work_tracking.domain.services.*")
            .check("src")
        )

    def test_value_objects_no_event_imports(self) -> None:
        """Value objects must not import from events."""
        (
            archrule("vo_no_events")
            .match("src.work_tracking.domain.value_objects.*")
            .should_not_import("src.work_tracking.domain.events.*")
            .check("src")
        )


# =============================================================================
# Aggregate Boundary Tests
# =============================================================================


class TestAggregateBoundaries:
    """Tests that aggregates respect their boundaries."""

    def test_aggregates_may_import_value_objects(self) -> None:
        """Aggregates may import value objects."""
        (
            archrule("aggregates_use_vos")
            .match("src.work_tracking.domain.aggregates.*")
            .may_import("src.work_tracking.domain.value_objects.*")
            .check("src")
        )

    def test_aggregates_may_import_events(self) -> None:
        """Aggregates may import domain events."""
        (
            archrule("aggregates_use_events")
            .match("src.work_tracking.domain.aggregates.*")
            .may_import("src.work_tracking.domain.events.*")
            .check("src")
        )

    def test_aggregates_no_infrastructure_imports(self) -> None:
        """Aggregates must not import from infrastructure."""
        (
            archrule("aggregates_no_infra")
            .match("src.work_tracking.domain.aggregates.*")
            .should_not_import("src.work_tracking.infrastructure.*")
            .check("src")
        )


# =============================================================================
# Service Layer Tests
# =============================================================================


class TestServiceLayerBoundaries:
    """Tests that domain services respect boundaries."""

    def test_services_may_import_value_objects(self) -> None:
        """Domain services may import value objects."""
        (
            archrule("services_use_vos")
            .match("src.work_tracking.domain.services.*")
            .may_import("src.work_tracking.domain.value_objects.*")
            .check("src")
        )

    def test_services_may_import_shared_kernel(self) -> None:
        """Domain services may import from shared kernel."""
        (
            archrule("services_use_shared_kernel")
            .match("src.work_tracking.domain.services.*")
            .may_import("src.shared_kernel.*")
            .check("src")
        )

    def test_services_no_infrastructure_imports(self) -> None:
        """Domain services must not import from infrastructure."""
        (
            archrule("services_no_infra")
            .match("src.work_tracking.domain.services.*")
            .should_not_import("src.work_tracking.infrastructure.*")
            .check("src")
        )


# =============================================================================
# Port Purity Tests
# =============================================================================


class TestPortPurity:
    """Tests that ports (interfaces) are pure abstractions."""

    def test_ports_no_infrastructure_imports(self) -> None:
        """Ports must not import from infrastructure (their implementers)."""
        (
            archrule("ports_no_infra")
            .match("src.work_tracking.domain.ports.*")
            .should_not_import("src.work_tracking.infrastructure.*")
            .check("src")
        )

    def test_ports_may_import_domain(self) -> None:
        """Ports may import domain types for their signatures."""
        (
            archrule("ports_use_domain")
            .match("src.work_tracking.domain.ports.*")
            .may_import("src.work_tracking.domain.value_objects.*")
            .check("src")
        )
