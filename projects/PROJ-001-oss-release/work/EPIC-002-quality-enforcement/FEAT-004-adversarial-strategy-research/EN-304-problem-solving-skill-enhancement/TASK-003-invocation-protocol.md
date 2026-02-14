# TASK-003: Invocation Protocol for Adversarial Strategies

<!--
DOCUMENT-ID: FEAT-004:EN-304:TASK-003
VERSION: 1.0.0
AGENT: ps-architect-304 (creator)
DATE: 2026-02-13
STATUS: Draft
PARENT: EN-304 (Problem-Solving Skill Enhancement)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DESIGN
INPUT: TASK-001 (requirements), TASK-002 (mode design), EN-303 TASK-004 (decision tree), Barrier-2 ENF-to-ADV handoff
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-304
> **Quality Target:** >= 0.92
> **Purpose:** Design the invocation protocol for adversarial strategy selection -- explicit mode selection, automatic selection via EN-303 decision tree, multi-mode pipelines, /orchestration integration, and S-014 quality score tracking

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What the invocation protocol delivers |
| [Explicit Mode Selection](#explicit-mode-selection) | How users and orchestrators select modes directly |
| [Automatic Mode Selection](#automatic-mode-selection) | How modes are selected via the EN-303 decision tree |
| [Multi-Mode Pipelines](#multi-mode-pipelines) | How multiple modes compose and execute sequentially |
| [Orchestration Integration](#orchestration-integration) | How the protocol integrates with /orchestration skill |
| [Quality Score Tracking](#quality-score-tracking) | How S-014 scores are tracked across iterations |
| [Invocation Context Schema](#invocation-context-schema) | Updated PS CONTEXT schema for adversarial invocations |
| [Error Handling](#error-handling) | How invocation errors are handled |
| [Traceability](#traceability) | Mapping to TASK-001 requirements |
| [References](#references) | Source citations |

---

## Summary

This document defines the invocation protocol for selecting and applying adversarial strategies through the ps-critic agent. The protocol supports three invocation patterns:

1. **Explicit selection** -- user or orchestrator names specific modes (`--mode red-team,llm-as-judge`)
2. **Automatic selection** -- context vector is provided and the EN-303 TASK-004 decision tree determines the mode set
3. **Pipeline composition** -- multiple modes execute in sequence with output chaining and a final quality score

All invocation patterns produce consistent output via the updated PS CONTEXT schema and are P-003 compliant (the orchestrator manages invocation; ps-critic executes and returns).

---

## Explicit Mode Selection

### Syntax

```
ps-critic --mode <mode-name>[,<mode-name>,...] [--artifact <path>] [--criticality <C1|C2|C3|C4>]
```

**Examples:**

```bash
# Single mode
ps-critic --mode red-team --artifact projects/PROJ-001/decisions/ADR-003.md

# Multi-mode pipeline
ps-critic --mode steelman,devils-advocate,llm-as-judge --artifact work/EN-304/TASK-002.md

# With criticality override
ps-critic --mode constitutional --artifact src/domain/aggregates/work_item.py --criticality C3
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--mode` | No | `standard` | Comma-separated list of mode names to execute |
| `--artifact` | Yes | -- | Path to the artifact under review |
| `--criticality` | No | Auto-detected | Override criticality level (C1, C2, C3, C4) |
| `--iteration` | No | 1 | Iteration number in the creator-critic-revision cycle |
| `--previous-score` | No | -- | Quality score from previous iteration (enables trend tracking) |
| `--threshold` | No | 0.92 (from SSOT) | Quality gate threshold |
| `--budget` | No | Auto-detected | Token budget state (FULL, CONST, EXHAUST) |

### Validation Rules

| Rule | Behavior |
|------|----------|
| Unknown mode name | REJECT with error: `Unknown mode '{name}'. Available modes: self-refine, steelman, inversion, constitutional, devils-advocate, pre-mortem, fmea, chain-of-verification, llm-as-judge, red-team` |
| Empty mode list | Fall back to `standard` (v2.2.0 default behavior per BC-304-001) |
| Missing artifact | REJECT with error: `Artifact path required` |
| Artifact not found | REJECT with error: `Artifact not found at '{path}'` |
| TEN pair in mode list | WARN: `Tension pair detected: {mode1} and {mode2}. Proceeding with caution. See EN-303 TASK-003 for tension management guidance.` |

---

## Automatic Mode Selection

### Overview

When no `--mode` parameter is specified but a context vector is available, the invocation protocol uses the EN-303 TASK-004 decision tree to determine the mode set.

### Context Vector Input

The orchestrator provides the context vector via the invocation context schema:

```yaml
adversarial_context:
  criticality: "C2"           # CRIT dimension (primary branch)
  phase: "PH-DESIGN"          # Review phase
  target_type: "TGT-ARCH"     # Artifact type
  maturity: "MAT-DRAFT"       # Artifact maturity
  team: "TEAM-MULTI"          # Team composition
  enforcement: "ENF-FULL"     # Enforcement layer availability
  platform: "PLAT-CC"         # Platform context
  token_budget: "TOK-FULL"    # Token budget state
```

### Selection Algorithm

```
FUNCTION select_modes(context_vector):
    # Step 1: Auto-escalation (AE-001 through AE-005)
    criticality = context_vector.criticality
    IF artifact modifies JERRY_CONSTITUTION.md:
        criticality = max(criticality, C3)     # AE-001
    IF artifact modifies .claude/rules/*:
        criticality = max(criticality, C3)     # AE-002
    IF artifact is new/modified ADR:
        criticality = max(criticality, C3)     # AE-003
    IF artifact modifies baselined ADR:
        criticality = C4                       # AE-004
    IF artifact modifies security-relevant code:
        criticality = max(criticality, C3)     # AE-005

    # Step 2: Phase modifier (with PR-001 precedence)
    original_criticality = context_vector.criticality
    IF criticality > original_criticality:
        # Auto-escalated: phase modifier CANNOT reduce below escalated level (PR-001)
        phase_modified = apply_phase_modifier(criticality, context_vector.phase)
        criticality = max(criticality, phase_modified)
    ELSE:
        criticality = apply_phase_modifier(criticality, context_vector.phase)

    # Step 3: Look up base strategy set by criticality
    modes = STRATEGY_SETS[criticality]  # C1/C2/C3/C4 lookup table

    # Step 4: Apply token budget adaptation
    IF context_vector.token_budget == "TOK-CONST":
        modes = adapt_for_constrained_budget(criticality, modes)
    ELIF context_vector.token_budget == "TOK-EXHAUST":
        modes = adapt_for_exhausted_budget(criticality, modes)
        IF criticality >= C3:
            add_human_escalation_flag()     # AE-006

    # Step 5: Apply maturity gate
    IF context_vector.maturity in [MAT-APPR, MAT-BASE]:
        modes = restrict_to_verification_modes(modes)

    # Step 6: Apply team check
    IF context_vector.team == "TEAM-SINGLE" AND criticality >= C3:
        modes = restrict_to_single_agent_modes(modes)
        add_escalation_recommendation()
    IF context_vector.team == "TEAM-SINGLE" AND criticality == C4:
        REJECT("C4 review NOT PERMITTED for TEAM-SINGLE. Escalate to TEAM-MULTI + TEAM-HIL.")

    # Step 7: Apply ENF-MIN override
    IF context_vector.enforcement == "ENF-MIN":
        modes = adapt_for_enf_min(criticality, modes)   # ENF-MIN-001 through ENF-MIN-004
        IF criticality >= C3:
            add_human_escalation_flag()    # ENF-MIN-002

    # Step 8: Apply sequencing rules (SEQ-001 through SEQ-005)
    modes = apply_sequencing_constraints(modes)

    RETURN modes
```

### Strategy Set Lookup Tables

**Base strategy sets (TOK-FULL, PLAT-CC):**

| Criticality | Required Modes | Recommended Modes |
|-------------|----------------|-------------------|
| C1 | `self-refine` | `steelman`, `llm-as-judge` |
| C2 | `constitutional`, `devils-advocate`, `llm-as-judge` | `steelman`, `self-refine` |
| C3 | `constitutional`, `devils-advocate`, `llm-as-judge`, `pre-mortem`, `fmea`, `inversion` | `steelman`, `self-refine`, `chain-of-verification` |
| C4 | All 10 modes | -- |

**TOK-CONST adapted sets:**

| Criticality | Adapted Set | Estimated Tokens |
|-------------|-------------|------------------|
| C1 | `self-refine` | 2,000 |
| C2 | `steelman`, `llm-as-judge`, `self-refine` | 5,600 |
| C3 | `steelman`, `devils-advocate`, `llm-as-judge`, `inversion` | 10,300 |
| C4 | `steelman`, `devils-advocate`, `inversion`, `llm-as-judge`, `constitutional` (single-pass) | ~18,300 |

**TOK-EXHAUST adapted sets:**

| Criticality | Adapted Set | Action |
|-------------|-------------|--------|
| C1 | `self-refine` (or skip) | Minimal check |
| C2 | `steelman`, `llm-as-judge` | Scoring only |
| C3 | `llm-as-judge` | Human escalation MANDATORY |
| C4 | -- | End session. Human review MANDATORY. |

---

## Multi-Mode Pipelines

### Pipeline Execution Model

When multiple modes are selected, they execute sequentially as a pipeline managed by the orchestrator:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Mode 1     │───>│  Mode 2     │───>│  Mode 3     │───>│  Mode N     │
│  (e.g.      │    │  (e.g.      │    │  (e.g.      │    │  (e.g.      │
│  steelman)  │    │  DA)        │    │  const.)    │    │  judge)     │
│             │    │             │    │             │    │             │
│  Output:    │    │  Output:    │    │  Output:    │    │  Output:    │
│  Steelman   │    │  Challenges │    │  Compliance │    │  Score:0.93 │
│  argument   │    │  found      │    │  report     │    │  PASS       │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │
      └──────────────────┴──────────────────┴──────────────────┘
                              Pipeline Context
                         (accumulated mode outputs)
```

### Sequencing Constraints

The pipeline engine enforces the following ordering constraints from TASK-002:

| ID | Constraint | Effect |
|----|-----------|--------|
| SEQ-001 | `steelman` before `devils-advocate`, `constitutional`, `red-team` | Ensures critique engages with strongest argument formulation |
| SEQ-002 | `inversion` before `constitutional`, `fmea`, `red-team` | Provides anti-pattern criteria for subsequent evaluation |
| SEQ-003 | `llm-as-judge` last | Provides final authoritative quality score |
| SEQ-004 | `self-refine` first | Creator self-improvement before external critique |
| SEQ-005 | `chain-of-verification` is order-independent | Factual verification is context-isolated |

### Pipeline Context Accumulation

Each mode's output is accumulated into a pipeline context document that grows as modes execute:

```markdown
# Pipeline Context (accumulated)

## Mode: steelman (S-003)
[steelman output here]

## Mode: constitutional (S-007)
[constitutional output here, referencing steelman findings]

## Mode: devils-advocate (S-002)
[DA output here, challenging steelmanned argument]

## Mode: llm-as-judge (S-014)
[final score, informed by all prior mode outputs]
```

### Pipeline Abort Conditions

| Condition | Action |
|-----------|--------|
| A mode detects C3/C4 governance violation | Abort pipeline; escalate to human review |
| Token budget exhausted mid-pipeline | Complete current mode; skip remaining; emit warning |
| Mode produces CONTRADICTED claim on a HARD rule | Abort pipeline; the artifact CANNOT pass quality gate |
| Orchestrator timeout | Complete current mode; return partial results |

---

## Orchestration Integration

### /orchestration Skill Coordination

The invocation protocol integrates with the /orchestration skill for multi-phase adversarial workflows:

| Integration Point | Description | /orchestration Artifact |
|-------------------|-------------|------------------------|
| **Phase tracking** | Each adversarial review cycle is tracked as a phase in ORCHESTRATION.yaml | `phases[].adversarial_review` |
| **Sync barriers** | Multi-pipeline adversarial reviews (parallel critic agents) synchronize at barriers | `barriers[].type: adversarial_sync` |
| **State checkpointing** | Pipeline context is checkpointed after each mode for recovery | `checkpoints[].pipeline_state` |
| **Cross-pollination** | Adversarial findings from one pipeline inform another (like barrier-2 ENF->ADV) | `cross_pollination[].handoff` |

### Creator-Critic-Revision Cycle Integration

The invocation protocol maps to the 3-iteration minimum cycle (H-14):

**Iteration 1: Create**
```yaml
invocation:
  agent: ps-architect  # Creator
  mode: implicit-self-refine  # Creator applies S-010 during creation
  output: initial artifact
```

**Iteration 2: Critique**
```yaml
invocation:
  agent: ps-critic
  mode: auto  # Automatic selection via decision tree
  context:
    criticality: "C2"  # Example
    phase: "PH-DESIGN"
    # ... full context vector
  output: pipeline results + quality score
```

**Iteration 3: Revise**
```yaml
invocation:
  agent: ps-architect  # Creator revises
  input: iteration 2 critique output
  mode: implicit-self-refine  # S-010 during revision

# Then verify revision:
invocation:
  agent: ps-critic
  mode: llm-as-judge,chain-of-verification
  input: revised artifact + iteration 2 critique
  output: final quality score + verification results
```

### Extended Cycle (Iterations 4+)

If the quality threshold (>= 0.92) is not met after iteration 3:

```
IF quality_score >= 0.92:
    ACCEPT
ELIF iteration >= circuit_breaker_max (default 3):
    IF quality_score >= 0.85:
        ACCEPT_WITH_CAVEATS (document shortfall)
    ELSE:
        ESCALATE to user per P-020
ELIF (current_score - previous_score) < 0.05 for 2 consecutive iterations:
    ACCEPT_WITH_CAVEATS (plateau detected)
ELSE:
    REVISE (additional iteration)
```

---

## Quality Score Tracking

### Score Tracking Schema

Quality scores from S-014 (`llm-as-judge` mode) are tracked across iterations:

```yaml
quality_tracking:
  artifact: "<artifact path>"
  threshold: 0.92  # From quality-enforcement.md SSOT
  iterations:
    - iteration: 1
      score: null  # No critique in creation iteration
      modes_applied: ["self-refine"]
      notes: "Creator self-improvement"
    - iteration: 2
      score: 0.78
      modes_applied: ["steelman", "constitutional", "devils-advocate", "llm-as-judge"]
      improvement_areas: ["Completeness: missing edge case analysis", "Traceability: 3 claims unlinked"]
      notes: "Standard C2 critique"
    - iteration: 3
      score: 0.93
      modes_applied: ["llm-as-judge", "chain-of-verification"]
      improvement_delta: +0.15
      threshold_met: true
      notes: "Revision addressed all improvement areas; quality gate PASS"
```

### Score Trend Analysis

When multiple iteration scores are available, the protocol produces trend analysis:

| Metric | Calculation | Purpose |
|--------|------------|---------|
| Improvement delta | `current_score - previous_score` | Detect progress or plateau |
| Average improvement rate | `total_improvement / iterations` | Predict convergence |
| Projected iterations to threshold | `(threshold - current) / avg_rate` | Estimate remaining effort |
| Plateau detection | `delta < 0.05 for 2 consecutive` | Trigger early termination or escalation |

### Anti-Leniency Monitoring

Per HARD rule H-16, the protocol monitors for leniency bias:

| Check | Action |
|-------|--------|
| Score jumps > 0.20 in one iteration | Flag for human review (unusual improvement) |
| Scores consistently > 0.95 across artifacts | Flag for rubric recalibration |
| Score improvement without corresponding artifact changes | Flag as potential leniency drift |
| First-iteration scores > 0.90 | Flag for review (C2+ artifacts rarely score this high initially) |

---

## Invocation Context Schema

### Updated PS CONTEXT for Adversarial Invocations

The current ps-critic invocation schema (PS CONTEXT from ps-critic.md v2.2.0) is extended for adversarial mode support:

```markdown
## PS CONTEXT (REQUIRED)
- **PS ID:** {ps_id}
- **Entry ID:** {entry_id}
- **Iteration:** {iteration_number} (1-based)
- **Artifact to Critique:** {path_to_artifact}
- **Generator Agent:** {agent_that_produced_artifact}

## ADVERSARIAL CONTEXT (NEW - optional, triggers adversarial mode)
- **Mode:** {explicit mode(s) OR "auto"}
- **Criticality:** {C1|C2|C3|C4 OR "auto-detect"}
- **Phase:** {PH-EXPLORE|PH-DESIGN|PH-IMPL|PH-VALID|PH-MAINT}
- **Target Type:** {TGT-CODE|TGT-ARCH|TGT-REQ|TGT-RES|TGT-DEC|TGT-PROC}
- **Maturity:** {MAT-DRAFT|MAT-REVIEW|MAT-APPR|MAT-BASE}
- **Team:** {TEAM-SINGLE|TEAM-MULTI|TEAM-HIL}
- **Enforcement:** {ENF-FULL|ENF-PORT|ENF-MIN}
- **Platform:** {PLAT-CC|PLAT-CC-WIN|PLAT-GENERIC}
- **Token Budget:** {TOK-FULL|TOK-CONST|TOK-EXHAUST}
- **Previous Score:** {0.00-1.00 or null}

## EVALUATION CRITERIA
{criteria_definition - mode-specific or default}

## IMPROVEMENT THRESHOLD
- **Target Score:** {0.92 from SSOT}
- **Max Iterations:** {3 minimum per H-14}
```

### Backward Compatibility

When the `ADVERSARIAL CONTEXT` section is absent:
- ps-critic operates in default `standard` mode (BC-304-001)
- Default quality dimensions apply (Completeness, Accuracy, Clarity, Actionability, Alignment)
- Default threshold: 0.85 (BC-304-003)
- Existing workflows continue without modification (BC-304-002)

When `ADVERSARIAL CONTEXT` is present:
- Threshold automatically becomes 0.92 (from SSOT via IR-304-003)
- Mode selection follows the protocol defined in this document
- Output includes mode-specific sections and pipeline results

---

## Error Handling

### Invocation Error Taxonomy

| Error | Severity | Response |
|-------|----------|----------|
| Unknown mode name | ERROR | Reject invocation with valid mode list |
| Missing artifact | ERROR | Reject invocation |
| Artifact not found | ERROR | Reject invocation with path |
| Invalid criticality value | WARNING | Fall back to auto-detection |
| Missing context dimension | WARNING | Use default value for missing dimension |
| Token budget exhausted mid-pipeline | WARNING | Complete current mode; skip remaining; document gap |
| Mode timeout (single mode > 60s) | WARNING | Return partial results; flag as incomplete |
| Pipeline abort (governance violation) | CRITICAL | Halt immediately; escalate to human review |

### Graceful Degradation

When errors prevent full protocol execution, the invocation degrades:

```
Full protocol available?
  YES -> Execute full pipeline
  NO  -> Missing adversarial context?
           YES -> Fall back to standard mode (v2.2.0)
           NO  -> Token budget exhausted?
                    YES -> Execute minimal strategy set per criticality
                    NO  -> Mode(s) unavailable?
                             YES -> Skip unavailable modes; execute remainder
                             NO  -> Standard error handling
```

---

## Traceability

### Requirements Coverage

| Requirement | Coverage |
|-------------|----------|
| FR-304-003 (Explicit selection) | Explicit Mode Selection section |
| FR-304-004 (Automatic selection) | Automatic Mode Selection section |
| FR-304-005 (Multi-mode pipelines) | Multi-Mode Pipelines section |
| FR-304-007 (Auto-escalation) | Selection algorithm steps 1-2 |
| FR-304-008 (Quality score tracking) | Quality Score Tracking section |
| FR-304-009 (Creator-critic cycle) | Orchestration Integration section |
| FR-304-011 (Escalation) | Pipeline abort, extended cycle logic |
| FR-304-012 (Token budget adaptation) | Strategy set lookup tables |
| IR-304-001 (C1-C4 trigger integration) | Auto-escalation in selection algorithm |
| IR-304-003 (SSOT consumption) | Threshold sourced from SSOT |
| BC-304-001 (Default behavior) | Invocation Context Schema backward compatibility |
| BC-304-003 (Threshold migration) | ADVERSARIAL CONTEXT presence determines threshold |

---

## References

| # | Citation | Relevance |
|---|----------|-----------|
| 1 | EN-303 TASK-004 | Decision tree algorithm, auto-escalation rules, budget adaptation tables |
| 2 | EN-303 TASK-003 | Sequencing constraints from pairing reference |
| 3 | EN-303 TASK-001 | Context taxonomy dimension definitions |
| 4 | Barrier-2 ENF-to-ADV | ContentBlock system, SSOT, token budgets |
| 5 | TASK-001 (this enabler) | Formal requirements (FR-304-xxx, IR-304-xxx, BC-304-xxx) |
| 6 | TASK-002 (this enabler) | Mode definitions and sequencing rules |
| 7 | ps-critic.md v2.2.0 | Current PS CONTEXT schema |
| 8 | PLAYBOOK.md v3.3.0 | Current Generator-Critic Loop (Pattern 6) |
| 9 | EN-404 HARD rules | H-13 (>= 0.92), H-14 (3 iterations), H-15 (S-014 required), H-16 (anti-leniency) |

---

*Document ID: FEAT-004:EN-304:TASK-003*
*Agent: ps-architect-304*
*Created: 2026-02-13*
*Status: Draft*
