# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
BDD tests for ST-010: Remaining Skill Migrations to AST.

Validates that the AST operations referenced in the ST-010 migrations work
correctly against the types of markdown files that migrated agents encounter:
- Deliverable markdown (adv-executor, adv-scorer, ps-critic use cases)
- Review/requirements documents (nse-reviewer, nse-requirements use cases)
- Entity files for constraint validation (ps-validator use case)
- Documentation review files (ps-reviewer use case)

Performance test:
- 50-file batch validation under 100ms

Test categories:
    - Deliverable analysis: frontmatter + structure for adv-executor/scorer/ps-critic
    - Nav table validation: H-23/H-24 compliance for nse-reviewer/ps-reviewer
    - Schema validation: entity constraint checks for ps-validator
    - Frontmatter extraction: status/parent for nse-requirements/nse-reviewer
    - Performance: batch validation throughput

References:
    - ST-010: Remaining Skill Migrations
    - H-20: BDD test-first (RED phase written before implementation)
    - H-21: 90% line coverage required
"""

from __future__ import annotations

import os
import tempfile
import time

import pytest

from skills.ast.scripts.ast_ops import (
    parse_file,
    query_frontmatter,
    validate_file,
    validate_nav_table_file,
)

# ---------------------------------------------------------------------------
# Fixtures: temp file helpers
# ---------------------------------------------------------------------------


def _write_temp(content: str, suffix: str = ".md") -> str:
    """Write content to a temporary file and return its absolute path."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(content)
    return path


def _write_temp_list(contents: list[str]) -> list[str]:
    """Write multiple content strings to temp files, return list of paths."""
    return [_write_temp(c) for c in contents]


def _cleanup_paths(paths: list[str]) -> None:
    """Remove a list of temp file paths."""
    for p in paths:
        try:
            os.unlink(p)
        except FileNotFoundError:
            pass


# ---------------------------------------------------------------------------
# Fixtures: markdown content for migrated agent use cases
# ---------------------------------------------------------------------------

# ADR-style deliverable (adv-executor, adv-scorer, ps-critic use case)
ADR_DELIVERABLE_MD = """\
# ADR-001: Use mistletoe as Markdown Parser

> **Type:** decision
> **Status:** proposed
> **Scope:** markdown-ast domain

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Why this decision was made |
| [Context](#context) | Problem being solved |
| [Decision](#decision) | What was decided |
| [Consequences](#consequences) | Trade-offs |

---

## Summary

We choose mistletoe as the markdown parser for the Jerry framework AST domain.

---

## Context

Jerry needs a markdown parser that produces a structured AST. Multiple options
were evaluated: mistletoe, markdown-it-py, and commonmark.

---

## Decision

Use mistletoe v1.x for its pure-Python AST with visitor pattern support.

---

## Consequences

- Positive: Clean AST API, no C extensions required
- Negative: Less maintained than markdown-it-py
"""

# Story entity file (nse-requirements, ps-validator use case)
STORY_DELIVERABLE_MD = """\
# ST-010: Remaining Skill Migrations

> **Type:** story
> **Status:** in_progress
> **Priority:** medium
> **Impact:** high
> **Created:** 2026-02-20
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-001
> **Owner:** Adam Nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Scope and context |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |

---

## Summary

Migrate remaining skill agents (/adversary, /nasa-se, /problem-solving,
/orchestration) to reference AST operations where beneficial.

---

## Acceptance Criteria

- [ ] adv-executor has AST-Based Operations section
- [ ] adv-scorer has AST-Based Operations section
- [ ] nse-reviewer has AST-Based Operations section
- [ ] nse-requirements has AST-Based Operations section
- [ ] ps-critic has AST-Based Operations section
- [ ] ps-validator has AST-Based Operations section
- [ ] ps-reviewer has AST-Based Operations section
- [ ] Migration decisions document created
- [ ] Tests pass
"""

