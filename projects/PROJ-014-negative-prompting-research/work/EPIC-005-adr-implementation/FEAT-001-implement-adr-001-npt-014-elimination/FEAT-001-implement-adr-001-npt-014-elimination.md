# FEAT-001: Implement ADR-001: NPT-014 Elimination

> **Type:** feature
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-28
> **Completed:** 2026-02-28
> **Parent:** EPIC-005
> **Owner:** Claude

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature description and value |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children Stories/Enablers](#children-storiesenablers) | Task inventory |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Dependencies and links |
| [History](#history) | Status changes |

---

## Summary

Upgrade all 47 bare prohibition instances (NPT-014) to structured negation patterns (NPT-009/NPT-013) across rule files, agent definitions, and SKILL.md files. Each upgrade adds consequence text and alternative/instead guidance to existing NEVER/MUST NOT/DO NOT statements.

**Value Proposition:**
- Improved LLM instruction-following compliance through consequence-aware prohibitions
- Consistent negative prompting quality across all Jerry framework artifacts

---

## Acceptance Criteria

### Definition of Done

- [x] All 47 NPT-014 instances identified in Phase 1 inventory are upgraded
- [x] Rule files (.context/rules/) upgraded — 8 instances across 7 files
- [x] Agent definitions (skills/*/agents/) upgraded — 28 files + 3 individual instances
- [x] SKILL.md files upgraded — 4 instances across 2 files
- [x] All changes committed and pushed

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Every NPT-014 instance has consequence text | [x] |
| AC-2 | Every NPT-014 instance has alternative/instead guidance where applicable | [x] |
| AC-3 | No behavioral changes — only structural upgrades to existing prohibitions | [x] |

---

## Children Stories/Enablers

### Task Inventory

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| TASK-021 | Phase 1: Baseline capture | completed | high |
| TASK-022 | Phase 2: Rule files upgrade | completed | high |
| TASK-023 | Phase 3: Agent definitions upgrade | completed | high |
| TASK-024 | Phase 4: SKILL.md files upgrade | completed | high |

### Task Links

- [TASK-021: Baseline capture](./TASK-021-baseline-capture.md)
- [TASK-022: Rule files upgrade](./TASK-022-rule-files-upgrade.md)
- [TASK-023: Agent definitions upgrade](./TASK-023-agent-definitions-upgrade.md)
- [TASK-024: SKILL-md-upgrade](./TASK-024-skill-md-upgrade.md)

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 4 |
| **Completed Tasks** | 4 |
| **Completion %** | 100% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-005: ADR Implementation](../EPIC-005-adr-implementation.md)

### References

- ADR-001: `orchestration/neg-prompting-20260227-001/phase-5/ADR-001-npt014-elimination.md`
- Implementation plan: `orchestration/adr001-implementation/ORCHESTRATION_PLAN.md`
- Phase 1 inventory: `orchestration/adr001-implementation/phase-1-npt014-inventory.md`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-28 | Claude | pending | Feature created |
| 2026-02-28 | Claude | in_progress | Phase 1 baseline capture started |
| 2026-02-28 | Claude | completed | All 4 phases delivered — 47 NPT-014 instances upgraded |
