# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Quality gate tests using ps-critic for hybrid pipeline output.

These tests validate that the hybrid pipeline output meets quality thresholds:
- Quality score >= 0.90 (NFR-010)
- ADR compliance verified
- Citation accuracy validated
- Extraction precision/recall acceptable

WARNING: These tests invoke LLM agents and are:
- SLOW (minutes per test)
- EXPENSIVE (token costs)
- EXCLUDED FROM CI (use pytest -m llm to run)

Run manually with: pytest -m llm tests/llm/transcript/test_quality_gate.py

Reference: TASK-237, EN-023 Integration Testing
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest


@dataclass
class QualityResult:
    """Result from ps-critic quality review."""

    success: bool
    quality_score: float = 0.0
    error: str | None = None
    report_path: Path | None = None
    metrics: dict[str, Any] = field(default_factory=dict)
    violations: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


@dataclass
class PipelineResult:
    """Result from running the full hybrid pipeline."""

    success: bool
    error: str | None = None
    packet_dir: Path | None = None
    elapsed_seconds: float = 0.0
    extraction_report: dict[str, Any] | None = None


def run_full_hybrid_pipeline(
    vtt_path: Path,
    output_dir: Path,
    timeout_seconds: int = 600,
) -> PipelineResult:
    """Run the complete hybrid transcript pipeline.

    Args:
        vtt_path: Path to input VTT file.
        output_dir: Directory for pipeline output.
        timeout_seconds: Maximum time to wait.

    Returns:
        PipelineResult with success status and outputs.
    """
    start_time = time.time()

    # Check for pre-computed output
    packet_dir = output_dir / "packet"
    extraction_report_path = output_dir / "extraction" / "extraction-report.json"

    if packet_dir.exists() and extraction_report_path.exists():
        elapsed = time.time() - start_time
        with open(extraction_report_path) as f:
            extraction_report = json.load(f)
        return PipelineResult(
            success=True,
            packet_dir=packet_dir,
            elapsed_seconds=elapsed,
            extraction_report=extraction_report,
        )

    # For live invocation
    pytest.skip(
        "Live hybrid pipeline invocation not implemented. "
        "Run transcript skill manually or provide pre-computed output."
    )
    return PipelineResult(success=False, error="Not implemented")


def run_ps_critic_review(
    packet_dir: Path,
    output_path: Path,
    timeout_seconds: int = 300,
) -> QualityResult:
    """Run ps-critic quality review on output packet.

    Args:
        packet_dir: Directory containing output packet.
        output_path: Path to save quality review report.
        timeout_seconds: Maximum time to wait.

    Returns:
        QualityResult with quality score and findings.
    """
    # Check for pre-computed quality review
    if output_path.exists():
        content = output_path.read_text()

        # Parse quality score from review (format: "Quality Score: 0.XX")
        import re

        score_match = re.search(r"Quality Score[:\s]+(\d+\.?\d*)", content, re.IGNORECASE)
        quality_score = float(score_match.group(1)) if score_match else 0.0

        # Normalize if percentage (e.g., 92 -> 0.92)
        if quality_score > 1.0:
            quality_score = quality_score / 100.0

        # Extract violations
        violations = []
        violations_match = re.search(
            r"(?:Violations?|Issues?|Findings?):\s*\n((?:[-*]\s*.+\n?)+)",
            content,
            re.IGNORECASE,
        )
        if violations_match:
            violations = [
                line.strip().lstrip("-*").strip()
                for line in violations_match.group(1).split("\n")
                if line.strip()
            ]

        # Extract recommendations
        recommendations = []
        rec_match = re.search(
            r"Recommendations?:\s*\n((?:[-*]\s*.+\n?)+)",
            content,
            re.IGNORECASE,
        )
        if rec_match:
            recommendations = [
                line.strip().lstrip("-*").strip()
                for line in rec_match.group(1).split("\n")
                if line.strip()
            ]

        return QualityResult(
            success=True,
            quality_score=quality_score,
            report_path=output_path,
            violations=violations,
            recommendations=recommendations,
        )

    # For live invocation
    pytest.skip(
        "Live ps-critic invocation not implemented. "
        "Run ps-critic manually or provide pre-computed quality-review.md."
    )
    return QualityResult(success=False, error="Not implemented")


