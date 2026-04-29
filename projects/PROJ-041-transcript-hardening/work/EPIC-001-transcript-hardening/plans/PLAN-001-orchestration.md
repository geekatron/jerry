# PLAN-001: Orchestration Plan — `/transcript` Skill Hardening

> Eight-phase orchestration coordinating all 37 work items across 7 skills (`/orchestration`, `/problem-solving`, `/eng-team`, `/red-team`, `/user-experience`, `/diataxis`, `/adversary`, `/worktracker`). Authored by EN-007. The execution playbook for EPIC-001.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Phase Overview](#phase-overview) | All 8 phases at a glance |
| [Phase 0: Project Scaffolding](#phase-0-project-scaffolding) | Already complete — recorded for traceability |
| [Phase 1: Discovery in Parallel](#phase-1-discovery-in-parallel) | UX + red-team threat model + research |
| [Phase 2: Architecture and Governance](#phase-2-architecture-and-governance) | DDD scaffolding + ADRs |
| [Phase 3: Quick-Win Track (Parallel)](#phase-3-quick-win-track-parallel) | Mindmap fixes + ADR-007 vendoring |
| [Phase 4: Implementation](#phase-4-implementation) | Validators + CLI + integration |
| [Phase 5: Security Review](#phase-5-security-review) | Manual code review + red-team validation |
| [Phase 6: Schema Extensions](#phase-6-schema-extensions) | Additive schema work |
| [Phase 7: Documentation](#phase-7-documentation) | /diataxis pass |
| [Phase 8: Final Acceptance](#phase-8-final-acceptance) | C4 tournament |
| [Sync Barriers and Quality Gates](#sync-barriers-and-quality-gates) | Phase boundary protocol |
| [Cross-Skill Handoff Protocol](#cross-skill-handoff-protocol) | How agents pass context |
| [Failure Modes and Escalation](#failure-modes-and-escalation) | What happens when things go wrong |

---

## Phase Overview

| Phase | Name | Skills | Key Entities | Sync Barrier? | Adversary Gate |
|-------|------|--------|--------------|---------------|----------------|
| 0 | Project Scaffolding | /worktracker | (this plan; already done) | — | — |
| 1 | Discovery in Parallel | /problem-solving, /red-team, /user-experience | EN-004 (Phase 1), EN-005, research handoffs | YES (entry to Phase 2) | C4 ≥0.95 on syntheses |
| 2 | Architecture and Governance | /eng-team, /problem-solving, /worktracker | EN-001, FEAT-002 (5 bugs), DEC-001..005 ADRs | YES (entry to Phase 3) | C4 ≥0.95 on architecture + ADR amendments |
| 3 | Quick-Win Track (Parallel with Phase 4) | /eng-team, /worktracker | FEAT-005 (BUG-006, BUG-007), FEAT-001 STORY-001 | NO (independent ship) | C4 ≥0.95 per Bug |
| 4 | Implementation | /eng-team, /problem-solving, /worktracker | EN-002, EN-003, STORY-003..STORY-008 | YES (entry to Phase 5) | C4 ≥0.95 per Story |
| 5 | Security Review | /eng-team (eng-security, eng-reviewer), /red-team (Phase 4 validation) | EN-004 Phase 4 deliverables, eng-security review pass | YES (entry to Phase 6) | C4 ≥0.95 on review + remediation |
| 6 | Schema Extensions | /eng-team, /worktracker | FEAT-004 (4 stories), FEAT-001 STORY-002 (ADR-007 promotion) | YES (entry to Phase 7) | C4 ≥0.95 per Story |
| 7 | Documentation | /diataxis | EN-006 (8 docs across 4 quadrants) | YES (entry to Phase 8) | C4 ≥0.95 on doc set |
| 8 | Final Acceptance | /adversary | EN-008 final tournament | — | C4 ≥0.95 on Epic |

---

## Phase 0: Project Scaffolding

**Status:** completed by Claude during 2026-04-28 scaffolding session.

**Deliverables (this artifact set):**
- PLAN.md, WORKTRACKER.md, projects/README.md registry update
- 1 Epic + 5 Features + 5 cross-cutting Enablers + 16 Stories + 7 Bugs + 3 in-feature Enablers = 37 entities
- This orchestration plan

---

## Phase 1: Discovery in Parallel

**Goal:** Surface findings that must inform Phase 2 design — security threat model, UX angles, and research synthesis. Run in parallel; sync at Phase 2 entry.

| Agent | Task | Deliverable | Path |
|-------|------|-------------|------|
| `red-lead` | Author RoE/scope document for /red-team engagement | scope.md | `work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/` |
| `red-recon` | Reconnaissance of existing surface | recon-existing-surface.md | (same) |
| `red-recon` | Reconnaissance of planned new surface (per FEAT-003 design draft) | recon-new-surface.md | (same) |
| `red-vuln` | STRIDE threat model | stride-threat-model.md | (same) |
| `red-vuln` | Attack path analysis | attack-paths.md | (same) |
| `red-reporter` | Phase 1 handoff to /eng-team | phase-1-handoff-to-eng-team.md | (same) |
| `ux-orchestrator` | Route to JTBD/HEART/heuristic/inclusive/behavior sub-skills | (multiple) | `work/EPIC-001-transcript-hardening/EN-005-user-experience-exploration/` |
| `ux-jtbd-analyst` | Job map for `/transcript` consumers | jtbd-job-map.md | (same) |
| `ux-heart-analyst` | HEART dashboard spec | heart-dashboard.md | (same) |
| `ux-heuristic-evaluator` | CLI surface heuristic eval (per FEAT-003 design draft) | heuristic-findings.md | (same) |
| `ux-inclusive-evaluator` | Persona spectrum audit | inclusive-audit.md | (same) |
| `ux-behavior-diagnostician` | B=MAP analysis on agent-runs-validators bottleneck | behavior-diagnosis.md | (same) |
| `ps-researcher` | Codebase recon: existing /transcript code + author's gist analysis | research-existing-state.md | `work/EPIC-001-transcript-hardening/research/` |
| `ps-synthesizer` | Cross-pollinate findings (red-team + UX + research) | phase-1-synthesis.md | `work/EPIC-001-transcript-hardening/research/` |
| `adv-executor` + `adv-scorer` | C4 review on phase-1-synthesis.md | adversary-phase-1.md | (same) |

**Sync barrier (entry to Phase 2):**
- All Phase 1 deliverables exist and pass adversary review.
- EPIC-001 scope optionally adjusted based on EN-005 synthesis (Risk R-06 mitigation).
- Phase 1 handoff to /eng-team transmitted with success criteria.

---

## Phase 2: Architecture and Governance

**Goal:** Resolve the 5 framework-internal contradictions and produce the design ADRs (DEC-001..DEC-005) so Phase 4 implements against locked interfaces.

| Agent | Task | Entity Coverage |
|-------|------|----------------|
| `ps-architect` | Author DEC-001 (validation as operation within /transcript BC) | EN-001 |
| `ps-architect` | Author DEC-002 (hexagonal with 4 layers) | EN-001 |
| `ps-architect` | Author DEC-003 (SubprocessSandbox separate port) | EN-001, EN-003 |
| `ps-architect` | Author DEC-004 (gist as reference, not literal port) | EN-001 |
| `ps-architect` | Author DEC-005 (validators in src/jerry/ vs skills/scripts/) | EN-001 |
| `eng-architect` | Threat-informed architecture review on DEC-001..005 | EN-001 |
| `eng-lead` | Implementation plan + dependency governance | (Phase 4 prep) |
| `worktracker` (BUG fixers) | Resolve 5 contradictions per recommended resolutions in FEAT-002 | BUG-001..BUG-005 |
| `ps-architect` | Update affected ADRs (ADR-001, ADR-002, ADR-003, ADR-007) per BUG resolutions | (cross-references) |
| `ps-critic` + `adv-executor` | C4 review on architecture + ADR amendments | EN-007 gate |

**Sync barrier (entry to Phase 3):**
- DEC-001..005 authored, reviewed, approved.
- All 5 FEAT-002 Bugs status `completed` with delivery evidence.
- `eng-architect` review: PASS.
- Adversary C4 ≥0.95 on architecture + amendments.

---

## Phase 3: Quick-Win Track (Parallel with Phase 4)

**Goal:** Land FEAT-005 (mindmap fixes) and FEAT-001 STORY-001 (vendor ADR-007) early. These are unblocked by Phase 2 sync barrier and ship independently of Phase 4.

| Agent | Task | Entity Coverage |
|-------|------|----------------|
| `eng-backend` | Update ts-mindmap-mermaid agent prompt to HTML-escape brackets | BUG-006 |
| `eng-qa` | Regression test: render bracket-canonical golden via mmdc | BUG-006 |
| `eng-reviewer` | BUG-007 decision: render capability vs scope-honest claim | BUG-007 |
| `eng-backend` | Apply BUG-007 decision (Option A or B) | BUG-007 |
| (chore) | Cross-repo file copy ADR-007 from jerry-core | STORY-001 |
| `eng-backend` | Update SKILL.md, ts-formatter.md, etc. cross-references | STORY-001 |
| `eng-qa` | CI check for SKILL.md ADR cross-reference resolution | STORY-001 |
| `adv-executor` | C4 ≥0.95 per item before merge | (each item) |

**No sync barrier** — these merge independently of Phase 4 progress. Each ships to main as a standalone PR.

---

## Phase 4: Implementation

**Goal:** Build the validators, CLI, and integration. TDD R/G/R discipline. SubprocessSandbox is security-critical and gated by Phase 5 review.

| Phase 4.A — Foundation (sequential within phase) | Agent | Entity Coverage |
|---|---|---|
| Test harness + golden packets | eng-qa | EN-002 |
| SubprocessSandbox port + adapter | eng-infra + eng-security | EN-003 |
| `red-team` validates sandbox boundary (Phase 4 verification of EN-004) | red-exploit | EN-004 Phase 4 |

| Phase 4.B — Validators (parallel after 4.A) | Agent | Entity Coverage |
|---|---|---|
| FILE-* validators (TDD R/G/R) | eng-backend | STORY-003 |
| CONTENT-* validators (TDD R/G/R) | eng-backend | STORY-004 |
| ANCHOR-* validators (TDD R/G/R) | eng-backend | STORY-005 |
| SCHEMA-* validators (TDD R/G/R) | eng-backend | STORY-006 |
| Adversary C4 review per family | adv-executor | (each story) |

| Phase 4.C — Integration (sequential after 4.B) | Agent | Entity Coverage |
|---|---|---|
| `jerry transcript verify` CLI | eng-backend | STORY-007 |
| `jerry transcript update-anchors` CLI | eng-backend | STORY-008 |
| Wire verify into ts-formatter post-render hook | eng-backend + eng-reviewer | STORY-009 |
| Wire update-anchors into ts-formatter write pipeline | eng-backend + eng-reviewer | STORY-010 |
| Update ts-critic-extension.md | eng-backend | STORY-011 |
| CI workflow for validators | eng-devsecops | STORY-012 |

**Sync barrier (entry to Phase 5):**
- All Phase 4 stories status `completed` with test runs and adversary scores in History.
- Coverage gate ≥90% (≥95% on subprocess sandbox).
- Reproduction: validators correctly identify the audit's iter-9 drift case.

---

## Phase 5: Security Review

**Goal:** Manual security code review, eng-team final-gate review, red-team Phase 4 validation closure.

| Agent | Task |
|-------|------|
| `eng-security` | Manual secure code review on validation/ module |
| `eng-reviewer` | Final-gate review (architecture compliance, security standards, test coverage) per H-13 |
| `red-exploit` | Final exploit attempts against integrated system |
| `red-reporter` | Engagement report (closure of EN-004) |
| `adv-executor` | C4 ≥0.95 review on review pass |

**Sync barrier (entry to Phase 6):**
- All Critical findings remediated.
- Major findings either remediated or explicitly accepted with rationale.
- eng-reviewer: PASS.

---

## Phase 6: Schema Extensions

**Goal:** Land FEAT-004 schema additions and FEAT-001 STORY-002 (ADR-007 promotion to ACCEPTED) — now safe because contradictions are resolved (Phase 2) and validators encode rules (Phase 4).

| Agent | Task | Entity Coverage |
|-------|------|----------------|
| `eng-backend` | editorial_conventions block | STORY-013 |
| `eng-backend` | arithmetic_invariants for stat blocks | STORY-014 |
| `eng-backend` | discussions[] entity type | STORY-015 |
| `eng-backend` | provenance.audit_basis | STORY-016 |
| `ps-architect` | ADR amendments per Story acceptance | (multiple) |
| `eng-backend` | Promote ADR-007 PROPOSED → ACCEPTED | STORY-002 |
| `adv-executor` | C4 ≥0.95 per story + on promotion | (each) |

**Sync barrier (entry to Phase 7):**
- All FEAT-004 stories closed.
- ADR-007 status ACCEPTED.
- All schemas validate; golden packets demonstrate new shapes.

---

## Phase 7: Documentation

**Goal:** /diataxis pass — 8 docs across 4 quadrants per EN-006.

| Agent | Task | Entity Coverage |
|-------|------|----------------|
| `diataxis-classifier` | Classify each planned doc | EN-006 |
| `diataxis-tutorial` | first-validation tutorial | EN-006 |
| `diataxis-howto` × 2 | repair-drift, ci-integration | EN-006 |
| `diataxis-reference` × 3 | validation rules, CLI, schema | EN-006 |
| `diataxis-explanation` × 2 | substrate-coupling, bounded-context | EN-006 |
| `diataxis-auditor` | Quadrant audit on doc set | EN-006 |
| `eng-reviewer` | Confirm docs match implementation | EN-006 |
| `adv-executor` | C4 ≥0.95 on doc set | EN-006 |

**Sync barrier (entry to Phase 8):**
- All 8 docs written, classified, and audited.
- Doc set surfaced from SKILL.md References section.

---

## Phase 8: Final Acceptance

**Goal:** EN-008 final adversary tournament. EPIC-001 closes if and only if this phase passes.

| Agent | Task |
|-------|------|
| `adv-selector` | Select C4 strategy set (all 10) |
| `adv-executor` | Execute all 10 strategies against merged Epic deliverable |
| `adv-scorer` | S-014 LLM-as-Judge composite + dimension scores |
| (Fresh-context) `adv-executor` + `adv-scorer` | FC-M-001 second-reviewer independent run |
| `adv-executor` | Reproduce audit author's 9-iter scenario; verify ≥0.95 reachable |
| `red-reporter` | Close issue #273 with summary comment |
| `worktracker` | Move EPIC-001 status to completed (with delivery evidence) |

**No further sync barrier.** Pass = Epic done.

---

## Sync Barriers and Quality Gates

| Barrier | Entry Conditions | Exit Conditions |
|---------|-----------------|-----------------|
| Phase 1 → 2 | Phase 1 syntheses delivered | C4 ≥0.95 on synthesis; scope optionally adjusted |
| Phase 2 → 3 | DEC-001..005 + 5 BUGs closed | C4 ≥0.95; eng-architect PASS |
| Phase 4 → 5 | All Phase 4 stories closed; coverage thresholds met | Iter-9 audit case mechanically caught |
| Phase 5 → 6 | All Critical findings remediated | eng-reviewer PASS |
| Phase 6 → 7 | All FEAT-004 stories + STORY-002 closed | All schemas validate |
| Phase 7 → 8 | All 8 docs written, audited | diataxis-auditor PASS |
| Phase 8 → DONE | Tournament composite ≥0.95; second-reviewer ≥0.95; reproduction succeeds | EPIC-001 closes; #273 closes |

**Universal gate:** No phase advances without `/adversary` C4 ≥0.95. Plateau detection (delta < 0.01 for 3 iterations) triggers AE-006 mandatory human escalation at C3+.

---

## Cross-Skill Handoff Protocol

Per `agent-development-standards.md` Handoff Protocol v2 (`docs/schemas/handoff-v2.schema.json`). Required fields per handoff:

| Field | Purpose |
|-------|---------|
| `from_agent`, `to_agent` | Identity |
| `task` | What's delegated |
| `success_criteria` | Verifiable per RV-01..04 |
| `artifacts` | File paths (existence-validated per HD-M-002) |
| `key_findings` | 3-5 bullets per CB-04 |
| `blockers` | Persistent items prefixed `[PERSISTENT]` |
| `confidence` | 0.0-1.0 calibrated |
| `criticality` | C3+ for this Epic |

Critical handoffs in this plan:

| Handoff | Stage |
|---------|-------|
| red-team Phase 1 → eng-team | End of Phase 1 — threat findings inform Phase 2 design |
| ps-architect → eng-architect | Phase 2 — DEC-001..005 reviewed before implementation |
| eng-team Phase 4 → red-team Phase 4 | Implementation completion enables exploit attempts |
| eng-team Phase 5 → diataxis Phase 7 | Implementation locks before docs |

---

## Failure Modes and Escalation

| Failure | Detection | Escalation |
|---------|-----------|------------|
| Plateau at <0.95 in any phase | adv-scorer reports delta <0.01 across 3 iters | AE-006 mandatory human escalation; phase pauses for re-scoping |
| red-team finds Critical post-implementation | red-exploit log + red-reporter | Phase 5 cannot exit until remediated |
| UX synthesis introduces scope-changing finding | EN-005 synthesis report | Phase 1 sync barrier check; Epic re-scope at user discretion |
| Coverage drops below threshold in CI | STORY-012 workflow | Phase 4 cannot exit; offending PR reverted |
| C4 governance change blocked by unresolved contradiction | STORY-002 acceptance check | Phase 6 cannot proceed; loop back to Phase 2 |

---

## State Persistence

`orch-tracker` maintains state at `work/EPIC-001-transcript-hardening/orchestration/state.md` (initialized by orch-planner at Phase 0 close). Records phase entry/exit timestamps, gate scores, sync-barrier passage, and active blockers.

`orch-synthesizer` runs at every phase exit to consolidate findings across parallel tracks (especially Phase 1's red-team + UX + research streams).

---

## References

| Source | Path |
|--------|------|
| Quality SSOT | `.context/rules/quality-enforcement.md` |
| Agent dev standards | `.context/rules/agent-development-standards.md` |
| Routing standards | `.context/rules/agent-routing-standards.md` |
| /orchestration skill | `skills/orchestration/SKILL.md` |
| /adversary skill | `skills/adversary/SKILL.md` |
| Worktracker SSOT | `skills/worktracker/rules/` |
| Project plan | `projects/PROJ-041-transcript-hardening/PLAN.md` |
| Epic | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EPIC-001-transcript-hardening.md` |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | created | 8-phase plan authored as part of EN-007. Awaits orch-planner/orch-tracker/orch-synthesizer agent invocations during Phase 0 close to instantiate state. |
