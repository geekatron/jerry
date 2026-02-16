# TASK-006: Verify all 24 HARD rules preserved and measure token count

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** REVIEW
> **Created:** 2026-02-16
> **Parent:** EN-901

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description, acceptance criteria, implementation notes |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Content

### Description

Cross-reference all 24 HARD rules (H-01 through H-24) from `quality-enforcement.md` against the thinned rule files. Verify each rule appears in at least one auto-loaded file. Measure total auto-loaded token count.

Verification procedure:
1. Read `quality-enforcement.md` HARD Rule Index (H-01 through H-24)
2. For each HARD rule, search all 10 thinned `.context/rules/` files for the rule ID
3. Confirm the rule text and consequence are present
4. Record which file(s) contain each rule
5. Measure token count for each thinned file (characters / 4 approximation)
6. Sum total auto-loaded tokens across all 10 files
7. Verify total <= 6K tokens

Output: Verification report with:
- 24-row table: Rule ID | Rule Text | File(s) | Present (Y/N)
- Per-file token count table
- Total token count
- Pass/fail determination

### Acceptance Criteria

- [ ] 24/24 HARD rules verified present
- [ ] Total auto-loaded token count documented
- [ ] No enforcement semantics lost
- [ ] Report with per-file token breakdown

### Implementation Notes

The quality-enforcement.md file itself is part of the auto-loaded set and should NOT be thinned (it is the SSOT). Its token count still counts toward the 6K budget. If the total exceeds 6K, identify which files need further thinning.

### Related Items

- Parent: [EN-901: Rules File Thinning](EN-901-rules-thinning.md)
- Depends on: TASK-002, TASK-003, TASK-004, TASK-005 (all thinning must be complete before verification)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| HARD rule verification report | Document | pending |
| Per-file token count table | Document | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] 24/24 rules confirmed present in auto-loaded files
- [ ] Token budget verified <= 6K
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-901 rules thinning verification phase. |
