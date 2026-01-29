# Task: TASK-149 - CON-FMT-007 Contract Test Execution

> **Task ID:** TASK-149
> **Status:** pending
> **Priority:** high
> **Enabler:** [EN-018-split-validation](./EN-018-split-validation.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Execute contract test CON-FMT-007 (Split Navigation) using the large transcript dataset, validating that file splitting behavior meets all contract requirements.

---

## Acceptance Criteria

- [ ] **AC-1:** CON-FMT-007 passes for meeting-005 (single split)
- [ ] **AC-2:** CON-FMT-007 passes for meeting-006 (multi-split)
- [ ] **AC-3:** All contract criteria documented as verified
- [ ] **AC-4:** Evidence captured in validation report
- [ ] **AC-5:** EN-018 marked complete with evidence

---

## Technical Specifications

### CON-FMT-007 Contract Definition

From `contract-tests.yaml`:

```yaml
CON-FMT-007:
  name: "Split Navigation"
  description: "Split files contain navigation links"
  requirements:
    - Forward link at end of non-final split
    - Backward link at start of non-first split
    - Links use correct relative paths
    - Links point to valid anchors
    - _anchors.json tracks split file locations
```

### Test Execution Matrix

| Transcript | Expected Splits | Test Focus |
|------------|-----------------|------------|
| meeting-005 | 1 | Single split behavior |
| meeting-006 | 2-3 | Multi-split chaining |

### Verification Checklist

| # | Criterion | meeting-005 | meeting-006 |
|---|-----------|-------------|-------------|
| 1 | Forward links present | ☐ | ☐ |
| 2 | Backward links present | ☐ | ☐ |
| 3 | Relative paths correct | ☐ | ☐ |
| 4 | Target anchors valid | ☐ | ☐ |
| 5 | _anchors.json accurate | ☐ | ☐ |

---

## Unit of Work

### Step 1: Prepare Test Environment
- Confirm EN-017 transcripts available
- Verify ts-formatter ready
- Set up output directories

### Step 2: Execute meeting-005 Contract Test
- Process meeting-005 through ts-formatter
- Verify single split generated
- Check all CON-FMT-007 criteria

### Step 3: Execute meeting-006 Contract Test
- Process meeting-006 through ts-formatter
- Verify 2-3 splits generated
- Check all CON-FMT-007 criteria

### Step 4: Document Results
- Create CON-FMT-007 verification report
- Capture screenshots/evidence
- Update contract-tests.yaml with results

### Step 5: Complete EN-018
- Mark all acceptance criteria
- Update enabler status
- Prepare GATE-6 evidence

---

## Dependencies

### Depends On
- TASK-147 (Navigation Link Tests)
- TASK-148 (Anchor Tracking Tests)

### Blocks
- GATE-6 (Integration & Validation Review)

---

## Verification Evidence

| Criterion | Evidence Required |
|-----------|-------------------|
| AC-1 | meeting-005 test output and verification |
| AC-2 | meeting-006 test output and verification |
| AC-3 | Completed verification checklist |
| AC-4 | Validation report document |
| AC-5 | EN-018 status update commit |

---

## Contract Test Report Template

```markdown
# CON-FMT-007 Contract Test Report

## Test Execution Date: YYYY-MM-DD

## Test Results

### meeting-005 (Single Split)
- Splits Generated: X
- Forward Links: ✓/✗
- Backward Links: ✓/✗
- Relative Paths: ✓/✗
- Anchor Tracking: ✓/✗
- **Result: PASS/FAIL**

### meeting-006 (Multi-Split)
- Splits Generated: X
- Forward Links: ✓/✗
- Backward Links: ✓/✗
- Relative Paths: ✓/✗
- Anchor Tracking: ✓/✗
- **Result: PASS/FAIL**

## Overall: CON-FMT-007 PASS/FAIL
```

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
