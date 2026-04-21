# Pre-Flight Check for orch-planner Outputs

> Discipline to prevent missing-artifact gaps before declaring any orchestration plan complete. Applies to Waves 2-5 and any future wave-planning invocation.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Why this exists](#why-this-exists) | The failure mode this prevents |
| [Required outputs per orch-planner](#required-outputs-per-orch-planner) | Canonical output contract |
| [Pre-flight checklist](#pre-flight-checklist) | Verify before adversarial review |
| [Adversarial review scoping](#adversarial-review-scoping) | Review the full deliverable set, not just .md |

---

## Why this exists

During Wave 1 planning, `orch-planner` produced only `wave-1-discovery-plan.md`. The companion `ORCHESTRATION.yaml` (the machine-readable SSOT required by the agent's own `must` clauses) was never generated. The gap was not caught until after three iterations of adversarial review on the `.md` alone had already declared the plan "APPROVED." Remediation took three additional iterations of a full-set review to close.

Root cause: the orchestrator (main context) did not verify orch-planner's output against the agent definition's declared outputs before scoping the adversarial review.

Fix: run this pre-flight check before invoking adversarial review on any orch-planner output.

---

## Required outputs per orch-planner

Per `skills/orchestration/agents/orch-planner.md` `must` clauses (lines 301-310, 328-329), every orch-planner invocation MUST produce BOTH files:

| File | Purpose | Canonical path |
|------|---------|---------------|
| `ORCHESTRATION_PLAN.md` (or per-wave equivalent) | Strategic context, human-readable | `projects/{project_id}/ORCHESTRATION_PLAN.md` OR `projects/{project_id}/orchestration/plans/{wave}-plan.md` |
| `ORCHESTRATION.yaml` | Machine-readable SSOT for workflow execution state | `projects/{project_id}/ORCHESTRATION.yaml` |

**Both are mandatory.** The `.md` alone does NOT satisfy the skill contract. `orch-synthesizer` (wave-exit convergence agent) reads `ORCHESTRATION.yaml` to enumerate artifacts; without it, the convergence gate cannot operate.

---

## Pre-flight checklist

Before sending any orch-planner output to `/adversary` for C3+ review, verify all of the following:

### Existence checks

- [ ] `ORCHESTRATION_PLAN.md` (or per-wave equivalent) exists at the canonical path
- [ ] `ORCHESTRATION.yaml` exists at the canonical path
- [ ] No other required outputs declared in the specific wave's planner prompt are missing

### `.md` basic checks

- [ ] Navigation table present (NAV-001, H-23)
- [ ] L0/L1/L2 output levels declared (per orch-planner agent spec line 302)
- [ ] ASCII workflow diagram present (line 303)
- [ ] Disclaimer present (line 306)

### `.yaml` basic checks

- [ ] Parses via `python3 -c "import yaml; yaml.safe_load(open('path'))"` without error
- [ ] Top-level keys include at minimum: `schema_version`, `workflow`, `paths`, `pipelines`, `barriers`, `adversarial`, `execution_queue`, `checkpoints`, `metrics`, `blockers`, `issues`, `next_actions`, `resumption`
- [ ] `workflow.constraints` includes `max_agent_nesting: 1` (P-003) and `file_persistence: true` (P-002)
- [ ] `adversarial` section enumerates required strategies per criticality correctly per `quality-enforcement.md` — especially **C3 required = 6 strategies (S-007, S-002, S-014, S-004, S-012, S-013)**, NOT the C2 baseline of 3

### Cross-file consistency

- [ ] Phase counts in `.md` match `.yaml` `pipelines[].phases[]`
- [ ] Feature IDs in `.md` exist in `.yaml` (pipelines, barriers, or execution_queue)
- [ ] Gate names in `.md` match `.yaml` `barriers[].id`
- [ ] Threshold values consistent across both files
- [ ] Iteration ceilings consistent across both files (and aligned with RT-M-010: C3=7, C4=10)
- [ ] Artifact path scheme in `.md` matches `.yaml` `paths` block
- [ ] First-dispatch priority (if applicable) reflected in `.yaml` `execution_queue.ready_to_dispatch`

### Quick command for existence + yaml-validity

```bash
PROJECT="PROJ-NNN-name"
ls -la projects/${PROJECT}/ORCHESTRATION.yaml && \
ls -la projects/${PROJECT}/orchestration/plans/ && \
python3 -c "import yaml; d=yaml.safe_load(open('projects/${PROJECT}/ORCHESTRATION.yaml')); print('keys:', list(d.keys()))"
```

If any check fails, re-invoke orch-planner with an explicit mandate to produce the missing artifact — do NOT proceed to adversarial review on a partial deliverable set.

---

## Adversarial review scoping

When invoking `/adversary` on orchestration planning output, the review target MUST be the full deliverable set, not individual files.

### Correct prompt framing

```
Target deliverable SET (both files together):
1. projects/{project}/orchestration/plans/{wave}-plan.md
2. projects/{project}/ORCHESTRATION.yaml

Both are required per skills/orchestration/agents/orch-planner.md
lines 301-310 and 328-329. They must be consistent with each other AND
satisfy the skill's must clauses.

Specifically verify:
- YAML parses cleanly
- Cross-file consistency on feature counts, gate names, thresholds, paths
- adversarial strategy catalog matches quality-enforcement.md for each criticality
- All required top-level YAML sections present
```

### Incorrect prompt framing (what failed before)

```
Target: projects/{project}/orchestration/plans/{wave}-plan.md
```

Single-file scoping cannot surface a missing companion file. The review will score what it is given without probing for absence of required artifacts.

---

## Application to Waves 2-5

Every future orch-planner invocation in PROJ-040 (Waves 2, 3, 4, 5) MUST:

1. Explicitly mandate production of ORCHESTRATION.yaml update alongside the wave's plan `.md`
2. Run this pre-flight checklist before adversarial review
3. Scope adversarial review to the full deliverable set
4. Update ORCHESTRATION.yaml `workflow.status` and populate wave-specific approval fields before declaring the wave plan approved

---

## References

| Source | Content |
|--------|---------|
| `skills/orchestration/agents/orch-planner.md` | Agent definition with must-clauses (lines 301-310, 328-329) |
| `skills/orchestration/agents/orch-synthesizer.md` | Downstream consumer that reads ORCHESTRATION.yaml (lines 78, 98) |
| `projects/PROJ-007-agent-patterns/ORCHESTRATION.yaml` | Canonical reference implementation (1055 lines) |
| `projects/PROJ-004-context-resilience/ORCHESTRATION.yaml` | Secondary reference (637 lines) |
| `.context/rules/quality-enforcement.md` | Criticality-specific strategy catalog SSOT |
| `projects/PROJ-040-documentation/orchestration/reviews/wave-1-fullset-iter-{1..3}-*.md` | Evidence trail of the remediation that motivated this checklist |
