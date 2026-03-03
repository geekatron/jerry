# TASK-024: Phase 4: SKILL.md files — upgrade "Do NOT use when:" sections

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-02-28
> **Completed:** 2026-02-28
> **Parent:** FEAT-001
> **Owner:** Claude
> **Activity:** DEVELOPMENT

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

Upgrade 4 NPT-014 instances across 2 SKILL.md files (saucer-boy and saucer-boy-framework-voice) for P-003 and governance-context prohibitions.

---

## Content

### Description

Upgrade 4 NPT-014 instances across 2 SKILL.md files. These are P-003 agent hierarchy prohibitions and governance-context prohibitions in the saucer-boy and saucer-boy-framework-voice skills.

### Acceptance Criteria

- [x] P4-01: saucer-boy/SKILL.md agent invocation prohibition upgraded with consequence + alternative
- [x] P4-02: saucer-boy-framework-voice/SKILL.md cross-agent prohibition upgraded with consequence + alternative
- [x] P4-03: saucer-boy/SKILL.md governance artifact prohibition upgraded with explanation
- [x] No functional changes — structural upgrades only

### Related Items

- Parent: [FEAT-001: Implement ADR-001](./FEAT-001-implement-adr-001-npt-014-elimination.md)
- Depends On: [TASK-021: Baseline capture](./TASK-021-baseline-capture.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| saucer-boy/SKILL.md | SKILL.md edit | `skills/saucer-boy/SKILL.md` |
| saucer-boy-framework-voice/SKILL.md | SKILL.md edit | `skills/saucer-boy-framework-voice/SKILL.md` |

### Verification

- [x] Acceptance criteria verified
- [x] 4 instances across 2 SKILL.md files upgraded
- [x] Committed in 47451ef6

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
| 2026-02-28 | completed | 4 instances across 2 SKILL.md files upgraded |
