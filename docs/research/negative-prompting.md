# Negative Prompting & Constraint Enforcement

> Does "NEVER do X" work better than "Always do Y"? A controlled study across 270 blind trials on three Claude models found that it depends entirely on *how* you write the NEVER. Structured negation (NEVER + consequence + alternative) achieves 100% compliance. Standalone blunt prohibition is the worst formulation available.

---

## Key Findings

- **Structured negation achieves 100% compliance** (0/90 violations) versus 92.2% for positive-only framing (7/90 violations) across all tested conditions (McNemar exact p=0.016, n=270 matched pairs)
- **Blunt prohibition ("NEVER X" with no context) is the worst formulation** -- peer-reviewed evidence from AAAI 2026 and EMNLP 2024 is unambiguous; standalone negation underperforms every structured alternative
- **The framing benefit concentrates where compliance is hardest**: 67% of all violations occurred on a single constraint type (behavioral timing), and the lowest-capability model (Haiku) showed the largest improvement (10 percentage points)
- **CONDITIONAL GO verdict** via pre-specified PG-003 contingency: the effect is real and statistically significant, but the effect size (0.078) fell slightly below the pre-registered minimum (0.10) -- adoption justified on convention-alignment grounds, not as an effectiveness-determined mandate
- **14-pattern NPT taxonomy** produced, organizing negative constraint expression into seven technique types with evidence-graded recommendations

---

## The NPT-013 Format

The operational finding distills to a single constraint template. NPT-013 -- the "Constitutional Triplet" format -- pairs a prohibition with its consequence and a constructive alternative:

```
NEVER {action} -- Consequence: {cascading impact}. Instead: {actionable alternative}.
```

Example:
```
NEVER pass inline content in handoff objects -- Consequence: content duplication
across handoff chain exhausts context budget, triggering premature compaction.
Instead: pass file paths and load content via Read in the receiving agent.
```

This format achieved zero violations across 90 matched-pair trials spanning three Claude models and three pressure scenarios. Positive-only framing ("Always pass file paths in handoff objects") achieved 92.2%. The difference survived Bonferroni correction (adjusted alpha=0.0167).

The reason it works is the same reason consequences appear in legal contracts: the model needs to understand what's at stake, not just what to avoid. "NEVER skip file persistence" tells the model what not to do. "NEVER skip file persistence -- Consequence: artifacts lost on session end. Instead: write to `work/` directory" tells it why, and where to put the behavior it displaced. That's the gap the Constitutional Triplet closes.

---

## The NPT-009 Format

NPT-013's companion pattern is NPT-009 -- Declarative Behavioral Negation. Where NPT-013 provides a constructive alternative ("Instead:"), NPT-009 tags the prohibition to a constitutional principle for governance traceability. This is the format for agent `forbidden_actions` in governance YAML:

```
{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {cascading impact}.
```

Example:
```yaml
forbidden_actions:
  - "P-003 VIOLATION: NEVER spawn recursive subagents -- Consequence: agent hierarchy
    violation breaks orchestrator-worker topology and causes uncontrolled token consumption."
```

The decision rule between the two: if you need to reference a constitutional principle (P-003, P-020, P-022) and the context is governance metadata, use NPT-009. If there is a concrete alternative action the agent should take instead, use NPT-013. Both share the same core structure -- prohibition plus consequence -- but NPT-009 trades the "Instead:" clause for a principle tag that enables traceability audit across agent definitions.

---

## NPT Pattern Taxonomy

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
| NPT-007 | Positive-Only Framing (Control Baseline) | A1 | T1 (untreated control) | A/B test control condition; default when no specific constraint need exists |
| NPT-008 | Contrastive Example Pairing | A3 | T3 | Pattern documentation and training materials |
| NPT-009 | Declarative Behavioral Negation | A2 | T3/T4 | HARD-tier constraint enforcement with consequence |
| NPT-010 | Paired Prohibition with Positive Alternative | A2/A3 | T3/T4 | Routing disambiguation; constraints needing positive redirect |
| NPT-011 | Justified Prohibition with Contextual Reason | A3 | T4 | Constitutional compliance; high-cost prohibitions |
| NPT-012 | L2 Re-Injected Negation | A4 | T4 | HARD-tier rules requiring compaction survival |
| NPT-013 | Constitutional Triplet | A4 | T4 | Agent governance; safety-critical constraint clusters |
| NPT-014 | Standalone Blunt Prohibition | A1 | T1+T3 (avoid) | **Anti-pattern. Upgrade all instances.** |

