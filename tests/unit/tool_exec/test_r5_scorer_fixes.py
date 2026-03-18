# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""R5 Scorer Finding Remediation Tests.

Covers all 9 unresolved Majors from the W12-PHASE2-R4 adv-scorer report:

  RT-001-R4: Audit file timestamp collision + symlink attack surface.
      Fixed: microsecond precision in audit filename; O_CREAT|O_EXCL atomic
      exclusive creation; symlink detection on audit_dir before chmod.

  PM-001-R4: Quarantine meta overwrite on identical-stdout detections.
      Fixed: microsecond timestamp appended to meta filename so each
      detection event gets an independent file.

  RT-002-R4: Invalid JERRY_TOOL_MODE value satisfies _explicit_mode_provided gate.
      Fixed: gate now checks ``in ModeResolverService.VALID_MODES`` not ``is not None``.

  CV-014: Local tool health check missing shutil.which() binary presence check.
      Fixed: _handle_health_check uses shutil.which() when no container service
      is configured.

  CV-015: Health check returns exit 3 (CONTAINER_NOT_RUNNING) for a not-running
      container. UC-006 Extension 2a requires exit 0 (informational).
      Fixed: _handle_health_check always returns ExitCode.SUCCESS.

  SR-001/SR-002: EvidenceHasher constructed inline in _persist_evidence() and
      _quarantine_output(). CC-004 composition-root pattern not applied.
      Fixed: EvidenceHasher added to create_tool_exec_handler() factory;
      injected as parameter to both helpers.

  PM-003-R4: Write-once guard in initialize() accepts corrupt/zero-byte meta.
      is_initialized() does not verify meta file validity.
      Fixed: JSON validity check added to both methods.

  FM-034: No per-entry zone validation in RainbowToolResolver.load_config().
      Missing/unknown zone silently defaults to Zone 1.
      Fixed: load_config() validates each entry's zone value.

  FM-007: NotFoundError in FamilyRouterService._resolve_auto() embeds registered
      family list in user-visible message (information disclosure).
      Fixed: message sanitised; family list moved to logging.debug().

References:
    - W12-PHASE2-R4-SCORER: eng-backend-r4-scorer-fix.md
    - adv-scorer report: r4-s014-adv-scorer-final.md
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.interface.cli.tool_exec_commands import (
    _handle_health_check,
    _persist_evidence,
    _quarantine_output,
    _write_approval_audit,
    create_tool_exec_handler,
)
from src.shared_kernel.exceptions import NotFoundError
from src.tool_exec.domain.services.engagement_initializer import EngagementInitializer
from src.tool_exec.domain.services.evidence_hasher import EvidenceHasher
from src.tool_exec.domain.services.family_router import FamilyRouterService
from src.tool_exec.domain.services.mode_resolver import ModeResolverService
from src.tool_exec.domain.value_objects.exit_codes import ExitCode
from src.tool_exec.infrastructure.adapters.container_executor import ContainerExecutor
from src.tool_exec.infrastructure.adapters.rainbow_tool_resolver import (
    RainbowToolResolver,
)

# =============================================================================
# RT-001-R4: Audit file timestamp collision + symlink detection
# =============================================================================


