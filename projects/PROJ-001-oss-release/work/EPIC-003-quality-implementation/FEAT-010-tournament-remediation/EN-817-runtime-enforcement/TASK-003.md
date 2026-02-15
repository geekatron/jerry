# TASK-003: Add auto-escalation cross-check to adv-selector.md

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-15
> **Parent:** EN-817

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Update skills/adversary/agents/adv-selector.md Step 1 (strategy selection) to cross-check the auto-escalation rules (AE-001 through AE-006) from quality-enforcement.md. When selecting strategies for a given criticality level, the selector must verify that the criticality has not been overridden by an auto-escalation rule (e.g., touching .context/rules/ = auto-C3 minimum).

### Acceptance Criteria
- [ ] adv-selector.md Step 1 updated with AE cross-check
- [ ] All 6 AE rules referenced
- [ ] Escalation overrides criticality input when applicable

### Related Items
- Parent: [EN-817: Runtime Enforcement](EN-817-runtime-enforcement.md)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | — |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated adv-selector.md | Documentation | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-817 breakdown. |
