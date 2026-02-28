# PROJ-014: Negative Prompting Research — Work Tracker

> Work decomposition and progress tracking for PROJ-014.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Project status overview |
| [Work Items](#work-items) | Entity tracking |

---

## Summary

| Metric | Value |
|--------|-------|
| Project | PROJ-014-negative-prompting-research |
| Status | IN PROGRESS |
| Created | 2026-02-27 |
| GitHub Issue | [#122](https://github.com/geekatron/jerry/issues/122) |
| Criticality | C4 (Critical) |
| Quality Threshold | >= 0.95 |
| Orchestration | `neg-prompting-20260227-001` |
| Progress | 15% (Phase 1 COMPLETE — 3/3 research tasks DONE, Barrier 1 ready) |

## Work Items

> **Quality Model:** Per-agent adversary gates (adv-selector → adv-executor → adv-scorer) at every creator output. 23 total gates: 17 agent + 5 barrier synthesis + 1 C4 tournament. Every task includes its per-agent /adversary C4 gate (>= 0.95, max 5 iterations).

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| EPIC-001 | Epic | Literature Research & Evidence Gathering | IN PROGRESS | — |
| EPIC-002 | Epic | Comparative Analysis & Taxonomy | NOT STARTED | — |
| EPIC-003 | Epic | Jerry Framework Application | NOT STARTED | — |
| EPIC-004 | Epic | Final Synthesis & Recommendations | NOT STARTED | — |
| TASK-001 | Task | Phase 1: Academic Literature Research (25+ sources) + per-agent /adversary C4 gate | DONE (0.950, 5 iter) | EPIC-001 |
| TASK-002 | Task | Phase 1: Industry & Practitioner Research (25+ sources) + per-agent /adversary C4 gate | DONE (0.9325, 5 iter, user-accepted) | EPIC-001 |
| TASK-003 | Task | Phase 1: Context7 Library Documentation Research + per-agent /adversary C4 gate | DONE (0.935, 6 iter, user-accepted) | EPIC-001 |
| TASK-004 | Task | Barrier 1: Research cross-pollination (gated inputs) + /adversary C4 on synthesis | NOT STARTED | TASK-001, TASK-002, TASK-003 |
| TASK-005 | Task | Phase 2: Claim Validation (60% hallucination) + per-agent /adversary C4 gate | NOT STARTED | EPIC-001 |
| TASK-006 | Task | Phase 2: Comparative Effectiveness Analysis (5 dimensions) + per-agent /adversary C4 gate | NOT STARTED | EPIC-001 |
| TASK-007 | Task | Barrier 2: Analysis cross-pollination (gated inputs) + /adversary C4 on synthesis | NOT STARTED | TASK-005, TASK-006 |
| TASK-008 | Task | Phase 3: Negative Prompting Taxonomy & Pattern Catalog + per-agent /adversary C4 gates | NOT STARTED | EPIC-002 |
| TASK-009 | Task | Barrier 3: Taxonomy quality gate — /adversary C4 on cross-artifact coherence | NOT STARTED | TASK-008 |
| TASK-010 | Task | Phase 4: Jerry Skills Update Analysis + per-agent /adversary C4 gate | NOT STARTED | EPIC-003 |
| TASK-011 | Task | Phase 4: Jerry Agents Update Analysis + per-agent /adversary C4 gate | NOT STARTED | EPIC-003 |
| TASK-012 | Task | Phase 4: Jerry Rules Update Analysis + per-agent /adversary C4 gate (AE-002) | NOT STARTED | EPIC-003 |
| TASK-013 | Task | Phase 4: Jerry Patterns Update Analysis + per-agent /adversary C4 gate | NOT STARTED | EPIC-003 |
| TASK-014 | Task | Phase 4: Jerry Templates Update Analysis + per-agent /adversary C4 gate | NOT STARTED | EPIC-003 |
| TASK-015 | Task | Barrier 4: Application cross-pollination (gated inputs) + /adversary C4 on synthesis | NOT STARTED | TASK-010 through TASK-014 |
| TASK-016 | Task | Phase 5: Implementation Planning (4 ADRs) + per-agent /adversary C4 gates | NOT STARTED | EPIC-003 |
| TASK-017 | Task | Barrier 5: Implementation quality gate — /adversary C4 on cross-ADR coherence | NOT STARTED | TASK-016 |
| TASK-018 | Task | Phase 6: Final Synthesis & Implementation Roadmap + per-agent /adversary C4 gates | NOT STARTED | EPIC-004 |
| TASK-019 | Task | Phase 6: /adversary C4 tournament (all 10 strategies, >= 0.95, max 5 iter) | NOT STARTED | TASK-018 |
| TASK-020 | Task | Documentation & commit | NOT STARTED | TASK-019 |

---

*All paths relative to `projects/PROJ-014-negative-prompting-research/`*
