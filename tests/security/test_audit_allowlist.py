# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for scripts/security/audit_allowlist.py — fail-closed CVE accept-list parser.

Security-critical logic deserves direct unit coverage.  Tests invoke the script
both via function-level import and via subprocess (uv run python) to verify the
full exit-code contract that the composite action relies on.

PyYAML skip guard: `importorskip` at module level skips this entire file if
PyYAML is absent — this NEVER breaks CI.  In practice PyYAML is always present
when running `uv sync --all-extras` (transitive dep via mkdocs-material).
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from datetime import date, timedelta
from pathlib import Path

import pytest

yaml = pytest.importorskip("yaml")  # skip gracefully if PyYAML is absent

# ---------------------------------------------------------------------------
# Import the module under test.
# The script lives at scripts/security/audit_allowlist.py; we add the repo root
# to sys.path so the import resolves without installing the package.
# ---------------------------------------------------------------------------
WT_ROOT = Path(__file__).parent.parent.parent  # tests/security/../../ == worktree root
sys.path.insert(0, str(WT_ROOT))

from scripts.security.audit_allowlist import (  # noqa: E402
    _build_ignore_flags,
    _validate_entries,
    main,
)

SCRIPT_PATH = WT_ROOT / "scripts" / "security" / "audit_allowlist.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_allowlist(tmp_path: Path, content: str) -> Path:
    """Write YAML content to a temp audit-allowlist.yml and return its path."""
    f = tmp_path / "audit-allowlist.yml"
    f.write_text(textwrap.dedent(content), encoding="utf-8")
    return f


def _valid_entry(
    *,
    cve_id: str = "CVE-2099-00001",
    review_by: date | None = None,
    accepted_on: date | None = None,
) -> dict:
    """Build a minimally valid allowlist entry."""
    today = date.today()
    if accepted_on is None:
        accepted_on = today
    if review_by is None:
        review_by = today + timedelta(days=30)
    return {
        "id": cve_id,
        "package": "example-pkg",
        "reason": "No upstream fix; code path not reachable in Jerry.",
        "accepted_by": "geekatron",
        "accepted_on": accepted_on.isoformat(),
        "review_by": review_by.isoformat(),
        "ticket": "https://github.com/geekatron/jerry/issues/999",
    }


# ---------------------------------------------------------------------------
# (a) Valid unexpired entry → exit 0, prints --ignore-vuln <id>
# ---------------------------------------------------------------------------


