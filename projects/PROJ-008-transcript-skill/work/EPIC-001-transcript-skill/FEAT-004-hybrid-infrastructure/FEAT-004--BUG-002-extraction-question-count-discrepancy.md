# BUG-002: Extraction Layer Question Count Discrepancy

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-01-30 (EN-025 quality verification)
PURPOSE: Document extraction layer defect causing inflated question counts

DISCOVERY: Found during EN-025 live test quality review (ps-critic validation)
ROOT CAUSE: ts-extractor agent over-extracting questions from transcript
-->

> **Type:** bug
> **Status:** in_progress
> **Priority:** medium
> **Impact:** medium
> **Severity:** major
> **Created:** 2026-01-30T14:30:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** FEAT-004
> **Owner:** Claude
> **Found In:** v2.0.0 (Hybrid Pipeline)
> **Fix Version:** ts-extractor v1.3.0

---

## Summary

During EN-025 live test quality review, ps-critic identified a significant discrepancy between reported question count (63) and actual questions verifiable in transcript (15). This causes the overall quality score to fall below the 0.90 threshold (actual: 0.78), despite Parser/Chunker pipeline scoring 1.00 (100% compliant).

**Key Details:**
- **Symptom:** Extraction report claims 63 questions, manual verification finds ~15
- **Frequency:** Consistent across all test transcripts
- **Workaround:** Manual review and filtering of extraction-report.json

---

## Reproduction Steps

### Prerequisites

- VTT transcript file (e.g., meeting-006.vtt)
- Functional hybrid pipeline (EN-020, EN-021, EN-025)
- ts-extractor agent definition

### Steps to Reproduce

1. Run hybrid pipeline: `uv run jerry transcript parse <file.vtt> --output-dir <dir>`
2. Execute ts-extractor agent on chunked output
3. Review extraction-report.json question count
4. Manually verify questions in source transcript
5. Compare counts

### Expected Result

Question count in extraction-report.json should match actual questions in transcript (within 10% margin for borderline cases like rhetorical questions).

### Actual Result

Extraction report shows 63 questions, but only ~15 are verifiable as genuine questions in the source transcript. Discrepancy ratio: ~4.2x over-extraction.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS Darwin 25.2.0 |
| **Browser/Runtime** | Python 3.11+ via UV |
| **Application Version** | Jerry v0.2.0, Transcript Skill v2.0.0 |
| **Configuration** | Default ts-extractor.md v1.2.0 |
| **Deployment** | Local development (Claude Code CLI) |

### Additional Environment Details

- Parser: Python VTT parser (100% compliant)
- Chunker: Token-based chunker (18K tokens/chunk, 100% compliant)
- Test file: live-output-meeting-006/
- Quality review: quality-review-2026-01-30.md

---

## Evidence

### Bug Documentation

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| quality-review-2026-01-30.md | Report | ps-critic quality review showing 0.78 score | 2026-01-30 |
| extraction-report.json | Data | Shows 63 questions extracted | 2026-01-30 |
| canonical-transcript.json | Data | Source transcript for manual verification | 2026-01-30 |

### Quality Review Extract

From `quality-review-2026-01-30.md`:

```
Parser/Chunker Compliance: 1.00 (100%)
Overall Quality Score: 0.78 (BELOW 0.90 threshold)

Issue: Question count discrepancy
- Reported: 63 questions
- Verified: ~15 questions
- Discrepancy: 4.2x over-extraction
```

---

## Root Cause Analysis

### Investigation Summary

Investigation confirmed. The ts-extractor agent was counting questions at two different points:

1. **extraction_stats calculation**: Counted ALL segments ending with "?" (~63)
2. **questions array population**: Only populated semantically valid questions (15)

This created a stats-array mismatch that violated data integrity (P-001).

### Root Cause

**Dual-count discrepancy in ts-extractor agent definition:**

The agent's tiered extraction pipeline (PAT-001) has a Tier 1 rule:
```
QUESTION PATTERNS:
- Ends with "?" → confidence 0.95
```

This syntactic rule detected 63 "?" segments, but the semantic extraction only produced 15 actual questions. The stats were calculated from the syntactic count, not the final array.

### Contributing Factors

- **Syntactic vs Semantic counting**: Stats counted "?" occurrences, not extracted questions
- **No validation rule**: No requirement that `extraction_stats.questions == len(questions)`
- **Rhetorical questions**: Tag questions like "...right?", "...okay?" were counted but not extracted
- **Conversational fillers**: Segments like "you know?" counted in stats but filtered during extraction

