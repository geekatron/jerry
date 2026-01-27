# DISC-002: Future Scope Analysis - EN-011 and EN-012

<!--
TEMPLATE: Discovery
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** discovery
> **Status:** EXECUTED
> **Created:** 2026-01-26T22:30:00Z
> **Executed:** 2026-01-26T23:30:00Z
> **Parent:** FEAT-002
> **Owner:** Claude
> **Trigger:** User feedback during BUG-001 resolution

---

## Summary

User requested analysis of whether EN-011 (Worktracker Integration) and EN-012 (Skill CLI Interface) should be moved to a new feature for future enhancements. This discovery documents the analysis and provides recommendations.

---

## Analysis

### EN-011: Worktracker Integration

| Attribute | Value | Analysis |
|-----------|-------|----------|
| **Gate** | GATE-6 (Final Review) | Core delivery gate |
| **Priority** | medium | Standard priority |
| **Tasks** | TASK-055..058 (4 tasks) | Reasonable scope |
| **Dependencies** | EN-016 (ts-formatter) | Depends on core artifact packaging |
| **Purpose** | Convert extracted entities to work items | **Core value proposition** |

**Evidence:**
- Worktracker integration is mentioned in FEAT-002 Benefit Hypothesis: "Work items suggested with traceability"
- TDD-ts-formatter.md explicitly defines worktracker integration as output
- ADR-002 (Artifact Structure) includes `08-workitems/suggested-tasks.md` as part of core packet

**Recommendation: KEEP IN FEAT-002**

EN-011 is core functionality that completes the "meeting → insights → action" loop. Moving it would break the value proposition.

---

### EN-012: Skill CLI Interface

| Attribute | Value | Analysis |
|-----------|-------|----------|
| **Gate** | GATE-7 (Above and Beyond - LITERALLY LAST) | Explicitly marked as optional |
| **Priority** | low | Lowest priority in feature |
| **Tasks** | TASK-059..062 (4 tasks) | Reasonable scope |
| **Dependencies** | EN-016 (ts-formatter) | Depends on core functionality |
| **Purpose** | `/transcript` slash command interface | **Nice-to-have enhancement** |

**Evidence:**
- Explicitly marked as "Above and Beyond - LITERALLY LAST" in multiple locations
- GATE-7 is isolated from GATE-5/6 review cycles
- Skill can function without CLI - user can invoke via natural language
- Definition of Done in FEAT-002 marks it as "(GATE-7 - Above and Beyond)"

**Recommendation: MOVE TO FEAT-003**

EN-012 is explicitly designed as an optional enhancement. Moving it to a future feature:
1. Clarifies scope of FEAT-002 (core implementation)
2. Allows FEAT-002 to be marked complete after GATE-6
3. Aligns with "MVP first" delivery approach

---

## Impact Analysis

### L0: Executive Summary (ELI5)

EN-011 (Worktracker) is like the "action" button after a meeting - it's essential. EN-012 (CLI) is like a fancy shortcut - nice to have but not required to use the skill.

### L1: Engineer Impact

Moving EN-012 to FEAT-003 would:
- Remove GATE-7 from FEAT-002 (now has 2 gates: GATE-5, GATE-6)
- Reduce FEAT-002 task count from 49 to 45
- Create cleaner separation of "core" vs "enhancement"

### L2: Architectural Impact

No architectural changes required. EN-012 dependencies on EN-016 remain valid across features. The skill invocation pattern (natural language → skill resolution) already exists - CLI is an alternative entry point.

---

## Recommendation

| Enabler | Current | Recommended | Rationale |
|---------|---------|-------------|-----------|
| EN-011 | FEAT-002 | **KEEP IN FEAT-002** | Core value delivery |
| EN-012 | FEAT-002 | **MOVE TO FEAT-003** | Explicit "Above and Beyond" scope |

### Proposed FEAT-003: Future Enhancements

```
FEAT-003: Future Enhancements
├── EN-012: Skill CLI Interface (from FEAT-002)
├── (future): Real-time streaming support
├── (future): Custom entity extractors
└── (future): Team/organization context
```

---

## Action Items

**APPROVED AND EXECUTED (2026-01-26):**

1. [x] Create FEAT-003-future-enhancements folder and feature file
2. [x] Move EN-012 folder from FEAT-002 to FEAT-003
3. [x] Update EN-012.md parent reference to FEAT-003
4. [x] Update FEAT-002-implementation.md to remove EN-012 and GATE-7
5. [x] Update WORKTRACKER.md with FEAT-003 reference (completed 2026-01-27)
6. [x] Update ORCHESTRATION.yaml (EN-012 status, GATE-7 status, metrics, history)

**Note:** TASK-059..062 parent references remain in EN-012 (now in FEAT-003).

**All action items complete.**

---

## Related Items

- **User Feedback:** "If EN-011 or EN-012 are future items they should be put moved into new feature for dealing with future enhancements."
- **BUG-001:** [EN-009 ID Conflict](./FEAT-002--BUG-001-en009-id-conflict.md) - Discovery triggered during resolution
- **EN-011:** [Worktracker Integration](./EN-011-worktracker-integration/EN-011-worktracker-integration.md)
- **EN-012:** [Skill CLI Interface](./EN-012-skill-interface/EN-012-skill-interface.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | OPEN | Discovery created per user feedback |
| 2026-01-26 | Claude | ANALYZED | Analysis complete, awaiting decision |
| 2026-01-26 | Claude | EXECUTED | User approved Option B. EN-012 moved to FEAT-003. GATE-7 removed from FEAT-002. |

---

## Decision Outcome

**Human decision received:** Option B approved.

- ~~**Option A:** Keep EN-012 in FEAT-002 (current state)~~
- **Option B (Recommended):** Move EN-012 to new FEAT-003 for future enhancements ✅ **SELECTED**

**Executed:** 2026-01-26. EN-012 now resides in [FEAT-003](../FEAT-003-future-enhancements/EN-012-skill-interface/EN-012-skill-interface.md).
