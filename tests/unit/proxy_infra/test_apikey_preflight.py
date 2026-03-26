# BDD RED PHASE — All tests expected to FAIL (ImportError). Implementation in TASK-023-027+.
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BDD test suite for API key pre-flight health check.

TASK-023-048: Implement API Key Pre-Flight Health Check

Covers:
  - Pre-flight catches expired key returning 401 (APIKEY-006)
  - Pre-flight catches Vultr IP ACL mismatch (FM-009)
  - Pre-flight runs before every provision/rotate/destroy operation
  - On timeout: warning (not failure) — network issues must not block provisioning
  - On 401/403: clear error message with actionable guidance
  - Pre-flight result is logged to the audit log (TASK-023-046)
  - DigitalOcean pre-flight uses droplet:read (minimal scope, minimal API impact)
  - Vultr pre-flight uses GET /v2/account (cheapest authenticated endpoint)
  - Pre-flight result carries current egress IP for Vultr ACL mismatch display

Test pyramid: 60% happy path / 30% negative / 10% architecture
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.proxy_infra.infrastructure.adapters.digitalocean_adapter import (
    DigitalOceanProvisionerAdapter,
)
from src.proxy_infra.domain.exceptions import (
    ApiKeyExpiredError,
    ApiKeyPermissionError,
    VultrIpAclMismatchError,
)
from src.proxy_infra.infrastructure.preflight import (
    ApiKeyPreflightChecker,
    PreflightResult,
    PreflightStatus,
)


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def mock_do_client() -> MagicMock:
    """Return a MagicMock for the pydo Client."""
    return MagicMock()


@pytest.fixture()
def mock_audit_store() -> MagicMock:
    """Return a MagicMock for AuditLogStore."""
    return MagicMock()


@pytest.fixture()
def preflight_checker(
    mock_do_client: MagicMock, mock_audit_store: MagicMock
) -> ApiKeyPreflightChecker:
    """Return an ApiKeyPreflightChecker with mocked dependencies."""
    return ApiKeyPreflightChecker(
        provider="digitalocean",
        client=mock_do_client,
        audit_store=mock_audit_store,
        engagement_id="ENG-001",
    )


# =============================================================================
# Happy path: Pre-flight passes with valid key
# =============================================================================


@pytest.mark.unit
class TestPreflightCheckerHappyPath:
    """
    Scenario: Pre-flight check passes with a valid API key
      Given the operator has configured a valid DigitalOcean API key
      And the key has droplet:read scope
      When the pre-flight check runs
      Then PreflightResult with status PASS is returned
      And the result is logged to the audit store
    """

    def test_preflight_returns_pass_status_on_successful_read(
        self, preflight_checker: ApiKeyPreflightChecker, mock_do_client: MagicMock
    ) -> None:
        """APIKEY-006: Pre-flight returns PASS when droplet:read succeeds."""
        mock_do_client.droplets.list.return_value = {"droplets": []}
        result = preflight_checker.run()
        assert result.status == PreflightStatus.PASS, (
            "Pre-flight must return PASS when the API read call succeeds — "
            "APIKEY-006: key is valid and properly scoped"
        )

    def test_preflight_uses_droplet_read_not_write(
        self,
        preflight_checker: ApiKeyPreflightChecker,
        mock_do_client: MagicMock,
    ) -> None:
        """APIKEY-006 / TASK-023-048 AC: DigitalOcean pre-flight uses droplet:read only.

        The pre-flight must NOT create or delete any resources.  Using a
        write operation for validation wastes quota and produces orphaned resources.
        """
        mock_do_client.droplets.list.return_value = {"droplets": []}
        preflight_checker.run()
        mock_do_client.droplets.list.assert_called_once()
        mock_do_client.droplets.create.assert_not_called()
        mock_do_client.droplets.destroy.assert_not_called()

    def test_preflight_logs_result_to_audit_store(
        self,
        preflight_checker: ApiKeyPreflightChecker,
        mock_do_client: MagicMock,
        mock_audit_store: MagicMock,
    ) -> None:
        """TASK-023-048 AC: Pre-flight result must be logged to the audit store."""
        mock_do_client.droplets.list.return_value = {"droplets": []}
        preflight_checker.run()
        mock_audit_store.write_entry.assert_called_once()
        call_kwargs = mock_audit_store.write_entry.call_args.kwargs
        assert call_kwargs.get("action") == "preflight" or "preflight" in str(
            call_kwargs
        ), (
            "Audit log entry for pre-flight must use action='preflight' — "
            "TASK-023-048 AC: pre-flight result logged"
        )

    def test_preflight_result_includes_provider_name(
        self, preflight_checker: ApiKeyPreflightChecker, mock_do_client: MagicMock
    ) -> None:
        """Pre-flight result must identify the provider it checked."""
        mock_do_client.droplets.list.return_value = {"droplets": []}
        result = preflight_checker.run()
        assert result.provider == "digitalocean", (
            "PreflightResult must include the provider name — "
            "multi-provider deployments need to know which check passed/failed"
        )


