# EN-005: `/user-experience` JTBD + feedback exploration

> **Type:** enabler
> **Enabler Type:** exploration
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** EPIC-001
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Enabler delivers |
| [Technical Approach](#technical-approach) | Methodology overview |
| [Methodology](#methodology) | Sub-skills and frameworks invoked |
| [Inputs to Synthesize](#inputs-to-synthesize) | Source material for UX analysis |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

Per user direction: **"Both. We should collect some feedback on how we can best enhance the `/transcript` skill to see if there are angles we are missing."** — meaning *both* JTBD analysis and broader feedback synthesis. This Enabler runs `/user-experience` sub-skills against the `/transcript` skill to surface stakeholder angles the audit didn't capture, before FEAT-003 design locks.

The output **may** introduce new Stories or Bugs that re-shape downstream work. The Phase 1 sync barrier in EN-007 orchestration plan allows scope adjustment based on this Enabler's output.

---

## Technical Approach

Invoke `ux-orchestrator` with the full input set (issue #273, gist, SKILL.md, golden packets, EN-004 threat findings). The orchestrator routes to the right sub-skills (jtbd, heart, heuristic-eval, inclusive, behavior) and returns synthesized findings. The Methodology subsection below specifies the candidate sub-skills; the orchestrator decides which actually run based on its lifecycle-stage triage.

---

## Methodology

| Sub-skill | Why it applies | Output |
|-----------|---------------|--------|
| `ux-jtbd-analyst` | "What jobs are stakeholders hiring `/transcript` to do?" — surfaces hire/fire decisions humans make about adopting transcript output. The audit ran a single packet through review; JTBD broadens to *who else uses this and for what*. | Job statements, switch triggers, outcome expectations |
| `ux-heart-analyst` | Define HEART metrics for `/transcript` skill quality (Happiness, Engagement, Adoption, Retention, Task Success). Establish baselines we can measure post-EPIC-001 to verify hardening worked. | HEART dashboard spec, baseline measurement plan |
| `ux-heuristic-evaluator` | Evaluate the CLI surface (`jerry transcript verify`, `update-anchors`) and agent return contracts against Nielsen heuristics. Identify usability gaps before STORY-007/STORY-008 lock. | Severity-rated findings, remediation list |
| `ux-inclusive-evaluator` | Persona Spectrum review of the CLI consumer: are there permanent/temporary/situational disabilities that affect users of `jerry transcript verify` output? Are error messages cognitively accessible? | Inclusive design audit |
| `ux-behavior-diagnostician` | B=MAP analysis: do `ts-formatter` agents currently *not* run validators because Motivation/Ability/Prompt are below threshold? Diagnose the bottleneck before STORY-009/STORY-010 wire integration. | Behavior bottleneck diagnosis |

The `ux-orchestrator` parent skill routes between these as appropriate. We do not pre-commit to using all five — some may be redundant once others run. The orchestrator decides.

---

## Inputs to Synthesize

| Input | Path |
|-------|------|
| Issue #273 (full body + 3 comments) | https://github.com/geekatron/jerry/issues/273 |
| Audit author's prototype gist | https://gist.github.com/anowak-delinea/f6748192a6e32bb65c874cd0e5dde924 |
| `/transcript` SKILL.md | `skills/transcript/SKILL.md` |
| Existing transcript packets | `test_data/expected_output/` (existing golden) + audit packet (if shareable) |
| Phase 1 red-team threat model (EN-004) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/` |

---

## Agent Assignment

| Step | Skill | Agent | Wave | Purpose |
|------|-------|-------|------|---------|
| 1 | `/user-experience` | `ux-orchestrator` | 0 | T5 routing: load full input set, select Wave 1-4 sub-skills based on lifecycle-stage triage |
| 2 | `/user-experience` | `ux-jtbd-analyst` | 1 | Produce job map: ≥3 jobs people hire `/transcript` for + switch triggers + outcome expectations |
| 3 | `/user-experience` | `ux-heuristic-evaluator` | 1 | Nielsen heuristic eval of planned CLI surface (`jerry transcript verify`/`update-anchors`); severity-rated findings |
| 4 | `/user-experience` | `ux-heart-analyst` | 2 | HEART dashboard spec + baseline measurement plan |
| 5 | `/user-experience` | `ux-inclusive-evaluator` | 3 | Persona Spectrum / WCAG 2.2 audit of CLI consumer ergonomics |
| 6 | `/user-experience` | `ux-behavior-diagnostician` | 4 | B=MAP analysis on "agents that should run validators but don't" bottleneck (informs FEAT-003 STORY-009/010 hook design) |
| 7 | `/user-experience` | `ux-orchestrator` | — | Cross-framework synthesis report at `work/EPIC-001-transcript-hardening/EN-005-user-experience-exploration/synthesis.md` |
| 8 | `/worktracker` | New entities filed | — | If synthesis surfaces net-new findings, file new Stories/Bugs as worktracker entities (linked from this Enabler) |
| 9 | `/adversary` | `adv-executor` + `adv-scorer` | — | C4 ≥0.95 review on synthesis report |
| 10 | `/worktracker` | `wt-verifier` | — | Validate AC; close |

---

## Acceptance Criteria

- [ ] `ux-jtbd-analyst` job map produced; lists at minimum 3 distinct jobs people hire `/transcript` for (e.g., meeting decision capture, knowledge graph ingestion, audit-ready compliance trail).
- [ ] `ux-heart-analyst` HEART dashboard spec authored with baseline + target values.
- [ ] `ux-heuristic-evaluator` produces severity-rated findings on the planned CLI surfaces (per EN-001 design).
- [ ] `ux-inclusive-evaluator` persona-spectrum audit of CLI consumer ergonomics produces remediation list.
- [ ] `ux-behavior-diagnostician` B=MAP analysis produces explicit bottleneck diagnosis for "agents that should run validators but don't."
- [ ] **Synthesis report** captured at `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-005-user-experience-exploration/synthesis.md` enumerating: (a) net-new findings the audit didn't capture, (b) recommended new Stories/Bugs (file as worktracker entities, link from this Enabler), (c) explicit "no new finding" for areas examined.
- [ ] Phase 1 sync barrier check: EPIC-001 scope adjusted (or explicitly held) based on synthesis.
- [ ] `/adversary` C4 ≥0.95 review on the synthesis report.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Invoke ux-orchestrator with full input set | pending |
| TASK-002 | ux-jtbd-analyst run + job map | pending |
| TASK-003 | ux-heart-analyst run + HEART dashboard spec | pending |
| TASK-004 | ux-heuristic-evaluator run on CLI design | pending |
| TASK-005 | ux-inclusive-evaluator persona-spectrum audit | pending |
| TASK-006 | ux-behavior-diagnostician B=MAP analysis | pending |
| TASK-007 | Author synthesis report enumerating findings | pending |
| TASK-008 | File new worktracker entities for any net-new findings | pending |
| TASK-009 | Run /adversary C4 review on synthesis | pending |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001](../EPIC-001-transcript-hardening.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Cooperates | EN-004 | Threat model is one of the inputs to UX synthesis |
| Blocks | EN-001 | UX findings inform DDD scaffolding decisions (CLI ergonomics) |
| Blocks | STORY-007, STORY-008 | CLI surface design absorbs UX heuristic findings |
| Cooperates | EN-006 | UX surface findings inform diataxis docs scope |

### Source

- User direction: "Both. We should collect some feedback on how we can best enhance the /transcript skill to see if there are angles we are missing."

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Cross-cutting Enabler created. 5 ux sub-skills planned. Orchestrator decides which run. |