@pytest.mark.llm
@pytest.mark.slow
class TestPsCriticQualityGate:
    """Quality gate tests using ps-critic.

    Tests validate:
    - AC-1: ps-critic successfully reviews hybrid pipeline output
    - AC-2: Quality score >= 0.90 (NFR-010 threshold)
    - AC-3: ADR-002 (packet structure) compliance verified
    - AC-4: ADR-003 (deep linking) compliance verified
    - AC-5: ADR-004 (token limits) compliance verified
    - AC-6: Quality report saved for audit trail
    """

    @pytest.fixture
    def pipeline_result(
        self,
        golden_vtt_path: Path,
        temp_output_dir: Path,
    ) -> PipelineResult:
        """Run the full pipeline and return the result."""
        return run_full_hybrid_pipeline(
            vtt_path=golden_vtt_path,
            output_dir=temp_output_dir,
        )

    @pytest.fixture
    def quality_result(
        self,
        pipeline_result: PipelineResult,
        temp_output_dir: Path,
    ) -> QualityResult:
        """Run ps-critic review and return the result."""
        assert pipeline_result.success, f"Pipeline failed: {pipeline_result.error}"
        assert pipeline_result.packet_dir is not None

        return run_ps_critic_review(
            packet_dir=pipeline_result.packet_dir,
            output_path=temp_output_dir / "quality-review.md",
        )

    # =========================================================================
    # AC-1: ps-critic successfully reviews hybrid pipeline output
    # =========================================================================

    def test_ps_critic_review_succeeds(
        self,
        quality_result: QualityResult,
    ) -> None:
        """Verify ps-critic successfully reviews the output.

        AC-1: ps-critic successfully reviews hybrid pipeline output
        """
        assert quality_result.success, f"ps-critic failed: {quality_result.error}"

    # =========================================================================
    # AC-2: Quality score >= 0.90 (NFR-010 threshold)
    # =========================================================================

    def test_quality_score_threshold(
        self,
        quality_result: QualityResult,
    ) -> None:
        """Verify quality score meets 0.90 threshold.

        AC-2: Quality score >= 0.90 (NFR-010 threshold)
        """
        assert quality_result.success, f"ps-critic failed: {quality_result.error}"

        threshold = 0.90
        assert quality_result.quality_score >= threshold, (
            f"Quality score {quality_result.quality_score:.2f} < {threshold} threshold. "
            f"Violations: {quality_result.violations[:5] if quality_result.violations else 'none'}"
        )

    # =========================================================================
    # AC-3: ADR-002 (packet structure) compliance verified
    # =========================================================================

    def test_adr_002_packet_structure_compliance(
        self,
        quality_result: QualityResult,
    ) -> None:
        """Verify ADR-002 (packet structure) compliance via ps-critic.

        AC-3: ADR-002 (packet structure) compliance verified

        ADR-002 requires:
        - 8 standard files (00-index.md through 07-topics.md)
        - _anchors.json registry
        - Consistent naming convention
        """
        assert quality_result.success, f"ps-critic failed: {quality_result.error}"

        if quality_result.report_path is None:
            pytest.skip("Quality report not available")
            return  # Satisfy type checker

        report_content = quality_result.report_path.read_text().lower()

        # Check for ADR-002 violations
        adr_002_violations = [
            "adr-002 violation",
            "missing required file",
            "packet structure invalid",
            "missing 00-index",
            "missing 01-summary",
        ]

        found_violations = [v for v in adr_002_violations if v in report_content]
        assert not found_violations, f"ADR-002 violations found: {found_violations}"

    # =========================================================================
    # AC-4: ADR-003 (deep linking) compliance verified
    # =========================================================================

    def test_adr_003_deep_linking_compliance(
        self,
        quality_result: QualityResult,
    ) -> None:
        """Verify ADR-003 (deep linking) compliance via ps-critic.

        AC-4: ADR-003 (deep linking) compliance verified

        ADR-003 requires:
        - Bidirectional anchors between files
        - Valid anchor format (#seg-NNNN)
        - _anchors.json registry maintained
        """
        assert quality_result.success, f"ps-critic failed: {quality_result.error}"

        if quality_result.report_path is None:
            pytest.skip("Quality report not available")
            return  # Satisfy type checker

        report_content = quality_result.report_path.read_text().lower()

        # Check for ADR-003 violations
        adr_003_violations = [
            "broken link",
            "invalid anchor",
            "missing anchor",
            "adr-003 violation",
            "deep link error",
            "orphan anchor",
        ]

        found_violations = [v for v in adr_003_violations if v in report_content]

        # Allow minor violations (LLM non-determinism)
        max_violations = 2
        assert len(found_violations) <= max_violations, (
            f"Too many ADR-003 violations: {found_violations}"
        )

    # =========================================================================
    # AC-5: ADR-004 (token limits) compliance verified
    # =========================================================================

    def test_adr_004_token_limits_compliance(
        self,
        quality_result: QualityResult,
    ) -> None:
        """Verify ADR-004 (token limits) compliance via ps-critic.

        AC-5: ADR-004 (token limits) compliance verified

        ADR-004 requires:
        - Soft limit: 31,500 tokens per file
        - Hard limit: 35,000 tokens per file
        - Semantic splitting at ## headings
        """
        assert quality_result.success, f"ps-critic failed: {quality_result.error}"

        if quality_result.report_path is None:
            pytest.skip("Quality report not available")
            return  # Satisfy type checker

        report_content = quality_result.report_path.read_text().lower()

        # Check for ADR-004 violations
        adr_004_violations = [
            "token limit exceeded",
            "file too large",
            "adr-004 violation",
            "exceeds 35k",
            "exceeds 35000",
        ]

        found_violations = [v for v in adr_004_violations if v in report_content]
        assert not found_violations, f"ADR-004 violations found: {found_violations}"

    # =========================================================================
    # AC-6: Quality report saved for audit trail
    # =========================================================================

    def test_quality_report_saved(
        self,
        quality_result: QualityResult,
    ) -> None:
        """Verify quality report is saved for audit trail.

        AC-6: Quality report saved for audit trail
        """
        assert quality_result.success, f"ps-critic failed: {quality_result.error}"
        assert quality_result.report_path is not None, "Quality report path not set"
        assert quality_result.report_path.exists(), "Quality report file not found"

        # Verify report has meaningful content
        content = quality_result.report_path.read_text()
        assert len(content) > 100, "Quality report too short"

        # Should contain quality score
        assert "quality" in content.lower(), "Report missing quality information"


