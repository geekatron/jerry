---
date: 2026-03-01
categories:
  - Prompting
  - Quality
authors:
  - geekatron
slug: structured-negation-constraint-enforcement
---

# Structured Negation in LLM Constraint Enforcement

Does "NEVER do X" work better than "Always do Y"? PROJ-014 spent six research phases and a controlled A/B test finding out. The short answer: it depends entirely on how you write the NEVER.

**The core finding:** NPT-013 structured negation -- a constraint format that pairs a prohibition with its consequence and a constructive alternative -- achieves 100% compliance across all tested conditions. Positive-only framing achieves 92.2%. The difference is statistically significant (McNemar exact p=0.016, n=270 matched pairs across three Claude models).

**The format that works:**

```
NEVER {action} -- Consequence: {cascading impact}. Instead: {actionable alternative}.
```

**The format that does not:**

```
Don't do X.
```

Standalone blunt prohibitions -- "NEVER do X" with nothing else -- are the *worst* formulation available. Worse than positive-only framing, worse than any structured alternative. Peer-reviewed evidence from AAAI 2026 and EMNLP 2024 is unambiguous on this. When you add consequence documentation and a constructive alternative, the picture reverses: structured negation never underperforms positive-only framing and demonstrably prevents violations on the constraint types where compliance is hardest.

This article covers what the research found, the taxonomy it produced, and how to apply the findings.

<!-- more -->

## Research Background

### The Problem

LLM-based agent frameworks live on behavioral constraints -- rules like "never spawn recursive subagents" or "always persist output to files." These constraints are expressed as natural language instructions in system prompts, rule files, and agent definitions. The question is whether the *framing* of those constraints affects how reliably the LLM follows them.

The conventional wisdom was split. Anthropic's published guidance generally recommends positive framing ("tell the model what to do, not what to avoid"). At the same time, Anthropic's own Claude Code rule files contain 33 instances of NEVER/MUST NOT/DO NOT across 10 files, all in the highest enforcement tier. The Jerry Framework itself had 36 negative constraint instances across 17 rule files at the start of this research, with 22 of those (61%) being bare "NEVER X" statements -- no consequence, no alternative.

### The Hypothesis

PROJ-014 started with two claims to test:

1. **Claim A:** Negative unambiguous prompting reduces hallucination by 60%.
2. **Claim B:** Negative prompting achieves better results than explicit positive prompting.

These were split into independently testable questions and pursued through a six-phase pipeline.

### Methodology

| Phase | Focus | Output |
|-------|-------|--------|
| Phase 1 | Literature survey | 75 unique sources across academic, industry, and vendor documentation |
| Phase 2 | Claim validation and comparative effectiveness | Research question bifurcation; null finding on 60% claim |
| Phase 3 | Taxonomy development | 14-pattern NPT taxonomy (NPT-001 through NPT-014) |
| Phase 4 | Jerry Framework application analysis | 130 specific upgrade recommendations across 5 domains |
| Phase 5 | Architecture decisions | 4 ADRs governing framework evolution |
| Phase 6 | Final synthesis | Implementation roadmap and consolidated findings |

After the six-phase research, TASK-025 ran a controlled A/B test: 270 blind invocations across three Claude models (Haiku, Sonnet, Opus), testing 10 constraints under 3 framing conditions with 3 pressure scenarios each. All quality gate scores across the research pipeline met or exceeded the 0.92 threshold, with most scoring above 0.950.

---

## Key Findings

### The 60% Claim: Untested, Not Disproven

The primary claim -- that negative prompting reduces hallucination by 60% -- has no evidential basis. A systematic search across 75 sources found zero controlled evidence for this specific effect size. The claim entered the project as a hypothesis. It is not disproven; it is simply unestablished.

### Blunt Prohibition Is the Worst Formulation

This is the single most actionable finding. It does not depend on further experimentation. Peer-reviewed evidence establishes that standalone NEVER/MUST NOT statements without consequence documentation produce inferior behavioral outcomes versus any structured alternative:

- Liu's team at AAAI 2026 documented instruction hierarchy failure under standalone negative constraints.
- Wen's team at EMNLP 2024 found a +7.3-8% compliance improvement with structured versus blunt negative framing.
- arXiv T3 evidence: 55% improvement for affirmative directive pairing versus standalone negation.

At the start of this research, 61% of all negative constraints in the Jerry Framework (22 out of 36) used this blunt prohibition format. Every one was an upgrade candidate.

### Structured Negation Achieves 100% Compliance

The A/B test produced a consistent ordering across all three Claude models:

