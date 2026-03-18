# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""TASK-032: Engagement lifecycle E2E tests.

Tests the full --init-engagement -> evidence-persistence cycle through the
real CLI.  All filesystem assertions are against the live project tree;
cleanup is handled by the engagement_cleanup fixture.

Directory layout after --init-engagement E2E-TEST-{N}:
    work/engagements/E2E-TEST-{N}/
        evidence/
        reports/
        .credential-quarantine/    (mode 0o700)
        .engagement-meta.json      (JSON with id, created_at, created_by)

OWASP A01:2021: Engagement IDs are validated by EngagementInitializer._validate_id();
traversal tests belong in test_error_paths.py.

References:
    - TASK-032: Engagement lifecycle E2E
    - ADR-PROJ023-001: UC-003 Engagement Management
"""

from __future__ import annotations

import json
import stat
from pathlib import Path

import pytest

pytestmark = pytest.mark.e2e


class TestEngagementInit:
    """--init-engagement creates the expected directory structure."""

    def test_init_engagement_exit_0(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
    ) -> None:
        """--init-engagement E2E-TEST-L001 returns exit code 0."""
        eng_id = "E2E-TEST-L001"
        engagement_cleanup.append(eng_id)
        exit_code, stdout, stderr = cli_run("--init-engagement", eng_id)
        assert exit_code == 0, f"Expected exit 0. stderr={stderr!r}"

    def test_init_engagement_stdout_contains_path(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
    ) -> None:
        """--init-engagement prints the created path to stdout."""
        eng_id = "E2E-TEST-L002"
        engagement_cleanup.append(eng_id)
        exit_code, stdout, _stderr = cli_run("--init-engagement", eng_id)
        assert exit_code == 0
        assert eng_id in stdout, f"Expected engagement ID in stdout. stdout={stdout!r}"

    def test_init_creates_evidence_directory(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
        project_root: Path,
    ) -> None:
        """--init-engagement creates the evidence/ subdirectory."""
        eng_id = "E2E-TEST-L003"
        engagement_cleanup.append(eng_id)
        exit_code, _stdout, _stderr = cli_run("--init-engagement", eng_id)
        assert exit_code == 0
        evidence_dir = project_root / "work" / "engagements" / eng_id / "evidence"
        assert evidence_dir.is_dir(), f"evidence/ not created: {evidence_dir}"

    def test_init_creates_reports_directory(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
        project_root: Path,
    ) -> None:
        """--init-engagement creates the reports/ subdirectory."""
        eng_id = "E2E-TEST-L004"
        engagement_cleanup.append(eng_id)
        exit_code, _stdout, _stderr = cli_run("--init-engagement", eng_id)
        assert exit_code == 0
        reports_dir = project_root / "work" / "engagements" / eng_id / "reports"
        assert reports_dir.is_dir(), f"reports/ not created: {reports_dir}"

    def test_init_creates_quarantine_directory_with_restricted_permissions(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
        project_root: Path,
    ) -> None:
        """--init-engagement creates .credential-quarantine/ with mode 0o700.

        M-10 (T-21, DREAD 24): quarantine directory must not be world-readable.
        """
        eng_id = "E2E-TEST-L005"
        engagement_cleanup.append(eng_id)
        exit_code, _stdout, _stderr = cli_run("--init-engagement", eng_id)
        assert exit_code == 0
        quarantine_dir = project_root / "work" / "engagements" / eng_id / ".credential-quarantine"
        assert quarantine_dir.is_dir(), f".credential-quarantine/ not created: {quarantine_dir}"
        dir_mode = stat.S_IMODE(quarantine_dir.stat().st_mode)
        assert dir_mode == 0o700, f"Expected quarantine dir mode 0o700, got 0o{dir_mode:o}"

    def test_init_creates_meta_json(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
        project_root: Path,
    ) -> None:
        """--init-engagement writes .engagement-meta.json with required fields."""
        eng_id = "E2E-TEST-L006"
        engagement_cleanup.append(eng_id)
        exit_code, _stdout, _stderr = cli_run("--init-engagement", eng_id)
        assert exit_code == 0
        meta_path = project_root / "work" / "engagements" / eng_id / ".engagement-meta.json"
        assert meta_path.exists(), f".engagement-meta.json not created: {meta_path}"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        assert meta.get("id") == eng_id, f"meta.id mismatch: {meta}"
        assert "created_at" in meta, f"meta missing created_at: {meta}"
        assert "created_by" in meta, f"meta missing created_by: {meta}"

    def test_init_is_idempotent(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
        project_root: Path,
    ) -> None:
        """Running --init-engagement twice on the same ID is safe (idempotent).

        DR-010 write-once: the second call preserves the original created_at.
        """
        eng_id = "E2E-TEST-L007"
        engagement_cleanup.append(eng_id)

        exit_code_1, _stdout_1, _stderr_1 = cli_run("--init-engagement", eng_id)
        assert exit_code_1 == 0

        meta_path = project_root / "work" / "engagements" / eng_id / ".engagement-meta.json"
        first_created_at = json.loads(meta_path.read_text(encoding="utf-8"))["created_at"]

        exit_code_2, _stdout_2, _stderr_2 = cli_run("--init-engagement", eng_id)
        assert exit_code_2 == 0

        second_created_at = json.loads(meta_path.read_text(encoding="utf-8"))["created_at"]
        assert first_created_at == second_created_at, (
            "DR-010 violated: second init overwrote created_at. "
            f"first={first_created_at!r} second={second_created_at!r}"
        )


class TestEngagementWithToolExecution:
    """Zone 1 tool execution with --engagement-id persists evidence."""

    def test_syft_with_engagement_creates_evidence_file(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
        project_root: Path,
    ) -> None:
        """syft version with --engagement-id persists output to evidence/.

        Uses local mode because syft is installed on the host PATH and the
        docker-compose scanner service has no long-running process (exits
        immediately after start, making `docker compose exec` fail).

        Steps:
        1. Init engagement.
        2. Run syft version with --engagement-id in local mode.
        3. Verify at least one file appears in evidence/.
        """
        eng_id = "E2E-TEST-L008"
        engagement_cleanup.append(eng_id)

        init_code, _out, _err = cli_run("--init-engagement", eng_id)
        assert init_code == 0, f"Init failed. stderr={_err!r}"

        exec_code, stdout, stderr = cli_run(
            "--mode",
            "local",
            "--engagement-id",
            eng_id,
            "syft",
            "version",
        )
        assert exec_code == 0, (
            f"syft version with engagement failed. stdout={stdout!r} stderr={stderr!r}"
        )

        evidence_dir = project_root / "work" / "engagements" / eng_id / "evidence"
        evidence_files = list(evidence_dir.iterdir())
        assert evidence_files, (
            f"No evidence files created in {evidence_dir}. stdout={stdout!r} stderr={stderr!r}"
        )

    def test_evidence_file_contains_tool_output(
        self,
        cli_run,  # type: ignore[no-untyped-def]
        engagement_cleanup: list[str],
        project_root: Path,
    ) -> None:
        """The persisted evidence file contains the syft version output."""
        eng_id = "E2E-TEST-L009"
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
        # Find any non-metadata file (.json metadata files are expected alongside raw output)
        evidence_files = sorted(evidence_dir.iterdir())
        assert evidence_files, f"No evidence files in {evidence_dir}"

        # At least one file should contain text output (not just metadata JSON)
        combined_content = " ".join(
            f.read_text(encoding="utf-8", errors="replace") for f in evidence_files
        )
        assert "syft" in combined_content.lower(), (
            f"Evidence files do not contain 'syft'. Files: {[f.name for f in evidence_files]}"
        )
