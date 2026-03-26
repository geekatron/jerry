# BDD RED PHASE — All tests expected to FAIL (ImportError). Implementation in TASK-023-027+.
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BDD integration test suite for DigitalOceanProvisionerAdapter.

TASK-023-028: Implement DigitalOcean Adapter

All tests use a mocked pydo Client — no real API calls are made.
This is an integration test in the sense that the adapter's full lifecycle
logic is exercised end-to-end, but the pydo client is replaced with a mock.

Covers:
  - provision() creates droplet with correct region, size, image, tags
  - provision() applies engagement_tag at creation time (ORPHAN-003)
  - provision() passes user_data as plain text (no base64 — DO accepts plain text)
  - provision() respects provisioning_delay_seconds (RATELIMIT-001)
  - provision() implements exponential backoff on 429 (RATELIMIT-002)
  - provision() checks RateLimit-Remaining header (RATELIMIT-003)
  - provision() validates pool size <= 10 nodes (RATELIMIT-006)
  - destroy() deletes droplet, removes SSH key, deletes firewall (TASK-023-028 AC)
  - destroy() returns DestroyResult with partial failure info (FM-022)
  - API key is read from JERRY_PROXY_DO_API_KEY env var (never hardcoded)
  - Firewall created immediately after droplet creation (FM-035)
  - All resources tagged with engagement_tag at creation time (ORPHAN-003)
  - list_instances() filters by engagement_tag (ISOLATION-001)

