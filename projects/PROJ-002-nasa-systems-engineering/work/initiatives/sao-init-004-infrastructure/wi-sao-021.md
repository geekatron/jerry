---
id: wi-sao-021
title: "Orchestration Folder Refactoring"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-004
children: []
depends_on: []
blocks: []
created: "2026-01-10"
started: "2026-01-10"
completed: "2026-01-10"
priority: "P1"
estimated_effort: "8h"
actual_effort: "8h"
entry_id: "sao-021"
source: "Cross-pollination pipeline architecture review"
commit: "fdc48ab"
token_estimate: 2000
---

# WI-SAO-021: Orchestration Folder Refactoring

> **Status:** ✅ COMPLETE
> **Started:** 2026-01-10
> **Completed:** 2026-01-10
> **Commit:** `fdc48ab` - refactor(orchestration): implement dynamic path scheme

---

## Description

Refactor orchestration output structure from flat `ps-pipeline/`, `nse-pipeline/`, `cross-pollination/` folders to hierarchical `orchestration/{workflow_id}/{pipeline_id}/{phase_id}/` scheme with **dynamic identifiers** (no hardcoded values).

---

## Rationale

Current flat structure doesn't scale for multiple orchestration runs. New structure provides:
1. Run isolation via dynamic `{workflow_id}`
2. Dynamic pipeline namespacing via `{pipeline_id}`
3. Phase progression visibility via `{phase_id}`
4. Centralized cross-pollination within each run
5. Extensibility for future pipelines

---

## Approved Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Identifier Strategy | Option 3: User-specified with semantic fallback | Balance of user control and defaults |
| Workflow ID Format | `{purpose}-{YYYYMMDD}-{NNN}` | Human-readable, sortable, unique |
| Pipeline Aliases | Default from skill, overridable | Flexibility with defaults |
| Test Migration | New versions + deprecated/ | Clean separation |

---

## Target Structure

```
orchestration/{workflow_id}/
├── {pipeline_alias_1}/{phase}/   # e.g., ps/phase-1-research/
├── {pipeline_alias_2}/{phase}/   # e.g., nse/phase-1-scope/
└── cross-pollination/
    └── barrier-{n}/
        ├── {source}-to-{target}/ # e.g., ps-to-nse/
```

---

## Acceptance Criteria (11/11 PASS)

1. ✅ Research complete - identifier strategy documented
2. ✅ Existing tests analyzed for hardcoded paths
3. ✅ Archive created at `archive/v_initial/`
4. ✅ Orchestration skill templates updated
5. ✅ Pipeline alias configuration documented
6. ✅ orch-planner agent updated
7. ✅ orch-tracker agent updated
8. ✅ New E2E tests created
9. ✅ Old E2E tests moved to deprecated/
10. ✅ E2E validation passes
11. ✅ All changes committed

---

## Migration Status

| Item | From | To | Status |
|------|------|-----|--------|
| ps-pipeline/ | project root | archive/v_initial/ | ✅ Complete |
| nse-pipeline/ | project root | archive/v_initial/ | ✅ Complete |
| cross-pollination/ | project root | archive/v_initial/ | ✅ Complete |
| Old E2E tests | tests/e2e/ | tests/e2e/deprecated/ | ✅ Complete |

---

## Tasks (19/19 COMPLETE)

**Phase 1: Research & Archive**
- [x] T-021.1 - T-021.4: Research and archive

**Phase 2: Template Updates**
- [x] T-021.5 - T-021.8: Template and skill updates

**Phase 3: Agent Updates**
- [x] T-021.9 - T-021.10: orch-planner and orch-tracker

**Phase 4: Test Migration**
- [x] T-021.11 - T-021.15: Test migration and v2 creation

**Phase 5: Validation**
- [x] T-021.16 - T-021.17: Validation

**Phase 6: Finalization**
- [x] T-021.18 - T-021.19: Commit (34 files changed, 1693 insertions, 185 deletions)

---

*Source: Extracted from WORKTRACKER.md lines 1662-1821*