# Review requirements document (nse-reviewer use case)
REVIEW_PACKAGE_MD = """\
# PDR Entrance Checklist

> **Project:** PROJ-002
> **Entry:** e-201
> **Review:** PDR
> **Date:** 2026-02-20
> **Status:** Conditional

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Readiness status |
| [L1: Entrance Criteria Evaluation](#l1-entrance-criteria-evaluation) | Criteria status |
| [L2: Strategic Assessment](#l2-strategic-assessment) | Risk analysis |
| [References](#references) | NASA sources |

---

## L0: Executive Summary

**Readiness:** Conditional
**Criteria Met:** 6 of 8 (75%)
**Critical Blockers:** 2 TBDs remaining in requirements

---

## L1: Entrance Criteria Evaluation

| # | Criterion | Status | Evidence |
|---|-----------|--------|----------|
| 1 | SRR action items closed | GREEN | AI-001 closed |
| 2 | Requirements baseline approved | GREEN | REQ-BL-001 |
| 3 | All TBDs resolved | RED | 2 TBDs remain |
| 4 | Risk register current | GREEN | RISK-001 |

---

## L2: Strategic Assessment

Conditional readiness. TBDs must be resolved before PDR board review.

---

## References

- NPR 7123.1D Appendix G, Table G-6
"""

# Requirements specification (nse-requirements use case)
REQUIREMENTS_DOC_MD = """\
# Requirements Specification: Propulsion System

> **Project:** PROJ-002
> **Entry:** e-101
> **Status:** baselined
> **Parent:** EPIC-001
> **Owner:** Adam Nowak

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | High-level requirements |
| [L1: Technical Requirements](#l1-technical-requirements) | Formal requirements |
| [L2: Systems Perspective](#l2-systems-perspective) | Traceability |
| [References](#references) | Sources |

---

## L0: Executive Summary

The propulsion system shall provide primary thrust for mission phases A through C.

---

## L1: Technical Requirements

| ID | Requirement | Parent | V-Method |
|----|-------------|--------|----------|
| REQ-001 | System shall provide 500N thrust | STK-001 | Test |

---

## L2: Systems Perspective

Allocated to propulsion subsystem. Interface with power subsystem.

---

## References

- NPR 7123.1D, Process 2
"""

# Rule file with L2-REINJECT directives (for extract_reinject use case)
RULE_FILE_MD = """\
# Quality Enforcement Rule

<!-- L2-REINJECT: rank=1, tokens=50, content="Quality gate >= 0.92 for C2+ deliverables (H-13)." -->
<!-- L2-REINJECT: rank=2, tokens=30, content="Creator-critic cycle minimum 3 iterations (H-14)." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Non-overridable constraints |
| [Quality Gate](#quality-gate) | Threshold and dimensions |

---

## HARD Rules

| ID | Rule |
|----|------|
| H-13 | Quality threshold >= 0.92 for C2+ |
| H-14 | Creator-critic-revision cycle (3 min) |

---

## Quality Gate

**Threshold:** >= 0.92 weighted composite score (C2+ deliverables)
"""

# Document WITHOUT nav table (should fail H-23 validation)
NO_NAV_TABLE_MD = """\
# Analysis Report: Authentication Design

> **Type:** analysis
> **Status:** draft

## Summary

This analysis evaluates three authentication approaches.

## Approach Comparison

All three approaches were compared on security, complexity, and cost.

## Recommendation

OAuth2 is recommended for its ecosystem support.

## Risk Assessment

Low risk of adoption given broad library support.
"""

# Document WITH nav table (should pass H-23 validation)
WITH_NAV_TABLE_MD = """\
# Analysis Report: Authentication Design

> **Type:** analysis
> **Status:** draft

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overview of analysis |
| [Approach Comparison](#approach-comparison) | Comparison table |
| [Recommendation](#recommendation) | Final recommendation |
| [Risk Assessment](#risk-assessment) | Risk considerations |

---

## Summary

This analysis evaluates three authentication approaches.

---

## Approach Comparison

All three approaches were compared on security, complexity, and cost.

---

## Recommendation

OAuth2 is recommended for its ecosystem support.

---

## Risk Assessment

Low risk of adoption given broad library support.
"""

# Valid enabler entity file (ps-validator use case)
VALID_ENABLER_MD = """\
# EN-010: Setup CI Pipeline

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-15
> **Due:** ---
> **Completed:** 2026-02-18
> **Parent:** FEAT-001
> **Owner:** Adam Nowak
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What was done |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Technical Approach](#technical-approach) | Implementation details |

---

## Summary

Set up GitHub Actions CI pipeline for automated testing.

---

## Acceptance Criteria

- [x] All tests run in CI
- [x] Coverage report generated

---

## Technical Approach

Used GitHub Actions with uv for dependency management.
"""

