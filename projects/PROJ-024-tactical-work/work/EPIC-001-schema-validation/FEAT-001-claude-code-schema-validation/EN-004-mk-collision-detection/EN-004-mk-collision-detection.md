# EN-004: Memory-Keeper Collision Detection Enhancement

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.7
PURPOSE: Post-migration defense-in-depth for MK namespace collision prevention
-->

> **Type:** enabler
> **Enabler Type:** infrastructure
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-28T18:00:00Z
> **Due:**
> **Completed:**
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What and why |
| [Problem Statement](#problem-statement) | The risk this mitigates |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Technical Approach](#technical-approach) | Implementation strategy |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Status changes |

---

## Summary

The tier renumbering (Option A) moves Memory-Keeper from T4 to T3, making it available to more agents. While the MCP-002 key namespace standard (`jerry/{project}/{entity-type}/{entity-id}`) provides governance, there is no runtime mechanism to detect or prevent key collisions when two agents write to the same key in concurrent sessions.

This enabler implements defense-in-depth: collision detection and prevention for Memory-Keeper writes. It is **non-blocking** for the tier migration (tracked as FM-5 in the ADR FMEA, RPN=105) and can be implemented post-migration.

**Provisional ID:** EN-MK-COLLISION-DETECT (referenced in ADR-STORY015-001 FM-5)

**Skills informing this enabler:**
- `/eng-team` (eng-backend): Implementation of collision detection mechanism
- `/eng-team` (eng-security): Security review of the MK write path

---

## Problem Statement

When two sessions run in parallel on the same project, both invoking agents with Memory-Keeper access, they may write to the same key (`jerry/{project}/research/{slug}`). The current behavior is last-write-wins with silent overwrite. The losing session's findings are discarded without notification.

**Current mitigation:** MCP-002 key namespace standard + agent-specific key patterns. Adequate for 7 T4 agents; may be insufficient as more agents gain MK access at T3+ under the new model.

**Target mitigation:** Write-time collision detection that warns or blocks when a key was modified by another session since the agent last read it (optimistic concurrency).

---

## Acceptance Criteria

### /eng-team (eng-backend)

- [ ] Memory-Keeper write operations check for concurrent modification
- [ ] Collision detected: agent receives clear error with the conflicting session's metadata
- [ ] Collision resolution options: overwrite (explicit), merge (if supported), abort
- [ ] No performance regression for non-conflicting writes (optimistic path)

### /eng-team (eng-security)

- [ ] Collision detection cannot be bypassed by crafting key patterns
- [ ] Error messages do not leak sensitive session data
- [ ] Audit trail: collisions are logged for post-hoc analysis

---

## Technical Approach

Implement optimistic concurrency control for Memory-Keeper writes. On write, check if the key's last-modified timestamp differs from the value read at session start. If a collision is detected, return an error with the conflicting session's metadata and offer overwrite, merge, or abort options.

---

## Children (Tasks)

| ID | Title | Status | Owner | Skill |
|----|-------|--------|-------|-------|
| TASK-001 | Feasibility spike: evaluate optimistic concurrency for MK (research before committing to design) | pending | -- | /problem-solving |
| TASK-002 | Design collision detection mechanism based on spike findings | pending | -- | /eng-team |
| TASK-003 | Implement write-time collision check in MK integration | pending | -- | /eng-team |
| TASK-004 | Security review of collision detection | pending | -- | /eng-team |
| TASK-005 | Update MCP-002 governance standard with collision handling guidance | pending | -- | /eng-team |
| TASK-006 | C3 adversarial review of MCP-002 update (AE-002 mandatory for rule file changes) | pending | -- | /adversary |

---

## Related Items

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Informed By | STORY-015 | ADR FMEA FM-5 (RPN=105) identifies collision risk |
| Informed By | STORY-018 | Migration increases the number of MK-eligible agents |
| Non-blocking | STORY-018 | Migration can proceed without this enabler |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-28 | adam.nowak | pending | Created -- post-migration enabler from ADR FM-5 |
