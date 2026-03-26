# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Sidecar access logging infrastructure for the proxy bounded context.

Provides structured JSONL access logging for proxied connections, mounted
to a host volume for CLM consumption and post-engagement forensics.

References:
    - TASK-023-044: Sidecar JSON Access Logging with Volume Mount
    - T-SP-05: Without access logs, compromised sidecar traffic cannot be
      reconstructed during incident response.
"""

from src.proxy_infra.infrastructure.logging.sidecar_access_logger import SidecarAccessLogger

__all__ = ["SidecarAccessLogger"]
