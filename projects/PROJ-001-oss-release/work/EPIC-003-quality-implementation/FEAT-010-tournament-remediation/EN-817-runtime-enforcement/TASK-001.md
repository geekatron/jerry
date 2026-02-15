# TASK-001: Update adv-executor.md — block S-002 without prior S-003

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
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
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Update skills/adversary/agents/adv-executor.md to add a runtime check before executing S-002 (Devil's Advocate). The executor MUST verify that S-003 (Steelman) appears in the prior_strategies_executed list. If S-003 is not present, the executor MUST halt with an H-16 VIOLATION finding and refuse to execute S-002.

### Acceptance Criteria
- [ ] adv-executor.md updated with H-16 check
- [ ] Check occurs before S-002 execution
- [ ] Violation produces clear error message
- [ ] References H-16 rule source

### Related Items
- Parent: [EN-817: Runtime Enforcement](EN-817-runtime-enforcement.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated adv-executor.md | Documentation | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-817 breakdown. |
