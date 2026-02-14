# TASK-001: Requirements for Orchestration Adversarial Enhancement

<!--
DOCUMENT-ID: FEAT-004:EN-307:TASK-001
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
> **Purpose:** Define formal requirements for enhancing the /orchestration skill to automatically embed adversarial feedback loops in workflow plans

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this requirements document delivers |
| [Functional Requirements: Auto-Generation](#functional-requirements-auto-generation) | FR-307-001 through FR-307-010: Automatic creator-critic-revision cycle generation |
| [Functional Requirements: Quality Gate Tracking](#functional-requirements-quality-gate-tracking) | FR-307-011 through FR-307-018: Quality score tracking and enforcement at sync barriers |
| [Functional Requirements: Adversarial Synthesis](#functional-requirements-adversarial-synthesis) | FR-307-019 through FR-307-024: Adversarial-aware synthesis capabilities |
| [Integration Requirements: Enforcement Hooks](#integration-requirements-enforcement-hooks) | IR-307-001 through IR-307-006: Integration with barrier-2 enforcement designs |
| [Integration Requirements: Quality Scoring](#integration-requirements-quality-scoring) | IR-307-007 through IR-307-010: S-014 LLM-as-Judge scoring integration |
| [Non-Functional Requirements](#non-functional-requirements) | NFR-307-001 through NFR-307-008: Backward compatibility, performance, portability |
| [Traceability](#traceability) | Mapping to EN-302, EN-303, barrier-2, and ADR-EPIC002-001 |
| [References](#references) | Source citations |

---

## Summary

This document defines the formal requirements for enhancing the /orchestration skill to automatically embed adversarial feedback loops into workflow plans. Currently, adversarial review only occurs when a user explicitly requests it. After this enhancement, the orch-planner will automatically generate creator-critic-revision cycles, the orch-tracker will track quality scores at sync barriers, and the orch-synthesizer will incorporate adversarial findings into final outputs.

The requirements are organized into three functional categories (auto-generation, quality gate tracking, adversarial synthesis), two integration categories (enforcement hooks, quality scoring), and one non-functional category (backward compatibility, performance, portability).

**Key design input:** The current EPIC-002 ORCHESTRATION.yaml (workflow `epic002-crosspoll-20260213-001`) is a live example of what the enhanced skill should produce automatically. It already contains `adversarial_iteration_min: 3`, `quality_gate_threshold: 0.92`, and execution queue groups that implement creator-critic-revision cycles (Groups 2-6 for Phase 1, Group 10 for Phase 2). The enhancement formalizes these patterns as automatic defaults rather than manual configuration.

---

## Functional Requirements: Auto-Generation

### FR-307-001: Automatic Adversarial Cycle Detection

The orch-planner MUST automatically detect which workflow phases require adversarial feedback loops based on the following criteria:

| Criterion | Trigger | Source |
|-----------|---------|--------|
| Artifact type is TGT-ARCH, TGT-DEC, TGT-REQ, TGT-RES, TGT-PROC | Always inject adversarial cycle | EN-303 TASK-001 Dimension 1 |
| Artifact type is TGT-CODE | Inject adversarial cycle if C2+ criticality | EN-303 TASK-001 Dimension 3 |
| Decision criticality is C3 or C4 | Always inject full adversarial cycle | ADR-EPIC002-001, barrier-2 handoff |
| Phase produces deliverables consumed by downstream phases | Inject adversarial cycle to prevent error propagation | EN-307 enabler specification |

**Enforcement tier:** HARD

### FR-307-002: Creator-Critic-Revision Pattern Injection

For each phase requiring adversarial review, the orch-planner MUST generate the following execution queue structure:

```
Group N:   Creator agents (PARALLEL)
Group N+1: Critic agents - Iteration 1 (PARALLEL, blocked_by: Group N)
Group N+2: Creator revision - Iteration 1 (PARALLEL, blocked_by: Group N+1)
Group N+3: Critic agents - Iteration 2 (PARALLEL, blocked_by: Group N+2)
Group N+4: Creator revision - Iteration 2 (PARALLEL, blocked_by: Group N+3)
Group N+5: Critic agents - Iteration 3 / Final scoring (PARALLEL, blocked_by: Group N+4)
Group N+6: Validation (PARALLEL, blocked_by: Group N+5)
```

This pattern mirrors the execution queue structure in the live EPIC-002 ORCHESTRATION.yaml (Groups 1-7 for Phase 1, Groups 9-10a for Phase 2).

**Enforcement tier:** HARD

### FR-307-003: Minimum Iteration Count

The orch-planner MUST enforce a minimum of 3 creator-critic-revision iterations per adversarial cycle. This corresponds to `adversarial_iteration_min: 3` in the ORCHESTRATION.yaml constraints section.

**Exception:** If the quality score reaches >= 0.92 at iteration 2, iteration 3 MAY be SKIPPED (as demonstrated by EN-302 and EN-402 in the live workflow). The SKIPPED status MUST be recorded with rationale.

**Enforcement tier:** HARD
**Source:** Barrier-2 ENF-to-ADV handoff (H-14: "Minimum 3 creator-critic iterations REQUIRED")

### FR-307-004: Strategy Assignment by Criticality

The orch-planner MUST assign adversarial strategies to critic agents based on the decision criticality level:

| Criticality | Iteration 1 Strategy | Iteration 2 Strategy | Iteration 3 Strategy |
|-------------|---------------------|---------------------|---------------------|
| C1 | S-010 Self-Refine | S-014 LLM-as-Judge (optional) | -- |
| C2 | S-002 Devil's Advocate | S-007 Constitutional AI + S-014 LLM-as-Judge | S-003 Steelman + S-014 |
| C3 | S-002 DA + S-004 Pre-Mortem | S-007 + S-012 FMEA + S-013 Inversion | S-001 Red Team + S-014 |
| C4 | All 10 strategies (phased) | All 10 strategies (phased) | All 10 strategies + S-014 final scoring |

**Source:** EN-303 TASK-001 Dimension 3 (Strategy Allocation by Criticality), ADR-EPIC002-001

**Enforcement tier:** MEDIUM (strategy selection is advisory; critic agent MAY adapt based on findings)

### FR-307-005: Adversarial Agent Specification in ORCHESTRATION.yaml

For each critic agent in the execution queue, the orch-planner MUST specify the `adversarial_strategies` field listing which strategies the critic agent should employ. This field is already present in the live ORCHESTRATION.yaml:

```yaml
- id: "ps-critic-302"
  adversarial_strategies: ["S-002 Devil's Advocate", "S-005 Dialectical Inquiry", "S-014 LLM-as-Judge"]
```

**Enforcement tier:** HARD

### FR-307-006: Quality Gate Threshold in Workflow Constraints

The orch-planner MUST include the quality gate threshold in the ORCHESTRATION.yaml `workflow.constraints` section:

```yaml
constraints:
  quality_gate_threshold: 0.92
  adversarial_iteration_min: 3
  adversarial_validation: true
```

**Source:** Barrier-2 ENF-to-ADV handoff (H-13: "Quality gate score >= 0.92 REQUIRED"), quality-enforcement.md SSOT

**Enforcement tier:** HARD

### FR-307-007: Iteration Score Tracking in Execution Queue

The orch-planner MUST generate execution queue groups that include iteration-level score tracking fields:

```yaml
iterations:
  - iteration: 1
    status: "PENDING"
    critique_agents: []
    revision_agents: []
    scores: {}
    findings_resolved: {}
  - iteration: 2
    status: "PENDING"
    ...
  - iteration: 3
    status: "PENDING"
    ...
```

This mirrors the `iterations` structure in Group 10 of the live ORCHESTRATION.yaml.

**Enforcement tier:** HARD

### FR-307-008: Early Exit on Quality Gate Pass

The orch-planner MUST generate execution queue logic that allows early exit from the adversarial cycle when the quality gate threshold (>= 0.92) is met before the maximum iteration count. The SKIPPED status MUST be used for bypassed iterations:

```yaml
- iteration: 3
  status: "SKIPPED"
  note: "Both pipelines achieved PASS at iteration 2, no iteration 3 needed"
```

**Source:** Live ORCHESTRATION.yaml Groups 5-6 (SKIPPED)

**Enforcement tier:** MEDIUM

### FR-307-009: Adversarial Feedback Status in Resumption Context

The orch-planner MUST generate a `resumption.adversarial_feedback_status` section in ORCHESTRATION.yaml tracking:

```yaml
adversarial_feedback_status:
  total_enablers: N
  enablers_complete: N
  enablers_validated: N
  current_enabler: "string"
  current_iteration: "N/A | 1 | 2 | 3"
  iterations_complete: N
  iterations_total: N
```

**Source:** Live ORCHESTRATION.yaml resumption section

**Enforcement tier:** HARD

### FR-307-010: Validation Agent Auto-Injection

The orch-planner MUST automatically inject a validation agent (ps-validator) after each adversarial cycle. The validator confirms all acceptance criteria are met and produces a validation report with a quality verdict (PASS / CONDITIONAL PASS / FAIL).

**Source:** Live ORCHESTRATION.yaml Groups 7 and 10a

**Enforcement tier:** HARD

---

## Functional Requirements: Quality Gate Tracking

### FR-307-011: Quality Score Recording at Phase Completion

The orch-tracker MUST record quality scores at phase completion in the phase definition:

```yaml
quality_scores: [0.79, 0.935]
final_quality_score: 0.935
validation_verdict: "CONDITIONAL PASS"
```

**Source:** Live ORCHESTRATION.yaml phase 1 definitions

**Enforcement tier:** HARD

### FR-307-012: Quality Score Aggregation Across Artifacts

The orch-tracker MUST aggregate quality scores across multiple artifacts within a phase. When a phase contains multiple enablers (e.g., Phase 2 has EN-403 and EN-404), scores MUST be tracked per-enabler:

```yaml
scores:
  EN-303: 0.928
  EN-403-404: 0.93
```

**Source:** Live ORCHESTRATION.yaml Group 10 iterations

**Enforcement tier:** HARD

### FR-307-013: Quality Gate Pass/Fail Determination

The orch-tracker MUST determine quality gate pass/fail based on:
- Score >= 0.92: **PASS**
- Score >= 0.85 AND < 0.92 after max iterations: **CONDITIONAL PASS** (user ratification required per P-020)
- Score < 0.85 after max iterations: **FAIL** (blocker created)

**Source:** Barrier-2 ENF-to-ADV handoff (H-13, H-15), ADR-EPIC002-001

**Enforcement tier:** HARD

### FR-307-014: Escalation Protocol on Quality Gate Failure

When the quality gate fails after the maximum iteration count (3), the orch-tracker MUST:

1. Create a blocker entry in `blockers.active`
2. Set the next phase to BLOCKED
3. Record the failure in `metrics.quality.quality_scores`
4. Escalate to human review per P-020 (User Authority)

```yaml
blockers:
  active:
    - id: "BLK-QG-001"
      description: "Quality score < 0.92 after 3 adversarial iterations for EN-XXX"
      blocking: ["next-phase-agents"]
      severity: "HIGH"
      escalation: "P-020 user review required"
```

**Enforcement tier:** HARD

### FR-307-015: Iteration Delta Tracking

The orch-tracker MUST track the score delta between iterations to measure adversarial review effectiveness:

```yaml
iterations:
  - iteration: 1
    scores: { EN-302: 0.79 }
  - iteration: 2
    scores: { EN-302: 0.935 }
    delta: { EN-302: +0.145 }
```

**Enforcement tier:** MEDIUM

### FR-307-016: Finding Resolution Tracking

The orch-tracker MUST track finding resolution across iterations:

```yaml
findings_resolved:
  EN-303: "3/3 blocking, 5/5 major, 3/4 minor"
  EN-403-404: "4/4 blocking, 7/7 major, 5/5 minor"
```

**Source:** Live ORCHESTRATION.yaml Group 10 iterations

**Enforcement tier:** MEDIUM

### FR-307-017: Quality Metrics in Metrics Section

The orch-tracker MUST maintain cumulative quality metrics:

```yaml
metrics:
  quality:
    adversarial_iterations_completed: N
    adversarial_iterations_total: N
    quality_scores:
      - enabler: "EN-XXX"
        iteration_1: 0.XX
        iteration_2: 0.XX
        validation: "PASS | CONDITIONAL PASS | FAIL"
```

**Source:** Live ORCHESTRATION.yaml metrics.quality section

**Enforcement tier:** HARD

### FR-307-018: Barrier Quality Gate

At each sync barrier, the orch-tracker MUST verify that all upstream phases have achieved quality gate pass (>= 0.92) before allowing cross-pollination. Barriers MUST NOT be crossed if any upstream phase has a quality score below threshold.

**Enforcement tier:** HARD

---

## Functional Requirements: Adversarial Synthesis

### FR-307-019: Adversarial Findings in Synthesis

The orch-synthesizer MUST include adversarial review findings as a first-class section in the final synthesis document:

```markdown
## Adversarial Review Summary

| Enabler | Iterations | Final Score | Key Findings | Resolution |
|---------|-----------|-------------|--------------|------------|
```

**Enforcement tier:** HARD

### FR-307-020: Quality Score Trend Analysis

The orch-synthesizer MUST produce a quality score trend analysis showing improvement across iterations for each enabler, demonstrating the effectiveness of the adversarial review process.

**Enforcement tier:** MEDIUM

### FR-307-021: Cross-Pipeline Adversarial Pattern Extraction

The orch-synthesizer MUST extract and document recurring adversarial findings across pipelines at each barrier. Patterns that appear in multiple enablers indicate systemic issues.

**Enforcement tier:** MEDIUM

### FR-307-022: Adversarial Strategy Effectiveness Report

The orch-synthesizer MUST report which adversarial strategies produced the most impactful findings, enabling calibration of strategy selection for future workflows.

**Enforcement tier:** MEDIUM

### FR-307-023: Residual Risk Documentation

The orch-synthesizer MUST document residual risks identified by adversarial review that were accepted (CONDITIONAL PASS) or deferred, with mitigation plans.

**Enforcement tier:** HARD

### FR-307-024: Lessons Learned from Adversarial Cycles

The orch-synthesizer MUST capture lessons learned about the adversarial review process itself, including:
- Which strategies were most effective for which artifact types
- Iteration count statistics (how many cycles were needed on average)
- Common finding categories and their resolution patterns

**Enforcement tier:** MEDIUM

---

## Integration Requirements: Enforcement Hooks

### IR-307-001: C1-C4 Criticality Integration

The orch-planner MUST integrate the C1-C4 criticality framework from the barrier-2 ENF-to-ADV handoff into adversarial cycle configuration. Criticality assessment determines:
- Which strategies are assigned to critic agents (FR-307-004)
- How many iterations are budgeted (FR-307-003)
- Whether human escalation is required (FR-307-014)

**Source:** Barrier-2 ENF-to-ADV handoff, Section "Criticality Assessment (C1-C4)"

**Enforcement tier:** HARD

### IR-307-002: Quality-Enforcement.md SSOT Consumption

The orch-planner MUST read quality gate threshold, iteration minimums, and tier vocabulary from the `quality-enforcement.md` SSOT file rather than hardcoding values. This ensures consistency across all consumers (hooks, rules, skills).

**Source:** Barrier-2 ENF-to-ADV handoff, Section "quality-enforcement.md (SSOT)"

**Enforcement tier:** HARD

### IR-307-003: L2-REINJECT Tag Awareness

The orchestration templates SHOULD include L2-REINJECT tags for adversarial review reminders in generated workflow plans, enabling the PromptReinforcementEngine to reinforce adversarial quality expectations:

```html
<!-- L2-REINJECT: rank=3, tokens=30, content="Quality gate >= 0.92. Min 3 adversarial iterations. S-014 LLM-as-Judge scoring REQUIRED." -->
```

**Source:** Barrier-2 ENF-to-ADV handoff, Section "L2-REINJECT Tag Integration"

**Enforcement tier:** MEDIUM

### IR-307-004: Adversarial Pattern in ORCHESTRATION.yaml Patterns List

The orch-planner MUST include `ADVERSARIAL_FEEDBACK` in the `workflow.patterns` list when adversarial cycles are present (already demonstrated in live ORCHESTRATION.yaml):

```yaml
patterns:
  - ADVERSARIAL_FEEDBACK
```

**Enforcement tier:** HARD

### IR-307-005: Defense-in-Depth Layer Mapping

The orchestration plan MUST document which enforcement layers (L1-L5 + Process) are available for each adversarial strategy in the workflow, enabling graceful degradation on platforms without hooks.

**Source:** Barrier-2 ENF-to-ADV handoff, Section "5-Layer Architecture Update"; EN-303 TASK-003 Enforcement Layer Mapping

**Enforcement tier:** MEDIUM

### IR-307-006: Token Budget Awareness

The orch-planner SHOULD estimate cumulative token budget for adversarial cycles at each criticality level and warn when the total exceeds the context window capacity. The token costs per strategy are defined in EN-303 TASK-003.

**Source:** EN-303 TASK-003 Cumulative Token Budget Verification; Barrier-2 ENF-to-ADV handoff, Section "Token Budget Summary"

**Enforcement tier:** MEDIUM

---

## Integration Requirements: Quality Scoring

### IR-307-007: S-014 LLM-as-Judge Scoring Protocol

The orch-tracker MUST enforce S-014 LLM-as-Judge scoring at every adversarial iteration. The scoring protocol is:

1. Critic agent evaluates artifact using assigned strategies
2. Critic agent produces a numerical quality score (0.00-1.00) using S-014
3. Score is recorded in the iteration's `scores` field
4. Score is compared against `quality_gate_threshold` (0.92)

**Source:** ADR-EPIC002-001 (S-014 rank 1); Barrier-2 ENF-to-ADV handoff (H-15: "S-014 LLM-as-Judge scoring REQUIRED")

**Enforcement tier:** HARD

### IR-307-008: Anti-Leniency Calibration

The orchestration templates MUST include anti-leniency calibration instructions for critic agents. The PromptReinforcementEngine ContentBlock `leniency-calibration` (~25 tokens) provides the calibration text.

**Source:** Barrier-2 ENF-to-ADV handoff (H-16: "Anti-leniency calibration REQUIRED"), ContentBlock system

**Enforcement tier:** HARD

### IR-307-009: Score Dimension Breakdown

The orch-tracker SHOULD support per-dimension score breakdown when available from S-014:

```yaml
score_breakdown:
  completeness: 0.95
  consistency: 0.92
  evidence_quality: 0.88
  rigor: 0.90
  actionability: 0.94
  traceability: 0.96
```

**Enforcement tier:** MEDIUM

### IR-307-010: Evidence-Based Closure Integration

The orch-tracker MUST enforce evidence-based closure (V-060) for each adversarial cycle: artifacts cannot be marked COMPLETE without a quality score from S-014 and a validation verdict from ps-validator.

**Source:** Barrier-2 ENF-to-ADV handoff (H-17: "Evidence-based closure REQUIRED")

**Enforcement tier:** HARD

---

## Non-Functional Requirements

### NFR-307-001: Backward Compatibility

The enhanced orchestration skill MUST remain backward compatible with existing workflows that do not use adversarial feedback loops. Workflows without `adversarial_validation: true` in constraints MUST function identically to the pre-enhancement behavior.

**Enforcement tier:** HARD

### NFR-307-002: Opt-Out Mechanism

Users MUST be able to opt out of automatic adversarial cycle injection for specific phases via explicit configuration:

```yaml
phases:
  - id: 1
    adversarial_review: false  # Explicit opt-out
```

**Source:** P-020 (User Authority)

**Enforcement tier:** HARD

### NFR-307-003: Default-On Behavior

For new workflows created after this enhancement, adversarial feedback loops MUST be enabled by default. The default configuration is:
- `adversarial_validation: true`
- `quality_gate_threshold: 0.92`
- `adversarial_iteration_min: 3`

**Enforcement tier:** HARD

### NFR-307-004: Template Compatibility

Enhanced templates MUST be valid YAML/Markdown that can be parsed by existing tooling. No new dependencies beyond stdlib.

**Enforcement tier:** HARD

### NFR-307-005: P-003 Compliance

All adversarial cycle patterns MUST comply with P-003 (No Recursive Subagents). Critic agents are workers invoked by the orchestrator, not subagents of creator agents.

```
Orchestrator → Creator (worker)
Orchestrator → Critic (worker)
Orchestrator → Validator (worker)
```

**Enforcement tier:** HARD (Constitutional)

### NFR-307-006: Platform Portability

The adversarial loop patterns MUST work on all platforms (PLAT-CC, PLAT-CC-WIN, PLAT-GENERIC). Enforcement intensity degrades gracefully per the ENF-MIN handling rules in EN-303 TASK-003.

**Enforcement tier:** MEDIUM

### NFR-307-007: Documentation Completeness

All new adversarial loop patterns MUST be documented in SKILL.md, PLAYBOOK.md, and agent specs before the enhancement is considered complete.

**Enforcement tier:** HARD

### NFR-307-008: Live Example Consistency

The enhancement documentation MUST reference the EPIC-002 ORCHESTRATION.yaml as a live example, demonstrating that the patterns being formalized are already proven in production use.

**Enforcement tier:** MEDIUM

---

## Traceability

### Upstream Dependencies

| Source | What It Provides | Requirements Informed |
|--------|-----------------|----------------------|
| ADR-EPIC002-001 (EN-302 TASK-005) | 10 selected strategies, C1-C4 criticality, quality layers L0-L4 | FR-307-004, IR-307-001 |
| EN-303 TASK-001 | 8-dimension context taxonomy, strategy allocation by criticality | FR-307-001, FR-307-004 |
| EN-303 TASK-003 | Per-strategy applicability profiles, token budgets, enforcement layer mapping | IR-307-006, NFR-307-006 |
| Barrier-2 ENF-to-ADV handoff | Hook designs, HARD rules H-13 through H-18, SSOT, L2-REINJECT tags | IR-307-001 through IR-307-008 |
| Live ORCHESTRATION.yaml | Proven adversarial patterns (Groups 1-10a, iterations, quality scores) | FR-307-002 through FR-307-010, FR-307-011 through FR-307-017 |

### Downstream Consumers

| Consumer | What It Needs |
|----------|--------------|
| TASK-002 (orch-planner adversarial design) | FR-307-001 through FR-307-010, IR-307-001 through IR-307-006 |
| TASK-003 (orch-tracker quality gate design) | FR-307-011 through FR-307-018, IR-307-007 through IR-307-010 |
| TASK-004 (orch-planner spec) | All FR-307-0xx requirements |
| TASK-005 (orch-tracker spec) | All FR-307-01x requirements, all IR-307-0xx |
| TASK-006 (orch-synthesizer spec) | FR-307-019 through FR-307-024 |
| TASK-007/008/009 (documentation and templates) | All requirements for documentation completeness |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | ADR-EPIC002-001 (ACCEPTED) -- FEAT-004:EN-302:TASK-005 | Strategy selection, C1-C4 criticality, quality layers |
| 2 | EN-303 TASK-001 -- FEAT-004:EN-303:TASK-001 | 8-dimension context taxonomy, strategy allocation |
| 3 | EN-303 TASK-003 -- FEAT-004:EN-303:TASK-003 | Per-strategy applicability profiles, token budgets, enforcement layer mapping |
| 4 | Barrier-2 ENF-to-ADV Handoff -- EPIC002-CROSSPOLL-B2-ENF-TO-ADV | Hook designs, HARD rules, SSOT, L2-REINJECT, 5-layer architecture |
| 5 | Live ORCHESTRATION.yaml -- PROJ-001-ORCH-STATE v2.0 | Proven adversarial patterns, execution queue structure, quality metrics |
| 6 | EN-307 Enabler Specification -- FEAT-004:EN-307 | Problem statement, technical approach, acceptance criteria |

---

*Document ID: FEAT-004:EN-307:TASK-001*
*Agent: ps-architect-307*
*Created: 2026-02-13*
*Status: Complete*