| Framing Condition | Format | Violation Rate |
|-------------------|--------|---------------|
| C3: Structured negation (NPT-013) | NEVER + consequence + alternative | 0.0% (0/90) |
| C2: Blunt prohibition (NPT-014) | NEVER X (no context) | 2.2% (2/90) |
| C1: Positive-only (NPT-007) | Always do Y | 7.8% (7/90) |

The pooled McNemar exact p-value for C1 versus C3 is 0.016, significant at alpha=0.05 and surviving Bonferroni correction for three pairwise comparisons (adjusted alpha=0.0167). The effect size (pi_d=0.078) is modest but nonzero, with a 95% confidence interval of 0.023 to 0.133.

Two additional findings from the A/B test worth holding onto:

67% of all violations (6 of 9) occurred on a single constraint type -- H22, behavioral timing. Structured negation eliminated this vulnerability entirely. And the lower-capability models benefit most: Haiku showed the largest C1-to-C3 improvement (10 percentage points) and was the only model with C2 violations. The framing benefit concentrates where compliance is hardest.

### CONDITIONAL GO, Not Unconditional Mandate

The A/B test reached a CONDITIONAL GO via the pre-specified PG-003 contingency pathway. The framing effect is real and statistically significant, but the effect size fell slightly below the pre-registered minimum (0.078 observed versus 0.10 threshold). That means NPT-013 adoption is justified on *convention-alignment* grounds -- structured negation never performs worse and demonstrably prevents violations -- not on an effectiveness-determined mandate.

The practical implication: if you are deciding whether to use structured negation in your own work, the evidence says it is safe and beneficial, not that it is categorically required. The benefit concentrates on the constraints and conditions where compliance is already at risk.

---

## The NPT Pattern Taxonomy

The research produced a 14-pattern taxonomy organizing how negative constraints can be expressed, sorted into seven technique types.

### Technique Types

| Type | Name | Description |
|------|------|-------------|
| A1 | Prohibition-only | Standalone negation without structure |
| A2 | Structured prohibition | Negation with consequence, scope, or decomposition |
| A3 | Augmented prohibition | Negation enhanced with examples, alternatives, or justification |
| A4 | Enforcement-tier prohibition | Negation tied to enforcement mechanism (L2 re-injection, constitutional triplet) |
| A5 | Programmatic enforcement | Code-level or infrastructure-level constraint enforcement |
| A6 | Training-time constraint | Model-internal behavioral intervention (RLHF, fine-tuning) |
| A7 | Meta-prompting | Constraint priming and atomic decomposition |

### Pattern Catalog

| Pattern | Name | Type | Evidence | Recommendation |
|---------|------|------|----------|----------------|
| NPT-001 | Model-Internal Behavioral Intervention | A6 | T1 (peer-reviewed) | Foundation model fine-tuning; requires model access |
| NPT-002 | Instruction Hierarchy Prioritization | A6 | T1 | System prompt structural enforcement |
| NPT-003 | Hard-Coded Constraint Integration | A5 | T4 | Non-negotiable limits baked into infrastructure |
| NPT-004 | Output Filter and Validation | A5 | T4 | Post-generation constraint enforcement |
| NPT-005 | Warning-Based Meta-Prompt | A7 | T3/T4 | Pre-task constraint priming |
| NPT-006 | Atomic Decomposition of Constraints | A7 | T4 | Break compound constraints into single sub-constraints |
| NPT-007 | Positive-Only Framing | -- | Untested baseline | Default when no specific constraint need exists |
| NPT-008 | Contrastive Example Pairing | A3 | T3 | Pattern documentation and training materials |
| NPT-009 | Declarative Behavioral Negation | A2 | T3/T4 | HARD-tier constraint enforcement with consequence |
| NPT-010 | Paired Prohibition with Positive Alternative | A2/A3 | T3/T4 | Routing disambiguation; constraints needing positive redirect |
| NPT-011 | Justified Prohibition with Contextual Reason | A3 | T4 | Constitutional compliance; high-cost prohibitions |
| NPT-012 | L2 Re-Injected Negation | A4 | T4 | HARD-tier rules requiring compaction survival |
| NPT-013 | Constitutional Triplet | A4 | T4 | Agent governance; safety-critical constraint clusters |
| NPT-014 | Standalone Blunt Prohibition | A1 | T1+T3 (avoid) | Anti-pattern. Upgrade all instances. |

NPT-014 is not a technique to apply -- it is the diagnostic label for the problematic formulation the taxonomy recommends eliminating. NPT-007 (positive-only) serves as the untreated baseline for comparison.