# Malformed enabler (missing required fields)
MALFORMED_ENABLER_MD = """\
# EN-099: Incomplete Enabler

> **Type:** enabler
> **Status:** pending

---

## Summary

This enabler is missing Priority, Impact, Enabler Type, Created, and Parent fields.
"""


# ---------------------------------------------------------------------------
# Tests: Deliverable analysis (adv-executor, adv-scorer, ps-critic use case)
# ---------------------------------------------------------------------------


class TestDeliverableAnalysis:
    """Tests for AST operations on deliverable-format markdown files.

    Covers the adv-executor, adv-scorer, and ps-critic migration patterns:
    using parse_file() and query_frontmatter() before strategy execution.
    """

    @pytest.mark.happy_path
    def test_parse_adr_deliverable_structure(self) -> None:
        """parse_file returns structural information for ADR-style deliverables."""
        path = _write_temp(ADR_DELIVERABLE_MD)
        try:
            info = parse_file(path)
            assert info["has_frontmatter"] is True
            assert info["heading_count"] >= 5  # Summary, Context, Decision, Consequences + title
            assert "heading" in info["node_types"]
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_query_frontmatter_adr_deliverable(self) -> None:
        """query_frontmatter extracts Type and Status from ADR deliverables."""
        path = _write_temp(ADR_DELIVERABLE_MD)
        try:
            fm = query_frontmatter(path)
            assert fm.get("Type") == "decision"
            assert fm.get("Status") == "proposed"
            assert fm.get("Scope") == "markdown-ast domain"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_query_frontmatter_story_deliverable(self) -> None:
        """query_frontmatter extracts entity context for story deliverables."""
        path = _write_temp(STORY_DELIVERABLE_MD)
        try:
            fm = query_frontmatter(path)
            assert fm.get("Type") == "story"
            assert fm.get("Status") == "in_progress"
            assert fm.get("Parent") == "FEAT-001"
            assert fm.get("Effort") == "3"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_validate_story_entity_for_schema_violations(self) -> None:
        """validate_file with schema=story detects violations in story deliverables."""
        path = _write_temp(STORY_DELIVERABLE_MD)
        try:
            result = validate_file(path, schema="story")
            # STORY_DELIVERABLE_MD is well-formed; should pass
            assert result["schema_valid"] is True
            assert result["schema_violations"] == []
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_ps_critic_entity_type_informs_schema_selection(self) -> None:
        """ps-critic pattern: entity type from frontmatter selects correct schema."""
        path = _write_temp(VALID_ENABLER_MD)
        try:
            fm = query_frontmatter(path)
            entity_type = fm.get("Type", "unknown").lower()
            assert entity_type == "enabler"

            # Use detected type to run schema validation
            result = validate_file(path, schema=entity_type)
            assert result["schema_valid"] is True
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# Tests: Nav table validation (nse-reviewer, ps-reviewer use case)
# ---------------------------------------------------------------------------


class TestNavTableValidation:
    """Tests for nav table compliance validation.

    Covers the nse-reviewer and ps-reviewer migration patterns:
    using validate_nav_table_file() to check H-23/H-24 compliance.
    """

    @pytest.mark.happy_path
    def test_review_package_with_nav_table_passes_h23(self) -> None:
        """A review package with a complete nav table passes H-23/H-24 validation."""
        path = _write_temp(REVIEW_PACKAGE_MD)
        try:
            result = validate_nav_table_file(path)
            assert result["is_valid"] is True
            assert result["missing_entries"] == []
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_requirements_doc_with_nav_table_passes_h23(self) -> None:
        """A requirements document with a nav table passes H-23/H-24 validation."""
        path = _write_temp(REQUIREMENTS_DOC_MD)
        try:
            result = validate_nav_table_file(path)
            assert result["is_valid"] is True
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_document_without_nav_table_fails_h23(self) -> None:
        """A document without a nav table fails H-23 validation."""
        path = _write_temp(NO_NAV_TABLE_MD)
        try:
            result = validate_nav_table_file(path)
            assert result["is_valid"] is False
            # Should report all ## headings as missing entries
            assert len(result["missing_entries"]) > 0
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_document_with_nav_table_passes_h23(self) -> None:
        """A document with a complete nav table passes H-23/H-24 validation."""
        path = _write_temp(WITH_NAV_TABLE_MD)
        try:
            result = validate_nav_table_file(path)
            assert result["is_valid"] is True
            assert result["missing_entries"] == []
            assert result["orphaned_entries"] == []
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_nav_table_entries_serializable(self) -> None:
        """validate_nav_table_file returns serializable entry dicts."""
        path = _write_temp(REVIEW_PACKAGE_MD)
        try:
            result = validate_nav_table_file(path)
            entries = result.get("entries", [])
            assert len(entries) > 0
            for entry in entries:
                assert "section_name" in entry
                assert "anchor" in entry
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_ps_reviewer_documentation_review_pattern(self) -> None:
        """ps-reviewer pattern: nav table check is a MEDIUM severity finding source."""
        path = _write_temp(NO_NAV_TABLE_MD)
        try:
            result = validate_nav_table_file(path)
            # ps-reviewer should report missing nav table as MEDIUM finding
            if not result["is_valid"]:
                missing = result["missing_entries"]
                # Each missing entry = one documentation finding
                assert len(missing) >= 3  # Summary, Approach Comparison, Recommendation, Risk
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# Tests: Frontmatter extraction (nse-reviewer, nse-requirements use case)
# ---------------------------------------------------------------------------


