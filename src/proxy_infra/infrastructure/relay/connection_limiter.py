# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""ConnectionLimiter — per-proxy-node concurrent connection enforcement.

Enforces a maximum number of concurrent connections through the socks-bridge
sidecar, with per-proxy-node tracking to detect hot-spot imbalance.  Excess
connection attempts are rejected with HTTP 503 and the rejection event is
logged to the SidecarAccessLogger.

Threat addressed (T-SP-09): Without connection limits, a single misconfigured
tool can monopolize the entire proxy pool, exhausting resources or triggering
provider rate limits.

Configuration:
    JERRY_SIDECAR_MAX_CONNECTIONS: Environment variable to override the
    default maximum of 256 concurrent connections.

References:
    - TASK-023-047: Implement Sidecar Connection Limits
    - T-SP-09: Proxy pool resource exhaustion via runaway tool
    - TASK-023-044: SidecarAccessLogger (rejection events logged there)
"""

from __future__ import annotations

import json
import os
from collections import defaultdict

from src.proxy_infra.infrastructure.logging.sidecar_access_logger import SidecarAccessLogger

#: Environment variable name for overriding max concurrent connections.
_ENV_MAX_CONNECTIONS: str = "JERRY_SIDECAR_MAX_CONNECTIONS"

#: HTTP 503 rejection body template — TASK-023-047 AC.
_REJECTION_BODY_TEMPLATE: str = json.dumps(
    {"error": "proxy_pool_exhausted", "max_connections": None}
)


class ConnectionLimiter:
    """Per-proxy-node concurrent connection limiter for the socks-bridge sidecar.

    Tracks active connection counts per proxy node and enforces a configurable
    maximum.  When a connection attempt exceeds the limit, the limiter returns
    a rejection body (HTTP 503) and logs the rejection to the SidecarAccessLogger.

    Counting is done at the Python level (thread-local in the current
    implementation).  For production multi-threaded / async use, callers
    should protect ``try_acquire``/``release`` with an external lock if
    concurrency is required.

    Class constants:
        DEFAULT_MAX_CONNECTIONS: Default max concurrent connections (256).

    Attributes:
        max_connections: Configured maximum concurrent connections.
        logger: SidecarAccessLogger instance for rejection event logging.
    """

    #: Default maximum concurrent connections (TASK-023-047 AC: 256).
    DEFAULT_MAX_CONNECTIONS: int = 256

    def __init__(
        self,
        max_connections: int = DEFAULT_MAX_CONNECTIONS,
        logger: SidecarAccessLogger | None = None,
    ) -> None:
        """Initialise the ConnectionLimiter.

        Args:
            max_connections: Maximum number of concurrent connections allowed
                (default 256 per TASK-023-047 AC).  Configurable via
                ``JERRY_SIDECAR_MAX_CONNECTIONS`` environment variable using
                :meth:`from_env`.
            logger: SidecarAccessLogger instance to which rejection events are
                written.  When ``None``, rejection events are silently dropped
                (useful for unit tests that do not care about logging).
        """
        self.max_connections: int = max_connections
        self.logger: SidecarAccessLogger | None = logger
        # Per-node connection counters.  defaultdict(int) returns 0 for unseen nodes.
        self._counts: defaultdict[str, int] = defaultdict(int)

    @classmethod
    def from_env(
        cls,
        logger: SidecarAccessLogger | None = None,
    ) -> ConnectionLimiter:
        """Construct a ConnectionLimiter from environment variables.

        Reads ``JERRY_SIDECAR_MAX_CONNECTIONS`` to override the default.
        Falls back to :attr:`DEFAULT_MAX_CONNECTIONS` when the variable is
        absent or empty.

        Args:
            logger: SidecarAccessLogger instance for rejection logging.

        Returns:
            A new ConnectionLimiter configured from the environment.
        """
        raw = os.environ.get(_ENV_MAX_CONNECTIONS, "").strip()
        max_connections = int(raw) if raw else cls.DEFAULT_MAX_CONNECTIONS
        return cls(max_connections=max_connections, logger=logger)

    def try_acquire(
        self,
        *,
        proxy_node: str,
    ) -> tuple[bool, str | None]:
        """Attempt to acquire a connection slot on the given proxy node.

        Increments the per-node counter when a slot is available.  Returns
        the rejection body and logs the rejection when the limit is reached.

        Args:
            proxy_node: Identifier of the proxy node handling this connection
                (e.g., ``"node-fra-001"``).  Used for per-node tracking and
                for logging rejection events.

        Returns:
            A tuple of ``(accepted, body)`` where:
                - ``accepted`` is ``True`` when the connection was accepted,
                  ``False`` when rejected.
                - ``body`` is ``None`` when accepted, or a JSON string
                  containing ``{"error": "proxy_pool_exhausted",
                  "max_connections": N}`` when rejected (HTTP 503 body per
                  TASK-023-047 AC).
        """
        if self._counts[proxy_node] >= self.max_connections:
            self._log_rejection(proxy_node=proxy_node)
            rejection_body = json.dumps(
                {"error": "proxy_pool_exhausted", "max_connections": self.max_connections}
            )
            return False, rejection_body

        self._counts[proxy_node] += 1
        return True, None

    def release(self, *, proxy_node: str) -> None:
        """Release a previously acquired connection slot on the given proxy node.

        Decrements the per-node counter.  Safe to call even when the current
        count is already zero — guards against race conditions in teardown
        paths without raising exceptions.

        Args:
            proxy_node: Identifier of the proxy node whose slot is released.
        """
        if self._counts[proxy_node] > 0:
            self._counts[proxy_node] -= 1

    def active_count(self, proxy_node: str) -> int:
        """Return the current active connection count for a proxy node.

        Args:
            proxy_node: Identifier of the proxy node to query.

        Returns:
            Current active connection count.  Returns 0 for unseen nodes.
        """
        return self._counts[proxy_node]

    def all_node_counts(self) -> dict[str, int]:
        """Return a snapshot of active connection counts for all known nodes.

        Useful for hot-spot detection — callers can identify nodes with
        disproportionately high connection counts and route new connections
        elsewhere.

        Returns:
            A dict mapping proxy node identifier to its current active count.
            Only nodes that have had at least one connection attempt are
            included.
        """
        return dict(self._counts)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _log_rejection(self, *, proxy_node: str) -> None:
        """Log a connection rejection event to the sidecar access logger.

        Writes a zero-byte-count entry with ``status="rejected_max_connections"``
        so the rejection is visible in CLM and post-engagement forensics.

        Args:
            proxy_node: Identifier of the proxy node on which the rejection
                occurred.
        """
        if self.logger is None:
            return

        self.logger.write_entry(
            src_ip="0.0.0.0",
            dst_ip="0.0.0.0",
            dst_port=0,
            proxy_node=proxy_node,
            bytes_sent=0,
            bytes_received=0,
            duration_ms=0,
            status="rejected_max_connections",
        )
