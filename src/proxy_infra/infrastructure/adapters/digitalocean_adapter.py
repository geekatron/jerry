# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""DigitalOceanProvisionerAdapter — ProxyProvisionerPort implementation for DigitalOcean.

Uses the `pydo` SDK to manage Droplets, SSH keys, and firewall rules.

References:
    - ADR-PROJ023-008: Direct API over Terraform decision
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

import logging
import os
import time
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from src.proxy_infra.domain.exceptions import ProvisionError
from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort
from src.proxy_infra.domain.value_objects.destroy_result import DestroyResult
from src.proxy_infra.domain.value_objects.health_status import HealthStatus
from src.proxy_infra.domain.value_objects.node_status import NodeStatus
from src.proxy_infra.domain.value_objects.proxy_node import ProxyNode

try:
    from pydo import Client  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
    Client = None  # type: ignore[assignment, misc]

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.firewall_rule import FirewallRule
    from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig

logger = logging.getLogger(__name__)

#: Default droplet image.
_DEFAULT_IMAGE: str = "ubuntu-24-04-x64"
#: Default droplet size (1 vCPU, 1 GB RAM).
_DEFAULT_SIZE: str = "s-1vcpu-1gb"
#: Maximum retry attempts on 429 rate-limit response (RATELIMIT-002).
_MAX_RETRY_ATTEMPTS: int = 3
#: Initial backoff delay in seconds for exponential backoff (RATELIMIT-002).
_INITIAL_BACKOFF_SECONDS: float = 1.0
#: Maximum backoff cap in seconds (RATELIMIT-002).
_MAX_BACKOFF_SECONDS: float = 60.0
#: Interval between droplet IP polling iterations in seconds.
_POLL_INTERVAL_SECONDS: float = 2.0
#: Maximum number of polling iterations before giving up on IP assignment.
_MAX_POLL_ITERATIONS: int = 30


def _build_cloud_init(config: ProvisionConfig) -> str:  # type: ignore[name-defined]
    """Build a minimal cloud-init user-data script for SOCKS5 proxy configuration.

    DigitalOcean accepts plain text cloud-init — do NOT base64-encode this value.
    Base64 encoding user_data on DO causes cloud-init to treat the payload as a
    literal base64 string, preventing script execution (TASK-023-028 AC).

    Args:
        config: Provisioning parameters containing socks_port and operator_ip.

    Returns:
        Cloud-init YAML string as plain text.
    """
    return f"""#cloud-config
packages:
  - microsocks
  - ufw
runcmd:
  - ufw default deny incoming
  - ufw default allow outgoing
  - ufw allow from {config.operator_ip} to any port 22 proto tcp
  - ufw allow from {config.operator_ip} to any port {config.socks_port} proto tcp
  - ufw --force enable
  - systemctl enable microsocks
  - systemctl start microsocks
"""


