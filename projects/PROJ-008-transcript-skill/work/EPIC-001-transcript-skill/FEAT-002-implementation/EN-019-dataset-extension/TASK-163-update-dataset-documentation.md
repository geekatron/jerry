# Task: TASK-163 - Update Dataset Documentation

> **Task ID:** TASK-163
> **Status:** pending
> **Priority:** medium
> **Enabler:** [EN-019-dataset-extension](./EN-019-dataset-extension.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Update EN-017 dataset documentation to reflect the extended transcript sizes and close the test coverage gap identified in DISC-008.

---

## Acceptance Criteria

- [ ] **AC-1:** EN-017 documentation updated with new word counts
- [ ] **AC-2:** DISC-008 marked as resolved
- [ ] **AC-3:** Test coverage gap documented as closed
- [ ] **AC-4:** Token calculation formula clarified (Markdown vs VTT)
- [ ] **AC-5:** ORCHESTRATION.yaml updated with EN-019 completion

---

## Technical Specifications

### Documentation Updates Required

| Document | Update |
|----------|--------|
| EN-017-large-transcript-dataset.md | New word counts and token estimates |
| DISC-008 | Mark as RESOLVED with EN-019 reference |
| ORCHESTRATION.yaml | EN-019 status: complete |
| EN-018-split-validation.md | Update test coverage notes |

### Updated Test Matrix

**Before (EN-017 original):**

| Transcript | Words | MD Tokens | Splits | Coverage Gap |
|------------|-------|-----------|--------|--------------|
| meeting-004 | 13,030 | 18,633 | 0 | Near-limit NOT tested |
| meeting-005 | 20,202 | 28,889 | 0 | 1-split NOT tested |
| meeting-006 | 44,225 | 63,242 | 2 | Working |

**After (EN-019 extended):**

| Transcript | Words | MD Tokens | Splits | Coverage |
|------------|-------|-----------|--------|----------|
| meeting-004-ext | 22,500 | 32,175 | 0-1 | Near-limit TESTED |
| meeting-005-ext | 26,000 | 37,180 | 1 | 1-split TESTED |
| meeting-006 | 44,225 | 63,242 | 2 | Multi-split TESTED |

---

## Unit of Work

### Step 1: Update EN-017 Documentation
- Update word count table
- Update token estimates with Markdown formula
- Document extension rationale

### Step 2: Resolve DISC-008
- Add resolution section
- Reference EN-019 as corrective work
- Mark status as RESOLVED

### Step 3: Update ORCHESTRATION.yaml
- Set EN-019 status: complete
- Update metrics
- Add history entry

### Step 4: Update Test Coverage Notes
- Update EN-018 with full coverage note
- Remove test coverage gap warning
- Document final split test matrix

---

## Dependencies

### Depends On
- TASK-162 (Validation complete)

### Blocks
- GATE-6 (Full split testing complete)

---

## Evidence

| Criterion | Evidence Required | Status |
|-----------|-------------------|--------|
| AC-1 | EN-017 updated content | pending |
| AC-2 | DISC-008 resolution section | pending |
| AC-3 | Test matrix update | pending |
| AC-4 | Formula clarification | pending |
| AC-5 | ORCHESTRATION.yaml update | pending |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created per DISC-008 corrective work |