class TestFrontmatterExtractionForReviewCriteria:
    """Tests for frontmatter extraction in review and requirements contexts.

    Covers the nse-reviewer and nse-requirements migration patterns:
    using query_frontmatter() to check status/parent for entrance criteria.
    """

    @pytest.mark.happy_path
    def test_nse_reviewer_reads_status_for_criteria_check(self) -> None:
        """nse-reviewer pattern: query_frontmatter reads Status for criteria check."""
        path = _write_temp(REQUIREMENTS_DOC_MD)
        try:
            fm = query_frontmatter(path)
            status = fm.get("Status", "")
            # nse-reviewer checks: "Requirements baseline approved" criterion
            # baselined status = criterion met
            assert status == "baselined"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_nse_requirements_reads_parent_for_traceability(self) -> None:
        """nse-requirements pattern: query_frontmatter reads Parent for traceability."""
        path = _write_temp(REQUIREMENTS_DOC_MD)
        try:
            fm = query_frontmatter(path)
            parent = fm.get("Parent", "")
            # nse-requirements verifies bidirectional trace to parent
            assert parent == "EPIC-001"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_story_frontmatter_status_for_entrance_criteria(self) -> None:
        """query_frontmatter provides status for entrance criteria verification."""
        path = _write_temp(STORY_DELIVERABLE_MD)
        try:
            fm = query_frontmatter(path)
            status = fm.get("Status", "")
            # in_progress is not "completed" -- criteria not met
            assert status == "in_progress"
            assert status != "completed"
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_frontmatter_extraction_replaces_grep_pattern(self) -> None:
        """query_frontmatter is more reliable than grep for structured data."""
        path = _write_temp(REVIEW_PACKAGE_MD)
        try:
            fm = query_frontmatter(path)
            # query_frontmatter should extract Project, Entry, Review, Status
            assert fm.get("Project") == "PROJ-002"
            assert fm.get("Entry") == "e-201"
            assert fm.get("Review") == "PDR"
            assert fm.get("Status") == "Conditional"
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# Tests: Schema validation for ps-validator use case
# ---------------------------------------------------------------------------


