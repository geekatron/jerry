# PROJ-014 Orchestration Plan: Negative Prompting Research

> Workflow: neg-prompting-20260227-001 | Criticality: C4 | Threshold: >= 0.95
> Hypothesis: Negative prompting outperforms positive prompting for LLM behavioral compliance.
> Updated: 2026-02-27

## Document Sections

| Section | Purpose |
|---------|---------|
| [Hypothesis](#hypothesis) | Core research question and framing |
| [Orchestration Directives](#orchestration-directives) | Non-negotiable execution constraints |
| [Phase Summary](#phase-summary) | All phases with status |
| [Barrier 1 Status](#barrier-1-status) | Research cross-pollination (PASSED) |
| [A/B Testing Design](#ab-testing-design) | Retrospective + controlled experiment |
| [Phase 2 Plan](#phase-2-plan) | Claim validation and comparative analysis |
| [Downstream Phases](#downstream-phases) | Phases 3-6 overview |
| [Artifact Registry](#artifact-registry) | All produced artifacts with paths |

---

## Hypothesis

**Negative unambiguous prompting reduces hallucination by 60% and achieves better results than explicit positive prompting.**

This project does not abandon this hypothesis based on literature gaps. The absence of published controlled evidence is the research opportunity, not a reason to retreat. The project proceeds with the working assumption that negative prompting is the superior framing for LLM behavioral compliance, and will produce the first controlled evidence to validate or refute this claim.

---

## Orchestration Directives

These directives govern the entire orchestration run. You must not violate them.

1. You must not use positive prompting for the duration of this orchestration run — all prompts use negative constraint framing
2. You must not omit the supplemental vendor evidence report from downstream phase inputs
3. You must not let any deliverable pass a quality gate below 0.95
4. You must not run more than 5 adversary iterations per deliverable
5. You must not leave ORCHESTRATION.yaml or this plan out of date after any phase completion
6. You must not dismiss practitioner evidence or vendor self-practice evidence as inferior
7. You must not treat absence of published evidence as evidence of absence
8. You must not abandon the hypothesis based on literature review alone — the A/B testing must be completed

---

## Phase Summary

| Phase | Description | Status | Barrier |
|-------|-------------|--------|---------|
| Phase 1 | Literature Research (academic + industry + context7) | **COMPLETE** | Barrier 1: **PASSED** (0.953 synthesis + 0.951 supplemental) |
| Phase 2 | Evidence Analysis (claim validation + comparative effectiveness) | NOT STARTED | Barrier 2 |
| Phase 3 | Negative Prompting Taxonomy & Pattern Catalog | NOT STARTED | Barrier 3 |
| Phase 4 | Jerry Framework Application Analysis (5 sub-tasks) | NOT STARTED | Barrier 4 |
| Phase 5 | Implementation Planning (4 ADRs) | NOT STARTED | Barrier 5 |
| Phase 6 | Final Synthesis & Recommendations | NOT STARTED | C4 Tournament |

---

## Barrier 1 Status

**Status: PASSED**

### Primary Synthesis

| Metric | Value |
|--------|-------|
| Artifact | `barrier-1/synthesis.md` (R4) |
| Score | 0.953 |
| Iterations | 4 of 5 |
| Unique sources | 75 (deduplicated across 3 surveys) |
| Gate report | `barrier-1/adversary-gate.md` |

### Supplemental Vendor Evidence

| Metric | Value |
|--------|-------|
| Artifact | `barrier-1/supplemental-vendor-evidence.md` (R4) |
| Score | 0.951 |
| Iterations | 4 of 5 |
| Evidence categories | 4 (vendor self-practice, Jerry framework, session empirical, innovator's gap) |
| Gate report | `barrier-1/supplemental-adversary-gate.md` |

### Key Findings for Downstream

1. Zero published evidence validates the 60% hallucination reduction claim — this is the research gap, not a refutation
2. Anthropic uses negative prompting extensively in its own production behavioral enforcement (33 NEVER/MUST NOT instances across 10 rule files)
3. This session's negative-constraint prompts produced C4-passing results (0.953, 0.951) — empirical observation, not controlled evidence
4. The controlled A/B experiment designed in the supplemental report (270 matched pairs, McNemar test) directly addresses the critical literature gap
5. The 12-level effectiveness hierarchy from the synthesis provides the experimental conditions framework

### Mandatory Downstream Inputs

Both barrier-1 artifacts must be provided to all downstream phases. You must not omit the supplemental report.

| Artifact | Path | Required By |
|----------|------|-------------|
| Primary synthesis | `barrier-1/synthesis.md` | All downstream phases |
| Supplemental vendor evidence | `barrier-1/supplemental-vendor-evidence.md` | All downstream phases |
| Adversary gate (primary) | `barrier-1/adversary-gate.md` | Quality audit trail |
| Adversary gate (supplemental) | `barrier-1/supplemental-adversary-gate.md` | Quality audit trail |

---

## A/B Testing Design

### Retrospective Comparison (This Orchestration Run)

| Condition | Source | Framing |
|-----------|--------|---------|
| A (negative) | PROJ-014 sessions | All prompts use NEVER/MUST NOT constraint framing |
| B (positive) | PROJ-006, PROJ-007 sessions | Standard positive framing |

Metrics: quality gate scores, iteration counts to pass, scope violation rate, user intervention frequency.
Limitation: not controlled (different tasks, different complexity). Provides directional signal only.

### Controlled Experiment (Phase 2)

| Parameter | Value |
|-----------|-------|
| Sample size | 270 matched prompt pairs |
| Pairs per category | 54 |
| Task categories | 5 |
| Models | Claude Opus, Claude Sonnet, Claude Haiku |
| Scoring | S-014 LLM-as-Judge (6 dimensions) |
| Statistical test | McNemar paired test (continuity-corrected) |
| Power | 80% at alpha=0.05 |
| Primary outcomes | Constraint adherence rate, quality gate first-pass rate |
| Secondary outcomes | Hallucination rate, iteration count to convergence |
| Pilot | n=30 to calibrate discordant proportion assumption |

---

## Phase 2 Plan

Phase 2 (TASK-005, TASK-006) executes with both barrier-1 artifacts as input:

### TASK-005: Claim Validation
- Validate/refute the 60% hallucination reduction claim with primary evidence
- Execute the retrospective A/B comparison using PROJ-014 vs PROJ-006/PROJ-007 data
- Design the controlled experiment pilot (n=30 matched pairs)
- Quality gate: /adversary C4 >= 0.95

### TASK-006: Comparative Effectiveness Analysis
- 5-dimension comparison of positive vs negative prompting
- Use the 12-level effectiveness hierarchy from synthesis as framework
- Incorporate vendor self-practice evidence from supplemental report
- Quality gate: /adversary C4 >= 0.95

### Barrier 2: Analysis Cross-Pollination
- Cross-pollinate TASK-005 + TASK-006 outputs
- Quality gate: /adversary C4 >= 0.95

---

## Downstream Phases

### Phase 3: Taxonomy & Pattern Catalog (TASK-008, Barrier 3)
- Build negative prompting taxonomy from all prior evidence
- Catalog patterns by type, effectiveness tier, and applicability

### Phase 4: Jerry Framework Application (TASK-010 through TASK-014, Barrier 4)
- Skills update analysis (TASK-010)
- Agents update analysis (TASK-011)
- Rules update analysis (TASK-012, auto-C3 per AE-002)
- Patterns update analysis (TASK-013)
- Templates update analysis (TASK-014)

### Phase 5: Implementation Planning (TASK-016, Barrier 5)
- 4 ADRs for Jerry framework changes

### Phase 6: Final Synthesis (TASK-018, TASK-019, TASK-020)
- Final synthesis and implementation roadmap
- C4 tournament (all 10 strategies, >= 0.95)
- Documentation and commit

---

## Artifact Registry

All paths relative to `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/`.

### Phase 1 Research (COMPLETE)

| Artifact | Path | Score |
|----------|------|-------|
| Academic survey | `../../research/academic-survey.md` | 0.950 |
| Industry survey | `../../research/industry-survey.md` | 0.9325 |
| Context7 survey | `../../research/context7-survey.md` | 0.935 |

### Barrier 1 (PASSED)

| Artifact | Path | Score |
|----------|------|-------|
| Primary synthesis (R4) | `barrier-1/synthesis.md` | 0.953 |
| Supplemental vendor evidence (R4) | `barrier-1/supplemental-vendor-evidence.md` | 0.951 |
| Adversary gate (primary) | `barrier-1/adversary-gate.md` | — |
| Adversary gate (supplemental) | `barrier-1/supplemental-adversary-gate.md` | — |
| Strategy selection (primary) | `barrier-1/adversary-selection.md` | — |
| Strategy selection (supplemental) | `barrier-1/supplemental-adversary-selection.md` | — |
| Executor findings (primary, I1-I3) | `barrier-1/adversary-executor-findings-i{1,2,3}.md` | — |
| Scorer (primary, I4) | `barrier-1/adversary-scorer-i4.md` | — |
| Executor findings (supplemental, I1-I3) | `barrier-1/supplemental-adversary-findings-i{1,2,3}.md` | — |
| Scorer (supplemental, I4) | `barrier-1/supplemental-adversary-scorer-i4.md` | — |

---

*GitHub Issue: [#122](https://github.com/geekatron/jerry/issues/122)*
*ORCHESTRATION.yaml: Updated 2026-02-27 with supplemental report and A/B testing design*
*All paths relative to `projects/PROJ-014-negative-prompting-research/`*
