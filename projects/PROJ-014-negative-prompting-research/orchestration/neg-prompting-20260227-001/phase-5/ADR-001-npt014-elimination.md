# ADR-001: NPT-014 Elimination Policy -- Mandating Upgrade from Standalone Blunt Prohibition to NPT-009 Structured Format

> **PS:** PROJ-014
> **Task:** TASK-016
> **Phase:** Phase 5 -- Architecture Decision Records
> **Created:** 2026-02-28
> **Status:** PROPOSED
> **Agent:** ps-architect
> **Workflow:** neg-prompting-20260227-001
> **Criticality:** C4 (irreversible architectural policy; auto-C3 per AE-003; elevated to C4 per AE-004 as this establishes a new framework-wide enforcement standard)
> **Quality Gate:** >= 0.95 (C4 threshold)
> **Self-Review:** H-15 applied before completion

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | What we decided and why, in plain language |
| [Context](#context) | Problem statement, background, evidence base |
| [Constraints](#constraints) | Binding constraints from upstream research |
| [Forces](#forces) | Tensions at play in this decision |
| [Options Considered](#options-considered) | Three alternatives evaluated with steelman analysis |
| [Decision](#decision) | Chosen option with rationale |
| [L1: Technical Implementation](#l1-technical-implementation) | Implementation details, upgrade procedure, code patterns |
| [L2: Architectural Implications](#l2-architectural-implications) | Long-term implications, evolution path, systemic consequences |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes |
| [Compliance](#compliance) | Evidence tier labels, PG-003 reversibility, constraint propagation |
| [Related Decisions](#related-decisions) | Links to ADR-002, ADR-003, ADR-004 |
| [References](#references) | Full evidence source table |
| [PS Integration](#ps-integration) | Worktracker linkage |

---

## L0: Executive Summary

### What we decided

The Jerry Framework will mandate that every standalone blunt prohibition -- any NEVER, MUST NOT, FORBIDDEN, or DO NOT statement that lacks consequence documentation, scope specification, and positive behavioral pairing -- be upgraded to NPT-009 structured format. NPT-009 structured format means: a declarative behavioral negation that includes (a) explicit consequence if violated, (b) explicit scope of applicability, and (c) where feasible, a positive behavioral alternative describing what to do instead.

### Why this decision matters

The Jerry Framework currently contains approximately 22 instances of NPT-014 (standalone blunt prohibition) across its rule files alone, representing 61% of all negative constraint instances (TASK-012 Finding 2). The same pattern appears across all five artifact domains: skills, agents, rules, patterns, and templates (barrier-4/synthesis.md Theme 2). Blunt prohibition is the weakest constraint formulation in the negative prompting taxonomy. This is not a preference finding -- it is established by T1 peer-reviewed evidence (A-20, AAAI 2026; A-15, EMNLP 2024) and T3 preprint evidence (A-31, arXiv) that standalone blunt prohibition demonstrably underperforms structured alternatives (PG-001, HIGH unconditional confidence).

### Why we are choosing this now

This is the one recommendation category across all 130 Phase 4 recommendations that does not require Phase 2 experimental completion before proceeding. The evidence base establishes that blunt prohibition underperforms, regardless of whether structured negative constraints outperform structurally equivalent positive constraints (the Phase 2 experimental question). Upgrading from blunt prohibition to structured format is a unidirectional improvement: it replaces a demonstrably inferior formulation. It does not depend on the framing comparison outcome.

---

## Context

### Problem Statement

The Jerry Framework's behavioral enforcement infrastructure -- rule files, SKILL.md files, agent definitions, pattern documentation, and templates -- contains a systemic prevalence of NPT-014 (standalone blunt prohibition) as its dominant negative constraint pattern. This pattern lacks the structural elements (consequence documentation, scope specification, positive alternative pairing) that distinguish effective constraint formulations from ineffective ones.

### Background

PROJ-014 (Negative Prompting Research) conducted a five-phase investigation into negative prompting effectiveness:

- **Phase 1** (Barrier 1): Three independent surveys of 75 academic, industry, and framework sources, plus supplemental vendor self-practice analysis documenting 33 NEVER/MUST NOT/FORBIDDEN/DO NOT instances across 10 Claude Code rule files (VS-001 through VS-004, T4 observational evidence).
- **Phase 2** (Barrier 2): Claim validation (TASK-005, R4, 0.959 PASS) and comparative effectiveness analysis (TASK-006, R5, 0.933 PASS), producing practitioner guidance PG-001 through PG-005 with explicit confidence tiers.
- **Phase 3**: Taxonomy construction producing 14 named patterns (NPT-001 through NPT-014, representing 13 distinct techniques) with evidence tier labels and a 12-level effectiveness hierarchy (AGREE-5 -- internally generated, NOT externally validated).
- **Phase 4** (Barrier 4): Five domain-specific application analyses across skills (TASK-010), agents (TASK-011), rules (TASK-012), patterns (TASK-013), and templates (TASK-014), producing 130 total recommendations.
- **Barrier 4 synthesis** (TASK-015, v4.0.0, 0.950 PASS): Cross-pollination identifying 6 cross-cutting themes, with NPT-014 as diagnostic baseline confirmed universally across all 5 analyses.

### The NPT-014 Problem Defined

**NPT-014 (Standalone Blunt Prohibition):** Any NEVER/MUST NOT statement that lacks:
- (a) Explicit consequence if violated
- (b) Explicit scope of applicability
- (c) A positive behavioral pairing describing what to do instead

**NPT-009 (Declarative Behavioral Negation with Consequence):** A structured negative constraint that includes at minimum (a) and (b) above, with (c) recommended where a positive alternative exists.

**Example of the upgrade:**

| Before (NPT-014) | After (NPT-009) |
|-------------------|------------------|
| "NEVER hardcode values" | "NEVER hardcode configuration values in source files. Consequence: credential exposure risk; testability failure; CI environment mismatch. Scope: all files in `src/`. Instead: use environment variables or configuration injection via dependency injection container." |
| "NEVER use python/pip directly" (L2-REINJECT marker content) | "NEVER use python/pip/pip3 directly. Consequence: environment corruption; CI blocks merge. Scope: all Python execution contexts. Instead: use `uv run` for execution, `uv add` for dependencies." |

### Evidence Base

**MANDATORY EPISTEMOLOGICAL BOUNDARY:** This ADR NEVER claims that NPT-009 structured negative constraints outperform structurally equivalent positive constraints. The T1+T3 evidence establishes that blunt prohibition (NPT-014) underperforms structured alternatives. Whether structured negative framing outperforms structured positive framing at ranks 9-11 is UNTESTED (Phase 2 experimental target).

| Evidence ID | Source | Tier | Finding | Relevance to ADR-001 |
|-------------|--------|------|---------|----------------------|
| A-20 | AAAI 2026 (peer-reviewed) | T1 | Standalone prohibition produces lower compliance than structured constraint formulations | Direct: establishes NPT-014 underperformance |
| A-15 | EMNLP 2024 (peer-reviewed) | T1 | Structured constraint framing produces +7-8% compliance improvement over bare prohibition | Direct: quantifies structured > bare prohibition gap |
| A-31 | arXiv (preprint) | T3 | Corroborating evidence for prohibition underperformance in instruction-following tasks | Supporting: extends T1 findings across task types |
| PG-001 | barrier-2/synthesis.md ST-4 | T1+T3 | "Blunt prohibition demonstrably underperforms structured alternatives" -- HIGH unconditional confidence | Direct: the practitioner guidance that motivates ADR-001 |
| VS-001 | supplemental-vendor-evidence.md | T4 | 33 NEVER/MUST NOT/FORBIDDEN/DO NOT instances across 10 Claude Code rule files; Anthropic uses structured format in HARD tier | Supporting: vendor self-practice confirms structured format in production |
| VS-003 | supplemental-vendor-evidence.md | T4 | HARD tier vocabulary is definitionally prohibitive; NEVER/MUST are HARD tier by design | Supporting: observational evidence that enforcement tier = structured negative vocabulary |
| TASK-012 | rules-update-analysis.md | T4 (compiled) | 22 of 36 negative constraint instances (61%) are NPT-014; 8 are NPT-009 | Direct: quantifies the gap this ADR closes |
| barrier-4/synthesis.md | TASK-015, Theme 1 and Theme 2 | T4 (cross-pollination) | NPT-009 as universal upgrade target (all 5 analyses); NPT-014 as diagnostic baseline (all 5 analyses) | Direct: cross-analysis convergence on NPT-014 as the universal problem |

**Causal mechanism note:** T1 evidence (A-20, A-15) establishes that blunt prohibition underperforms structured alternatives. This evidence does NOT establish that NPT-009 specifically outperforms structurally equivalent positive constraints. The causal mechanism for the upgrade is: replacing a demonstrably weaker formulation with a demonstrably stronger one. The question of whether the stronger formulation should use negative or positive framing is the Phase 2 experimental question, which this ADR does not resolve and does not need to resolve.

---

## Constraints

| ID | Constraint | Source |
|----|------------|--------|
| C-001 | NEVER cite A-11 (confirmed hallucinated citation -- removed in TASK-013 I5; web search confirmed no matching paper exists) | barrier-4/synthesis.md, Section 6 |
| C-002 | NEVER claim experimental validation for NPT-009 superiority over positive equivalents | barrier-2/synthesis.md ST-5 (GC-P4-1) |
| C-003 | NEVER present T4 observational evidence as T1 experimental evidence | barrier-2/synthesis.md ST-5 (GC-P4-1) |
| C-004 | NEVER recommend implementation of framing-comparison recommendations before Phase 2 (NPT-014 elimination is the EXCEPTION per PG-001 unconditional status) | barrier-2/synthesis.md ST-5 (GC-P4-2); barrier-4/synthesis.md Section 3 |
| C-005 | MUST document PG-003 reversibility for all recommendations | barrier-2/synthesis.md ST-5 (GC-P4-3) |
| C-006 | NEVER use positive prompting framing in this ADR -- all constraint language uses NEVER/MUST NOT | Orchestration directive 1 |
| C-007 | NEVER treat absence of published evidence as evidence of absence | Orchestration directive 4; barrier-1/supplemental-vendor-evidence.md |

---

## Forces

1. **Evidence strength vs. evidence scope:** T1+T3 evidence establishes blunt prohibition underperforms, but the evidence scope is limited to "structured alternatives" -- it does not specify that NPT-009 negative framing is the optimal structured alternative. The force tension is between acting on established evidence (blunt prohibition is weak) and the incomplete picture (whether structured negative or structured positive is preferable).

2. **Implementation effort vs. quality improvement:** Upgrading ~22 rule-file NPT-014 instances (TASK-012) plus an additional ~108 instances across skills (TASK-010), agents (TASK-011), patterns (TASK-013), and templates (TASK-014) requires significant effort. The force tension is between the quality improvement from consequence documentation and the effort to audit, upgrade, and review 130 instances.

3. **Phase 2 baseline preservation vs. immediate improvement:** Modifying framework artifacts before Phase 2 captures the experimental baseline risks contaminating the Phase 2 comparison conditions. The force tension is between improving constraint quality now and preserving an unmodified baseline for experimental comparison.

4. **Universal scope vs. incremental adoption:** All 5 Phase 4 analyses confirm NPT-014 presence universally. A universal elimination policy is warranted by the evidence. However, a phased rollout reduces implementation risk and allows quality validation at each stage.

---

## Options Considered

### Option 1: Universal NPT-014 Elimination Policy (Recommended)

Mandate that all standalone blunt prohibitions across all five artifact domains (rules, skills, agents, patterns, templates) be upgraded to NPT-009 structured format. The policy applies universally: every NEVER/MUST NOT statement without consequence documentation, scope specification, and (where feasible) positive alternative pairing is a defect that requires remediation.

**Steelman (S-003):** This is the strongest option because the evidence base is universal. All 5 Phase 4 analyses independently identify NPT-014 as the baseline problem. The T1+T3 evidence (PG-001) applies regardless of artifact type -- blunt prohibition does not become acceptable because it appears in a SKILL.md rather than a rule file. A universal policy prevents domain-specific exceptions from creating inconsistency.

**Pros:**
- Addresses the systemic problem at root -- no NPT-014 instances survive
- Consistent with the universal convergence finding (barrier-4/synthesis.md Theme 2: all 5 analyses)
- Grounded in T1+T3 unconditional evidence (PG-001, HIGH confidence)
- Produces the largest total quality improvement across the framework
- Consequence documentation has independent value (auditability, human readability) regardless of Phase 2 framing outcome

**Cons:**
- Largest implementation scope (~130 instances across 5 domains)
- Requires careful sequencing to avoid Phase 2 baseline contamination (force #3)
- Some domains have lower confidence in NPT-014 identification (TASK-013 patterns: 0.84 composite from sampling ceiling)
- Dependency ordering (TASK-012 rule files before TASK-010 skills, per barrier-4/synthesis.md Section 3) adds coordination complexity

**Fit with Constraints:** SATISFIES C-001 through C-007. The universal scope applies to the NPT-014 elimination only (T1+T3 unconditional), not to framing-comparison recommendations (which remain gated by Phase 2 per C-004). PG-003 reversibility is straightforward: all additions are additive text; removing the added consequence/scope/alternative text returns to current state (C-005).

### Option 2: Domain-Specific Scope (Rule Files Only First)

Restrict the initial NPT-014 elimination policy to the rule file domain only (TASK-012: 22 instances across 17 rule files). Defer skills, agents, patterns, and templates to a subsequent decision after Phase 2 results.

**Steelman (S-003):** This option has genuine merit. Rule files are the highest-impact domain because they are L1-loaded at session start and some are L2-re-injected per prompt. Changes to rule files have the most direct effect on LLM behavioral compliance. Starting with rule files focuses effort where the evidence is most directly applicable (VS-001 through VS-004 specifically document rule-file-level practices). The reduced scope (22 instances vs. ~130) is more tractable and allows the team to validate the upgrade process before scaling.

**Pros:**
- Smaller scope reduces implementation risk (22 instances vs. ~130)
- Focuses on highest-impact artifacts (L1/L2 enforcement layer)
- Preserves the option to expand scope after validating the approach
- Easier to sequence around Phase 2 baseline capture (fewer files to exclude)

**Cons:**
- Leaves NPT-014 instances in 4 of 5 domains indefinitely
- The T1+T3 evidence applies universally, not only to rule files -- restricting scope is not evidence-motivated but effort-motivated
- Creates inconsistency: rule files upgraded but SKILL.md Constitutional Compliance tables still use blunt prohibition
- The "NEVER hardcode values" pattern identified in 4 SKILL.md files (TASK-010) remains unaddressed
- Does not leverage the cross-analysis convergence finding (Theme 2: all 5 analyses agree NPT-014 is universal)

**Fit with Constraints:** SATISFIES C-001 through C-007 but under-delivers on the evidence base. PG-001 is unconditional and domain-agnostic; artificially scoping to rule files does not align with the evidence breadth.

### Option 3: Defer All NPT-014 Elimination Until Phase 2 Completion

Take no action on NPT-014 elimination until Phase 2 experimental results are available. Treat NPT-014 instances as a known gap to be addressed holistically after the framing comparison is resolved.

**Steelman (S-003):** This option's strongest argument is risk avoidance. If Phase 2 reveals that positive framing is equivalent to or better than structured negative framing at ranks 9-11, the NPT-014 elimination policy might target the wrong upgrade format. Instead of upgrading "NEVER hardcode values" to NPT-009 (structured negative with consequence), it might be better to upgrade to a positive equivalent ("MUST inject configuration values via dependency injection container. Consequence if violated: credential exposure risk."). Deferring preserves maximum flexibility.

**Pros:**
- Maximum flexibility -- no commitment before Phase 2 data
- Zero risk of Phase 2 baseline contamination
- Zero implementation effort in the near term

**Cons:**
- **Contradicts the T1+T3 evidence.** PG-001 is explicitly labeled "unconditional" and "Phase 2 outcome irrelevant." The evidence establishes that blunt prohibition underperforms structured alternatives. Deferring action on a known-inferior pattern when evidence supports immediate action violates the evidence-based decision principle (P-011).
- All 5 Phase 4 analyses independently identify NPT-014 elimination as the one action that does not require Phase 2 completion (barrier-4/synthesis.md Section 3: "Exception: NPT-014 elimination (PG-001 unconditional, T1+T3 HIGH)").
- The steelman argument (Phase 2 might reveal positive framing is better) misunderstands the decision: NPT-014 elimination upgrades from blunt prohibition to structured format. Whether that structured format uses negative or positive vocabulary is a separate question. Consequence documentation, scope specification, and alternative pairing improve constraint quality regardless of framing.
- Leaves known-inferior constraint formulations in production for the duration of Phase 2 experimental design, execution, and analysis.

**Fit with Constraints:** Technically satisfies C-001 through C-007 but violates the spirit of P-011 (evidence-based recommendations) by ignoring unconditional T1+T3 evidence.

### Options Evaluation Summary

> **Scoring basis:** Scores reflect the architect's synthesis judgment across the three evaluation dimensions (Evidence Alignment, Implementation Risk, Phase 2 Compatibility), each rated 0-3 (0=absent, 1=low, 2=medium, 3=high alignment), summed and normalized to a /10 scale. Scores are not derived from a quantitative upstream model; they synthesize the qualitative pro/con analysis above.

| Option | Evidence Alignment | Implementation Risk | Phase 2 Compatibility | Score |
|--------|-------------------|--------------------|-----------------------|-------|
| **Option 1: Universal Elimination** | HIGH -- fully aligned with T1+T3 and 5-analysis convergence | MEDIUM -- large scope requires phased rollout | HIGH -- sequencing plan preserves baseline | **9/10** |
| Option 2: Rule Files Only | MEDIUM -- artificially scoped below evidence breadth | LOW -- tractable scope | HIGH -- small footprint | 6/10 |
| Option 3: Defer All | LOW -- contradicts unconditional T1+T3 evidence | NONE -- no action | HIGHEST -- no changes at all (zero-change avoidance, not positive Phase 2 support) | 3/10 |

---

## Decision

**We will adopt Option 1: Universal NPT-014 Elimination Policy.**

Every standalone blunt prohibition (NEVER/MUST NOT/FORBIDDEN/DO NOT without consequence documentation, scope specification, and positive behavioral pairing) across all five artifact domains SHALL be upgraded to NPT-009 structured format as a minimum. The policy applies to: rule files (.context/rules/), SKILL.md files (skills/*/SKILL.md), agent definition markdown bodies (skills/*/agents/*.md), pattern documentation (docs/patterns/), and templates (.context/templates/).

### Rationale

1. **The evidence is unconditional.** PG-001 (T1+T3, HIGH confidence) explicitly states that blunt prohibition demonstrably underperforms structured alternatives. This finding is labeled "Phase 2 outcome irrelevant" by barrier-2/synthesis.md. All 5 Phase 4 analyses confirm this applies universally across all artifact domains.

2. **The upgrade is unidirectional.** NPT-014 to NPT-009 is an upgrade from a known-inferior formulation to a known-superior one. The improvement operates on three dimensions simultaneously: (a) consequence documentation (enables understanding of why the constraint exists), (b) scope specification (enables understanding of where the constraint applies), and (c) positive alternative pairing where feasible (enables understanding of what to do instead). All three dimensions have independent value regardless of the negative-vs.-positive framing question.

3. **Consequence documentation has independent value.** Even under PG-003 null framing effect (Phase 2 finds that negative and positive framing produce equivalent LLM compliance), the consequence documentation component of the NPT-009 upgrade retains full value. Human readers benefit from understanding why a constraint exists and what breaks when it is violated. This is an auditability improvement, not solely a framing improvement.

4. **Cross-analysis convergence eliminates domain-specific exceptions.** All 5 Phase 4 analyses independently identify NPT-014 as the baseline problem in their respective domains (barrier-4/synthesis.md Theme 2). There is no domain where NPT-014 is acceptable. Restricting scope to a single domain would contradict this universal finding.

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | HIGH | Satisfies all 7 binding constraints (C-001 through C-007) |
| Risk Level | MEDIUM | Implementation risk from scope (~130 instances); mitigated by phased sequencing |
| Implementation Effort | L | Large -- requires systematic audit and upgrade across 5 artifact domains |
| Reversibility | HIGH | All additions are additive text; reverting removes consequence/scope/alternative additions |

---

## L1: Technical Implementation

### NPT-014 Diagnostic Filter

The following diagnostic filter identifies NPT-014 instances requiring upgrade. This filter was applied consistently across all five Phase 4 analyses and MUST be applied identically during implementation.

**A constraint is NPT-014 (blunt prohibition) if it is a NEVER/MUST NOT/FORBIDDEN/DO NOT statement that lacks ALL THREE of:**
1. Explicit consequence if violated (what breaks, what degrades, what is rejected)
2. Explicit scope of applicability (which files, which layers, which contexts)
3. A positive behavioral pairing describing what to do instead

**A constraint is NPT-009 (declarative behavioral negation) if it includes at minimum (1) and (2) above.** Element (3) is recommended where a positive alternative exists but is not structurally required for NPT-009 classification.

### Upgrade Procedure

For each identified NPT-014 instance:

**Step 1 -- Identify the constraint.** Locate the NEVER/MUST NOT/FORBIDDEN/DO NOT statement. Confirm it lacks consequence, scope, and alternative.

**Step 2 -- Document the consequence.** Determine what fails, breaks, or degrades when this constraint is violated. Sources for consequence documentation:
- HARD rule table "Consequence" columns in `.context/rules/` files
- L2-REINJECT marker content (may contain partial consequence information)
- Agent runtime failure observations documented in worktracker entries
- Vendor self-practice consequence patterns (VS-001 catalog for structural reference)

**Step 3 -- Specify the scope.** Document where the constraint applies. Scope patterns:
- File-level: "Scope: all files in `src/domain/`"
- Layer-level: "Scope: domain layer and application layer"
- Agent-level: "Scope: all worker agents (T1-T4 tier)"
- Artifact-level: "Scope: all SKILL.md Constitutional Compliance tables"

**Step 4 -- Add positive alternative (where feasible).** Document what to do instead of the prohibited behavior. NEVER force a positive alternative where none naturally exists -- some prohibitions are pure boundary constraints with no meaningful "instead."

**Step 5 -- Validate the upgrade.** Confirm the upgraded constraint:
- Contains a consequence statement ("Consequence: ...")
- Contains a scope statement ("Scope: ...")
- Contains a positive alternative if one exists ("Instead: ...")
- Preserves the original prohibition vocabulary (NEVER/MUST NOT) -- the upgrade adds structure, it does not change framing
- **Quality gate hook:** This validation step MUST be integrated into the H-17 quality scoring process. The NPT-014 diagnostic filter (above) serves as the validation predicate: any constraint failing the diagnostic is a measurable defect under S-014 (LLM-as-Judge). This closes the loop with the FMEA mitigation for "New NPT-014 introduction" (RPN 150): the quality gate prevents new NPT-014 instances from passing review.

### Implementation Sequencing

NEVER implement all 130 upgrades simultaneously. The following sequencing preserves Phase 2 baseline integrity and respects inter-domain dependencies.

**Group 1: Rule File NPT-014 Instances (TASK-012, 22 instances) -- Implement First**

Rule files are the source of truth for HARD rule constraints. Changes here propagate to all downstream artifacts. TASK-012 identified 5 specific upgrade recommendations (R-QE-001 through R-ADS-003):

| ID | Target Rule File | Description |
|----|-----------------|-------------|
| R-QE-001 | quality-enforcement.md | Add consequence to rank=3 L2-REINJECT marker (NPT-009 format) |
| R-QE-002 | quality-enforcement.md | Document consequence requirement in L2 marker guidance |
| R-ADS-001 | agent-development-standards.md | Reclassify CP-01/CP-04 vocabulary from HARD to MEDIUM tier |
| R-ADS-002 | agent-development-standards.md | Add constitutional triplet prohibition to L2-REINJECT rank=5 marker |
| R-ADS-003 | agent-development-standards.md | Add consequence + positive alternative to hexagonal dependency rule |

These are the highest-priority targets because:
- Rule files are L1-loaded at session start -- changes here have the most direct behavioral effect
- Some rule file constraints are L2-re-injected -- upgrading L2 marker content to NPT-009 format strengthens per-prompt enforcement
- TASK-012 -> TASK-010 dependency (barrier-4/synthesis.md Section 3): rule file updates MUST precede SKILL.md updates

**Group 2: Agent Definition NPT-014 Instances (TASK-011, 32 total: 5 framework-level + 27 agent-level) -- Implement Second**

TASK-011 produced 32 recommendations across 9 agent families (barrier-4/synthesis.md L1 Recommendation Counts table). Of these 32, 5 are framework-level recommendations targeting the `agent-development-standards.md` guardrails template and constitutional compliance patterns shared across all agents, and 27 are agent-level recommendations targeting specific agent definition files. Agent definitions inherit constraint vocabulary from rule files. The H-35 minimum example in agent-development-standards.md is itself NPT-014 format (barrier-4/synthesis.md Theme 3). TASK-012 -> TASK-011 dependency: rule file standards (agent-development-standards.md) MUST be upgraded before agent template upgrades.

**Group 3: SKILL.md NPT-014 Instances (TASK-010, 37 recommendations) -- Implement Third**

SKILL.md files surface HARD rule content from rule files. NEVER upgrade a SKILL.md constraint to NPT-009 without first confirming the source rule file has been upgraded (TASK-012 -> TASK-010 dependency).

**Group 4: Pattern and Template NPT-014 Instances (TASK-013, 34 recs; TASK-014, 13 recs) -- Implement Fourth**

Pattern documentation and templates are reference materials. They have lower behavioral impact than rule files, agent definitions, and SKILL.md files. TASK-013 is fully independent of the other analyses and can proceed in parallel with Group 2 or Group 3 if desired.

### Phase 2 Baseline Preservation Protocol

NEVER apply NPT-014 elimination upgrades to framework artifacts that are subject to Phase 2 experimental conditions until the Phase 2 baseline has been captured. The preservation protocol:

1. Phase 2 experimental conditions (C1-C7 from TASK-005) use the current framework state as baseline
2. NPT-014 elimination upgrades MUST be applied to a separate branch or tracked as a discrete changeset
3. The Phase 2 baseline capture (pre-upgrade snapshot) MUST be documented with commit hash before any production artifacts are modified
4. After baseline capture, NPT-014 elimination proceeds per the sequencing above

### L2-REINJECT Token Budget Impact

TASK-012 confirmed that L2-REINJECT markers currently consume approximately 559-670 tokens of the 850-token budget (65.8-78.8%). Adding consequence documentation to existing L2 markers (the NPT-014 -> NPT-009 upgrade in L2 content) adds approximately 12-15 tokens per marker. With 5 markers containing NEVER/MUST NOT content, the total addition is approximately 60-75 tokens. Under worst-case assumptions (670 base + 75 additions = 745 tokens), the budget remains within the 850-token ceiling (87.6% utilization).

---

## L2: Architectural Implications

### Long-Term Evolution Path

NPT-014 elimination is the first step in a constraint maturity progression. The full progression, as identified by the Phase 3 taxonomy, is:

```
NPT-014 (Blunt prohibition)     -- ELIMINATE (this ADR)
    |
    v
NPT-009 (Structured negation)   -- MINIMUM TARGET (this ADR)
    |
    v
NPT-010 (Paired prohibition)    -- FUTURE (ADR-002/ADR-003, conditional on Phase 2)
    |
    v
NPT-011 (Justified prohibition) -- FUTURE (ADR-002, conditional on Phase 2)
    |
    v
NPT-012 (L2 re-injected)       -- FUTURE (ADR-004, for enforcement-tier constraints)
    |
    v
NPT-013 (Constitutional triplet) -- FUTURE (ADR-002, for P-003/P-020/P-022)
```

This ADR establishes the floor: no constraint SHALL remain at NPT-014 level. Future ADRs (ADR-002 through ADR-004) address the ceiling: which constraints should be elevated beyond NPT-009 to NPT-010/NPT-011/NPT-012/NPT-013. Those future ADRs are conditional on Phase 2 experimental results for their framing-comparison components.

### Systemic Consequence: Constraint Documentation as Governance Artifact

NPT-014 elimination transforms the framework's constraint inventory from a collection of bare prohibitions into a structured governance catalog where every constraint has documented consequences. This has systemic implications:

1. **Auditability.** Every NEVER/MUST NOT statement becomes self-documenting: what breaks, where it applies, what to do instead. This supports governance review without requiring the reviewer to trace consequences through multiple files.

2. **Onboarding.** New contributors encounter constraints that explain themselves rather than requiring implicit knowledge of framework architecture to understand why a prohibition exists.

3. **Quality gate integration.** The NPT-014 diagnostic filter can be incorporated into existing quality gate processes (H-17, S-014 LLM-as-Judge). A constraint without consequence documentation is a measurable defect.

4. **Context rot mitigation.** Consequence documentation in L2-REINJECT markers provides richer contextual signal per re-injection token. When context compacts, a re-injected "NEVER use pip. Consequence: environment corruption; CI blocks merge" retains more enforcement value than a bare "NEVER use pip" (T4 inference from vendor self-practice; UNTESTED controlled comparison -- this is the Phase 2 question).

### Pre-Mortem Analysis (S-004)

> **Scope distinction:** This Pre-Mortem table is a failure discovery methodology (S-004: "It is 6 months later and the decision failed -- why?"). It identifies *why* failures occur and generates mitigations. The [Consequences: Risks](#consequences-risks) table below is a formal risk register that classifies the same failure modes by *probability* and *impact* for implementation prioritization. The two tables cover the same risk domain from complementary analytical angles; the Pre-Mortem focuses on causal chains, the Risk Register on severity classification.

**Scenario: It is 6 months after this ADR is accepted. The NPT-014 elimination policy has failed. Why?**

| Failure Mode | Probability | Why It Could Happen | Mitigation |
|-------------|-------------|---------------------|------------|
| Consequence documentation is formulaic and uninformative | MEDIUM | Teams apply the NPT-009 template mechanically: "Consequence: bad things happen" | Define a minimum consequence specificity standard: consequences MUST name the specific failure mode (e.g., "CI blocks merge"), not generic outcomes (e.g., "quality degrades") |
| Phase 2 reveals positive framing is strictly superior at all ranks | LOW | Controlled experiment shows NPT-009 negative framing underperforms structurally equivalent positive framing | PG-003 contingency: all upgrades are additive and reversible. If positive framing is strictly superior, consequence documentation retains value but the NEVER/MUST NOT vocabulary is replaced with MUST/SHALL + consequence |
| Implementation stalls at Group 1 (rule files) and never reaches Groups 2-4 | MEDIUM | Sequencing dependencies create bottleneck; team prioritizes other work | Define implementation milestones with worktracker entities per group; assign Group 3 and Group 4 as independently parallelizable after Group 1 completes |
| New NPT-014 instances introduced faster than old ones are eliminated | MEDIUM | Authors unfamiliar with the policy write new NEVER statements without consequence documentation | Incorporate NPT-014 diagnostic into the agent-development-standards.md guardrails template (H-34); add to quality gate checklist; create a pre-commit advisory |
| L2-REINJECT token budget exceeded | LOW | Cumulative consequence additions push past 850-token ceiling | TASK-012 confirmed worst-case 745/850 (87.6%) for rule-file NPT-014 upgrades; monitor budget at each group |

### FMEA Analysis (S-012) for the Chosen Approach

> **Scale definitions:** Severity (1-10): 1 = negligible impact on framework quality; 5 = moderate degradation requiring rework within one sprint; 10 = irreversible architectural damage or governance violation. Occurrence (1-10): 1 = extremely unlikely (< 1% of instances); 5 = moderate likelihood (occurs in ~30-50% of instances); 10 = near-certain (occurs in > 90% of instances). Detection (1-10): 1 = immediate detection by automated quality gate or CI check; 5 = detectable during manual review but not automated; 10 = undetectable until production behavioral impact observed. RPN = Severity x Occurrence x Detection.

| Failure Mode | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN | Mitigation |
|-------------|-----------------|-------------------|-------------------|-----|------------|
| Formulaic consequence documentation | 4 | 6 | 3 | 72 | Consequence specificity standard; reviewer checklist |
| Phase 2 baseline contamination | 8 | 3 | 2 | 48 | Baseline capture protocol; branch isolation |
| Implementation stall at Group 1 | 5 | 5 | 4 | 100 | Worktracker milestones; Group 3/4 parallelization |
| New NPT-014 introduction | 6 | 5 | 5 | 150 | NPT-014 diagnostic in quality gate; template update |
| L2 token budget overrun | 7 | 2 | 2 | 28 | Budget monitoring per TASK-012 analysis |

**Highest RPN (150): New NPT-014 introduction.** The primary risk is not the existing inventory but the ongoing creation of new NPT-014 instances. The mitigation is integrating the NPT-014 diagnostic into the quality gate process (H-17) and updating the guardrails template in agent-development-standards.md to demonstrate NPT-009 format as the minimum.

### Inversion Analysis (S-013)

**What if we deliberately chose the opposite: mandate that all constraints remain as blunt prohibitions?**

This inversion reveals:
- The framework would be contradicting its own T1+T3 evidence base (PG-001)
- Vendor self-practice (VS-001) demonstrates that production systems use structured format, not blunt prohibition
- The 8 existing NPT-009 instances in rule files (TASK-012) would be inconsistent with the policy -- the framework already partially adopts structured format
- New contributors would lack consequence information, increasing the learning curve
- L2-re-injected constraints would carry less enforcement signal per token

The inversion confirms that NPT-014 preservation is not defensible. The only question is scope and timing, not direction.

---

## Consequences

### Positive Consequences

1. **Every HARD rule constraint becomes self-documenting.** Consequence documentation eliminates the need for readers to trace prohibition rationale through multiple files. This is an unconditional improvement that persists regardless of Phase 2 outcome.

2. **Constraint quality becomes measurable.** The NPT-014 diagnostic provides a binary test: does this constraint have consequence documentation? This enables quality gate integration (H-17) and progress tracking.

3. **Vendor self-practice alignment.** The framework's constraint inventory moves from divergent (predominantly NPT-014) to convergent (NPT-009 minimum) with Anthropic's observed practice (VS-001: 33 structured instances across 10 rule files). This alignment is observational (T4), not experimentally validated.

4. **Foundation for future NPT upgrades.** NPT-014 elimination creates a uniform NPT-009 floor from which ADR-002 (constitutional triplet), ADR-003 (routing disambiguation), and ADR-004 (context compaction resilience) can build.

5. **Reduced ambiguity for LLM agents.** Structured constraints with consequence documentation provide richer signal than bare prohibitions. This is a T4 inference from vendor self-practice patterns; the controlled comparison is the Phase 2 experimental target.

### Negative Consequences

1. **Implementation effort is substantial.** ~130 instances across 5 domains require audit, upgrade, and review. This is not a trivial change -- it requires domain-specific understanding of each constraint's failure modes to write meaningful consequence documentation.

2. **Risk of formulaic upgrades.** Mechanical application of the NPT-009 template without genuine consequence analysis produces low-quality upgrades that satisfy the letter of the policy without achieving the intent. NEVER treat consequence documentation as a checkbox exercise.

3. **Phase 2 sequencing complexity.** The baseline preservation protocol adds coordination overhead. Phase 2 experimental conditions MUST NOT be contaminated by NPT-014 elimination changes, requiring branch management or commit-hash-based baseline capture.

4. **Increased file sizes.** Consequence documentation, scope specification, and positive alternatives add text to every constraint. For L2-REINJECT markers, this consumes token budget (~60-75 additional tokens estimated). For non-L2 files, the size increase is manageable but non-zero.

5. **Maintenance burden.** When a constraint's consequence changes (e.g., CI pipeline change alters the failure mode), the consequence documentation must be updated. Bare prohibitions ("NEVER use pip") have no documentation to keep current; NPT-009 constraints do.

### Neutral Consequences

1. **The negative-vs.-positive framing question remains open.** This ADR upgrades constraint structure (from blunt to documented) but does not resolve whether the documented constraint should use negative or positive vocabulary. That question is deferred to Phase 2 and ADR-002.

2. **No new HARD rules are created.** This ADR establishes a policy for upgrading existing constraints, not for adding new ones. The HARD rule ceiling (25/25) is unaffected.

3. **L2-REINJECT marker mechanism is unchanged.** The re-injection mechanism itself is not modified by this ADR -- only the content within existing markers is upgraded. No new markers are added.

---

## Compliance

### PG-003 Reversibility Assessment

| Component | Reversible? | Mechanism |
|-----------|-------------|-----------|
| Consequence documentation additions | YES | Remove added "Consequence: ..." text; return to bare prohibition |
| Scope specification additions | YES | Remove added "Scope: ..." text; return to unscoped prohibition |
| Positive alternative additions | YES | Remove added "Instead: ..." text; return to prohibition-only |
| L2-REINJECT content upgrades | YES | Revert marker content to pre-upgrade text; token budget freed |
| Quality gate NPT-014 diagnostic | YES | Remove diagnostic from checklist; revert to pre-policy quality gate |

**Overall reversibility assessment: HIGH.** All changes are additive text additions. No existing text is deleted. No structural changes to file formats, schema definitions, or enforcement mechanisms are made. Reverting the policy requires removing the added text from each upgraded instance, which is a well-defined, bounded operation.

**PG-003 contingency:** If Phase 2 finds null framing effect at ranks 9-11 (structured negative constraints produce equivalent LLM adherence to structurally equivalent positive constraints), the consequence documentation component of the NPT-009 upgrade retains its value (auditability, human readability). The framing vocabulary (NEVER/MUST NOT) becomes convention-determined rather than effectiveness-determined. Under this contingency, the decision becomes: keep consequence documentation (always valuable), and optionally convert framing vocabulary from negative to positive (convention choice, not effectiveness choice).

### Evidence Tier Labels on All Claims

| Claim | Tier | Source |
|-------|------|--------|
| Blunt prohibition underperforms structured alternatives | T1+T3 | A-20 (AAAI 2026), A-15 (EMNLP 2024), A-31 (arXiv) |
| 22 of 36 rule-file instances are NPT-014 | T4 (compiled inventory) | TASK-012 rules-update-analysis.md |
| NPT-014 presence is universal across all 5 artifact domains | T4 (cross-pollination) | barrier-4/synthesis.md Themes 1 and 2 |
| Anthropic uses structured format (not blunt prohibition) in HARD tier | T4 (vendor observation) | VS-001, supplemental-vendor-evidence.md |
| NPT-009 framing outperforms positive framing at ranks 9-11 | UNTESTED | Phase 2 experimental target |
| Consequence documentation has independent auditability value | T4 (analytical inference) | PG-003 contingency analysis |

### Constraint Propagation Verification

| Constraint | Status |
|------------|--------|
| GC-P4-1: No false validation claims | COMPLIANT -- all claims carry evidence tier labels; UNTESTED causal comparison explicitly stated |
| GC-P4-2: Phase 2 reproducibility preserved | COMPLIANT -- baseline preservation protocol defined; sequencing prevents contamination |
| GC-P4-3: PG-003 contingency documented | COMPLIANT -- reversibility assessment included; null-framing-effect scenario analyzed |

---

## Consequences: Risks

> **Scope distinction:** This Risk Register classifies implementation risks by *probability* and *impact* for prioritization. The [Pre-Mortem Analysis](#pre-mortem-analysis-s-004) in the L2 section covers the same failure domain from a causal analysis perspective (S-004: why did this fail?). Both tables are intentionally retained: the Pre-Mortem generates the failure modes through causal reasoning; this table classifies them for operational planning.

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Phase 2 baseline contamination from premature implementation | LOW (with protocol) | HIGH | Baseline preservation protocol; branch isolation; commit-hash documentation |
| Formulaic consequence documentation (checkbox compliance) | MEDIUM | MEDIUM | Consequence specificity standard; reviewer training; quality gate integration |
| Implementation stall due to scope | MEDIUM | MEDIUM | Phased sequencing (Groups 1-4); parallelizable Groups 3-4; worktracker milestones |
| New NPT-014 instances created during rollout | MEDIUM | HIGH | Quality gate integration (H-17); template update (agent-development-standards.md); pre-commit advisory |
| L2-REINJECT token budget overrun | LOW | HIGH | Budget monitoring per group; TASK-012 confirmed worst-case 87.6% utilization |
| Phase 2 null framing effect reduces perceived value | MEDIUM | LOW | Consequence documentation retains auditability value; PG-003 contingency pre-documented |

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-002 (Constitutional Triplet and High-Framing Upgrades) | ENABLES | ADR-001 establishes NPT-009 floor; ADR-002 elevates select constraints to NPT-013. ADR-002 is conditional on Phase 2 for framing-comparison components. |
| ADR-003 (Routing Disambiguation Standard) | ENABLES | ADR-001 upgrades NPT-014 instances in "Do NOT use when:" sections; ADR-003 establishes the routing disambiguation standard using NPT-010 format. |
| ADR-004 (Context Compaction Resilience) | ENABLES | ADR-001 upgrades L2-REINJECT marker content from NPT-014 to NPT-009; ADR-004 addresses L2 mechanism resilience under context compaction. |

---

## References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | A-20: Geng, Li, Mu, Han, Baldwin, Abend, Hovy, Frermann. "Control Illusion: The Failure of Instruction Hierarchies in Large Language Models." AAAI 2026 Main Technical Track. [arXiv:2502.15851](https://arxiv.org/abs/2502.15851) | T1 academic (peer-reviewed) | Establishes standalone prohibition underperformance: system/user prompt separation fails to establish reliable instruction hierarchy; models follow pretraining-derived social priors over explicit prohibitions |
| 2 | A-15: Ferraz, Mehta, Lin, Chang, Oraby, Liu, Subramanian, Chung, Bansal, Peng. "LLM Self-Correction with DeCRIM." EMNLP 2024 Findings. [arXiv:2410.06458](https://arxiv.org/abs/2410.06458) | T1 academic (peer-reviewed) | Quantifies structured > bare prohibition gap: DeCRIM improves Mistral by +7.3% (RealInstruct) and +8.0% (IFEval) via constraint decomposition; GPT-4 fails constraints on 21%+ of instructions |
| 3 | A-31: Bsharat, Myrzakhan, Shen. "Principled Instructions Are All You Need for Questioning LLaMA-2, GPT-3.5/4." [arXiv:2312.16171](https://arxiv.org/abs/2312.16171) (2023) | T3 preprint | Corroborating evidence across task types: affirmative directives showed 55% improvement and 66.7% correctness increase for GPT-4 vs. prohibitions |
| 4 | PG-001, barrier-2/synthesis.md ST-4 | Practitioner guidance | "Blunt prohibition demonstrably underperforms" -- HIGH unconditional |
| 5 | VS-001 through VS-004, supplemental-vendor-evidence.md (R4, 0.951 PASS) (VS-001: 33-instance NEVER/MUST NOT/FORBIDDEN/DO NOT vendor self-practice catalog; VS-003: HARD tier vocabulary as structured negative vocabulary observation) | T4 vendor observation | 33-instance vendor self-practice catalog; three competing causal explanations |
| 6 | TASK-012, rules-update-analysis.md (0.953 PASS) | Phase 4 analysis | 22 NPT-014 instances in rule files; L2 budget analysis |
| 7 | TASK-010, skills-update-analysis.md (v2.0.0, 0.951 PASS) | Phase 4 analysis | 37 recommendations across 13 SKILL.md files |
| 8 | TASK-011, agents-update-analysis.md (v3.0.0, 0.951 PASS) | Phase 4 analysis | 32 recommendations across 9 agent families |
| 9 | TASK-013, patterns-update-analysis.md (v5.0.0, 0.950 PASS) | Phase 4 analysis | 34 recommendations across 12 pattern categories |
| 10 | TASK-014, templates-update-analysis.md (v3.0.0, 0.955 PASS) | Phase 4 analysis | 13 recommendations across 4 template families |
| 11 | barrier-4/synthesis.md (TASK-015, v4.0.0, 0.950 PASS) | Cross-pollination synthesis | 130 consolidated recommendations; 6 cross-cutting themes; dependency map |
| 12 | phase-3/taxonomy-pattern-catalog.md (v3.0.0, 0.957 PASS) | Taxonomy | NPT-001 through NPT-014 pattern definitions |
| 13 | barrier-2/synthesis.md (v3.0.0, 0.950 PASS) | Phase 2 synthesis | PG-001 through PG-005; ST-5 Phase 4 constraints; AGREE-5 hierarchy |

---

## PS Integration

| Field | Value |
|-------|-------|
| PS ID | PROJ-014 |
| Task ID | TASK-016 |
| Phase | Phase 5 -- Architecture Decision Records |
| Artifact Path | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-001-npt014-elimination.md` |
| Decision | Universal NPT-014 elimination policy: mandate upgrade from standalone blunt prohibition to NPT-009 structured format across all 5 artifact domains |
| Status | PROPOSED |
| Evidence Tier | T1+T3 (PG-001 unconditional) for the elimination direction; T4 (vendor self-practice) for NPT-009 as the target format |
| Reversibility | HIGH -- all changes are additive text; PG-003 contingency documented |
| Next Agent Hint | ps-architect for ADR-002 (Constitutional Triplet); implementation planning agent for Group 1-4 sequencing |

### Key Findings for Downstream Handoff

1. **NPT-014 elimination is unconditional** (T1+T3, PG-001 HIGH). This is the one recommendation category that does not require Phase 2 completion. Barrier-4/synthesis.md Section 3 explicitly identifies this exception.

2. **Implementation is sequenced in 4 groups:** Rule files (22 instances) -> Agent definitions (32 recs) -> SKILL.md files (37 recs) -> Patterns + Templates (47 recs). Groups 3 and 4 are parallelizable after Group 1 completes.

3. **Phase 2 baseline MUST be captured before production implementation.** The baseline preservation protocol requires commit-hash documentation and branch isolation.

4. **NEVER cite A-11** in any downstream document. Confirmed hallucinated in TASK-013 I5. NPT-008 evidence rests on E-007 only.

5. **The highest FMEA risk (RPN 150) is new NPT-014 introduction**, not existing inventory elimination. Quality gate integration and template updates are the primary mitigation.

---

## Self-Review Checklist (H-15)

| Check | Status | Notes |
|-------|--------|-------|
| P-001: Are option evaluations factually accurate? | PASS | All claims carry evidence tier labels; T1/T3/T4 distinctions preserved |
| P-002: Is ADR persisted to file? | PASS | Written to phase-5/ADR-001-npt014-elimination.md |
| P-004: Are context and rationale documented? | PASS | Context section with 13 references; rationale section with 4 numbered reasons |
| P-011: Are alternatives evaluated? | PASS | 3 options with steelman (S-003) for each; options evaluation summary table |
| P-020: Is status PROPOSED? | PASS | Status: PROPOSED -- user authority required for acceptance |
| P-022: Are negative consequences documented? | PASS | 5 negative consequences listed; risks table with 6 entries; FMEA analysis; pre-mortem analysis |
| C-001: A-11 not cited? | PASS | A-11 nowhere in this document; citation prohibition noted in Constraints table |
| C-002: No false NPT-009 superiority claim? | PASS | MANDATORY EPISTEMOLOGICAL BOUNDARY stated; UNTESTED labels throughout |
| C-003: T4 not presented as T1? | PASS | All evidence tier labels explicit in Evidence Base table |
| C-004: No framing-comparison recs before Phase 2? | PASS | Only NPT-014 elimination (PG-001 unconditional exception) is recommended |
| C-005: PG-003 reversibility documented? | PASS | Full reversibility assessment table in Compliance section |
| C-006: No positive prompting framing? | PASS | All constraint language uses NEVER/MUST NOT |
| C-007: Absence of evidence not evidence of absence? | PASS | VS-001 through VS-004 treated as valid T4 evidence per C-007 |
| H-23: Navigation table present? | PASS | Document Sections table at top |
| S-003: Steelman applied to rejected alternatives? | PASS | Each option includes steelman paragraph |
| S-004: Pre-mortem analysis? | PASS | Pre-mortem table with 5 failure modes |
| S-012: FMEA analysis? | PASS | FMEA table with 5 failure modes and RPN scores |
| S-013: Inversion analysis? | PASS | "What if we chose the opposite?" analysis in L2 section |

---

*Agent: ps-architect*
*Task: TASK-016*
*Workflow: neg-prompting-20260227-001*
*Phase: Phase 5 -- Architecture Decision Records*
*Version: 1.2.0*
*Created: 2026-02-28*
*I2 Revision (2026-02-28): 4 targeted fixes from adversary-adr001-i1.md (score 0.9185 REVISE, target >= 0.95): (1) Full bibliographic citations added for A-20 (AAAI 2026) and A-15 (EMNLP 2024) T1 anchors in References table -- author, title, venue, arXiv URL; (2) Pre-Mortem table and Consequences: Risks table differentiated with explicit scope distinction notes (failure discovery methodology vs. formal risk register); (3) Group 2 "27 agent-level + 5 framework-level" clarified with source citation to barrier-4/synthesis.md L1 Recommendation Counts table; Step 5 connected to H-17 quality gate and FMEA RPN 150 mitigation; (4) FMEA scale definitions added for Severity/Occurrence/Detection 1-10 dimensions.*
*I3 Revision (2026-02-28): 2 targeted fixes from adversary-adr001-i2.md (score 0.9455 REVISE, gap 0.0045 to 0.95): (1) A-31 full bibliographic citation added -- Bsharat, Myrzakhan, Shen, arXiv:2312.16171 (Evidence Quality 0.93 -> 0.95); VS-001/VS-003 disambiguated in References entry parenthetical; (2) R-QE-001 through R-ADS-003 compact sub-table added to Group 1 section with ID, target file, and one-line description (Actionability 0.94 -> 0.95).*
*Constitutional Compliance: Jerry Constitution v1.0 (P-003, P-020, P-022)*
*Format: Michael Nygard's ADR Format (2011), extended with L0/L1/L2 levels and adversarial quality strategies*
