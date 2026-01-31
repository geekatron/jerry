# Task: TASK-162 - Validate Extended Transcripts

> **Task ID:** TASK-162
> **Status:** pending
> **Priority:** high
> **Enabler:** [EN-019-dataset-extension](./EN-019-dataset-extension.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Validate that the extended meeting-004 and meeting-005 transcripts are syntactically valid VTT files and can be successfully processed by ts-parser to produce canonical JSON output.

---

## Acceptance Criteria

- [ ] **AC-1:** meeting-004 extended passes ts-parser validation
- [ ] **AC-2:** meeting-005 extended passes ts-parser validation
- [ ] **AC-3:** Token counts within expected ranges (+/- 5%)
- [ ] **AC-4:** No VTT format errors or warnings
- [ ] **AC-5:** Canonical JSON output is well-formed

---

## Technical Specifications

### Validation Matrix

| Transcript | Target Words | Expected MD Tokens | Split Behavior |
|------------|--------------|-------------------|----------------|
| meeting-004-extended | 22,500 | ~32,175 | Near soft limit |
| meeting-005-extended | 26,000 | ~37,180 | 1 split |

### Validation Steps

1. **Syntax Validation**
   - VTT header present and valid
   - All timestamps in correct format
   - Speaker tags properly formatted
   - No orphaned cues

2. **Parser Validation**
   - ts-parser processes without errors
   - Canonical JSON output generated
   - All segments extracted correctly

3. **Token Verification**
   - Word count matches target (+/- 5%)
   - Calculated tokens within range
   - Split predictions validated

---

## Unit of Work

### Step 1: Validate meeting-004 Extended
- Run VTT syntax check
- Parse with ts-parser
- Verify word count: 22,500 +/- 5%
- Calculate: `words × 1.43 = ~32,175 tokens`

### Step 2: Validate meeting-005 Extended
- Run VTT syntax check
- Parse with ts-parser
- Verify word count: 26,000 +/- 5%
- Calculate: `words × 1.43 = ~37,180 tokens`

### Step 3: Verify Canonical JSON
- Confirm segments array populated
- Verify speaker attribution present
- Check timestamp ordering

### Step 4: Document Validation Results
- Create validation report
- Document any warnings or issues
- Confirm readiness for EN-018 re-run

---

## Dependencies

### Depends On
- TASK-160 (Extend meeting-004)
- TASK-161 (Extend meeting-005)

### Blocks
- TASK-163 (Documentation Update)

---

## Evidence

| Criterion | Evidence Required | Status |
|-----------|-------------------|--------|
| AC-1 | ts-parser output for meeting-004 | pending |
| AC-2 | ts-parser output for meeting-005 | pending |
| AC-3 | Token calculation verification | pending |
| AC-4 | VTT validation output | pending |
| AC-5 | Canonical JSON samples | pending |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created per DISC-008 corrective work |
