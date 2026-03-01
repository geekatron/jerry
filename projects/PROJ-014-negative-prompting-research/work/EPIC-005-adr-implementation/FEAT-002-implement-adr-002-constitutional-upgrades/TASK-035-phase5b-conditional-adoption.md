# TASK-035: Phase 5B — Full Adoption or Contingency

> **Type:** task
> **Status:** pending
> **Priority:** low
> **Created:** 2026-02-28
> **Parent:** FEAT-002
> **Owner:** —
> **Activity:** IMPLEMENTATION

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Summary

Conditional on TASK-025 (A/B testing) results: implement NPT-013 constitutional triplet in all 13 SKILL.md files if framing effect confirmed, or implement consequence documentation only if null framing effect found.

---

## Content

### Description

ADR-002 Sub-Decision 4. This task is BLOCKED until TASK-025 (A/B testing) produces results. Based on those results:

- **If Phase 2 confirms framing effect (GO verdict):** Implement NPT-013 NEVER-framed constitutional triplet in all 13 SKILL.md files per TASK-010 recommendations.
- **If Phase 2 finds null framing effect (PG-003 triggered):** Implement consequence documentation only. NEVER-framing becomes convention-alignment only, not effectiveness-motivated.

### Acceptance Criteria

- [ ] TASK-025 A/B testing results available
- [ ] GO/NO-GO decision made based on framing effect evidence
- [ ] If GO: NPT-013 constitutional triplet added to all 13 SKILL.md files
- [ ] If NO-GO: Consequence documentation added without NEVER-framing mandate

### Related Items

- Parent: [FEAT-002: Implement ADR-002](./FEAT-002-implement-adr-002-constitutional-upgrades.md)
- Blocked By: TASK-025 (A/B testing results)
- References: ADR-002 Sub-Decision 4

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated SKILL.md files (13) | Skill modifications | `skills/*/SKILL.md` |

### Verification

- [ ] Acceptance criteria verified

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation — blocked by TASK-025 |
