# BDD RED PHASE — All tests expected to FAIL (ImportError). Implementation in TASK-023-027+.
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BDD test suite for AuditLogStore.

TASK-023-046: Implement CLM Audit Logging for Provisioner API Calls

Covers:
  - Every provision/destroy/list/health_check call generates an audit entry
  - APICALL-004: response bodies with tokens/keys NEVER logged
  - JSONL format: one JSON object per line with required fields
  - Required fields: timestamp (ISO 8601), engagement_id, action, provider,
    resource_id, response_code
  - Log location: ./logs/audit/{engagement_id}/provisioner.jsonl
  - Logs survive engagement teardown (not in ./secrets/ which is purged)
  - Rotation: max 10MB per file, 90-day retention per FM-025
  - Audit log is append-only (previous entries are never modified)

Test pyramid: 60% happy path / 30% negative / 10% architecture
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest

from src.proxy_infra.infrastructure.persistence.audit_log_store import AuditLogStore


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def temp_log_dir(tmp_path: Path) -> Path:
    """Return a temporary directory for audit log output."""
    return tmp_path


@pytest.fixture()
def audit_store(temp_log_dir: Path) -> AuditLogStore:
    """Return an AuditLogStore writing to a temporary directory."""
    return AuditLogStore(base_log_dir=temp_log_dir)


# =============================================================================
# Happy path: Audit entry written for every adapter operation
# =============================================================================


@pytest.mark.unit
class TestAuditLogStoreWritesEntries:
    """
    Scenario: Provisioner API calls are audit logged
      Given CLM is provisioning a new proxy node
      When the DigitalOcean adapter calls droplets.create()
      Then an audit log entry is written with required fields
      And the entry is valid JSON
      And the entry does NOT contain API tokens, SSH keys, or SOCKS5 credentials
    """

    def test_write_entry_creates_log_file(
        self, audit_store: AuditLogStore, temp_log_dir: Path
    ) -> None:
        """AuditLogStore must create the JSONL file on first write."""
        audit_store.write_entry(
            engagement_id="ENG-001",
            action="provision",
            provider="digitalocean",
            resource_id="do-12345",
            response_code=200,
        )
        log_path = temp_log_dir / "ENG-001" / "provisioner.jsonl"
        assert log_path.exists(), (
            "AuditLogStore must create ./logs/audit/{engagement_id}/provisioner.jsonl — "
            "TASK-023-046 AC: log location is engagement-scoped"
        )

    def test_write_entry_produces_valid_json_per_line(
        self, audit_store: AuditLogStore, temp_log_dir: Path
    ) -> None:
        """Each audit entry must be a valid JSON object on its own line (JSONL)."""
        audit_store.write_entry(
            engagement_id="ENG-001",
            action="provision",
            provider="digitalocean",
            resource_id="do-12345",
            response_code=200,
        )
        log_path = temp_log_dir / "ENG-001" / "provisioner.jsonl"
        lines = log_path.read_text().strip().splitlines()
        assert len(lines) == 1, "One write_entry call must produce one JSONL line"
        try:
            entry = json.loads(lines[0])
        except json.JSONDecodeError as exc:
            pytest.fail(
                f"Audit log line is not valid JSON: {exc} — "
                f"FM-025: JSONL format required for structured log processing"
            )
        assert isinstance(entry, dict), "Each JSONL line must parse to a dict"

    def test_write_entry_includes_all_required_fields(
        self, audit_store: AuditLogStore, temp_log_dir: Path
    ) -> None:
        """Audit entry must include: timestamp, engagement_id, action, provider,
        resource_id, response_code (TASK-023-046 AC)."""
        audit_store.write_entry(
            engagement_id="ENG-001",
            action="provision",
            provider="digitalocean",
            resource_id="do-12345",
            response_code=201,
        )
        log_path = temp_log_dir / "ENG-001" / "provisioner.jsonl"
        entry = json.loads(log_path.read_text().strip())
        required_fields = {
            "timestamp",
            "engagement_id",
            "action",
            "provider",
            "resource_id",
            "response_code",
        }
        missing = required_fields - set(entry.keys())
        assert not missing, (
            f"Audit entry missing fields: {missing} — "
            f"TASK-023-046 AC: all six fields are required"
        )

    def test_write_entry_timestamp_is_iso_8601(
        self, audit_store: AuditLogStore, temp_log_dir: Path
    ) -> None:
        """Audit entry timestamp must be ISO 8601 format."""
        audit_store.write_entry(
            engagement_id="ENG-001",
            action="destroy",
            provider="digitalocean",
            resource_id="do-12345",
            response_code=204,
        )
        log_path = temp_log_dir / "ENG-001" / "provisioner.jsonl"
        entry = json.loads(log_path.read_text().strip())
        ts = entry["timestamp"]
        try:
            datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            pytest.fail(
                f"Audit entry timestamp '{ts}' is not ISO 8601 — "
                f"TASK-023-046 AC: timestamp must be ISO 8601"
            )

    def test_multiple_entries_are_appended_not_overwritten(
        self, audit_store: AuditLogStore, temp_log_dir: Path
    ) -> None:
        """AuditLogStore must append entries — previous entries must not be lost."""
        audit_store.write_entry(
            engagement_id="ENG-001",
            action="provision",
            provider="digitalocean",
            resource_id="do-11111",
            response_code=201,
        )
        audit_store.write_entry(
            engagement_id="ENG-001",
            action="provision",
            provider="digitalocean",
            resource_id="do-22222",
            response_code=201,
        )
        log_path = temp_log_dir / "ENG-001" / "provisioner.jsonl"
        lines = log_path.read_text().strip().splitlines()
        assert len(lines) == 2, (
            "AuditLogStore must append entries — "
            "both provision events must appear in the log"
        )

    def test_all_four_adapter_actions_produce_entries(
        self, audit_store: AuditLogStore, temp_log_dir: Path
    ) -> None:
        """All four adapter methods must produce audit entries (TASK-023-046 AC)."""
        actions = ["provision", "destroy", "list_instances", "health_check"]
        for action in actions:
            audit_store.write_entry(
                engagement_id="ENG-001",
                action=action,
                provider="digitalocean",
                resource_id="do-99999",
                response_code=200,
            )
        log_path = temp_log_dir / "ENG-001" / "provisioner.jsonl"
        logged_actions = [
            json.loads(line)["action"]
            for line in log_path.read_text().strip().splitlines()
        ]
        for action in actions:
            assert action in logged_actions, (
                f"Action '{action}' must appear in audit log — "
                f"TASK-023-046 AC: all four adapter methods must be logged"
            )

    def test_log_path_is_engagement_scoped(
        self, audit_store: AuditLogStore, temp_log_dir: Path
    ) -> None:
        """Audit logs for different engagements must be in separate directories."""
        audit_store.write_entry(
            engagement_id="ENG-001",
            action="provision",
            provider="digitalocean",
            resource_id="do-001",
            response_code=201,
        )
        audit_store.write_entry(
            engagement_id="ENG-002",
            action="provision",
            provider="digitalocean",
            resource_id="do-002",
            response_code=201,
        )
        eng1_log = temp_log_dir / "ENG-001" / "provisioner.jsonl"
        eng2_log = temp_log_dir / "ENG-002" / "provisioner.jsonl"
        assert eng1_log.exists(), "ENG-001 log must exist in its own directory"
        assert eng2_log.exists(), "ENG-002 log must exist in its own directory"

        # ENG-001 log must contain only ENG-001 entries
        eng1_entries = [
            json.loads(l) for l in eng1_log.read_text().strip().splitlines()
        ]
        for entry in eng1_entries:
            assert entry["engagement_id"] == "ENG-001", (
                "ENG-001 log file must only contain ENG-001 entries — "
                "multi-engagement isolation"
            )


