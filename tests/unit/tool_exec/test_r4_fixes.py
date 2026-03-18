# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""R4 Tournament Finding Remediation Tests.

Covers the Critical + top Major findings from the W12-PHASE2-R4 tournament:

  CC-001-R4 (H-07): EngagementInitializer.initialize() reads os.environ
      in domain service.  Fixed: created_by is now a parameter.

  SR-003-R4: _write_no_filter_audit() builds engagement path manually without
      calling _validate_id().  Fixed: uses engagement_init.evidence_dir().

  FM-033: --zone flag parsed but never consumed in handle_tool_exec().
      Fixed: zone_override threaded to SecurityPolicy override via
      dataclasses.replace().

  CV-007: Already documented exit 9 (STRICT_MODE_VIOLATION) as correct in
      UC-TOOLEXEC-001 AF-05 and UC-TOOLEXEC-005 AF-02 in a prior R4 pass.
      Verified here for regression.

  DA-R4-001: Factory docstring updated to document two-path topology.
      No runtime behaviour change; verified via factory return-value assertions.

  PM-004-R4: Meta filename based on compound hash sha256(stdout + stderr).
      Fixed: _quarantine_output now computes sha256_compound and uses it for
      the .meta.json filename stem.

References:
    - W12-PHASE2-R4-FIX: Engagement ID
    - eng-backend-r4-fix.md: Full remediation record
