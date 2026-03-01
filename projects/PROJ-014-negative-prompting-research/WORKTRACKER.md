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
| Progress | Phases 1-6 COMPLETE, ADR-001 core DONE — ADR-002/003/004 + post-impl + validation pending (EPIC-005, EPIC-006) |

## Work Items

> **Quality Model:** Per-agent adversary gates (adv-selector → adv-executor → adv-scorer) at every creator output. 23 total gates: 17 agent + 5 barrier synthesis + 1 C4 tournament. Every task includes its per-agent /adversary C4 gate (>= 0.95, max 5 iterations).

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| EPIC-001 | Epic | Literature Research & Evidence Gathering | DONE | — |
| EPIC-002 | Epic | Comparative Analysis & Taxonomy | DONE | — |
| EPIC-003 | Epic | Jerry Framework Application | DONE | — |
| EPIC-004 | Epic | Final Synthesis & Recommendations | DONE | — |
| TASK-001 | Task | Phase 1: Academic Literature Research (25+ sources) + per-agent /adversary C4 gate | DONE (0.950, 5 iter) | EPIC-001 |
| TASK-002 | Task | Phase 1: Industry & Practitioner Research (25+ sources) + per-agent /adversary C4 gate | DONE (0.9325, 5 iter, user-accepted) | EPIC-001 |
| TASK-003 | Task | Phase 1: Context7 Library Documentation Research + per-agent /adversary C4 gate | DONE (0.935, 6 iter, user-accepted) | EPIC-001 |
| TASK-004 | Task | Barrier 1: Research cross-pollination (gated inputs) + /adversary C4 on synthesis | DONE (0.953, 4 iter) | TASK-001, TASK-002, TASK-003 |
| TASK-005 | Task | Phase 2: Claim Validation (60% hallucination) + per-agent /adversary C4 gate | DONE (0.959, 4 iter) | EPIC-001 |
| TASK-006 | Task | Phase 2: Comparative Effectiveness Analysis (5 dimensions) + per-agent /adversary C4 gate | DONE (0.933, 5 iter, max-iterations) | EPIC-001 |
| TASK-007 | Task | Barrier 2: Analysis cross-pollination (gated inputs) + /adversary C4 on synthesis | DONE (0.950, 3 iter) | TASK-005, TASK-006 |
| TASK-008 | Task | Phase 3: Negative Prompting Taxonomy & Pattern Catalog + per-agent /adversary C4 gates | DONE (0.957, 3 iter) | EPIC-002 |
| TASK-009 | Task | Barrier 3: Taxonomy quality gate — /adversary C4 on cross-artifact coherence | DONE (0.957, 3 iter) | TASK-008 |
| TASK-010 | Task | Phase 4: Jerry Skills Update Analysis + per-agent /adversary C4 gate | DONE (0.951, 2 iter) — Artifact: `orchestration/neg-prompting-20260227-001/phase-4/skills-update-analysis.md` | EPIC-003 |
| TASK-011 | Task | Phase 4: Jerry Agents Update Analysis + per-agent /adversary C4 gate | DONE (0.951, 3 iter) — Artifact: `orchestration/neg-prompting-20260227-001/phase-4/agents-update-analysis.md` | EPIC-003 |
| TASK-012 | Task | Phase 4: Jerry Rules Update Analysis + per-agent /adversary C4 gate (AE-002) | DONE (0.953, 3 iter) — Artifact: `orchestration/neg-prompting-20260227-001/phase-4/rules-update-analysis.md` | EPIC-003 |
| TASK-013 | Task | Phase 4: Jerry Patterns Update Analysis + per-agent /adversary C4 gate | DONE (0.950, 5 iter) — Artifact: `orchestration/neg-prompting-20260227-001/phase-4/patterns-update-analysis.md` | EPIC-003 |
| TASK-014 | Task | Phase 4: Jerry Templates Update Analysis + per-agent /adversary C4 gate | DONE (0.955, 3 iter) — Artifact: `orchestration/neg-prompting-20260227-001/phase-4/templates-update-analysis.md` | EPIC-003 |
| TASK-015 | Task | Barrier 4: Application cross-pollination (gated inputs) + /adversary C4 on synthesis | DONE (0.950, 4 iter) — Artifact: `orchestration/neg-prompting-20260227-001/barrier-4/synthesis.md` | TASK-010 through TASK-014 |
| TASK-016 | Task | Phase 5: Implementation Planning (4 ADRs) + per-agent /adversary C4 gates | DONE — ADR-001 (0.952, 4 iter), ADR-002 (0.951, 3 iter), ADR-003 (0.957, 4 iter), ADR-004 (0.955, 3 iter) | EPIC-003 |
| TASK-017 | Task | Barrier 5: Implementation quality gate — /adversary C4 on cross-ADR coherence | DONE (0.956, 2 iter) — Artifact: `orchestration/neg-prompting-20260227-001/barrier-5/synthesis.md` | TASK-016 |
| TASK-018 | Task | Phase 6: Final Synthesis & Implementation Roadmap + per-agent /adversary C4 gates | DONE (0.954, 2 iter) — Artifact: `orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md` | EPIC-004 |
| TASK-019 | Task | Phase 6: /adversary C4 tournament (all 10 strategies, >= 0.95, max 5 iter) | DONE (0.954, 2 iter) — Tournament report: `orchestration/neg-prompting-20260227-001/phase-6/adversary-tournament-i2.md` | TASK-018 |
| TASK-020 | Task | Documentation & commit | DONE | TASK-019 |
| EPIC-005 | Epic | ADR Implementation | IN PROGRESS | — |
| FEAT-001 | Feature | Implement ADR-001: NPT-014 Elimination | IN PROGRESS | EPIC-005 |
| TASK-021 | Task | Phase 1: Baseline capture — identify all NPT-014 instances + quality metrics | DONE — 47 NPT-014, 28 NPT-009, 36 NPT-013 identified | FEAT-001 |
| TASK-022 | Task | Phase 2: Rule files — upgrade NPT-014 to NPT-009/NPT-013 in .context/rules/ | DONE — 8 instances across 7 files upgraded | FEAT-001 |
| TASK-023 | Task | Phase 3: Agent definitions — upgrade forbidden_actions in skills/*/agents/ | DONE — 28 agent files upgraded (Phase 3A batch + Phase 3B individual) | FEAT-001 |
| TASK-024 | Task | Phase 4: SKILL.md files — upgrade "Do NOT use when:" sections | DONE — 4 instances across 2 SKILL.md files upgraded | FEAT-001 |
| TASK-030 | Task | Run NPT-014 diagnostic scan on all modified files | PENDING | FEAT-001 |
| TASK-031 | Task | Update Phase 1 inventory with completion status | PENDING | FEAT-001 |
| TASK-032 | Task | Update ADR-001 status to ACCEPTED (requires user approval per P-020) | PENDING | FEAT-001 |
| FEAT-002 | Feature | Implement ADR-002: Constitutional Triplet and High-Framing Upgrades | PENDING | EPIC-005 |
| TASK-033 | Task | Phase 5A: Update guardrails template to NPT-009 format | PENDING | FEAT-002 |
| TASK-034 | Task | Phase 5A: Add forbidden_action_format field to governance schema | PENDING | FEAT-002 |
| TASK-035 | Task | Phase 5B: Full adoption or contingency (blocked by TASK-025 A/B testing) | PENDING | FEAT-002 |
| FEAT-003 | Feature | Implement ADR-003: Routing Disambiguation Standard | PENDING | EPIC-005 |
| TASK-036 | Task | Component A: Add routing disambiguation sections to all 13 skills | PENDING | FEAT-003 |
| TASK-037 | Task | Component B: Framing vocabulary standardization (blocked by TASK-025) | PENDING | FEAT-003 |
| FEAT-004 | Feature | Implement ADR-004: Compaction Resilience | PENDING | EPIC-005 |
| TASK-038 | Task | Decision 1: PG-004 Compaction testing requirement | PENDING | FEAT-004 |
| TASK-039 | Task | Decision 2: Add L2-REINJECT markers for H-04 and H-32 | PENDING | FEAT-004 |
| TASK-040 | Task | Decision 3: T-004 Failure mode documentation in templates | PENDING | FEAT-004 |
| EPIC-006 | Epic | Validation & Publication | PENDING | — |
| TASK-025 | Task | A/B Testing: Positive vs Negative vs Negative with Consequence | PENDING | EPIC-006 |
| TASK-026 | Task | Write Jerry MD Docs Site Article | PENDING | EPIC-006 |
| TASK-027 | Task | Write Medium Article | PENDING | EPIC-006 |
| TASK-028 | Task | Write Tweet and Cross-Post Medium + Jerry Articles | PENDING | EPIC-006 |
| TASK-029 | Task | Slack Message Announcement | PENDING | EPIC-006 |

---

*All paths relative to `projects/PROJ-014-negative-prompting-research/`*
