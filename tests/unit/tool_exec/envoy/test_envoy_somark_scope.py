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
        """Transparent TCP listener has a deny-all default filter chain.

        The last filter chain has no filter_chain_match (catch-all) and routes
        to a deny cluster, blocking all TCP destinations not in engagement scope.
        """
        listener = _find_listener(generated_config, "transparent_tcp")
        assert listener is not None, "transparent_tcp listener not found"

        filter_chains = listener.get("filter_chains", [])
        assert len(filter_chains) >= 2, (
            "transparent_tcp must have at least 2 filter chains "
            "(scope-allowed + deny-all catch-all)"
        )

        # Last filter chain is the deny-all catch-all (no filter_chain_match)
        deny_chain = filter_chains[-1]
        assert "filter_chain_match" not in deny_chain, (
            "Deny-all filter chain must not have filter_chain_match (catch-all)"
        )

        # Deny chain routes to deny_all_tcp cluster
        tcp_proxy = deny_chain["filters"][0]
        tcp_proxy_config = tcp_proxy["typed_config"]
        assert tcp_proxy_config["cluster"] == "deny_all_tcp", (
            f"Deny chain must route to deny_all_tcp cluster, got {tcp_proxy_config.get('cluster')}"
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
        """Both egress_proxy and transparent_tcp reference the same engagement scope domains.

        The HTTP forward proxy uses virtual_host domains. The transparent TCP
        listener uses filter_chain_match server_names. Both must contain the
        same set of scope-derived domains.
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

        # Extract TCP filter chain server_names (excluding deny-all catch-all)
        tcp = _find_listener(generated_config, "transparent_tcp")
        assert tcp is not None
        tcp_domains: set[str] = set()
        for chain in tcp.get("filter_chains", []):
            match = chain.get("filter_chain_match", {})
            server_names = match.get("server_names", [])
            tcp_domains.update(server_names)

        # Both must reference the same scope domains
        assert len(http_domains) > 0, "No HTTP scope domains found"
        assert len(tcp_domains) > 0, "No TCP scope domains found"
        assert http_domains == tcp_domains, (
            f"HTTP and TCP scope domains differ.\n"
            f"HTTP: {sorted(http_domains)}\n"
            f"TCP:  {sorted(tcp_domains)}"
        )