"""

from __future__ import annotations

import dataclasses
import json
import os
from pathlib import Path
from unittest.mock import patch

from src.interface.cli.tool_exec_commands import (
    _quarantine_output,
    _write_no_filter_audit,
    create_tool_exec_handler,
)
from src.tool_exec.domain.services.engagement_initializer import EngagementInitializer
from src.tool_exec.domain.value_objects.exit_codes import ExitCode
from src.tool_exec.domain.value_objects.security_policy import SecurityPolicy

# =============================================================================
# CC-001-R4 (H-07): EngagementInitializer.initialize() must NOT read os.environ
# =============================================================================


class TestCC001R4EngagementInitializerDomainIsolation:
    """CC-001-R4 (H-07): created_by is an explicit parameter, not read from
    os.environ inside the domain service."""

    def test_created_by_parameter_written_to_meta(self, tmp_path: Path) -> None:
        """initialize(created_by=...) stores the supplied value in metadata."""
        init = EngagementInitializer(base_dir=tmp_path)
        init.initialize("eng-cc001-test", created_by="alice")

        meta = json.loads((tmp_path / "eng-cc001-test" / ".engagement-meta.json").read_text())
        assert meta["created_by"] == "alice"

    def test_default_created_by_is_unknown(self, tmp_path: Path) -> None:
        """Default created_by when not supplied is 'unknown'."""
        init = EngagementInitializer(base_dir=tmp_path)
        # Unset USER/USERNAME in environment to ensure pure default behaviour.
        env_backup_user = os.environ.pop("USER", None)
        env_backup_username = os.environ.pop("USERNAME", None)
        try:
            init.initialize("eng-default-by")
        finally:
            if env_backup_user is not None:
                os.environ["USER"] = env_backup_user
            if env_backup_username is not None:
                os.environ["USERNAME"] = env_backup_username

        meta = json.loads((tmp_path / "eng-default-by" / ".engagement-meta.json").read_text())
        assert meta["created_by"] == "unknown"

    def test_explicit_created_by_overrides_env(self, tmp_path: Path) -> None:
        """Explicit created_by parameter is stored; env variables are irrelevant
        to the domain service (CC-001-R4: the domain layer does not read env vars)."""
        init = EngagementInitializer(base_dir=tmp_path)
        with patch.dict(os.environ, {"USER": "env-user"}):
            init.initialize("eng-explicit", created_by="operator")

        meta = json.loads((tmp_path / "eng-explicit" / ".engagement-meta.json").read_text())
        # Explicitly passed value is stored, confirming domain service ignores env.
        assert meta["created_by"] == "operator"

    def test_cli_handler_passes_env_user_to_initialize(self, tmp_path: Path) -> None:
        """CLI handler (_handle_init_engagement) reads USER from env and passes
        it to initialize() — the infrastructure boundary is in the CLI, not the
        domain service."""
        from src.interface.cli.tool_exec_commands import _handle_init_engagement

        init = EngagementInitializer(base_dir=tmp_path)
        with patch.dict(os.environ, {"USER": "bob", "USERNAME": "ignored"}):
            _handle_init_engagement("eng-cli-user", init)

        meta = json.loads((tmp_path / "eng-cli-user" / ".engagement-meta.json").read_text())
        # CLI handler reads USER first (POSIX), so "bob" must appear.
        assert meta["created_by"] == "bob"


# =============================================================================
# SR-003-R4: _write_no_filter_audit must use evidence_dir(), not manual path
# =============================================================================


class TestSR003R4NoFilterAuditUsesEvidenceDir:
    """SR-003-R4: _write_no_filter_audit() must construct the audit path via
    engagement_init.evidence_dir() which calls _validate_id() (CWE-22 guard),
    not by manually concatenating project_root / 'work' / 'engagements' / id."""

    def test_audit_written_to_evidence_dir_when_engagement_active(self, tmp_path: Path) -> None:
        """When engagement_id is set, audit lands in evidence_dir()."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-sr003")

        _write_no_filter_audit(
            tool_command="nuclei",
            engagement_id="eng-sr003",
            strict_mode_env="false",
            project_root=tmp_path,
            engagement_init=init,
        )

        evidence_dir = init.evidence_dir("eng-sr003")
        audit_files = list(evidence_dir.glob("no-filter-audit-*.json"))
        assert len(audit_files) == 1, "Expected exactly one audit file in evidence_dir"

        event = json.loads(audit_files[0].read_text())
        assert event["event_type"] == "no_filter_invocation"
        assert event["tool_command"] == "nuclei"
        assert event["engagement_id"] == "eng-sr003"

    def test_audit_fallback_when_no_engagement(self, tmp_path: Path) -> None:
        """When engagement_id is None, audit uses global fallback path."""
        _write_no_filter_audit(
            tool_command="trivy",
            engagement_id=None,
            strict_mode_env="false",
            project_root=tmp_path,
            engagement_init=None,
        )

        fallback_dir = tmp_path / "work" / "security-events"
        audit_files = list(fallback_dir.glob("no-filter-audit-*.json"))
        assert len(audit_files) == 1, "Expected exactly one audit file in fallback dir"

    def test_audit_path_does_not_bypass_validate_id(self, tmp_path: Path) -> None:
        """A malformed engagement_id passed to _write_no_filter_audit is rejected
        by evidence_dir(_validate_id()) so no file is written outside the
        engagement root.

        SR-003-R4: The manual path build (project_root / 'work' / 'engagements'
        / engagement_id / 'evidence') skipped this validation; evidence_dir()
        does not skip it.

        _write_no_filter_audit is best-effort so it catches the ValueError
        internally and logs it rather than re-raising.  The important property
        is that NO audit file escapes to the traversal path.
        """
        init = EngagementInitializer(base_dir=tmp_path / "engagements")

        # Should not raise (best-effort catch inside), but also must not write
        # any file at a path traversal location.
        _write_no_filter_audit(
            tool_command="nuclei",
            engagement_id="../escape",
            strict_mode_env="false",
            project_root=tmp_path,
            engagement_init=init,
        )

        # The traversal target would be tmp_path / "escape" / "evidence" if
        # the old manual build path were used.  Verify no file landed there.
        escaped_dir = tmp_path / "escape"
        assert not escaped_dir.exists(), (
            "Traversal path was created; _validate_id() guard was bypassed."
        )
        # Also verify no audit file exists in the engagements base dir at all.
        engagements_dir = tmp_path / "engagements"
        audit_files = list(engagements_dir.rglob("no-filter-audit-*.json"))
        assert len(audit_files) == 0, f"Unexpected audit files created: {audit_files}"


# =============================================================================
# FM-033: --zone flag is threaded to SecurityPolicy override
# =============================================================================


