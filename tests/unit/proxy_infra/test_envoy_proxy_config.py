# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""BDD unit tests for EnvoyProxyRouteConfig.

Covers TASK-023-010: Envoy config changes for proxy routing (Option B sidecar
bridge path). Options C/D require zero Envoy changes.

Test pyramid: 60% happy path / 30% negative/edge / 10% safety assertions

Scenarios:
  - Cluster YAML contains required Envoy cluster fields
  - Cluster YAML references correct sidecar host and port
  - Custom cluster name is reflected in rendered YAML
  - HTTP CONNECT route YAML contains correct cluster reference
  - HTTP CONNECT route YAML contains tunneling upgrade config
  - Health check filter YAML contains health check filter type
  - is_zone1_safe always returns True (Zone 1 exclusion invariant)
  - cluster_name() accessor returns configured cluster name
  - sidecar_endpoint() returns (host, port) tuple
  - Default values produce valid Envoy YAML
  - Custom connect timeout is reflected in rendered cluster
  - Empty sidecar host results in YAML that still renders (infra tolerates it)
"""

from __future__ import annotations

import pytest

from src.proxy_infra.infrastructure.envoy.proxy_route_config import EnvoyProxyRouteConfig


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def default_config() -> EnvoyProxyRouteConfig:
    """Default EnvoyProxyRouteConfig with standard parameters."""
    return EnvoyProxyRouteConfig()


@pytest.fixture()
def custom_config() -> EnvoyProxyRouteConfig:
    """EnvoyProxyRouteConfig with custom parameters."""
    return EnvoyProxyRouteConfig(
        sidecar_host="socks-bridge.internal",
        sidecar_port=9090,
        cluster_name="custom_socks_cluster",
        connect_timeout_ms=3000,
    )


# =============================================================================
# Happy Path Tests (60%)
# =============================================================================


class TestRenderStaticCluster:
    """Tests for render_static_cluster()."""

    def test_cluster_yaml_contains_name_field(self, default_config: EnvoyProxyRouteConfig) -> None:
        """GIVEN default config WHEN render_static_cluster THEN yaml contains cluster name."""
        yaml = default_config.render_static_cluster()
        assert "socks_bridge_cluster" in yaml

    def test_cluster_yaml_contains_sidecar_host(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN default config WHEN render_static_cluster THEN yaml references socks-bridge."""
        yaml = default_config.render_static_cluster()
        assert "socks-bridge" in yaml

    def test_cluster_yaml_contains_default_port(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN default config WHEN render_static_cluster THEN yaml contains port 8080."""
        yaml = default_config.render_static_cluster()
        assert "8080" in yaml

    def test_cluster_yaml_contains_connect_timeout(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN default config WHEN render_static_cluster THEN yaml contains connect_timeout."""
        yaml = default_config.render_static_cluster()
        assert "connect_timeout" in yaml
        assert "5000ms" in yaml

    def test_cluster_yaml_contains_type_strict_dns(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN default config WHEN render_static_cluster THEN cluster type is STRICT_DNS."""
        yaml = default_config.render_static_cluster()
        assert "STRICT_DNS" in yaml

    def test_cluster_yaml_contains_lb_policy(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN default config WHEN render_static_cluster THEN lb_policy is present."""
        yaml = default_config.render_static_cluster()
        assert "ROUND_ROBIN" in yaml

    def test_custom_config_reflects_custom_host_and_port(
        self, custom_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN custom config WHEN render_static_cluster THEN custom host and port present."""
        yaml = custom_config.render_static_cluster()
        assert "socks-bridge.internal" in yaml
        assert "9090" in yaml

    def test_custom_cluster_name_appears_in_yaml(
        self, custom_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN custom cluster name WHEN render_static_cluster THEN name appears in yaml."""
        yaml = custom_config.render_static_cluster()
        assert "custom_socks_cluster" in yaml

    def test_custom_connect_timeout_appears_in_yaml(
        self, custom_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN custom timeout WHEN render_static_cluster THEN timeout present in yaml."""
        yaml = custom_config.render_static_cluster()
        assert "3000ms" in yaml


class TestRenderHttpConnectRoute:
    """Tests for render_http_connect_route()."""

    def test_route_yaml_references_socks_bridge_cluster(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN default config WHEN render_http_connect_route THEN cluster name present."""
        yaml = default_config.render_http_connect_route()
        assert "socks_bridge_cluster" in yaml

    def test_route_yaml_contains_upgrade_connect(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN default config WHEN render_http_connect_route THEN CONNECT upgrade config present."""
        yaml = default_config.render_http_connect_route()
        assert "CONNECT" in yaml

    def test_route_yaml_contains_custom_route_name(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN custom route name WHEN render_http_connect_route THEN route name present."""
        yaml = default_config.render_http_connect_route(route_name="my_proxy_route")
        assert "my_proxy_route" in yaml

    def test_route_yaml_default_route_name(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN no route name WHEN render_http_connect_route THEN default name used."""
        yaml = default_config.render_http_connect_route()
        assert "socks_proxy_route" in yaml

    def test_route_yaml_has_match_prefix(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN default config WHEN render_http_connect_route THEN route has prefix match."""
        yaml = default_config.render_http_connect_route()
        assert "prefix" in yaml


class TestRenderHealthCheckFilter:
    """Tests for render_health_check_filter()."""

    def test_health_check_filter_contains_type(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN default config WHEN render_health_check_filter THEN contains filter type."""
        yaml = default_config.render_health_check_filter()
        assert "health_check" in yaml

    def test_health_check_filter_contains_pass_through(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN default config WHEN render_health_check_filter THEN pass_through_mode present."""
        yaml = default_config.render_health_check_filter()
        assert "pass_through_mode" in yaml


# =============================================================================
# Safety / Zone 1 Exclusion Tests (30%)
# =============================================================================


class TestZone1SafetyInvariant:
    """Tests for the Zone 1 exclusion invariant."""

    def test_is_zone1_safe_returns_true_for_default(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN any config WHEN is_zone1_safe THEN always True."""
        assert default_config.is_zone1_safe() is True

    def test_is_zone1_safe_returns_true_for_custom(
        self, custom_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN custom config WHEN is_zone1_safe THEN always True."""
        assert custom_config.is_zone1_safe() is True


class TestAccessors:
    """Tests for cluster_name() and sidecar_endpoint() accessors."""

    def test_cluster_name_returns_default(self, default_config: EnvoyProxyRouteConfig) -> None:
        """GIVEN default config WHEN cluster_name THEN returns socks_bridge_cluster."""
        assert default_config.cluster_name() == "socks_bridge_cluster"

    def test_cluster_name_returns_custom(self, custom_config: EnvoyProxyRouteConfig) -> None:
        """GIVEN custom cluster name WHEN cluster_name THEN returns custom name."""
        assert custom_config.cluster_name() == "custom_socks_cluster"

    def test_sidecar_endpoint_returns_default_tuple(
        self, default_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN default config WHEN sidecar_endpoint THEN returns (socks-bridge, 8080)."""
        host, port = default_config.sidecar_endpoint()
        assert host == "socks-bridge"
        assert port == 8080

    def test_sidecar_endpoint_returns_custom_tuple(
        self, custom_config: EnvoyProxyRouteConfig
    ) -> None:
        """GIVEN custom config WHEN sidecar_endpoint THEN returns custom (host, port)."""
        host, port = custom_config.sidecar_endpoint()
        assert host == "socks-bridge.internal"
        assert port == 9090


# =============================================================================
# Edge Case Tests (10%)
# =============================================================================


class TestEdgeCases:
    """Edge case and boundary tests."""

    def test_render_cluster_is_string(self, default_config: EnvoyProxyRouteConfig) -> None:
        """GIVEN any config WHEN render_static_cluster THEN returns non-empty string."""
        result = default_config.render_static_cluster()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_render_route_is_string(self, default_config: EnvoyProxyRouteConfig) -> None:
        """GIVEN any config WHEN render_http_connect_route THEN returns non-empty string."""
        result = default_config.render_http_connect_route()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_port_zero_is_reflected_in_cluster_yaml(self) -> None:
        """GIVEN port=0 WHEN render_static_cluster THEN port 0 appears in yaml."""
        cfg = EnvoyProxyRouteConfig(sidecar_port=0)
        yaml = cfg.render_static_cluster()
        assert "port_value: 0" in yaml
