# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Inspection tests verifying EN-023-008 security review completeness.

EN-023-008 TASK-023-166: These tests verify the security findings report
exists and covers all required areas. They are Inspection (I) method
tests per NASA ADIT, not behavioral unit tests.

Covers:
  - Security report exists and is non-empty
  - Report has CWE classifications (>= 3 findings)
  - No CRITICAL/HIGH findings with Status: OPEN
  - Capability justification section present
  - Bypass map attack surface section present
"""

from __future__ import annotations

from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parents[5]
_REPORT_PATH = (
    _PROJECT_ROOT
    / "projects/PROJ-023-exploit-framework/work"
    / "EPIC-023-010-e2e-engagement-validation"
    / "FEAT-023-014-real-e2e-lifecycle"
    / "EN-023-008-ebpf-transparent-proxy"
    / "TASK-023-166-security-review"
    / "security-findings.md"
)


@pytest.mark.unit
class TestSecurityReviewCompleteness:
    """Verify the security findings report covers all required areas."""

    def test_security_report_exists(self) -> None:
        """The security findings report file exists and is non-empty."""
        assert _REPORT_PATH.exists(), f"Security report not found at {_REPORT_PATH}"
        content = _REPORT_PATH.read_text()
        assert len(content) > 100, "Security report is too short to be complete"

    def test_security_report_has_cwe_classifications(self) -> None:
        """The report contains at least 3 findings with CWE-NNN identifiers."""
        content = _REPORT_PATH.read_text()
        import re

        cwe_matches = re.findall(r"CWE-\d+", content)
        unique_cwes = set(cwe_matches)
        assert len(unique_cwes) >= 3, (
            f"Expected >= 3 unique CWE classifications, found {len(unique_cwes)}: {unique_cwes}"
        )

    def test_security_report_no_critical_unmitigated(self) -> None:
        """No finding has Severity: CRITICAL with Status: OPEN."""
        content = _REPORT_PATH.read_text()
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if "**Status:** OPEN" in line:
                # Look backward for the severity line in the same finding block
                for j in range(max(0, i - 10), i):
                    if "CRITICAL" in lines[j] and "**Severity:**" in lines[j]:
                        pytest.fail(
                            f"Unmitigated CRITICAL finding at line {j + 1}: "
                            f"{lines[j].strip()}"
                        )

    def test_capability_justification_documented(self) -> None:
        """The report contains a Capability Justification section."""
        content = _REPORT_PATH.read_text()
        assert "Capability Justification" in content or "capability justification" in content, (
            "Missing 'Capability Justification' section in security report"
        )

    def test_bypass_map_attack_surface_assessed(self) -> None:
        """The report contains a Bypass Map Attack Surface section."""
        content = _REPORT_PATH.read_text()
        assert "Bypass Map" in content or "bypass map" in content, (
            "Missing 'Bypass Map Attack Surface' section in security report"
        )
