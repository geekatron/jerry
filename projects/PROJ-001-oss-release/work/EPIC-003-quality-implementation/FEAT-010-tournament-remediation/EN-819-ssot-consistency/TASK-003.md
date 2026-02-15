# TASK-003: Define malformed template fallback behavior in adv-executor.md

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
> **Parent:** EN-819

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

Update skills/adversary/agents/adv-executor.md to define the fallback behavior when a malformed template is encountered during execution. The executor MUST emit a CRITICAL finding (severity: CRITICAL, category: TEMPLATE_INTEGRITY) and halt execution of that strategy. It MUST NOT attempt to execute a malformed template or silently skip it.

### Acceptance Criteria
- [ ] adv-executor.md updated with malformed template handling
- [ ] Behavior is emit CRITICAL + halt
- [ ] Finding includes template path and parse error
- [ ] No silent skipping

### Related Items
- Parent: [EN-819: SSOT Consistency & Template Resilience](EN-819-ssot-consistency.md)

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
| Updated adv-executor.md | Documentation | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-819 breakdown. |