### The Two Patterns That Matter Most

For day-to-day use in the Jerry Framework, two patterns emerged as the operational workhorses.

**NPT-009 (Declarative Behavioral Negation)** -- Used for agent governance YAML `forbidden_actions` where a constitutional principle reference provides traceability:

```
{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {cascading impact}.
```

Example:
```yaml
forbidden_actions:
  - "P-003 VIOLATION: NEVER spawn recursive subagents -- Consequence: agent hierarchy
    violation breaks orchestrator-worker topology and causes uncontrolled token consumption."
```

**NPT-013 (Constitutional Triplet format)** -- Used for behavioral constraints, routing rules, and methodology guardrails where a constructive alternative exists:

```
NEVER {action} -- Consequence: {cascading impact}. Instead: {actionable alternative}.
```

Example:
```
NEVER pass inline content in handoff objects -- Consequence: content duplication across
handoff chain exhausts context budget, triggering premature compaction. Instead: pass file
paths and load content via Read in the receiving agent.
```

The key distinction: NPT-013 adds an "Instead:" clause that provides a constructive replacement action. NPT-009 states the consequence only. Use NPT-009 when tracing to a constitutional principle; use NPT-013 when a concrete alternative action exists.

---

## Practical Application

### Using the `/prompt-engineering` Skill

The research findings are operationalized through the `/prompt-engineering` skill, which provides three agents:

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| `pe-builder` | Interactive prompt assembly | Building structured prompts from scratch |
| `pe-constraint-gen` | NPT pattern constraint formatter | Converting intent descriptions into NPT-009/NPT-013 constraints |
| `pe-scorer` | Prompt quality evaluation | Scoring prompts against the 7-criterion rubric |

To generate constraints, describe your intent in natural language:

```
"Generate NPT-013 constraints for a research agent that must not hallucinate sources"
```

The `pe-constraint-gen` agent selects the appropriate NPT pattern, formats the constraint, and wraps it in the correct XML structure for the target context (governance YAML, agent markdown body, or standalone block).

### Deciding Between NPT-009 and NPT-013

| Context | Pattern | Rationale |
|---------|---------|-----------|
| Agent `forbidden_actions` in governance YAML | NPT-009 | Principle-tagged for constitutional traceability |
| SKILL.md routing disambiguation | NPT-013 | "Instead:" redirects to the correct skill |
| Rule file behavioral constraints | NPT-013 | "Instead:" provides the corrective action |
| Agent markdown body guardrails | NPT-013 | Full consequence + alternative improves compliance |
| Constitutional compliance tables | NPT-009 | Principle prefix enables traceability audit |

The decision rule: if you need to reference a constitutional principle (P-003, P-020, P-022) and the context is governance metadata, use NPT-009. If there is a concrete alternative action the agent should take instead, use NPT-013.

### Upgrading Existing Constraints

When you encounter a constraint that looks like this:

```
NEVER hardcode values.
```

That is NPT-014 -- the formulation peer-reviewed evidence establishes as the worst option. Here is how to upgrade it.

**Step 1:** Add specificity and consequence (NPT-009):
```
NEVER hardcode configuration values in source files -- Consequence: credential exposure
risk; testability failure; CI environment mismatch.
```

**Step 2:** Add a constructive alternative (NPT-013):
```
NEVER hardcode configuration values in source files -- Consequence: credential exposure
risk; testability failure; CI environment mismatch. Instead: use environment variables
via src/shared_kernel/config.py.
```

Three criteria to check against the finished constraint: the action must be binary-testable (an observer can verify compliance without interpretation), the consequence must name the specific downstream effect (not "quality degrades"), and the alternative must be achievable with the agent's declared tools.

---

## Implementation in Jerry

### Architecture Decision Records

PROJ-014 produced four ADRs governing how the findings are applied to the Jerry Framework:

| ADR | Decision | Status |
|-----|----------|--------|
| ADR-001 | Eliminate all NPT-014 instances; universal upgrade to NPT-009 | Unconditional -- evidence is T1+T3 |
| ADR-002 | Constitutional constraint upgrades (Phase 5A unconditional, Phase 5B conditional) | Phase 5A implemented; Phase 5B completed via PG-003 |
| ADR-003 | Routing disambiguation standard with consequence documentation | Component A implemented; Component B completed via PG-003 |
| ADR-004 | Compaction resilience -- L2 re-injection for Tier B HARD rules | Unconditional -- structural gap independent of framing preference |