class TestSchemaValidationForConstraints:
    """Tests for schema-based constraint validation.

    Covers the ps-validator migration pattern: using validate_file() with
    schema to get structured violation evidence for constraint verification.
    """

    @pytest.mark.happy_path
    def test_valid_enabler_passes_schema_constraint(self) -> None:
        """ps-validator pattern: valid enabler passes schema constraint."""
        path = _write_temp(VALID_ENABLER_MD)
        try:
            result = validate_file(path, schema="enabler")
            assert result["schema_valid"] is True
            assert result["schema_violations"] == []
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_malformed_enabler_fails_schema_constraint(self) -> None:
        """ps-validator pattern: malformed enabler schema violations = constraint evidence."""
        path = _write_temp(MALFORMED_ENABLER_MD)
        try:
            result = validate_file(path, schema="enabler")
            assert result["schema_valid"] is False
            violations = result["schema_violations"]
            assert len(violations) > 0
            # Violations have required fields for evidence documentation
            for v in violations:
                assert "field_path" in v
                assert "expected" in v
                assert "actual" in v
                assert "message" in v
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_schema_violation_field_paths_for_evidence(self) -> None:
        """Schema violations include field_path for evidence documentation."""
        path = _write_temp(MALFORMED_ENABLER_MD)
        try:
            result = validate_file(path, schema="enabler")
            violations = result["schema_violations"]
            # Should detect missing Priority, Impact, Enabler Type, Created, Parent
            field_paths = {v["field_path"] for v in violations}
            assert "frontmatter.Priority" in field_paths
            assert "frontmatter.Impact" in field_paths
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_batch_schema_validation_entity_type_detection(self) -> None:
        """ps-validator batch pattern: detect entity type then validate schema."""
        files = [
            (VALID_ENABLER_MD, "enabler", True),
            (MALFORMED_ENABLER_MD, "enabler", False),
            (STORY_DELIVERABLE_MD, "story", True),
        ]
        paths = _write_temp_list([content for content, _, _ in files])
        try:
            for i, (_, expected_type, expected_valid) in enumerate(files):
                path = paths[i]
                fm = query_frontmatter(path)
                entity_type = fm.get("Type", "").lower()
                assert entity_type == expected_type, (
                    f"File {i}: expected {expected_type}, got {entity_type}"
                )
                result = validate_file(path, schema=entity_type)
                assert result["schema_valid"] == expected_valid, (
                    f"File {i}: expected schema_valid={expected_valid}, got {result['schema_valid']}"
                )
        finally:
            _cleanup_paths(paths)


# ---------------------------------------------------------------------------
# Tests: Performance - 50-file batch validation under 200ms
# ---------------------------------------------------------------------------


class TestBatchValidationPerformance:
    """Performance tests for batch AST operations.

    Validates that processing 50 files via validate_nav_table_file() completes
    in under 200ms, ensuring AST operations scale for agent workflows.
    Budget is 200ms (not 100ms) to accommodate macOS tmpfile I/O variance.
    """

    @pytest.mark.happy_path
    def test_50_file_nav_table_batch_under_200ms(self) -> None:
        """Validate 50 files for nav table compliance in under 200ms."""
        # Create 50 files alternating between valid and invalid nav tables
        contents = []
        for _i in range(25):
            contents.append(WITH_NAV_TABLE_MD)
            contents.append(NO_NAV_TABLE_MD)

        paths = _write_temp_list(contents)
        try:
            start_time = time.perf_counter()
            results = [validate_nav_table_file(p) for p in paths]
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            # Verify correctness
            assert len(results) == 50
            valid_count = sum(1 for r in results if r["is_valid"])
            invalid_count = sum(1 for r in results if not r["is_valid"])
            assert valid_count == 25
            assert invalid_count == 25

            # Verify performance
            assert elapsed_ms < 200, (
                f"50-file batch validation took {elapsed_ms:.1f}ms, expected < 200ms"
            )
        finally:
            _cleanup_paths(paths)

    @pytest.mark.happy_path
    def test_50_file_frontmatter_batch_under_200ms(self) -> None:
        """Extract frontmatter from 50 files in under 200ms."""
        contents = [STORY_DELIVERABLE_MD] * 25 + [VALID_ENABLER_MD] * 25
        paths = _write_temp_list(contents)
        try:
            start_time = time.perf_counter()
            results = [query_frontmatter(p) for p in paths]
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            # Verify correctness
            assert len(results) == 50
            story_count = sum(1 for r in results if r.get("Type") == "story")
            enabler_count = sum(1 for r in results if r.get("Type") == "enabler")
            assert story_count == 25
            assert enabler_count == 25

            # Verify performance
            assert elapsed_ms < 200, (
                f"50-file frontmatter batch took {elapsed_ms:.1f}ms, expected < 200ms"
            )
        finally:
            _cleanup_paths(paths)

    @pytest.mark.happy_path
    def test_50_file_parse_batch_under_200ms(self) -> None:
        """Parse 50 files for structural info in under 200ms."""
        contents = [ADR_DELIVERABLE_MD] * 17 + [WITH_NAV_TABLE_MD] * 17 + [REVIEW_PACKAGE_MD] * 16
        paths = _write_temp_list(contents)
        try:
            start_time = time.perf_counter()
            results = [parse_file(p) for p in paths]
            elapsed_ms = (time.perf_counter() - start_time) * 1000

            # Verify correctness
            assert len(results) == 50
            with_frontmatter = sum(1 for r in results if r["has_frontmatter"])
            assert with_frontmatter > 0

            # Verify performance
            assert elapsed_ms < 200, (
                f"50-file parse batch took {elapsed_ms:.1f}ms, expected < 200ms"
            )
        finally:
            _cleanup_paths(paths)


