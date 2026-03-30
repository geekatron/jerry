# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Translate engagement scope YAML to Envoy virtual_host configuration.

Reads authorized_targets from an engagement scope document and generates
Envoy route_config virtual_hosts entries that enforce the engagement-scope
allowlist. The deny-all catch-all in the base Envoy config blocks anything
not explicitly allowed.

Architecture: ADR-PROJ023-003 v2 (Envoy Forward Proxy)
Task: T13-012
"""

from __future__ import annotations

import copy
import logging
import re
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)

# Cloud provider endpoint mappings for cloud_account target type.
# When the engagement scope includes a cloud_account target, the translator
# adds the provider's API endpoints to the allowlist so that tools like
# Prowler and Kubescape can reach the cloud APIs.
_CLOUD_PROVIDER_DOMAINS: dict[str, list[str]] = {
    "aws": [
        "*.amazonaws.com",
        "*.aws.amazon.com",
        "sts.amazonaws.com",
    ],
    "azure": [
        "*.azure.com",
        "*.microsoftonline.com",
        "management.azure.com",
        "login.microsoftonline.com",
    ],
    "gcp": [
        "*.googleapis.com",
        "accounts.google.com",
        "oauth2.googleapis.com",
        "cloudresourcemanager.googleapis.com",
    ],
}

# Validation: domain must be a valid hostname (no protocol, no path)
_DOMAIN_PATTERN = re.compile(
    r"^(\*\.)?[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*$"
)

# Validation: IP address (v4 only for now)
_IPV4_PATTERN = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")


class ScopeTranslationError(Exception):
    """Raised when scope translation fails due to invalid input."""


def translate_scope_to_envoy(
    scope_path: Path,
    zone: int,
    *,
    include_c2: bool = False,
) -> list[dict[str, Any]]:
    """Convert engagement scope authorized_targets to Envoy virtual_host entries.

    Args:
        scope_path: Path to the engagement scope YAML file.
        zone: Target zone (2 or 3). Zone 1 uses static allowlists.
        include_c2: If True, include c2_infrastructure targets (Zone 3 only).

    Returns:
        List of Envoy virtual_host dictionaries ready for injection
        into the route_config.virtual_hosts array.

    Raises:
        ScopeTranslationError: If scope file is invalid or contains
            unsupported target types.
        FileNotFoundError: If scope_path does not exist.
    """
    if zone not in (2, 3):
        msg = f"Envoy scope translation only supports zones 2 and 3, got {zone}"
        raise ScopeTranslationError(msg)

    scope_data = _load_scope(scope_path)
    engagement = scope_data.get("engagement", {})

    authorized_targets = engagement.get("authorized_targets", [])
    if not authorized_targets:
        msg = f"No authorized_targets in scope file: {scope_path}"
        raise ScopeTranslationError(msg)

    # Collect all domains from authorized_targets
    domains = _extract_domains(authorized_targets)

    # Add C2 infrastructure domains for Zone 3
    if include_c2 and zone == 3:
        c2_targets = engagement.get("c2_infrastructure", [])
        if c2_targets:
            c2_domains = _extract_domains(c2_targets)
            domains.extend(c2_domains)
            logger.info("Added %d C2 infrastructure domains for Zone 3", len(c2_domains))

    if not domains:
        msg = f"No resolvable domains extracted from scope targets: {scope_path}"
        raise ScopeTranslationError(msg)

    # Deduplicate while preserving order
    seen: set[str] = set()
    unique_domains: list[str] = []
    for d in domains:
        if d not in seen:
            seen.add(d)
            unique_domains.append(d)

    logger.info(
        "Translated %d scope targets to %d unique domains for Zone %d",
        len(authorized_targets),
        len(unique_domains),
        zone,
    )

    # Build the virtual_host entry with both CONNECT and HTTP routes.
    # CONNECT route must come first for HTTPS tunneling support.
    virtual_host: dict[str, Any] = {
        "name": f"engagement_scope_zone{zone}",
        "domains": unique_domains,
        "routes": [
            {
                "match": {"connect_matcher": {}},
                "route": {
                    "cluster": "dynamic_forward_proxy_cluster",
                    "timeout": "60s",
                    "upgrade_configs": [
                        {"upgrade_type": "CONNECT", "connect_config": {}},
                    ],
                },
            },
            {
                "match": {"prefix": "/"},
                "route": {
                    "cluster": "dynamic_forward_proxy_cluster",
                    "timeout": "60s",
                },
            },
        ],
    }

    return [virtual_host]


def generate_envoy_config(
    base_config_path: Path,
    scope_path: Path,
    output_path: Path,
    zone: int,
    *,
    include_c2: bool = False,
) -> Path:
    """Generate a complete Envoy config by injecting scope-derived virtual_hosts.

    Reads the base Envoy config template, injects engagement-scope-derived
    virtual_host entries before the deny_all catch-all, and writes the
    result to output_path.

    Args:
        base_config_path: Path to the base Envoy config template.
        scope_path: Path to the engagement scope YAML.
        output_path: Path to write the generated Envoy config.
        zone: Target zone (2 or 3).
        include_c2: If True, include c2_infrastructure targets.

    Returns:
        Path to the generated config file.

    Raises:
        ScopeTranslationError: If translation or config generation fails.
        FileNotFoundError: If base config or scope file does not exist.
    """
    # Load base config
    with base_config_path.open() as f:
        base_config = yaml.safe_load(f)

    if not base_config:
        msg = f"Empty or invalid base config: {base_config_path}"
        raise ScopeTranslationError(msg)

    # Generate virtual_hosts from scope
    scope_vhosts = translate_scope_to_envoy(scope_path, zone, include_c2=include_c2)

    # Deep copy to avoid mutating the original
    config = copy.deepcopy(base_config)

    # Navigate to route_config.virtual_hosts
    try:
        listeners = config["static_resources"]["listeners"]
        hcm_filter = listeners[0]["filter_chains"][0]["filters"][0]
        hcm_config = hcm_filter["typed_config"]
        route_config = hcm_config["route_config"]
        virtual_hosts = route_config["virtual_hosts"]
    except (KeyError, IndexError, TypeError) as e:
        msg = f"Invalid Envoy config structure in {base_config_path}: {e}"
        raise ScopeTranslationError(msg) from e

    # Insert scope virtual_hosts BEFORE the deny_all catch-all
    # The deny_all entry has domains: ["*"] and must be last
    deny_all_idx = _find_deny_all_index(virtual_hosts)
    for i, vhost in enumerate(scope_vhosts):
        virtual_hosts.insert(deny_all_idx + i, vhost)

    # EN-023-008: Add transparent TCP listener + ORIGINAL_DST cluster
    # for BPF-redirected raw TCP connections. This is groundwork for full
    # Envoy unification (requires 3 BPF programs per ps-researcher finding).
    # Current architecture: raw TCP scope enforcement via SocksBridge, not Envoy.
    _add_transparent_tcp_listener(config)
    _add_original_dst_cluster(config)

    # Write generated config
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w") as f:
        f.write(f"# GENERATED by scope_translator.py from: {scope_path.name}\n")
        f.write(f"# Zone: {zone}\n")
        f.write("# DO NOT EDIT MANUALLY during an engagement.\n\n")
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    logger.info("Generated Envoy config: %s", output_path)
    return output_path


def _add_transparent_tcp_listener(config: dict[str, Any]) -> None:
    """Add a transparent TCP listener with original_dst filter to the config.

    EN-023-008: This listener recovers the original destination from
    BPF-redirected connections. Coexists with the HTTP forward proxy
    on port 3128. Port 15001 chosen to avoid conflict with standard ports.

    Args:
        config: Mutable Envoy config dict to add the listener to.
    """
    transparent_listener: dict[str, Any] = {
        "name": "transparent_tcp",
        "address": {
            "socket_address": {"address": "0.0.0.0", "port_value": 15001},
        },
        "listener_filters": [
            {
                "name": "envoy.filters.listener.original_dst",
                "typed_config": {
                    "@type": "type.googleapis.com/envoy.extensions.filters.listener.original_dst.v3.OriginalDst",
                },
            },
        ],
        "filter_chains": [
            {
                "filters": [
                    {
                        "name": "envoy.filters.network.tcp_proxy",
                        "typed_config": {
                            "@type": "type.googleapis.com/envoy.extensions.filters.network.tcp_proxy.v3.TcpProxy",
                            "stat_prefix": "transparent_tcp",
                            "cluster": "original_dst_cluster",
                        },
                    },
                ],
            },
        ],
    }
    config["static_resources"]["listeners"].append(transparent_listener)
    logger.info("Added transparent_tcp listener on port 15001")


def _add_original_dst_cluster(config: dict[str, Any]) -> None:
    """Add an ORIGINAL_DST cluster for transparent TCP proxying.

    EN-023-008: The ORIGINAL_DST cluster type selects upstream hosts
    based on the downstream connection's restored original destination.
    lb_policy must be CLUSTER_PROVIDED (mandatory for ORIGINAL_DST).

    Args:
        config: Mutable Envoy config dict to add the cluster to.
    """
    original_dst_cluster: dict[str, Any] = {
        "name": "original_dst_cluster",
        "type": "ORIGINAL_DST",
        "connect_timeout": "10s",
        "lb_policy": "CLUSTER_PROVIDED",
    }
    clusters = config["static_resources"].setdefault("clusters", [])
    clusters.append(original_dst_cluster)
    logger.info("Added original_dst_cluster (type: ORIGINAL_DST)")


def _load_scope(scope_path: Path) -> dict[str, Any]:
    """Load and validate an engagement scope YAML file."""
    if not scope_path.exists():
        msg = f"Scope file not found: {scope_path}"
        raise FileNotFoundError(msg)

    with scope_path.open() as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        msg = f"Scope file must contain a YAML mapping: {scope_path}"
        raise ScopeTranslationError(msg)

    if "engagement" not in data:
        msg = f"Scope file missing 'engagement' key: {scope_path}"
        raise ScopeTranslationError(msg)

    return data


def _extract_domains(targets: list[dict[str, str]]) -> list[str]:
    """Extract domain names from authorized_targets entries.

    Supports: domain, ip, url, cloud_account target types.
    Rejects: ip_range (requires RBAC filter, not supported in Phase 1).

    Returns:
        List of domain strings suitable for Envoy virtual_host domains.
    """
    domains: list[str] = []

    for target in targets:
        target_type = target.get("type", "")
        value = target.get("value", "").strip()

        if not value:
            logger.warning("Skipping empty target value: %s", target)
            continue

        if target_type == "domain":
            _validate_domain(value)
            # Add bare domain and :443 (for CONNECT/HTTPS).
            # Envoy CONNECT authority includes port suffix per GitHub #13704.
            # CLM-004: Wildcard subdomains are NOT auto-expanded. If subdomain
            # coverage is needed, the scope document must declare an explicit
            # wildcard entry (e.g., type: domain, value: "*.target.example.com").
            domains.append(value)
            domains.append(f"{value}:443")

        elif target_type == "ip":
            _validate_ipv4(value)
            domains.append(value)
            domains.append(f"{value}:443")

        elif target_type == "url":
            # Extract host from URL
            # CLM-004: No wildcard auto-expansion for URL targets either.
            host = _extract_host_from_url(value)
            _validate_domain(host)
            domains.append(host)
            domains.append(f"{host}:443")

        elif target_type == "cloud_account":
            # Map cloud provider to API domains
            cloud_domains = _resolve_cloud_account(value)
            # Add :443 suffix for each cloud domain (CONNECT support)
            for cd in list(cloud_domains):
                cloud_domains.append(f"{cd}:443")
            domains.extend(cloud_domains)

        elif target_type == "ip_range":
            msg = (
                f"ip_range targets are not supported in Phase 1 scope translation. "
                f"Use type: ip for individual IPs or type: domain. Got: {value}"
            )
            raise ScopeTranslationError(msg)

        else:
            logger.warning("Unknown target type '%s', skipping: %s", target_type, target)

    return domains


def _validate_domain(domain: str) -> None:
    """Validate a domain string."""
    if not _DOMAIN_PATTERN.match(domain):
        msg = f"Invalid domain format: {domain}"
        raise ScopeTranslationError(msg)


def _validate_ipv4(ip: str) -> None:
    """Validate an IPv4 address."""
    if not _IPV4_PATTERN.match(ip):
        msg = f"Invalid IPv4 address: {ip}"
        raise ScopeTranslationError(msg)
    # Check octet ranges
    octets = ip.split(".")
    for octet in octets:
        if int(octet) > 255:
            msg = f"Invalid IPv4 octet value in: {ip}"
            raise ScopeTranslationError(msg)


def _extract_host_from_url(url: str) -> str:
    """Extract the hostname from a URL."""
    # Remove protocol
    if "://" in url:
        url = url.split("://", 1)[1]
    # Remove path
    host = url.split("/", 1)[0]
    # Remove port
    host = host.split(":", 1)[0]
    return host


def _resolve_cloud_account(value: str) -> list[str]:
    """Resolve a cloud_account target to API endpoint domains.

    Expected format: "provider:account_id" (e.g., "aws:123456789012")
    """
    if ":" not in value:
        msg = f"cloud_account must be 'provider:account_id', got: {value}"
        raise ScopeTranslationError(msg)

    provider = value.split(":", 1)[0].lower()
    if provider not in _CLOUD_PROVIDER_DOMAINS:
        msg = (
            f"Unknown cloud provider '{provider}' in cloud_account target. "
            f"Supported: {', '.join(_CLOUD_PROVIDER_DOMAINS.keys())}"
        )
        raise ScopeTranslationError(msg)

    return list(_CLOUD_PROVIDER_DOMAINS[provider])


def _find_deny_all_index(virtual_hosts: list[dict[str, Any]]) -> int:
    """Find the index of the deny_all virtual_host (must be last).

    Raises:
        ScopeTranslationError: If no deny_all catch-all is found. The
            deny_all entry is a hard OPSEC requirement — without it,
            Envoy passes through unmatched routes instead of blocking them.
    """
    for i, vhost in enumerate(virtual_hosts):
        if vhost.get("name") == "deny_all":
            return i
        domains = vhost.get("domains", [])
        if "*" in domains and len(domains) == 1:
            return i
    msg = (
        "Base Envoy config is missing the deny_all catch-all virtual_host. "
        "Without deny_all, out-of-scope destinations are silently reachable. "
        "Add a virtual_host with domains: ['*'] and a direct_response 403 action."
    )
    raise ScopeTranslationError(msg)
