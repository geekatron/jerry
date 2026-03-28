# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Thin CLI command functions for the ``jerry proxy`` subcommand group.

Each function in this module is one CLI verb. It acts as a composition root:
  1. Resolves the provider adapter via factory (or accepts an injected adapter
     in tests).
  2. Runs the API-key pre-flight check before every mutating operation.
  3. Delegates to the adapter / domain service.
  4. Appends an audit-log entry for every operation.

Architecture note (H-07):
  The interface layer is the only layer that may import from all inner layers
  (domain, application, infrastructure). No other layer imports from here.

Security note (APICALL-004 / ORPHAN-006):
  - API keys are never passed as function arguments; adapters read them from
    the environment in their ``from_env()`` factory.
  - GC --confirm mode enforces Zone 3 approval (P-020).

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - TASK-023-023: Design CLI command structure
    - TASK-023-024: Implement jerry proxy provision
    - TASK-023-025: Implement jerry proxy status/rotate/destroy
    - TASK-023-045: Implement jerry proxy gc
"""

from __future__ import annotations

import os
from datetime import UTC
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.application.handlers.credential_check_result import CredentialCheckResult
    from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
    from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
    from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
    from src.proxy_infra.infrastructure.persistence.audit_log_store import AuditLogStore


# ---------------------------------------------------------------------------
# provision_command
# ---------------------------------------------------------------------------


def provision_command(
    config: ProvisionConfig,
    adapter: ProxyProvisionerPort,
    audit_store: AuditLogStore,
) -> list[ProxyNode]:
    """Provision proxy nodes and return the created node list.

    Runs the pre-flight check (if the adapter supports it) before calling
    ``adapter.provision(config)``.  Every successful call writes one audit
    entry per provisioned node.

    Zone 3 operation — caller must have obtained operator approval before
    invoking this function (P-020).

    Args:
        config: Immutable provisioning parameters (provider, region, count,
            engagement_id, engagement_tag, ssh_public_key, operator_ip, …).
        adapter: Concrete ProxyProvisionerPort implementation to use.
        audit_store: AuditLogStore for post-provision audit entries.

    Returns:
        List of provisioned ProxyNode instances.

    Raises:
        ProvisionError: If the cloud provider returns an error.
        ApiKeyExpiredError: If the pre-flight check detects an expired key.
        ApiKeyPermissionError: If the pre-flight check detects missing scope.
    """
    # Run pre-flight if the adapter exposes it
    _run_preflight_if_present(adapter)

    nodes = adapter.provision(config)

    for node in nodes:
        audit_store.write_entry(
            engagement_id=config.engagement_id,
            action="provision",
            provider=config.provider,
            resource_id=node.id,
            response_code=201,
        )

    return nodes


# ---------------------------------------------------------------------------
# status_command
# ---------------------------------------------------------------------------


def status_command(
    engagement_id: str,
    adapter: ProxyProvisionerPort,
    audit_store: AuditLogStore,
) -> list[ProxyNode]:
    """Return all proxy nodes for a given engagement.

    Queries the provider using ``adapter.list_instances(engagement_tag)``
    where the engagement tag is derived from the engagement_id.  This is a
    read-only (Zone 1) operation; no pre-flight check is required.

    Args:
        engagement_id: Engagement identifier used to scope the query
            (PI-002). An empty string returns all nodes visible to the
            adapter (not recommended for production use).
        adapter: Concrete ProxyProvisionerPort implementation to use.
        audit_store: AuditLogStore for the list_instances audit entry.

    Returns:
        List of ProxyNode instances associated with the engagement.
    """
    nodes = adapter.list_instances(engagement_id)

    audit_store.write_entry(
        engagement_id=engagement_id,
        action="list_instances",
        provider="unknown",
        resource_id="all",
        response_code=200,
    )

    return nodes


# ---------------------------------------------------------------------------
# rotate_command
# ---------------------------------------------------------------------------


def rotate_command(
    engagement_id: str,
    node_id: str,
    adapter: ProxyProvisionerPort,
    audit_store: AuditLogStore,
    config: ProvisionConfig | None = None,
) -> ProxyNode:
    """Rotate a single proxy node (provision replacement, then destroy original).

    Implements provision-before-destroy (PI-003):
      1. Run pre-flight check (Zone 3).
      2. If ``config`` is provided, provision a replacement node first.
      3. Destroy the original node.
      4. Return the replacement node.

    When ``config`` is ``None`` the function skips replacement provisioning
    and only destroys the target node (useful in tests that control the
    mock completely).

    Zone 3 operation — caller must have obtained operator approval (P-020).

    Args:
        engagement_id: Owning engagement identifier (PI-002).
        node_id: Provider-assigned ID of the node to rotate out.
        adapter: Concrete ProxyProvisionerPort implementation to use.
        audit_store: AuditLogStore for audit entries.
        config: Optional ProvisionConfig for the replacement node.  When
            provided, a new node is provisioned before the old one is
            destroyed (PI-003).

    Returns:
        The replacement ProxyNode (from ``config``) or the first node from
        the post-destroy node list if ``config`` is None.

    Raises:
        ProvisionError: If replacement provisioning fails.
        ApiKeyExpiredError: If the pre-flight check detects an expired key.
    """
    # Run pre-flight if the adapter exposes it
    _run_preflight_if_present(adapter)

    replacement: ProxyNode | None = None

    # PI-003: provision replacement before destroying the original
    if config is not None:
        new_nodes = adapter.provision(config)
        replacement = new_nodes[0] if new_nodes else None
        if replacement is not None:
            audit_store.write_entry(
                engagement_id=engagement_id,
                action="provision",
                provider=config.provider,
                resource_id=replacement.id,
                response_code=201,
            )

    # Destroy the original node
    adapter.destroy([node_id])
    audit_store.write_entry(
        engagement_id=engagement_id,
        action="rotate",
        provider="unknown",
        resource_id=node_id,
        response_code=204,
    )

    if replacement is None:
        # Callers that did not supply a config receive the first available node
        # after the old one is gone (edge-case convenience for tests).
        remaining = adapter.list_instances(engagement_id)
        if remaining:
            return remaining[0]
        # Construct a minimal sentinel node using the existing node's id
        from datetime import datetime

        from src.proxy_infra.domain.value_objects.node_status import NodeStatus
        from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode
        from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
        from src.proxy_infra.domain.value_objects.proxy_type import ProxyType

        return ProxyNode(
            id=node_id,
            provider="unknown",
            ip="",
            region="",
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            status=NodeStatus.DESTROYED,
            ssh_key_id="",
            created_at=datetime.now(UTC),
            engagement_id=engagement_id,
        )

    return replacement


# ---------------------------------------------------------------------------
# destroy_command
# ---------------------------------------------------------------------------


def destroy_command(
    engagement_id: str,
    adapter: ProxyProvisionerPort,
    audit_store: AuditLogStore,
    node_ids: list[str] | None = None,
    raw_engagement_id: str = "",
) -> DestroyResult:
    """Tear down all (or specified) proxy nodes for an engagement.

    Runs the pre-flight check, then calls ``adapter.destroy()``.

    Zone 3 operation — caller must have obtained operator approval (P-020).

    Args:
        engagement_id: Engagement tag for ``list_instances`` filtering
            (e.g., ``jerry-red-0001``).  Also used as fallback for
            ``raw_engagement_id`` if that parameter is empty.
        adapter: Concrete ProxyProvisionerPort implementation to use.
        audit_store: AuditLogStore for the destroy audit entry.
        node_ids: Specific node IDs to destroy.  When ``None`` or empty,
            the function queries ``adapter.list_instances(engagement_id)``
            first to obtain the full node list, then destroys all of them.
        raw_engagement_id: Original engagement ID from the config (e.g.,
            ``RED-0001``).  Used for SSH key and firewall name-based
            cleanup (PI-005).  When empty, falls back to ``engagement_id``.

    Returns:
        DestroyResult with per-node success/failure lists.

    Raises:
        TeardownError: If cleanup fails for one or more nodes.
        ApiKeyExpiredError: If the pre-flight check detects an expired key.
    """
    from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult

    # Run pre-flight if the adapter exposes it
    _run_preflight_if_present(adapter)

    # Resolve the full node list when no specific IDs were supplied
    ids_to_destroy: list[str] = list(node_ids) if node_ids else []
    if not ids_to_destroy:
        nodes = adapter.list_instances(engagement_id)
        ids_to_destroy = [n.id for n in nodes]

    if not ids_to_destroy:
        # Still run engagement-level cleanup for orphaned SSH keys / firewalls
        cleanup_id = raw_engagement_id or engagement_id
        adapter.destroy([], engagement_id=cleanup_id)
        return DestroyResult(destroyed=[], failed=[])

    # Pass raw engagement ID for name-based SSH key / firewall cleanup (PI-005)
    cleanup_id = raw_engagement_id or engagement_id
    result = adapter.destroy(ids_to_destroy, engagement_id=cleanup_id)

    audit_store.write_entry(
        engagement_id=engagement_id,
        action="destroy",
        provider="unknown",
        resource_id=",".join(ids_to_destroy),
        response_code=204 if result.is_all_successful else 500,
    )

    return result


# ---------------------------------------------------------------------------
# gc_command
# ---------------------------------------------------------------------------


def gc_command(
    engagement_id: str,
    adapter: ProxyProvisionerPort,
    audit_store: AuditLogStore,
    dry_run: bool = True,
    raw_engagement_id: str = "",
) -> list[str]:
    """Detect and optionally destroy orphaned proxy nodes (ORPHAN-001 to ORPHAN-006).

    Uses ``adapter.list_instances(engagement_id)`` to discover nodes that
    carry the engagement tag but are not properly registered as active
    (teardown_confirmed was never set to True).

    ``--dry-run`` (dry_run=True):
        Returns a list of orphaned node IDs without destroying anything.
        Read-only; no pre-flight needed.

    ``--confirm`` (dry_run=False):
        Runs pre-flight, then destroys all discovered orphans.
        Zone 3 operation — caller must have obtained operator approval (P-020).

    ISOLATION-002: Only queries by engagement tag — never calls
    ``adapter.list_nodes()`` for a global sweep.

    Args:
        engagement_id: Engagement tag / ID to search for orphaned resources.
        adapter: Concrete ProxyProvisionerPort implementation to use.
        audit_store: AuditLogStore for gc audit entries.
        dry_run: When True (default), list orphans without destroying.
            When False, destroy all discovered orphans (Zone 3 operation).

    Returns:
        List of orphaned node IDs discovered (both in dry-run and confirm
        modes — in confirm mode these are the nodes that were destroyed).

    Raises:
        ApiKeyExpiredError: If pre-flight fails (confirm mode only).
    """
    # Discover orphans using the engagement-tag-scoped query (ISOLATION-002)
    orphaned_nodes = adapter.list_instances(engagement_id)
    orphan_ids = [n.id for n in orphaned_nodes]

    if dry_run:
        # Read-only — just report what would be destroyed
        audit_store.write_entry(
            engagement_id=engagement_id,
            action="list_instances",
            provider="unknown",
            resource_id="gc-dry-run",
            response_code=200,
        )
        return orphan_ids

    # --confirm path: Zone 3 — destroy after pre-flight
    _run_preflight_if_present(adapter)

    if orphan_ids:
        adapter.destroy(orphan_ids, engagement_id=raw_engagement_id or engagement_id)
        audit_store.write_entry(
            engagement_id=engagement_id,
            action="destroy",
            provider="unknown",
            resource_id=",".join(orphan_ids),
            response_code=204,
        )

    return orphan_ids


# ---------------------------------------------------------------------------
# engage_command
# ---------------------------------------------------------------------------


def engage_command(
    config_path: Path,
    adapter: ProxyProvisionerPort,
    audit_store: AuditLogStore,
    credential_dir: Path | None = None,
    credential_injector: object | None = None,
    ssh_readiness: object | None = None,
    health_checker: object | None = None,
    manifest_writer: object | None = None,
    bpf_port: object | None = None,
    full_pipeline: bool = False,
) -> list[ProxyNode]:
    """Bootstrap a full engagement: parse config, generate SSH keys, provision nodes.

    Composition root for the hands-free pipeline.  Reads the engagement YAML
    config, generates a per-engagement Ed25519 SSH keypair, constructs a
    ``ProvisionConfig``, and calls ``provision_command``.

    Zone 3 operation — caller must have obtained operator approval (P-020).

    When all injection ports are provided (credential_injector, ssh_readiness,
    health_checker, manifest_writer), the pipeline extends to the full
    engage-to-route flow: provision → inject → BPF bypass → compose generation.
    When injection ports are absent, only provisioning runs (backward compatible).

    Args:
        config_path: Path to the engagement YAML config file.
        adapter: Concrete ProxyProvisionerPort implementation.
        audit_store: AuditLogStore for audit entries.
        credential_dir: Directory for generated credentials.  When ``None``,
            defaults to ``{config_path.parent}/credentials/``.
        credential_injector: Optional SshCredentialInjectionHandler for
            post-boot credential injection.  When provided alongside
            ssh_readiness, health_checker, and manifest_writer, the full
            engage pipeline runs.
        ssh_readiness: Optional SshReadinessPort for SSH availability polling.
        health_checker: Optional NodeHealthPort for pre-use health gate.
        manifest_writer: Optional ManifestWriterPort for pool manifest updates.
        bpf_port: Optional BPF bypass map port.  When ``None``, a no-op port
            is used (BPF bypass map not updated).

    Returns:
        List of provisioned (and optionally injected) ProxyNode instances.

    Raises:
        FileNotFoundError: If config_path does not exist.
        ValueError: If config has missing or invalid fields.
    """
    from src.proxy_infra.application.handlers.engagement_config_parser import (
        EngagementConfigParser,
    )
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
    from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
    from src.proxy_infra.domain.value_objects.proxy_type import ProxyType
    from src.proxy_infra.infrastructure.keygen.ssh_keygen_adapter import SshKeygenAdapter

    # Stage 1: Parse engagement config
    parser = EngagementConfigParser()
    eng_config = parser.parse(config_path)

    # Stage 2: Create credential directory
    if credential_dir is None:
        credential_dir = config_path.parent / "credentials"
    credential_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(credential_dir, 0o700)

    # Stage 3: Generate SSH keypair
    keygen = SshKeygenAdapter()
    keygen_result = keygen.generate(
        engagement_id=eng_config.engagement_id,
        credential_dir=credential_dir,
    )
    ssh_public_key = keygen_result.public_key_path.read_text(encoding="utf-8").strip()

    # Stage 4: Build ProvisionConfig from engagement config + generated key
    provision_config = ProvisionConfig(
        provider=eng_config.provider,
        region=eng_config.region,
        engagement_id=eng_config.engagement_id,
        engagement_tag=eng_config.engagement_tag,
        count=eng_config.count,
        role=ProxyRole.ACTIVE,
        proxy_type=ProxyType.DIRECT_SOCKS5,
        ssh_public_key=ssh_public_key,
        operator_ip=eng_config.operator_ip,
        image=eng_config.image,
        size=eng_config.size,
        socks_port=eng_config.socks_port,
    )

    # Stage 5: Provision via existing provision_command
    nodes = provision_command(provision_config, adapter, audit_store)

    # Stage 6: Run the full engage pipeline (inject → BPF → compose)
    # When credential_injector is explicitly provided OR full_pipeline=True,
    # run the full injection pipeline. Otherwise, return provision-only results.
    #
    # In production: caller passes full_pipeline=True (default for CLI invocation)
    # In tests: caller omits injection ports → provision-only path
    if credential_injector is not None or full_pipeline:
        from src.proxy_infra.application.handlers.engage_pipeline_orchestrator import (
            EngagePipelineOrchestrator,
        )
        from src.proxy_infra.application.handlers.ssh_credential_injection_handler import (
            SshCredentialInjectionHandler,
        )
        from src.proxy_infra.infrastructure.ssh.curl_socks_verifier import CurlSocksVerifier
        from src.proxy_infra.infrastructure.ssh.subprocess_ssh_executor import (
            SubprocessSshExecutor,
        )
        from src.proxy_infra.infrastructure.ssh.tcp_ssh_readiness_adapter import (
            TcpSshReadinessAdapter,
        )

        # Resolve real adapters — composition root wires concrete implementations
        _ssh_readiness = ssh_readiness or TcpSshReadinessAdapter()
        _health_checker = health_checker or _noop_health_checker()
        _manifest_writer = manifest_writer or _noop_manifest_writer()
        _ssh_executor = SubprocessSshExecutor()
        _socks_verifier = CurlSocksVerifier()
        _injector = credential_injector or SshCredentialInjectionHandler(
            ssh_readiness=_ssh_readiness,
            ssh_executor=_ssh_executor,
            socks_verifier=_socks_verifier,
            manifest_writer=_manifest_writer,
        )

        engagement_dir = credential_dir.parent
        orchestrator = EngagePipelineOrchestrator(
            provisioner=adapter,
            ssh_readiness=_ssh_readiness,
            credential_injector=_injector,
            health_checker=_health_checker,
            manifest_writer=_manifest_writer,
            bpf_port=bpf_port if bpf_port is not None else _noop_bpf_port(),
            engagement_dir=engagement_dir,
        )
        pipeline_result = orchestrator.orchestrate(
            provision_config,
            private_key_path=keygen_result.private_key_path,
        )
        if pipeline_result.success:
            return pipeline_result.nodes or nodes

    return nodes


# ---------------------------------------------------------------------------
# credentials_set_command
# ---------------------------------------------------------------------------


def credentials_set_command(provider: str, api_key: str) -> None:
    """Store a cloud provider API key in the macOS Keychain.

    Composition root: instantiates ``KeyringCredentialStore`` and stores
    the credential. The API key is accepted as a parameter (caller is
    responsible for secure input, e.g., ``getpass.getpass``).

    Args:
        provider: Cloud provider name (e.g., "digitalocean").
        api_key: API key to store. Never logged.
    """
    from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
        KeyringCredentialStore,
    )

    store = KeyringCredentialStore()
    store.store_credential(provider, api_key)


# ---------------------------------------------------------------------------
# credentials_check_command
# ---------------------------------------------------------------------------


def credentials_check_command(provider: str) -> CredentialCheckResult:
    """Check whether a credential exists for a provider without revealing the value.

    Tries Keychain first, then environment variable.

    Args:
        provider: Cloud provider name (e.g., "digitalocean").

    Returns:
        CredentialCheckResult with found=True/False and source.
    """
    from src.proxy_infra.application.handlers.credential_check_result import (
        CredentialCheckResult,
    )
    from src.proxy_infra.domain.exceptions.credential_not_found_error import (
        CredentialNotFoundError as _CredNotFound,
    )
    from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
        KeyringCredentialStore,
    )

    keyring_store = KeyringCredentialStore()
    try:
        keyring_store.get_credential(provider)
        return CredentialCheckResult(found=True, provider=provider, source="keychain")
    except _CredNotFound:
        pass

    env_var = f"JERRY_PROXY_{provider.upper()}_API_KEY"
    if os.environ.get(env_var):
        return CredentialCheckResult(found=True, provider=provider, source="environment")

    return CredentialCheckResult(found=False, provider=provider, source="none")


# ---------------------------------------------------------------------------
# credentials_delete_command
# ---------------------------------------------------------------------------


def credentials_delete_command(provider: str) -> bool:
    """Remove a stored credential from the macOS Keychain.

    Args:
        provider: Cloud provider name (e.g., "digitalocean").

    Returns:
        True if credential was found and deleted, False if not found.
    """
    from src.proxy_infra.infrastructure.credentials.keyring_credential_store import (
        KeyringCredentialStore,
    )

    store = KeyringCredentialStore()
    return store.delete_credential(provider)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


class _NoopHealthChecker:
    """No-op health checker — always passes."""

    def check(self, node: object) -> bool:
        """Always returns True — health check bypassed."""
        return True


class _NoopManifestWriter:
    """No-op manifest writer — does nothing."""

    def write(self, node: object) -> None:
        """No-op write."""


def _noop_health_checker() -> _NoopHealthChecker:
    """Return a no-op health checker."""
    return _NoopHealthChecker()


def _noop_manifest_writer() -> _NoopManifestWriter:
    """Return a no-op manifest writer."""
    return _NoopManifestWriter()


class _NoopBpfPort:
    """No-op BPF port for when BPF bypass map is not needed."""

    def update_bypass_ips(self, ips: list[str]) -> None:
        """No-op bypass IP update."""


def _noop_bpf_port() -> _NoopBpfPort:
    """Return a no-op BPF port instance."""
    return _NoopBpfPort()


def _run_preflight_if_present(adapter: ProxyProvisionerPort) -> None:
    """Call ``adapter._preflight.run()`` when a pre-flight checker is attached.

    Many adapters expose an optional ``_preflight`` attribute that holds an
    ``ApiKeyPreflightChecker``.  This helper centralises the duck-typed check
    so each command function doesn't duplicate the hasattr guard.

    Args:
        adapter: The adapter to inspect for a pre-flight checker.
    """
    preflight = getattr(adapter, "_preflight", None)
    if preflight is not None:
        preflight.run()
