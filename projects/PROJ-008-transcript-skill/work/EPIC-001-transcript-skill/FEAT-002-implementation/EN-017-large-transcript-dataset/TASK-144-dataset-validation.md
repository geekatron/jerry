# Task: TASK-144 - Validate Dataset & Update Documentation

> **Task ID:** TASK-144
> **Status:** pending
> **Priority:** high
> **Enabler:** [EN-017-large-transcript-dataset](./EN-017-large-transcript-dataset.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Validate all 3 large transcripts meet specifications, pass ts-parser validation, and update test data documentation. This is the final gate before EN-018 split validation testing.

---

## Acceptance Criteria

- [ ] **AC-1:** All 3 transcripts pass ts-parser W3C WebVTT validation
- [ ] **AC-2:** Token counts verified within target ranges
- [ ] **AC-3:** Expected split counts documented
- [ ] **AC-4:** ts-extractor produces valid extraction reports
- [ ] **AC-5:** Test data README.md updated with new transcripts
- [ ] **AC-6:** EN-017 enabler marked complete

---

## Technical Specifications

### Validation Matrix

| Transcript | Token Range | Split Count | ts-parser | ts-extractor |
|------------|-------------|-------------|-----------|--------------|
| meeting-004 | 22K-28K | 0 | ✓ | ✓ |
| meeting-005 | 42K-48K | 1 | ✓ | ✓ |
| meeting-006 | 85K-95K | 2-3 | ✓ | ✓ |

### Validation Checklist

For each transcript:
1. W3C WebVTT format compliance
2. Token count within range
3. Expected split count calculation
4. Entity extraction success
5. No parsing errors or warnings

---

## Unit of Work

### Step 1: Validate meeting-004
- Run ts-parser validation
- Verify token count (22K-28K)
- Confirm no splits required
- Verify entity extraction

### Step 2: Validate meeting-005
- Run ts-parser validation
- Verify token count (42K-48K)
- Confirm 1 split required
- Verify entity extraction

### Step 3: Validate meeting-006
- Run ts-parser validation
- Verify token count (85K-95K)
- Confirm 2-3 splits required
- Verify entity extraction

### Step 4: Update Test Data Documentation
Update `skills/transcript/test_data/README.md` with:
- New transcript descriptions
- Token counts and split expectations
- Usage notes for split testing

### Step 5: Update EN-017 Status
- Mark all acceptance criteria as complete
- Update enabler status to complete
- Document validation evidence

### Step 6: Prepare for EN-018
- Confirm EN-018 can proceed
- Document handoff notes

---

## Dependencies

### Depends On
- TASK-141 (meeting-004 creation)
- TASK-142 (meeting-005 creation)
- TASK-143 (meeting-006 creation)

### Blocks
- EN-018 (Split Validation Testing)

---

## Verification Evidence

| Criterion | Evidence Required |
|-----------|-------------------|
| AC-1 | ts-parser output logs for all 3 |
| AC-2 | TokenCounter output for all 3 |
| AC-3 | Split calculation documentation |
| AC-4 | ts-extractor reports for all 3 |
| AC-5 | README.md diff/commit |
| AC-6 | EN-017 status updated |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
