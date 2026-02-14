# TASK-002: Adversarial Loop Integration Design for orch-planner

<!--
DOCUMENT-ID: FEAT-004:EN-307:TASK-002
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
> **Purpose:** Design how orch-planner automatically detects adversarial cycle needs and injects creator-critic-revision patterns into generated orchestration plans

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this design delivers |
| [Adversarial Cycle Detection](#adversarial-cycle-detection) | How orch-planner decides which phases need adversarial cycles |
| [Creator-Critic-Revision Pattern Injection](#creator-critic-revision-pattern-injection) | How execution queue groups are auto-generated |
| [Strategy Selection Logic](#strategy-selection-logic) | Which adversarial strategies are assigned per workflow context |
| [Criticality Integration](#criticality-integration) | C1-C4 criticality level integration from barrier-2 |
| [Quality Threshold Enforcement](#quality-threshold-enforcement) | Quality gate >= 0.92 enforcement design |
| [Iteration Minimum Enforcement](#iteration-minimum-enforcement) | Minimum 3 iteration enforcement with early exit |
| [Progressive Escalation (S-015)](#progressive-escalation-s-015) | Graduated escalation across iterations |
| [ORCHESTRATION.yaml Schema Additions](#orchestrationyaml-schema-additions) | New fields required in the state schema |
| [Algorithm: Plan Generation](#algorithm-plan-generation) | Pseudocode for the complete auto-generation algorithm |
| [Live Example Analysis](#live-example-analysis) | Mapping the design to the EPIC-002 ORCHESTRATION.yaml |
| [Traceability](#traceability) | Mapping to requirements and upstream sources |
| [References](#references) | Source citations |

---

## Summary

This document designs how the orch-planner agent will automatically detect which workflow phases require adversarial feedback loops and inject creator-critic-revision patterns into the generated orchestration plan. The design covers six key areas:

1. **Detection logic** -- How orch-planner determines whether a phase needs adversarial review based on artifact type, decision criticality, and downstream consumption
2. **Pattern injection** -- How execution queue groups are structured to implement creator-critic-revision cycles
3. **Strategy selection** -- Which of the 10 selected adversarial strategies (ADR-EPIC002-001) are assigned to critic agents based on context
4. **Criticality integration** -- How C1-C4 criticality levels from the barrier-2 ENF-to-ADV handoff determine review intensity
5. **Quality enforcement** -- How the >= 0.92 quality gate threshold is encoded and enforced
6. **Iteration management** -- How the minimum 3 iterations and early exit conditions work

The design uses the live EPIC-002 ORCHESTRATION.yaml as its primary reference implementation, formalizing the patterns already proven in production use.

---

## Adversarial Cycle Detection

### Detection Algorithm

When orch-planner generates a new orchestration plan, it evaluates each phase against three detection criteria. If any criterion triggers, the phase receives an adversarial cycle.

#### Criterion 1: Artifact Type (EN-303 Dimension 1)

| Artifact Type | Code | Always Inject? | Condition |
|---------------|------|----------------|-----------|
| Architecture Decision | TGT-ARCH | Yes | -- |
| Design Decision | TGT-DEC | Yes | -- |
| Requirements | TGT-REQ | Yes | -- |
| Research/Analysis | TGT-RES | Yes | -- |
| Process Definition | TGT-PROC | Yes | -- |
| Code/Implementation | TGT-CODE | Conditional | Only if C2+ criticality |

**Source:** FR-307-001, EN-303 TASK-001 Dimension 1

#### Criterion 2: Decision Criticality (EN-303 Dimension 3)

| Criticality | Level | Always Inject? |
|-------------|-------|----------------|
| C1 (Routine) | Low | No -- only if other criteria trigger |
| C2 (Significant) | Medium | Yes |
| C3 (Major) | High | Yes (full cycle) |
| C4 (Critical) | Maximum | Yes (full cycle, all strategies) |

**Source:** FR-307-001, ADR-EPIC002-001

#### Criterion 3: Downstream Consumption

If a phase produces deliverables that are consumed by downstream phases (cross-barrier propagation, phase dependency), adversarial review is injected to prevent error propagation. This is assessed by examining the execution queue dependency graph.

**Source:** FR-307-001, EN-307 enabler specification

### Detection Pseudocode

```python
def should_inject_adversarial_cycle(phase, workflow_config):
    """Determine if a phase needs adversarial feedback loop."""

    # Criterion 1: Artifact type
    always_review_types = {TGT_ARCH, TGT_DEC, TGT_REQ, TGT_RES, TGT_PROC}
    if phase.artifact_type in always_review_types:
        return True

    # Criterion 1b: Code at C2+
    if phase.artifact_type == TGT_CODE and phase.criticality >= C2:
        return True

    # Criterion 2: Decision criticality
    if phase.criticality >= C2:
        return True

    # Criterion 3: Downstream consumption
    if has_downstream_consumers(phase, workflow_config):
        return True

    # Default: check workflow-level setting
    return workflow_config.constraints.get("adversarial_validation", True)
```

### Opt-Out Mechanism

Per NFR-307-002 (P-020 User Authority), users can explicitly disable adversarial injection for specific phases:

```yaml
phases:
  - id: 1
    name: "Quick research"
    adversarial_review: false  # Explicit opt-out
```

When `adversarial_review: false` is set, the detection algorithm returns `False` regardless of other criteria.

---

## Creator-Critic-Revision Pattern Injection

### Execution Queue Structure

When a phase requires adversarial review, the orch-planner generates the following execution queue group pattern:

```
Group N:     Creator agents        (PARALLEL, produces initial artifacts)
Group N+1:   Critic - Iteration 1  (PARALLEL, blocked_by: Group N)
Group N+2:   Revision - Iteration 1 (PARALLEL, blocked_by: Group N+1)
Group N+3:   Critic - Iteration 2  (PARALLEL, blocked_by: Group N+2)
Group N+4:   Revision - Iteration 2 (PARALLEL, blocked_by: Group N+3)
Group N+5:   Critic - Iteration 3  (PARALLEL, blocked_by: Group N+4)
Group N+6:   Validation            (PARALLEL, blocked_by: Group N+5)
```

This mirrors the proven pattern in the live EPIC-002 ORCHESTRATION.yaml:
- Groups 1-7 implement Phase 1 (creator -> iter 1 critic -> iter 1 revision -> iter 2 critic -> iter 2 revision -> validation -> cross-poll)
- Groups 9-10a implement Phase 2 with a condensed iteration structure

### Group Metadata

Each generated group includes metadata enabling the orch-tracker to manage the adversarial cycle:

```yaml
execution_queue:
  groups:
    - id: 2
      name: "Phase 1 - Adversarial Iteration 1 (Critic)"
      execution_mode: "PARALLEL"
      blocked_by: [1]
      adversarial_context:
        cycle_phase: "critic"
        iteration: 1
        max_iterations: 3
        quality_threshold: 0.92
        strategies: ["S-002", "S-007", "S-014"]
      agents:
        - id: "ps-critic-301"
          role: "critic"
          adversarial_strategies: ["S-002 Devil's Advocate", "S-014 LLM-as-Judge"]
          target_artifacts: ["ps-architect-301/artifact.md"]
```

### Agent Pairing Rules

For each creator agent, the orch-planner generates a corresponding critic agent:

| Creator Agent | Critic Agent Pattern | Naming Convention |
|---------------|---------------------|-------------------|
| ps-architect-{NNN} | ps-critic-{NNN} | Same numeric suffix |
| ps-researcher-{NNN} | ps-critic-{NNN} | Same numeric suffix |
| nse-requirements-{NNN} | nse-critic-{NNN} or ps-critic-{NNN} | Same numeric suffix |

**Rule:** Critic agents are distinct agents from creators. They are NOT the same agent running in a different mode (P-003 compliance -- all are workers of the orchestrator).

### Validation Agent Injection

After the final adversarial iteration, a ps-validator agent is automatically injected (FR-307-010):

```yaml
- id: 7
  name: "Phase 1 - Validation"
  execution_mode: "PARALLEL"
  blocked_by: [6]
  adversarial_context:
    cycle_phase: "validation"
    iteration: "final"
  agents:
    - id: "ps-validator-301"
      role: "validator"
      target_artifacts: ["all_phase_1_artifacts"]
      validation_criteria: "acceptance_criteria_from_enabler"
```

---

## Strategy Selection Logic

### Strategy Pool

The 10 selected strategies from ADR-EPIC002-001 are the candidate pool:

| Strategy | Code | Token Cost | Primary Use |
|----------|------|------------|-------------|
| LLM-as-Judge | S-014 | 4,000-8,000 | Scoring (every iteration) |
| Steelman | S-003 | 3,000-7,500 | Strengthening arguments |
| Inversion | S-013 | 2,000-6,000 | Reverse assumption testing |
| Constitutional AI | S-007 | 3,500-7,500 | Rule compliance checking |
| Devil's Advocate | S-002 | 2,500-6,000 | Challenging assumptions |
| Pre-Mortem | S-004 | 3,000-8,000 | Failure scenario analysis |
| Self-Refine | S-010 | 1,600-2,100 | Self-improvement (C1 only) |
| FMEA | S-012 | 5,000-16,000 | Failure mode analysis |
| CoVe | S-011 | 4,000-12,000 | Verification chain |
| Red Team | S-001 | 4,000-12,000 | Adversarial attack simulation |

### Selection Algorithm

The strategy selection algorithm uses three inputs:

1. **Decision criticality** (C1-C4) -- primary driver
2. **Artifact type** (TGT-*) -- determines which strategies are most relevant
3. **Iteration number** -- progressive escalation across iterations (S-015 pattern)

```python
def select_strategies(criticality, artifact_type, iteration, token_budget_state):
    """Select adversarial strategies for a critic agent."""

    # S-014 is ALWAYS included (H-15)
    strategies = ["S-014"]

    if criticality == C1:
        # Minimal: self-refine + optional scoring
        strategies = ["S-010"]
        if iteration >= 2:
            strategies.append("S-014")
        return strategies

    if criticality == C2:
        iteration_map = {
            1: ["S-002", "S-014"],                    # Challenge + Score
            2: ["S-007", "S-014"],                    # Compliance + Score
            3: ["S-003", "S-014"],                    # Strengthen + Score
        }
        return iteration_map.get(iteration, strategies)

    if criticality == C3:
        iteration_map = {
            1: ["S-002", "S-004", "S-014"],           # Challenge + Pre-Mortem + Score
            2: ["S-007", "S-012", "S-013", "S-014"],  # Compliance + FMEA + Inversion + Score
            3: ["S-001", "S-003", "S-014"],            # Red Team + Steelman + Score
        }
        return iteration_map.get(iteration, strategies)

    if criticality == C4:
        # All strategies, phased across iterations
        iteration_map = {
            1: ["S-002", "S-004", "S-007", "S-014"],              # Foundation
            2: ["S-001", "S-012", "S-013", "S-011", "S-014"],     # Deep analysis
            3: ["S-001", "S-003", "S-010", "S-011", "S-014"],     # Comprehensive final
        }
        return iteration_map.get(iteration, strategies)

    return strategies
```

### Artifact-Type Modifiers

Certain artifact types benefit from specific strategies:

| Artifact Type | Preferred Strategies | Rationale |
|---------------|---------------------|-----------|
| TGT-ARCH, TGT-DEC | S-002, S-004, S-013 | Decisions benefit from challenge, pre-mortem, inversion |
| TGT-REQ | S-007, S-011, S-012 | Requirements need compliance checking, verification, FMEA |
| TGT-RES | S-003, S-013, S-014 | Research needs steelman, inversion, scoring |
| TGT-CODE | S-001, S-012, S-014 | Code needs red team, FMEA, scoring |
| TGT-PROC | S-007, S-004, S-014 | Process needs compliance, pre-mortem, scoring |

These modifiers adjust the strategy selection within a criticality level. For example, at C2, a TGT-REQ artifact might get S-007 at iteration 1 instead of S-002.

---

## Criticality Integration

### C1-C4 Framework

The orch-planner integrates the barrier-2 C1-C4 criticality framework to determine review intensity:

| Level | Description | Adversarial Intensity | Iteration Budget | Token Budget |
|-------|-------------|----------------------|------------------|--------------|
| C1 | Routine decisions | Minimal (S-010 only) | 1-2 iterations | Ultra-Low (1,600-2,100) |
| C2 | Significant decisions | Standard (2-3 strategies) | 3 iterations | Low-Medium (8,000-20,000) |
| C3 | Major decisions | Enhanced (3-5 strategies) | 3 iterations | Medium (15,000-40,000) |
| C4 | Critical decisions | Full (all 10 phased) | 3+ iterations | High (40,000-80,000) |

### Criticality Assessment

The orch-planner assesses criticality at plan generation time using these signals:

1. **Explicit user specification:** User provides criticality level in workflow request
2. **Artifact type inference:** TGT-ARCH and TGT-DEC default to C3+, TGT-CODE defaults to C2
3. **Downstream impact:** Artifacts consumed by 3+ downstream phases default to C3
4. **SSOT override:** `quality-enforcement.md` may specify criticality thresholds

```yaml
# In ORCHESTRATION_PLAN.md, criticality is documented per phase
phases:
  - id: 1
    name: "Strategy Selection Framework"
    criticality: C3
    criticality_rationale: "ADR affects all downstream adversarial strategy usage"
```

### Criticality in ORCHESTRATION.yaml

```yaml
workflow:
  constraints:
    criticality_default: C2          # Default if not specified per phase
    quality_gate_threshold: 0.92
    adversarial_iteration_min: 3

pipelines:
  adv:
    phases:
      - id: 1
        criticality: C3              # Per-phase override
```

---

## Quality Threshold Enforcement

### Threshold Configuration

The orch-planner encodes the quality gate threshold in the ORCHESTRATION.yaml constraints section (FR-307-006):

```yaml
workflow:
  constraints:
    quality_gate_threshold: 0.92
    adversarial_iteration_min: 3
    adversarial_validation: true
  patterns:
    - ADVERSARIAL_FEEDBACK
```

### SSOT Consumption

Per IR-307-002, the threshold value MUST be read from `quality-enforcement.md` rather than hardcoded. The orch-planner reads this file at plan generation time and embeds the current value.

### Threshold Encoding in Execution Queue

Each adversarial critic group includes the threshold for orch-tracker reference:

```yaml
adversarial_context:
  quality_threshold: 0.92     # From quality-enforcement.md SSOT
  scoring_required: true       # S-014 LLM-as-Judge mandatory (H-15)
  anti_leniency: true          # Anti-leniency calibration required (H-16)
```

### L2-REINJECT Tag Generation

Per IR-307-003, the orch-planner generates L2-REINJECT tags in the ORCHESTRATION_PLAN.md:

```html
<!-- L2-REINJECT: rank=3, tokens=30, content="Quality gate >= 0.92. Min 3 adversarial iterations. S-014 LLM-as-Judge scoring REQUIRED." -->
```

This enables the PromptReinforcementEngine to reinforce quality expectations in subsequent prompts.

---

## Iteration Minimum Enforcement

### Minimum Iteration Count

The orch-planner generates a minimum of 3 adversarial iterations (FR-307-003, H-14). This means:

- 3 critic groups (iterations 1, 2, 3)
- 2 revision groups (after iterations 1 and 2; iteration 3 is scoring-only)
- 1 validation group

### Early Exit Design

Iteration 3 MAY be SKIPPED if the quality gate is met at iteration 2 (FR-307-008). The orch-planner generates the full 3-iteration structure, but the orch-tracker applies early exit logic at runtime:

```yaml
# Generated structure (always 3 iterations)
iterations:
  - iteration: 1
    status: "PENDING"
  - iteration: 2
    status: "PENDING"
  - iteration: 3
    status: "PENDING"
    early_exit_eligible: true     # Can be SKIPPED if threshold met at iter 2
```

**Early exit conditions:**
1. All artifacts in the phase achieved quality score >= 0.92 at iteration 2
2. No BLOCKING findings remain unresolved from iteration 2 critique
3. The workflow criticality is not C4 (C4 always requires all 3 iterations)

**Evidence from live ORCHESTRATION.yaml:** Groups 5-6 in the EPIC-002 workflow demonstrate early exit with `status: "SKIPPED"` and note: "Both pipelines achieved PASS at iteration 2, no iteration 3 needed".

---

## Progressive Escalation (S-015)

### S-015 as Orchestration Configuration

Per ADR-EPIC002-001, S-015 (Progressive Adversarial Escalation) is categorized as an orchestration pattern, not an adversarial strategy. The orch-planner implements S-015 by progressively increasing adversarial intensity across iterations:

| Iteration | Intensity | Strategy Focus | Purpose |
|-----------|-----------|----------------|---------|
| 1 | Foundation | S-002, S-004 (challenge, pre-mortem) | Surface obvious issues |
| 2 | Deep Analysis | S-007, S-012, S-013 (compliance, FMEA, inversion) | Systematic coverage |
| 3 | Comprehensive | S-001, S-003 (red team, steelman) | Final stress test + strengthening |

### Escalation Logic

Each iteration escalates in three dimensions:

1. **Strategy count:** More strategies per iteration at C3/C4
2. **Strategy depth:** Deeper strategies (Red Team, FMEA) in later iterations
3. **Scoring rigor:** S-014 LLM-as-Judge scoring at every iteration, with anti-leniency calibration increasing

This ensures early iterations catch low-hanging issues while later iterations apply more rigorous analysis.

---

## ORCHESTRATION.yaml Schema Additions

### New Fields

The following fields are added to ORCHESTRATION.yaml to support adversarial feedback loops:

```yaml
# workflow-level additions
workflow:
  constraints:
    quality_gate_threshold: 0.92         # NEW: quality gate score
    adversarial_iteration_min: 3         # NEW: minimum iterations
    adversarial_validation: true         # NEW: adversarial mode flag
    criticality_default: "C2"            # NEW: default criticality
  patterns:
    - ADVERSARIAL_FEEDBACK               # NEW: pattern flag

# execution_queue group additions
execution_queue:
  groups:
    - id: N
      adversarial_context:               # NEW: adversarial metadata block
        cycle_phase: "creator|critic|revision|validation"
        iteration: 1
        max_iterations: 3
        quality_threshold: 0.92
        strategies: ["S-002", "S-014"]
        early_exit_eligible: false
      iterations:                         # NEW: iteration tracking
        - iteration: 1
          status: "PENDING"
          critique_agents: []
          revision_agents: []
          scores: {}
          findings_resolved: {}

# agent-level additions
agents:
  - id: "ps-critic-301"
    role: "critic"                        # NEW: explicit role
    adversarial_strategies: [...]         # NEW: strategy assignment
    target_artifacts: [...]               # NEW: what to review
    anti_leniency: true                   # NEW: calibration flag

# resumption additions
resumption:
  adversarial_feedback_status:            # NEW: cross-session adversarial state
    total_enablers: N
    enablers_complete: N
    enablers_validated: N
    current_enabler: "string"
    current_iteration: "N/A|1|2|3"
    iterations_complete: N
    iterations_total: N

# metrics additions
metrics:
  quality:                                # NEW: quality metrics section
    adversarial_iterations_completed: N
    adversarial_iterations_total: N
    quality_scores:
      - enabler: "EN-XXX"
        iteration_1: 0.XX
        iteration_2: 0.XX
        validation: "PASS|CONDITIONAL PASS|FAIL"
```

### Backward Compatibility

All new fields are optional. If `adversarial_validation` is absent or `false`, the orch-planner generates plans without adversarial cycles, preserving pre-enhancement behavior (NFR-307-001).

---

## Algorithm: Plan Generation

### Complete Auto-Generation Algorithm

```python
def generate_orchestration_plan(workflow_request, quality_enforcement_ssot):
    """
    Main algorithm for orch-planner adversarial-enhanced plan generation.

    FR-307-001 through FR-307-010 implementation.
    """

    # Step 1: Read SSOT configuration
    config = read_quality_enforcement_ssot(quality_enforcement_ssot)
    threshold = config.quality_gate_threshold  # 0.92
    min_iterations = config.adversarial_iteration_min  # 3

    # Step 2: Generate base plan (existing orch-planner behavior)
    plan = generate_base_plan(workflow_request)

    # Step 3: Check if adversarial validation is enabled
    if not plan.constraints.get("adversarial_validation", True):
        return plan  # No adversarial enhancement (NFR-307-002)

    # Step 4: Add ADVERSARIAL_FEEDBACK to patterns
    plan.patterns.append("ADVERSARIAL_FEEDBACK")

    # Step 5: For each phase, determine if adversarial cycle needed
    group_id = 1
    for phase in plan.phases:
        # Generate creator group (existing behavior)
        creator_group = generate_creator_group(phase, group_id)
        plan.execution_queue.add(creator_group)
        group_id += 1

        # Check if adversarial cycle needed
        if should_inject_adversarial_cycle(phase, plan):
            criticality = phase.criticality or plan.constraints.criticality_default

            # Generate adversarial iteration groups
            for iteration in range(1, min_iterations + 1):
                # Critic group
                strategies = select_strategies(
                    criticality, phase.artifact_type, iteration,
                    plan.constraints.token_budget_state
                )
                critic_group = generate_critic_group(
                    phase, group_id, iteration, strategies, threshold
                )
                plan.execution_queue.add(critic_group)
                group_id += 1

                # Revision group (not for final iteration -- it's scoring-only)
                if iteration < min_iterations:
                    revision_group = generate_revision_group(
                        phase, group_id, iteration
                    )
                    plan.execution_queue.add(revision_group)
                    group_id += 1

            # Validation group (FR-307-010)
            validation_group = generate_validation_group(phase, group_id)
            plan.execution_queue.add(validation_group)
            group_id += 1

    # Step 6: Generate resumption context (FR-307-009)
    plan.resumption.adversarial_feedback_status = {
        "total_enablers": count_enablers(plan),
        "enablers_complete": 0,
        "enablers_validated": 0,
        "current_enabler": "N/A",
        "current_iteration": "N/A",
    }

    # Step 7: Generate L2-REINJECT tags (IR-307-003)
    plan.l2_reinject_tags.append(
        f'Quality gate >= {threshold}. Min {min_iterations} adversarial iterations. '
        f'S-014 LLM-as-Judge scoring REQUIRED.'
    )

    return plan
```

---

## Live Example Analysis

### Mapping to EPIC-002 ORCHESTRATION.yaml

The live EPIC-002 ORCHESTRATION.yaml (`epic002-crosspoll-20260213-001`) demonstrates the exact patterns this design formalizes:

| Design Element | Live YAML Evidence | Location |
|----------------|-------------------|----------|
| Quality gate threshold | `constraints.quality_gate_threshold: 0.92` | `workflow.constraints` |
| Iteration minimum | `constraints.adversarial_iteration_min: 3` | `workflow.constraints` |
| ADVERSARIAL_FEEDBACK pattern | `patterns: [ADVERSARIAL_FEEDBACK]` | `workflow.patterns` |
| Creator group | Group 1: creator agents (PARALLEL) | `execution_queue.groups[0]` |
| Critic iteration 1 | Group 2: critic agents (PARALLEL, blocked_by: [1]) | `execution_queue.groups[1]` |
| Revision iteration 1 | Group 3: creator revision (PARALLEL, blocked_by: [2]) | `execution_queue.groups[2]` |
| Critic iteration 2 | Group 4: critic agents (PARALLEL, blocked_by: [3]) | `execution_queue.groups[3]` |
| Early exit (SKIPPED) | Groups 5-6: `status: "SKIPPED"` | `execution_queue.groups[4-5]` |
| Validation | Group 7: validation (PARALLEL, blocked_by: [6]) | `execution_queue.groups[6]` |
| Strategy assignment | `adversarial_strategies: ["S-002", "S-005", "S-014"]` | Agent entries |
| Iteration scores | `iterations[].scores: {EN-302: 0.935}` | Group 10 |
| Finding resolution | `findings_resolved: {EN-303: "3/3 blocking..."}` | Group 10 |
| Resumption context | `adversarial_feedback_status` | `resumption` |
| Quality metrics | `quality_scores` | `metrics.quality` |

This design formalizes ALL of these patterns for automatic generation.

---

## Traceability

### Requirement Coverage

| Requirement | Design Section | Status |
|-------------|---------------|--------|
| FR-307-001 | Adversarial Cycle Detection | Covered |
| FR-307-002 | Creator-Critic-Revision Pattern Injection | Covered |
| FR-307-003 | Iteration Minimum Enforcement | Covered |
| FR-307-004 | Strategy Selection Logic | Covered |
| FR-307-005 | ORCHESTRATION.yaml Schema Additions (agent fields) | Covered |
| FR-307-006 | Quality Threshold Enforcement | Covered |
| FR-307-007 | ORCHESTRATION.yaml Schema Additions (iteration tracking) | Covered |
| FR-307-008 | Iteration Minimum Enforcement (early exit) | Covered |
| FR-307-009 | ORCHESTRATION.yaml Schema Additions (resumption) | Covered |
| FR-307-010 | Creator-Critic-Revision Pattern Injection (validation) | Covered |
| IR-307-001 | Criticality Integration | Covered |
| IR-307-002 | Quality Threshold Enforcement (SSOT) | Covered |
| IR-307-003 | Quality Threshold Enforcement (L2-REINJECT) | Covered |
| IR-307-004 | ORCHESTRATION.yaml Schema Additions (patterns) | Covered |
| IR-307-005 | Criticality Integration (layer mapping) | Partially Covered |
| IR-307-006 | Strategy Selection Logic (token budget) | Partially Covered |
| NFR-307-001 | ORCHESTRATION.yaml Schema Additions (backward compat) | Covered |
| NFR-307-002 | Adversarial Cycle Detection (opt-out) | Covered |
| NFR-307-003 | Quality Threshold Enforcement (default-on) | Covered |
| NFR-307-005 | Creator-Critic-Revision Pattern Injection (P-003) | Covered |

---

## References

| # | Citation | Sections Referenced |
|---|----------|-------------------|
| 1 | FEAT-004:EN-307:TASK-001 (Requirements) | FR-307-001 through FR-307-010, IR-307-001 through IR-307-006, NFR-307-001 through NFR-307-003 |
| 2 | ADR-EPIC002-001 (EN-302 TASK-005) | 10 selected strategies, C1-C4 criticality |
| 3 | EN-303 TASK-001 | 8-dimension context taxonomy, artifact type triggers |
| 4 | EN-303 TASK-003 | Strategy profiles, token budgets, enforcement layer mapping |
| 5 | Barrier-2 ENF-to-ADV Handoff | H-13, H-14, H-15, H-16, quality-enforcement.md SSOT, L2-REINJECT |
| 6 | Live ORCHESTRATION.yaml (epic002-crosspoll-20260213-001) | Proven patterns, execution queue structure, quality metrics |
| 7 | Orchestration SKILL.md v2.1.0 | Current state schema, workflow patterns |
| 8 | orch-planner agent spec v2.1.0 | Current capabilities, output format |

---

*Document ID: FEAT-004:EN-307:TASK-002*
*Agent: ps-architect-307*
*Created: 2026-02-13*
*Status: Complete*
