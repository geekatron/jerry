# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak
"""Unit tests for Envoy original_dst transparent TCP listener configuration.

EN-023-008 TASK-023-162: Verify that scope_translator.py generates the
original_dst listener filter and ORIGINAL_DST cluster alongside the
existing HTTP forward proxy configuration.

The original_dst listener provides transparent TCP proxying as groundwork
for full Envoy integration. In the current architecture, raw TCP scope
enforcement is via SocksBridge (not Envoy). The original_dst cluster is
added for future unification (requires 3 BPF programs per ps-researcher
finding).

BDD RED phase (H-20):
    These tests FAIL initially because scope_translator.py does not
    generate original_dst configuration yet.

No mocks. Tests inspect generated YAML structure.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.tool_exec.infrastructure.envoy.scope_translator import (
    generate_envoy_config,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


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
            "engagement_id": "RBW-TEST-ORIGINALDST",
            "authorized_targets": [
                {"type": "domain", "value": "target.example.com"},
            ],
        }
    }
    scope_path.write_text(yaml.dump(scope_data))
    return scope_path


@pytest.fixture()
def base_envoy_config(tmp_path: Path) -> Path:
    """Create a base Envoy config template with deny_all catch-all."""
    config_path = tmp_path / "envoy-base.yaml"
    config = {
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
                                        "stat_prefix": "egress",
                                        "route_config": {
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
                                            ]
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
                    "type": "LOGICAL_DNS",
                    "connect_timeout": "5s",
                    "lb_policy": "ROUND_ROBIN",
                }
            ],
        }
    }
    config_path.write_text(yaml.dump(config, default_flow_style=False))
    return config_path


# ---------------------------------------------------------------------------
# Tests — RED phase (H-20: all must FAIL initially)
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestEnvoyOriginalDstListener:
    """Verify generated Envoy config includes original_dst listener filter."""

    def test_envoy_config_has_original_dst_listener_filter(
        self,
        basic_scope: Path,
        base_envoy_config: Path,
        tmp_path: Path,
    ) -> None:
        """Given a scope and base config, the generated Envoy config includes
        an original_dst listener filter on a transparent TCP listener.

        RED: Fails because scope_translator.py does not generate
        original_dst listener filter.
        """
        output_path = tmp_path / "generated-envoy.yaml"
        generate_envoy_config(
            base_envoy_config,
            basic_scope,
            output_path,
            zone=2,
        )

        with output_path.open() as f:
            # Skip comment lines
            lines = f.readlines()
            yaml_content = "".join(line for line in lines if not line.startswith("#"))
            config = yaml.safe_load(yaml_content)

        listeners = config["static_resources"]["listeners"]
        listener_names = [lis["name"] for lis in listeners]

        assert "transparent_tcp" in listener_names, (
            f"Expected 'transparent_tcp' listener, got: {listener_names}"
        )

        transparent = next(lis for lis in listeners if lis["name"] == "transparent_tcp")
        listener_filter_names = [lf["name"] for lf in transparent.get("listener_filters", [])]
        assert "envoy.filters.listener.original_dst" in listener_filter_names, (
            f"Expected original_dst listener filter, got: {listener_filter_names}"
        )

    def test_envoy_config_has_original_dst_cluster(
        self,
        basic_scope: Path,
        base_envoy_config: Path,
        tmp_path: Path,
    ) -> None:
        """Given a scope and base config, the generated Envoy config includes
        an ORIGINAL_DST cluster with lb_policy CLUSTER_PROVIDED.

        RED: Fails because scope_translator.py does not generate
        ORIGINAL_DST cluster.
        """
        output_path = tmp_path / "generated-envoy.yaml"
        generate_envoy_config(
            base_envoy_config,
            basic_scope,
            output_path,
            zone=2,
        )

        with output_path.open() as f:
            lines = f.readlines()
            yaml_content = "".join(line for line in lines if not line.startswith("#"))
            config = yaml.safe_load(yaml_content)

        clusters = config["static_resources"]["clusters"]
        cluster_names = [c["name"] for c in clusters]

        assert "original_dst_cluster" in cluster_names, (
            f"Expected 'original_dst_cluster', got: {cluster_names}"
        )

        original_dst = next(c for c in clusters if c["name"] == "original_dst_cluster")
        assert original_dst["type"] == "ORIGINAL_DST", (
            f"Expected type ORIGINAL_DST, got: {original_dst.get('type')}"
        )
        assert original_dst["lb_policy"] == "CLUSTER_PROVIDED", (
            f"Expected lb_policy CLUSTER_PROVIDED, got: {original_dst.get('lb_policy')}"
        )

    def test_existing_http_forward_proxy_unchanged(
        self,
        basic_scope: Path,
        base_envoy_config: Path,
        tmp_path: Path,
    ) -> None:
        """Given a scope and base config, the existing HTTP forward proxy
        listener on port 3128 is preserved alongside the new transparent_tcp
        listener.

        RED: May fail if generate_envoy_config crashes on the new
        transparent_tcp requirement.
        """
        output_path = tmp_path / "generated-envoy.yaml"
        generate_envoy_config(
            base_envoy_config,
            basic_scope,
            output_path,
            zone=2,
        )

        with output_path.open() as f:
            lines = f.readlines()
            yaml_content = "".join(line for line in lines if not line.startswith("#"))
            config = yaml.safe_load(yaml_content)

        listeners = config["static_resources"]["listeners"]
        listener_names = [lis["name"] for lis in listeners]

        assert "egress_proxy" in listener_names, (
            f"Expected 'egress_proxy' listener preserved, got: {listener_names}"
        )

        egress = next(lis for lis in listeners if lis["name"] == "egress_proxy")
        port = egress["address"]["socket_address"]["port_value"]
        assert port == 3128, f"Expected egress_proxy on port 3128, got: {port}"
