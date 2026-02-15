# TASK-002: Update all 10 strategy templates with scoped finding ID format

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
> **Parent:** EN-814

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

Update the Output Format section of all 10 strategy templates in .context/templates/adversarial/ to use the new execution-scoped finding ID format. Each template must specify its STRATEGY_PREFIX and show the scoped format in examples.

### Acceptance Criteria

- [ ] All 10 templates updated (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014)
- [ ] Each template defines its STRATEGY_PREFIX
- [ ] Examples show scoped format

### Related Items

- Parent: [EN-814: Finding ID Scoping & Uniqueness](EN-814-finding-id-scoping.md)
- Dependency: TASK-001 (TEMPLATE-FORMAT.md must define format first)

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
| Updated S-001 Red Team template | Documentation | --- |
| Updated S-002 Devil's Advocate template | Documentation | --- |
| Updated S-003 Steelman template | Documentation | --- |
| Updated S-004 Pre-Mortem template | Documentation | --- |
| Updated S-007 Constitutional AI template | Documentation | --- |
| Updated S-010 Self-Refine template | Documentation | --- |
| Updated S-011 Chain-of-Verification template | Documentation | --- |
| Updated S-012 FMEA template | Documentation | --- |
| Updated S-013 Inversion template | Documentation | --- |
| Updated S-014 LLM-as-Judge template | Documentation | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-814 technical approach. |
