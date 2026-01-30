# BUG-001: ts-extractor Question Count Inflation

<!--
TEMPLATE: Bug
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.10
CREATED: 2026-01-30 (investigation during TASK-253)
PURPOSE: Document defect in ts-extractor question counting logic
-->

> **Type:** bug
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-01-30T03:15:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** EN-008
> **Owner:** -
> **Found In:** ts-extractor v1.0.0
> **Fix Version:** TBD

---

## Frontmatter

```yaml
id: "BUG-001"
work_type: BUG
title: "ts-extractor Question Count Inflation"

classification: ENABLER
status: pending
resolution: null

priority: high
impact: high

assignee: null
created_by: "Claude"

created_at: "2026-01-30T03:15:00Z"
updated_at: "2026-01-30T03:15:00Z"
completed_at: null

parent_id: "EN-008"

tags:
  - "ts-extractor"
  - "data-integrity"
  - "extraction-stats"
  - "questions"

severity: major
found_in_version: "ts-extractor v1.0.0"
fix_version: null

reproduction_steps: |
  1. Run /transcript skill on meeting-006-all-hands.vtt
  2. Check extraction-report.json
  3. Compare extraction_stats.questions_found vs questions array length
environment: |
  - Jerry Framework PROJ-008-transcript-skill
  - ts-extractor agent (sonnet)
  - meeting-006-all-hands.vtt (3071 segments, 50 speakers)
root_cause: null
acceptance_criteria: |
  - extraction_stats.questions_found MUST equal len(questions) array
  - All extracted questions must be included in the output array
  - No phantom counts in extraction statistics
```

---

## Summary

The ts-extractor agent reports an inflated question count in `extraction_stats.questions_found` (63) that does not match the actual number of questions in the `questions` array (15). This represents a **320% inflation** (63 vs 15).

**Key Details:**
- **Symptom:** extraction_stats reports 63 questions found, but only 15 questions in array
- **Frequency:** Consistent across live test runs
- **Workaround:** Manual count of questions array for accurate metrics

---

## Reproduction Steps

### Prerequisites

- Jerry Framework with transcript skill installed
- Access to test file: `skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt`

### Steps to Reproduce

1. Run the transcript skill:
   ```
   /transcript skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt --output skills/transcript/test_data/validation/live-output-meeting-006
   ```

2. Open `extraction-report.json`

3. Compare:
   - `extraction_stats.questions_found` value
   - Actual length of `questions` array

### Expected Result

`extraction_stats.questions_found` should equal the actual count of items in the `questions` array.

### Actual Result

```json
{
  "extraction_stats": {
    "questions_found": 63,   // <-- Reports 63
    ...
  },
  "questions": [ ... ]       // <-- Actually contains 15 items
}
```

**Discrepancy:** 63 reported vs 15 actual = 320% inflation

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | macOS Darwin 25.2.0 |
| **Browser/Runtime** | Claude Code CLI |
| **Application Version** | PROJ-008-transcript-skill |
| **Configuration** | Default transcript skill settings |
| **Deployment** | Local development |

### Additional Environment Details

- Test file: `meeting-006-all-hands.vtt`
- File stats: 3071 segments, 50 speakers, 18,231,500ms duration
- Parser/Chunker pipeline: PASS (100% compliant)
- ts-extractor: Exhibits this bug

---

## Evidence

### Bug Documentation

| Evidence | Type | Description | Date |
|----------|------|-------------|------|
| extraction-report.json | JSON | Contains the discrepancy | 2026-01-30 |
| quality-review-2026-01-30.md | Report | ps-critic identified Data Integrity: 0.50 | 2026-01-30 |

### Other Entity Counts (For Reference)

The following counts ARE accurate (array length matches stats):

| Entity | Reported | Actual | Status |
|--------|----------|--------|--------|
| speakers | 50 | 50 | PASS |
| action_items | 9 | 9 | PASS |
| decisions | 5 | 5 | PASS |
| topics | 6 | 6 | PASS |
| **questions** | **63** | **15** | **FAIL** |

---

## Root Cause Analysis

### Investigation Summary

*To be completed during fix*

### Hypothesis

The ts-extractor may be counting ALL sentences containing "?" characters in the transcript, but then only extracting those that meet a confidence threshold into the actual array. The stats counter increments for every potential question, but the array only includes high-confidence extractions.

**Evidence supporting hypothesis:**
- 63 is plausible for total "?" occurrences in a 3071-segment meeting
- 15 is plausible for questions with high confidence/relevance

### Root Cause

*To be documented when fix is implemented*

### Contributing Factors

- Likely separation between "detection count" and "extraction count"
- Missing reconciliation between stats and actual output

---

## Fix Description

*To be completed when fix is implemented*

### Solution Approach

Options to consider:
1. **Option A:** Fix stats to count only what's in the array (post-filtering count)
2. **Option B:** Include all detected questions in array with confidence scores
3. **Option C:** Add two separate stats: `questions_detected` and `questions_extracted`

### Changes Made

*To be documented*

### Code References

| File | Change Description |
|------|-------------------|
| skills/transcript/agents/ts-extractor.md | Agent instructions for question extraction |

---

## Acceptance Criteria

### Fix Verification

- [ ] `extraction_stats.questions_found` equals `len(questions)` array
- [ ] All test transcripts pass data integrity validation
- [ ] ps-critic Data Integrity score >= 1.00 for extraction report

### Quality Checklist

- [ ] Contract tests updated for stats/array consistency
- [ ] Existing extraction tests still passing
- [ ] No regression in other entity extraction
- [ ] ts-extractor.md updated with correct counting logic

---

## Related Items

### Hierarchy

- **Parent:** [EN-008: Entity Extraction](./EN-008-entity-extraction.md)

### Related Items

- **Related Task:** TASK-253 (Integration Verification Tests) - discovered during this task
- **Affected Contract:** `skills/transcript/test_data/validation/contract-tests.yaml`
- **Quality Review:** `live-output-meeting-006/quality-review-2026-01-30.md`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-30 | Claude | pending | Initial report - discovered during TASK-253 integration verification |

---

## Impact Assessment

### Blast Radius

- **Direct:** Extraction report statistics are unreliable for questions
- **Indirect:** Any downstream processing relying on question counts
- **ps-critic:** Will fail Data Integrity checks (0.50 score observed)

### Scope of Fix

This may be part of a larger pattern. Investigation should verify:
1. Are other entity stats accurate? (Currently: YES for speakers, actions, decisions, topics)
2. Is this a ts-extractor instruction issue or implementation pattern?
3. Should extraction_stats schema be updated to distinguish detected vs extracted?

---
