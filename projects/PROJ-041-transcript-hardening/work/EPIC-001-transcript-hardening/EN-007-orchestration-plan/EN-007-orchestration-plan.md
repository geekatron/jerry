# EN-007: `/orchestration` plan + sync barriers

> **Type:** enabler
> **Enabler Type:** architecture
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** EPIC-001
> **Owner:** adam.nowak
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Enabler delivers |
| [Technical Approach](#technical-approach) | Plan structure and authoring approach |
| [Pointer to Plan](#pointer-to-plan) | Where the orchestration plan lives |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

Author the orchestration plan that coordinates all 37 work items across 7 skills, with explicit phase definitions, sync barriers, `/adversary` C4 ≥0.95 quality gates between phases, and criticality propagation. This Enabler is **Phase 0** of the project — it executes before any other work and produces the playbook the rest of the Epic follows.

The plan itself is large enough to warrant its own document and is captured at the path below. This Enabler entity tracks its authoring as a single deliverable.

---

## Technical Approach

Use `/orchestration` skill agents (orch-planner, orch-tracker, orch-synthesizer) to author and run the plan. orch-planner produces the 8-phase plan with named agents, deliverables, sync barriers, and `/adversary` C4 ≥0.95 quality gates. orch-tracker maintains workflow state at `work/EPIC-001-transcript-hardening/orchestration/state.md` across sessions. orch-synthesizer runs at every phase exit to consolidate findings across parallel tracks. The Pointer to Plan section below references the actual plan artifact.

---

## Pointer to Plan

| Plan | Path |
|------|------|
| Orchestration plan | [`plans/PLAN-001-orchestration.md`](../plans/PLAN-001-orchestration.md) |

The plan covers: 8 phases (0 through 8) — Phase 0 (this Enabler), Phase 1 (parallel discovery), Phase 2 (architecture), Phase 3 (early-land quick-wins), Phase 4 (implementation), Phase 5 (security review), Phase 6 (schema extensions), Phase 7 (documentation), Phase 8 (final acceptance). Each phase has named agents, deliverables, sync barriers, and quality gates.

---

## Acceptance Criteria

- [ ] `plans/PLAN-001-orchestration.md` exists and is complete (all 8 phases captured).
- [ ] Each phase lists the agents invoked, the entity IDs the phase covers, sync barriers, and the `/adversary` gate threshold.
- [ ] Phase entry/exit criteria are explicit (no ambiguity about when a phase is done).
- [ ] Cross-skill handoffs documented per the [Handoff Protocol](../../../../skills/problem-solving/) standard (artifact paths, key findings, success criteria).
- [ ] Plan is reviewable: a person reading it can execute the project without needing additional context.
- [ ] `orch-planner` invoked to produce the plan; `orch-tracker` configured for state persistence; `orch-synthesizer` registered for cross-pollination at sync barriers.
- [ ] Plan registered in this project's WORKTRACKER.md under EN-007.
- [ ] `/adversary` C4 ≥0.95 review on the plan.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Author plans/PLAN-001-orchestration.md (full 8-phase plan) | pending |
| TASK-002 | Configure orch-tracker state schema for this Epic | pending |
| TASK-003 | Run orch-planner self-review | pending |
| TASK-004 | Run /adversary C4 review on the plan | pending |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001](../EPIC-001-transcript-hardening.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocks | All other entities | The plan defines the execution sequence |

### Source

- User direction: "We will have to spend extra time ensure that we build out the appropriate /orchestration plan"

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Enabler created. Plan to be authored as Task #7 of project scaffolding (next). |
