# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SidecarComposeGenerator — generates Docker Compose service stanzas for socks-bridge.

Produces a Docker Compose v3 service fragment for the socks-bridge sidecar.
The sidecar is profile-gated (``profiles: ["socks"]``) and only starts when
``--profile socks`` is passed to ``docker compose up``.

Design constraints:
    H-07: Infrastructure layer — no domain service imports.
    H-10: One public class per file.
    H-11: All public methods have type annotations.
    TASK-023-012: Docker Compose socks-bridge sidecar service.
    Zone 1 (supply chain / blue-team) MUST NOT include the socks-bridge service.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

#: Docker Compose profile that activates the sidecar.
_SOCKS_PROFILE: str = "socks"

#: Default socks-bridge Docker image tag.
_DEFAULT_IMAGE: str = "ghcr.io/geekatron/socks-bridge:latest"

#: Default port the sidecar listens on inside the Docker network.
_DEFAULT_SIDECAR_PORT: int = 8080

#: Health check endpoint path.
_HEALTH_CHECK_PATH: str = "/health"


class SidecarComposeGenerator:
    """Generates Docker Compose YAML service stanzas for the socks-bridge sidecar.

    The generated service:
    - Uses ``profiles: ["socks"]`` so it only starts with ``--profile socks``
    - Attaches to both the internal zone network and the egress network
    - Injects ``SOCKS_PROXY_POOL``, ``SOCKS_LB_STRATEGY``, ``SOCKS_FAIL_CLOSED``
      from host environment variables (${VAR:-default} syntax)
    - Exposes no ports to the host — internal Docker network only
    - Includes a health check on the /health endpoint

    Args:
        zone: Zone identifier for network names (e.g. "zone3-exploit").
        image: Docker image for the socks-bridge container.
        sidecar_port: Port the sidecar listens on inside the container.
    """

    def __init__(
        self,
        zone: str,
        image: str = _DEFAULT_IMAGE,
        sidecar_port: int = _DEFAULT_SIDECAR_PORT,
    ) -> None:
        """Initialise the sidecar compose generator.

        Args:
            zone: Zone network name prefix (e.g. ``"zone3-exploit"``).
            image: Full Docker image reference for the socks-bridge container.
            sidecar_port: Port the sidecar container listens on.

        Raises:
            ValueError: If zone is empty.
        """
        if not zone or not zone.strip():
            raise ValueError("zone must be a non-empty string")
        self._zone = zone.strip()
        self._image = image
        self._sidecar_port = sidecar_port

    def render_service(self) -> str:
        """Render the socks-bridge service stanza for a Docker Compose file.

        The generated YAML:
        - Is gated by ``profiles: ["socks"]`` — no-op when profile absent
        - Attaches to both the internal zone network and the egress network
        - Does NOT expose any ports to the host
        - Includes a liveness health check

        Returns:
            YAML string for the ``socks-bridge`` service definition.
        """
        logger.debug("Rendering socks-bridge Compose service for zone=%s", self._zone)
        return (
            "  socks-bridge:\n"
            f"    image: {self._image}\n"
            f"    profiles:\n"
            f'      - "{_SOCKS_PROFILE}"\n'
            f"    networks:\n"
            f"      - {self._zone}\n"
            f"      - {self._zone}-egress\n"
            f"    environment:\n"
            f"      SOCKS_PROXY_POOL: ${{SOCKS_PROXY_POOL:-}}\n"
            f"      SOCKS_LB_STRATEGY: ${{SOCKS_LB_STRATEGY:-random}}\n"
            f"      SOCKS_FAIL_CLOSED: ${{SOCKS_FAIL_CLOSED:-true}}\n"
            f"    healthcheck:\n"
            f"      test:\n"
            f'        - "CMD"\n'
            f'        - "curl"\n'
            f'        - "-f"\n'
            f'        - "http://localhost:{self._sidecar_port}{_HEALTH_CHECK_PATH}"\n'
            f"      interval: 30s\n"
            f"      timeout: 5s\n"
            f"      retries: 3\n"
            f"    restart: unless-stopped\n"
        )

    def render_egress_network(self) -> str:
        """Render the egress network definition for the Compose networks section.

        Returns:
            YAML string for the ``{zone}-egress`` network definition.
        """
        return (
            f"  {self._zone}-egress:\n"
            f"    driver: bridge\n"
        )

    def zone(self) -> str:
        """Return the zone name this generator is configured for.

        Returns:
            Zone identifier string.
        """
        return self._zone

    def sidecar_port(self) -> int:
        """Return the configured sidecar port.

        Returns:
            Port integer the sidecar listens on.
        """
        return self._sidecar_port
