# EN-009: CI Pipeline Optimization Tasks

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-08-05
> **Completed:** 2026-04-15
> **Parent:** EPIC-003
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Enabler scope and retroactive-container note |
| [Problem Statement](#problem-statement) | Why this enabler exists |
| [Technical Approach](#technical-approach) | How the two phases were delivered |
| [Children (Tasks)](#children-tasks) | 7 tasks re-parented from EPIC-003 |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [History](#history) | Status changes |

---

## Summary

Container enabler for the 7 CI pipeline optimization tasks originally created as direct children of EPIC-003 (Phase 1 security hardening + Phase 2 job consolidation). All 7 tasks were delivered on 2026-04-13 via commits `1dc99c75` (Phase 1) and `29e61240` (Phase 2), reducing the CI pipeline from 29 to ~19 jobs.

> **Retroactive container (2026-08-05):** created during audit remediation (audit finding E-014) to resolve the Epic→Task containment violation — the TASK template allows parents of Story/Bug/Enabler only, and the EPIC template allows children of Capability/Feature only. Per H-32 this enabler references the existing closed umbrella issue #252 (same as its sibling EN-006 and all child tasks) rather than a new dedicated GitHub issue; the completion date is backfilled per audit guidance (children delivered 2026-04-13; epic-level work concluded mid-April 2026). The `Created` date reflects the actual file-creation date; the `Completed` date reflects when the contained work was done.

**Technical Scope:**
- Phase 1 — Security hardening: uv migration, pip-audit scope, permission scoping, push-trigger restriction
- Phase 2 — Job consolidation: pip matrix removal, validation job consolidation, static-analysis merge

---

## Problem Statement

TASK-016 through TASK-022 declared `Parent: EPIC-003` directly, violating the containment rules (`TASK.md` allowed parents: Story, Bug, Enabler; `EPIC.md` allowed children: Capability, Feature). This enabler provides the valid Epic→Enabler→Task chain, mirroring how EN-006 already contains TASK-023 through TASK-034.

---

## Technical Approach

Phase 1 (security hardening: TASK-017/018/021/022) landed first as independent, parallelizable changes (commit `1dc99c75`); Phase 2 (consolidation: TASK-016/019/020) followed once the uv migration was in place (commit `29e61240`). All 7 tasks shipped in the same PR train on 2026-04-13.

---

## Children (Tasks)

| ID | Title | Status | Phase | Dependencies |
|----|-------|--------|-------|--------------|
| TASK-016 | Remove pip test matrix (8 jobs) | completed | 2 | TASK-017 |
| TASK-017 | Migrate lint, type-check, security to uv | completed | 1 | -- |
| TASK-018 | Fix pip-audit to scan full dependency tree | completed | 1 | -- |
| TASK-019 | Consolidate 6 validation jobs into 1 | completed | 2 | -- |
| TASK-020 | Merge lint + type-check into static-analysis | completed | 2 | TASK-017 |
| TASK-021 | Scope pull-requests:write to coverage-report only | completed | 1 | -- |
| TASK-022 | Restrict push trigger to protected branches only | completed | 1 | -- |

---

## Acceptance Criteria

- [x] All 7 CI optimization tasks (TASK-016..022) completed with their own ACs verified
- [x] CI pipeline reduced from 29 to ~19 jobs with zero H-05 violations remaining
- [x] Delivery evidenced in git history (commits `1dc99c75`, `29e61240`, 2026-04-13)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-05 | completed | Retroactive container created per audit finding E-014; TASK-016..022 re-parented from EPIC-003; completion backfilled to 2026-04-15 per audit guidance (delivery commits dated 2026-04-13) |
