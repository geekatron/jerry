# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Inspection tests verifying EN-023-008 C4 adversarial quality gate.

EN-023-008 TASK-023-167: These tests verify the adversarial review report
exists and covers all 10 strategies with the required quality threshold.
Inspection (I) method per NASA ADIT.

Covers:
  - Adversary report exists and is non-empty
  - All 10 strategies executed (S-001 through S-014, excluding 5)
  - Composite score meets C4 threshold (>= 0.95)
  - No CRITICAL/HIGH findings with Status: OPEN
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_REPORT_PATH = (
    _PROJECT_ROOT
    / "projects/PROJ-023-exploit-framework/work"
    / "EPIC-023-010-e2e-engagement-validation"
    / "FEAT-023-014-real-e2e-lifecycle"
    / "EN-023-008-ebpf-transparent-proxy"
    / "TASK-023-167-adversary-c4-gate"
    / "adversary-c4-report.md"
)

_REQUIRED_STRATEGIES = [
    "S-001", "S-002", "S-003", "S-004", "S-007",
    "S-010", "S-011", "S-012", "S-013", "S-014",
]


@pytest.mark.unit
class TestAdversaryGateCompleteness:
    """Verify the C4 adversarial quality gate report."""

    def test_adversary_report_exists(self) -> None:
        """The adversary C4 report exists and is non-empty."""
        assert _REPORT_PATH.exists(), f"Adversary report not found at {_REPORT_PATH}"
        content = _REPORT_PATH.read_text()
        assert len(content) > 200, "Adversary report is too short"

    def test_all_10_strategies_executed(self) -> None:
        """The report contains sections for all 10 required strategies."""
        content = _REPORT_PATH.read_text()
        missing = [s for s in _REQUIRED_STRATEGIES if s not in content]
        assert not missing, f"Missing strategies in report: {missing}"

    def test_composite_score_meets_threshold(self) -> None:
        """The report contains a composite score >= 0.95."""
        content = _REPORT_PATH.read_text()
        score_match = re.search(r"[Cc]omposite\s+[Ss]core[:\s]+(\d+\.\d+)", content)
        assert score_match is not None, "Composite Score not found in report"
        score = float(score_match.group(1))
        assert score >= 0.95, f"Composite score {score} < 0.95 threshold"

    def test_no_critical_high_unmitigated(self) -> None:
        """No finding has CRITICAL or HIGH severity with OPEN status."""
        content = _REPORT_PATH.read_text()
        lines = content.splitlines()
        for i, line in enumerate(lines):
            if ("CRITICAL" in line or "HIGH" in line) and "OPEN" in line:
                pytest.fail(
                    f"Unmitigated CRITICAL/HIGH finding at line {i + 1}: {line.strip()}"
                )
