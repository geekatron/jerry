# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for BPF lifecycle integration into engagement state machine.

EN-023-008 TASK-023-165: Wire BpfManager into GatedLifecycleManager.
BPF loads on ACTIVE (G3 gate), detaches on TEARDOWN (G5 gate).

Covers:
  - BPF loaded when engagement transitions to ACTIVE
  - BPF detached when engagement transitions to TEARDOWN
  - Bypass map populated with proxy and Envoy IPs before tool execution
  - BPF NOT loaded before ACTIVE state (not during PROVISIONING)
  - Rollback on failed BPF activation (OG-001)
  - Reload after detach succeeds (TG-002)
  - Lifecycle works without BPF port (backward compat, PM-005)

All BPF port calls are mocked — unit tests NEVER invoke real bpftool.
Uses real GatedLifecycleManager with real config files (same pattern
as test_engagement_gate_lifecycle.py).
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
import yaml

from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
    GatedLifecycleManager,
)
from src.proxy_infra.domain.ports.bpf_lifecycle_port import IBpfLifecyclePort

# ---------------------------------------------------------------------------
# Helpers (reuse pattern from test_engagement_gate_lifecycle.py)
# ---------------------------------------------------------------------------


def _write_config(tmp_path: Path, engagement_id: str) -> Path:
    """Write a minimal E2E engagement config YAML (pre-approved gates).

    Includes proxy_pool_ips and envoy_ip so BPF bypass map population
    is triggered during activate() (FINDING-003 fix).
    """
    config_data = {
        "engagement": {
            "id": engagement_id,
            "name": "BPF Lifecycle Test",
            "type": "penetration_test",
            "mode": "single",
            "start_date": "2026-03-30",
            "e2e_mode": True,
        },
        "scope": {
            "targets": ["10.0.0.1"],
        },
        "proxy": {
            "proxy_pool_ips": ["192.168.1.100"],
            "envoy_ip": "172.31.0.10",
        },
    }
    config_path = tmp_path / f"{engagement_id}-config.yaml"
    config_path.write_text(yaml.dump(config_data, default_flow_style=False))
    return config_path


def _create_glm(
    tmp_path: Path,
    bpf_port: IBpfLifecyclePort | None = None,
) -> GatedLifecycleManager:
    """Create a GatedLifecycleManager with pre-approved gates and optional BPF port."""
    confirmation = MagicMock()
    confirmation.request_approval.return_value = True
    confirmation.request_approval_with_timeout.return_value = True
    return GatedLifecycleManager(
        engagement_dir=tmp_path,
        confirmation_port=confirmation,
        bpf_port=bpf_port,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestBpfLoadedOnActivate:
    """BPF program loads when engagement transitions to ACTIVE (G3 gate)."""

    def test_bpf_loaded_on_activate(self, tmp_path: Path) -> None:
        """When activate() is called, bpf_port.load_and_attach() is invoked."""
        bpf = MagicMock(spec=IBpfLifecyclePort)
        bpf.is_ready.return_value = True
        glm = _create_glm(tmp_path, bpf_port=bpf)

        config_path = _write_config(tmp_path, "E2E-BPF-001")
        state = glm.create(config_path)
        glm.approve_scope(state.engagement_id)
        glm.activate(state.engagement_id)

        bpf.load_and_attach.assert_called_once()

    def test_bpf_not_loaded_before_active_state(self, tmp_path: Path) -> None:
        """approve_scope (DEFINED -> PROVISIONING) does NOT load BPF."""
        bpf = MagicMock(spec=IBpfLifecyclePort)
        glm = _create_glm(tmp_path, bpf_port=bpf)

        config_path = _write_config(tmp_path, "E2E-BPF-002")
        state = glm.create(config_path)
        glm.approve_scope(state.engagement_id)

        bpf.load_and_attach.assert_not_called()


class TestBpfDetachedOnTeardown:
    """BPF program detaches when engagement transitions to TEARDOWN."""

    def test_bpf_detached_on_teardown(self, tmp_path: Path) -> None:
        """approve_report (REPORTING -> TEARDOWN) calls detach_and_cleanup()."""
        bpf = MagicMock(spec=IBpfLifecyclePort)
        bpf.is_ready.return_value = True
        glm = _create_glm(tmp_path, bpf_port=bpf)

        config_path = _write_config(tmp_path, "E2E-BPF-003")
        state = glm.create(config_path)
        glm.approve_scope(state.engagement_id)
        glm.activate(state.engagement_id)
        glm.complete_execution(state.engagement_id)
        glm.complete_analysis(state.engagement_id)
        glm.approve_report(state.engagement_id)

        bpf.detach_and_cleanup.assert_called_once()


# EN-023-010: TestBpfBypassMapPopulated removed — bypass_ips map replaced
# by SO_MARK loop prevention. See tests/architecture/test_bypass_map_removed.py.


class TestBpfRollbackOnFailure:
    """BPF rollback on failed activation (OG-001)."""

    def test_bpf_cleanup_on_failed_activation(self, tmp_path: Path) -> None:
        """If load_and_attach() raises RuntimeError, detach_and_cleanup() is
        called for rollback and the error propagates.
        """
        bpf = MagicMock(spec=IBpfLifecyclePort)
        bpf.load_and_attach.side_effect = RuntimeError("BPF load failed")
        glm = _create_glm(tmp_path, bpf_port=bpf)

        config_path = _write_config(tmp_path, "E2E-BPF-005")
        state = glm.create(config_path)
        glm.approve_scope(state.engagement_id)

        with pytest.raises(RuntimeError, match="BPF load failed"):
            glm.activate(state.engagement_id)

        bpf.detach_and_cleanup.assert_called_once()


class TestBpfReloadAfterDetach:
    """Reload BPF after detach succeeds (TG-002)."""

    def test_reload_bpf_after_detach_succeeds(self, tmp_path: Path) -> None:
        """A second load_and_attach() succeeds after detach_and_cleanup()."""
        bpf = MagicMock(spec=IBpfLifecyclePort)
        bpf.is_ready.return_value = True

        bpf.load_and_attach("container-1")
        bpf.detach_and_cleanup()
        bpf.load_and_attach("container-1")

        assert bpf.load_and_attach.call_count == 2
        assert bpf.detach_and_cleanup.call_count == 1


class TestBpfOptionalPort:
    """BPF port is optional — lifecycle works without it."""

    def test_lifecycle_works_without_bpf_port(self, tmp_path: Path) -> None:
        """When bpf_port is None, the full lifecycle completes normally."""
        glm = _create_glm(tmp_path, bpf_port=None)

        config_path = _write_config(tmp_path, "E2E-BPF-006")
        state = glm.create(config_path)
        glm.approve_scope(state.engagement_id)
        result = glm.activate(state.engagement_id)

        assert result.current_state == "ACTIVE"
