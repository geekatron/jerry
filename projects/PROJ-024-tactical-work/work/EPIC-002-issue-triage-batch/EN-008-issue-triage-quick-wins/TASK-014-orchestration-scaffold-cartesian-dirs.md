# TASK-014: Orchestration Scaffold Cartesian Product Dirs

> **Type:** task
> **Status:** completed
> **Priority:** low
> **Created:** 2026-03-31
> **Completed:** 2026-03-31
> **Parent:** EN-008
> **GitHub Issue:** [#53](https://github.com/geekatron/jerry/issues/53)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |
| [Evidence](#evidence) | Delivery evidence |
| [Related Items](#related-items) | Hierarchy |
| [History](#history) | Status changes |

---

## Summary

Orchestration scaffolding used bash brace expansion (`{a,b,c}`) to create directory structures, producing a cartesian product of hundreds of empty directories that agents never write to (GH #53). Add a guardrail to orch-planner forbidding brace-expansion scaffolding in favour of on-demand `mkdir -p` at write time with `phase-N-{phase-name}` naming.

> **Entity file recreated 2026-08-05** during audit remediation (finding E-002) — the work was delivered 2026-03-31 but tracked only as a manifest row with no entity file.

---

## Acceptance Criteria

- [x] orch-planner agent definition contains a SCAFFOLD VIOLATION guardrail forbidding bash brace expansion for directory creation, prescribing on-demand `mkdir -p` and `phase-N-{phase-name}` naming
- [x] GH issue #53 closed

---

## Evidence

| Deliverable | Type | Link |
|-------------|------|------|
| Commit `077750b9` — "feat(EPIC-002): execute Phase 0-1" (2026-03-31), adds SCAFFOLD VIOLATION entry to `skills/orchestration/agents/orch-planner.md` (cites GH #53) | Commit | [077750b9](https://github.com/geekatron/jerry/commit/077750b91aed7ee997e8ed9e8622c7363c81eb24) |
| Guardrail present in `skills/orchestration/agents/orch-planner.md` ("SCAFFOLD VIOLATION: DO NOT use bash brace expansion...") | File | verified in working tree 2026-08-05 |

---

## Related Items

- Parent: [EN-008: Issue Triage Quick Wins](./EN-008-issue-triage-quick-wins.md)
- Coordinating epic: [EPIC-002: Issue Triage Batch](../EPIC-002-issue-triage-batch.md) (Phase 0)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-03-31 | completed | Delivered via commit 077750b9 (EPIC-002 Phase 0); GH #53 closed |
| 2026-08-05 | completed | Entity file recreated per audit finding E-002; re-parented under EN-008 (E-014) |
