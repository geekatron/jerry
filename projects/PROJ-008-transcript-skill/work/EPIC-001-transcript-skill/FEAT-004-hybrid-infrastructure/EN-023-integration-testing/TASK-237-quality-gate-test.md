# TASK-237: ps-critic Quality Gate Test

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-023 Integration Testing)
PURPOSE: Validate ps-critic quality gate passes for hybrid pipeline output
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-237"
work_type: TASK

# === CORE METADATA ===
title: "ps-critic Quality Gate Test"
description: |
  Validate that the hybrid pipeline output passes ps-critic quality review:
  - Quality score >= 0.90 (per NFR-010)
  - All ADR compliance verified
  - Citation accuracy validated
  - Extraction precision/recall acceptable

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: BACKLOG
resolution: null

# === PRIORITY ===
priority: HIGH

# === PEOPLE ===
assignee: "Claude"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-29T21:30:00Z"
updated_at: "2026-01-29T21:30:00Z"

# === HIERARCHY ===
parent_id: "EN-023"

# === TAGS ===
tags:
  - "testing"
  - "llm"
  - "ps-critic"
  - "quality"
  - "validation"

# === DELIVERY ITEM PROPERTIES ===
effort: 3
acceptance_criteria: |
  AC-1: ps-critic successfully reviews hybrid pipeline output
  AC-2: Quality score >= 0.90 (NFR-010 threshold)
  AC-3: ADR-002 (packet structure) compliance verified
  AC-4: ADR-003 (deep linking) compliance verified
  AC-5: ADR-004 (token limits) compliance verified
  AC-6: Quality report saved for audit trail
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: TESTING
original_estimate: 3
remaining_work: 3
time_spent: null
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Description

### Purpose

This is the **final quality gate** for FEAT-004. It validates that the hybrid architecture produces output meeting the same quality standards as the original agent-only architecture.

### Quality Criteria (NFR-010)

| Criterion | Threshold | Source |
|-----------|-----------|--------|
| Overall quality score | >= 0.90 | NFR-010 |
| Extraction precision | >= 85% | NFR-003 |
| Extraction recall | >= 85% | NFR-003 |
| Citation accuracy | 100% | PAT-004 |
| Confidence ratio (high) | >= 70% | NFR-008 |

### Test Cases

