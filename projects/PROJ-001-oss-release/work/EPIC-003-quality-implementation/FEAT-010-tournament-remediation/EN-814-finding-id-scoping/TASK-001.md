# TASK-001: Add execution-scoped finding ID prefix format to TEMPLATE-FORMAT.md

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
> **Parent:** EN-814

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

Update .context/templates/adversarial/TEMPLATE-FORMAT.md to define the execution-scoped finding ID format. Finding IDs MUST use the format {STRATEGY_PREFIX}-{SEQ}-{EXECUTION_ID} where STRATEGY_PREFIX is strategy-specific (e.g., FM for FMEA, DA for Devil's Advocate), SEQ is a zero-padded sequence number, and EXECUTION_ID is a unique execution identifier.

### Acceptance Criteria

- [ ] TEMPLATE-FORMAT.md updated with finding ID format specification
- [ ] Format documented with examples
- [ ] Backward compatibility note included

### Related Items

- Parent: [EN-814: Finding ID Scoping & Uniqueness](EN-814-finding-id-scoping.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated TEMPLATE-FORMAT.md | Documentation | --- |
| Finding ID format specification | Documentation | --- |
| Examples and backward compatibility note | Documentation | --- |

### Verification

- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-814 technical approach. |