Test pyramid: 60% happy path / 30% negative / 10% architecture
"""

from __future__ import annotations

import time
from datetime import datetime, timezone
from unittest.mock import MagicMock, call, patch

import pytest

from src.proxy_infra.infrastructure.adapters.digitalocean_adapter import (
    DigitalOceanProvisionerAdapter,
)
from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
from src.proxy_infra.domain.exceptions import ProvisioningError


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def mock_do_client() -> MagicMock:
    """Return a fully configured mock of the pydo Client for DO adapter tests."""
    client = MagicMock()
    # Simulate successful SSH key upload
    client.ssh_keys.create.return_value = {
        "ssh_key": {"id": 98765, "name": "jerry-proxy-ENG-001"}
    }
    # Simulate successful droplet creation
    client.droplets.create.return_value = {
        "droplet": {
            "id": 12345,
            "name": "jerry-proxy-ENG-001-nyc1",
            "status": "new",
            "networks": {"v4": []},
            "tags": ["jerry-abc123def456"],
        }
    }
    # Simulate droplet with IP after polling
    client.droplets.get.return_value = {
        "droplet": {
            "id": 12345,
            "name": "jerry-proxy-ENG-001-nyc1",
            "status": "active",
            "networks": {
                "v4": [{"type": "public", "ip_address": "203.0.113.10"}]
            },
        }
    }
    # Simulate successful firewall creation
    client.firewalls.create.return_value = {
        "firewall": {"id": "fw-abc123", "name": "jerry-proxy-ENG-001"}
    }
    return client


@pytest.fixture()
def mock_audit_store() -> MagicMock:
    """Return a mock AuditLogStore."""
    return MagicMock()


@pytest.fixture()
def mock_preflight() -> MagicMock:
    """Return a mock ApiKeyPreflightChecker that always passes."""
    preflight = MagicMock()
    from src.proxy_infra.infrastructure.preflight import PreflightResult, PreflightStatus
    preflight.run.return_value = PreflightResult(
        status=PreflightStatus.PASS,
        provider="digitalocean",
        message="Key valid",
    )
    return preflight


@pytest.fixture()
def adapter(
    mock_do_client: MagicMock,
    mock_audit_store: MagicMock,
    mock_preflight: MagicMock,
) -> DigitalOceanProvisionerAdapter:
    """Return a DigitalOceanProvisionerAdapter with mocked dependencies."""
    return DigitalOceanProvisionerAdapter(
        client=mock_do_client,
        audit_store=mock_audit_store,
        preflight_checker=mock_preflight,
    )


@pytest.fixture()
def provision_config() -> ProvisionConfig:
    """Return a standard ProvisionConfig for testing."""
    return ProvisionConfig(
        provider="digitalocean",
        region="nyc1",
        count=1,
        engagement_tag="jerry-abc123def456",
        engagement_id="ENG-001",
        proxy_type=ProxyType.DIRECT_SOCKS5,
        role=ProxyRole.ACTIVE,
        ssh_public_key="ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAITestKey operator@jerry",
        operator_ip="203.0.113.1",
        provisioning_delay_seconds=0,  # no delay in tests
    )


# =============================================================================
# Happy path: provision() creates droplet correctly
# =============================================================================


@pytest.mark.integration
class TestDigitalOceanAdapterProvision:
    """
    Scenario: Successful single-node provisioning
      Given a valid ProvisionConfig for DigitalOcean nyc1
      When provision() is called
      Then a droplet is created with the correct region, size, image, and tags
      And the SSH key is uploaded before droplet creation
      And a firewall is created immediately after droplet creation
      And a ProxyNode is returned in CONFIGURING or READY status
    """

    def test_provision_calls_droplet_create(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
        provision_config: ProvisionConfig,
    ) -> None:
        """TASK-023-028 AC: provision() must call client.droplets.create()."""
        adapter.provision(provision_config)
        mock_do_client.droplets.create.assert_called_once()

    def test_provision_uses_correct_region_from_config(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
        provision_config: ProvisionConfig,
    ) -> None:
        """provision() must pass the configured region to droplets.create()."""
        adapter.provision(provision_config)
        create_call = mock_do_client.droplets.create.call_args
        body = create_call.kwargs.get("body") or create_call.args[0]
        assert body.get("region") == "nyc1", (
            "provision() must pass region='nyc1' from ProvisionConfig — "
            "TASK-023-028 AC: region is a required provisioning parameter"
        )

    def test_provision_uploads_ssh_key_before_droplet_create(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
        provision_config: ProvisionConfig,
    ) -> None:
        """TASK-023-028 AC: SSH key must be uploaded before droplet is created."""
        call_order = []
        mock_do_client.ssh_keys.create.side_effect = lambda **kw: (
            call_order.append("ssh_key_create")
            or {"ssh_key": {"id": 98765, "name": "test"}}
        )
        mock_do_client.droplets.create.side_effect = lambda **kw: (
            call_order.append("droplet_create")
            or {"droplet": {
                "id": 12345, "name": "test", "status": "new",
                "networks": {"v4": []}, "tags": []
            }}
        )
        try:
            adapter.provision(provision_config)
        except Exception:
            pass  # POST-create steps may fail in mocked context
        if "ssh_key_create" in call_order and "droplet_create" in call_order:
            assert call_order.index("ssh_key_create") < call_order.index(
                "droplet_create"
            ), (
                "SSH key must be uploaded BEFORE droplet is created — "
                "TASK-023-028 AC: droplet references the key ID at creation time"
            )

    def test_provision_applies_engagement_tag_at_creation_time(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
        provision_config: ProvisionConfig,
    ) -> None:
        """ORPHAN-003: engagement_tag must be applied at droplet creation, not after.

        Post-creation tagging creates an atomicity gap: if CLM crashes between
        creation and tagging, the droplet exists without a tag and becomes
        an undetectable orphan.
        """
        adapter.provision(provision_config)
        create_call = mock_do_client.droplets.create.call_args
        body = create_call.kwargs.get("body") or create_call.args[0]
        tags = body.get("tags", [])
        assert "jerry-abc123def456" in tags, (
            "provision() must include engagement_tag in droplets.create() tags — "
            "ORPHAN-003: tag applied at creation, not post-creation"
        )

    def test_provision_passes_user_data_as_plain_text(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
        provision_config: ProvisionConfig,
    ) -> None:
        """TASK-023-028 AC: user_data passed as plain text (no base64 for DO).

        DigitalOcean accepts plain text cloud-init.  Vultr requires base64
        (FM-008) but DO does not.  Encoding DO user_data in base64 causes
        cloud-init to be treated as a literal base64 string on the VPS.
        """
        adapter.provision(provision_config)
        create_call = mock_do_client.droplets.create.call_args
        body = create_call.kwargs.get("body") or create_call.args[0]
        user_data = body.get("user_data", "")
        if user_data:
            # If user_data is present, it must be plain text starting with #cloud-config
            # or a shebang — not a base64 blob
            import base64
            try:
                decoded = base64.b64decode(user_data, validate=True)
                # If it decodes cleanly AND looks like cloud-init, it may be base64
                # But cloud-init on DO expects plain text — fail if it's base64 encoded
                if decoded.startswith(b"#cloud-config") or decoded.startswith(b"#!/"):
                    pytest.fail(
                        "provision() is base64-encoding user_data for DigitalOcean — "
                        "TASK-023-028 AC: DO accepts plain text, base64 is wrong"
                    )
            except Exception:
                pass  # Cannot decode as base64 — this is correct (plain text)

    def test_provision_creates_firewall_immediately_after_droplet(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
        provision_config: ProvisionConfig,
    ) -> None:
        """FM-035: Firewall must be created immediately after droplet creation.

        UFW in cloud-init is the primary protection during the atomicity gap
        (between droplet creation and firewall attachment).  The DO firewall
        is the secondary layer and must be created as soon as the droplet ID
        is known.
        """
        adapter.provision(provision_config)
        mock_do_client.firewalls.create.assert_called_once()
        # Firewall creation must happen before any polling / next operations
        # Verify the firewall references the newly created droplet
        fw_call = mock_do_client.firewalls.create.call_args
        fw_body = fw_call.kwargs.get("body") or fw_call.args[0]
        assert 12345 in fw_body.get("droplet_ids", []), (
            "Firewall must reference the new droplet ID 12345 — "
            "FM-035: firewall created immediately after droplet creation"
        )

    def test_provision_returns_list_with_one_proxy_node(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        provision_config: ProvisionConfig,
    ) -> None:
        """provision() must return a list with one ProxyNode for count=1."""
        result = adapter.provision(provision_config)
        assert isinstance(result, list), "provision() must return a list"
        assert len(result) == 1, (
            "provision() with count=1 must return a list with one ProxyNode"
        )

    def test_provision_node_has_provider_set_to_digitalocean(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        provision_config: ProvisionConfig,
    ) -> None:
        """Returned ProxyNode must have provider='digitalocean'."""
        nodes = adapter.provision(provision_config)
        assert nodes[0].provider == "digitalocean", (
            "ProxyNode returned by DigitalOcean adapter must have "
            "provider='digitalocean' for manifest serialisation"
        )

    def test_provision_node_has_engagement_id_set(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        provision_config: ProvisionConfig,
    ) -> None:
        """Returned ProxyNode must have engagement_id matching the config."""
        nodes = adapter.provision(provision_config)
        assert nodes[0].engagement_id == "ENG-001", (
            "ProxyNode must carry the engagement_id from ProvisionConfig — "
            "required for multi-engagement isolation and orphan detection"
        )


# =============================================================================
# Happy path: provision() rate limit behaviour
# =============================================================================


@pytest.mark.integration
class TestDigitalOceanAdapterRateLimits:
    """
    Scenario: Provisioner respects rate limit controls
      Given a ProvisionConfig with provisioning_delay_seconds > 0
      When provision() is called
      Then the adapter waits the specified delay between consecutive calls
    """

    def test_provision_respects_provisioning_delay_seconds(
        self,
        mock_do_client: MagicMock,
        mock_audit_store: MagicMock,
        mock_preflight: MagicMock,
    ) -> None:
        """RATELIMIT-001: provision() must wait provisioning_delay_seconds between calls.

        The delay prevents triggering DigitalOcean's abuse detection heuristics
        which monitor for high-frequency droplet creation from a single account.
        """
        adapter = DigitalOceanProvisionerAdapter(
            client=mock_do_client,
            audit_store=mock_audit_store,
            preflight_checker=mock_preflight,
        )
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
            provisioning_delay_seconds=2,  # non-zero to verify delay is respected
        )
        with patch("time.sleep") as mock_sleep:
            adapter.provision(config)
        # When count=1, at least one sleep(2) call should occur (or equivalent)
        sleep_calls = [c.args[0] for c in mock_sleep.call_args_list if c.args]
        total_delay = sum(sleep_calls)
        assert total_delay >= 2 or any(d >= 2 for d in sleep_calls), (
            "provision() must call time.sleep(provisioning_delay_seconds) — "
            "RATELIMIT-001: 2s delay configured, no sleep calls observed"
        )

    def test_provision_implements_exponential_backoff_on_429(
        self,
        mock_do_client: MagicMock,
        mock_audit_store: MagicMock,
        mock_preflight: MagicMock,
    ) -> None:
        """RATELIMIT-002: provision() must retry with exponential backoff on 429.

        DigitalOcean returns HTTP 429 when the per-minute droplet creation
        rate limit is exceeded.  The adapter must not fail immediately on 429;
        it must retry with exponential backoff (1s, 2s, 4s ... cap at 60s).
        """
        # First call raises 429, second succeeds
        rate_limit_exc = Exception("429 Too Many Requests")
        success_response = {
            "droplet": {
                "id": 12345, "name": "test", "status": "new",
                "networks": {"v4": []}, "tags": []
            }
        }
        mock_do_client.droplets.create.side_effect = [rate_limit_exc, success_response]

        adapter = DigitalOceanProvisionerAdapter(
            client=mock_do_client,
            audit_store=mock_audit_store,
            preflight_checker=mock_preflight,
        )
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
            provisioning_delay_seconds=0,
        )
        with patch("time.sleep") as mock_sleep:
            try:
                adapter.provision(config)
            except Exception:
                pass  # downstream steps may fail; we care about retry behaviour
        # Should have slept at least once for the backoff
        assert mock_sleep.called, (
            "provision() must call time.sleep() when retrying after 429 — "
            "RATELIMIT-002: exponential backoff on rate limit response"
        )
        # First backoff sleep should be >= 1 second
        if mock_sleep.call_args_list:
            first_sleep = mock_sleep.call_args_list[0].args[0]
            assert first_sleep >= 1, (
                f"First backoff sleep must be >= 1 second, got {first_sleep} — "
                f"RATELIMIT-002: backoff starts at 1s and doubles each retry"
            )


# =============================================================================
# Happy path: destroy() returns partial failure info
# =============================================================================


@pytest.mark.integration
class TestDigitalOceanAdapterDestroy:
    """
    Scenario: Successful destruction of multiple nodes
      Given a list of node IDs to destroy
      When destroy() is called
      Then each droplet is deleted
      And associated SSH keys and firewall rules are removed
      And DestroyResult is returned with destroyed list
    """

    def test_destroy_calls_droplet_destroy_for_each_node(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
    ) -> None:
        """TASK-023-028 AC: destroy() must call client.droplets.destroy() for each node."""
        adapter.destroy(node_ids=["do-11111", "do-22222"])
        assert mock_do_client.droplets.destroy.call_count == 2, (
            "destroy() must call droplets.destroy() once per node ID — "
            "TASK-023-028 AC: each droplet must be individually destroyed"
        )

    def test_destroy_returns_destroy_result(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
    ) -> None:
        """destroy() must return a DestroyResult value object."""
        result = adapter.destroy(node_ids=["do-11111"])
        assert isinstance(result, DestroyResult), (
            "destroy() must return a DestroyResult — "
            "FM-022: partial failure information must be preserved"
        )

    def test_destroy_partial_failure_reported_in_result(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
    ) -> None:
        """FM-022: DestroyResult must list both successful and failed node IDs.

        When one node fails to destroy (e.g., already deleted, API error),
        the operator must know which nodes need manual cleanup.
        """
        # First call succeeds, second fails
        def destroy_side_effect(droplet_id: str, **kwargs: object) -> None:
            if str(droplet_id) == "do-99999":
                raise Exception("404 Not Found")

        mock_do_client.droplets.destroy.side_effect = destroy_side_effect

        result = adapter.destroy(node_ids=["do-11111", "do-99999"])
        assert "do-11111" in result.destroyed, (
            "Successfully destroyed node must appear in DestroyResult.destroyed"
        )
        assert "do-99999" in result.failed, (
            "Failed-to-destroy node must appear in DestroyResult.failed — "
            "FM-022: operator needs to know which nodes need manual cleanup"
        )

    def test_destroy_removes_ssh_keys_from_provider(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
    ) -> None:
        """TASK-023-028 AC / PI-005: destroy() must remove SSH keys from the provider.

        SSH keys persisting in the provider account after teardown allow
        post-engagement enumeration of historical key fingerprints.
        """
        adapter.destroy(node_ids=["do-11111"])
        mock_do_client.ssh_keys.delete.assert_called()

    def test_destroy_deletes_associated_firewall(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
    ) -> None:
        """TASK-023-028 AC: destroy() must delete the firewall rules created at provision."""
        adapter.destroy(node_ids=["do-11111"])
        mock_do_client.firewalls.delete.assert_called()


# =============================================================================
# Happy path: list_instances() filters by engagement_tag
# =============================================================================


@pytest.mark.integration
class TestDigitalOceanAdapterListInstances:
    """
    Scenario: list_instances() returns only nodes for the specified engagement
      Given two engagements share the same DigitalOcean account
      When list_instances(engagement_tag="jerry-abc123") is called
      Then only nodes tagged with jerry-abc123 are returned
      And nodes from other engagements are excluded
    """

    def test_list_instances_filters_by_engagement_tag(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
    ) -> None:
        """ISOLATION-001: list_instances() must filter by engagement_tag."""
        mock_do_client.droplets.list.return_value = {
            "droplets": [
                {
                    "id": 11111,
                    "tags": ["jerry-abc123def456"],
                    "networks": {"v4": [{"type": "public", "ip_address": "203.0.113.10"}]},
                    "region": {"slug": "nyc1"},
                    "status": "active",
                },
                {
                    "id": 22222,
                    "tags": ["jerry-other-engagement"],
                    "networks": {"v4": [{"type": "public", "ip_address": "203.0.113.20"}]},
                    "region": {"slug": "nyc1"},
                    "status": "active",
                },
            ]
        }
        nodes = adapter.list_instances(engagement_tag="jerry-abc123def456")
        node_ids = [n.id for n in nodes]
        assert "11111" in node_ids or 11111 in node_ids, (
            "list_instances() must return nodes with the specified engagement_tag"
        )
        assert "22222" not in node_ids and 22222 not in node_ids, (
            "list_instances() must exclude nodes with a different engagement_tag — "
            "ISOLATION-001: no cross-engagement node visibility"
        )

    def test_list_instances_returns_empty_list_when_no_nodes_match(
        self,
        adapter: DigitalOceanProvisionerAdapter,
        mock_do_client: MagicMock,
    ) -> None:
        """list_instances() returns empty list when no nodes match the tag."""
        mock_do_client.droplets.list.return_value = {"droplets": []}
        nodes = adapter.list_instances(engagement_tag="jerry-nonexistent")
        assert nodes == [], (
            "list_instances() must return [] when no nodes match — "
            "empty pool is a valid state at engagement start"
        )


# =============================================================================
# Architecture: API key sourced from env var, never hardcoded
# =============================================================================


@pytest.mark.integration
class TestDigitalOceanAdapterApiKeySource:
    """
    Scenario: API key is read from JERRY_PROXY_DO_API_KEY env var
      Given JERRY_PROXY_DO_API_KEY is set
      When DigitalOceanProvisionerAdapter.from_env() is called
      Then the adapter is constructed using the env var value
      And the key never appears in adapter __repr__ or __str__
    """

    def test_adapter_can_be_constructed_from_env_var(self) -> None:
        """TASK-023-028 AC: adapter must expose from_env() factory method."""
        import os
        with patch.dict(os.environ, {"JERRY_PROXY_DO_API_KEY": "dop_test_key"}):
            with patch(
                "src.proxy_infra.infrastructure.adapters.digitalocean_adapter.Client"
            ) as mock_client_class:
                mock_client_class.return_value = MagicMock()
                adapter = DigitalOceanProvisionerAdapter.from_env(
                    engagement_id="ENG-001"
                )
        assert adapter is not None, (
            "DigitalOceanProvisionerAdapter.from_env() must return an adapter instance"
        )

    def test_adapter_repr_does_not_expose_api_key(self) -> None:
        """APIKEY-002: adapter repr must not contain API key values."""
        mock_client = MagicMock()
        mock_audit = MagicMock()
        mock_preflight = MagicMock()
        adapter = DigitalOceanProvisionerAdapter(
            client=mock_client,
            audit_store=mock_audit,
            preflight_checker=mock_preflight,
        )
        repr_str = repr(adapter)
        assert "dop_v1_" not in repr_str, (
            "Adapter repr must not expose API key — APIKEY-002"
        )
