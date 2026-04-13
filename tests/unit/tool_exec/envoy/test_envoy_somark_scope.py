# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD tests for Envoy SO_MARK + transparent TCP scope enforcement.

TASK-023-172 RED phase: These tests MUST fail before implementation.
GREEN phase: Modify scope_translator.py to make them pass.

Modifications under test:
    - original_dst_cluster has socket_options with SO_MARK=100
    - transparent_tcp listener enforces scope via filter chain matching
    - HTTP forward proxy on port 3128 is unchanged
    - Both listeners derive from the same engagement scope
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.tool_exec.infrastructure.envoy.scope_translator import (
    generate_envoy_config,
)


@pytest.fixture()
def scope_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for scope files."""
    return tmp_path / "scopes"


@pytest.fixture()
def basic_scope(scope_dir: Path) -> Path:
    """Create a basic engagement scope with domain targets."""
    scope_dir.mkdir(parents=True, exist_ok=True)
    scope_path = scope_dir / "scope.yaml"
    scope_data = {
        "engagement": {
            "engagement_id": "RBW-SOMARK-001",
            "authorized_targets": [
                {"type": "domain", "value": "target.example.com"},
                {"type": "domain", "value": "api.example.com"},
            ],
        }
    }
    scope_path.write_text(yaml.dump(scope_data))
    return scope_path


@pytest.fixture()
def zone2_base_config(tmp_path: Path) -> Path:
    """Create a minimal Zone 2 base Envoy config with deny_all."""
    config_path = tmp_path / "envoy-zone2-base.yaml"
    config_data = {
        "admin": {"address": {"socket_address": {"address": "0.0.0.0", "port_value": 9901}}},
        "static_resources": {
            "listeners": [
                {
                    "name": "egress_proxy",
                    "address": {"socket_address": {"address": "0.0.0.0", "port_value": 3128}},
                    "filter_chains": [
                        {
                            "filters": [
                                {
                                    "name": "envoy.filters.network.http_connection_manager",
                                    "typed_config": {
                                        "@type": "type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager",
                                        "stat_prefix": "zone2_test",
                                        "upgrade_configs": [{"upgrade_type": "CONNECT"}],
                                        "http_filters": [
                                            {
                                                "name": "envoy.filters.http.router",
                                                "typed_config": {},
                                            },
                                        ],
                                        "route_config": {
                                            "name": "zone2_test_routes",
                                            "virtual_hosts": [
                                                {
                                                    "name": "deny_all",
                                                    "domains": ["*"],
                                                    "routes": [
                                                        {
                                                            "match": {"prefix": "/"},
                                                            "direct_response": {
                                                                "status": 403,
                                                                "body": {"inline_string": "DENIED"},
                                                            },
                                                        }
                                                    ],
                                                }
                                            ],
                                        },
                                    },
                                }
                            ]
                        }
                    ],
                }
            ],
            "clusters": [
                {
                    "name": "dynamic_forward_proxy_cluster",
                    "lb_policy": "CLUSTER_PROVIDED",
                }
            ],
        },
    }
    config_path.write_text(yaml.dump(config_data, default_flow_style=False))
    return config_path


@pytest.fixture()
def generated_config(zone2_base_config: Path, basic_scope: Path, tmp_path: Path) -> dict:
    """Generate an Envoy config and return the parsed YAML dict."""
    output = tmp_path / "generated-somark.yaml"
    generate_envoy_config(zone2_base_config, basic_scope, output, zone=2)
    with output.open() as f:
        return yaml.safe_load(f)


def _find_listener(config: dict, name: str) -> dict | None:
    """Find a listener by name in the Envoy config."""
    for listener in config.get("static_resources", {}).get("listeners", []):
        if listener.get("name") == name:
            return listener
    return None


def _find_cluster(config: dict, name: str) -> dict | None:
    """Find a cluster by name in the Envoy config."""
    for cluster in config.get("static_resources", {}).get("clusters", []):
        if cluster.get("name") == name:
            return cluster
    return None


class TestOriginalDstClusterSomark:
    """AC-1: original_dst_cluster must have SO_MARK=100 socket_options."""

    def test_original_dst_cluster_has_somark(self, generated_config: dict) -> None:
        """Generated YAML includes socket_options with SO_MARK=100 on original_dst_cluster.

        SO_MARK prevents BPF re-interception of Envoy upstream connections (C2).
        Linux socket option: level=1 (SOL_SOCKET), name=36 (SO_MARK), value=100.
        """
        cluster = _find_cluster(generated_config, "original_dst_cluster")
        assert cluster is not None, "original_dst_cluster not found in generated config"

        # SO_MARK must be in upstream_bind_config.socket_options
        bind_config = cluster.get("upstream_bind_config", {})
        socket_options = bind_config.get("socket_options", [])
        assert len(socket_options) > 0, "No socket_options on original_dst_cluster"

        somark_option = None
        for opt in socket_options:
            if opt.get("name") == 36 and opt.get("level") == 1:
                somark_option = opt
                break

        assert somark_option is not None, "SO_MARK option (level=1, name=36) not found"
        assert somark_option["int_value"] == 100, (
            f"SO_MARK value must be 100 (C2), got {somark_option.get('int_value')}"
        )


class TestTransparentTcpScopeEnforcement:
    """AC-2: transparent_tcp listener must deny out-of-scope destinations."""

    def test_transparent_tcp_denies_out_of_scope(self, generated_config: dict) -> None:
        """Transparent TCP listener uses RBAC to deny out-of-scope destinations.

        BUG-023-002/DEC-023-002: RBAC network filter with ALLOW policy replaces
        the old server_names filter chain match + deny-all catch-all. Connections
        to destinations NOT in the RBAC policy are denied by RBAC before reaching
        the tcp_proxy filter.
        """
        listener = _find_listener(generated_config, "transparent_tcp")
        assert listener is not None, "transparent_tcp listener not found"

        filter_chains = listener.get("filter_chains", [])
        assert len(filter_chains) >= 1, "transparent_tcp must have at least 1 filter chain"

        # First filter chain must have RBAC as the first filter
        scope_chain = filter_chains[0]
        rbac_filter = scope_chain["filters"][0]
        assert "rbac" in rbac_filter["name"], (
            f"First filter must be RBAC, got {rbac_filter['name']}"
        )

        # RBAC must use ALLOW action (deny everything not matched)
        rbac_config = rbac_filter["typed_config"]
        rules = rbac_config.get("rules", {})
        assert rules.get("action") == "ALLOW", (
            f"RBAC must use ALLOW action (implicit deny), got {rules.get('action')}"
        )


class TestHttpForwardProxyUnchanged:
    """AC-3: HTTP forward proxy on port 3128 must be unchanged."""

    def test_http_forward_proxy_unchanged(self, generated_config: dict) -> None:
        """Egress proxy listener on port 3128 is unaffected by SO_MARK changes.

        Regression test: the HTTP forward proxy configuration must not change
        when transparent TCP scope enforcement is added.
        """
        listener = _find_listener(generated_config, "egress_proxy")
        assert listener is not None, "egress_proxy listener not found"

        # Port must still be 3128
        port = listener["address"]["socket_address"]["port_value"]
        assert port == 3128, f"egress_proxy port changed from 3128 to {port}"

        # Must still have HTTP connection manager
        hcm_filter = listener["filter_chains"][0]["filters"][0]
        assert "http_connection_manager" in hcm_filter["name"]

        # Must still have deny_all virtual_host
        hcm_config = hcm_filter["typed_config"]
        virtual_hosts = hcm_config["route_config"]["virtual_hosts"]
        deny_all = next((vh for vh in virtual_hosts if vh.get("name") == "deny_all"), None)
        assert deny_all is not None, "deny_all virtual_host missing from egress_proxy"


class TestBothListenersFromSameScope:
    """AC-4: Both listeners derive allowed destinations from the same scope."""

    def test_both_listeners_generated_from_same_scope(self, generated_config: dict) -> None:
        """Both egress_proxy and transparent_tcp derive from the same engagement scope.

        BUG-023-002/DEC-023-002: The HTTP forward proxy uses virtual_host domains.
        The transparent TCP listener uses RBAC with hybrid permissions
        (requested_server_name for TLS + destination_ip for plain TCP).
        Both must contain scope-derived entries from the same scope document.
        """
        # Extract HTTP virtual_host domains (excluding deny_all)
        egress = _find_listener(generated_config, "egress_proxy")
        assert egress is not None
        hcm_config = egress["filter_chains"][0]["filters"][0]["typed_config"]
        virtual_hosts = hcm_config["route_config"]["virtual_hosts"]
        http_domains: set[str] = set()
        for vh in virtual_hosts:
            if vh.get("name") != "deny_all":
                http_domains.update(vh.get("domains", []))

        # Extract TCP RBAC scope entries (requested_server_name + destination_ip)
        tcp = _find_listener(generated_config, "transparent_tcp")
        assert tcp is not None
        rbac_filter = tcp["filter_chains"][0]["filters"][0]
        rbac_config = rbac_filter["typed_config"]
        policies = rbac_config.get("rules", {}).get("policies", {})
        scope_policy = policies.get("engagement_scope", {})
        permissions = scope_policy.get("permissions", [])

        # RBAC uses or_rules containing both server_name and IP entries
        tcp_scope_entries: set[str] = set()
        for perm in permissions:
            or_rules = perm.get("or_rules", {}).get("rules", [])
            for rule in or_rules:
                if "requested_server_name" in rule:
                    sni = rule["requested_server_name"]
                    name = sni.get("exact", sni.get("suffix", ""))
                    if name:
                        tcp_scope_entries.add(name)
                if "destination_ip" in rule:
                    ip = rule["destination_ip"].get("address_prefix", "")
                    if ip:
                        tcp_scope_entries.add(ip)

        # Both must have scope-derived entries
        assert len(http_domains) > 0, "No HTTP scope domains found"
        assert len(tcp_scope_entries) > 0, "No TCP RBAC scope entries found"

        # The TCP entries should contain server names that overlap with HTTP domains
        # (stripped of :443 suffixes). Not an exact match because TCP also has IPs.
        http_bare_domains = {d.split(":")[0] for d in http_domains}
        tcp_names = {e.lstrip(".") for e in tcp_scope_entries if not e[0].isdigit()}
        overlap = http_bare_domains & tcp_names
        assert len(overlap) > 0, (
            f"No overlap between HTTP domains and TCP SNI names.\n"
            f"HTTP domains: {sorted(http_bare_domains)}\n"
            f"TCP SNI names: {sorted(tcp_names)}\n"
            "Both listeners should derive from the same engagement scope."
        )