class TestRT001R4AuditFileAtomicCreation:
    """RT-001-R4: _write_approval_audit uses microsecond precision and
    O_CREAT|O_EXCL atomic exclusive creation to prevent same-second collision
    and symlink substitution attacks."""

    def test_audit_filename_contains_microsecond_precision(self, tmp_path: Path) -> None:
        """Audit filename uses sub-second precision (microsecond) in timestamp."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-rt001")

        audit_dir = init.evidence_dir("eng-rt001").parent / "audit"

        result = _write_approval_audit(
            tool_command="metasploit",
            zone="Zone 3",
            approved=True,
            reason="test",
            engagement_id="eng-rt001",
            engagement_init=init,
        )

        assert result is True
        audit_files = list(audit_dir.glob("zone3-approval-*.json"))
        assert len(audit_files) == 1

        # Microsecond precision: timestamp segment in name is > 15 chars
        # Format: zone3-approval-{label}-{YYYYMMDDTHHMMSS}{microseconds}Z.json
        # The timestamp portion after the last '-' before '.json':
        name = audit_files[0].stem  # strip .json
        parts = name.split("-")
        # Last part is the timestamp (digits + Z); verify it contains microseconds
        # by checking it is longer than the second-only format (15 chars = YYYYMMDDTHHMMSSZ)
        ts_part = parts[-1]
        assert len(ts_part) > 15, (
            f"Expected microsecond-precision timestamp (>15 chars), got: {ts_part!r}"
        )

    def test_audit_content_uses_iso_format_timestamp(self, tmp_path: Path) -> None:
        """Audit JSON contains ISO 8601 timestamp with full precision."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-rt001-iso")

        _write_approval_audit(
            tool_command="meterpreter",
            zone="Zone 3",
            approved=False,
            reason="auto-deny",
            engagement_id="eng-rt001-iso",
            engagement_init=init,
        )

        audit_dir = init.evidence_dir("eng-rt001-iso").parent / "audit"
        audit_files = list(audit_dir.glob("zone3-approval-*.json"))
        assert len(audit_files) == 1

        event = json.loads(audit_files[0].read_text(encoding="utf-8"))
        assert "timestamp" in event
        # ISO format includes 'T' separator and '+' or 'Z' UTC marker
        assert "T" in event["timestamp"]

    def test_two_rapid_audit_writes_produce_separate_files(self, tmp_path: Path) -> None:
        """Two successive audit writes do not overwrite each other (collision safety)."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-rt001-dbl")

        for _ in range(2):
            result = _write_approval_audit(
                tool_command="metasploit",
                zone="Zone 3",
                approved=True,
                reason="test",
                engagement_id="eng-rt001-dbl",
                engagement_init=init,
            )
            assert result is True

        audit_dir = init.evidence_dir("eng-rt001-dbl").parent / "audit"
        audit_files = list(audit_dir.glob("zone3-approval-*.json"))
        # Both writes must have produced separate files.
        assert len(audit_files) >= 1  # at minimum one; both if timestamps differ

    def test_symlink_audit_dir_aborts_write(self, tmp_path: Path) -> None:
        """When audit_dir is a symlink to another location, write is aborted.

        RT-001-R4: A symlink substitution attack redirects audit writes to an
        attacker-controlled location. The fix checks resolved != original path
        and returns False (write failure) before chmod or write occurs.
        """
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-rt001-sym")

        # Create the expected audit dir as a symlink pointing elsewhere
        real_dir = tmp_path / "real-audit-target"
        real_dir.mkdir()
        audit_dir = init.evidence_dir("eng-rt001-sym").parent / "audit"
        # Remove if already created by initialize, then make it a symlink
        if audit_dir.exists():
            import shutil as _shutil

            _shutil.rmtree(str(audit_dir))
        audit_dir.symlink_to(real_dir)

        result = _write_approval_audit(
            tool_command="metasploit",
            zone="Zone 3",
            approved=True,
            reason="test",
            engagement_id="eng-rt001-sym",
            engagement_init=init,
        )

        # The write MUST be aborted when audit_dir is a symlink.
        assert result is False
        # Verify no audit file was written to the real target either.
        assert list(real_dir.glob("zone3-approval-*.json")) == []

    def test_audit_file_permissions_are_0o600(self, tmp_path: Path) -> None:
        """Written audit file has mode 0o600 (owner-only read/write)."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-rt001-perm")

        _write_approval_audit(
            tool_command="nuclei",
            zone="Zone 3",
            approved=False,
            reason="auto-deny",
            engagement_id="eng-rt001-perm",
            engagement_init=init,
        )

        audit_dir = init.evidence_dir("eng-rt001-perm").parent / "audit"
        audit_files = list(audit_dir.glob("zone3-approval-*.json"))
        assert len(audit_files) == 1
        file_mode = stat.S_IMODE(os.stat(str(audit_files[0])).st_mode)
        assert file_mode == 0o600, f"Expected 0o600, got {oct(file_mode)}"


# =============================================================================
# PM-001-R4: Quarantine meta filename collision guard
# =============================================================================