### Features Delivered

| Feature | Description |
|---------|-------------|
| FEAT-001 | ADR-001 implementation: NPT-014 elimination across rule files |
| FEAT-002 | ADR-002 Phase 5A: constitutional triplet upgrades in SKILL.md files and agent standards |
| FEAT-003 | ADR-003 routing disambiguation and consequence documentation across 13 skills |
| FEAT-004 | ADR-004 compaction resilience: L2 re-injection for H-04 and H-32 |
| FEAT-005 | New `/prompt-engineering` skill with pe-builder, pe-constraint-gen, and pe-scorer agents |

### The `/prompt-engineering` Skill

The most visible output of the research is the new `/prompt-engineering` skill, which encodes three knowledge sources into reusable tooling:

1. **NPT pattern reference** -- The pe-constraint-gen agent uses the taxonomy to select the appropriate pattern and format constraints systematically.
2. **Prompt quality rubric** -- The pe-scorer agent implements the 7-criterion evaluation framework (task specificity, skill routing, context provision, quality specification, decomposition, output specification, positive framing).
3. **5-element prompt anatomy** -- The pe-builder agent walks users through structured prompt construction (routing, scope, data source, quality gate, output path).

### What the Research Did Not Change

The CONDITIONAL GO verdict means the research was honest about what the data showed:

- Structured negation is adopted as the *preferred* format, not an effectiveness-proven mandate.
- Convention-alignment -- it works at least as well as alternatives and matches Anthropic's own practice -- is the rationale, not causal superiority.
- All framework changes are reversible if future evidence contradicts the findings.
- The causal comparison of structured negative versus structurally equivalent positive framing remains the open research question for future work.

---

## References

### Primary Research Artifacts

| Document | Location |
|----------|----------|
| Final synthesis (Phase 6) | [:octicons-link-external-16: final-synthesis.md](https://github.com/geekatron/jerry/blob/feat/proj-014-negative-prompting-research/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md) |
| A/B testing go-no-go determination | [:octicons-link-external-16: go-no-go-determination.md](https://github.com/geekatron/jerry/blob/feat/proj-014-negative-prompting-research/projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-3-analysis/go-no-go-determination.md) |
| NPT pattern reference | [:octicons-link-external-16: npt-pattern-reference.md](https://github.com/geekatron/jerry/blob/feat/proj-014-negative-prompting-research/skills/prompt-engineering/rules/npt-pattern-reference.md) |
| NPT taxonomy catalog | [:octicons-link-external-16: taxonomy-pattern-catalog.md](https://github.com/geekatron/jerry/blob/feat/proj-014-negative-prompting-research/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md) |
| Prompt Engineering SKILL.md | [:octicons-link-external-16: SKILL.md](https://github.com/geekatron/jerry/blob/feat/proj-014-negative-prompting-research/skills/prompt-engineering/SKILL.md) |

### Architecture Decision Records

| ADR | Location |
|-----|----------|
| ADR-001: NPT-014 Elimination | [:octicons-link-external-16: ADR-001](https://github.com/geekatron/jerry/blob/feat/proj-014-negative-prompting-research/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-001-npt014-elimination.md) |
| ADR-002: Constitutional Upgrades | [:octicons-link-external-16: ADR-002](https://github.com/geekatron/jerry/blob/feat/proj-014-negative-prompting-research/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-002-constitutional-upgrades.md) |
| ADR-003: Routing Disambiguation | [:octicons-link-external-16: ADR-003](https://github.com/geekatron/jerry/blob/feat/proj-014-negative-prompting-research/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-003-routing-disambiguation.md) |
| ADR-004: Compaction Resilience | [:octicons-link-external-16: ADR-004](https://github.com/geekatron/jerry/blob/feat/proj-014-negative-prompting-research/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-004-compaction-resilience.md) |

### Key Academic Citations

| Citation | Source | Relevance |
|----------|--------|-----------|
| Liu et al., AAAI 2026 | Instruction hierarchy failure under standalone negative constraint | Establishes NPT-014 underperformance |
| Wen et al., EMNLP 2024 | +7.3-8% compliance with structured vs. blunt negative framing | Confirms structured > blunt |
| Barreto & Jana, EMNLP 2025 Findings | +25.14% negation reasoning accuracy for structured negation | Supports negation comprehension (not behavioral compliance) |

---

*Source: PROJ-014 Negative Prompting Research (2026-02-27 through 2026-03-01). Six-phase research pipeline + controlled A/B test (TASK-025). All quality gate scores >= 0.92.*
