# TASK-002: Add WTI-007 Mandatory Template Usage to behavior-rules.md

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

Add a new WTI-007 section to `skills/worktracker/rules/worktracker-behavior-rules.md` after the existing WTI-006 section (around line 115). The rule must specify:

1. **HARD enforcement level** -- This is a MUST/SHALL/NEVER rule that cannot be overridden
2. **Read-template-first procedure** with entity-to-template mapping table (entity type -> template file path)
3. **Anti-pattern warning** -- Creating entity files from memory or by copying other instance files is explicitly forbidden

The rule ensures that agents always consult the canonical template before creating any worktracker entity file, preventing structural drift.

### Acceptance Criteria

- [x] WTI-007 rule exists in behavior-rules.md with HARD enforcement level
- [x] Rule includes entity-to-template mapping table (10 types including Impediment/Spike)
- [x] Rule includes Read-template-first procedural steps
- [x] Rule includes anti-pattern section warning against creating from memory
- [x] Rule integrates naturally with existing WTI-001 through WTI-006 rules

### Implementation Notes

File: `skills/worktracker/rules/worktracker-behavior-rules.md`, location: after the existing WTI-006 section (around line 115), between "Worktracker Integrity Rules" and "Work tracker Behavior" sections.

The WTI-007 rule should follow the same formatting pattern as existing WTI rules. Key content:
- Rule ID: WTI-007
- Rule Name: Mandatory Template Usage
- Enforcement: HARD
- Procedure: (1) Identify entity type, (2) Read canonical template, (3) Populate from template, (4) Never create from memory

### Related Items

- Parent: [EN-820](EN-820-fix-behavioral-root-cause.md)
- Depends On: TASK-001 (conceptually -- templates must be loadable for the rule to reference them)
- Blocks: EN-821, EN-822, EN-823 (remediation enablers depend on this rule being in place)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | 0.5 hours |
| Remaining Work | 0.5 hours |
| Time Spent | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| WTI-007 rule | Code change | `skills/worktracker/rules/worktracker-behavior-rules.md` |
| WTI-007 canonical | Code change | `.context/templates/worktracker/WTI_RULES.md` |

### Verification

- [x] Acceptance criteria verified
- [x] WTI-007 rule follows existing WTI rule formatting conventions
- [x] Reviewed by: Claude (adversarial C3 cycle, 0.941 PASS)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Initial creation. Part of EN-820 behavioral root cause fix. |
| 2026-02-15 | DONE | Implemented with 10 entity types, section categories. Commit 1b98ecc. |
