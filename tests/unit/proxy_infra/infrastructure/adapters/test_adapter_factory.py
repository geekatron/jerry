# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""RED phase tests for TASK-023-104: Bootstrap + CLI Integration.

Tests verify:
1. Factory creates TerraformProvisionerAdapter by default for digitalocean
2. Factory creates legacy adapter when JERRY_PROVISIONER_BACKEND=legacy
3. Invalid backend value raises ValueError
4. Default terraform dir is engagement-scoped

All tests MUST FAIL before implementation (H-20 RED phase).
"""

from __future__ import annotations

from pathlib import Path

import pytest


class TestAdapterFactory:
    """Tests for provisioner adapter factory."""

    def test_factory_creates_terraform_adapter_for_digitalocean(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Default for digitalocean provider is TerraformProvisionerAdapter."""
        from src.proxy_infra.infrastructure.adapters.provisioner_adapter_factory import (
            create_provisioner_adapter,
        )
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        monkeypatch.delenv("JERRY_PROVISIONER_BACKEND", raising=False)

        adapter = create_provisioner_adapter(
            provider="digitalocean",
            engagement_dir=tmp_path,
        )

        assert isinstance(adapter, TerraformProvisionerAdapter)

    def test_factory_creates_legacy_adapter_when_feature_flag_set(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """JERRY_PROVISIONER_BACKEND=legacy creates DigitalOceanProvisionerAdapter."""
        from src.proxy_infra.infrastructure.adapters.digitalocean_adapter import (
            DigitalOceanProvisionerAdapter,
        )
        from src.proxy_infra.infrastructure.adapters.provisioner_adapter_factory import (
            create_provisioner_adapter,
        )

        monkeypatch.setenv("JERRY_PROVISIONER_BACKEND", "legacy")
        monkeypatch.setenv("JERRY_PROXY_DO_API_KEY", "test-key-for-factory")

        adapter = create_provisioner_adapter(
            provider="digitalocean",
            engagement_dir=tmp_path,
        )

        assert isinstance(adapter, DigitalOceanProvisionerAdapter)

    def test_factory_raises_on_invalid_backend_value(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Unrecognized JERRY_PROVISIONER_BACKEND value raises ValueError."""
        from src.proxy_infra.infrastructure.adapters.provisioner_adapter_factory import (
            create_provisioner_adapter,
        )

        monkeypatch.setenv("JERRY_PROVISIONER_BACKEND", "invalid_typo")

        with pytest.raises(ValueError, match="terraform.*legacy"):
            create_provisioner_adapter(
                provider="digitalocean",
                engagement_dir=tmp_path,
            )

    def test_default_terraform_dir_is_engagement_scoped(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Default terraform work_dir should be {engagement_dir}/terraform/."""
        from src.proxy_infra.infrastructure.adapters.provisioner_adapter_factory import (
            create_provisioner_adapter,
        )
        from src.proxy_infra.infrastructure.adapters.terraform_provisioner_adapter import (
            TerraformProvisionerAdapter,
        )

        monkeypatch.delenv("JERRY_PROVISIONER_BACKEND", raising=False)

        adapter = create_provisioner_adapter(
            provider="digitalocean",
            engagement_dir=tmp_path,
        )

        assert isinstance(adapter, TerraformProvisionerAdapter)
        assert adapter._work_dir == tmp_path / "terraform"
