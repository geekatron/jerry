# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Factory for provisioner adapter selection.

Routes provider name + feature flag to the correct ProxyProvisionerPort
implementation. The default backend for digitalocean is
TerraformProvisionerAdapter (ADR-EN023-003 Option C). The legacy
DigitalOceanProvisionerAdapter is available via JERRY_PROVISIONER_BACKEND=legacy.

References:
    - TASK-023-104: Bootstrap + CLI integration
    - ADR-EN023-003: Infrastructure provisioning (Option C: Hybrid)
"""

from __future__ import annotations

import os
from pathlib import Path

from src.proxy_infra.domain.ports.proxy_provisioner_port import ProxyProvisionerPort

#: Valid backend values for JERRY_PROVISIONER_BACKEND.
_VALID_BACKENDS = ("terraform", "legacy")


def create_provisioner_adapter(
    provider: str,
    engagement_dir: Path,
    terraform_dir: Path | None = None,
) -> ProxyProvisionerPort:
    """Create a provisioner adapter based on provider and feature flag.

    Selection logic:
    1. Read ``JERRY_PROVISIONER_BACKEND`` env var (default: "terraform").
    2. If "terraform": return ``TerraformProvisionerAdapter``.
    3. If "legacy": return ``DigitalOceanProvisionerAdapter``.
    4. Otherwise: raise ``ValueError`` listing valid values.

    Args:
        provider: Cloud provider name (e.g., "digitalocean").
        engagement_dir: Engagement-scoped directory for state files.
        terraform_dir: Optional override for terraform working directory.
            Defaults to ``{engagement_dir}/terraform/``.

    Returns:
        Configured ProxyProvisionerPort implementation.

    Raises:
        ValueError: If JERRY_PROVISIONER_BACKEND contains an unrecognised value.
    """
    backend = os.environ.get("JERRY_PROVISIONER_BACKEND", "terraform").lower()

    if backend not in _VALID_BACKENDS:
        raise ValueError(
            f"JERRY_PROVISIONER_BACKEND='{backend}' is not recognised — "
            f"valid values are: {', '.join(_VALID_BACKENDS)} "
            f"(terraform=default, legacy=DigitalOcean pydo SDK fallback)"
        )

    if backend == "legacy":
        from src.proxy_infra.infrastructure.adapters.digitalocean_adapter import (
            DigitalOceanProvisionerAdapter,
        )

        return DigitalOceanProvisionerAdapter.from_env(
            engagement_id="",
        )

    from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
        TerraformProvisionerAdapter,
    )

    return TerraformProvisionerAdapter(
        engagement_dir=engagement_dir,
    )