class TestValidUnexpiredEntry:
    """Valid entry with review_by in the future → flags emitted, exit 0."""

    def test_main_exits_zero(self, tmp_path: Path) -> None:
        f = _write_allowlist(
            tmp_path,
            """
            accepted:
              - id: CVE-2099-00001
                package: example-pkg
                reason: No fix available yet.
                accepted_by: geekatron
                accepted_on: 2026-06-01
                review_by: 2026-08-30
                ticket: https://github.com/geekatron/jerry/issues/999
        """,
        )
        result = main(["--allowlist", str(f)])
        assert result == 0

    def test_main_prints_ignore_flag(self, tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
        f = _write_allowlist(
            tmp_path,
            """
            accepted:
              - id: CVE-2099-00001
                package: example-pkg
                reason: No fix available yet.
                accepted_by: geekatron
                accepted_on: 2026-06-01
                review_by: 2026-08-30
                ticket: https://github.com/geekatron/jerry/issues/999
        """,
        )
        main(["--allowlist", str(f)])
        captured = capsys.readouterr()
        assert "--ignore-vuln" in captured.out
        assert "CVE-2099-00001" in captured.out

    def test_subprocess_exit_zero_and_flag_present(self, tmp_path: Path) -> None:
        """Subprocess variant — validates the full exit-code contract."""
        f = _write_allowlist(
            tmp_path,
            """
            accepted:
              - id: CVE-2099-99999
                package: some-pkg
                reason: Mitigation in place.
                accepted_by: geekatron
                accepted_on: 2026-06-01
                review_by: 2026-08-30
                ticket: https://github.com/geekatron/jerry/issues/999
        """,
        )
        result = subprocess.run(
            [
                "uv",
                "run",
                "--all-extras",
                "--project",
                str(WT_ROOT),
                "python",
                str(SCRIPT_PATH),
                "--allowlist",
                str(f),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
        assert "--ignore-vuln" in result.stdout
        assert "CVE-2099-99999" in result.stdout


# ---------------------------------------------------------------------------
# (b) Missing required field → exit 1
# ---------------------------------------------------------------------------


class TestMissingRequiredField:
    """Entry missing a required field must cause exit 1."""

    def test_missing_review_by_exits_one(self, tmp_path: Path) -> None:
        f = _write_allowlist(
            tmp_path,
            """
            accepted:
              - id: CVE-2099-00002
                package: example-pkg
                reason: Some reason.
                accepted_by: geekatron
                accepted_on: 2026-06-01
                ticket: https://github.com/geekatron/jerry/issues/999
        """,
        )
        result = main(["--allowlist", str(f)])
        assert result == 1

    def test_missing_reason_exits_one(self, tmp_path: Path) -> None:
        entry = _valid_entry(cve_id="CVE-2099-00003")
        del entry["reason"]
        errors = _validate_entries([entry], date.today())
        assert any("reason" in e for e in errors)

    def test_empty_ticket_exits_one(self, tmp_path: Path) -> None:
        entry = _valid_entry(cve_id="CVE-2099-00004")
        entry["ticket"] = ""
        errors = _validate_entries([entry], date.today())
        assert any("ticket" in e for e in errors)

    def test_subprocess_missing_field_exits_one(self, tmp_path: Path) -> None:
        f = _write_allowlist(
            tmp_path,
            """
            accepted:
              - id: CVE-2099-00005
                package: example-pkg
                reason: Some reason.
                accepted_by: geekatron
                accepted_on: 2026-06-01
                ticket: https://github.com/geekatron/jerry/issues/999
        """,
        )
        result = subprocess.run(
            [
                "uv",
                "run",
                "--all-extras",
                "--project",
                str(WT_ROOT),
                "python",
                str(SCRIPT_PATH),
                "--allowlist",
                str(f),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1


# ---------------------------------------------------------------------------
# (c) Malformed YAML / top-level not a mapping / `accepted` not a list → exit 1
# ---------------------------------------------------------------------------


class TestMalformedYaml:
    """Structural or parse errors must exit 1, never silently continue."""

    def test_invalid_yaml_syntax_exits_one(self, tmp_path: Path) -> None:
        f = tmp_path / "audit-allowlist.yml"
        f.write_text("accepted: [unclosed", encoding="utf-8")
        result = main(["--allowlist", str(f)])
        assert result == 1

    def test_top_level_list_exits_one(self, tmp_path: Path) -> None:
        f = _write_allowlist(
            tmp_path,
            """
            - id: CVE-2099-00006
              package: example-pkg
        """,
        )
        result = main(["--allowlist", str(f)])
        assert result == 1

    def test_accepted_not_a_list_exits_one(self, tmp_path: Path) -> None:
        f = _write_allowlist(
            tmp_path,
            """
            accepted: "this should be a list"
        """,
        )
        result = main(["--allowlist", str(f)])
        assert result == 1

    def test_accepted_is_mapping_exits_one(self, tmp_path: Path) -> None:
        f = _write_allowlist(
            tmp_path,
            """
            accepted:
              id: CVE-2099-00007
              package: example-pkg
        """,
        )
        result = main(["--allowlist", str(f)])
        assert result == 1

    def test_missing_accepted_key_exits_one(self, tmp_path: Path) -> None:
        f = _write_allowlist(
            tmp_path,
            """
            suppressed:
              - id: CVE-2099-00008
        """,
        )
        result = main(["--allowlist", str(f)])
        assert result == 1

    def test_subprocess_malformed_exits_one(self, tmp_path: Path) -> None:
        f = tmp_path / "audit-allowlist.yml"
        f.write_text("accepted: [unclosed", encoding="utf-8")
        result = subprocess.run(
            [
                "uv",
                "run",
                "--all-extras",
                "--project",
                str(WT_ROOT),
                "python",
                str(SCRIPT_PATH),
                "--allowlist",
                str(f),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1


# ---------------------------------------------------------------------------
# (d) review_by - accepted_on > 90 days → exit 1
# ---------------------------------------------------------------------------


class TestNinetyDayCap:
    """Entries exceeding the 90-day acceptance window must be rejected."""

    def test_91_day_window_exits_one(self, tmp_path: Path) -> None:
        today = date.today()
        accepted_on = today - timedelta(days=1)
        review_by = accepted_on + timedelta(days=91)
        entry = _valid_entry(accepted_on=accepted_on, review_by=review_by)
        errors = _validate_entries([entry], today)
        assert any("91" in e or "max allowed" in e for e in errors)

    def test_exactly_90_day_window_passes(self) -> None:
        today = date.today()
        accepted_on = today - timedelta(days=1)
        review_by = accepted_on + timedelta(days=90)  # exactly at cap
        entry = _valid_entry(accepted_on=accepted_on, review_by=review_by)
        errors = _validate_entries([entry], today - timedelta(days=2))  # not yet expired
        cap_errors = [e for e in errors if "max allowed" in e]
        assert cap_errors == [], f"Unexpected cap violation: {cap_errors}"

    def test_100_day_window_main_exits_one(self, tmp_path: Path) -> None:
        today = date.today()
        accepted_on = (today - timedelta(days=5)).isoformat()
        review_by = (today + timedelta(days=95)).isoformat()
        f = _write_allowlist(
            tmp_path,
            f"""
            accepted:
              - id: CVE-2099-00009
                package: example-pkg
                reason: Some reason.
                accepted_by: geekatron
                accepted_on: {accepted_on}
                review_by: {review_by}
                ticket: https://github.com/geekatron/jerry/issues/999
        """,
        )
        result = main(["--allowlist", str(f)])
        assert result == 1


# ---------------------------------------------------------------------------
# (e) Expiry boundary: today >= review_by → entry NOT suppressed (exit 1)
# ---------------------------------------------------------------------------


class TestExpiryBoundary:
    """On the review_by date itself the entry is expired (>= semantics)."""

    def test_review_by_today_is_expired(self) -> None:
        today = date.today()
        entry = _valid_entry(
            review_by=today,  # today == review_by → expired
            accepted_on=today - timedelta(days=30),
        )
        errors = _validate_entries([entry], today)
        assert any("expired" in e for e in errors)

    def test_review_by_yesterday_is_expired(self) -> None:
        today = date.today()
        entry = _valid_entry(
            review_by=today - timedelta(days=1),
            accepted_on=today - timedelta(days=31),
        )
        errors = _validate_entries([entry], today)
        assert any("expired" in e for e in errors)

    def test_review_by_tomorrow_is_not_expired(self) -> None:
        today = date.today()
        entry = _valid_entry(
            review_by=today + timedelta(days=1),
            accepted_on=today - timedelta(days=1),
        )
        errors = _validate_entries([entry], today)
        expiry_errors = [e for e in errors if "expired" in e]
        assert expiry_errors == [], f"Should not be expired yet: {expiry_errors}"

    def test_expired_entry_not_in_flags(self) -> None:
        today = date.today()
        expired = _valid_entry(cve_id="CVE-2099-EXPIRED", review_by=today)
        # _build_ignore_flags is called only after validation passes;
        # for this test we call it directly to verify belt-and-suspenders guard.
        flags = _build_ignore_flags([expired], today)
        assert "--ignore-vuln" not in flags
        assert "CVE-2099-EXPIRED" not in flags

    def test_main_exits_one_when_expired(self, tmp_path: Path) -> None:
        today = date.today()
        accepted_on = (today - timedelta(days=30)).isoformat()
        review_by = today.isoformat()  # on boundary — expired
        f = _write_allowlist(
            tmp_path,
            f"""
            accepted:
              - id: CVE-2099-EXPBND
                package: example-pkg
                reason: Some reason.
                accepted_by: geekatron
                accepted_on: {accepted_on}
                review_by: {review_by}
                ticket: https://github.com/geekatron/jerry/issues/999
        """,
        )
        result = main(["--allowlist", str(f)])
        assert result == 1

    def test_subprocess_expired_exits_one(self, tmp_path: Path) -> None:
        today = date.today()
        accepted_on = (today - timedelta(days=30)).isoformat()
        review_by = today.isoformat()
        f = _write_allowlist(
            tmp_path,
            f"""
            accepted:
              - id: CVE-2099-SUBEXP
                package: example-pkg
                reason: Some reason.
                accepted_by: geekatron
                accepted_on: {accepted_on}
                review_by: {review_by}
                ticket: https://github.com/geekatron/jerry/issues/999
        """,
        )
        result = subprocess.run(
            [
                "uv",
                "run",
                "--all-extras",
                "--project",
                str(WT_ROOT),
                "python",
                str(SCRIPT_PATH),
                "--allowlist",
                str(f),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1


# ---------------------------------------------------------------------------
# Empty allowlist → exit 0, no flags
# ---------------------------------------------------------------------------


class TestEmptyAllowlist:
    """An allowlist with no accepted entries is valid and produces no flags."""

    def test_empty_list_exits_zero(self, tmp_path: Path) -> None:
        f = _write_allowlist(tmp_path, "accepted: []\n")
        result = main(["--allowlist", str(f)])
        assert result == 0

    def test_absent_file_exits_zero(self, tmp_path: Path) -> None:
        nonexistent = tmp_path / "no-such-file.yml"
        result = main(["--allowlist", str(nonexistent)])
        assert result == 0

    def test_empty_list_subprocess_exit_zero(self, tmp_path: Path) -> None:
        f = _write_allowlist(tmp_path, "accepted: []\n")
        result = subprocess.run(
            [
                "uv",
                "run",
                "--all-extras",
                "--project",
                str(WT_ROOT),
                "python",
                str(SCRIPT_PATH),
                "--allowlist",
                str(f),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"stderr: {result.stderr}"
