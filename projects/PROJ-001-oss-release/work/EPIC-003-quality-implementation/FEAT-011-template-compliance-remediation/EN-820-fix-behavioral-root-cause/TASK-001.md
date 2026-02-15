# TASK-001: Add @import for worktracker-templates.md to SKILL.md

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** DONE
> **Priority:** CRITICAL
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-15
> **Parent:** EN-820

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description, acceptance criteria, implementation notes |
| [Time Tracking](#time-tracking) | Effort estimates |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Content

### Description

Add `@rules/worktracker-templates.md` as a second `@` import in `skills/worktracker/SKILL.md` line 66 (after the existing `@rules/worktracker-behavior-rules.md`). This ensures the CRITICAL template usage rules are auto-loaded into agent context when `/worktracker` is invoked.

This is the single most important fix in EN-820 -- without this `@` import, the template rules file exists on disk but is never loaded, making all its CRITICAL rules dead code.

### Acceptance Criteria

- [x] SKILL.md contains two `@` imports (behavior-rules and templates)
- [x] `/worktracker` invocation loads template rules into agent context
- [x] No existing functionality is broken by the addition

### Implementation Notes

Single line addition. File: `skills/worktracker/SKILL.md`, location: after line 66 (after the existing `@rules/worktracker-behavior-rules.md` import). The line to add:

```
@rules/worktracker-templates.md
```

### Related Items

- Parent: [EN-820](EN-820-fix-behavioral-root-cause.md)
- Blocks: TASK-002 (conceptually -- WTI-007 rule references templates that must be loadable)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | 0.25 hours |
| Remaining Work | 0.25 hours |
| Time Spent | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| SKILL.md @import | Code change | `skills/worktracker/SKILL.md` line 67 |

### Verification

- [x] Acceptance criteria verified
- [x] SKILL.md contains `@rules/worktracker-templates.md` import
- [x] Reviewed by: Claude (adversarial C3 cycle, 0.941 PASS)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Initial creation. Part of EN-820 behavioral root cause fix. |
| 2026-02-15 | DONE | Implemented. Commit 1b98ecc. Adversarial gate PASS 0.941. |
