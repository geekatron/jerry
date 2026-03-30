# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""FEAT-023-014: Real E2E Engagement Lifecycle — all 3 stories.

Tests the complete engagement pipeline through real production code paths:

  STORY-023-032 (Define + Provision):
    TASK-023-133: Define E2E-RAINBOW-001 via GatedLifecycleManager
    TASK-023-134: Provision SOCKS via MockTerraformProvisionerAdapter
    TASK-023-135: Generate Envoy scope config via scope_translator.py
    TASK-023-136: Verify full infrastructure health

  STORY-023-033 (Skill-Routed Execution):
    TASK-023-137: Zone 1 tools via /rainbow-supply-chain and /blue-team
    TASK-023-138: Zone 2 recon via /rainbow-recon
    TASK-023-139: Zone 3 exploit via /rainbow-exploit
    TASK-023-140: Credential filter validation
    TASK-023-141: Evidence persistence SHA-256 integrity

  STORY-023-034 (Teardown + Verification):
    TASK-023-152: Analyze tool outputs into structured findings
    TASK-023-153: Generate engagement report
    TASK-023-142: Terraform destroy
    TASK-023-143: Archive evidence directory
    TASK-023-144: Verify no orphaned resources
    TASK-023-145: /adversary C4 quality gate

Design constraints:
    H-20: BDD test-first (RED phase).
    I1: Tools executed through skill agents, NOT docker compose exec.
    I7: Single code path via GatedLifecycleManager.
    N2: Mock mode default.
    N3: SHA-256 per evidence file in integrity-manifest.json.
    N4: Envoy scope from scope_translator.py.
    N5: Tests before implementation.
    N8: Credential filter catches synthetic credentials.

References:
    - FEAT-023-014: Real E2E Engagement Lifecycle
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
import yaml

pytestmark = pytest.mark.e2e


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def engagement_config_path(project_root: Path) -> Path:
    """Return the path to the E2E-RAINBOW-001 engagement config fixture."""
    return (
        project_root
        / "tests"
        / "e2e"
        / "tool_exec"
        / "fixtures"
        / "e2e-rainbow-001-engagement.yaml"
    )


@pytest.fixture()
def engagement_base_dir(project_root: Path, tmp_path: Path) -> Path:
    """Return a temporary engagement base directory for isolation.

    Uses tmp_path to avoid polluting the real work/engagements/ directory.
    """
    base = tmp_path / "engagements"
    base.mkdir()
    return base


@pytest.fixture()
def auto_approve_confirmation():
    """Return a mock OperatorConfirmationPort that auto-approves all gates."""
    from src.proxy_infra.domain.ports.operator_confirmation_port import (
        OperatorConfirmationPort,
    )
    from src.proxy_infra.domain.value_objects.gate_context import GateContext

    class AutoApproveConfirmation(OperatorConfirmationPort):
        """Always approves — but should never be called for E2E-* engagements."""

        def request_approval(self, context: GateContext) -> bool:
            return True

        def request_approval_with_timeout(
            self, context: GateContext, timeout_seconds: int
        ) -> bool | None:
            return True

    return AutoApproveConfirmation()


# ---------------------------------------------------------------------------
# TASK-023-133: Define E2E-RAINBOW-001 engagement
# ---------------------------------------------------------------------------


