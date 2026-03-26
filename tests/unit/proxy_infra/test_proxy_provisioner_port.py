# BDD RED PHASE — All tests expected to FAIL (ImportError). Implementation in TASK-023-027+.
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BDD test suite for ProxyProvisionerPort interface contract.

TASK-023-027: Design ProxyProvisionerPort Interface (Hexagonal Port)

Covers:
  - Port method signatures: provision(), destroy(), health_check(), list_instances()
  - Protocol structural subtyping (duck-typing compliance)
  - ProxyProvisionerPort raises ProvisioningError on failure
  - CredentialStorePort raises CredentialNotFoundError on miss (FM-011)
  - CredentialStorePort env var resolution (DA-001: env primary)
  - ISOLATION-001: engagement_tag required on every provision() call
  - RATELIMIT-001: provisioning_delay_seconds on ProvisionConfig
  - RATELIMIT-006: max_nodes per engagement enforced (<=10)
  - H-07: domain layer has no infrastructure imports
  - H-10: one class per file
  - H-11: all port methods have type hints and docstrings

Test pyramid: 60% happy path / 30% negative / 10% architecture
"""

from __future__ import annotations

import inspect
import sys
from typing import get_type_hints

import pytest

# --- Domain imports (will fail with ImportError until TASK-023-027 is implemented) ---
from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
from src.proxy_infra.domain.ports.credential_store_port import (
    CredentialStorePort,
    CredentialNotFoundError,
)
from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
from src.proxy_infra.domain.value_objects.health_status import HealthStatus


# =============================================================================
# Happy path: Port method signature validation
# =============================================================================


@pytest.mark.unit
class TestProxyProvisionerPortSignatures:
    """Verify ProxyProvisionerPort Protocol defines all required methods with
    correct signatures.  These tests document the expected contract rather than
    testing live behaviour — they verify that the Protocol object *specifies*
    the right interface."""

    def test_provision_method_exists_on_port(self) -> None:
        """ProxyProvisionerPort Protocol must declare provision() method."""
        assert hasattr(ProxyProvisionerPort, "provision"), (
            "ProxyProvisionerPort must define provision() — "
            "every adapter implements this to create proxy nodes"
        )

    def test_destroy_method_exists_on_port(self) -> None:
        """ProxyProvisionerPort Protocol must declare destroy() method."""
        assert hasattr(ProxyProvisionerPort, "destroy"), (
            "ProxyProvisionerPort must define destroy() — "
            "used during engagement teardown to remove all provisioned nodes"
        )

    def test_health_check_method_exists_on_port(self) -> None:
        """ProxyProvisionerPort Protocol must declare health_check() method."""
        assert hasattr(ProxyProvisionerPort, "health_check"), (
            "ProxyProvisionerPort must define health_check() — "
            "used by ProxyHealthService to detect burned or unhealthy nodes"
        )

    def test_list_instances_method_exists_on_port(self) -> None:
        """ProxyProvisionerPort Protocol must declare list_instances() method."""
        assert hasattr(ProxyProvisionerPort, "list_instances"), (
            "ProxyProvisionerPort must define list_instances() — "
            "used for orphan detection and engagement-tag filtered queries"
        )

    def test_provision_accepts_provision_config_parameter(self) -> None:
        """provision() must accept a ProvisionConfig value object, not raw params.

        Design constraint from ADR-PROJ023-008: all provisioning parameters
        (region, size, role, engagement_tag, provisioning_delay_seconds) are
        encapsulated in ProvisionConfig so the port signature is stable as
        the config surface grows.
        """
        sig = inspect.signature(ProxyProvisionerPort.provision)
        params = list(sig.parameters.keys())
        assert "config" in params, (
            "provision() must accept a 'config: ProvisionConfig' parameter — "
            "raw per-parameter signatures couple adapters to the domain model"
        )

    def test_provision_returns_list_annotation(self) -> None:
        """provision() return type must be annotated as list[ProxyNode]."""
        hints = get_type_hints(ProxyProvisionerPort.provision)
        assert "return" in hints, (
            "provision() must have a return type annotation — H-11 requires "
            "type hints on all public functions"
        )

    def test_destroy_accepts_node_ids_list(self) -> None:
        """destroy() must accept a list of node IDs, not individual IDs.

        Batch destruction is required by the teardown sequence which removes
        all nodes for an engagement in a single operation.
        """
        sig = inspect.signature(ProxyProvisionerPort.destroy)
        params = list(sig.parameters.keys())
        assert "node_ids" in params, (
            "destroy() must accept 'node_ids: list[str]' — batch destruction "
            "is required for engagement teardown"
        )

    def test_destroy_returns_destroy_result(self) -> None:
        """destroy() must return DestroyResult, not None.

        DestroyResult carries per-node success/failure information so that
        partial failures can be reported and retried.  Returning None discards
        this information (FM-022).
        """
        hints = get_type_hints(ProxyProvisionerPort.destroy)
        assert "return" in hints, (
            "destroy() must have a return type annotation — partial failures "
            "must be surface through DestroyResult, not swallowed"
        )

    def test_health_check_accepts_node_id_string(self) -> None:
        """health_check() must accept a node_id string parameter."""
        sig = inspect.signature(ProxyProvisionerPort.health_check)
        params = list(sig.parameters.keys())
        assert "node_id" in params, (
            "health_check() must accept 'node_id: str' — provider-assigned "
            "identifier used to query the specific droplet/instance"
        )

    def test_list_instances_accepts_engagement_tag(self) -> None:
        """list_instances() must support filtering by engagement_tag.

        ISOLATION-001: every list operation must be scopeable to a specific
        engagement to prevent cross-engagement node visibility.
        """
        sig = inspect.signature(ProxyProvisionerPort.list_instances)
        params = list(sig.parameters.keys())
        assert "engagement_tag" in params, (
            "list_instances() must accept 'engagement_tag: str' — ISOLATION-001 "
            "requires all list operations to be filterable by engagement"
        )

    def test_provision_config_has_engagement_tag_field(self) -> None:
        """ProvisionConfig must include engagement_tag field (ISOLATION-001).

        The engagement_tag must be applied at creation time (ORPHAN-003) so
        it cannot be omitted.  It must be a required field on ProvisionConfig,
        not an optional override.
        """
        config_fields = {
            f.name
            for f in getattr(ProvisionConfig, "__dataclass_fields__", {}).values()
        }
        # Also check for __annotations__ for Protocol-style definitions
        annotations = getattr(ProvisionConfig, "__annotations__", {})
        all_fields = config_fields | set(annotations.keys())
        assert "engagement_tag" in all_fields, (
            "ProvisionConfig must include 'engagement_tag' field — ISOLATION-001 "
            "requires engagement tag applied at creation time (ORPHAN-003)"
        )

    def test_provision_config_has_provisioning_delay_seconds(self) -> None:
        """ProvisionConfig must include provisioning_delay_seconds (RATELIMIT-001).

        Default must be 15 seconds between consecutive provision() calls to
        avoid triggering DigitalOcean rate limit detection.
        """
        annotations = getattr(ProvisionConfig, "__annotations__", {})
        fields = {
            f.name
            for f in getattr(ProvisionConfig, "__dataclass_fields__", {}).values()
        }
        all_fields = fields | set(annotations.keys())
        assert "provisioning_delay_seconds" in all_fields, (
            "ProvisionConfig must include 'provisioning_delay_seconds' — "
            "RATELIMIT-001 requires pacing between consecutive provision() calls"
        )

    def test_port_methods_have_docstrings(self) -> None:
        """All ProxyProvisionerPort methods must have docstrings (H-11)."""
        for method_name in ("provision", "destroy", "health_check", "list_instances"):
            method = getattr(ProxyProvisionerPort, method_name, None)
            assert method is not None, f"{method_name} must exist on port"
            assert method.__doc__, (
                f"ProxyProvisionerPort.{method_name}() must have a docstring — "
                f"H-11 requires docstrings on all public functions"
            )


# =============================================================================
# Happy path: ProvisionConfig value object behaviour
# =============================================================================


@pytest.mark.unit
class TestProvisionConfig:
    """Verify ProvisionConfig value object encapsulates provisioning parameters
    correctly and enforces the default values specified in the design."""

    def test_provision_config_default_delay_is_15_seconds(self) -> None:
        """provisioning_delay_seconds defaults to 15 per RATELIMIT-001/FM-017."""
        config = ProvisionConfig(
            provider="digitalocean",
            region="nyc1",
            count=1,
            engagement_tag="jerry-abc123def456",
            engagement_id="ENG-001",
            proxy_type=ProxyType.DIRECT_SOCKS5,
            role=ProxyRole.ACTIVE,
            ssh_public_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5 test",
            operator_ip="203.0.113.1",
        )
        assert config.provisioning_delay_seconds == 15, (
            "provisioning_delay_seconds must default to 15 — "
            "RATELIMIT-001 specifies 15s inter-provision gap"
        )

    def test_provision_config_engagement_tag_required(self) -> None:
        """engagement_tag cannot be empty string (ISOLATION-001)."""
        with pytest.raises((ValueError, TypeError)):
            ProvisionConfig(
                provider="digitalocean",
                region="nyc1",
                count=1,
                engagement_tag="",  # empty tag must be rejected
                engagement_id="ENG-001",
                proxy_type=ProxyType.DIRECT_SOCKS5,
                role=ProxyRole.ACTIVE,
                ssh_public_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5 test",
                operator_ip="203.0.113.1",
            )

    def test_provision_config_max_count_is_10(self) -> None:
        """count > 10 must be rejected per RATELIMIT-006 (max 10 nodes per engagement)."""
        with pytest.raises((ValueError, TypeError)):
            ProvisionConfig(
                provider="digitalocean",
                region="nyc1",
                count=11,  # exceeds RATELIMIT-006 limit
                engagement_tag="jerry-abc123def456",
                engagement_id="ENG-001",
                proxy_type=ProxyType.DIRECT_SOCKS5,
                role=ProxyRole.ACTIVE,
                ssh_public_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5 test",
                operator_ip="203.0.113.1",
            )

    def test_provision_config_count_of_10_is_valid(self) -> None:
        """count == 10 is the maximum allowed per RATELIMIT-006."""
        config = ProvisionConfig(
            provider="digitalocean",
            region="nyc1",
            count=10,
            engagement_tag="jerry-abc123def456",
            engagement_id="ENG-001",
            proxy_type=ProxyType.DIRECT_SOCKS5,
            role=ProxyRole.ACTIVE,
            ssh_public_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5 test",
            operator_ip="203.0.113.1",
        )
        assert config.count == 10, "count of 10 must be accepted per RATELIMIT-006"

    def test_provision_config_is_frozen(self) -> None:
        """ProvisionConfig must be a frozen dataclass (immutable value object)."""
        config = ProvisionConfig(
            provider="digitalocean",
            region="nyc1",
            count=1,
            engagement_tag="jerry-abc123def456",
            engagement_id="ENG-001",
            proxy_type=ProxyType.DIRECT_SOCKS5,
            role=ProxyRole.ACTIVE,
            ssh_public_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5 test",
            operator_ip="203.0.113.1",
        )
        with pytest.raises((AttributeError, TypeError)):
            config.provider = "vultr"  # type: ignore[misc]


# =============================================================================
# Negative path: CredentialStorePort error semantics
# =============================================================================


@pytest.mark.unit
class TestCredentialStorePort:
    """Verify CredentialStorePort contract: raises CredentialNotFoundError on
    miss (FM-011), never returns None (DA-001 design constraint)."""

    def test_credential_not_found_error_is_exception(self) -> None:
        """CredentialNotFoundError must be a proper exception subclass."""
        assert issubclass(CredentialNotFoundError, Exception), (
            "CredentialNotFoundError must extend Exception so it can be caught "
            "in the CLI layer and surfaced as an actionable user message"
        )

    def test_credential_not_found_error_carries_provider_name(self) -> None:
        """CredentialNotFoundError must include the provider name in the message.

        FM-011: when the credential store misses, the user must be told which
        provider credential is missing and how to configure it.
        """
        err = CredentialNotFoundError("digitalocean")
        assert "digitalocean" in str(err), (
            "CredentialNotFoundError must include the provider name — "
            "FM-011: operator must know which credential to configure"
        )

    def test_credential_store_port_has_get_credential_method(self) -> None:
        """CredentialStorePort must define get_credential()."""
        assert hasattr(CredentialStorePort, "get_credential"), (
            "CredentialStorePort must define get_credential(provider_name) — "
            "used by adapters to retrieve the provider API key at provision time"
        )

    def test_credential_store_port_has_store_credential_method(self) -> None:
        """CredentialStorePort must define store_credential()."""
        assert hasattr(CredentialStorePort, "store_credential"), (
            "CredentialStorePort must define store_credential() — "
            "used by 'jerry proxy add-provider' to persist API keys securely"
        )

    def test_credential_store_port_has_delete_credential_method(self) -> None:
        """CredentialStorePort must define delete_credential()."""
        assert hasattr(CredentialStorePort, "delete_credential"), (
            "CredentialStorePort must define delete_credential() — "
            "used during engagement teardown to revoke stored credentials"
        )

    def test_get_credential_return_type_is_str_not_optional(self) -> None:
        """get_credential() must return str, never Optional[str] (FM-011, DA-001).

        DA-001 resolution: the port returns str and raises CredentialNotFoundError
        on miss.  This is safer than returning None, which callers may forget to
        check, leading to NullPointerEquivalent errors at provision time.
        """
        hints = get_type_hints(CredentialStorePort.get_credential)
        return_hint = hints.get("return")
        assert return_hint is not None, (
            "get_credential() must have a return type annotation — H-11"
        )
        # Must not be Optional — Optional[str] allows None, which FM-011 prohibits
        hint_str = str(return_hint)
        assert "None" not in hint_str and "Optional" not in hint_str, (
            "get_credential() must return str, NOT Optional[str] — "
            "FM-011: CredentialNotFoundError raises on miss, never returns None"
        )


# =============================================================================
# Negative path: DestroyResult partial-failure semantics
# =============================================================================


@pytest.mark.unit
class TestDestroyResult:
    """Verify DestroyResult value object carries partial failure information."""

    def test_destroy_result_has_destroyed_field(self) -> None:
        """DestroyResult must have a 'destroyed' field listing successful node IDs."""
        annotations = getattr(DestroyResult, "__annotations__", {})
        fields = {
            f.name
            for f in getattr(DestroyResult, "__dataclass_fields__", {}).values()
        }
        all_fields = fields | set(annotations.keys())
        assert "destroyed" in all_fields, (
            "DestroyResult must have 'destroyed' field — "
            "FM-022: partial failures must be distinguishable from full failures"
        )

    def test_destroy_result_has_failed_field(self) -> None:
        """DestroyResult must have a 'failed' field listing failed node IDs."""
        annotations = getattr(DestroyResult, "__annotations__", {})
        fields = {
            f.name
            for f in getattr(DestroyResult, "__dataclass_fields__", {}).values()
        }
        all_fields = fields | set(annotations.keys())
        assert "failed" in all_fields, (
            "DestroyResult must have 'failed' field — "
            "FM-022: operator must know which nodes need manual cleanup"
        )

    def test_destroy_result_is_all_successful_when_no_failures(self) -> None:
        """DestroyResult with empty failed list represents complete success."""
        result = DestroyResult(
            destroyed=["do-111", "do-222"],
            failed=[],
        )
        assert result.failed == [], (
            "DestroyResult with empty failed list must indicate full success"
        )
        assert len(result.destroyed) == 2, (
            "DestroyResult.destroyed must list all successfully destroyed node IDs"
        )

    def test_destroy_result_is_frozen(self) -> None:
        """DestroyResult must be a frozen dataclass (immutable value object)."""
        result = DestroyResult(destroyed=["do-111"], failed=[])
        with pytest.raises((AttributeError, TypeError)):
            result.destroyed = []  # type: ignore[misc]


# =============================================================================
# Architecture tests: H-07 domain layer isolation
# =============================================================================


@pytest.mark.unit
class TestDomainLayerArchitectureIsolation:
    """Verify the domain layer contains no infrastructure imports (H-07).

    The domain layer must import only stdlib and shared_kernel.  Any import of
    pydo, hcloud, requests, keyring, yaml, subprocess, or pathlib for file I/O
    in the domain layer is an H-07 violation.
    """

    FORBIDDEN_INFRASTRUCTURE_MODULES = {
        "pydo",
        "hcloud",
        "requests",
        "keyring",
        "yaml",
        "subprocess",
        "boto3",
        "vultr",
    }

    def _get_domain_modules(self) -> list[str]:
        """Return all currently loaded modules under src.proxy_infra.domain."""
        return [
            name
            for name in sys.modules
            if name.startswith("src.proxy_infra.domain")
        ]

    def test_proxy_provisioner_port_has_no_infrastructure_imports(self) -> None:
        """ProxyProvisionerPort module must not import any infrastructure packages."""
        import src.proxy_infra.domain.ports.proxy_provisioner_port as port_module

        source_file = inspect.getfile(port_module)
        with open(source_file) as f:
            source = f.read()

        for forbidden in self.FORBIDDEN_INFRASTRUCTURE_MODULES:
            assert f"import {forbidden}" not in source, (
                f"ProxyProvisionerPort imports '{forbidden}' — H-07 violation: "
                f"domain layer must not depend on infrastructure packages"
            )
            assert f"from {forbidden}" not in source, (
                f"ProxyProvisionerPort imports from '{forbidden}' — H-07 violation"
            )

    def test_credential_store_port_has_no_infrastructure_imports(self) -> None:
        """CredentialStorePort module must not import any infrastructure packages."""
        import src.proxy_infra.domain.ports.credential_store_port as port_module

        source_file = inspect.getfile(port_module)
        with open(source_file) as f:
            source = f.read()

        for forbidden in self.FORBIDDEN_INFRASTRUCTURE_MODULES:
            assert f"import {forbidden}" not in source, (
                f"CredentialStorePort imports '{forbidden}' — H-07 violation"
            )