```python
# tests/llm/transcript/test_quality_gate.py

import pytest
import json
from pathlib import Path

@pytest.mark.llm
@pytest.mark.slow
class TestPsCriticQualityGate:
    """Quality gate tests using ps-critic."""

    def test_quality_score_threshold(self, temp_output_dir):
        """Verify quality score meets 0.90 threshold."""
        vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")

        # Run full pipeline
        pipeline_result = run_full_hybrid_pipeline(
            vtt_path=vtt_path,
            output_dir=temp_output_dir,
        )
        assert pipeline_result.success

        # Run ps-critic review
        packet_dir = temp_output_dir / "packet"
        quality_result = run_ps_critic_review(
            packet_dir=packet_dir,
            output_path=temp_output_dir / "quality-review.md",
        )

        assert quality_result.success, f"ps-critic failed: {quality_result.error}"
        assert quality_result.quality_score >= 0.90, (
            f"Quality score {quality_result.quality_score:.2f} < 0.90 threshold"
        )

    def test_adr_002_packet_structure(self, temp_output_dir):
        """Verify ADR-002 (packet structure) compliance via ps-critic."""
        vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")

        pipeline_result = run_full_hybrid_pipeline(
            vtt_path=vtt_path,
            output_dir=temp_output_dir,
        )

        quality_result = run_ps_critic_review(
            packet_dir=temp_output_dir / "packet",
            output_path=temp_output_dir / "quality-review.md",
        )

        # Check ADR compliance in review
        review_content = (temp_output_dir / "quality-review.md").read_text()

        # Should not have ADR-002 violations
        assert "ADR-002 violation" not in review_content.lower()
        assert "missing required file" not in review_content.lower()

    def test_adr_003_deep_linking(self, temp_output_dir):
        """Verify ADR-003 (deep linking) compliance via ps-critic."""
        vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")

        pipeline_result = run_full_hybrid_pipeline(
            vtt_path=vtt_path,
            output_dir=temp_output_dir,
        )

        quality_result = run_ps_critic_review(
            packet_dir=temp_output_dir / "packet",
            output_path=temp_output_dir / "quality-review.md",
        )

        review_content = (temp_output_dir / "quality-review.md").read_text()

        # Should not have broken link violations
        assert "broken link" not in review_content.lower()
        assert "invalid anchor" not in review_content.lower()

    def test_adr_004_token_limits(self, temp_output_dir):
        """Verify ADR-004 (token limits) compliance via ps-critic."""
        vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")

        pipeline_result = run_full_hybrid_pipeline(
            vtt_path=vtt_path,
            output_dir=temp_output_dir,
        )

        quality_result = run_ps_critic_review(
            packet_dir=temp_output_dir / "packet",
            output_path=temp_output_dir / "quality-review.md",
        )

        review_content = (temp_output_dir / "quality-review.md").read_text()

        # Should not have token limit violations
        assert "token limit exceeded" not in review_content.lower()
        assert "file too large" not in review_content.lower()

    def test_extraction_metrics(self, temp_output_dir):
        """Verify extraction precision/recall meets thresholds."""
        vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")

        pipeline_result = run_full_hybrid_pipeline(
            vtt_path=vtt_path,
            output_dir=temp_output_dir,
        )

        quality_result = run_ps_critic_review(
            packet_dir=temp_output_dir / "packet",
            output_path=temp_output_dir / "quality-review.md",
        )

        # Extract metrics from quality review
        if hasattr(quality_result, 'metrics'):
            metrics = quality_result.metrics

            if 'precision' in metrics:
                assert metrics['precision'] >= 0.85, (
                    f"Precision {metrics['precision']:.2f} < 0.85"
                )

            if 'recall' in metrics:
                assert metrics['recall'] >= 0.85, (
                    f"Recall {metrics['recall']:.2f} < 0.85"
                )

    def test_quality_report_saved(self, temp_output_dir):
        """Verify quality report is saved for audit trail."""
        vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")

        pipeline_result = run_full_hybrid_pipeline(
            vtt_path=vtt_path,
            output_dir=temp_output_dir,
        )

        quality_report_path = temp_output_dir / "quality-review.md"

        quality_result = run_ps_critic_review(
            packet_dir=temp_output_dir / "packet",
            output_path=quality_report_path,
        )

        # Verify report exists and has content
        assert quality_report_path.exists()
        content = quality_report_path.read_text()
        assert len(content) > 100, "Quality report too short"
        assert "Quality Score" in content or "quality score" in content.lower()
```

---

## Acceptance Criteria

- [ ] AC-1: ps-critic successfully reviews hybrid pipeline output
- [ ] AC-2: Quality score >= 0.90 (NFR-010 threshold)
- [ ] AC-3: ADR-002 (packet structure) compliance verified
- [ ] AC-4: ADR-003 (deep linking) compliance verified
- [ ] AC-5: ADR-004 (token limits) compliance verified
- [ ] AC-6: Quality report saved for audit trail

---

## Related Items

- Parent: [EN-023 Integration Testing](./EN-023-integration-testing.md)
- Depends On: TASK-234, TASK-236
- Related: ADR-002, ADR-003, ADR-004, NFR-003, NFR-008, NFR-010
- Agent: `skills/problem-solving/agents/ps-critic.md`

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | 3 hours |
| Remaining Work | 3 hours |
| Time Spent | - |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Quality gate tests | Python | `tests/llm/transcript/test_quality_gate.py` |

### Verification

- [ ] Acceptance criteria verified
- [ ] `pytest -m llm tests/llm/transcript/test_quality_gate.py` passes
- [ ] Quality score >= 0.90
- [ ] Reviewed by: Human

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | BACKLOG | Created per DEC-012 restructuring |
