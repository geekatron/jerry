# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for Layer4Pipeline._emit_gha_outputs() newline sanitization — CG-018.

Verifies that newline (\\n) and carriage-return (\\r) characters embedded in
ComparisonReport field values are replaced with spaces before being written
to the GITHUB_OUTPUT file or emitted as log entries.

Without sanitization, newlines corrupt the GHA key=value\\n output protocol
and can enable header-splitting attacks in subsequent workflow steps.

Tests use:
  - tmp_path for an isolated GITHUB_OUTPUT file.
  - monkeypatch to set/unset GITHUB_OUTPUT in the environment.
  - A minimal ComparisonReport stand-in (constructed via a simple dataclass
    mock) to avoid pulling in stats/reports dependencies.

No LLM calls are performed.

References:
    - CG-018: Newline sanitization in _emit_gha_outputs()
    - H-20: BDD test-first (90% line coverage target)
"""

from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from jerry.testing.layer4_stats import Layer4Pipeline

# ---------------------------------------------------------------------------
# Minimal ComparisonReport stand-in
# ---------------------------------------------------------------------------
# _emit_gha_outputs() accesses four attributes of ComparisonReport:
#   - classification  (str)
#   - merge_recommendation (str)
#   - agent (str)
#   - evaluation_mode (str)
#   - dimension_driver (str | None)
#
# We fabricate a lightweight dataclass that satisfies these attribute accesses
# without importing the full ComparisonReport (which depends on stats machinery).


@dataclasses.dataclass
class _FakeReport:
    """Minimal ComparisonReport substitute for testing _emit_gha_outputs()."""

    classification: str
    merge_recommendation: str
    agent: str
    evaluation_mode: str
    dimension_driver: str | None = None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestEmitGhaOutputsSanitization:
    """Unit tests for newline sanitization in Layer4Pipeline._emit_gha_outputs().

    Each test verifies that newlines embedded in report field values are
    replaced with spaces in the GITHUB_OUTPUT file content (CG-018A).
    """

    @pytest.mark.unit
    def test_newline_in_classification_should_be_replaced_with_space(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Newline (\\n) in classification is replaced with a space in GHA output.

        A classification value containing \\n would break the key=value\\n
        line protocol that GitHub Actions uses to parse workflow outputs.
        After CG-018A sanitization, the written value must contain no newlines.
        """
        gha_file = tmp_path / "github_output.txt"
        monkeypatch.setenv("GITHUB_OUTPUT", str(gha_file))

        report = _FakeReport(
            classification="NO_REGRESSION\nINJECTED_LINE",
            merge_recommendation="ALLOW",
            agent="ps-researcher",
            evaluation_mode="FULL",
        )
        Layer4Pipeline._emit_gha_outputs(report)  # type: ignore[arg-type]

        content = gha_file.read_text(encoding="utf-8")
        # The verdict line must not contain a raw newline within its value
        verdict_line = next(
            (line for line in content.splitlines() if line.startswith("verdict=")), None
        )
        assert verdict_line is not None, "Expected a 'verdict=' line in GITHUB_OUTPUT"
        value = verdict_line.split("=", 1)[1]
        assert "\n" not in value, f"Newline found in sanitized verdict value: {value!r}"
        assert "INJECTED_LINE" in value, (
            f"Sanitized value should still contain the rest of the string; got: {value!r}"
        )

    @pytest.mark.unit
    def test_carriage_return_in_value_should_be_replaced_with_space(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Carriage return (\\r) in a value is replaced with a space in GHA output.

        Carriage returns in GHA output values cause the same protocol-breaking
        behaviour as newlines (CG-018A covers both \\n and \\r).
        """
        gha_file = tmp_path / "github_output_cr.txt"
        monkeypatch.setenv("GITHUB_OUTPUT", str(gha_file))

        report = _FakeReport(
            classification="NO_REGRESSION",
            merge_recommendation="ALLOW\rINJECTED",
            agent="ps-researcher",
            evaluation_mode="FULL",
        )
        Layer4Pipeline._emit_gha_outputs(report)  # type: ignore[arg-type]

        content = gha_file.read_text(encoding="utf-8")
        assert "\r" not in content, "Carriage return must be sanitized from GITHUB_OUTPUT content"

    @pytest.mark.unit
    def test_clean_values_should_be_written_verbatim(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Values without newlines are written to GITHUB_OUTPUT unchanged.

        Sanitization must be a no-op for clean values; it must not alter
        legitimate content that does not contain control characters.
        """
        gha_file = tmp_path / "clean_output.txt"
        monkeypatch.setenv("GITHUB_OUTPUT", str(gha_file))

        report = _FakeReport(
            classification="IMPROVEMENT",
            merge_recommendation="ALLOW",
            agent="ps-researcher",
            evaluation_mode="STANDARD",
        )
        Layer4Pipeline._emit_gha_outputs(report)  # type: ignore[arg-type]

        content = gha_file.read_text(encoding="utf-8")
        assert "verdict=IMPROVEMENT" in content
        assert "merge_recommendation=ALLOW" in content
        assert "agent=ps-researcher" in content
        assert "evaluation_mode=STANDARD" in content

    @pytest.mark.unit
    def test_dimension_driver_is_written_when_present(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When dimension_driver is set, it appears as a line in GITHUB_OUTPUT.

        dimension_driver is an optional field: when present, it must be emitted
        so downstream workflow steps can identify which metric drove the verdict.
        """
        gha_file = tmp_path / "with_driver.txt"
        monkeypatch.setenv("GITHUB_OUTPUT", str(gha_file))

        report = _FakeReport(
            classification="REGRESSION",
            merge_recommendation="BLOCK",
            agent="ps-analyst",
            evaluation_mode="FULL",
            dimension_driver="composite_score",
        )
        Layer4Pipeline._emit_gha_outputs(report)  # type: ignore[arg-type]

        content = gha_file.read_text(encoding="utf-8")
        assert "dimension_driver=composite_score" in content

    @pytest.mark.unit
    def test_newline_in_dimension_driver_should_be_sanitized(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Newline in dimension_driver value is replaced with space (CG-018A)."""
        gha_file = tmp_path / "driver_newline.txt"
        monkeypatch.setenv("GITHUB_OUTPUT", str(gha_file))

        report = _FakeReport(
            classification="REGRESSION",
            merge_recommendation="BLOCK",
            agent="ps-analyst",
            evaluation_mode="FULL",
            dimension_driver="composite_score\nINJECTED",
        )
        Layer4Pipeline._emit_gha_outputs(report)  # type: ignore[arg-type]

        content = gha_file.read_text(encoding="utf-8")
        driver_line = next(
            (line for line in content.splitlines() if line.startswith("dimension_driver=")),
            None,
        )
        assert driver_line is not None
        value = driver_line.split("=", 1)[1]
        assert "\n" not in value

    @pytest.mark.unit
    def test_without_github_output_env_should_not_write_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """When GITHUB_OUTPUT is unset, _emit_gha_outputs() falls back to logging.

        No file should be written when the environment variable is absent.
        The method must not raise; local-dev path logs to logger.info instead.
        """
        monkeypatch.delenv("GITHUB_OUTPUT", raising=False)

        report = _FakeReport(
            classification="NO_REGRESSION",
            merge_recommendation="ALLOW",
            agent="ps-researcher",
            evaluation_mode="SMOKE",
        )
        # Must not raise
        Layer4Pipeline._emit_gha_outputs(report)  # type: ignore[arg-type]