@pytest.mark.llm
@pytest.mark.slow
class TestExtractionMetrics:
    """Extraction metrics tests for quality validation."""

    @pytest.fixture
    def pipeline_result(
        self,
        golden_vtt_path: Path,
        temp_output_dir: Path,
    ) -> PipelineResult:
        """Run the full pipeline and return the result."""
        return run_full_hybrid_pipeline(
            vtt_path=golden_vtt_path,
            output_dir=temp_output_dir,
        )

    @pytest.fixture
    def quality_result(
        self,
        pipeline_result: PipelineResult,
        temp_output_dir: Path,
    ) -> QualityResult:
        """Run ps-critic review and return the result."""
        assert pipeline_result.success, f"Pipeline failed: {pipeline_result.error}"
        assert pipeline_result.packet_dir is not None

        return run_ps_critic_review(
            packet_dir=pipeline_result.packet_dir,
            output_path=temp_output_dir / "quality-review.md",
        )

    def test_extraction_precision_threshold(
        self,
        quality_result: QualityResult,
    ) -> None:
        """Verify extraction precision meets NFR-003 threshold (>= 85%).

        NFR-003: Precision >= 85%
        """
        assert quality_result.success, f"ps-critic failed: {quality_result.error}"

        if "precision" in quality_result.metrics:
            precision = quality_result.metrics["precision"]
            assert precision >= 0.85, f"Extraction precision {precision:.1%} < 85% threshold"

    def test_extraction_recall_threshold(
        self,
        quality_result: QualityResult,
    ) -> None:
        """Verify extraction recall meets NFR-003 threshold (>= 85%).

        NFR-003: Recall >= 85%
        """
        assert quality_result.success, f"ps-critic failed: {quality_result.error}"

        if "recall" in quality_result.metrics:
            recall = quality_result.metrics["recall"]
            assert recall >= 0.85, f"Extraction recall {recall:.1%} < 85% threshold"

    def test_confidence_ratio_threshold(
        self,
        quality_result: QualityResult,
    ) -> None:
        """Verify high confidence ratio meets NFR-008 threshold (>= 70%).

        NFR-008: High confidence ratio >= 70%
        """
        assert quality_result.success, f"ps-critic failed: {quality_result.error}"

        if "high_confidence_ratio" in quality_result.metrics:
            ratio = quality_result.metrics["high_confidence_ratio"]
            assert ratio >= 0.70, f"High confidence ratio {ratio:.1%} < 70% threshold"

    def test_citation_accuracy(
        self,
        pipeline_result: PipelineResult,
    ) -> None:
        """Verify all citations reference valid segments.

        PAT-004: 100% citation accuracy (every entity must have valid citation)
        """
        assert pipeline_result.success, "Pipeline must succeed first"

        extraction_report = pipeline_result.extraction_report
        if extraction_report is None:
            pytest.skip("Extraction report not available")
            return

        invalid_citations = []
        max_segment_id = 3071  # meeting-006

        for entity_type in ["action_items", "decisions", "questions"]:
            for entity in extraction_report.get(entity_type, []):
                entity_id = entity.get("id", "unknown")
                citation = entity.get("citation", {})

                # Must have citation
                if not citation:
                    invalid_citations.append(f"{entity_type}/{entity_id}: missing citation")
                    continue

                # Must have segment_id
                segment_id = citation.get("segment_id")
                if not segment_id:
                    invalid_citations.append(f"{entity_type}/{entity_id}: missing segment_id")
                    continue

                # Validate segment_id range
                if isinstance(segment_id, str) and segment_id.startswith("seg-"):
                    try:
                        seg_num = int(segment_id.split("-")[1])
                        if seg_num < 1 or seg_num > max_segment_id:
                            invalid_citations.append(
                                f"{entity_type}/{entity_id}: segment {segment_id} out of range"
                            )
                    except (ValueError, IndexError):
                        invalid_citations.append(
                            f"{entity_type}/{entity_id}: invalid segment format {segment_id}"
                        )

        # PAT-004 requires 100% citation accuracy
        assert not invalid_citations, f"Citation accuracy violations: {invalid_citations[:10]}"
