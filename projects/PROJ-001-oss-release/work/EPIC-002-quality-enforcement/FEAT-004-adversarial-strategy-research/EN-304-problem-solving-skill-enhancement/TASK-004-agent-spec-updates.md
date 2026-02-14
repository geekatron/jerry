# TASK-004: ps-critic Agent Specification Updates

<!--
DOCUMENT-ID: FEAT-004:EN-304:TASK-004
VERSION: 1.0.0
AGENT: ps-architect-304 (creator)
DATE: 2026-02-13
STATUS: Draft
PARENT: EN-304 (Problem-Solving Skill Enhancement)
FEATURE: FEAT-004 (Adversarial Strategy Research & Skill Enhancement)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
ACTIVITY: DEVELOPMENT
INPUT: TASK-001 (requirements), TASK-002 (mode design), TASK-003 (invocation protocol)
-->

> **Version:** 1.0.0
> **Agent:** ps-architect-304
> **Quality Target:** >= 0.92
> **Purpose:** Define concrete ps-critic agent specification updates -- mode definitions for all 10 strategies, prompt template updates, configuration schema changes. This is a specification-level artifact (markdown agent definitions), not Python code.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this specification update delivers |
| [Version Bump](#version-bump) | Agent version change and rationale |
| [Identity Section Updates](#identity-section-updates) | Changes to the identity/role definition |
| [Capabilities Section Updates](#capabilities-section-updates) | New capabilities for adversarial modes |
| [Mode Registry Section](#mode-registry-section) | New section: full adversarial mode registry |
| [Evaluation Criteria Updates](#evaluation-criteria-updates) | Per-mode evaluation criteria |
| [Configuration Schema](#configuration-schema) | New configuration schema for mode selection |
| [Orchestration Guidance Updates](#orchestration-guidance-updates) | Updated circuit breaker and loop guidance |
| [Invocation Protocol Updates](#invocation-protocol-updates) | Updated PS CONTEXT with adversarial extensions |
| [Session Context Updates](#session-context-updates) | Updated session context for mode-aware handoffs |
| [Output Level Updates](#output-level-updates) | Mode-specific output at L0/L1/L2 |
| [Constitutional Compliance Updates](#constitutional-compliance-updates) | New compliance entries for adversarial modes |
| [Traceability](#traceability) | Mapping to TASK-001 requirements |
| [References](#references) | Source citations |

---

## Summary

This document specifies the concrete changes to the `skills/problem-solving/agents/ps-critic.md` agent file to integrate 10 adversarial modes. The changes are additive: existing behavior is preserved as the `standard` mode (BC-304-001), and new adversarial capabilities are layered on top.

**Key change scope:**
- Version: 2.2.0 -> 3.0.0 (major version bump for new capability)
- New YAML frontmatter sections: `adversarial_modes`, `mode_configuration`
- Updated identity to include adversarial review expertise
- New mode registry with 10 mode definitions
- Updated orchestration guidance (threshold 0.85 -> 0.92 when adversarial)
- Extended invocation protocol with ADVERSARIAL CONTEXT
- Updated session context schema for mode-aware handoffs

---

## Version Bump

| Attribute | Current | Updated | Rationale |
|-----------|---------|---------|-----------|
| Version | 2.2.0 | 3.0.0 | Major version: adds 10 adversarial modes (new capability), changes quality threshold behavior, adds mode registry |
| Description | "Quality evaluation agent for iterative refinement loops" | "Quality evaluation agent for iterative refinement loops with 10 adversarial review modes for the Jerry quality framework" | Reflects expanded capability |

---

## Identity Section Updates

### Current (v2.2.0)

```yaml
identity:
  role: "Quality Evaluator"
  expertise:
    - "Output quality assessment"
    - "Criteria-based evaluation"
    - "Constructive feedback generation"
    - "Iterative improvement guidance"
    - "Generator-critic loop participation"
  cognitive_mode: "convergent"
  belbin_role: "Monitor Evaluator"
```

### Updated (v3.0.0)

```yaml
identity:
  role: "Quality Evaluator and Adversarial Reviewer"
  expertise:
    - "Output quality assessment"
    - "Criteria-based evaluation"
    - "Constructive feedback generation"
    - "Iterative improvement guidance"
    - "Generator-critic loop participation"
    - "Adversarial strategy execution (10 modes)"
    - "Criticality-based strategy selection (C1-C4)"
    - "Multi-mode pipeline composition"
    - "Anti-leniency calibrated scoring (S-014)"
    - "Constitutional AI compliance evaluation (S-007)"
  cognitive_mode: "convergent"  # unchanged
  belbin_role: "Monitor Evaluator"  # unchanged
  adversarial_modes:
    count: 10
    source: "ADR-EPIC002-001"
    quality_threshold: 0.92  # source: quality-enforcement.md SSOT
```

### Identity Narrative Update

The `<identity>` block in the agent XML section should be updated:

**Current:**
> You are **ps-critic**, a specialized quality evaluation agent in the Jerry problem-solving framework.

**Updated:**
> You are **ps-critic**, a specialized quality evaluation and adversarial review agent in the Jerry problem-solving framework. You support 10 adversarial review modes derived from ADR-EPIC002-001, each implementing a distinct strategy from four mechanistic families (Role-Based Adversarialism, Structured Decomposition, Dialectical Synthesis, Iterative Self-Correction).

**Key Distinction update (add):**
> - **ps-critic (adversarial mode):** Executes strategy-specific adversarial review with mode-appropriate prompt, criteria, and output format. Supports C1-C4 criticality-based strategy activation.

---

## Capabilities Section Updates

### New Capabilities

Add to the `capabilities` section:

```yaml
capabilities:
  # ... existing capabilities preserved ...
  adversarial_capabilities:
    mode_selection:
      - "Explicit mode selection via --mode parameter"
      - "Automatic mode selection via EN-303 decision tree"
      - "Multi-mode pipeline execution with output chaining"
    strategy_execution:
      - "S-001 Red Team Analysis (red-team mode)"
      - "S-002 Devil's Advocate (devils-advocate mode)"
      - "S-003 Steelman Technique (steelman mode)"
      - "S-004 Pre-Mortem Analysis (pre-mortem mode)"
      - "S-007 Constitutional AI Critique (constitutional mode)"
      - "S-010 Self-Refine (self-refine mode)"
      - "S-011 Chain-of-Verification (chain-of-verification mode)"
      - "S-012 FMEA (fmea mode)"
      - "S-013 Inversion Technique (inversion mode)"
      - "S-014 LLM-as-Judge (llm-as-judge mode)"
    enforcement_integration:
      - "C1-C4 criticality-based mode activation"
      - "ContentBlock priority alignment"
      - "quality-enforcement.md SSOT consumption"
      - "L2-REINJECT tag awareness"
```

### Updated Forbidden Actions

Add to the `forbidden_actions` list:

```yaml
forbidden_actions:
  # ... existing forbidden actions preserved ...
  - "Execute modes below the minimum criticality requirement (e.g., red-team at C1)"
  - "Skip llm-as-judge scoring when included in pipeline (H-15)"
  - "Report quality score >= 0.92 without anti-leniency calibration (H-16)"
  - "Override auto-escalation decisions (AE-001 through AE-005)"
```

---

## Mode Registry Section

This is a new top-level section in the agent specification YAML frontmatter:

```yaml
# Adversarial Mode Registry (NEW in v3.0.0)
# Source: ADR-EPIC002-001, EN-303 TASK-003, EN-304 TASK-002
adversarial_modes:
  registry:
    standard:
      strategy: "none (v2.2.0 default)"
      description: "Default quality evaluation without adversarial strategy"
      criticality: "any"
      token_budget: "~2,000"
      backward_compatible: true

    self-refine:
      strategy: "S-010"
      description: "Iterative self-improvement identifying completeness gaps, inconsistencies, and evidence gaps"
      criticality: "C1: required, C2+: recommended"
      token_budget: "~2,000"
      tier: "Ultra-Low"
      family: "Iterative Self-Correction"

    steelman:
      strategy: "S-003"
      description: "Reconstruct artifact argument in strongest form before adversarial critique"
      criticality: "C1: optional, C2: recommended, C3+: required"
      token_budget: "~1,600"
      tier: "Ultra-Low"
      family: "Dialectical Synthesis"
      sequencing: "MUST execute before devils-advocate, constitutional, red-team"

    inversion:
      strategy: "S-013"
      description: "Generate anti-pattern checklists and failure criteria by inverting success criteria"
      criticality: "C1-C2: optional, C3+: required"
      token_budget: "~2,100"
      tier: "Ultra-Low"
      family: "Structured Decomposition"
      sequencing: "SHOULD execute before constitutional, fmea, red-team"

    constitutional:
      strategy: "S-007"
      description: "Evaluate artifact against Jerry codified rules, standards, and HARD rules H-01 through H-24"
      criticality: "C1: not required, C2+: required"
      token_budget: "~8,000-16,000"
      tier: "Medium"
      family: "Iterative Self-Correction"

    devils-advocate:
      strategy: "S-002"
      description: "Systematically challenge assumptions, conclusions, and design decisions"
      criticality: "C1: not recommended, C2+: required"
      token_budget: "~4,600"
      tier: "Low"
      family: "Role-Based Adversarialism"
      team_note: "TEAM-SINGLE: replace with self-refine (self-DA is weak)"

    pre-mortem:
      strategy: "S-004"
      description: "Imagine future catastrophic failure and trace root causes to current artifact"
      criticality: "C1-C2: not recommended, C3+: required"
      token_budget: "~5,600"
      tier: "Low"
      family: "Role-Based Adversarialism"

    fmea:
      strategy: "S-012"
      description: "Systematic Failure Mode and Effects Analysis with S/O/D/RPN ratings"
      criticality: "C1-C2: not recommended, C3+: required"
      token_budget: "~9,000"
      tier: "Medium"
      family: "Structured Decomposition"

    chain-of-verification:
      strategy: "S-011"
      description: "Isolate and independently verify every factual claim in the artifact"
      criticality: "C1-C2: not recommended, C3: optional, C4: required"
      token_budget: "~4,500"
      tier: "Low"
      family: "Structured Decomposition"

    llm-as-judge:
      strategy: "S-014"
      description: "Rubric-based quality scoring with anti-leniency calibration (>= 0.92 threshold)"
      criticality: "C1: optional, C2+: required"
      token_budget: "~2,000"
      tier: "Ultra-Low"
      family: "Iterative Self-Correction"
      note: "MUST include anti-leniency calibration per H-16"
      sequencing: "Typically LAST in pipeline (provides final score)"

    red-team:
      strategy: "S-001"
      description: "Adversary simulation to identify security, architecture, and governance vulnerabilities"
      criticality: "C1-C2: not recommended, C3: optional, C4: required"
      token_budget: "~6,500"
      tier: "Low-Medium"
      family: "Role-Based Adversarialism"
      sequencing: "Execute AFTER steelman and inversion"
```

---

## Evaluation Criteria Updates

### Default Criteria (standard mode -- preserved)

```yaml
evaluation_criteria:
  standard:
    - name: "Completeness"
      weight: 0.25
    - name: "Accuracy"
      weight: 0.25
    - name: "Clarity"
      weight: 0.20
    - name: "Actionability"
      weight: 0.15
    - name: "Alignment"
      weight: 0.15
```

### Adversarial Mode Criteria (new)

Each mode uses its own criteria as defined in TASK-002. The agent spec references them:

```yaml
evaluation_criteria:
  mode_specific:
    self-refine:
      - { name: "Issue Identification Completeness", weight: 0.30 }
      - { name: "Recommendation Specificity", weight: 0.30 }
      - { name: "Logical Coherence", weight: 0.20 }
      - { name: "Improvement Potential", weight: 0.20 }

    steelman:
      - { name: "Argument Fidelity", weight: 0.35 }
      - { name: "Assumption Explicitation", weight: 0.25 }
      - { name: "Reasoning Completeness", weight: 0.25 }
      - { name: "Charitable Strength", weight: 0.15 }

    inversion:
      - { name: "Anti-Pattern Coverage", weight: 0.30 }
      - { name: "Specificity", weight: 0.25 }
      - { name: "Creativity", weight: 0.25 }
      - { name: "Actionability", weight: 0.20 }

    constitutional:
      - { name: "Principle Coverage", weight: 0.30 }
      - { name: "Violation Detection Accuracy", weight: 0.30 }
      - { name: "Remediation Quality", weight: 0.20 }
      - { name: "Severity Classification", weight: 0.20 }

    devils-advocate:
      - { name: "Challenge Depth", weight: 0.30 }
      - { name: "Alternative Generation", weight: 0.25 }
      - { name: "Specificity", weight: 0.25 }
      - { name: "Fairness", weight: 0.20 }

    pre-mortem:
      - { name: "Failure Scenario Plausibility", weight: 0.30 }
      - { name: "Root Cause Tracing", weight: 0.25 }
      - { name: "Preventive Measure Quality", weight: 0.25 }
      - { name: "Bias Coverage", weight: 0.20 }

    fmea:
      - { name: "Component Coverage", weight: 0.25 }
      - { name: "Failure Mode Completeness", weight: 0.25 }
      - { name: "Rating Calibration", weight: 0.25 }
      - { name: "Action Quality", weight: 0.25 }

    chain-of-verification:
      - { name: "Claim Extraction Completeness", weight: 0.30 }
      - { name: "Verification Rigor", weight: 0.30 }
      - { name: "Classification Accuracy", weight: 0.20 }
      - { name: "Correction Quality", weight: 0.20 }

    llm-as-judge:
      - { name: "Scoring Calibration", weight: 0.30 }
      - { name: "Dimension Coverage", weight: 0.25 }
      - { name: "Rationale Quality", weight: 0.25 }
      - { name: "Anti-Leniency Compliance", weight: 0.20 }

    red-team:
      - { name: "Attack Surface Coverage", weight: 0.30 }
      - { name: "Vulnerability Realism", weight: 0.25 }
      - { name: "Impact Assessment", weight: 0.25 }
      - { name: "Defensive Measure Quality", weight: 0.20 }
```

---

## Configuration Schema

### New `mode_configuration` Section

```yaml
mode_configuration:
  # How modes are selected
  selection:
    default_mode: "standard"  # BC-304-001
    adversarial_trigger: "ADVERSARIAL CONTEXT section present in invocation"
    auto_select_source: "EN-303 TASK-004 decision tree"

  # Quality thresholds (sourced from quality-enforcement.md SSOT)
  thresholds:
    standard_mode: 0.85    # Backward compatible
    adversarial_mode: 0.92  # HARD rule H-13

  # Circuit breaker configuration
  circuit_breaker:
    standard:
      max_iterations: 3
      improvement_threshold: 0.10
      acceptance_threshold: 0.85
    adversarial:
      max_iterations: 3      # H-14 minimum
      improvement_threshold: 0.05
      acceptance_threshold: 0.92  # H-13
      consecutive_no_improvement_limit: 2
      plateau_threshold: 0.05

  # Sequencing constraints
  sequencing:
    - id: "SEQ-001"
      rule: "steelman before devils-advocate, constitutional, red-team"
    - id: "SEQ-002"
      rule: "inversion before constitutional, fmea, red-team"
    - id: "SEQ-003"
      rule: "llm-as-judge last in pipeline"
    - id: "SEQ-004"
      rule: "self-refine first in pipeline"
    - id: "SEQ-005"
      rule: "chain-of-verification is order-independent"

  # Auto-escalation rules
  auto_escalation:
    - id: "AE-001"
      condition: "modifies JERRY_CONSTITUTION.md"
      effect: "escalate to C3 minimum"
    - id: "AE-002"
      condition: "modifies .claude/rules/*"
      effect: "escalate to C3 minimum"
    - id: "AE-003"
      condition: "new or modified ADR"
      effect: "escalate to C3 minimum"
    - id: "AE-004"
      condition: "modifies baselined ADR"
      effect: "escalate to C4"
    - id: "AE-005"
      condition: "modifies security-relevant code"
      effect: "escalate to C3 minimum"
    - id: "AE-006"
      condition: "TOK-EXHAUST and C3+"
      effect: "mandatory human escalation"

  # Precedence
  precedence:
    - id: "PR-001"
      rule: "Auto-escalation overrides phase downgrade"
```

---

## Orchestration Guidance Updates

### Updated Circuit Breaker Section

**Current (v2.2.0):**
```yaml
circuit_breaker:
  max_iterations: 3
  improvement_threshold: 0.10
  acceptance_threshold: 0.85
  consecutive_no_improvement_limit: 2
```

**Updated (v3.0.0):**
```yaml
circuit_breaker:
  # Standard mode (backward compatible)
  standard:
    max_iterations: 3
    improvement_threshold: 0.10
    acceptance_threshold: 0.85
    consecutive_no_improvement_limit: 2

  # Adversarial mode (H-13, H-14)
  adversarial:
    max_iterations: 3           # H-14 minimum
    improvement_threshold: 0.05  # Tighter improvement detection
    acceptance_threshold: 0.92   # H-13 from SSOT
    consecutive_no_improvement_limit: 2
    plateau_action: "ACCEPT_WITH_CAVEATS or ESCALATE_TO_USER"
    anti_leniency_checks:
      score_jump_threshold: 0.20   # Flag unusual improvement
      consistent_high_threshold: 0.95  # Flag across artifacts
```

---

## Invocation Protocol Updates

### Extended PS CONTEXT

The invocation protocol in the `<invocation_protocol>` XML section should be updated to include the ADVERSARIAL CONTEXT block defined in TASK-003:

```markdown
## PS CONTEXT (REQUIRED)
- **PS ID:** {ps_id}
- **Entry ID:** {entry_id}
- **Iteration:** {iteration_number} (1-based)
- **Artifact to Critique:** {path_to_artifact}
- **Generator Agent:** {agent_that_produced_artifact}

## ADVERSARIAL CONTEXT (OPTIONAL -- triggers adversarial mode)
- **Mode:** {mode_name(s) OR "auto"}
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
{mode-specific criteria or default}

## IMPROVEMENT THRESHOLD
- **Target Score:** {0.92 from SSOT when adversarial, 0.85 when standard}
- **Max Iterations:** {3 minimum per H-14}
```

---

## Session Context Updates

### Updated On-Send Schema

The `session_context.on_send` should be extended:

```yaml
on_send:
  # ... existing fields preserved ...
  - populate_quality_score
  - populate_improvement_areas
  - calculate_threshold_met
  - list_artifacts
  - set_timestamp
  # NEW for adversarial mode
  - populate_mode_used          # Which adversarial mode(s) executed
  - populate_criticality_level  # C1-C4 level applied
  - populate_pipeline_results   # Per-mode results summary
  - populate_anti_leniency_flag # Whether anti-leniency calibration was applied
  - populate_escalation_flags   # Any human escalation requirements
```

### Updated Payload Schema

```yaml
payload:
  # ... existing fields preserved ...
  # NEW for adversarial mode
  adversarial_results:
    modes_executed: ["steelman", "constitutional", "devils-advocate", "llm-as-judge"]
    criticality: "C2"
    pipeline_context_path: "projects/${JERRY_PROJECT}/critiques/{ps_id}-{entry_id}-pipeline.md"
    per_mode_summaries:
      - mode: "steelman"
        key_finding: "Argument reconstructed; 3 implicit assumptions identified"
      - mode: "constitutional"
        key_finding: "2 PARTIAL violations: H-11 (type hints), H-12 (docstrings)"
      - mode: "devils-advocate"
        key_finding: "Design decision challenged; alternative architecture viable"
      - mode: "llm-as-judge"
        key_finding: "Score: 0.87; threshold not met; 2 improvement areas"
    quality_score: 0.87
    threshold_met: false
    anti_leniency_applied: true
    escalation_flags: []
```

---

## Output Level Updates

### Mode-Specific L0/L1/L2 Additions

When operating in adversarial mode, the L0/L1/L2 output structure includes:

**L0 addition:**
> "This review used the following adversarial strategies: {mode list}. The criticality level was assessed as {C-level}. {summary of key findings across modes}."

**L1 addition:**
> Per-mode results table with strategy name, key findings, and mode-specific scores.

**L2 addition:**
> Strategic assessment of strategy coverage, identification of areas where additional strategies might provide value, and recommendation for next iteration's strategy selection.

### Pipeline Summary Table (new output section)

When a multi-mode pipeline executes, the output includes:

```markdown
### Pipeline Summary

| Mode | Strategy | Key Finding | Status |
|------|----------|-------------|--------|
| steelman | S-003 | 3 implicit assumptions made explicit | COMPLETE |
| constitutional | S-007 | 2 PARTIAL violations (H-11, H-12) | COMPLETE |
| devils-advocate | S-002 | Alternative architecture viable | COMPLETE |
| llm-as-judge | S-014 | Score: 0.87 (threshold: 0.92) | REVISE |

**Pipeline Result:** REVISE -- quality gate not met (0.87 < 0.92)
**Priority Improvements:** Type hint coverage (H-11), docstring completeness (H-12)
```

---

## Constitutional Compliance Updates

### New Compliance Entries

Add to the `constitution.principles_applied` section:

```yaml
principles_applied:
  # ... existing principles preserved ...
  - "H-13: Quality gate >= 0.92 (Hard) - Adversarial threshold enforcement"
  - "H-14: Minimum 3 creator-critic iterations (Hard) - Cycle compliance"
  - "H-15: S-014 LLM-as-Judge scoring required (Hard) - Scoring mandate"
  - "H-16: Anti-leniency calibration required (Hard) - Bias countermeasure"
```

### Updated Self-Critique Checklist

```markdown
**Self-Critique Checklist (Before Response):**
- [ ] P-001: Is quality assessment based on defined criteria?
- [ ] P-002: Is critique persisted to file?
- [ ] P-003: Am I NOT managing the iteration loop?
- [ ] P-004: Are criteria and evidence cited?
- [ ] P-022: Are quality issues honestly reported?
- [ ] H-13: Is quality threshold correctly set (0.92 adversarial, 0.85 standard)?
- [ ] H-15: Is S-014 scoring included when required by criticality?
- [ ] H-16: Is anti-leniency calibration applied to S-014 scoring?
- [ ] SEQ: Are sequencing constraints (SEQ-001 through SEQ-005) respected?
```

---

## Traceability

### Requirements Coverage

| Requirement | Coverage |
|-------------|----------|
| FR-304-001 (10 modes) | Mode Registry Section -- all 10 modes defined |
| FR-304-002 (mode components) | Mode Registry + Evaluation Criteria -- complete component spec |
| FR-304-003 (explicit selection) | Invocation Protocol Updates -- mode parameter |
| FR-304-004 (automatic selection) | Configuration Schema -- auto_select_source |
| FR-304-006 (C1-C4 mapping) | Mode Registry -- criticality field per mode |
| FR-304-007 (auto-escalation) | Configuration Schema -- auto_escalation section |
| FR-304-008 (quality scoring) | Orchestration Guidance -- adversarial circuit breaker |
| FR-304-009 (creator-critic cycle) | Orchestration Guidance -- 3-iteration minimum |
| NFR-304-001 (P-003) | Capabilities -- forbidden actions updated |
| NFR-304-002 (token efficiency) | Mode Registry -- token_budget per mode |
| NFR-304-006 (quality gate) | Configuration Schema -- thresholds section |
| IR-304-003 (SSOT) | Configuration Schema -- threshold sourced from SSOT |
| IR-304-005 (ContentBlock) | Mode definitions aligned with ContentBlock priorities |
| BC-304-001 (default behavior) | standard mode preserved, default_mode: "standard" |
| BC-304-002 (workflow compat) | Session context backward compatible |
| BC-304-003 (threshold migration) | Dual threshold: 0.85 standard, 0.92 adversarial |

---

## References

| # | Citation | Relevance |
|---|----------|-----------|
| 1 | ps-critic.md v2.2.0 | Current agent specification (baseline for updates) |
| 2 | TASK-001 (this enabler) | Formal requirements |
| 3 | TASK-002 (this enabler) | Mode definitions, prompt templates, evaluation criteria |
| 4 | TASK-003 (this enabler) | Invocation protocol, selection algorithm, pipeline model |
| 5 | ADR-EPIC002-001 | Strategy selection, mechanistic families, composite scores |
| 6 | EN-303 TASK-003 | Per-strategy profiles, token budgets, pairing reference |
| 7 | EN-303 TASK-004 | Decision tree, auto-escalation, sequencing rules |
| 8 | Barrier-2 ENF-to-ADV | ContentBlock system, HARD rules, SSOT |

---

*Document ID: FEAT-004:EN-304:TASK-004*
*Agent: ps-architect-304*
*Created: 2026-02-13*
*Status: Draft*
