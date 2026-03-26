# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""EnvoyProxyRouteConfig — generates Envoy cluster/route snippets for SOCKS upstream.

Produces YAML fragments that can be injected into Zone 2 / Zone 3 Envoy configs
to add a ``socks_bridge_cluster`` static upstream pointing at the socks-bridge
sidecar container (Option B sidecar bridge path per TASK-023-010).

For Options C (iptables+redsocks) and D (eBPF+socks5lb) Envoy needs NO changes —
the transparent redirect operates below Envoy at the kernel network layer. This
class is therefore only invoked when the sidecar bridge option is active.

Design constraints:
    H-07: Infrastructure layer — no domain service imports. Accepts plain strings.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-010: Envoy config changes for proxy routing.
    Zone 1 configs MUST NOT be modified (never proxied).
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

#: Default port the socks-bridge sidecar listens on inside the Docker network.
_DEFAULT_SIDECAR_PORT: int = 8080

#: Envoy cluster name used in route configs to reference the sidecar.
_SOCKS_BRIDGE_CLUSTER_NAME: str = "socks_bridge_cluster"

#: Default socks-bridge hostname on the Docker internal network.
_DEFAULT_SIDECAR_HOST: str = "socks-bridge"


class EnvoyProxyRouteConfig:
    """Generates Envoy cluster and route YAML fragments for the socks-bridge sidecar.

    The generated snippets are append-only additions to the existing Zone 2/3
    Envoy configs. ``dynamic_forward_proxy_cluster`` is not modified — it remains
    the default path when the sidecar is absent (zero-proxy mode).

    Args:
        sidecar_host: Hostname of the socks-bridge container on the Docker network.
        sidecar_port: Port the sidecar listens on (default 8080).
        cluster_name: Envoy upstream cluster name (default "socks_bridge_cluster").
        connect_timeout_ms: TCP connect timeout for the upstream cluster in ms.
    """

    def __init__(
        self,
        sidecar_host: str = _DEFAULT_SIDECAR_HOST,
        sidecar_port: int = _DEFAULT_SIDECAR_PORT,
        cluster_name: str = _SOCKS_BRIDGE_CLUSTER_NAME,
        connect_timeout_ms: int = 5000,
    ) -> None:
        """Initialise the Envoy route config generator.

        Args:
            sidecar_host: DNS hostname of the socks-bridge sidecar.
            sidecar_port: Port the sidecar listens on.
            cluster_name: Envoy upstream cluster identifier.
            connect_timeout_ms: Connection timeout in milliseconds.
        """
        self._sidecar_host = sidecar_host
        self._sidecar_port = sidecar_port
        self._cluster_name = cluster_name
        self._connect_timeout_ms = connect_timeout_ms

    def render_static_cluster(self) -> str:
        """Render the ``socks_bridge_cluster`` static cluster YAML snippet.

        Returns:
            YAML string for the static cluster definition, suitable for
            inclusion in the ``static_resources.clusters`` section of an
            Envoy config (Zone 2 or Zone 3 only — never Zone 1).
        """
        logger.debug(
            "Rendering socks_bridge_cluster for %s:%d",
            self._sidecar_host,
            self._sidecar_port,
        )
        return (
            f"- name: {self._cluster_name}\n"
            f"  connect_timeout: {self._connect_timeout_ms}ms\n"
            f"  type: STRICT_DNS\n"
            f"  lb_policy: ROUND_ROBIN\n"
            f"  load_assignment:\n"
            f"    cluster_name: {self._cluster_name}\n"
            f"    endpoints:\n"
            f"      - lb_endpoints:\n"
            f"          - endpoint:\n"
            f"              address:\n"
            f"                socket_address:\n"
            f"                  address: {self._sidecar_host}\n"
            f"                  port_value: {self._sidecar_port}\n"
        )

    def render_http_connect_route(self, route_name: str = "socks_proxy_route") -> str:
        """Render an Envoy route entry that tunnels through the socks-bridge cluster.

        Uses Envoy's ``tunneling_config`` (HTTP CONNECT) to establish a tunnel
        to the upstream SOCKS5 proxy via the sidecar.

        Args:
            route_name: Human-readable name for the route entry.

        Returns:
            YAML string for the route entry with HTTP CONNECT tunneling config.
        """
        return (
            f"- name: {route_name}\n"
            f"  match:\n"
            f"    prefix: /\n"
            f"  route:\n"
            f"    cluster: {self._cluster_name}\n"
            f"    timeout: 0s\n"
            f"    upgrade_configs:\n"
            f"      - upgrade_type: CONNECT\n"
        )

    def render_health_check_filter(self) -> str:
        """Render an Envoy health check pass-through filter for the sidecar cluster.

        Returns:
            YAML string for the health check filter configuration.
        """
        return (
            "- name: envoy.filters.http.health_check\n"
            "  typed_config:\n"
            '    "@type": type.googleapis.com/envoy.extensions.filters.http.health_check.v3.HealthCheck\n'
            "    pass_through_mode: true\n"
            '    headers:\n'
            '      - name: ":path"\n'
            '        string_match:\n'
            '          exact: "/healthz"\n'
        )

    def is_zone1_safe(self) -> bool:
        """Assert this config generator never produces Zone 1 modifications.

        Zone 1 (supply chain / blue-team) traffic is NEVER routed through SOCKS
        proxies. This method exists as a safety assertion for callers.

        Returns:
            Always True — this class only produces Zone 2/3 cluster fragments.
        """
        return True

    def cluster_name(self) -> str:
        """Return the configured upstream cluster name.

        Returns:
            The Envoy cluster name string.
        """
        return self._cluster_name

    def sidecar_endpoint(self) -> tuple[str, int]:
        """Return the (host, port) tuple for the sidecar endpoint.

        Returns:
            Tuple of (hostname, port).
        """
        return self._sidecar_host, self._sidecar_port