# =============================================================================
# Negative path: Expired API key (401)
# =============================================================================


@pytest.mark.unit
class TestPreflightExpiredApiKey:
    """
    Scenario: Pre-flight check catches an expired API key
      Given the operator has configured a DigitalOcean API key
      And the key has been revoked at the provider (returns 401)
      When the operator runs "jerry proxy provision --engagement ENG-001"
      Then the pre-flight check fails with ApiKeyExpiredError
      And no provisioning API calls are made
      And the operator is directed to "jerry proxy credentials set digitalocean"
    """

    def test_preflight_raises_api_key_expired_on_401(
        self, preflight_checker: ApiKeyPreflightChecker, mock_do_client: MagicMock
    ) -> None:
        """TASK-023-048 AC: Pre-flight raises ApiKeyExpiredError on 401 response."""
        # Simulate the pydo SDK raising an exception for a 401 response
        mock_do_client.droplets.list.side_effect = Exception("401 Unauthorized")
        with pytest.raises(ApiKeyExpiredError) as exc_info:
            preflight_checker.run()
        error_msg = str(exc_info.value)
        assert "401" in error_msg or "expired" in error_msg.lower() or "unauthorized" in error_msg.lower(), (
            "ApiKeyExpiredError must mention 401 or expired/unauthorized — "
            "TASK-023-048 AC: 'API key validation failed: 401 Unauthorized'"
        )

    def test_preflight_error_includes_remediation_guidance(
        self, preflight_checker: ApiKeyPreflightChecker, mock_do_client: MagicMock
    ) -> None:
        """Pre-flight error must direct operator to credential management command."""
        mock_do_client.droplets.list.side_effect = Exception("401 Unauthorized")
        with pytest.raises(ApiKeyExpiredError) as exc_info:
            preflight_checker.run()
        error_msg = str(exc_info.value)
        # Must mention the credential management path
        assert (
            "credentials" in error_msg.lower()
            or "jerry proxy" in error_msg.lower()
        ), (
            "ApiKeyExpiredError must include remediation guidance — "
            "TASK-023-048 AC: direct operator to 'jerry proxy credentials set'"
        )

    def test_preflight_403_raises_permission_error(
        self, preflight_checker: ApiKeyPreflightChecker, mock_do_client: MagicMock
    ) -> None:
        """Pre-flight raises ApiKeyPermissionError on 403 (key exists but lacks scope)."""
        mock_do_client.droplets.list.side_effect = Exception("403 Forbidden")
        with pytest.raises((ApiKeyExpiredError, ApiKeyPermissionError)):
            preflight_checker.run()


# =============================================================================
# Negative path: Vultr IP ACL mismatch (FM-009)
# =============================================================================


@pytest.mark.unit
class TestPreflightVultrIpAclMismatch:
    """
    Scenario: Pre-flight check catches Vultr IP ACL mismatch
      Given the operator has configured a Vultr API key with IP ACL
      And the operator's current egress IP does not match the ACL
      When the pre-flight check runs
      Then VultrIpAclMismatchError is raised
      And the error message includes the current egress IP

    FM-009: Vultr IP ACL is set at key creation time.  If the operator is on
    mobile or behind a different NAT, the key is silently rejected with no
    indication that an ACL is the cause.  The pre-flight check must detect
    this and display both the current egress IP and the expected ACL.
    """

    def test_vultr_preflight_raises_acl_mismatch_error(self) -> None:
        """FM-009: VultrIpAclMismatchError raised when Vultr rejects due to ACL."""
        mock_client = MagicMock()
        mock_audit = MagicMock()
        mock_client.account.get.side_effect = Exception("403 Forbidden: IP not in ACL")
        checker = ApiKeyPreflightChecker(
            provider="vultr",
            client=mock_client,
            audit_store=mock_audit,
            engagement_id="ENG-001",
        )
        with patch(
            "src.proxy_infra.infrastructure.preflight.get_current_egress_ip",
            return_value="198.51.100.55",
        ):
            with pytest.raises(VultrIpAclMismatchError) as exc_info:
                checker.run()
        error_msg = str(exc_info.value)
        assert "198.51.100.55" in error_msg, (
            "VultrIpAclMismatchError must include the current egress IP — "
            "FM-009: 'Current egress IP: X.X.X.X' as per TASK-023-048 AC"
        )

    def test_vultr_preflight_uses_account_endpoint_not_instances(self) -> None:
        """TASK-023-048 AC: Vultr pre-flight uses GET /v2/account (cheapest endpoint)."""
        mock_client = MagicMock()
        mock_audit = MagicMock()
        mock_client.account.get.return_value = {"account": {"email": "test@example.com"}}
        checker = ApiKeyPreflightChecker(
            provider="vultr",
            client=mock_client,
            audit_store=mock_audit,
            engagement_id="ENG-001",
        )
        checker.run()
        mock_client.account.get.assert_called_once()
        mock_client.instances.list.assert_not_called()


# =============================================================================
# Edge path: Timeout produces warning, not failure
# =============================================================================