---

## Fix Description

### Solution Approach

Added two mandatory data integrity invariants to ts-extractor.md v1.3.0:

1. **INV-EXT-001 (Stats-Array Consistency)**: All `extraction_stats` counts MUST equal corresponding array lengths
2. **INV-EXT-002 (Semantic Question Extraction)**: Questions extracted by semantic meaning, not "?" punctuation

### Changes Made

**File:** `skills/transcript/agents/ts-extractor.md`
**Version:** 1.2.0 → 1.3.0

1. Added comments to extraction_stats schema requiring counts match array lengths
2. Added "Data Integrity Invariants" section with:
   - INV-EXT-001: Stats-Array Consistency (MANDATORY validation)
   - INV-EXT-002: Question Extraction (Semantic, Not Syntactic)
3. Updated Constitutional Compliance table with P-001 (Truth/Accuracy)
4. Updated Self-Critique Checklist with two new validation items
5. Updated version to 1.3.0 with changelog entry

---

## Acceptance Criteria

### Fix Verification

- [x] Agent definition updated with INV-EXT-001 (stats must equal array lengths)
- [x] Agent definition updated with INV-EXT-002 (semantic question extraction)
- [ ] Question count in extraction-report.json within 10% of manual verification
- [ ] Rhetorical questions and filler phrases filtered out
- [ ] Overall quality score >= 0.90 with corrected extraction

### Quality Checklist

- [ ] Regression tests added for question extraction accuracy
- [ ] Existing tests still passing
- [ ] No new issues introduced
- [x] ts-extractor.md documentation updated (v1.3.0)

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-004: Hybrid Infrastructure](./FEAT-004-hybrid-infrastructure.md)

### Related Items

- **Discovery Context:** [EN-025: Skill Integration](./EN-025-skill-integration/EN-025-skill-integration.md) - Quality review during verification
- **Quality Review:** [quality-review-2026-01-30.md](../../skills/transcript/test_data/validation/live-output-meeting-006/quality-review-2026-01-30.md)
- **Not Related to:** EN-025 Parser/Chunker (scored 1.00, out of scope)

### Out of Scope Clarification

This bug is **NOT** related to EN-025 (ts-parser v2.0 + CLI + SKILL.md Integration). EN-025 scope is Parser/Chunker pipeline which scored 100% compliance. The extraction layer (ts-extractor) is a separate component that will be addressed in a future enabler or bug fix.

---

## State Machine Reference

```
+-------------------------------------------------------------------+
|                     BUG STATE MACHINE                              |
+-------------------------------------------------------------------+
|                                                                    |
|   +---------+     +-------------+     +-----------+               |
|   | PENDING |---->| IN_PROGRESS |---->| COMPLETED |               |
|   +---------+     +-------------+     +-----------+               |
|        ^               |                   |                       |
|        |               |                   |                       |
|        v               v                   v                       |
|   (current)        (Working)           (Verified)                  |
|                                                                    |
+-------------------------------------------------------------------+
```

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-30T14:30:00Z | Claude | pending | Bug created during EN-025 quality verification. Parser/Chunker compliant (1.00) but overall quality 0.78 due to extraction layer question count discrepancy. |
| 2026-01-30T15:00:00Z | Claude | in_progress | Root cause identified: stats calculated from "?" count (63), array from semantic extraction (15). Fix: INV-EXT-001 and INV-EXT-002 added to ts-extractor.md v1.3.0. Verification pending. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Bug |
| **SAFe** | Defect |
| **JIRA** | Bug |

---

<!--
DESIGN RATIONALE:

This bug tracks a quality issue discovered during EN-025 live test verification.
The Parser/Chunker pipeline (EN-025 scope) is 100% compliant.
The extraction layer (ts-extractor) has a separate quality issue that causes
the overall quality score to fall below the 0.90 threshold.

SCOPE SEPARATION:
- EN-025: Parser/Chunker pipeline -> COMPLIANT (1.00)
- This bug: Extraction layer -> NON-COMPLIANT (causes 0.78 overall)

This separation is important because:
1. EN-025 deliverables are complete and working
2. The extraction bug is a pre-existing issue in ts-extractor
3. Fixing this bug will be a separate effort (future enabler or task)

TRACE:
- EN-025 -> TASK-253 -> quality-review-2026-01-30.md -> this bug
-->