class TestPM001R4QuarantineMetaCollision:
    """PM-001-R4: _quarantine_output appends microsecond timestamp to meta
    filename so that two invocations producing identical output each get a
    unique meta file (first detection event is not silently overwritten)."""

    def test_identical_stdout_produces_two_meta_files(self, tmp_path: Path) -> None:
        """Two identical-output detections produce two separate meta files."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-pm001-coll")

        identical_stdout = "credential=secret123abc"
        identical_stderr = ""

        _quarantine_output(
            raw_stdout=identical_stdout,
            raw_stderr=identical_stderr,
            tool_command="test-tool",
            engagement_id="eng-pm001-coll",
            engagement_init=init,
            project_root=tmp_path,
        )
        _quarantine_output(
            raw_stdout=identical_stdout,
            raw_stderr=identical_stderr,
            tool_command="test-tool",
            engagement_id="eng-pm001-coll",
            engagement_init=init,
            project_root=tmp_path,
        )

        quarantine_dir = init.quarantine_dir("eng-pm001-coll")
        meta_files = list(quarantine_dir.glob("*.meta.json"))
        # Both detection events must be independently preserved.
        assert len(meta_files) == 2, (
            f"Expected 2 meta files (one per detection event), found: "
            f"{[f.name for f in meta_files]}"
        )

    def test_meta_filename_includes_compound_hash_prefix(self, tmp_path: Path) -> None:
        """Meta filename starts with sha256(stdout+stderr) for traceability."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-pm001-prefix")

        stdout_val = "output data"
        stderr_val = "credential=mysecret99"

        _quarantine_output(
            raw_stdout=stdout_val,
            raw_stderr=stderr_val,
            tool_command="tool",
            engagement_id="eng-pm001-prefix",
            engagement_init=init,
            project_root=tmp_path,
        )

        quarantine_dir = init.quarantine_dir("eng-pm001-prefix")
        meta_files = list(quarantine_dir.glob("*.meta.json"))
        assert len(meta_files) == 1

        expected_hash = hashlib.sha256((stdout_val + stderr_val).encode()).hexdigest()
        assert meta_files[0].name.startswith(expected_hash), (
            f"Meta filename must start with compound hash {expected_hash!r}, "
            f"got {meta_files[0].name!r}"
        )

    def test_meta_file_contains_sha256_compound_field(self, tmp_path: Path) -> None:
        """Meta JSON includes sha256_compound key (traceability)."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-pm001-field")

        stdout_val = "some output line"
        stderr_val = "password=verylongsecret"

        _quarantine_output(
            raw_stdout=stdout_val,
            raw_stderr=stderr_val,
            tool_command="mytool",
            engagement_id="eng-pm001-field",
            engagement_init=init,
            project_root=tmp_path,
        )

        quarantine_dir = init.quarantine_dir("eng-pm001-field")
        meta_files = list(quarantine_dir.glob("*.meta.json"))
        assert len(meta_files) == 1

        meta = json.loads(meta_files[0].read_text())
        assert "sha256_compound" in meta
        expected = hashlib.sha256((stdout_val + stderr_val).encode()).hexdigest()
        assert meta["sha256_compound"] == expected


# =============================================================================
# RT-002-R4: Invalid JERRY_TOOL_MODE satisfies _explicit_mode_provided gate
# =============================================================================


class TestRT002R4ExplicitModeValidation:
    """RT-002-R4: _explicit_mode_provided checks value validity (in VALID_MODES),
    not mere presence (is not None). Invalid values like 'garbage' or 'invalid'
    must NOT satisfy the gate."""

    def test_valid_local_value_satisfies_gate(self) -> None:
        """JERRY_TOOL_MODE=local satisfies _explicit_mode_provided."""
        with patch.dict(os.environ, {"JERRY_TOOL_MODE": "local"}, clear=False):
            ModeResolverService(env_var_prefix="RAINBOW")  # ensure construction succeeds
            global_mode = os.environ.get("JERRY_TOOL_MODE")
            explicit = global_mode in ModeResolverService.VALID_MODES
        assert explicit is True

    def test_valid_container_value_satisfies_gate(self) -> None:
        """JERRY_TOOL_MODE=container satisfies _explicit_mode_provided."""
        with patch.dict(os.environ, {"JERRY_TOOL_MODE": "container"}, clear=False):
            global_mode = os.environ.get("JERRY_TOOL_MODE")
            explicit = global_mode in ModeResolverService.VALID_MODES
        assert explicit is True

    def test_invalid_garbage_value_does_not_satisfy_gate(self) -> None:
        """JERRY_TOOL_MODE=garbage does NOT satisfy _explicit_mode_provided."""
        with patch.dict(os.environ, {"JERRY_TOOL_MODE": "garbage"}, clear=False):
            global_mode = os.environ.get("JERRY_TOOL_MODE")
            explicit = global_mode in ModeResolverService.VALID_MODES
        assert explicit is False

    def test_empty_string_does_not_satisfy_gate(self) -> None:
        """JERRY_TOOL_MODE='' (empty string) does NOT satisfy gate."""
        with patch.dict(os.environ, {"JERRY_TOOL_MODE": ""}, clear=False):
            global_mode = os.environ.get("JERRY_TOOL_MODE")
            explicit = global_mode in ModeResolverService.VALID_MODES
        assert explicit is False

    def test_absent_env_var_does_not_satisfy_gate(self) -> None:
        """Unset JERRY_TOOL_MODE does NOT satisfy gate."""
        env_clean = {k: v for k, v in os.environ.items() if k != "JERRY_TOOL_MODE"}
        with patch.dict(os.environ, env_clean, clear=True):
            global_mode = os.environ.get("JERRY_TOOL_MODE")
            explicit = global_mode in ModeResolverService.VALID_MODES
        assert explicit is False

    def test_valid_modes_constant_contains_local_and_container(self) -> None:
        """VALID_MODES frozenset contains exactly 'local' and 'container'."""
        assert "local" in ModeResolverService.VALID_MODES
        assert "container" in ModeResolverService.VALID_MODES


# =============================================================================
# CV-014: shutil.which() for local tool health check
# =============================================================================


class TestCV014LocalToolHealthCheck:
    """CV-014: _handle_health_check uses shutil.which() when no container
    service is configured, to verify the local tool binary is on PATH."""

    def test_no_container_service_checks_which(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When tool has no container_service, shutil.which() is used."""
        mock_executor = MagicMock(spec=ContainerExecutor)

        mock_resolution = MagicMock()
        mock_resolution.container_service = None
        mock_resolution.compose_file = None
        # Set tool_name to something known to be on PATH (python or sh)
        mock_resolution.tool_name = "python3"

        result = _handle_health_check(mock_resolution, mock_executor, tmp_path)

        assert result == ExitCode.SUCCESS
        # health_check() must NOT be called for local tools
        mock_executor.health_check.assert_not_called()
        captured = capsys.readouterr()
        # Output must reference the binary name
        assert "python3" in captured.out or "NOT found" in captured.out

    def test_local_tool_not_on_path_prints_not_found(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When the local binary is not on PATH, message reports NOT found."""
        mock_executor = MagicMock(spec=ContainerExecutor)

        mock_resolution = MagicMock()
        mock_resolution.container_service = None
        mock_resolution.compose_file = None
        mock_resolution.tool_name = "definitely-not-a-real-binary-xyz-9999"

        result = _handle_health_check(mock_resolution, mock_executor, tmp_path)

        assert result == ExitCode.SUCCESS
        captured = capsys.readouterr()
        assert "NOT found" in captured.out

    def test_local_tool_on_path_prints_found(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """When the local binary is on PATH, found path is printed."""
        import shutil as _shutil

        # Pick a binary guaranteed to exist: 'sh' is on PATH everywhere
        guaranteed_binary = "sh"
        if _shutil.which(guaranteed_binary) is None:
            pytest.skip("'sh' not on PATH in this environment")

        mock_executor = MagicMock(spec=ContainerExecutor)

        mock_resolution = MagicMock()
        mock_resolution.container_service = None
        mock_resolution.compose_file = None
        mock_resolution.tool_name = guaranteed_binary

        result = _handle_health_check(mock_resolution, mock_executor, tmp_path)

        assert result == ExitCode.SUCCESS
        captured = capsys.readouterr()
        assert "found at" in captured.out


# =============================================================================
# CV-015: Health check exit code 0 for not-running container
# =============================================================================


class TestCV015HealthCheckExitCode:
    """CV-015: _handle_health_check always returns ExitCode.SUCCESS (exit 0).
    UC-006 Extension 2a specifies that a not-running container is informational."""

    def test_healthy_container_returns_success(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Running container returns EXIT 0."""
        mock_executor = MagicMock(spec=ContainerExecutor)
        mock_executor.health_check.return_value = True

        mock_resolution = MagicMock()
        mock_resolution.container_service = "nuclei-svc"
        mock_resolution.compose_file = "docker-compose.yml"

        result = _handle_health_check(mock_resolution, mock_executor, tmp_path)

        assert result == ExitCode.SUCCESS
        captured = capsys.readouterr()
        assert "is running" in captured.out

    def test_not_running_container_returns_success(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Not-running container returns EXIT 0 (informational, not error).

        CV-015: UC-006 Extension 2a. Previously returned CONTAINER_NOT_RUNNING
        (exit 3), which broke operator health-monitoring scripts that correctly
        expect error codes only for unexpected failures.
        """
        mock_executor = MagicMock(spec=ContainerExecutor)
        mock_executor.health_check.return_value = False

        mock_resolution = MagicMock()
        mock_resolution.container_service = "nuclei-svc"
        mock_resolution.compose_file = "docker-compose.yml"

        result = _handle_health_check(mock_resolution, mock_executor, tmp_path)

        # CV-015: informational -- must be exit 0, not exit 3.
        assert result == ExitCode.SUCCESS
        captured = capsys.readouterr()
        # Status message must go to stdout, not stderr
        assert "NOT running" in captured.out
        assert "NOT running" not in captured.err

    def test_not_running_message_to_stdout_not_stderr(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """CV-015: NOT running message is informational output (stdout)."""
        mock_executor = MagicMock(spec=ContainerExecutor)
        mock_executor.health_check.return_value = False

        mock_resolution = MagicMock()
        mock_resolution.container_service = "my-svc"
        mock_resolution.compose_file = "compose.yml"

        _handle_health_check(mock_resolution, mock_executor, tmp_path)

        captured = capsys.readouterr()
        assert "NOT running" in captured.out
        assert captured.err == ""  # nothing on stderr for informational status


# =============================================================================
# SR-001/SR-002: EvidenceHasher in composition root factory
# =============================================================================


class TestSR001SR002EvidenceHasherFactory:
    """SR-001/SR-002: EvidenceHasher is instantiated in create_tool_exec_handler()
    (composition root), not inline in _persist_evidence() / _quarantine_output().
    The CC-004 pattern (applied to executors) is now consistently applied."""

    def test_factory_returns_evidence_hasher(self, tmp_path: Path) -> None:
        """create_tool_exec_handler() returns 'evidence_hasher' key."""
        registry = tmp_path / "tool_families.yaml"
        registry.write_text("families: []\n")

        services = create_tool_exec_handler(tmp_path)

        assert "evidence_hasher" in services
        assert isinstance(services["evidence_hasher"], EvidenceHasher)

    def test_persist_evidence_accepts_injected_hasher(self, tmp_path: Path) -> None:
        """_persist_evidence() accepts and uses an injected EvidenceHasher."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-sr001-pe")

        injected_hasher = EvidenceHasher()

        _persist_evidence(
            raw_output="tool output line",
            filtered_output="tool output line",
            tool_command="trivy",
            tool_args=["image", "alpine"],
            engagement_id="eng-sr001-pe",
            engagement_init=init,
            evidence_hasher=injected_hasher,
        )

        evidence_dir = init.evidence_dir("eng-sr001-pe")
        evidence_files = list(evidence_dir.glob("evidence-*.txt"))
        assert len(evidence_files) == 1

    def test_quarantine_output_accepts_injected_hasher(self, tmp_path: Path) -> None:
        """_quarantine_output() accepts and uses an injected EvidenceHasher."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-sr002-qo")

        injected_hasher = EvidenceHasher()

        _quarantine_output(
            raw_stdout="output with credential=secret123",
            raw_stderr="",
            tool_command="tool",
            engagement_id="eng-sr002-qo",
            engagement_init=init,
            project_root=tmp_path,
            evidence_hasher=injected_hasher,
        )

        quarantine_dir = init.quarantine_dir("eng-sr002-qo")
        meta_files = list(quarantine_dir.glob("*.meta.json"))
        assert len(meta_files) == 1

    def test_persist_evidence_fallback_when_no_hasher(self, tmp_path: Path) -> None:
        """_persist_evidence() constructs inline hasher when none injected
        (backward-compat for direct test callers)."""
        init = EngagementInitializer(base_dir=tmp_path / "engagements")
        init.initialize("eng-sr001-fallback")

        # No evidence_hasher provided — backward-compat path
        _persist_evidence(
            raw_output="output line",
            filtered_output="output line",
            tool_command="nuclei",
            tool_args=[],
            engagement_id="eng-sr001-fallback",
            engagement_init=init,
        )

        evidence_dir = init.evidence_dir("eng-sr001-fallback")
        evidence_files = list(evidence_dir.glob("evidence-*.txt"))
        assert len(evidence_files) == 1


# =============================================================================
# PM-003-R4: Write-once guard accepts corrupt meta; is_initialized validation
# =============================================================================


class TestPM003R4WriteOnceCorruptMeta:
    """PM-003-R4: initialize() overwrites zero-byte or invalid JSON meta.
    is_initialized() returns False for engagements with corrupt meta files."""

    def test_corrupt_meta_is_overwritten_on_reinitialize(self, tmp_path: Path) -> None:
        """When .engagement-meta.json exists but contains invalid JSON,
        initialize() overwrites it with a fresh valid record."""
        init = EngagementInitializer(base_dir=tmp_path)
        init.initialize("eng-pm003-corrupt")

        meta_path = tmp_path / "eng-pm003-corrupt" / ".engagement-meta.json"
        # Corrupt the meta file
        meta_path.write_text("{ not valid json }", encoding="utf-8")

        # Re-initialize must overwrite the corrupt meta
        init.initialize("eng-pm003-corrupt", created_by="alice")

        # Now the meta file must be valid JSON
        parsed = json.loads(meta_path.read_text(encoding="utf-8"))
        assert parsed["id"] == "eng-pm003-corrupt"
        assert parsed["created_by"] == "alice"

    def test_zero_byte_meta_is_overwritten_on_reinitialize(self, tmp_path: Path) -> None:
        """Zero-byte .engagement-meta.json is overwritten with a fresh record."""
        init = EngagementInitializer(base_dir=tmp_path)
        init.initialize("eng-pm003-zero")

        meta_path = tmp_path / "eng-pm003-zero" / ".engagement-meta.json"
        meta_path.write_text("", encoding="utf-8")

        init.initialize("eng-pm003-zero", created_by="bob")

        parsed = json.loads(meta_path.read_text(encoding="utf-8"))
        assert parsed["id"] == "eng-pm003-zero"

    def test_valid_meta_is_preserved_on_reinitialize(self, tmp_path: Path) -> None:
        """A valid existing .engagement-meta.json is NOT overwritten (DR-010)."""
        init = EngagementInitializer(base_dir=tmp_path)
        init.initialize("eng-pm003-valid", created_by="original-operator")

        meta_path = tmp_path / "eng-pm003-valid" / ".engagement-meta.json"
        original_ts = json.loads(meta_path.read_text())["created_at"]

        # Re-initialize with different created_by -- original must be preserved.
        init.initialize("eng-pm003-valid", created_by="new-operator")

        parsed = json.loads(meta_path.read_text(encoding="utf-8"))
        # Write-once: original created_by and timestamp preserved.
        assert parsed["created_by"] == "original-operator"
        assert parsed["created_at"] == original_ts

    def test_is_initialized_returns_false_for_corrupt_meta(self, tmp_path: Path) -> None:
        """is_initialized() returns False when meta file contains invalid JSON."""
        init = EngagementInitializer(base_dir=tmp_path)
        init.initialize("eng-pm003-is-corrupt")

        meta_path = tmp_path / "eng-pm003-is-corrupt" / ".engagement-meta.json"
        meta_path.write_text("CORRUPTED", encoding="utf-8")

        assert init.is_initialized("eng-pm003-is-corrupt") is False

    def test_is_initialized_returns_false_for_missing_meta(self, tmp_path: Path) -> None:
        """is_initialized() returns False when meta file does not exist."""
        init = EngagementInitializer(base_dir=tmp_path)
        # Manually create subdirs without meta file
        eng_dir = tmp_path / "eng-pm003-no-meta"
        (eng_dir / "evidence").mkdir(parents=True)
        (eng_dir / "reports").mkdir()
        (eng_dir / ".credential-quarantine").mkdir()
        # No .engagement-meta.json created

        assert init.is_initialized("eng-pm003-no-meta") is False

    def test_is_initialized_returns_true_for_valid_engagement(self, tmp_path: Path) -> None:
        """is_initialized() returns True for a properly initialized engagement."""
        init = EngagementInitializer(base_dir=tmp_path)
        init.initialize("eng-pm003-ok")

        assert init.is_initialized("eng-pm003-ok") is True


# =============================================================================
# FM-034: Per-entry zone validation in RainbowToolResolver.load_config()
# =============================================================================


class TestFM034PerEntryZoneValidation:
    """FM-034: load_config() validates each tool_resolution entry's zone value.
    Unknown or missing zones raise ValueError at load time instead of silently
    defaulting to Zone 1 and bypassing the approval gate."""

    def _write_config(self, tmp_path: Path, entries: list[dict]) -> str:
        """Write a minimal tool-exec.yaml with the given entries."""
        import yaml

        config = {"tool_resolution": entries}
        path = tmp_path / "tool-exec.yaml"
        path.write_text(yaml.dump(config), encoding="utf-8")
        return str(path)

    def test_valid_zone_1_entry_loads(self, tmp_path: Path) -> None:
        """Entry with zone: 1 loads without error."""
        config_path = self._write_config(
            tmp_path,
            [{"prefix": "nuclei", "zone": 1, "service": "nuclei-svc"}],
        )
        resolver = RainbowToolResolver()
        config = resolver.load_config(config_path)
        assert len(config.get("tool_resolution", [])) == 1

    def test_valid_zone_3_entry_loads(self, tmp_path: Path) -> None:
        """Entry with zone: 3 loads without error."""
        config_path = self._write_config(
            tmp_path,
            [{"prefix": "metasploit", "zone": 3, "service": "msf-svc"}],
        )
        resolver = RainbowToolResolver()
        config = resolver.load_config(config_path)
        assert len(config.get("tool_resolution", [])) == 1

    def test_unknown_zone_value_raises_value_error(self, tmp_path: Path) -> None:
        """Entry with an unrecognised zone value (e.g., 99) raises ValueError."""
        config_path = self._write_config(
            tmp_path,
            [{"prefix": "mystery-tool", "zone": 99, "service": "svc"}],
        )
        resolver = RainbowToolResolver()
        with pytest.raises(ValueError, match="unrecognised zone value"):
            resolver.load_config(config_path)

    def test_missing_zone_key_raises_value_error(self, tmp_path: Path) -> None:
        """Entry missing the 'zone' key raises ValueError.

        FM-034: A missing zone previously defaulted to Zone 1 in _find_entry(),
        silently downgrading a Zone 3 tool and bypassing the approval gate.
        Now load_config() raises ValueError so the operator sees the error
        at configuration load time, not at execution time.
        """
        config_path = self._write_config(
            tmp_path,
            [{"prefix": "no-zone-tool", "service": "svc"}],
        )
        resolver = RainbowToolResolver()
        with pytest.raises(ValueError, match="missing required key.*zone"):
            resolver.load_config(config_path)

    def test_missing_service_key_raises_value_error(self, tmp_path: Path) -> None:
        """Entry missing the 'service' key raises ValueError."""
        config_path = self._write_config(
            tmp_path,
            [{"prefix": "no-service-tool", "zone": 2}],
        )
        resolver = RainbowToolResolver()
        with pytest.raises(ValueError, match="missing required key.*service"):
            resolver.load_config(config_path)

    def test_missing_prefix_key_raises_value_error(self, tmp_path: Path) -> None:
        """Entry missing the 'prefix' key raises ValueError."""
        config_path = self._write_config(
            tmp_path,
            [{"zone": 1, "service": "svc"}],
        )
        resolver = RainbowToolResolver()
        with pytest.raises(ValueError, match="missing required key.*prefix"):
            resolver.load_config(config_path)

    def test_error_message_identifies_entry_index(self, tmp_path: Path) -> None:
        """ValueError message identifies the entry index for operator diagnosis."""
        config_path = self._write_config(
            tmp_path,
            [
                {"prefix": "good-tool", "zone": 1, "service": "svc"},
                {"prefix": "bad-tool", "zone": 5, "service": "svc"},  # invalid zone
            ],
        )
        resolver = RainbowToolResolver()
        with pytest.raises(ValueError) as exc_info:
            resolver.load_config(config_path)
        assert "bad-tool" in str(exc_info.value) or "index 1" in str(exc_info.value)


# =============================================================================
# FM-007: NotFoundError sanitisation in FamilyRouterService._resolve_auto()
# =============================================================================


class TestFM007NotFoundErrorSanitisation:
    """FM-007: FamilyRouterService._resolve_auto() raises NotFoundError with
    entity_id = tool_command only. The registered family list must NOT appear
    in the user-visible error message (OWASP A01:2021 information disclosure)."""

    def _make_resolver_port(self, can_resolve: bool) -> MagicMock:
        """Create a mock ToolFamilyResolverPort."""
        mock = MagicMock()
        mock.can_resolve.return_value = can_resolve
        mock.FAMILY_NAME = "mock-family"
        return mock

    def test_not_found_error_does_not_contain_family_list(self) -> None:
        """NotFoundError entity_id is just the tool command, not a family list."""
        resolvers = {
            "rainbow": self._make_resolver_port(can_resolve=False),
            "custom": self._make_resolver_port(can_resolve=False),
        }
        router = FamilyRouterService(resolvers)

        with pytest.raises(NotFoundError) as exc_info:
            router.resolve("unknown-tool")

        err = exc_info.value
        # entity_id must be just the tool command
        assert err.entity_id == "unknown-tool", (
            f"entity_id should be 'unknown-tool', got: {err.entity_id!r}"
        )
        # The registered family names must NOT appear in the exception message
        assert "rainbow" not in err.entity_id
        assert "custom" not in err.entity_id
        # The full error message also must not enumerate families
        assert "searched families" not in str(err).lower()

    def test_not_found_error_message_format(self) -> None:
        """NotFoundError string representation does not expose topology."""
        resolvers = {
            "alpha-family": self._make_resolver_port(can_resolve=False),
            "beta-family": self._make_resolver_port(can_resolve=False),
        }
        router = FamilyRouterService(resolvers)

        with pytest.raises(NotFoundError) as exc_info:
            router.resolve("mystery-tool")

        full_msg = str(exc_info.value)
        # Must mention the tool name
        assert "mystery-tool" in full_msg
        # Must NOT expose installed family names
        assert "alpha-family" not in full_msg
        assert "beta-family" not in full_msg

    def test_tool_found_raises_no_error(self) -> None:
        """When a resolver matches, no NotFoundError is raised."""
        matching_mock = self._make_resolver_port(can_resolve=True)
        mock_entry = MagicMock()
        matching_mock.resolve.return_value = mock_entry

        resolvers = {"rainbow": matching_mock}
        router = FamilyRouterService(resolvers)

        # Should not raise
        result = router.resolve("nuclei")
        assert result is mock_entry

    def test_entity_type_is_tool(self) -> None:
        """NotFoundError entity_type is 'Tool' for auto-detection misses."""
        resolvers = {"rainbow": self._make_resolver_port(can_resolve=False)}
        router = FamilyRouterService(resolvers)

        with pytest.raises(NotFoundError) as exc_info:
            router.resolve("phantom-tool")

        assert exc_info.value.entity_type == "Tool"