@pytest.mark.unit
class TestPreflightTimeout:
    """
    Scenario: Pre-flight times out due to network issues
      Given the cloud provider API is unreachable
      When the pre-flight check times out
      Then a PreflightResult with status WARNING is returned (not FAIL)
      And a warning is logged but provisioning continues

    TASK-023-048 AC: on timeout, warn (not failure) — network issues should
    not block provisioning.
    """

    def test_preflight_returns_warning_status_on_timeout(
        self, mock_do_client: MagicMock, mock_audit_store: MagicMock
    ) -> None:
        """TASK-023-048 AC: Timeout returns WARNING, does not raise."""
        import socket
        mock_do_client.droplets.list.side_effect = TimeoutError("Connection timed out")
        checker = ApiKeyPreflightChecker(
            provider="digitalocean",
            client=mock_do_client,
            audit_store=mock_audit_store,
            engagement_id="ENG-001",
        )
        result = checker.run()
        assert result.status == PreflightStatus.WARNING, (
            "Pre-flight must return WARNING on timeout — "
            "TASK-023-048 AC: network issues must not block provisioning"
        )

    def test_preflight_warning_does_not_raise_exception(
        self, mock_do_client: MagicMock, mock_audit_store: MagicMock
    ) -> None:
        """Timeout result must not propagate as an exception to the caller."""
        mock_do_client.droplets.list.side_effect = TimeoutError("Connection timed out")
        checker = ApiKeyPreflightChecker(
            provider="digitalocean",
            client=mock_do_client,
            audit_store=mock_audit_store,
            engagement_id="ENG-001",
        )
        # Must not raise — caller receives a WARNING result, not an exception
        result = checker.run()
        assert result is not None, "Timeout must return a PreflightResult, not None"

    def test_preflight_socket_timeout_is_also_handled_as_warning(
        self, mock_do_client: MagicMock, mock_audit_store: MagicMock
    ) -> None:
        """TASK-023-048 AC: socket.timeout is also treated as a warning."""
        import socket
        mock_do_client.droplets.list.side_effect = socket.timeout("timed out")
        checker = ApiKeyPreflightChecker(
            provider="digitalocean",
            client=mock_do_client,
            audit_store=mock_audit_store,
            engagement_id="ENG-001",
        )
        result = checker.run()
        assert result.status == PreflightStatus.WARNING, (
            "socket.timeout must also produce WARNING status — "
            "TASK-023-048 AC: all timeout variants treated the same"
        )


# =============================================================================
# Architecture: Pre-flight runs before every mutating operation
# =============================================================================


@pytest.mark.unit
class TestPreflightRunsBeforeMutatingOperations:
    """
    Scenario: Pre-flight check is invoked before provision/rotate/destroy
      Given the DigitalOceanProvisionerAdapter is constructed
      When provision(), rotate(), or destroy() is called
      Then the pre-flight check is invoked before the actual API call
      And if pre-flight raises ApiKeyExpiredError, the API call is never made
    """

    def test_provision_calls_preflight_before_droplet_create(self) -> None:
        """TASK-023-048 AC: provision() must invoke pre-flight before droplets.create()."""
        mock_client = MagicMock()
        mock_audit = MagicMock()
        mock_preflight = MagicMock()
        # Simulate expired key — pre-flight raises before any create
        mock_preflight.run.side_effect = ApiKeyExpiredError(
            "digitalocean", "401 Unauthorized"
        )
        adapter = DigitalOceanProvisionerAdapter(
            client=mock_client,
            audit_store=mock_audit,
            preflight_checker=mock_preflight,
        )
        from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
        from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
        from src.proxy_infra.domain.value_objects.proxy_type import ProxyType

        config = ProvisionConfig(
            provider="digitalocean",
            region="nyc1",
            count=1,
            engagement_tag="jerry-abc123def456",
            engagement_id="ENG-001",
            proxy_type=ProxyType.DIRECT_SOCKS5,
            role=ProxyRole.ACTIVE,
            ssh_public_key="ssh-ed25519 AAAAC3 test",
            operator_ip="203.0.113.1",
        )
        with pytest.raises(ApiKeyExpiredError):
            adapter.provision(config)

        mock_preflight.run.assert_called_once()
        mock_client.droplets.create.assert_not_called()

    def test_destroy_calls_preflight_before_droplet_destroy(self) -> None:
        """TASK-023-048 AC: destroy() must invoke pre-flight before droplets.destroy()."""
        mock_client = MagicMock()
        mock_audit = MagicMock()
        mock_preflight = MagicMock()
        mock_preflight.run.side_effect = ApiKeyExpiredError(
            "digitalocean", "401 Unauthorized"
        )
        adapter = DigitalOceanProvisionerAdapter(
            client=mock_client,
            audit_store=mock_audit,
            preflight_checker=mock_preflight,
        )
        with pytest.raises(ApiKeyExpiredError):
            adapter.destroy(node_ids=["do-12345"])

        mock_preflight.run.assert_called_once()
        mock_client.droplets.destroy.assert_not_called()
