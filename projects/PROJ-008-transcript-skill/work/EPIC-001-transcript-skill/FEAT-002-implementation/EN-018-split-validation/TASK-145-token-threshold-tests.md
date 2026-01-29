# Task: TASK-145 - Token Threshold Validation

> **Task ID:** TASK-145
> **Status:** pending
> **Priority:** high
> **Enabler:** [EN-018-split-validation](./EN-018-split-validation.md)
> **Created:** 2026-01-28
> **Last Updated:** 2026-01-28

---

## Summary

Validate that TokenCounter correctly identifies split requirements for each large transcript based on the defined thresholds (31.5K soft, 35K hard).

---

## Acceptance Criteria

- [ ] **AC-1:** TokenCounter returns NO split for meeting-004 (~25K tokens)
- [ ] **AC-2:** TokenCounter returns 1 split for meeting-005 (~45K tokens)
- [ ] **AC-3:** TokenCounter returns 2-3 splits for meeting-006 (~90K tokens)
- [ ] **AC-4:** Split count calculation matches expected formula
- [ ] **AC-5:** Threshold detection documented

---

## Technical Specifications

### Token Thresholds (from ADR-004)

| Threshold | Tokens | Behavior |
|-----------|--------|----------|
| Soft Limit | 31,500 | Split at semantic boundary |
| Hard Limit | 35,000 | Force split |

### Expected Results

| Transcript | Est. Tokens | Expected Splits | Calculation |
|------------|-------------|-----------------|-------------|
| meeting-004 | ~25,000 | 0 | 25K < 31.5K (no split) |
| meeting-005 | ~45,000 | 1 | 45K ÷ 31.5K ≈ 1.4 → 1 split |
| meeting-006 | ~90,000 | 2-3 | 90K ÷ 31.5K ≈ 2.9 → 2-3 splits |

---

## Unit of Work

### Step 1: Test meeting-004 Token Count
- Invoke TokenCounter on meeting-004.vtt
- Verify count is in 22K-28K range
- Confirm no split required

### Step 2: Test meeting-005 Token Count
- Invoke TokenCounter on meeting-005.vtt
- Verify count is in 42K-48K range
- Confirm 1 split required

### Step 3: Test meeting-006 Token Count
- Invoke TokenCounter on meeting-006.vtt
- Verify count is in 85K-95K range
- Confirm 2-3 splits required

### Step 4: Document Threshold Detection
- Record actual token counts
- Record split calculations
- Create verification evidence

---

## Dependencies

### Depends On
- EN-017 (Large Transcript Dataset)

### Blocks
- TASK-146 (Boundary Detection Tests)

---

## Verification Evidence

| Criterion | Evidence Required |
|-----------|-------------------|
| AC-1 | TokenCounter output for meeting-004 |
| AC-2 | TokenCounter output for meeting-005 |
| AC-3 | TokenCounter output for meeting-006 |
| AC-4 | Split calculation documentation |
| AC-5 | Threshold test summary |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial task created |