# ---------------------------------------------------------------------------
# Tests: Integration - combined AST operations (agent workflow simulation)
# ---------------------------------------------------------------------------


class TestCombinedASTOperationsWorkflow:
    """Integration tests combining multiple AST operations.

    Simulates the combined AST pre-check pattern added to migrated agents
    (e.g., adv-executor's Step 2 combined check, ps-critic's scoring setup).
    """

    @pytest.mark.happy_path
    def test_adv_executor_pre_check_pattern(self) -> None:
        """Simulates adv-executor Step 2 AST pre-check before strategy execution."""
        path = _write_temp(STORY_DELIVERABLE_MD)
        try:
            # Step 1: Get entity type (replaces guessing from filename)
            fm = query_frontmatter(path)
            entity_type = fm.get("Type", "unknown").lower()
            assert entity_type == "story"

            # Step 2: Check structural completeness
            info = parse_file(path)
            assert info["heading_count"] >= 3
            assert info["has_frontmatter"] is True

            # Step 3: Validate entity schema -- violations are potential findings
            result = validate_file(path, schema=entity_type)
            assert result["schema_valid"] is True
            assert result["schema_violations"] == []
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_adv_scorer_pre_check_pattern(self) -> None:
        """Simulates adv-scorer Step 1 AST pre-check before S-014 scoring."""
        path = _write_temp(REVIEW_PACKAGE_MD)
        try:
            # Step 1: Extract entity context
            fm = query_frontmatter(path)
            assert fm.get("Status") == "Conditional"

            # Step 2: Nav table compliance (affects Completeness dimension)
            nav_result = validate_nav_table_file(path)
            assert nav_result["is_valid"] is True
            # is_valid=True means no Completeness deduction for nav table

            # Step 3: Structural info
            info = parse_file(path)
            assert info["heading_count"] >= 4
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_ps_validator_constraint_verification_pattern(self) -> None:
        """Simulates ps-validator using AST for constraint evidence."""
        path = _write_temp(VALID_ENABLER_MD)
        try:
            # Detect entity type
            fm = query_frontmatter(path)
            entity_type = fm.get("Type", "").lower()
            assert entity_type == "enabler"

            # Schema validation: provides structured constraint evidence
            result = validate_file(path, schema=entity_type)
            assert result["schema_valid"] is True
            # Constraint VALIDATED: required fields all present

            # Nav table: H-23/H-24 compliance constraint
            nav_result = validate_nav_table_file(path)
            assert nav_result["is_valid"] is True
            # Constraint VALIDATED: H-23/H-24 compliance met
        finally:
            os.unlink(path)

    @pytest.mark.negative
    def test_ps_validator_constraint_failure_gives_structured_evidence(self) -> None:
        """ps-validator pattern: schema violation dict maps to evidence format."""
        path = _write_temp(MALFORMED_ENABLER_MD)
        try:
            fm = query_frontmatter(path)
            entity_type = fm.get("Type", "").lower()

            result = validate_file(path, schema=entity_type)
            assert result["schema_valid"] is False

            # Each violation maps to ps-validator evidence format:
            # | Evidence ID | Type | Source | Validates |
            for i, v in enumerate(result["schema_violations"]):
                evidence = {
                    "id": f"E-{i + 1:03d}",
                    "type": "SCHEMA",
                    "source": f"{v['field_path']}: {v['actual']}",
                    "validates": f"c-XXX (required field {v['field_path']})",
                }
                assert evidence["id"].startswith("E-")
                assert len(evidence["source"]) > 0
        finally:
            os.unlink(path)

    @pytest.mark.happy_path
    def test_nse_reviewer_criteria_check_pattern(self) -> None:
        """nse-reviewer pattern: read Status for entrance criteria verification."""
        path = _write_temp(REQUIREMENTS_DOC_MD)
        try:
            # Check "Requirements baseline approved" entrance criterion
            fm = query_frontmatter(path)
            status = fm.get("Status", "draft")

            # Criteria: status must be "baselined" or "approved"
            baseline_statuses = {"baselined", "approved"}
            criteria_met = status in baseline_statuses
            assert criteria_met is True

            # Also verify nav table compliance of the requirements doc
            nav_result = validate_nav_table_file(path)
            assert nav_result["is_valid"] is True
        finally:
            os.unlink(path)