class DigitalOceanProvisionerAdapter(ProxyProvisionerPort):
    """ProxyProvisionerPort implementation for DigitalOcean via the pydo SDK.

    Manages Droplet lifecycle (create, delete, status), SSH key upload/removal,
    and Cloud Firewall rule configuration.

    Service name in providers.yaml: "digitalocean"

    Security properties:
        - API key is never stored as an instance attribute (APIKEY-002: key not
          exposed in repr).
        - All API operations are recorded in the audit log (APICALL-004).
        - Engagement tag is applied at creation time to prevent orphan resources
          (ORPHAN-003).
        - Firewall is created immediately after droplet to minimise the atomicity
          gap (FM-035).

    References:
        - ADR-PROJ023-008: DigitalOcean adapter design
    """

    def __init__(
        self,
        client: Any,
        audit_store: Any,
        preflight_checker: Any | None = None,
    ) -> None:
        """Initialise the DigitalOcean adapter.

        Args:
            client: pydo Client instance configured with the DigitalOcean API key.
                The caller is responsible for constructing the client — the adapter
                never stores or logs the raw API key.
            audit_store: AuditLogStore for recording all provisioner operations.
                Every API call appends one JSONL entry (APICALL-004).
            preflight_checker: Optional ApiKeyPreflightChecker.  When provided,
                ``run()`` is called before every mutating operation.
        """
        self._client = client
        self._audit = audit_store
        self._preflight = preflight_checker
        # Internal registry: maps node_id (str) -> {"ssh_key_id": str, "firewall_id": str}
        # Populated during provision(); consulted during destroy() for targeted cleanup.
        self._node_registry: dict[str, dict[str, str]] = {}

    def __repr__(self) -> str:
        """Return a safe string representation that never exposes the API key.

        Returns:
            String representation containing only the class name and client type.
        """
        return f"DigitalOceanProvisionerAdapter(client={type(self._client).__name__})"

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def from_env(
        cls,
        engagement_id: str,
        audit_store: Any | None = None,
        preflight_checker: Any | None = None,
    ) -> DigitalOceanProvisionerAdapter:
        """Construct an adapter by reading the API key from an environment variable.

        The API key is read from ``JERRY_PROXY_DO_API_KEY`` and passed directly
        to the pydo Client constructor.  The key is never stored as an instance
        attribute — only the constructed client is retained.

        Args:
            engagement_id: Engagement identifier used when creating the default
                AuditLogStore if none is provided.
            audit_store: Optional pre-constructed AuditLogStore.  When ``None``,
                a default store writing to ``./logs/audit/`` is created.
            preflight_checker: Optional ApiKeyPreflightChecker.

        Returns:
            Configured DigitalOceanProvisionerAdapter instance.

        Raises:
            EnvironmentError: If ``JERRY_PROXY_DO_API_KEY`` is not set.
        """
        api_key = os.environ.get("JERRY_PROXY_DO_API_KEY", "")
        if not api_key:
            raise OSError(
                "JERRY_PROXY_DO_API_KEY environment variable is not set — "
                "DigitalOcean adapter requires an API key to authenticate"
            )
        client = Client(token=api_key)

        if audit_store is None:
            from src.proxy_infra.infrastructure.persistence.audit_log_store import (
                AuditLogStore,
            )

            audit_store = AuditLogStore()

        return cls(
            client=client,
            audit_store=audit_store,
            preflight_checker=preflight_checker,
        )

    # ------------------------------------------------------------------
    # ProxyProvisionerPort implementation
    # ------------------------------------------------------------------

    def provision(self, config: ProvisionConfig) -> list[ProxyNode]:  # type: ignore[name-defined]
        """Provision Droplets on DigitalOcean.

        Execution order per TASK-023-028 AC:
        1. Preflight API key validation.
        2. Upload SSH public key (key ID needed for droplet creation).
        3. Create Droplet with engagement tag at creation time (ORPHAN-003).
        4. Create Cloud Firewall immediately after droplet ID is known (FM-035).
        5. Sleep ``provisioning_delay_seconds`` to respect rate limits (RATELIMIT-001).
        6. Poll for public IP assignment.
        7. Return ``ProxyNode`` list.

        Retry behaviour (RATELIMIT-002): ``droplets.create()`` is retried with
        exponential backoff (1 s, 2 s, 4 s … capped at 60 s) when the provider
        returns a 429 response.

        Args:
            config: Provisioning parameters.

        Returns:
            List of provisioned ProxyNode instances.

        Raises:
            ProvisionError: If Droplet creation fails after all retries.
        """
        if self._preflight is not None:
            self._preflight.run()

        nodes: list[ProxyNode] = []

        for node_index in range(config.count):
            node_name = f"jerry-proxy-{config.engagement_id}-{config.region}-{node_index}"

            # Step 1: Upload SSH key — must precede droplet creation so the
            # key ID is available as a creation parameter.
            ssh_key_resp = self._client.ssh_keys.create(
                body={
                    "name": f"jerry-proxy-{config.engagement_id}",
                    "public_key": config.ssh_public_key,
                }
            )
            ssh_key_id: str = str(ssh_key_resp["ssh_key"]["id"])
            self._audit.write_entry(
                engagement_id=config.engagement_id,
                action="provision",
                provider="digitalocean",
                resource_id=f"ssh-key-{ssh_key_id}",
                response_code=201,
            )

            # Step 2: Render cloud-init user_data as plain text.
            # DO accepts plain text — do NOT base64-encode (TASK-023-028 AC).
            user_data = _build_cloud_init(config)

            # Step 3: Create Droplet with exponential backoff on 429 (RATELIMIT-002).
            droplet_body = {
                "name": node_name,
                "region": config.region,
                "size": config.size,
                "image": config.image,
                "ssh_keys": [int(ssh_key_id)],
                "user_data": user_data,
                "tags": [config.engagement_tag],
                "monitoring": False,
            }
            droplet_resp = self._create_droplet_with_retry(droplet_body, config.engagement_id)
            droplet_id: int = droplet_resp["droplet"]["id"]
            node_id = str(droplet_id)

            self._audit.write_entry(
                engagement_id=config.engagement_id,
                action="provision",
                provider="digitalocean",
                resource_id=node_id,
                response_code=202,
            )

            # Step 4: Create Cloud Firewall immediately after droplet ID is known (FM-035).
            # This minimises the atomicity gap between droplet creation and firewall
            # attachment.  UFW (configured via cloud-init) provides protection during
            # the gap; the DO Cloud Firewall is the secondary layer.
            firewall_resp = self._client.firewalls.create(
                body={
                    "name": f"jerry-proxy-{config.engagement_id}-{node_index}",
                    "inbound_rules": [
                        {
                            "protocol": "tcp",
                            "ports": "22",
                            "sources": {"addresses": [f"{config.operator_ip}/32"]},
                        },
                        {
                            "protocol": "tcp",
                            "ports": str(config.socks_port),
                            "sources": {"addresses": [f"{config.operator_ip}/32"]},
                        },
                    ],
                    "outbound_rules": [
                        {
                            "protocol": "tcp",
                            "ports": "all",
                            "destinations": {"addresses": ["0.0.0.0/0", "::/0"]},
                        },
                    ],
                    "droplet_ids": [droplet_id],
                    "tags": [config.engagement_tag],
                }
            )
            firewall_id: str = str(firewall_resp["firewall"]["id"])
            self._audit.write_entry(
                engagement_id=config.engagement_id,
                action="provision",
                provider="digitalocean",
                resource_id=f"fw-{firewall_id}",
                response_code=202,
            )

            # Step 5: Respect provisioning_delay_seconds to avoid triggering
            # DigitalOcean abuse detection heuristics (RATELIMIT-001).
            if config.provisioning_delay_seconds > 0:
                time.sleep(config.provisioning_delay_seconds)

            # Step 6: Register node resources for cleanup during destroy().
            self._node_registry[node_id] = {
                "ssh_key_id": ssh_key_id,
                "firewall_id": firewall_id,
                "engagement_id": config.engagement_id,
            }

            # Step 7: Poll for public IP assignment.
            ip_address = self._poll_for_ip(node_id)

            nodes.append(
                ProxyNode(
                    id=node_id,
                    provider="digitalocean",
                    ip=ip_address,
                    region=config.region,
                    role=config.role,
                    proxy_type=config.proxy_type,
                    status=NodeStatus.CONFIGURING,
                    ssh_key_id=ssh_key_id,
                    created_at=datetime.now(UTC),
                    engagement_id=config.engagement_id,
                    socks_port=config.socks_port,
                )
            )

        return nodes

    def destroy(self, node_ids: list[str], engagement_id: str = "") -> DestroyResult:
        """Destroy Droplets by provider ID.

        Runs the API key pre-flight check before making any Droplet delete calls.
        For each node:
        1. Deletes the Droplet.
        2. Removes the associated SSH key from the provider account (PI-005).
        3. Deletes the associated Cloud Firewall rule set.

        After the per-node loop, performs an engagement-level sweep of any SSH
        keys and firewalls that were not captured by the in-memory registry
        (PI-005: cross-process resilience).  The sweep is triggered only when
        ``engagement_id`` is provided.

        Partial failures are captured in ``DestroyResult.failed`` so the operator
        can perform manual cleanup (FM-022).

        Args:
            node_ids: DigitalOcean Droplet IDs to destroy.  Each entry must be
                a string representation of the numeric Droplet ID, optionally
                prefixed with ``"do-"`` (e.g., ``"do-12345"`` or ``"12345"``).
            engagement_id: Optional engagement identifier.  When provided, a
                name-based API sweep is performed after the per-node loop to
                delete any SSH keys and firewalls that share the
                ``jerry-proxy-{engagement_id}`` name prefix but were not
                captured in the in-memory registry (cross-process destroy
                resilience, PI-005).

        Returns:
            DestroyResult with per-node success/failure details.
        """
        if self._preflight is not None:
            self._preflight.run()

        destroyed: list[str] = []
        failed: list[str] = []

        for node_id in node_ids:
            try:
                self._client.droplets.destroy(droplet_id=node_id)
                self._audit.write_entry(
                    engagement_id=self._node_registry.get(node_id, {}).get(
                        "engagement_id", "unknown"
                    ),
                    action="destroy",
                    provider="digitalocean",
                    resource_id=node_id,
                    response_code=204,
                )
                destroyed.append(node_id)
            except Exception:  # FM-022: catch all to build partial DestroyResult
                self._audit.write_entry(
                    engagement_id=self._node_registry.get(node_id, {}).get(
                        "engagement_id", "unknown"
                    ),
                    action="destroy",
                    provider="digitalocean",
                    resource_id=node_id,
                    response_code=500,
                )
                failed.append(node_id)

            # Always attempt SSH key cleanup (PI-005: SSH keys must not persist
            # in the provider account post-engagement — they enable fingerprint
            # enumeration of historical key material).
            self._cleanup_ssh_key(node_id)

            # Always attempt firewall cleanup.
            self._cleanup_firewall(node_id)

        # Engagement-level resource cleanup (PI-005: cross-process resilience).
        # Sweeps all SSH keys and firewalls matching the engagement name prefix
        # so that resources orphaned by a prior process (empty _node_registry)
        # are cleaned up even when the per-node registry path finds nothing.
        if engagement_id:
            self._cleanup_engagement_ssh_keys(engagement_id)
            self._cleanup_engagement_firewalls(engagement_id)

        return DestroyResult(destroyed=destroyed, failed=failed)

    def health_check(self, node_id: str) -> HealthStatus:
        """Check health via DigitalOcean API droplet status field.

        Args:
            node_id: DigitalOcean Droplet ID.

        Returns:
            HealthStatus with reachability and service status.
        """
        checked_at = datetime.now(UTC)
        try:
            raw_id = node_id.removeprefix("do-")
            resp = self._client.droplets.get(droplet_id=raw_id)
            droplet = resp.get("droplet", {})
            status = droplet.get("status", "unknown")
            is_active = status == "active"
            return HealthStatus(
                node_id=node_id,
                reachable=is_active,
                socks_port_open=False,
                ssh_accessible=is_active,
                checked_at=checked_at,
                error_message=None if is_active else f"droplet status={status}",
            )
        except Exception as exc:
            return HealthStatus(
                node_id=node_id,
                reachable=False,
                socks_port_open=False,
                ssh_accessible=False,
                checked_at=checked_at,
                error_message=str(exc),
            )

    def list_nodes(self) -> list[ProxyNode]:
        """List all Droplets visible to this adapter's API key.

        Returns:
            List of all ProxyNode instances from this provider.
        """
        resp = self._client.droplets.list()
        droplets = self._extract_list(resp, "droplets")
        return [self._droplet_to_node(d) for d in droplets]

    def list_instances(self, engagement_tag: str) -> list[ProxyNode]:
        """List Droplets filtered by engagement tag (ISOLATION-001).

        Only Droplets that carry the exact ``engagement_tag`` value are returned.
        Droplets from other engagements sharing the same provider account are
        excluded to prevent cross-engagement node visibility.

        Args:
            engagement_tag: Engagement tag to filter by (ISOLATION-001).

        Returns:
            List of ProxyNode instances matching the tag.
        """
        resp = self._client.droplets.list()
        droplets = self._extract_list(resp, "droplets")
        matching = [d for d in droplets if engagement_tag in d.get("tags", [])]
        return [self._droplet_to_node(d) for d in matching]

    def upload_ssh_key(self, public_key: str) -> str:
        """Upload an SSH public key to DigitalOcean.

        Args:
            public_key: OpenSSH public key string.

        Returns:
            DigitalOcean-assigned key ID as a string.
        """
        resp = self._client.ssh_keys.create(
            body={"name": "jerry-proxy-key", "public_key": public_key}
        )
        return str(resp["ssh_key"]["id"])

    def remove_ssh_key(self, key_id: str) -> None:
        """Remove an SSH key from DigitalOcean by key ID.

        Args:
            key_id: DigitalOcean-assigned SSH key identifier.
        """
        self._client.ssh_keys.delete(ssh_key_identifier=key_id)

    def configure_firewall(self, node_id: str, rules: list[FirewallRule]) -> None:  # type: ignore[name-defined]
        """Apply Cloud Firewall rules to a Droplet.

        If the node was provisioned through this adapter (and therefore has a
        firewall ID in the internal registry), the existing firewall is updated.
        Otherwise a new Cloud Firewall is created and attached to the Droplet.

        Args:
            node_id: DigitalOcean Droplet ID.
            rules: Firewall rules to apply.
        """
        inbound_rules: list[dict[str, Any]] = []
        outbound_rules: list[dict[str, Any]] = []
        for rule in rules:
            entry: dict[str, Any] = {
                "protocol": rule.protocol,
                "ports": rule.ports,
            }
            if rule.direction == "inbound":
                entry["sources"] = {"addresses": [rule.sources]}
                inbound_rules.append(entry)
            else:
                entry["destinations"] = {"addresses": [rule.sources]}
                outbound_rules.append(entry)

        registry_entry = self._node_registry.get(node_id, {})
        existing_fw_id = registry_entry.get("firewall_id")

        if existing_fw_id:
            self._client.firewalls.update(
                firewall_id=existing_fw_id,
                body={
                    "name": f"jerry-proxy-{node_id}",
                    "inbound_rules": inbound_rules,
                    "outbound_rules": outbound_rules,
                    "droplet_ids": [int(node_id)],
                },
            )
        else:
            resp = self._client.firewalls.create(
                body={
                    "name": f"jerry-proxy-{node_id}",
                    "inbound_rules": inbound_rules,
                    "outbound_rules": outbound_rules,
                    "droplet_ids": [int(node_id)],
                }
            )
            new_fw_id = str(resp["firewall"]["id"])
            if node_id not in self._node_registry:
                self._node_registry[node_id] = {}
            self._node_registry[node_id]["firewall_id"] = new_fw_id

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _create_droplet_with_retry(
        self, body: dict[str, Any], engagement_id: str
    ) -> dict[str, Any]:
        """Call droplets.create() with exponential backoff on 429 (RATELIMIT-002).

        Retries up to ``_MAX_RETRY_ATTEMPTS`` times.  The initial backoff is
        ``_INITIAL_BACKOFF_SECONDS``, doubling on each retry up to
        ``_MAX_BACKOFF_SECONDS``.

        Args:
            body: Request body dict for ``client.droplets.create(body=body)``.
            engagement_id: Engagement identifier for audit logging.

        Returns:
            Successful droplet creation response dict.

        Raises:
            ProvisionError: If all retry attempts are exhausted.
        """
        backoff = _INITIAL_BACKOFF_SECONDS
        last_exc: Exception | None = None

        for attempt in range(_MAX_RETRY_ATTEMPTS):
            try:
                return self._client.droplets.create(body=body)  # type: ignore[return-value]
            except Exception as exc:
                last_exc = exc
                if "429" in str(exc):
                    # Rate limited — apply exponential backoff (RATELIMIT-002).
                    time.sleep(backoff)
                    backoff = min(backoff * 2, _MAX_BACKOFF_SECONDS)
                else:
                    # Non-rate-limit failure — raise immediately as ProvisionError.
                    raise ProvisionError(
                        f"Droplet creation failed on attempt {attempt + 1}: {exc}"
                    ) from exc

        raise ProvisionError(
            f"Droplet creation failed after {_MAX_RETRY_ATTEMPTS} attempts: {last_exc}"
        )

    def _poll_for_ip(self, node_id: str) -> str:
        """Poll the Droplets API until a public IPv4 address is assigned.

        Args:
            node_id: DigitalOcean Droplet ID as a string.

        Returns:
            Public IPv4 address string, or empty string if not assigned within
            the polling window.
        """
        for _ in range(_MAX_POLL_ITERATIONS):
            try:
                resp = self._client.droplets.get(droplet_id=node_id)
                droplet = resp.get("droplet", {})
                networks = droplet.get("networks", {}).get("v4", [])
                public_ips = [n["ip_address"] for n in networks if n.get("type") == "public"]
                if public_ips:
                    return public_ips[0]
            except Exception:
                pass
            time.sleep(_POLL_INTERVAL_SECONDS)
        return ""

    def _cleanup_ssh_key(self, node_id: str) -> None:
        """Remove the SSH key associated with a node from DigitalOcean.

        Fast path: looks up the SSH key ID from the internal node registry
        (same-process provision -> destroy).  When the registry has no entry
        for this node (cross-process destroy), the deletion is skipped here;
        the caller is expected to follow up with
        ``_cleanup_engagement_ssh_keys()`` to perform a name-based sweep.

        Args:
            node_id: Provider-assigned Droplet ID used as the registry key.
        """
        registry_entry = self._node_registry.get(node_id, {})
        key_id = registry_entry.get("ssh_key_id")
        if not key_id:
            # Registry miss — cross-process sweep handles this via
            # _cleanup_engagement_ssh_keys(); nothing to do here.
            return
        try:
            self._client.ssh_keys.delete(ssh_key_identifier=key_id)
            self._audit.write_entry(
                engagement_id=registry_entry.get("engagement_id", "unknown"),
                action="cleanup_ssh_key",
                provider="digitalocean",
                resource_id=f"ssh-key-{key_id}",
                response_code=204,
            )
        except Exception as exc:
            logger.warning(
                "SSH key cleanup failed for node %s (key_id=%s): %s",
                node_id,
                key_id,
                exc,
            )

    def _cleanup_firewall(self, node_id: str) -> None:
        """Delete the Cloud Firewall associated with a node.

        Fast path: looks up the firewall ID from the internal node registry
        (same-process provision -> destroy).  When the registry has no entry
        for this node (cross-process destroy), the deletion is skipped here;
        the caller is expected to follow up with
        ``_cleanup_engagement_firewalls()`` to perform a name-based sweep.

        Args:
            node_id: Provider-assigned Droplet ID used as the registry key.
        """
        registry_entry = self._node_registry.get(node_id, {})
        firewall_id = registry_entry.get("firewall_id")
        if not firewall_id:
            # Registry miss — cross-process sweep handles this via
            # _cleanup_engagement_firewalls(); nothing to do here.
            return
        try:
            self._client.firewalls.delete(firewall_id=firewall_id)
            self._audit.write_entry(
                engagement_id=registry_entry.get("engagement_id", "unknown"),
                action="cleanup_firewall",
                provider="digitalocean",
                resource_id=f"fw-{firewall_id}",
                response_code=204,
            )
        except Exception as exc:
            logger.warning(
                "Firewall cleanup failed for node %s (firewall_id=%s): %s",
                node_id,
                firewall_id,
                exc,
            )

    def _cleanup_engagement_ssh_keys(self, engagement_id: str) -> None:
        """Delete all SSH keys whose name begins with ``jerry-proxy-{engagement_id}``.

        Fallback sweep for cross-process destroy scenarios where ``_node_registry``
        is empty (PI-005).  Queries the DigitalOcean SSH keys API, filters by the
        engagement-scoped name prefix, and deletes each match.  An audit entry is
        written for every deleted key (FIND-003).

        The name prefix is deliberately broad enough to catch both the per-engagement
        key (``jerry-proxy-{engagement_id}``) and any per-node variants that may
        exist from earlier adapter revisions.

        Args:
            engagement_id: Engagement identifier used to build the name prefix
                ``jerry-proxy-{engagement_id}``.
        """
        name_prefix = f"jerry-proxy-{engagement_id}"
        try:
            resp = self._client.ssh_keys.list()
            ssh_keys: list[dict[str, Any]] = self._extract_list(resp, "ssh_keys")
        except Exception as exc:
            logger.warning(
                "Could not list SSH keys for engagement-level cleanup (engagement_id=%s): %s",
                engagement_id,
                exc,
            )
            return

        for key in ssh_keys:
            key_name: str = key.get("name", "")
            if not key_name.startswith(name_prefix):
                continue
            key_id = str(key.get("id", ""))
            try:
                self._client.ssh_keys.delete(ssh_key_identifier=key_id)
                self._audit.write_entry(
                    engagement_id=engagement_id,
                    action="cleanup_ssh_key",
                    provider="digitalocean",
                    resource_id=f"ssh-key-{key_id}",
                    response_code=204,
                )
                logger.debug(
                    "Deleted engagement SSH key %s (name=%s) for engagement %s",
                    key_id,
                    key_name,
                    engagement_id,
                )
            except Exception as exc:
                logger.warning(
                    "Failed to delete SSH key %s (name=%s) for engagement %s: %s",
                    key_id,
                    key_name,
                    engagement_id,
                    exc,
                )

    def _cleanup_engagement_firewalls(self, engagement_id: str) -> None:
        """Delete all firewalls whose name begins with ``jerry-proxy-{engagement_id}``.

        Fallback sweep for cross-process destroy scenarios where ``_node_registry``
        is empty (PI-005).  Queries the DigitalOcean firewalls API, filters by the
        engagement-scoped name prefix, and deletes each match.  An audit entry is
        written for every deleted firewall (FIND-003).

        Firewall names follow the pattern ``jerry-proxy-{engagement_id}-{node_index}``
        (set at provision time).  The prefix filter
        ``jerry-proxy-{engagement_id}`` is therefore a correct sub-string match
        for all firewalls belonging to this engagement.

        Args:
            engagement_id: Engagement identifier used to build the name prefix
                ``jerry-proxy-{engagement_id}``.
        """
        name_prefix = f"jerry-proxy-{engagement_id}"
        try:
            resp = self._client.firewalls.list()
            firewalls: list[dict[str, Any]] = self._extract_list(resp, "firewalls")
        except Exception as exc:
            logger.warning(
                "Could not list firewalls for engagement-level cleanup (engagement_id=%s): %s",
                engagement_id,
                exc,
            )
            return

        for fw in firewalls:
            fw_name: str = fw.get("name", "")
            if not fw_name.startswith(name_prefix):
                continue
            fw_id = str(fw.get("id", ""))
            try:
                self._client.firewalls.delete(firewall_id=fw_id)
                self._audit.write_entry(
                    engagement_id=engagement_id,
                    action="cleanup_firewall",
                    provider="digitalocean",
                    resource_id=f"fw-{fw_id}",
                    response_code=204,
                )
                logger.debug(
                    "Deleted engagement firewall %s (name=%s) for engagement %s",
                    fw_id,
                    fw_name,
                    engagement_id,
                )
            except Exception as exc:
                logger.warning(
                    "Failed to delete firewall %s (name=%s) for engagement %s: %s",
                    fw_id,
                    fw_name,
                    engagement_id,
                    exc,
                )

    @staticmethod
    def _extract_list(resp: Any, key: str) -> list[dict[str, Any]]:
        """Safely extract a list from an API response dict.

        Args:
            resp: Raw API response (expected to be a dict).
            key: Key to extract from the response dict.

        Returns:
            The list value for the key, or an empty list if the response is not
            a dict or the key is absent.
        """
        if not isinstance(resp, dict):
            return []
        return resp.get(key, []) or []

    @staticmethod
    def _droplet_to_node(droplet: dict[str, Any]) -> ProxyNode:
        """Convert a raw DigitalOcean droplet dict to a ProxyNode value object.

        Args:
            droplet: Raw droplet dict from the DigitalOcean API.

        Returns:
            ProxyNode constructed from the droplet metadata.
        """
        from src.proxy_infra.domain.value_objects.proxy_role import ProxyRole
        from src.proxy_infra.domain.value_objects.proxy_type import ProxyType

        networks = droplet.get("networks", {}).get("v4", [])
        public_ips = [n["ip_address"] for n in networks if n.get("type") == "public"]
        ip = public_ips[0] if public_ips else ""

        region = droplet.get("region", {})
        region_slug = region.get("slug", "") if isinstance(region, dict) else str(region)

        do_status = droplet.get("status", "unknown")
        if do_status == "active":
            status = NodeStatus.READY
        elif do_status in ("new", "off"):
            status = NodeStatus.PROVISIONING
        else:
            status = NodeStatus.UNHEALTHY

        return ProxyNode(
            id=str(droplet.get("id", "")),
            provider="digitalocean",
            ip=ip,
            region=region_slug,
            role=ProxyRole.ACTIVE,
            proxy_type=ProxyType.DIRECT_SOCKS5,
            status=status,
            ssh_key_id="",
            created_at=datetime.now(UTC),
            engagement_id="",
        )