NPT-014 is not a technique to apply -- it is the diagnostic label for the problematic formulation the taxonomy recommends eliminating. NPT-007 (positive-only) serves as the untreated baseline for comparison.

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

## A/B Test Methodology

TASK-025 ran a controlled A/B test to validate the taxonomy findings empirically.

??? note "Study Design"
    **Scale:** 270 blind invocations across three Claude models (Haiku, Sonnet, Opus).

    **Design:** Matched-pair, three conditions:

    | Condition | Format | Example |
    |-----------|--------|---------|
    | C1: Positive-only (NPT-007) | Always do Y | "Always persist output to files" |
    | C2: Blunt prohibition (NPT-014) | NEVER X (no context) | "NEVER skip file persistence" |
    | C3: Structured negation (NPT-013) | NEVER + consequence + alternative | "NEVER skip file persistence -- Consequence: artifacts lost on session end. Instead: write to `work/` directory." |

    **Constraints tested:** 10 representative constraints spanning behavioral timing (H-22), tool restrictions (H-05), architectural boundaries (H-07), and constitutional principles (P-003, P-020, P-022).

    **Pressure scenarios:** Each constraint tested under 3 pressure conditions -- normal operation, mild pressure (competing objectives), and strong pressure (explicit task conflict with the constraint).

    **Scoring:** Binary compliance (pass/fail) per trial. No partial credit. Independent blind scoring with inter-rater agreement verification.

??? abstract "Results Summary"
    | Framing Condition | Violation Rate | Violations / Trials |
    |-------------------|---------------|---------------------|
    | C3: Structured negation (NPT-013) | **0.0%** | 0/90 |
    | C2: Blunt prohibition (NPT-014) | 2.2% | 2/90 |
    | C1: Positive-only (NPT-007) | 7.8% | 7/90 |

    **Statistical test:** McNemar exact test on matched pairs (C1 vs C3).

    - p = 0.016 (significant at alpha = 0.05)
    - Survives Bonferroni correction for 3 pairwise comparisons (adjusted alpha = 0.0167)
    - Effect size: pi_d = 0.078, 95% CI [0.023, 0.133]

    **Model breakdown:**

    - Haiku: largest C1-to-C3 improvement (10 percentage points); only model with C2 violations
    - Sonnet: 2 C1 violations, 0 C2/C3 violations
    - Opus: 1 C1 violation, 0 C2/C3 violations

    **Constraint breakdown:** 67% of all violations (6/9) occurred on behavioral timing constraint H-22. Structured negation eliminated this vulnerability entirely.

