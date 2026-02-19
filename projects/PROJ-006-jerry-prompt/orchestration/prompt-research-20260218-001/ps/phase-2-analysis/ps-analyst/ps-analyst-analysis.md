# ps-analyst Analysis: Prompt Effectiveness Pattern Analysis

> **Document ID:** PROJ-006-PS-ANALYST-001
> **Agent:** ps-analyst
> **Phase:** Phase 2 — Analysis
> **Workflow:** prompt-research-20260218-001
> **Version:** 1.0.0
> **Date:** 2026-02-18
> **Status:** COMPLETE
> **Primary Artifact:** `analysis/prompt-pattern-analysis.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Agent State Output](#agent-state-output) | YAML state schema for orchestrator handoff |
| [Analysis Summary](#analysis-summary) | Condensed findings for pipeline consumption |
| [Key Deliverables Status](#key-deliverables-status) | Completion status of all required deliverables |
| [Hypothesis Disposition](#hypothesis-disposition) | Gate 1 carry-forward hypothesis outcomes |
| [Next Agent Hint](#next-agent-hint) | Routing recommendation for Phase 2 continuation |

---

## Agent State Output

```yaml
analyst_output:
  ps_id: "prompt-research-20260218-001"
  entry_id: "phase-2-analysis"
  artifact_path: "projects/PROJ-006-jerry-prompt/analysis/prompt-pattern-analysis.md"
  agent: "ps-analyst"
  phase: "phase-2-analysis"
  confidence: "high"
  analysis_scope:
    - "prompt_structure_categories: 5 categories identified"
    - "effectiveness_correlation_map: 4 categories mapped (C1-C2-C3-C5 with evidence)"
    - "anti_pattern_taxonomy: 8 anti-patterns documented"
    - "pattern_frequency_analysis: Jerry 8 patterns + external applicability assessed"
  top_correlations:
    - trait: "explicit_skill_invocation_plus_numeric_quality_threshold"
      strength: "STRONG"
      evidence: "Salesforce prompt anatomy; ps-critic circuit_breaker schema"
    - trait: "rich_context_provision_with_data_source_constraint"
      strength: "STRONG"
      evidence: "External survey Finding 1.2; jerry-internals P-01 activation-keywords"
    - trait: "multi_skill_composition_with_named_agents"
      strength: "STRONG"
      evidence: "jerry-internals Finding 7; external survey Section 3.1"
  top_anti_patterns:
    - id: "AP-01"
      name: "vague_directives_without_skill_routing"
      severity: "HIGH"
    - id: "AP-02"
      name: "missing_quality_thresholds"
      severity: "HIGH"
    - id: "AP-03"
      name: "monolithic_prompts_without_decomposition"
      severity: "HIGH"
  hypothesis_dispositions:
    H-01_cognitive_mode: "UNCONFIRMED — insufficient controlled comparison evidence"
    H-02_73pct_shared_content: "UNVERIFIABLE — structure confirmed, percentage lacks methodology"
    H-03_react_benchmarks: "DIRECTIONALLY PLAUSIBLE — qualify for frontier model applicability"
  gaps_identified:
    - "4 skill files uninvestigated: worktracker, nasa-se, transcript, architecture"
    - "Sample size: only 1 confirmed effective user prompt analyzed"
    - "Multi-model prompt calibration has no external literature baseline"
    - "P-07 utilization gap: highest-impact pattern requires explicit invocation but rarely observed"
  quality_indicators:
    all_correlations_cited: true
    hypotheses_distinguished_from_confirmed: true
    gate_1_carry_forward_addressed: true
    anti_pattern_remediation_provided: true
  next_agent_hint: "ps-synthesizer for cross-document pattern synthesis and final recommendations"