# =============================================================================
# Critical security: APICALL-004 — credentials never in log output
# =============================================================================


@pytest.mark.unit
class TestAuditLogAPICAll004CredentialRedaction:
    """
    Scenario: Audit log never contains API tokens, SSH keys, or credentials
      Given an adapter call completes with a response body containing tokens
      When write_entry() is called with response metadata
      Then the written entry contains only the response_code and resource_id
      And no credential-like strings appear in the JSONL output

    APICALL-004: NEVER log API response bodies containing tokens, SSH keys,
    or credentials — log response code and resource ID only.
    """

    def test_write_entry_does_not_accept_response_body(
        self, audit_store: AuditLogStore
    ) -> None:
        """APICALL-004: write_entry() must not have a response_body parameter.

        The presence of a response_body parameter invites callers to pass
        credential-bearing response bodies.  The interface must structurally
        prohibit this.
        """
        import inspect
        sig = inspect.signature(audit_store.write_entry)
        param_names = set(sig.parameters.keys())
        assert "response_body" not in param_names, (
            "write_entry() must NOT have a response_body parameter — "
            "APICALL-004: response bodies with tokens are never logged"
        )
        assert "raw_response" not in param_names, (
            "write_entry() must NOT have a raw_response parameter — "
            "APICALL-004: only response_code and resource_id are logged"
        )

    def test_written_entry_contains_no_api_token_patterns(
        self, audit_store: AuditLogStore, temp_log_dir: Path
    ) -> None:
        """APICALL-004: Written JSONL must not contain DigitalOcean API token patterns."""
        # Simulate a write that might accidentally include a token prefix
        # by passing it as part of resource_id (should not appear verbatim if sanitised)
        audit_store.write_entry(
            engagement_id="ENG-001",
            action="provision",
            provider="digitalocean",
            resource_id="do-12345",  # sanitised resource ID only
            response_code=200,
        )
        log_path = temp_log_dir / "ENG-001" / "provisioner.jsonl"
        log_content = log_path.read_text()
        # DigitalOcean API token prefix is "dop_v1_" followed by hex
        assert "dop_v1_" not in log_content, (
            "Audit log must not contain DigitalOcean API token prefix 'dop_v1_' — "
            "APICALL-004"
        )

    def test_written_entry_contains_no_socks5_credential_patterns(
        self, audit_store: AuditLogStore, temp_log_dir: Path
    ) -> None:
        """APICALL-004: Written JSONL must not contain SOCKS5 credential fields."""
        audit_store.write_entry(
            engagement_id="ENG-001",
            action="health_check",
            provider="digitalocean",
            resource_id="do-12345",
            response_code=200,
        )
        log_path = temp_log_dir / "ENG-001" / "provisioner.jsonl"
        log_content = log_path.read_text()
        forbidden_keys = ["PROXY_PASS", "PROXY_USER", "proxy_password", "socks5_pass"]
        for key in forbidden_keys:
            assert key not in log_content, (
                f"Audit log must not contain SOCKS5 credential field '{key}' — "
                f"APICALL-004"
            )


