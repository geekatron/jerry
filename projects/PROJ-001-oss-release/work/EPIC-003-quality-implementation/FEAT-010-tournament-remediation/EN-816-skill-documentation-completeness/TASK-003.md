# TASK-003: Align fallback behavior between adv-executor.md and SKILL.md

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
> **Parent:** EN-816

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

Ensure adv-executor.md and SKILL.md describe the same fallback behavior when a strategy template is missing or malformed. Currently, the two documents may describe different behaviors. Choose the correct behavior (halt with CRITICAL finding) and update both documents to be consistent.

### Acceptance Criteria

- [ ] Both documents describe identical fallback behavior
- [ ] Behavior is halt with CRITICAL finding
- [ ] No contradictions between the two files
- [ ] Documentation updated in both locations

### Related Items
- Parent: [EN-816: Skill Documentation Completeness](EN-816-skill-documentation-completeness.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated adv-executor.md | file | skills/adversary/agents/adv-executor.md |
| Updated SKILL.md | file | skills/adversary/SKILL.md |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Created from EN-816 breakdown. |