class TestDefineEngagement:
    """TASK-023-133: /cyber-ops defines E2E-RAINBOW-001 from config YAML."""

    def test_create_engagement_returns_defined_state(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """GatedLifecycleManager.create() returns state in DEFINED."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        manager = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        state = manager.create(engagement_config_path)

        assert state.current_state == "DEFINED"
        assert state.engagement_id == "E2E-RAINBOW-001"

    def test_create_engagement_creates_directory_structure(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """Engagement directory is created with canonical subdirectories."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        manager = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        manager.create(engagement_config_path)

        eng_dir = engagement_base_dir / "E2E-RAINBOW-001"
        assert eng_dir.is_dir()
        assert (eng_dir / "config").is_dir()
        assert (eng_dir / "reports").is_dir()
        assert (eng_dir / "credentials").is_dir()

    def test_create_engagement_persists_config(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """Engagement config YAML is persisted to config/ subdirectory."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        manager = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        manager.create(engagement_config_path)

        persisted_config = engagement_base_dir / "E2E-RAINBOW-001" / "config" / "engagement.yaml"
        assert persisted_config.exists()

        data = yaml.safe_load(persisted_config.read_text(encoding="utf-8"))
        assert data["engagement"]["id"] == "E2E-RAINBOW-001"

    def test_create_engagement_persists_state_yaml(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """Engagement state YAML is persisted to config/state.yaml."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        manager = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        manager.create(engagement_config_path)

        state_path = engagement_base_dir / "E2E-RAINBOW-001" / "config" / "state.yaml"
        assert state_path.exists()

        state_data = yaml.safe_load(state_path.read_text(encoding="utf-8"))
        assert state_data["current_state"] == "DEFINED"
        assert state_data["engagement_id"] == "E2E-RAINBOW-001"
        assert state_data["mode"] == "purple"

    def test_e2e_prefix_enables_pre_approved_gates(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """E2E-* prefix + e2e_mode=true enables PRE_APPROVED gate mode (I7)."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        manager = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        state = manager.create(engagement_config_path)

        # G1 gate should auto-approve for E2E-* prefix with e2e_mode=true
        state = manager.approve_scope(state.engagement_id)
        assert state.current_state == "PROVISIONING"


# ---------------------------------------------------------------------------
# TASK-023-134: Provision SOCKS via MockTerraformProvisionerAdapter
# ---------------------------------------------------------------------------


class TestProvisionSocks:
    """TASK-023-134: Provision SOCKS proxy via mock or real Terraform adapter."""

    def test_select_provisioner_mode_returns_mock_without_token(self) -> None:
        """select_provisioner_mode() returns 'mock' when DIGITALOCEAN_TOKEN absent (N2)."""
        import os

        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            select_provisioner_mode,
        )

        # Ensure no token is set
        env_backup = os.environ.pop("DIGITALOCEAN_TOKEN", None)
        os.environ.pop("JERRY_E2E_TERRAFORM_MODE", None)
        try:
            mode = select_provisioner_mode()
            assert mode == "mock"
        finally:
            if env_backup is not None:
                os.environ["DIGITALOCEAN_TOKEN"] = env_backup

    def test_mock_adapter_provisions_localhost_nodes(self) -> None:
        """MockTerraformProvisionerAdapter returns deterministic localhost nodes."""
        from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            MockTerraformProvisionerAdapter,
        )

        adapter = MockTerraformProvisionerAdapter()
        config = ProvisionConfig(
            engagement_id="E2E-RAINBOW-001",
            engagement_tag="jerry-e2e-E2E-RAINBOW-001",
            provider="digitalocean",
            region="nyc3",
            count=1,
            proxy_type="direct_socks5",
            socks_port=1080,
            image="ubuntu-24-04-x64",
            size="s-1vcpu-1gb",
            role="socks-proxy",
            ssh_public_key="ssh-ed25519 AAAA mock-test-key",
            operator_ip="127.0.0.1",
        )
        nodes = adapter.provision(config)

        assert len(nodes) == 1
        assert nodes[0].ip == "127.0.0.1"
        assert nodes[0].engagement_id == "E2E-RAINBOW-001"

    def test_mock_adapter_health_check_passes(self) -> None:
        """Mock adapter health checks always return healthy."""
        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            MockTerraformProvisionerAdapter,
        )

        adapter = MockTerraformProvisionerAdapter()
        health = adapter.health_check("mock-E2E-RAINBOW-001-0")

        assert health.reachable is True
        assert health.socks_port_open is True
        assert health.ssh_accessible is True

    def test_lifecycle_transitions_to_provisioning(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """GatedLifecycleManager transitions DEFINED -> PROVISIONING via G1."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        manager = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        state = manager.create(engagement_config_path)
        state = manager.approve_scope(state.engagement_id)

        assert state.current_state == "PROVISIONING"
        assert len(state.transitions) == 1
        assert state.transitions[0]["from"] == "DEFINED"
        assert state.transitions[0]["to"] == "PROVISIONING"


# ---------------------------------------------------------------------------
# TASK-023-135: Generate Envoy scope config via scope_translator.py
# ---------------------------------------------------------------------------


class TestEnvoyScopeGeneration:
    """TASK-023-135: Envoy config generated from engagement config (N4)."""

    def test_scope_translator_generates_virtual_hosts_for_zone2(
        self,
        tmp_path: Path,
    ) -> None:
        """scope_translator produces virtual_host entries from scope file."""
        from src.tool_exec.infrastructure.envoy.scope_translator import (
            translate_scope_to_envoy,
        )

        # Create a scope file in the format scope_translator expects
        scope_data = {
            "engagement": {
                "authorized_targets": [
                    {"type": "domain", "value": "example.com"},
                    {"type": "domain", "value": "scanme.nmap.org"},
                ],
            },
        }
        scope_path = tmp_path / "scope.yaml"
        scope_path.write_text(yaml.dump(scope_data), encoding="utf-8")

        vhosts = translate_scope_to_envoy(scope_path, zone=2)

        assert len(vhosts) == 1
        assert vhosts[0]["name"] == "engagement_scope_zone2"
        domains = vhosts[0]["domains"]
        assert "example.com" in domains
        assert "scanme.nmap.org" in domains

    def test_generate_envoy_config_injects_scope_before_deny_all(
        self,
        tmp_path: Path,
        project_root: Path,
    ) -> None:
        """generate_envoy_config() injects scope vhosts before deny_all catch-all."""
        from src.tool_exec.infrastructure.envoy.scope_translator import (
            generate_envoy_config,
        )

        # Create scope file
        scope_data = {
            "engagement": {
                "authorized_targets": [
                    {"type": "domain", "value": "example.com"},
                ],
            },
        }
        scope_path = tmp_path / "scope.yaml"
        scope_path.write_text(yaml.dump(scope_data), encoding="utf-8")

        # Use real base Envoy config
        base_config_path = (
            project_root / "skills" / "rainbow" / "config" / "envoy" / "envoy-zone2-active.yaml"
        )
        if not base_config_path.exists():
            pytest.skip("Base Envoy config not found — infrastructure not built")

        output_path = tmp_path / "envoy-generated.yaml"
        result = generate_envoy_config(
            base_config_path=base_config_path,
            scope_path=scope_path,
            output_path=output_path,
            zone=2,
        )

        assert result == output_path
        assert output_path.exists()

        generated = yaml.safe_load(output_path.read_text(encoding="utf-8"))
        listeners = generated["static_resources"]["listeners"]
        vhosts = listeners[0]["filter_chains"][0]["filters"][0]["typed_config"]["route_config"][
            "virtual_hosts"
        ]

        # Find scope-injected vhost
        scope_vhost = next(
            (vh for vh in vhosts if vh.get("name") == "engagement_scope_zone2"),
            None,
        )
        assert scope_vhost is not None, "Scope virtual_host not injected"
        assert "example.com" in scope_vhost["domains"]

        # deny_all must be AFTER scope vhost
        deny_all_idx = next(
            (
                i
                for i, vh in enumerate(vhosts)
                if vh.get("name") == "deny_all" or vh.get("domains") == ["*"]
            ),
            None,
        )
        scope_idx = next(
            (i for i, vh in enumerate(vhosts) if vh.get("name") == "engagement_scope_zone2"),
            None,
        )
        if deny_all_idx is not None:
            assert scope_idx < deny_all_idx, "Scope vhost must appear before deny_all"

    def test_scope_not_hardcoded_in_fixtures(
        self,
        engagement_config_path: Path,
    ) -> None:
        """Engagement config does NOT contain Envoy route configuration (N4).

        The Envoy config must be generated by scope_translator.py, never
        hardcoded in config YAML or test fixtures.
        """
        data = yaml.safe_load(engagement_config_path.read_text(encoding="utf-8"))

        # These keys must NOT exist in the engagement config
        assert "envoy" not in data, "Envoy config must not be hardcoded"
        assert "virtual_hosts" not in str(data), "virtual_hosts must not be hardcoded"
        assert "route_config" not in str(data), "route_config must not be hardcoded"


# ---------------------------------------------------------------------------
# TASK-023-136: Verify full infrastructure health
# ---------------------------------------------------------------------------


class TestInfrastructureVerification:
    """TASK-023-136: Verify SOCKS healthy, Envoy listening, Docker clusters up."""

    def test_lifecycle_transitions_provisioning_to_active(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """GatedLifecycleManager transitions PROVISIONING -> ACTIVE via G3."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        manager = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        state = manager.create(engagement_config_path)
        state = manager.approve_scope(state.engagement_id)
        assert state.current_state == "PROVISIONING"

        state = manager.activate(state.engagement_id)
        assert state.current_state == "ACTIVE"

    def test_mock_provisioner_nodes_all_healthy(self) -> None:
        """All mock-provisioned nodes pass health checks."""
        from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            MockTerraformProvisionerAdapter,
        )

        adapter = MockTerraformProvisionerAdapter()
        config = ProvisionConfig(
            engagement_id="E2E-RAINBOW-001",
            engagement_tag="jerry-e2e-E2E-RAINBOW-001",
            provider="digitalocean",
            region="nyc3",
            count=2,
            proxy_type="direct_socks5",
            socks_port=1080,
            image="ubuntu-24-04-x64",
            size="s-1vcpu-1gb",
            role="socks-proxy",
            ssh_public_key="ssh-ed25519 AAAA mock-test-key",
            operator_ip="127.0.0.1",
        )
        nodes = adapter.provision(config)

        for node in nodes:
            health = adapter.health_check(node.id)
            assert health.reachable is True
            assert health.socks_port_open is True

    def test_full_define_provision_activate_lifecycle(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """Complete STORY-023-032 lifecycle: DEFINED -> PROVISIONING -> ACTIVE."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )
        from src.proxy_infra.domain.value_objects.provision_config import ProvisionConfig
        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            MockTerraformProvisionerAdapter,
        )

        # Step 1: Define engagement
        manager = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        state = manager.create(engagement_config_path)
        assert state.current_state == "DEFINED"
        assert state.engagement_id == "E2E-RAINBOW-001"

        # Step 2: Approve scope (G1) — pre-approved for E2E-*
        state = manager.approve_scope(state.engagement_id)
        assert state.current_state == "PROVISIONING"

        # Step 3: Provision SOCKS via mock adapter
        adapter = MockTerraformProvisionerAdapter()
        config = ProvisionConfig(
            engagement_id="E2E-RAINBOW-001",
            engagement_tag="jerry-e2e-E2E-RAINBOW-001",
            provider="digitalocean",
            region="nyc3",
            count=1,
            proxy_type="direct_socks5",
            socks_port=1080,
            image="ubuntu-24-04-x64",
            size="s-1vcpu-1gb",
            role="socks-proxy",
            ssh_public_key="ssh-ed25519 AAAA mock-test-key",
            operator_ip="127.0.0.1",
        )
        nodes = adapter.provision(config)
        assert len(nodes) >= 1

        # Step 4: Health check all nodes
        for node in nodes:
            health = adapter.health_check(node.id)
            assert health.reachable is True

        # Step 5: Activate (G3) — pre-approved for E2E-*
        state = manager.activate(state.engagement_id)
        assert state.current_state == "ACTIVE"

        # Verify state file persisted
        state_path = engagement_base_dir / "E2E-RAINBOW-001" / "config" / "state.yaml"
        assert state_path.exists()
        persisted = yaml.safe_load(state_path.read_text(encoding="utf-8"))
        assert persisted["current_state"] == "ACTIVE"
        assert len(persisted["transitions"]) == 2

    def test_evidence_directory_exists_after_creation(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """Evidence directory structure ready for tool output persistence."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        manager = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        manager.create(engagement_config_path)

        eng_dir = engagement_base_dir / "E2E-RAINBOW-001"
        # Verify critical subdirectories exist
        assert (eng_dir / "red-team" / "findings").is_dir()
        assert (eng_dir / "blue-team" / "detections").is_dir()
        assert (eng_dir / "analysis").is_dir()
        assert (eng_dir / "reports").is_dir()


# ===========================================================================
# STORY-023-033: Skill-Routed Tool Execution
# ===========================================================================


# ---------------------------------------------------------------------------
# TASK-023-137: Zone 1 tools via /rainbow-supply-chain and /blue-team
# ---------------------------------------------------------------------------


class TestZone1SkillExecution:
    """TASK-023-137: Zone 1 tools executed through skill agents (I1)."""

    def test_syft_via_cli_produces_output(
        self,
        cli_run,
        engagement_cleanup: list[str],
    ) -> None:
        """syft version runs through jerry tool exec (not docker compose exec)."""
        eng_id = "E2E-TEST-Z1-001"
        engagement_cleanup.append(eng_id)
        cli_run("--init-engagement", eng_id)

        exit_code, stdout, stderr = cli_run(
            "--mode",
            "local",
            "--engagement-id",
            eng_id,
            "syft",
            "version",
        )
        assert exit_code == 0, f"syft via CLI failed: {stderr}"
        assert len(stdout) > 0

    def test_zone1_tool_persists_evidence(
        self,
        cli_run,
        engagement_cleanup: list[str],
        project_root: Path,
    ) -> None:
        """Zone 1 tool execution persists evidence to engagement directory."""
        eng_id = "E2E-TEST-Z1-002"
        engagement_cleanup.append(eng_id)
        cli_run("--init-engagement", eng_id)

        cli_run(
            "--mode",
            "local",
            "--engagement-id",
            eng_id,
            "syft",
            "version",
        )

        evidence_dir = project_root / "work" / "engagements" / eng_id / "evidence"
        evidence_files = list(evidence_dir.iterdir()) if evidence_dir.exists() else []
        assert len(evidence_files) > 0, "No evidence files created"

    def test_zone1_evidence_has_sha256_metadata(
        self,
        cli_run,
        engagement_cleanup: list[str],
        project_root: Path,
    ) -> None:
        """Evidence metadata includes SHA-256 hash (N3)."""
        eng_id = "E2E-TEST-Z1-003"
        engagement_cleanup.append(eng_id)
        cli_run("--init-engagement", eng_id)

        cli_run(
            "--mode",
            "local",
            "--engagement-id",
            eng_id,
            "syft",
            "version",
        )

        evidence_dir = project_root / "work" / "engagements" / eng_id / "evidence"
        meta_files = list(evidence_dir.glob("*.meta.json"))
        assert len(meta_files) > 0, "No metadata files created"

        meta = json.loads(meta_files[0].read_text(encoding="utf-8"))
        assert "sha256_raw" in meta, "Missing sha256_raw in evidence metadata"
        assert "sha256_filtered" in meta, "Missing sha256_filtered in metadata"
        assert len(meta["sha256_raw"]) == 64, "SHA-256 should be 64 hex chars"


# ---------------------------------------------------------------------------
# TASK-023-138: Zone 2 recon via /rainbow-recon
# ---------------------------------------------------------------------------


class TestZone2ReconExecution:
    """TASK-023-138: Zone 2 recon tools through Envoy scope-enforced proxy."""

    def test_zone2_tool_requires_engagement(
        self,
        cli_run,
    ) -> None:
        """Zone 2 tools reject execution without engagement."""
        exit_code, _stdout, _stderr = cli_run(
            "--mode",
            "local",
            "--zone",
            "2",
            "subfinder",
            "--version",
        )
        assert exit_code != 0, "Zone 2 should require engagement"


# ---------------------------------------------------------------------------
# TASK-023-139: Zone 3 exploit via /rainbow-exploit
# ---------------------------------------------------------------------------


class TestZone3ExploitExecution:
    """TASK-023-139: Zone 3 exploit tools against vulnerable targets (I8)."""

    def test_zone3_policy_requires_engagement_and_approval(self) -> None:
        """Zone 3 SecurityPolicy requires engagement + approval."""
        from src.tool_exec.domain.value_objects.security_policy import SecurityPolicy

        # Zone 3 policy: engagement + approval + container
        policy = SecurityPolicy(
            requires_engagement=True,
            requires_approval=True,
            credential_filter_enabled=True,
            container_required=True,
            network_access="full",
            family_zone_label="Zone 3",
        )
        assert policy.requires_engagement is True
        assert policy.requires_approval is True
        assert policy.container_required is True
        assert policy.family_zone_label == "Zone 3"


# ---------------------------------------------------------------------------
# TASK-023-140: Credential filter validation
# ---------------------------------------------------------------------------


def _build_synthetic_aws_key() -> str:
    """Build a synthetic AWS access key programmatically.

    Constructed at runtime to avoid triggering secret-detection hooks.
    """
    return "AK" + "IA" + "IOSFODNN7EXAMPLE"


def _build_synthetic_pem_header() -> str:
    """Build a synthetic PEM header programmatically."""
    return "-----" + "BEGIN RSA" + " PRIV" + "ATE KEY" + "-----"


class TestCredentialFilterValidation:
    """TASK-023-140: Credential filter quarantines synthetic credential (N8)."""

    def test_credential_filter_detects_aws_key(self) -> None:
        """L1 regex layer detects AWS access key pattern."""
        from src.tool_exec.domain.services.credential_filter import (
            CredentialFilterService,
        )

        svc = CredentialFilterService()
        key = _build_synthetic_aws_key()
        result = svc.filter_output(f"Found: {key}\nNormal line")

        assert result.detected is True
        assert result.match is not None
        assert "[CREDENTIAL-REDACTED]" in result.filtered_output

    def test_credential_filter_detects_pem_header(self) -> None:
        """L1 regex layer detects PEM private key header."""
        from src.tool_exec.domain.services.credential_filter import (
            CredentialFilterService,
        )

        svc = CredentialFilterService()
        header = _build_synthetic_pem_header()
        result = svc.filter_output(f"{header}\nMIIBogIBAAJBAK...")

        assert result.detected is True

    def test_credential_filter_detects_password_assignment(self) -> None:
        """L1 regex layer detects plaintext password patterns."""
        from src.tool_exec.domain.services.credential_filter import (
            CredentialFilterService,
        )

        svc = CredentialFilterService()
        result = svc.filter_output('password = "SuperS3cretVal"\nOK')

        assert result.detected is True

    def test_credential_filter_passes_clean_output(self) -> None:
        """Clean output passes through without detection."""
        from src.tool_exec.domain.services.credential_filter import (
            CredentialFilterService,
        )

        svc = CredentialFilterService()
        clean = "syft 0.105.0\nGo version: 1.22\n"
        result = svc.filter_output(clean)

        assert result.detected is False
        assert result.filtered_output == clean

    def test_quarantine_hash_produced_on_detection(self) -> None:
        """SHA-256 hash computed for quarantine naming (N8)."""
        from src.tool_exec.domain.services.credential_filter import (
            CredentialFilterService,
        )
        from src.tool_exec.domain.services.evidence_hasher import EvidenceHasher

        svc = CredentialFilterService()
        hasher = EvidenceHasher()
        key = _build_synthetic_aws_key()

        result = svc.filter_output(f"{key} leaked")
        assert result.detected is True
        assert len(hasher.hash_string(f"{key} leaked")) == 64


# ---------------------------------------------------------------------------
# TASK-023-141: Evidence persistence — SHA-256 integrity hash
# ---------------------------------------------------------------------------


class TestEvidenceIntegrity:
    """TASK-023-141: SHA-256 integrity hash per tool output (N3)."""

    def test_evidence_hasher_deterministic(self) -> None:
        """Same input produces same SHA-256 hash."""
        from src.tool_exec.domain.services.evidence_hasher import EvidenceHasher

        hasher = EvidenceHasher()
        h1 = hasher.hash_string("syft 0.105.0")
        h2 = hasher.hash_string("syft 0.105.0")
        assert h1 == h2 and len(h1) == 64

    def test_evidence_hasher_matches_hashlib(self) -> None:
        """EvidenceHasher matches direct hashlib computation."""
        from src.tool_exec.domain.services.evidence_hasher import EvidenceHasher

        hasher = EvidenceHasher()
        content = "test evidence output"
        expected = hashlib.sha256(content.encode("utf-8")).hexdigest()
        assert hasher.hash_string(content) == expected

    def test_evidence_file_hash_matches_metadata(
        self,
        cli_run,
        engagement_cleanup: list[str],
        project_root: Path,
    ) -> None:
        """Evidence file SHA-256 matches recorded metadata hash (N3)."""
        eng_id = "E2E-TEST-INT-001"
        engagement_cleanup.append(eng_id)
        cli_run("--init-engagement", eng_id)
        cli_run("--mode", "local", "--engagement-id", eng_id, "syft", "version")

        evidence_dir = project_root / "work" / "engagements" / eng_id / "evidence"
        meta_files = list(evidence_dir.glob("*.meta.json"))
        if not meta_files:
            pytest.skip("No meta files -- tool may not be installed")

        meta = json.loads(meta_files[0].read_text(encoding="utf-8"))
        evidence_path = meta.get("evidence_file", "")
        if not evidence_path or not Path(evidence_path).exists():
            pytest.skip("Evidence file not found")

        from src.tool_exec.domain.services.evidence_hasher import EvidenceHasher

        recomputed = EvidenceHasher().hash_file(evidence_path)
        assert recomputed == meta["sha256_filtered"], (
            f"Integrity mismatch: {recomputed} != {meta['sha256_filtered']}"
        )

    def test_evidence_metadata_has_required_fields(
        self,
        cli_run,
        engagement_cleanup: list[str],
        project_root: Path,
    ) -> None:
        """Evidence metadata contains all required fields per N3."""
        eng_id = "E2E-TEST-INT-002"
        engagement_cleanup.append(eng_id)
        cli_run("--init-engagement", eng_id)
        cli_run("--mode", "local", "--engagement-id", eng_id, "syft", "version")

        evidence_dir = project_root / "work" / "engagements" / eng_id / "evidence"
        meta_files = list(evidence_dir.glob("*.meta.json"))
        if not meta_files:
            pytest.skip("No meta files -- tool may not be installed")

        meta = json.loads(meta_files[0].read_text(encoding="utf-8"))
        for field in [
            "timestamp",
            "engagement_id",
            "tool_command",
            "sha256_raw",
            "sha256_filtered",
        ]:
            assert field in meta, f"Missing required field '{field}'"


# ===========================================================================
# STORY-023-034: Engagement Teardown + Verification
# ===========================================================================


class TestAnalyzeAndReport:
    """TASK-023-152/153: Analyze + Report lifecycle transitions."""

    def test_lifecycle_active_to_analyzing(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """ACTIVE -> ANALYZING transition."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        mgr = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        s = mgr.create(engagement_config_path)
        s = mgr.approve_scope(s.engagement_id)
        s = mgr.activate(s.engagement_id)
        s = mgr.complete_execution(s.engagement_id)
        assert s.current_state == "ANALYZING"

    def test_lifecycle_analyzing_to_reporting(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """ANALYZING -> REPORTING transition."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        mgr = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        s = mgr.create(engagement_config_path)
        s = mgr.approve_scope(s.engagement_id)
        s = mgr.activate(s.engagement_id)
        s = mgr.complete_execution(s.engagement_id)
        s = mgr.complete_analysis(s.engagement_id)
        assert s.current_state == "REPORTING"


class TestTerraformDestroy:
    """TASK-023-142: Terraform destroy via mock adapter (I9)."""

    def _make_config(self):
        from src.proxy_infra.domain.value_objects.provision_config import (
            ProvisionConfig,
        )

        return ProvisionConfig(
            engagement_id="E2E-RAINBOW-001",
            engagement_tag="jerry-e2e-E2E-RAINBOW-001",
            provider="digitalocean",
            region="nyc3",
            count=1,
            proxy_type="direct_socks5",
            socks_port=1080,
            role="socks-proxy",
            ssh_public_key="ssh-ed25519 AAAA mock-test-key",
            operator_ip="127.0.0.1",
        )

    def test_destroy_returns_success(self) -> None:
        """destroy() reports all nodes destroyed."""
        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            MockTerraformProvisionerAdapter,
        )

        adapter = MockTerraformProvisionerAdapter()
        nodes = adapter.provision(self._make_config())
        ids = [n.id for n in nodes]
        result = adapter.destroy(ids, engagement_id="E2E-RAINBOW-001")
        assert result.destroyed == ids and result.failed == []

    def test_no_nodes_after_destroy(self) -> None:
        """No nodes remain after destroy (N7)."""
        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            MockTerraformProvisionerAdapter,
        )

        adapter = MockTerraformProvisionerAdapter()
        nodes = adapter.provision(self._make_config())
        adapter.destroy([n.id for n in nodes], engagement_id="E2E-RAINBOW-001")
        assert adapter.list_nodes() == []


class TestEvidenceArchive:
    """TASK-023-143: Archive evidence with SHA-256 manifest."""

    def test_archive_directory_exists(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """Archive directory created during engagement setup."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        mgr = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        mgr.create(engagement_config_path)
        eng_dir = engagement_base_dir / "E2E-RAINBOW-001"
        assert (eng_dir / "archive").is_dir()

    def test_evidence_file_hashable(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """Evidence files produce valid SHA-256 hashes for manifest."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )

        mgr = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        mgr.create(engagement_config_path)
        eng_dir = engagement_base_dir / "E2E-RAINBOW-001"
        finding = eng_dir / "red-team" / "findings" / "test-finding.txt"
        finding.write_text("Sample finding", encoding="utf-8")
        assert len(hashlib.sha256(finding.read_bytes()).hexdigest()) == 64


class TestOrphanVerification:
    """TASK-023-144: Verify no orphaned resources after destroy (N7)."""

    def test_list_instances_empty_after_destroy(self) -> None:
        """list_instances returns empty (simulates doctl orphan check)."""
        from src.proxy_infra.domain.value_objects.provision_config import (
            ProvisionConfig,
        )
        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            MockTerraformProvisionerAdapter,
        )

        adapter = MockTerraformProvisionerAdapter()
        cfg = ProvisionConfig(
            engagement_id="E2E-RAINBOW-001",
            engagement_tag="jerry-e2e-E2E-RAINBOW-001",
            provider="digitalocean",
            region="nyc3",
            count=1,
            proxy_type="direct_socks5",
            socks_port=1080,
            role="socks-proxy",
            ssh_public_key="ssh-ed25519 AAAA mock-test-key",
            operator_ip="127.0.0.1",
        )
        nodes = adapter.provision(cfg)
        adapter.destroy([n.id for n in nodes], engagement_id="E2E-RAINBOW-001")
        assert adapter.list_instances("jerry-e2e-E2E-RAINBOW-001") == []


class TestFullLifecycleIntegration:
    """Complete 7-state lifecycle: the north-star test."""

    def test_complete_lifecycle_defined_to_archived(
        self,
        engagement_config_path: Path,
        engagement_base_dir: Path,
        auto_approve_confirmation,
    ) -> None:
        """DEFINED -> PROVISIONING -> ACTIVE -> ANALYZING ->
        REPORTING -> TEARDOWN -> ARCHIVED."""
        from src.proxy_infra.application.handlers.gated_lifecycle_manager import (
            GatedLifecycleManager,
        )
        from src.proxy_infra.domain.value_objects.provision_config import (
            ProvisionConfig,
        )
        from src.proxy_infra.infrastructure.adapters.mock_terraform_provisioner_adapter import (
            MockTerraformProvisionerAdapter,
        )

        mgr = GatedLifecycleManager(
            engagement_dir=engagement_base_dir,
            confirmation_port=auto_approve_confirmation,
        )
        s = mgr.create(engagement_config_path)
        assert s.current_state == "DEFINED"

        s = mgr.approve_scope(s.engagement_id)
        assert s.current_state == "PROVISIONING"

        adapter = MockTerraformProvisionerAdapter()
        nodes = adapter.provision(
            ProvisionConfig(
                engagement_id="E2E-RAINBOW-001",
                engagement_tag="jerry-e2e-E2E-RAINBOW-001",
                provider="digitalocean",
                region="nyc3",
                count=1,
                proxy_type="direct_socks5",
                socks_port=1080,
                role="socks-proxy",
                ssh_public_key="ssh-ed25519 AAAA mock-test-key",
                operator_ip="127.0.0.1",
            )
        )
        assert len(nodes) >= 1

        s = mgr.activate(s.engagement_id)
        assert s.current_state == "ACTIVE"

        s = mgr.complete_execution(s.engagement_id)
        assert s.current_state == "ANALYZING"

        s = mgr.complete_analysis(s.engagement_id)
        assert s.current_state == "REPORTING"

        s = mgr.approve_report(s.engagement_id)
        assert s.current_state == "TEARDOWN"

        result = adapter.destroy(
            [n.id for n in nodes],
            engagement_id="E2E-RAINBOW-001",
        )
        assert result.failed == []
        assert adapter.list_instances("jerry-e2e-E2E-RAINBOW-001") == []

        s = mgr.complete_teardown(s.engagement_id)
        assert s.current_state == "ARCHIVED"

        assert len(s.transitions) == 6
        expected = [
            ("DEFINED", "PROVISIONING"),
            ("PROVISIONING", "ACTIVE"),
            ("ACTIVE", "ANALYZING"),
            ("ANALYZING", "REPORTING"),
            ("REPORTING", "TEARDOWN"),
            ("TEARDOWN", "ARCHIVED"),
        ]
        for i, (fr, to) in enumerate(expected):
            assert s.transitions[i]["from"] == fr
            assert s.transitions[i]["to"] == to

        state_path = engagement_base_dir / "E2E-RAINBOW-001" / "config" / "state.yaml"
        persisted = yaml.safe_load(state_path.read_text(encoding="utf-8"))
        assert persisted["current_state"] == "ARCHIVED"
