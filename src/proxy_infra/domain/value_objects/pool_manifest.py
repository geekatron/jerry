# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""PoolManifest value object — serializable pool state with integrity verification.

The manifest is the integration contract between the proxy_infra bounded context
and the Container Lifecycle Manager (CLM). Written by proxy_infra, read by CLM.

References:
    - ADR-PROJ023-008: CLI Bounded Context Architecture for Proxy Infrastructure
    - EPIC-023-007: Proxy infrastructure automation
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.proxy_infra.domain.value_objects.proxy_pool import ProxyPool


@dataclass(frozen=True)
class PoolManifest:
    """Serializable pool state with integrity verification.

    The manifest is the integration contract between the proxy_infra
    bounded context and the CLM. Written by proxy_infra, read by CLM.

    Attributes:
        version: Manifest schema version.
        engagement_id: Owning engagement.
        pool: Current pool state.
        integrity_hash: SHA-256 of the serialized pool data (excluding this field).
        updated_at: UTC timestamp of last modification.
        audit_trail: List of operation descriptions for traceability.
    """

    version: str
    engagement_id: str
    pool: ProxyPool
    integrity_hash: str
    updated_at: datetime
    audit_trail: tuple[str, ...] = field(default_factory=tuple)