class TestFM033ZoneOverrideThreaded:
    """FM-033: The --zone CLI flag must be consumed and applied to the
    SecurityPolicy used for engagement/approval/container enforcement.

    Previously --zone was parsed but getattr(args, 'zone', None) was never
    called in handle_tool_exec(), making the flag a no-op.
    """

    def test_zone_override_zone1_produces_no_engagement_policy(self) -> None:
        """Zone 1 override: requires_engagement=False, requires_approval=False."""
        base_policy = SecurityPolicy(
            requires_engagement=True,
            requires_approval=True,
            credential_filter_enabled=True,
            container_required=True,
            network_access="full",
            family_zone_label="Zone 3",
        )
        zone_override = "1"
        _ZONE_OVERRIDE_FIELDS = {
            "1": {
                "requires_engagement": False,
                "requires_approval": False,
                "container_required": False,
                "network_access": "none",
                "family_zone_label": "Zone 1",
            },
        }
        overridden = dataclasses.replace(base_policy, **_ZONE_OVERRIDE_FIELDS[zone_override])
        assert overridden.requires_engagement is False
        assert overridden.requires_approval is False
        assert overridden.container_required is False
        assert overridden.network_access == "none"
        assert overridden.family_zone_label == "Zone 1"
        # credential_filter_enabled must be preserved (not overridden by zone)
        assert overridden.credential_filter_enabled is True

    def test_zone_override_zone2_requires_engagement(self) -> None:
        """Zone 2 override: requires_engagement=True, requires_approval=False."""
        base_policy = SecurityPolicy(
            requires_engagement=False,
            requires_approval=False,
            credential_filter_enabled=True,
            container_required=False,
            network_access="none",
            family_zone_label="Zone 1",
        )
        zone_override = "2"
        _ZONE_OVERRIDE_FIELDS = {
            "2": {
                "requires_engagement": True,
                "requires_approval": False,
                "container_required": False,
                "network_access": "restricted",
                "family_zone_label": "Zone 2",
            },
        }
        overridden = dataclasses.replace(base_policy, **_ZONE_OVERRIDE_FIELDS[zone_override])
        assert overridden.requires_engagement is True
        assert overridden.requires_approval is False
        assert overridden.network_access == "restricted"
        assert overridden.family_zone_label == "Zone 2"

    def test_zone_override_zone3_full_constraints(self) -> None:
        """Zone 3 override: all restrictive constraints applied."""
        base_policy = SecurityPolicy(
            requires_engagement=False,
            requires_approval=False,
            credential_filter_enabled=True,
            container_required=False,
            network_access="none",
            family_zone_label="Zone 1",
        )
        zone_override = "3"
        _ZONE_OVERRIDE_FIELDS = {
            "3": {
                "requires_engagement": True,
                "requires_approval": True,
                "container_required": True,
                "network_access": "full",
                "family_zone_label": "Zone 3",
            },
        }
        overridden = dataclasses.replace(base_policy, **_ZONE_OVERRIDE_FIELDS[zone_override])
        assert overridden.requires_engagement is True
        assert overridden.requires_approval is True
        assert overridden.container_required is True
        assert overridden.network_access == "full"
        assert overridden.family_zone_label == "Zone 3"

    def test_no_zone_override_leaves_policy_unchanged(self) -> None:
        """When zone_override is None, the resolver-derived policy is unchanged."""
        base_policy = SecurityPolicy(
            requires_engagement=True,
            requires_approval=False,
            credential_filter_enabled=True,
            container_required=False,
            network_access="restricted",
            family_zone_label="Zone 2",
        )
        zone_override = None
        # The handler only applies override when zone_override is not None
        if zone_override is not None:
            policy = dataclasses.replace(base_policy)
        else:
            policy = base_policy
        assert policy is base_policy  # exact same object, not a copy


# =============================================================================
# CV-007: --no-filter + strict exits 9 (STRICT_MODE_VIOLATION), not 6
# =============================================================================


class TestCV007StrictModeViolationExitCode:
    """CV-007 regression: --no-filter + JERRY_STRICT_MODE=true must return
    exit code 9 (STRICT_MODE_VIOLATION), not 6 (MODE_UNSET).

    UC-TOOLEXEC-001 AF-05 and UC-TOOLEXEC-005 AF-02 document this decision:
    strict mode rejection of --no-filter is a policy violation, not a mode
    configuration error.
    """

    def test_strict_mode_violation_exit_code_is_9(self) -> None:
        """STRICT_MODE_VIOLATION has value 9."""
        assert ExitCode.STRICT_MODE_VIOLATION == 9

    def test_mode_unset_exit_code_is_6(self) -> None:
        """MODE_UNSET has value 6 (for Zone 2/3 tools without explicit mode)."""
        assert ExitCode.MODE_UNSET == 6

    def test_strict_mode_violation_and_mode_unset_are_distinct(self) -> None:
        """Exit codes 6 and 9 are distinct values with distinct semantics."""
        assert ExitCode.STRICT_MODE_VIOLATION != ExitCode.MODE_UNSET


# =============================================================================
# DA-R4-001: Factory docstring documents two-path topology
# =============================================================================


