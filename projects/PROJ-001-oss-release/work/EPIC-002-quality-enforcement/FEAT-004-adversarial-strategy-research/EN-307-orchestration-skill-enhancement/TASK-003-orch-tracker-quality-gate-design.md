# TASK-003: Quality Gate Integration Design for orch-tracker

<!--
DOCUMENT-ID: FEAT-004:EN-307:TASK-003
VERSION: 1.0.0
AGENT: ps-architect-307
DATE: 2026-02-13
STATUS: Complete
PARENT: EN-307 (Orchestration Skill Enhancement - Adversarial Loops)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DESIGN
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-307
> **Quality Target:** >= 0.92
> **Purpose:** Design how orch-tracker tracks quality scores at sync barriers, aggregates scores, determines pass/fail, and enforces escalation protocols

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this design delivers |
| [Quality Score Recording](#quality-score-recording) | How scores are captured per iteration |
| [Score Aggregation](#score-aggregation) | How per-artifact scores roll up to phase-level scores |
| [Pass/Fail Determination](#passfail-determination) | Quality gate decision logic |
| [Escalation Protocol](#escalation-protocol) | What happens on quality gate failure |
| [Early Exit Logic](#early-exit-logic) | When and how iterations can be skipped |
| [S-014 LLM-as-Judge Integration](#s-014-llm-as-judge-integration) | Scoring protocol and anti-leniency |
| [Barrier Quality Gate](#barrier-quality-gate) | Quality enforcement at sync barriers |
| [Finding Resolution Tracking](#finding-resolution-tracking) | How finding closure is tracked across iterations |
| [Iteration Delta Tracking](#iteration-delta-tracking) | Measuring adversarial review effectiveness |
| [State Update Protocol](#state-update-protocol) | How orch-tracker updates ORCHESTRATION.yaml |
| [Live Example Analysis](#live-example-analysis) | Mapping to EPIC-002 ORCHESTRATION.yaml |
| [Traceability](#traceability) | Mapping to requirements |
| [References](#references) | Source citations |

---

## Summary

This document designs how the orch-tracker agent integrates quality gate tracking into its state management responsibilities. The orch-tracker is the central state manager for orchestrated workflows. With this enhancement, it gains the ability to:

1. **Record quality scores** at each adversarial iteration (FR-307-011)
2. **Aggregate scores** across multiple artifacts within a phase (FR-307-012)
3. **Determine pass/fail** against the >= 0.92 threshold (FR-307-013)
4. **Execute escalation** when quality gates fail after max iterations (FR-307-014)
5. **Track deltas** between iterations to measure improvement (FR-307-015)
6. **Track finding resolution** across iterations (FR-307-016)
7. **Enforce barrier gates** preventing cross-pollination without quality validation (FR-307-018)

The design extends the existing orch-tracker state update protocol without breaking backward compatibility. When `adversarial_validation` is absent from the workflow constraints, the tracker operates identically to its pre-enhancement behavior.

---

## Quality Score Recording

### Per-Iteration Score Capture

After each critic agent completes, the orch-tracker records the quality score in the iteration tracking structure:

```yaml
execution_queue:
  groups:
    - id: 10
      iterations:
        - iteration: 1
          status: "COMPLETE"
          critique_agents: ["ps-critic-303", "ps-critic-403"]
          revision_agents: ["ps-architect-303", "ps-architect-403"]
          scores:
            EN-303: 0.79
            EN-403-404: 0.82
          findings_resolved:
            EN-303: "0/3 blocking, 0/5 major, 0/4 minor"
            EN-403-404: "0/4 blocking, 0/7 major, 0/5 minor"
```

### Score Source

Quality scores originate from the S-014 LLM-as-Judge scoring protocol (IR-307-007). The critic agent produces a score as part of its output artifact. The orch-tracker extracts this score from the artifact and records it in ORCHESTRATION.yaml.

**Score extraction protocol:**

1. Critic agent writes artifact with S-014 score section
2. Orchestrator reads the artifact (or receives score via session context)
3. Orchestrator invokes orch-tracker with the score
4. orch-tracker records score in `iterations[N].scores`

### Phase-Level Score Recording

At phase completion, the orch-tracker records cumulative quality scores in the phase definition (FR-307-011):

```yaml
pipelines:
  adv:
    phases:
      - id: 1
        status: "COMPLETE"
        quality_scores: [0.79, 0.935]          # Score per iteration
        final_quality_score: 0.935              # Final achieved score
        validation_verdict: "CONDITIONAL PASS"  # Validator judgment
```

---

## Score Aggregation

### Per-Enabler Scoring

When a phase contains multiple enablers (e.g., Phase 2 of EPIC-002 has EN-303, EN-403, and EN-404), scores are tracked per-enabler (FR-307-012):

```yaml
iterations:
  - iteration: 2
    scores:
      EN-303: 0.928
      EN-403-404: 0.93
    delta:
      EN-303: +0.138
      EN-403-404: +0.11
```

### Phase-Level Aggregation

The phase-level quality score is the **minimum** of all enabler scores in that phase. This ensures no enabler can slip through with a low score while others compensate:

```python
def calculate_phase_quality_score(iteration_scores):
    """
    Phase quality = minimum of all enabler scores.
    All enablers must meet threshold individually.
    """
    return min(iteration_scores.values())
```

**Rationale:** Using minimum rather than average prevents a scenario where one enabler scores 0.98 and another scores 0.86, producing an average of 0.92 that passes the gate despite one enabler being below threshold.

**Trade-Off Analysis (EN-307-F002 Fix):**

| Approach | Pros | Cons |
|----------|------|------|
| **min** (selected) | No enabler can hide below threshold; strict quality enforcement per H-13 | In phases with many enablers, a single marginal enabler (e.g., 0.91) forces CONDITIONAL PASS for the entire phase even when 90%+ of work exceeds threshold |
| **avg** (rejected) | More forgiving for large phases; one weak enabler does not dominate | Allows averaging-up: one excellent enabler can compensate for one below threshold, violating the spirit of H-13 per-artifact quality |
| **weighted avg** (rejected) | Could weight by enabler complexity or criticality | Adds configuration complexity; weight selection is subjective |

**Decision:** `min` is the default and RECOMMENDED approach per H-13 ("quality gate score >= 0.92" applies to each artifact individually). The `min` function correctly models this per-artifact requirement at the phase level. The CONDITIONAL PASS path with user ratification (P-020) provides an escape valve for legitimate edge cases where one enabler is marginally below threshold (0.85-0.91).

**Configuration Note:** The aggregation method is NOT configurable by default. Changing from `min` would weaken the quality gate contract. If a future use case requires a different aggregation, it should be proposed as a constitutional amendment with justification for why per-artifact quality assurance can be relaxed.

### Metrics Section Update

The orch-tracker updates the global metrics section (FR-307-017):

```yaml
metrics:
  quality:
    adversarial_iterations_completed: 4
    adversarial_iterations_total: 6
    quality_scores:
      - enabler: "EN-302"
        iteration_1: 0.79
        iteration_2: 0.935
        validation: "CONDITIONAL PASS"
      - enabler: "EN-303"
        iteration_1: 0.79
        iteration_2: 0.928
        validation: "PASS"
```

---

## Pass/Fail Determination

### Quality Gate Decision Logic

The orch-tracker applies the following decision logic at each iteration and at phase completion (FR-307-013):

```python
def determine_quality_gate(score, iteration, max_iterations, criticality):
    """
    Determine quality gate status.

    Returns: PASS | CONDITIONAL_PASS | FAIL | CONTINUE
    """
    THRESHOLD = 0.92  # From quality-enforcement.md SSOT
    CONDITIONAL_THRESHOLD = 0.85

    if score >= THRESHOLD:
        return "PASS"

    if iteration < max_iterations:
        return "CONTINUE"  # More iterations available

    # Max iterations reached
    if score >= CONDITIONAL_THRESHOLD:
        return "CONDITIONAL_PASS"  # P-020: user ratification required

    return "FAIL"  # Blocker created
```

### Decision Matrix

| Score Range | At Max Iterations? | Result | Action |
|-------------|-------------------|--------|--------|
| >= 0.92 | Any | PASS | Mark complete, proceed |
| < 0.92 | No | CONTINUE | Next iteration |
| 0.85 - 0.91 | Yes | CONDITIONAL PASS | Request user ratification (P-020) |
| < 0.85 | Yes | FAIL | Create blocker, escalate |

### Verdict Recording

```yaml
# Phase-level verdict
phases:
  - id: 1
    quality_gate_result: "PASS"        # PASS | CONDITIONAL_PASS | FAIL
    quality_gate_score: 0.935
    quality_gate_iteration: 2          # Which iteration achieved the result

# In metrics
metrics:
  quality:
    gates_passed: 2
    gates_conditional: 1
    gates_failed: 0
```

---

## Escalation Protocol

### On CONDITIONAL PASS

When the quality gate results in CONDITIONAL PASS (score 0.85-0.91 after max iterations):

1. Record verdict in ORCHESTRATION.yaml
2. Log rationale in ORCHESTRATION_WORKTRACKER.md
3. **Request user ratification** per P-020 (User Authority)
4. Block downstream phases until user confirms

```yaml
quality_gate_result: "CONDITIONAL_PASS"
quality_gate_note: "Score 0.893 after 3 iterations. User ratification required per P-020."
awaiting_ratification: true
```

### On FAIL (FR-307-014)

When the quality gate FAILS (score < 0.85 after max iterations):

1. Create a blocker entry in `blockers.active`:

```yaml
blockers:
  active:
    - id: "BLK-QG-001"
      description: "Quality score 0.78 < 0.92 after 3 adversarial iterations for EN-XXX"
      blocking: ["phase-2-agents"]
      severity: "HIGH"
      escalation: "P-020 user review required"
      created: "2026-02-13T14:30:00Z"
      quality_details:
        enabler: "EN-XXX"
        final_score: 0.78
        threshold: 0.92
        iterations_completed: 3
```

2. Set the next phase to BLOCKED:

```yaml
phases:
  - id: 2
    status: "BLOCKED"
    blocked_by: "BLK-QG-001"
```

3. Record the failure in metrics
4. Escalate to human review

### Escalation Flow

```
Score < 0.92 after iteration 3
    |
    +---> Score >= 0.85?
    |         |
    |    +----+----+
    |    |         |
    |   YES        NO
    |    |         |
    |    v         v
    | CONDITIONAL  FAIL
    | PASS         |
    |    |         +---> Create blocker
    |    |         +---> Block next phase
    |    |         +---> Escalate to user
    |    |
    |    +---> Request user ratification
    |    +---> Block until confirmed
```

---

## Early Exit Logic

### Conditions for Early Exit

The orch-tracker evaluates early exit conditions after each iteration (FR-307-008):

```python
def should_early_exit(iteration, scores, findings_resolved, criticality, max_iterations):
    """
    Determine if remaining iterations can be SKIPPED.

    Returns True if all conditions met for early exit.

    Args:
        iteration: Current iteration number (1-based).
        scores: Dict of enabler_id -> quality score for this iteration.
        findings_resolved: Dict of enabler_id -> findings resolution string
            (e.g., "3/3 blocking, 5/5 major, 3/4 minor").
        criticality: Criticality level (C1, C2, C3, C4).
        max_iterations: Maximum allowed iterations.
    """
    THRESHOLD = 0.92

    # C4 criticality: always complete all iterations
    if criticality == "C4":
        return False

    # Not eligible until at least iteration 2
    if iteration < 2:
        return False

    # All enablers must meet threshold
    if not all(score >= THRESHOLD for score in scores.values()):
        return False

    # No blocking findings remaining (MANDATORY -- EN-307-F003 fix)
    # Parse findings_resolved strings to check for unresolved blocking findings.
    # A blocking finding is unresolved if resolved_count < total_count.
    if has_unresolved_blocking_findings(findings_resolved):
        return False

    return True


def has_unresolved_blocking_findings(findings_resolved):
    """
    Check if any enabler has unresolved blocking findings.

    Args:
        findings_resolved: Dict of enabler_id -> resolution string
            (e.g., "3/3 blocking, 5/5 major, 3/4 minor").

    Returns:
        True if any enabler has unresolved blocking findings.
    """
    for enabler_id, resolution_str in findings_resolved.items():
        # Parse "X/Y blocking" from the resolution string
        parts = resolution_str.split(",")
        for part in parts:
            part = part.strip()
            if "blocking" in part.lower():
                fraction = part.split("blocking")[0].strip()
                resolved, total = fraction.split("/")
                if int(resolved.strip()) < int(total.strip()):
                    return True
    return False
```

### SKIPPED Status Recording

When early exit triggers, remaining iterations are marked SKIPPED:

```yaml
iterations:
  - iteration: 1
    status: "COMPLETE"
    scores: { EN-302: 0.79 }
  - iteration: 2
    status: "COMPLETE"
    scores: { EN-302: 0.935 }
  - iteration: 3
    status: "SKIPPED"
    note: "All enablers achieved PASS at iteration 2, no iteration 3 needed"
    skip_rationale: "EN-302: 0.935 >= 0.92 threshold"
```

**Live example:** Groups 5-6 in the EPIC-002 ORCHESTRATION.yaml show `status: "SKIPPED"` with the note "Both pipelines achieved PASS at iteration 2, no iteration 3 needed".

---

## S-014 LLM-as-Judge Integration

### Scoring Protocol (IR-307-007)

S-014 LLM-as-Judge scoring is mandatory at every adversarial iteration (H-15). The protocol is:

1. **Critic agent** evaluates the artifact using its assigned strategies
2. **Critic agent** produces a numerical quality score (0.00 - 1.00) using S-014
3. **Score** is extracted from the critic's output artifact
4. **orch-tracker** records the score in the iteration's `scores` field
5. **orch-tracker** compares against `quality_gate_threshold` (0.92)

### Score Dimension Breakdown (IR-307-009)

When the S-014 scoring produces per-dimension scores, the orch-tracker records them:

```yaml
score_breakdown:
  EN-303:
    completeness: 0.95
    internal_consistency: 0.92    # CE-005 fix: canonical name per EN-304 TASK-003 SSOT
    evidence_quality: 0.88
    methodological_rigor: 0.90    # CE-005 fix: canonical name per EN-304 TASK-003 SSOT
    actionability: 0.94
    traceability: 0.96
    composite: 0.928
```

**Canonical Dimension Names (CE-005 SSOT):** All quality score dimensions MUST use the canonical names defined in EN-304 TASK-003: `completeness`, `internal_consistency`, `evidence_quality`, `methodological_rigor`, `actionability`, `traceability`. Shortened forms (`consistency`, `rigor`) are NOT permitted to avoid key mismatch during cross-iteration and cross-pipeline score comparison.

The composite score is the weighted average used for pass/fail determination. Individual dimension scores enable targeted improvement in revision iterations.

### Anti-Leniency Enforcement (IR-307-008)

The orch-tracker verifies that critic agents include anti-leniency calibration (H-16). If a critic's output lacks anti-leniency indicators, the orch-tracker logs a warning:

```yaml
quality_warnings:
  - iteration: 1
    agent: "ps-critic-301"
    warning: "Anti-leniency calibration indicator not found in critique output"
    severity: "MEDIUM"
```

### Evidence-Based Closure (IR-307-010)

An artifact cannot be marked COMPLETE without:
1. A quality score from S-014 (the score exists in `iterations[].scores`)
2. A validation verdict from ps-validator (the verdict exists in `validation_verdict`)

```python
def can_close_artifact(enabler, orchestration_state):
    """Check evidence-based closure requirements (V-060)."""
    has_score = enabler in orchestration_state.quality_scores
    has_verdict = enabler in orchestration_state.validation_verdicts
    return has_score and has_verdict
```

---

## Barrier Quality Gate

### Gate Enforcement at Barriers (FR-307-018)

At each sync barrier, the orch-tracker verifies that ALL upstream phases have achieved quality gate pass before allowing cross-pollination:

```python
def can_cross_barrier(barrier, orchestration_state):
    """
    Check if a barrier can be crossed.

    All upstream phases must have quality gate PASS or CONDITIONAL_PASS.
    """
    for phase_id in barrier.prerequisite_phases:
        phase = orchestration_state.get_phase(phase_id)

        if phase.quality_gate_result not in ("PASS", "CONDITIONAL_PASS"):
            return False

        if phase.quality_gate_result == "CONDITIONAL_PASS":
            if not phase.ratification_confirmed:
                return False  # Awaiting user ratification

    return True
```

### Barrier Quality Report

When a barrier is crossed, the orch-tracker generates a quality summary:

```yaml
barriers:
  - id: "barrier-1"
    status: "COMPLETE"
    quality_summary:
      upstream_phases: ["adv-phase-1", "enf-phase-1"]
      quality_scores:
        adv-phase-1: 0.935
        enf-phase-1: 0.92
      all_passed: true
      crossed_at: "2026-02-13T12:00:00Z"
```

---

## Finding Resolution Tracking

### Finding Categories

Findings from adversarial review are categorized by severity (FR-307-016):

| Severity | Description | Must Resolve Before Pass? |
|----------|-------------|--------------------------|
| BLOCKING | Prevents completion | Yes |
| MAJOR | Significant issue | Yes for PASS, No for CONDITIONAL PASS |
| MINOR | Improvement suggestion | No |

### Resolution Tracking

The orch-tracker tracks finding resolution across iterations:

```yaml
iterations:
  - iteration: 1
    findings_resolved:
      EN-303: "0/3 blocking, 0/5 major, 0/4 minor"
      EN-403-404: "0/4 blocking, 0/7 major, 0/5 minor"
  - iteration: 2
    findings_resolved:
      EN-303: "3/3 blocking, 5/5 major, 3/4 minor"
      EN-403-404: "4/4 blocking, 7/7 major, 5/5 minor"
```

### Resolution Requirements

For a PASS verdict:
- 100% of BLOCKING findings must be resolved
- 100% of MAJOR findings must be resolved
- MINOR findings are advisory (no resolution requirement)

For CONDITIONAL PASS:
- 100% of BLOCKING findings must be resolved
- MAJOR findings may have acceptable residual count

---

## Iteration Delta Tracking

### Delta Calculation (FR-307-015)

The orch-tracker calculates score deltas between iterations to measure adversarial review effectiveness:

```yaml
iterations:
  - iteration: 1
    scores: { EN-302: 0.79, EN-402: 0.81 }
  - iteration: 2
    scores: { EN-302: 0.935, EN-402: 0.92 }
    delta: { EN-302: +0.145, EN-402: +0.11 }
```

### Effectiveness Metrics

The delta tracking enables effectiveness analysis:

```yaml
metrics:
  quality:
    average_delta_iter_1_to_2: +0.128
    average_delta_iter_2_to_3: +0.02
    most_improved: "EN-302 (+0.145 in iteration 2)"
    strategies_most_effective: "S-002 Devil's Advocate (used in all iter-1 critiques)"
```

---

## State Update Protocol

### Extended Update Protocol

The orch-tracker's existing state update protocol is extended with quality tracking steps:

```
EXISTING PROTOCOL:
1. Read current ORCHESTRATION.yaml
2. Validate update request
3. Update agent status
4. Register artifact
5. Recalculate metrics
6. Create checkpoint if triggered
7. Write updated ORCHESTRATION.yaml
8. Update ORCHESTRATION_WORKTRACKER.md

NEW ADDITIONS (after step 3):
3a. If agent is a critic: extract quality score from artifact
3b. Record score in iterations[N].scores
3c. Calculate delta from previous iteration
3d. Update findings_resolved
3e. Evaluate quality gate (pass/fail/continue)
3f. If PASS: check early exit eligibility
3g. If early exit: mark remaining iterations SKIPPED
3h. If FAIL: create blocker, block next phase
3i. If CONDITIONAL PASS: request user ratification
3j. Update phase quality_scores and final_quality_score

NEW ADDITIONS (after step 5):
5a. Update metrics.quality section
5b. Update resumption.adversarial_feedback_status
```

### Atomic Update Guarantee

All quality-related updates MUST be atomic with the agent status update. The orch-tracker MUST NOT write partial quality state (e.g., score without verdict, or verdict without score).

---

## Live Example Analysis

### Mapping to EPIC-002 ORCHESTRATION.yaml

| Design Element | Live YAML Evidence | Location |
|----------------|-------------------|----------|
| Per-iteration scores | `scores: {EN-302: 0.79}`, `{EN-302: 0.935}` | Group 10 iterations |
| Score aggregation | `scores: {EN-303: 0.928, EN-403-404: 0.93}` | Group 10 iteration 2 |
| Phase quality scores | `quality_scores: [0.79, 0.935]` | Phase 1 definitions |
| Final quality score | `final_quality_score: 0.935` | Phase 1 definitions |
| Validation verdict | `validation_verdict: "CONDITIONAL PASS"` | Phase 1 definitions |
| Finding resolution | `findings_resolved: {EN-303: "3/3 blocking, 5/5 major, 3/4 minor"}` | Group 10 iteration 2 |
| Early exit (SKIPPED) | `status: "SKIPPED"`, `note: "Both pipelines achieved PASS..."` | Groups 5-6 |
| Quality metrics | `quality_scores` array in metrics | `metrics.quality` |
| Adversarial feedback status | `adversarial_feedback_status` | `resumption` |
| Blocker creation | (not triggered in live workflow -- all passed) | `blockers.active` (empty) |

---

## Traceability

### Synthesis Phase Quality Review Note (EN-307-F004 Fix)

The orch-synthesizer produces a final synthesis document summarizing the workflow's quality story. This synthesis is **exempt from the full adversarial review cycle** for the following reasons:

1. **Derivative artifact:** The synthesis is a summary of already-reviewed artifacts. Each input artifact has already passed the >= 0.92 quality gate through adversarial review. The synthesis adds no new claims that are not traceable to reviewed sources.
2. **Diminishing returns:** Applying a full S-002/S-012/S-014 pipeline to the synthesis would add an additional iteration cycle without proportional quality benefit, since the underlying quality data has already been validated.
3. **Scope:** The synthesis phase is an aggregation activity, not a creation activity. It does not produce new requirements, designs, or specifications.

**Mitigation:** The orch-synthesizer SHOULD apply S-014 LLM-as-Judge as a lightweight self-scoring step (not a full adversarial cycle) to verify that the synthesis accurately reflects the underlying quality data. This self-score is recorded in metrics but does NOT trigger the full pass/fail/escalation protocol. If the self-score < 0.85, the orch-tracker flags the synthesis for human review.

### Requirement Coverage

| Requirement | Design Section | Status |
|-------------|---------------|--------|
| FR-307-011 | Quality Score Recording | Covered |
| FR-307-012 | Score Aggregation | Covered |
| FR-307-013 | Pass/Fail Determination | Covered |
| FR-307-014 | Escalation Protocol | Covered |
| FR-307-015 | Iteration Delta Tracking | Covered |
| FR-307-016 | Finding Resolution Tracking | Covered |
| FR-307-017 | Score Aggregation (metrics) | Covered |
| FR-307-018 | Barrier Quality Gate | Covered |
| IR-307-007 | S-014 LLM-as-Judge Integration | Covered |
| IR-307-008 | S-014 LLM-as-Judge Integration (anti-leniency) | Covered |
| IR-307-009 | S-014 LLM-as-Judge Integration (dimensions) | Covered |
| IR-307-010 | S-014 LLM-as-Judge Integration (evidence-based closure) | Covered |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | FEAT-004:EN-307:TASK-001 (Requirements) | FR-307-011 through FR-307-018, IR-307-007 through IR-307-010 |
| 2 | FEAT-004:EN-307:TASK-002 (Planner Design) | Schema additions, iteration structure, strategy assignment |
| 3 | ADR-EPIC002-001 (EN-302 TASK-005) | S-014 LLM-as-Judge rank 1, quality layers |
| 4 | Barrier-2 ENF-to-ADV Handoff | H-13, H-14, H-15, H-16, H-17, SSOT |
| 5 | Live ORCHESTRATION.yaml (epic002-crosspoll-20260213-001) | Quality metrics, iteration scores, finding resolution |
| 6 | orch-tracker agent spec v2.1.0 | Current state update protocol, checkpoint creation |

---

*Document ID: FEAT-004:EN-307:TASK-003*
*Agent: ps-architect-307*
*Created: 2026-02-13*
*Status: Complete*