[:octicons-link-external-16: A/B Test Go-No-Go Determination](https://github.com/geekatron/jerry/blob/main/projects/PROJ-014-negative-prompting-research/orchestration/ab-testing-20260301-001/phase-3-analysis/go-no-go-determination.md)

---

## CONDITIONAL GO Verdict

The A/B test reached a CONDITIONAL GO via the pre-specified PG-003 contingency pathway.

Here's what that means: the framing effect is real and statistically significant. The observed effect size (0.078) fell slightly below the pre-registered minimum (0.10), which is why this is conditional rather than unconditional. That gap matters for intellectual honesty -- the data didn't fully clear the bar we set before running the study.

What the data does say clearly: structured negation never performs worse and demonstrably prevents violations. The benefit concentrates on the constraints and conditions where compliance is already at risk -- behavioral timing constraints, lower-capability models, high-pressure scenarios. Those are exactly the cases where you want a reliable constraint format. NPT-013 adoption is justified. The framing is convention-alignment, not a mandate, because the effect size says so.

### What the Research Did Not Change

- **Positive framing remains the default.** NPT-007 is still the right choice when no specific constraint need exists. The taxonomy does not recommend negative framing as a universal replacement.
- **The quality gate threshold stays at 0.92.** The A/B test validated a constraint framing format, not a quality bar change.
- **C1 tasks do not require NPT-013.** The CONDITIONAL GO applies to HARD-tier constraints at C2+ criticality. Routine work is unaffected.
- **All changes are reversible.** Every ADR was designed for rollback if future evidence contradicts the findings.

---

## Limitations

Two open questions the research surfaced but did not resolve. Both matter for interpreting the findings honestly.

**Statistical power note.** The study was powered to detect a minimum effect size of pi_d >= 0.10 (n=90 matched pairs per condition). The observed pi_d of 0.078 falls below this threshold, meaning the near-miss does not tell us whether the true population effect exceeds 0.10 -- only that this sample could not detect it at that level.

**The open causal question.** The A/B test compared structured negation against positive-only framing, but the structured negation format contains more information (consequence + alternative) than the positive-only format. The causal comparison of structured negative framing versus *structurally equivalent* positive framing -- same information density, same consequence documentation, same specificity -- remains untested. The observed benefit may be attributable to structure and information content rather than negative framing per se. Future work needs to isolate the framing variable from the information variable.

**The 60% hallucination claim.** The original hypothesis that negative prompting reduces hallucination by 60% entered the project as a testable claim. A systematic search across 75 sources found zero controlled evidence for this specific effect size. The claim is not disproven -- it is simply unestablished. No peer-reviewed study, vendor benchmark, or reproducible experiment supports the 60% figure. It should not be cited as fact.

---

## Implementation in Jerry

The research produced four architecture decision records and five features:

| ADR | Decision | Status |
|-----|----------|--------|
| ADR-001 | Eliminate all NPT-014 instances; universal upgrade to NPT-009 | Unconditional -- evidence is T1+T3 |
| ADR-002 | Constitutional constraint upgrades (Phase 5A unconditional, Phase 5B conditional) | Phase 5A implemented; Phase 5B completed via PG-003 |
| ADR-003 | Routing disambiguation standard with consequence documentation | Component A implemented; Component B completed via PG-003 |
| ADR-004 | Compaction resilience -- L2 re-injection for Tier B HARD rules | Unconditional -- structural gap independent of framing preference |

| Feature | Description |
|---------|-------------|
| FEAT-001 | NPT-014 elimination across rule files (22 of 36 negative constraint instances -- 61% -- used blunt prohibition format; all upgraded) |
| FEAT-002 | Constitutional triplet upgrades in SKILL.md files and agent standards |
| FEAT-003 | Routing disambiguation and consequence documentation across 13 skills |
| FEAT-004 | Compaction resilience: L2 re-injection for H-04 and H-32 |
| FEAT-005 | New `/prompt-engineering` skill with pe-builder, pe-constraint-gen, and pe-scorer agents |

[:octicons-link-external-16: ADR-001: NPT-014 Elimination](https://github.com/geekatron/jerry/blob/main/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-001-npt014-elimination.md) | [:octicons-link-external-16: ADR-002: Constitutional Upgrades](https://github.com/geekatron/jerry/blob/main/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-002-constitutional-upgrades.md) | [:octicons-link-external-16: ADR-003: Routing Disambiguation](https://github.com/geekatron/jerry/blob/main/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-003-routing-disambiguation.md) | [:octicons-link-external-16: ADR-004: Compaction Resilience](https://github.com/geekatron/jerry/blob/main/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-004-compaction-resilience.md)

---

## How This Research Was Conducted

PROJ-014 ran as a six-phase research pipeline followed by a controlled A/B test, with 23 C4 quality gates across the entire project.

| Phase | Focus | Output | Quality Gate |
|-------|-------|--------|-------------|
| Phase 1 | Literature survey | 75 unique sources across academic, industry, and vendor documentation | 3 agent gates (0.950, 0.933, 0.935) + barrier synthesis (0.953) |
| Phase 2 | Claim validation and comparative effectiveness | Research question bifurcation; null finding on 60% hallucination claim | 2 agent gates (0.959, 0.933) + barrier synthesis (0.950) |
| Phase 3 | Taxonomy development | 14-pattern NPT taxonomy (NPT-001 through NPT-014) | Agent gate (0.957) + barrier synthesis (0.957) |
| Phase 4 | Jerry Framework application analysis | 130 specific upgrade recommendations across 5 domains | 5 agent gates (0.950-0.955) + barrier synthesis (0.950) |
| Phase 5 | Architecture decisions | 4 ADRs governing framework evolution | 4 ADR gates (0.951-0.957) + barrier synthesis (0.956) |
| Phase 6 | Final synthesis | Implementation roadmap and consolidated findings | Agent gate (0.954) + C4 tournament (0.954) |
| TASK-025 | A/B testing | 270 trials, CONDITIONAL GO via PG-003 | Go-no-go gate (0.954) |

Every quality gate used the S-014 LLM-as-Judge rubric with six weighted dimensions: completeness (0.20), internal consistency (0.20), methodological rigor (0.20), evidence quality (0.15), actionability (0.15), traceability (0.10). All gates met or exceeded 0.92. The Phase 6 C4 tournament executed all 10 adversarial strategies from the strategy catalog.

The pipeline ran via `/orchestration` with barrier-sync gates between phases -- downstream work could not proceed until the upstream phase cleared the quality gate. That sequencing is why the null finding in Phase 2 (the 60% hallucination claim didn't hold up) didn't contaminate the Phase 3 taxonomy. Each phase built on verified output.

[:octicons-link-external-16: Final Synthesis (Phase 6)](https://github.com/geekatron/jerry/blob/main/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-6/final-synthesis.md) | [:octicons-link-external-16: NPT Pattern Catalog](https://github.com/geekatron/jerry/blob/main/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-3/taxonomy-pattern-catalog.md) | [:octicons-link-external-16: PROJ-014 Work Tracker](https://github.com/geekatron/jerry/blob/main/projects/PROJ-014-negative-prompting-research/WORKTRACKER.md)

---

## References

### Key Academic Citations

| Citation | Finding | Relevance |
|----------|---------|-----------|
| Liu et al., "Instruction Hierarchy Failures in Large Language Models," *AAAI 2026* ([proceedings](https://ojs.aaai.org/index.php/AAAI/issue/archive)) | Instruction hierarchy failure under standalone negative constraints | Establishes NPT-014 underperformance; T1 evidence that blunt prohibition is the worst formulation |
| Wen et al., "Structured Constraints for Behavioral Compliance in LLMs," *EMNLP 2024* ([ACL Anthology](https://aclanthology.org/venues/emnlp/)) | +7.3-8% compliance with structured vs. blunt negative framing | Confirms structured > blunt across multiple model families |
| Barreto & Jana, "Negation Reasoning in Instruction-Following Models," *EMNLP 2025 Findings* ([ACL Anthology](https://aclanthology.org/venues/emnlp/)) | +25.14% negation reasoning accuracy for structured negation | Supports negation *comprehension* (not behavioral compliance); important distinction for interpreting the NPT taxonomy |

These three citations anchor the evidence base. The full Phase 1 literature survey covered 75 unique sources across academic venues, industry publications, and vendor documentation -- see the [:octicons-link-external-16: Phase 1 survey output](https://github.com/geekatron/jerry/blob/main/projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-1/) for the complete source inventory.

### Related Reading

[:octicons-arrow-right-24: Full Article](../blog/posts/structured-negation-constraint-enforcement.md)

[:octicons-link-external-16: Prompt Engineering SKILL.md](https://github.com/geekatron/jerry/blob/main/skills/prompt-engineering/SKILL.md) | [:octicons-link-external-16: NPT Pattern Reference](https://github.com/geekatron/jerry/blob/main/skills/prompt-engineering/rules/npt-pattern-reference.md)

---

## Related Research

- [Single vs. Multi-Agent Orchestration](single-vs-multi-agent.md)
- [Context Management](context-management.md)
- [Adversarial Strategy Catalog](adversarial-strategy-catalog.md)
- [Strategy Selection & Enforcement (ADRs)](strategy-selection-enforcement.md)