# =============================================================================
# Happy path: Audit logs survive engagement teardown
# =============================================================================


@pytest.mark.unit
class TestAuditLogSurvivesTeardown:
    """
    Scenario: Audit logs survive engagement teardown
      Given an engagement with 5 provisioner API calls logged
      When the operator runs "jerry proxy destroy --engagement ENG-001"
      Then the audit log file persists after teardown
      And contains all 5 entries plus the destroy operations

    Logs must be stored in ./logs/audit/{engagement_id}/, NOT in ./secrets/
    which is purged during teardown.
    """

    def test_audit_store_base_dir_is_not_secrets_directory(
        self, audit_store: AuditLogStore
    ) -> None:
        """AuditLogStore base directory must not be ./secrets/ (which is purged)."""
        base_dir = str(audit_store.base_log_dir)
        assert "secrets" not in base_dir.lower(), (
            "AuditLogStore base_log_dir must not be in ./secrets/ — "
            "TASK-023-046 AC: audit logs survive teardown; ./secrets/ is purged"
        )

    def test_audit_store_base_dir_is_under_logs_audit(
        self, temp_log_dir: Path
    ) -> None:
        """AuditLogStore must write logs under ./logs/audit/ per TASK-023-046 AC."""
        store = AuditLogStore(base_log_dir=temp_log_dir)
        store.write_entry(
            engagement_id="ENG-001",
            action="provision",
            provider="digitalocean",
            resource_id="do-001",
            response_code=201,
        )
        # The entry must have been written under the base_log_dir
        # (in production this is ./logs/audit/)
        log_path = temp_log_dir / "ENG-001" / "provisioner.jsonl"
        assert log_path.exists(), (
            "Audit log must be written under {base_log_dir}/ENG-001/provisioner.jsonl — "
            "TASK-023-046 AC: engagement-scoped log location"
        )

    def test_five_entries_all_present_after_destroy_entry(
        self, audit_store: AuditLogStore, temp_log_dir: Path
    ) -> None:
        """All preceding entries must remain intact after a destroy entry is appended."""
        for i in range(5):
            audit_store.write_entry(
                engagement_id="ENG-001",
                action="provision",
                provider="digitalocean",
                resource_id=f"do-{i:05d}",
                response_code=201,
            )
        # Simulate teardown destroy entry
        audit_store.write_entry(
            engagement_id="ENG-001",
            action="destroy",
            provider="digitalocean",
            resource_id="all",
            response_code=204,
        )
        log_path = temp_log_dir / "ENG-001" / "provisioner.jsonl"
        lines = log_path.read_text().strip().splitlines()
        assert len(lines) == 6, (
            f"Expected 6 entries (5 provisions + 1 destroy), got {len(lines)} — "
            f"TASK-023-046 AC: all entries persist after teardown"
        )


# =============================================================================
# Architecture: Rotation configuration
# =============================================================================


@pytest.mark.unit
class TestAuditLogRotationConfig:
    """AuditLogStore must expose rotation configuration constants per FM-025."""

    def test_max_file_size_is_10mb(self) -> None:
        """AuditLogStore.MAX_FILE_SIZE_BYTES must be 10MB (FM-025)."""
        expected = 10 * 1024 * 1024  # 10MB in bytes
        assert AuditLogStore.MAX_FILE_SIZE_BYTES == expected, (
            f"AuditLogStore.MAX_FILE_SIZE_BYTES must be {expected} — "
            f"FM-025: max 10MB per file"
        )

    def test_retention_days_is_90(self) -> None:
        """AuditLogStore.RETENTION_DAYS must be 90 (FM-025)."""
        assert AuditLogStore.RETENTION_DAYS == 90, (
            "AuditLogStore.RETENTION_DAYS must be 90 — "
            "FM-025: 90-day retention"
        )