```

---

## Analysis Summary

### Five Prompt Structure Categories Identified

1. **Skill Invocation Prompts (C1)** — Slash-command activations. Effectiveness depends on specificity of agent naming and presence of quality threshold.

2. **Agent Orchestration Prompts (C2)** — Multi-agent pipeline requests. Highest effectiveness when numeric quality threshold is specified and adversarial critique pattern is named explicitly.

3. **Research/Investigation Prompts (C3)** — Open-ended information gathering. Effectiveness improves with data source constraints, organizational scope, and correct cognitive mode alignment (ps-researcher for divergent, ps-investigator for convergent).

4. **Implementation Prompts (C4)** — Concrete artifact production. Primarily benefits from external prompt engineering principles (output format specification, degrees-of-freedom matching, positive framing). Least Jerry-specific of all categories.

5. **Hybrid Prompts (C5)** — Multi-category composition. Highest overall effectiveness when all clauses are complete, each clause maps to a distinct skill/agent, and a numeric quality gate is present. The Salesforce prompt is the canonical exemplar.

### Highest-Impact Correlations (Confirmed)

The three traits with the strongest evidence-backed correlation to quality outcomes:

1. **Explicit skill invocation + numeric quality threshold** → Activates full Jerry architecture including circuit-breaker-protected critique loops
2. **Rich context with data source and organizational scope** → Deterministic agent routing; prevents hallucination of research domain
3. **Multi-skill composition with named agents** → Activates cross-skill orchestration and adversarial critique layers

### Most Critical Anti-Patterns

Three anti-patterns with highest impact on Jerry performance degradation:
- **AP-01 (Vague directives)** — Bypasses entire Jerry architecture
- **AP-02 (Missing quality thresholds)** — ps-critic defaults to internal heuristics
- **AP-03 (Monolithic prompts)** — Prevents orchestration and parallelization

### P-07 Utilization Gap — Key Finding

The Adversarial Critique Loop (P-07) has the highest quality impact of any Jerry pattern but requires explicit user invocation. It is the most underutilized high-value pattern based on the Phase 1 corpus analysis. This gap should be a primary focus of the synthesizer's recommendations.

### External Best Practice Applicability Summary

| Applicability | Best Practices |
|--------------|----------------|
| ALREADY IMPLEMENTED by Jerry | Role definition, XML tags, prompt chaining (via orchestration), ReAct (macroscopic implementation) |
| FULLY APPLICABLE (user can apply) | Specificity, numeric quality thresholds, positive framing, evaluation-driven criteria |
| PARTIALLY APPLICABLE | Few-shot examples, extended thinking directives, multi-model calibration |
| LOW APPLICABILITY in Jerry context | Zero-shot CoT (agents have embedded frameworks), tool description authoring |

---

## Key Deliverables Status

| Deliverable | Status | Location |
|-------------|--------|----------|
| Prompt Structure Categories (5) | COMPLETE | analysis/prompt-pattern-analysis.md — L1 Prompt Structure Categories |
| Effectiveness Correlation Map | COMPLETE | analysis/prompt-pattern-analysis.md — L1 Effectiveness Correlation Map |
| Anti-Pattern Taxonomy (8 patterns) | COMPLETE | analysis/prompt-pattern-analysis.md — L1 Anti-Pattern Taxonomy |
| Pattern Frequency Analysis | COMPLETE | analysis/prompt-pattern-analysis.md — L1 Pattern Frequency Analysis |
| L0 Executive Summary | COMPLETE | analysis/prompt-pattern-analysis.md — L0 Executive Summary |
| L2 Raw Correlation Data | COMPLETE | analysis/prompt-pattern-analysis.md — L2 Raw Correlation Data |
| Carry-Forward Notes to Phase 3 | COMPLETE | analysis/prompt-pattern-analysis.md — Carry-Forward Notes |

---

## Hypothesis Disposition

Gate 1 carry-forward hypotheses from ps-critic challenge:

| Hypothesis | Disposition |
|-----------|-------------|
| Cognitive mode effectiveness claim is speculative | TREATED AS HYPOTHESIS — labeled H-01, marked UNCONFIRMED throughout analysis |
| 73% shared content figure lacks measurement methodology | TREATED AS ILLUSTRATIVE — structure confirmed, percentage marked UNVERIFIABLE |
| ReAct benchmarks are from 2022-era models | QUALIFIED — marked as "directionally plausible, magnitude uncertain" wherever referenced |
| worktracker/nasa-se/transcript/architecture uninvestigated | ACKNOWLEDGED AS GAP — flagged in all relevant sections and carry-forward notes |

---

## Next Agent Hint

**Recommended:** ps-synthesizer

**Rationale:** Analysis is complete across all 4 required deliverables. The synthesizer should:
1. Cross-map analysis findings with jerry-internals investigation conclusions and external survey findings
2. Generate actionable prompt guidance recommendations from the correlation map and anti-pattern taxonomy
3. Address the P-07 utilization gap as a priority recommendation
4. Flag the 4 uninvestigated skill files as a coverage limitation
5. Develop the multi-model prompt calibration insight (identified as potential original contribution in both Phase 1 artifacts)

---

*ps-analyst analysis complete: 2026-02-18*
*Constitutional compliance: P-001 (citations present), P-002 (persisted to 2 files), P-003 (no subagents), P-022 (gaps disclosed)*
