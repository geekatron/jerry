# TASK-009: Orchestration Template Updates

<!--
DOCUMENT-ID: FEAT-004:EN-307:TASK-009
VERSION: 1.0.0
AGENT: ps-architect-307
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-307 (Orchestration Skill Enhancement - Adversarial Loops)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DEVELOPMENT
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-307
> **Quality Target:** >= 0.92
> **Purpose:** Define updates to the three orchestration templates (ORCHESTRATION_PLAN.template.md, ORCHESTRATION.template.yaml, ORCHESTRATION_WORKTRACKER.template.md) to include adversarial sections by default

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this update delivers |
| [Template Inventory](#template-inventory) | Which templates are updated |
| [ORCHESTRATION_PLAN.template.md Updates](#orchestration_plantemplate-md-updates) | New adversarial sections in the plan template |
| [ORCHESTRATION.template.yaml Updates](#orchestrationtemplateyaml-updates) | New YAML fields for adversarial state tracking |
| [ORCHESTRATION_WORKTRACKER.template.md Updates](#orchestration_worktrackertemplate-md-updates) | New adversarial tracking sections in the worktracker |
| [Backward Compatibility](#backward-compatibility) | How templates support non-adversarial workflows |
| [Template Validation Checklist](#template-validation-checklist) | Verification criteria for updated templates |
| [Traceability](#traceability) | Mapping to requirements |
| [References](#references) | Source citations |

---

## Summary

This document defines the updates to the three orchestration templates to include adversarial feedback loop sections by default. When orch-planner creates a new workflow using these templates, adversarial review infrastructure is built in from the start. The templates remain usable for non-adversarial workflows through conditional sections.

The three templates updated:

1. **ORCHESTRATION_PLAN.template.md** -- Adds adversarial configuration, strategy assignment, and quality gate sections
2. **ORCHESTRATION.template.yaml** -- Adds constraint fields, iteration tracking, quality metrics, and resumption context
3. **ORCHESTRATION_WORKTRACKER.template.md** -- Adds adversarial iteration tracking and quality score logging

All template updates are additive. Non-adversarial workflows can omit or disable the adversarial sections.

---

## Template Inventory

| Template | Location | Current Version | Updated Version |
|----------|----------|-----------------|-----------------|
| ORCHESTRATION_PLAN.template.md | `skills/orchestration/templates/` | 1.0.0 | 2.0.0 |
| ORCHESTRATION.template.yaml | `skills/orchestration/templates/` | 1.0.0 | 2.0.0 |
| ORCHESTRATION_WORKTRACKER.template.md | `skills/orchestration/templates/` | 1.0.0 | 2.0.0 |

---

## ORCHESTRATION_PLAN.template.md Updates

### New Sections to Add

The following sections are added to the orchestration plan template after the existing L1 Technical Plan section:

#### Section: Adversarial Review Configuration

```markdown
## Adversarial Review Configuration

> This section is automatically generated when `adversarial_validation: true`.

### Quality Gate Settings

| Setting | Value | Source |
|---------|-------|--------|
| Quality Threshold | {QUALITY_GATE_THRESHOLD} | quality-enforcement.md SSOT |
| Minimum Iterations | {ADVERSARIAL_ITERATION_MIN} | quality-enforcement.md SSOT |
| Default Criticality | {CRITICALITY_DEFAULT} | Workflow configuration |
| Adversarial Validation | {true/false} | Workflow constraints |

<!-- L2-REINJECT: rank=3, tokens=30, content="Quality gate >= {QUALITY_GATE_THRESHOLD}. Min {ADVERSARIAL_ITERATION_MIN} adversarial iterations. S-014 LLM-as-Judge scoring REQUIRED." -->

### Phase Criticality Assignment

| Phase | Pipeline | Criticality | Rationale |
|-------|----------|-------------|-----------|
| {PHASE_ID} | {PIPELINE_ALIAS} | {C1/C2/C3/C4} | {RATIONALE} |

### Strategy Assignment by Phase

| Phase | Criticality | Iter 1 Strategies | Iter 2 Strategies | Iter 3 Strategies |
|-------|-------------|-------------------|-------------------|-------------------|
| {PHASE_ID} | {CRITICALITY} | {STRATEGIES_ITER_1} | {STRATEGIES_ITER_2} | {STRATEGIES_ITER_3} |

### Enforcement Layer Mapping

| Layer | Availability | Adversarial Coverage |
|-------|-------------|---------------------|
| L1 (Static Context) | All platforms | S-007 Constitutional AI |
| L2 (Per-Prompt) | PLAT-CC | S-014 scoring reminders |
| L3 (Pre-Action) | PLAT-CC | Quality gate pre-checks |
| L4 (Post-Action) | PLAT-CC | Score validation |
| L5 (Post-Hoc) | All platforms | ps-validator |
| Process | All platforms | Creator-critic-revision cycle |

### Token Budget Estimate

| Phase | Criticality | Estimated Token Budget | Breakdown |
|-------|-------------|----------------------|-----------|
| {PHASE_ID} | {CRITICALITY} | {TOTAL_TOKENS} | {PER_STRATEGY_BREAKDOWN} |
| **Total** | -- | {GRAND_TOTAL} | -- |
```

#### Section: Adversarial Review Workflow Diagram

```markdown
### Adversarial Review Workflow

```
For each phase requiring adversarial review:

  Creator (Group N)
      |
      v
  Critic Iter 1 (Group N+1) -- strategies: [{ITER_1_STRATEGIES}]
      |
      v
  Revision Iter 1 (Group N+2) -- addresses findings
      |
      v
  Critic Iter 2 (Group N+3) -- strategies: [{ITER_2_STRATEGIES}]
      |
      v
  Revision Iter 2 (Group N+4) -- final improvements
      |
      v
  Critic Iter 3 (Group N+5) -- final scoring (may be SKIPPED)
      |
      v
  Validation (Group N+6) -- quality verdict
      |
      v
  Quality Gate: >= {QUALITY_GATE_THRESHOLD} required
```
```

---

## ORCHESTRATION.template.yaml Updates

### New Fields in Template

The YAML template gains the following new sections and fields:

```yaml
# ========================================================================
# ORCHESTRATION.template.yaml v2.0.0
# Template for machine-readable orchestration state (SSOT)
# ========================================================================

workflow:
  id: "{WORKFLOW_ID}"
  name: "{WORKFLOW_NAME}"
  project_id: "{PROJECT_ID}"
  status: "PLANNED"
  created: "{ISO_DATE}"

  # v2.0.0: Adversarial Configuration
  constraints:
    quality_gate_threshold: 0.92          # From quality-enforcement.md SSOT
    adversarial_iteration_min: 3          # Minimum adversarial iterations
    adversarial_validation: true          # Enable adversarial feedback loops
    criticality_default: "C2"             # Default criticality level

  patterns:
    # - SEQUENTIAL                        # Uncomment patterns used
    # - FAN_OUT
    # - CROSS_POLLINATED
    - ADVERSARIAL_FEEDBACK                 # v2.0.0: Adversarial pattern

paths:
  base: "orchestration/{WORKFLOW_ID}/"
  pipeline: "{base}{PIPELINE_ALIAS}/{PHASE_ID}/"
  barrier: "{base}cross-pollination/{BARRIER_ID}/{DIRECTION}/"

pipelines:
  {PIPELINE_A_ID}:
    name: "{PIPELINE_A_NAME}"
    short_alias: "{PIPELINE_A_ALIAS}"
    skill_source: "{SKILL_NAME}"
    current_phase: 1
    phases:
      - id: 1
        name: "{PHASE_1_NAME}"
        path_id: "phase-1"
        status: "PENDING"
        criticality: "{C1|C2|C3|C4}"       # v2.0.0: Per-phase criticality
        adversarial_review: true             # v2.0.0: Enable per-phase (opt-out with false)
        quality_scores: []                   # v2.0.0: Scores per iteration
        final_quality_score: null            # v2.0.0: Final achieved score
        validation_verdict: null             # v2.0.0: PASS|CONDITIONAL PASS|FAIL
        agents:
          - id: "{AGENT_ID}"
            role: "creator"                  # v2.0.0: creator|critic|validator
            status: "PENDING"
            artifact: null
            adversarial_strategies: []       # v2.0.0: Strategy assignment (for critics)
            anti_leniency: false             # v2.0.0: Anti-leniency flag (for critics)

barriers:
  - id: "barrier-1"
    status: "PENDING"
    prerequisite_phases: ["{PIPELINE_A_ALIAS}-phase-1", "{PIPELINE_B_ALIAS}-phase-1"]
    # v2.0.0: Quality gate at barrier
    quality_summary:
      upstream_phases: []
      quality_scores: {}
      all_passed: false
    artifacts:
      "{PIPELINE_A_ALIAS}-to-{PIPELINE_B_ALIAS}":
        path: null
        status: "PENDING"
      "{PIPELINE_B_ALIAS}-to-{PIPELINE_A_ALIAS}":
        path: null
        status: "PENDING"

execution_queue:
  current_group: 1
  groups:
    # Group 1: Creator agents
    - id: 1
      name: "Phase 1 - Creator"
      execution_mode: "PARALLEL"
      status: "PENDING"
      blocked_by: []
      # v2.0.0: Adversarial context
      adversarial_context:
        cycle_phase: "creator"
        iteration: null
        max_iterations: 3
        quality_threshold: 0.92
        strategies: []
        early_exit_eligible: false
      agents: ["{CREATOR_AGENT_IDS}"]

    # Group 2: Adversarial Iteration 1 - Critic (v2.0.0)
    - id: 2
      name: "Phase 1 - Adversarial Iteration 1 (Critic)"
      execution_mode: "PARALLEL"
      status: "PENDING"
      blocked_by: [1]
      adversarial_context:
        cycle_phase: "critic"
        iteration: 1
        max_iterations: 3
        quality_threshold: 0.92
        strategies: ["{ITER_1_STRATEGIES}"]
        early_exit_eligible: false
      agents: ["{CRITIC_AGENT_IDS}"]

    # Group 3: Adversarial Iteration 1 - Revision (v2.0.0)
    - id: 3
      name: "Phase 1 - Adversarial Iteration 1 (Revision)"
      execution_mode: "PARALLEL"
      status: "PENDING"
      blocked_by: [2]
      adversarial_context:
        cycle_phase: "revision"
        iteration: 1
      agents: ["{REVISION_AGENT_IDS}"]

    # Groups 4-5: Iteration 2 (Critic + Revision)
    # Group 6: Iteration 3 (Critic / Final Scoring)
    # Group 7: Validation

    # v2.0.0: Iteration tracking (for phases with adversarial review)
    - id: "{ADVERSARIAL_GROUP_ID}"
      iterations:
        - iteration: 1
          status: "PENDING"
          critique_agents: []
          revision_agents: []
          scores: {}
          delta: {}
          findings_resolved: {}
        - iteration: 2
          status: "PENDING"
          critique_agents: []
          revision_agents: []
          scores: {}
          delta: {}
          findings_resolved: {}
        - iteration: 3
          status: "PENDING"
          critique_agents: []
          revision_agents: []
          scores: {}
          delta: {}
          findings_resolved: {}
          early_exit_eligible: true

checkpoints:
  latest_id: null
  entries: []

blockers:
  active: []
  resolved: []

metrics:
  phases_complete: 0
  phases_total: "{N}"
  agents_executed: 0
  agents_total: "{N}"
  barriers_complete: 0
  barriers_total: "{N}"
  # v2.0.0: Quality metrics
  quality:
    adversarial_iterations_completed: 0
    adversarial_iterations_total: "{N}"
    quality_scores: []
    gates_passed: 0
    gates_conditional: 0
    gates_failed: 0

resumption:
  last_completed_agent: null
  next_agent: "{FIRST_AGENT_ID}"
  files_to_read:
    - "ORCHESTRATION.yaml"
    - "ORCHESTRATION_PLAN.md"
  # v2.0.0: Adversarial feedback state
  adversarial_feedback_status:
    total_enablers: "{N}"
    enablers_complete: 0
    enablers_validated: 0
    current_enabler: "N/A"
    current_iteration: "N/A"
    iterations_complete: 0
    iterations_total: "{N}"
```

---

## ORCHESTRATION_WORKTRACKER.template.md Updates

### New Sections to Add

The worktracker template gains the following new sections:

#### Section: Adversarial Review Log

```markdown
## Adversarial Review Log

### Quality Gate Status

| Phase | Pipeline | Criticality | Iter 1 Score | Iter 2 Score | Iter 3 Score | Final | Verdict |
|-------|----------|-------------|-------------|-------------|-------------|-------|---------|
| -- | -- | -- | -- | -- | -- | -- | -- |

### Iteration Details

#### Phase {N}: {PHASE_NAME}

**Criticality:** {C1|C2|C3|C4}

| Iteration | Critic Agent | Strategies | Score | Delta | Findings (B/M/m) | Status |
|-----------|-------------|-----------|-------|-------|-------------------|--------|
| 1 | -- | -- | -- | -- | --/--/-- | PENDING |
| 2 | -- | -- | -- | -- | --/--/-- | PENDING |
| 3 | -- | -- | -- | -- | --/--/-- | PENDING |

**Quality Gate Result:** PENDING
**Validation Verdict:** PENDING

### Finding Resolution Tracking

| Enabler | Iteration | Blocking | Major | Minor | Resolution Rate |
|---------|-----------|----------|-------|-------|-----------------|
| -- | -- | --/-- | --/-- | --/-- | --% |

### Escalation Log

| Date | Enabler | Score | Action | Outcome |
|------|---------|-------|--------|---------|
| -- | -- | -- | -- | -- |
```

#### Section: Quality Metrics Summary

```markdown
## Quality Metrics Summary

| Metric | Value |
|--------|-------|
| Total Adversarial Iterations | 0 / {N} |
| Quality Gates Passed | 0 / {N} |
| Quality Gates Conditional | 0 |
| Quality Gates Failed | 0 |
| Average Quality Score | -- |
| Average Improvement per Iteration | -- |
| Most Effective Strategy | -- |
```

---

## Backward Compatibility

### Non-Adversarial Workflow Usage

All adversarial template sections are conditional. When `adversarial_validation: false`:

1. **ORCHESTRATION_PLAN.template.md:** "Adversarial Review Configuration" section omitted
2. **ORCHESTRATION.template.yaml:** Adversarial fields present but empty/null -- no functional impact
3. **ORCHESTRATION_WORKTRACKER.template.md:** "Adversarial Review Log" section shows "N/A - Adversarial validation not enabled"

### Field Defaults

| Field | Default (adversarial enabled) | Default (adversarial disabled) |
|-------|-------------------------------|-------------------------------|
| `adversarial_validation` | `true` | `false` |
| `quality_gate_threshold` | `0.92` | `null` |
| `adversarial_iteration_min` | `3` | `null` |
| `criticality_default` | `"C2"` | `null` |
| `patterns` | `[ADVERSARIAL_FEEDBACK]` | `[]` |
| `adversarial_context` | Full structure | `null` |
| `quality` in metrics | Full structure | `null` |
| `adversarial_feedback_status` | Full structure | `null` |

---

## Template Validation Checklist

### ORCHESTRATION_PLAN.template.md

- [ ] Contains "Adversarial Review Configuration" section
- [ ] Contains L2-REINJECT tag with quality gate values
- [ ] Contains phase criticality assignment table
- [ ] Contains strategy assignment table
- [ ] Contains enforcement layer mapping table
- [ ] Contains token budget estimate table
- [ ] Contains adversarial review workflow diagram
- [ ] All placeholder values use `{PLACEHOLDER}` format
- [ ] Non-adversarial workflows can omit section cleanly

### ORCHESTRATION.template.yaml

- [ ] Contains `workflow.constraints` with adversarial fields
- [ ] Contains `workflow.patterns` with ADVERSARIAL_FEEDBACK
- [ ] Phase definitions include `criticality`, `quality_scores`, `validation_verdict`
- [ ] Agent definitions include `role`, `adversarial_strategies`, `anti_leniency`
- [ ] Execution queue groups include `adversarial_context`
- [ ] Iteration tracking structure present
- [ ] Barrier includes `quality_summary`
- [ ] Metrics includes `quality` section
- [ ] Resumption includes `adversarial_feedback_status`
- [ ] Valid YAML when all placeholders are resolved
- [ ] Backward compatible when adversarial fields are null

### ORCHESTRATION_WORKTRACKER.template.md

- [ ] Contains "Adversarial Review Log" section
- [ ] Contains "Quality Gate Status" table
- [ ] Contains "Iteration Details" per phase
- [ ] Contains "Finding Resolution Tracking" table
- [ ] Contains "Escalation Log" table
- [ ] Contains "Quality Metrics Summary" section
- [ ] Non-adversarial workflows show "N/A" in adversarial sections

---

## Traceability

| Requirement | Template Section | Status |
|-------------|-----------------|--------|
| FR-307-002 | ORCHESTRATION.template.yaml (execution queue groups) | Covered |
| FR-307-005 | ORCHESTRATION.template.yaml (agent fields) | Covered |
| FR-307-006 | ORCHESTRATION.template.yaml (constraints) | Covered |
| FR-307-007 | ORCHESTRATION.template.yaml (iterations) | Covered |
| FR-307-009 | ORCHESTRATION.template.yaml (resumption) | Covered |
| FR-307-011 | ORCHESTRATION.template.yaml (quality_scores in phase) | Covered |
| FR-307-015 | ORCHESTRATION.template.yaml (delta in iterations) | Covered |
| FR-307-016 | ORCHESTRATION.template.yaml (findings_resolved) | Covered |
| FR-307-017 | ORCHESTRATION.template.yaml (metrics.quality) | Covered |
| IR-307-003 | ORCHESTRATION_PLAN.template.md (L2-REINJECT tag) | Covered |
| IR-307-004 | ORCHESTRATION.template.yaml (patterns list) | Covered |
| IR-307-005 | ORCHESTRATION_PLAN.template.md (enforcement layer mapping) | Covered |
| IR-307-006 | ORCHESTRATION_PLAN.template.md (token budget estimate) | Covered |
| NFR-307-001 | Backward Compatibility section | Covered |
| NFR-307-004 | Template Validation Checklist (valid YAML) | Covered |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | FEAT-004:EN-307:TASK-001 (Requirements) | FR-307-002 through FR-307-017, IR-307-003 through IR-307-006, NFR-307-001, NFR-307-004 |
| 2 | FEAT-004:EN-307:TASK-002 (Planner Design) | Schema additions, iteration structure |
| 3 | FEAT-004:EN-307:TASK-003 (Tracker Design) | Quality gate tracking fields |
| 4 | FEAT-004:EN-307:TASK-004 (Planner Spec) | Output format for ORCHESTRATION.yaml |
| 5 | FEAT-004:EN-307:TASK-005 (Tracker Spec) | State update protocol fields |
| 6 | Live ORCHESTRATION.yaml (epic002-crosspoll-20260213-001) | Proven field structures |
| 7 | Existing orchestration templates | Baseline for integration |

---

*Document ID: FEAT-004:EN-307:TASK-009*
*Agent: ps-architect-307*
*Created: 2026-02-13*
*Status: Complete*