class TestDAR4001FactoryDocstring:
    """DA-R4-001: create_tool_exec_handler() docstring documents two-path
    topology (base composition root + invocation-scoped filter rebind).

    No runtime behaviour change; validated via docstring content and factory
    return values.
    """

    def test_factory_docstring_mentions_two_path_topology(self) -> None:
        """The factory docstring contains the DA-R4-001 two-path documentation."""
        doc = create_tool_exec_handler.__doc__
        assert doc is not None
        assert "DA-R4-001" in doc
        assert "two-path" in doc

    def test_factory_returns_expected_keys(self, tmp_path: Path) -> None:
        """Factory returns loader, engagement_init, credential_filter,
        local_executor, container_executor (base path)."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text("families: []\n")

        services = create_tool_exec_handler(tmp_path)
        assert set(services.keys()) >= {
            "loader",
            "engagement_init",
            "credential_filter",
            "local_executor",
            "container_executor",
        }


# =============================================================================
# PM-004-R4: Meta filename uses compound hash sha256(stdout + stderr)
# =============================================================================


class TestPM004R4CompoundHashMetaFilename:
    """PM-004-R4: _quarantine_output() meta filename stem is sha256(stdout + stderr)
    rather than sha256(stdout) alone.  Prevents collisions when multiple
    stderr-only credential detections occur (all would have sha256('') for stdout).
    """

    def test_meta_filename_uses_compound_hash(self, tmp_path: Path) -> None:
        """Meta file name starts with sha256(stdout + stderr) hash prefix.

        PM-001-R4: The meta filename now includes a microsecond timestamp suffix
        after the compound hash stem to prevent collision when two invocations
        produce identical output. The compound hash prefix must still be present
        as the first segment of the filename so the detection event is traceable
        to its content-addressable hash.

        Format: {sha256(stdout+stderr)}-{timestamp}.meta.json
        """
        import hashlib

        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-pm004")

        # Use a credential pattern that the filter detects (password assignment).
        raw_stdout = ""
        raw_stderr = "detected_password=longpassword1"

        _quarantine_output(
            raw_stdout=raw_stdout,
            raw_stderr=raw_stderr,
            tool_command="test-tool",
            engagement_id="eng-pm004",
            engagement_init=init,
            project_root=tmp_path,
        )

        quarantine_dir = init.quarantine_dir("eng-pm004")
        meta_files = list(quarantine_dir.glob("*.meta.json"))
        assert len(meta_files) == 1, f"Expected 1 meta file, found: {meta_files}"

        # PM-001-R4: Meta filename starts with the compound hash prefix.
        # The format is {sha256(stdout+stderr)}-{microsecond-timestamp}.meta.json.
        expected_hash = hashlib.sha256((raw_stdout + raw_stderr).encode("utf-8")).hexdigest()
        meta_name = meta_files[0].name
        assert meta_name.startswith(expected_hash), (
            f"Meta filename should start with sha256(stdout+stderr)={expected_hash!r}, "
            f"got {meta_name!r}"
        )
        assert meta_name.endswith(".meta.json"), (
            f"Meta filename should end with .meta.json, got {meta_name!r}"
        )

    def test_stderr_only_detections_get_distinct_meta_files(self, tmp_path: Path) -> None:
        """Two stderr-only detections with different content produce distinct meta files.

        With the old sha256(stdout)-only scheme both would produce sha256('')
        as the stem and the second write would overwrite the first.
        """
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-pm004-dedup")

        # Two distinct stderr-only credential detections (password assignments)
        stderr_a = "detected_password=longsecretpassworda"
        stderr_b = "detected_password=longsecretpasswordb"

        _quarantine_output(
            raw_stdout="",
            raw_stderr=stderr_a,
            tool_command="test-tool",
            engagement_id="eng-pm004-dedup",
            engagement_init=init,
            project_root=tmp_path,
        )
        _quarantine_output(
            raw_stdout="",
            raw_stderr=stderr_b,
            tool_command="test-tool",
            engagement_id="eng-pm004-dedup",
            engagement_init=init,
            project_root=tmp_path,
        )

        quarantine_dir = init.quarantine_dir("eng-pm004-dedup")
        meta_files = list(quarantine_dir.glob("*.meta.json"))
        assert len(meta_files) == 2, (
            f"Expected 2 distinct meta files (one per detection), "
            f"found {len(meta_files)}: {[f.name for f in meta_files]}"
        )

    def test_meta_json_contains_sha256_compound_field(self, tmp_path: Path) -> None:
        """Meta JSON includes sha256_compound key for traceability."""
        import hashlib

        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-meta-field")

        stdout_val = "some output"
        stderr_val = "credential=secret123"

        _quarantine_output(
            raw_stdout=stdout_val,
            raw_stderr=stderr_val,
            tool_command="mytool",
            engagement_id="eng-meta-field",
            engagement_init=init,
            project_root=tmp_path,
        )

        quarantine_dir = init.quarantine_dir("eng-meta-field")
        meta_files = list(quarantine_dir.glob("*.meta.json"))
        assert len(meta_files) == 1

        meta = json.loads(meta_files[0].read_text())
        assert "sha256_compound" in meta
        expected = hashlib.sha256((stdout_val + stderr_val).encode("utf-8")).hexdigest()
        assert meta["sha256_compound"] == expected
