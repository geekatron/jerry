# TASK-002: Add P-003 runtime self-check to all 3 agent specifications

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

Add a P-003 compliance self-check section to each of the 3 adversary skill agent specifications (adv-selector.md, adv-executor.md, adv-scorer.md). Each agent must include a statement that it MUST NOT spawn subagents and MUST return results directly to the invoking orchestrator.

### Acceptance Criteria
- [ ] All 3 agent specs updated
- [ ] P-003 self-check section present in each
- [ ] Language matches P-003 constitutional principle

### Related Items
- Parent: [EN-817: Runtime Enforcement](EN-817-runtime-enforcement.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated adv-selector.md | Documentation | --- |
| Updated adv-executor.md | Documentation | --- |
| Updated adv-scorer.md | Documentation | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-817 breakdown. |
