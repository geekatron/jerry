# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""SidecarAccessLogger — JSONL access log for socks-bridge sidecar connections.

Security properties (APICALL-004 alignment):
    - write_entry() has NO password, token, api_key, credentials, or
      response_body parameter — credential material is structurally excluded
      from the log interface.
    - Only connection-level metadata is recorded: addresses, ports, byte
      counts, duration, status, and the proxy node identifier.

Log location (TASK-023-044 AC):
    Default: /var/log/jerry-proxy/access.json
    Docker Compose volume mount: ./logs/sidecar/:/var/log/jerry-proxy/:rw

Rotation constants (TASK-023-044 AC):
    MAX_FILE_SIZE_BYTES: 100MB maximum per file
    MAX_ROTATED_FILES:   3 rotated files retained

References:
    - TASK-023-044: Sidecar JSON Access Logging with Volume Mount
    - T-SP-05: Access log for incident response forensics
    - APICALL-004: Never log credentials or response bodies containing tokens
    - TASK-023-047: ConnectionLimiter logs rejection events here
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


class SidecarAccessLogger:
    """Append-only JSONL access logger for socks-bridge sidecar connections.

    Writes one JSON object per line (JSONL format) to the configured log
    file.  Each entry records connection-level metadata for every proxied
    connection through the sidecar.

    Security invariant (APICALL-004): write_entry() accepts only connection
    metadata — IP addresses, port, byte counts, duration, and status.
    No credential fields (passwords, tokens, API keys, SOCKS5 credentials)
    are accepted by the interface.  This structural constraint prevents
    accidental logging of authentication material.

    Rotation constants (TASK-023-044 AC):
        MAX_FILE_SIZE_BYTES: Maximum log file size in bytes (100MB).
        MAX_ROTATED_FILES: Number of rotated files retained (3).

    Attributes:
        log_path: Absolute path to the active JSONL access log file.
            Default: ``/var/log/jerry-proxy/access.json`` (Docker volume mount).
    """

    #: Maximum log file size in bytes before rotation (TASK-023-044 AC: 100MB).
    MAX_FILE_SIZE_BYTES: int = 100 * 1024 * 1024

    #: Maximum number of rotated log files retained (TASK-023-044 AC: 3 files).
    MAX_ROTATED_FILES: int = 3

    #: Production default — Docker Compose volume mount path (TASK-023-044 AC).
    _DEFAULT_LOG_PATH: Path = Path("/var/log/jerry-proxy/access.json")

    def __init__(self, log_path: Path | None = None) -> None:
        """Initialise the SidecarAccessLogger with an optional log file path.

        Args:
            log_path: Absolute path to the JSONL access log file.  Defaults
                to ``/var/log/jerry-proxy/access.json`` per the Docker Compose
                volume mount specification in TASK-023-044 AC.  Tests inject a
                temporary path to avoid touching the host filesystem.
        """
        self.log_path: Path = log_path if log_path is not None else self._DEFAULT_LOG_PATH

    def write_entry(
        self,
        *,
        src_ip: str,
        dst_ip: str,
        dst_port: int,
        proxy_node: str,
        bytes_sent: int,
        bytes_received: int,
        duration_ms: int,
        status: str,
    ) -> None:
        """Append one JSONL access record for a proxied connection.

        APICALL-004: This method intentionally has no ``password``,
        ``token``, ``api_key``, ``credentials``, or ``response_body``
        parameter.  Only connection-level metadata is persisted — never
        credential material which may contain SOCKS5 passwords, API tokens,
        or SSH private keys.

        Args:
            src_ip: Source IP address of the originating connection.
            dst_ip: Destination IP address of the proxied target.
            dst_port: Destination port number of the proxied target.
            proxy_node: Identifier of the SOCKS proxy node used for this
                connection (e.g., ``"node-fra-001"``).
            bytes_sent: Number of bytes transmitted from client to target.
            bytes_received: Number of bytes received from target to client.
            duration_ms: Total connection duration in milliseconds.
            status: Connection outcome — one of ``"success"``, ``"error"``,
                ``"timeout"``, or ``"rejected_max_connections"``.
        """
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "dst_port": dst_port,
            "proxy_node": proxy_node,
            "bytes_sent": bytes_sent,
            "bytes_received": bytes_received,
            "duration_ms": duration_ms,
            "status": status,
        }
        with self.log_path.open(mode="a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
