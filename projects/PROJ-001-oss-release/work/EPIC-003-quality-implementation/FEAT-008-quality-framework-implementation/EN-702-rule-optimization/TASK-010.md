# TASK-010: Validate Total Token Count Within Budget

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
> **Priority:** HIGH
> **Activity:** TESTING
> **Agents:** nse-verification
> **Created:** 2026-02-14
> **Parent:** EN-702

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Re-measure all optimized files (10 rule files + CLAUDE.md) to confirm the total L1 token count is within the ~12,500 token budget. Compare against TASK-001 baseline to calculate actual reduction percentage. Identify any files that exceed their per-file target from EN-404's optimization plan.

### Acceptance Criteria

- [ ] All 11 files re-measured with same tokenizer used in TASK-001
- [ ] Total L1 token count is <= 12,500 tokens
- [ ] Per-file token counts compared against EN-404 per-file targets
- [ ] Reduction percentage calculated (target: ~51.5% reduction)
- [ ] Any files exceeding per-file targets flagged for further optimization
- [ ] Validation report produced with before/after comparison table

### Related Items

- Parent: [EN-702: Rule File Token Optimization](EN-702-rule-optimization.md)
- Depends on: TASK-004 through TASK-009 (all optimization tasks)
- Blocks: TASK-011 (pytest verification)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Token validation report | Test artifact | -- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Total within budget
- [ ] Before/after comparison documented

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-14 | Created | Initial creation. Verification gate -- all optimization tasks must complete before token validation. |
