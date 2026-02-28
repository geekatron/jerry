# ADR-002: Constitutional Triplet and High-Framing Upgrades

> ps-architect | TASK-016 | Phase 5 | PROJ-014 | 2026-02-28
> Decision Type: Conditional on Phase 2 outcome; reversible under PG-003 null finding
> Criticality: C4 (auto-escalated per AE-003: new ADR)
> Quality threshold: >= 0.95
> Self-review: H-15 applied before completion
> Version: 2.1.0 (I3 revision — weight derivation traceability, A-15 baseline rate, S-002 challenge independence)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | ADR lifecycle state |
| [L0: Executive Summary](#l0-executive-summary) | What we decided and why, in plain language |
| [Context](#context) | Problem and motivation |
| [Forces](#forces) | Tensions at play |
| [Constraints](#constraints) | Phase 2 dependency gate and evidence boundaries |
| [Options Considered](#options-considered) | All evaluated alternatives with trade-offs |
| [Decision](#decision) | Chosen approach with per-sub-decision rationale |
| [L1: Technical Implementation](#l1-technical-implementation) | Implementation details, migration steps, code patterns |
| [L2: Architectural Implications](#l2-architectural-implications) | Long-term evolution, systemic consequences |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes |
| [Risks](#risks) | Risk register with mitigation |
| [PG-003 Reversibility Assessment](#pg-003-reversibility-assessment) | Per-sub-decision reversibility under null framing finding |
| [Phase 2 Dependency Gate](#phase-2-dependency-gate) | Explicit implementation prerequisites |
| [Evidence Register](#evidence-register) | All cited evidence with tier labels and source task provenance |
| [Related Decisions](#related-decisions) | Links to other ADRs |
| [PS Integration](#ps-integration) | Worktracker linkage |

---

## Status

**PROPOSED**

MUST NOT advance to ACCEPTED until:
1. Phase 2 experimental results are available (C1-C7 pilot conditions executed)
2. PG-003 contingency assessment is applied to Phase 2 results
3. User explicitly approves (P-020)

---

## L0: Executive Summary

### What we decided

This ADR proposes three interrelated upgrades to how the Jerry Framework expresses its most critical behavioral constraints:

1. **Constitutional triplet in SKILL.md files (NPT-013):** Every skill's "Constitutional Compliance" section MUST express the P-003/P-020/P-022 constraints as NEVER statements with consequence documentation, rather than the current positive-framed descriptions used in many skills.

2. **VIOLATION label format in agent guardrails (NPT-009):** The `forbidden_actions` entries in agent governance files MUST follow the format `{TYPE} VIOLATION: NEVER {action} -- Consequence: {impact}` instead of the current bare minimum `{description} ({principle-reference})`.

3. **Paired prohibition and justified prohibition in rule files (NPT-010/NPT-011):** Critical HARD rules SHOULD pair NEVER/MUST NOT statements with immediately adjacent positive alternatives ("Instead: ...") and justification clauses ("Reason: ...").

### Why it matters

The Jerry Framework currently has 22 standalone blunt prohibitions (NPT-014 pattern) across 17 rule files, zero instances of paired prohibition-with-positive-alternative (NPT-010), and zero instances of justified prohibition (NPT-011). Anthropic's own production rule files use NEVER-framed constitutional constraints (T4 evidence, VS-004) and prohibitive vocabulary for HARD-tier enforcement (T4 evidence, VS-003). The gap between Jerry's current practice and observed vendor self-practice represents a working-practice alignment opportunity.

### Why this is conditional

**NEVER treat this decision as experimentally validated.** The evidence that structured negative framing (NPT-009 through NPT-013) outperforms structurally equivalent positive framing is UNTESTED at the causal level. T4 observational evidence (VS-001 through VS-004, 33 instances across 10 Claude Code rule files) establishes that Anthropic uses this approach in production, but three competing causal explanations exist for why (VS-002): (a) negative framing is genuinely more effective, (b) negative framing emerged from development convention, or (c) negative framing is optimized for human auditability rather than LLM compliance. Phase 2 experimental conditions (C1-C7) are designed to resolve this ambiguity. This ADR MUST NOT be implemented before Phase 2 completion.

---

## Context

### The Problem

The Jerry Framework expresses behavioral constraints across three artifact layers: SKILL.md files (13 files), agent definition files (30+ agents across 9 families), and rule files (17 files in `.context/rules/`). Across these layers, constraint expression is inconsistent:

**Current state inventory (Phase 4 findings):**

| Layer | NPT-014 (blunt) | NPT-009 (structured) | NPT-010 (paired) | NPT-011 (justified) | NPT-012 (re-injected) | NPT-013 (constitutional) |
|-------|-----------------|---------------------|-------------------|---------------------|----------------------|--------------------------|
| Rule files (TASK-012) | 22 instances (61%) | 8 instances (22%) | 0 instances | 0 instances | 11 instances (31%) | 3 instances (8%) |
| Agent files (TASK-011) | Low-maturity agents: flat markdown | Mid-maturity: partial VIOLATION labels | 0 instances | 0 instances | N/A (architectural exclusion) | Schema-enforced minimum (H-35) |
| SKILL.md files (TASK-010) | Present in 10 of 13 files | transcript SKILL.md as exemplar | Not analyzed | Not analyzed | Excluded from scope | 3 of 13 files |

**The inconsistency problem:** The Jerry Framework's agent-development-standards.md (H-34) requires a constitutional triplet (P-003, P-020, P-022) in every agent, but the minimum example uses NPT-014 framing:

```yaml
# Current minimum example (NPT-014):
forbidden_actions:
  - "Spawn recursive subagents (P-003)"
  - "Override user decisions (P-020)"
  - "Misrepresent capabilities or confidence (P-022)"
```

This means agents satisfying the minimum standard are NPT-014 compliant by design. High-maturity agents (nse-requirements, ts-parser, wt-auditor) independently upgraded to NPT-009 with consequence documentation. Low-maturity agents (eng-team, red-team, adv-executor, adv-scorer, sb-voice) use flat markdown equivalents of NPT-014. The framework's own standards template produces the pattern that the research identifies as lowest-performing (T1 evidence, A-20 AAAI 2026, A-15 EMNLP 2024).

### Vendor Self-Practice Evidence

**[T4 observational -- NEVER cite as causal evidence]**

- **VS-003 (T4):** Anthropic's Claude Code rule files use prohibitive vocabulary (NEVER, MUST NOT, FORBIDDEN) exclusively in HARD-tier constraints. This is a design fact directly observable in production rule files.
- **VS-004 (T4):** Constitutional constraints (the most safety-critical rules) are expressed as NEVER statements in Anthropic rule files. The P-003/P-020/P-022 triplet is re-injected per-prompt via L2-REINJECT markers.
- **VS-001 (T4):** 33 NEVER/MUST NOT/DO NOT instances across 10 Claude Code rule files provide direct observation that structured negative framing is used at scale in production.
- **VS-002 (T4):** Three competing causal explanations exist for vendor divergence from published literature guidance. NEVER collapse these to a single explanation.

### What This ADR Does NOT Decide

- Whether negative framing is causally superior to positive framing (Phase 2 experimental target)
- NPT-014 elimination policy (ADR-001 scope -- unconditional, separate decision)
- Routing disambiguation standards (ADR-003 scope)
- Context compaction resilience (ADR-004 scope)
- L2-REINJECT applicability to agent files (architectural question excluded from agent scope per TASK-011)

---

## Forces

| Force | Direction | Evidence |
|-------|-----------|----------|
| Vendor self-practice alignment | Favors adoption | T4 (VS-003, VS-004): Anthropic uses NEVER-framed constitutional constraints in production |
| Compliance improvement evidence | Favors structured constraints | T1 (A-15, EMNLP 2024): Atomic decomposition improves compliance +7.3-8.0% relative to structurally equivalent monolithic constraint baseline |
| Auditability of consequence documentation | Favors adoption regardless of framing | Structural: consequence documentation improves human review quality independent of LLM framing effect |
| Absence of causal comparison | Opposes premature adoption | UNTESTED: NPT-009/NPT-010/NPT-011 vs. structurally equivalent positive framing has no controlled evidence |
| Framework consistency | Favors adoption | Current inconsistency across maturity levels creates confusion about what "good" looks like |
| Phase 2 baseline contamination risk | Opposes pre-Phase-2 implementation | Implementing before baseline capture makes C1-C7 conditions unreproducible. **Resolved for Phase 5A:** template/schema changes affect only new-agent standards, not existing artifacts that serve as Phase 2 baseline. Phase 5B remains gated. |
| Migration cost for 30+ agent files | Opposes universal adoption | 78 Group 2 recommendations across all artifact layers require sequenced implementation |
| Convention lock-in risk | Opposes premature adoption | Adopting NEVER framing as standard before causal evidence may create convention inertia even if null effect found |

---

## Constraints

### Phase 2 Dependency Gate (BLOCKING)

**MUST NOT implement any recommendation in this ADR before Phase 2 experimental conditions (C1-C7) are complete and results analyzed.**

Rationale: The C1-C7 experimental design (TASK-005, barrier-2/synthesis.md) requires isolated framing conditions. Framework changes that alter negative constraint vocabulary before baseline capture make experimental conditions unreproducible per Orchestration Directive 6.

### Evidence Boundaries

| Claim | Evidence Tier | NEVER Conflate With |
|-------|--------------|---------------------|
| Blunt prohibition underperforms structured alternatives | T1 (A-20, A-15) | The specific claim that NEVER framing outperforms positive framing |
| Atomic decomposition improves compliance | T1 (A-15, EMNLP 2024, +7.3-8.0%) | Hallucination rate reduction -- A-15 measures compliance, not factual accuracy |
| Warning-based prompts improve negation accuracy | T1 (A-23, EMNLP 2025 Findings, +25.14%) | Hallucination rate reduction -- A-23 measures negation reasoning accuracy, not hallucination |
| Anthropic uses NEVER-framed constitutional constraints | T4 (VS-004, directly observable) | Experimental evidence that this is causally superior |
| HARD tier vocabulary = prohibitive | T4 (VS-003, directly observable) | Evidence that prohibitive vocabulary is more effective than permissive vocabulary |
| AGREE-5 12-level effectiveness hierarchy | Internally generated synthesis (barrier-1/synthesis.md, 0.953 PASS) | Externally validated framework -- NEVER cite AGREE-5 as externally validated |
| NPT-009 through NPT-013 rank ordering (ranks 9-11) | Internally generated, T4 observational only | T1 evidence -- the ordering reflects synthesizer judgment, not controlled comparison |

### Orchestration Directives Inherited

- Directive 4: MUST NOT treat absence of published evidence as evidence of absence
- Directive 5: MUST NOT dismiss practitioner or vendor self-practice evidence
- Directive 6: MUST NOT implement changes that make Phase 2 conditions unreproducible

---

## Options Considered

### Option A: Full Adoption -- Implement All Three Upgrades After Phase 2

Adopt NPT-013 in SKILL.md, NPT-009 VIOLATION format in agents, and NPT-010/NPT-011 in rule files as framework standards. Implementation gated on Phase 2 completion with GO verdict.

| Dimension | Assessment |
|-----------|------------|
| Evidence alignment | T4 observational (VS-003, VS-004) + T1 (A-15 compliance improvement) |
| Scope | 78 recommendations across 13 skills, 30+ agents, 17 rule files |
| Migration cost | HIGH: requires sequenced rollout across all artifact layers |
| Consistency gain | HIGH: eliminates maturity-level inconsistency |
| Reversibility | HIGH: all changes are additive text; no deletions |
| Risk | MEDIUM: convention lock-in if Phase 2 finds null effect |

**Steelman (S-003):** This option has the strongest case for framework consistency. The current state where high-maturity agents use NPT-009 and low-maturity agents use NPT-014 creates an implicit quality gradient that is undocumented and confusing for new agent authors. Standardizing to NPT-009 with VIOLATION labels eliminates this gradient regardless of whether the framing has LLM compliance benefits. The consequence documentation component has independent value for human auditors (TASK-011 PG-003 contingency: "consequence documentation is structurally valuable regardless of framing").

### Option B: Partial Adoption -- Only Consequence Documentation, Not Framing Change

Adopt consequence documentation (the structural component of NPT-009) without mandating NEVER/MUST NOT vocabulary. Agents would add `-- Consequence: {impact}` to existing prohibitions without changing the prohibition verb framing.

| Dimension | Assessment |
|-----------|------------|
| Evidence alignment | Independent of framing evidence; consequence documentation has standalone auditability value |
| Scope | Same 78 recommendations but with reduced text changes per recommendation |
| Migration cost | MEDIUM: consequence text additions only, no vocabulary changes |
| Consistency gain | MEDIUM: standardizes consequence documentation but preserves vocabulary inconsistency |
| Reversibility | HIGH: additive text only |
| Risk | LOW: no framing commitment; no convention lock-in |

**Steelman (S-003):** This option isolates the component with the strongest independent justification (auditability) from the component with the weakest evidence (framing vocabulary). If Phase 2 finds a null framing effect, Option B produces the same auditability benefit without having committed to a vocabulary convention that is not effectiveness-motivated. This is the most conservative evidence-respecting choice.

### Option C: Defer Entirely -- Wait for Phase 2 Results Before Any Standardization

Make no standard changes. Wait for Phase 2 experimental results and then decide based on causal evidence rather than observational evidence.

| Dimension | Assessment |
|-----------|------------|
| Evidence alignment | Maximum evidence discipline -- no commitment before causal data |
| Scope | Zero changes until Phase 2 complete |
| Migration cost | ZERO now; full cost deferred |
| Consistency gain | ZERO: current inconsistency persists |
| Reversibility | N/A: nothing to reverse |
| Risk | Missed consistency improvement; continued divergence as new agents are created |

**Steelman (S-003):** This is the epistemologically purest option. Every sub-decision in this ADR relies on T4 observational evidence for the framing component. T4 evidence establishes that a practice exists, not that it works. Deferring until T1 evidence is available (Phase 2) is the only option that avoids any risk of evidence-exceeding commitment. The cost of deferral is continued inconsistency -- but inconsistency is a lesser harm than adopting a potentially null-effect convention as a framework standard.

### Option D: New-Agent-Only -- Apply Standards to New Agents, Backfill Later

Update agent-development-standards.md template (REC-F-001, REC-F-002, REC-F-003) so that new agents follow NPT-009 format. Defer backfilling existing agents until Phase 2 data is available.

| Dimension | Assessment |
|-----------|------------|
| Evidence alignment | Template change is T4-aligned; existing agents unchanged |
| Scope | 3 framework-level changes (REC-F-001, REC-F-002, REC-F-003) only |
| Migration cost | LOW: template update only; no per-agent migration |
| Consistency gain | LOW: only affects agents created after template update |
| Reversibility | HIGH: template example is illustrative, not schema-enforced |
| Risk | LOW: minimal commitment; does not alter Phase 2 baseline for existing agents |

**Steelman (S-003):** This option produces the best cost-benefit ratio at this evidence stage. Updating the template costs 3 changes in one file. Every new agent created after the template update follows NPT-009 format automatically. Existing agents remain in their current state (preserving Phase 2 baseline). If Phase 2 finds a positive framing effect, the template already guides new agents correctly; if Phase 2 finds a null effect, the consequence documentation in the template still provides auditability value and the VIOLATION label becomes a convention choice rather than an effectiveness choice.

### Comparative Assessment

> **Scoring rubric (ordinal judgment, not experimentally derived):** 0 = completely fails this dimension; 3 = marginally satisfies; 5 = partially satisfies with known limitations; 7 = substantially satisfies; 10 = fully satisfies with no residual concern. Scores are author-assessed ordinal judgments reflecting architectural analysis, not calibrated against an external benchmark. Weights are author judgment (no external source): they were selected to reflect the primacy of evidence discipline (0.25) in a Phase 2-gated decision, followed by framework consistency (0.20) as the primary operational motivator, with migration cost, auditability, baseline safety, and reversibility sharing the remaining weight proportionally. Note: alternative weighting schemes would change the ordinal ranking -- for example, if framework consistency were weighted at 0.30 instead of 0.20, Option A would outscore Option C. The weight selection is a judgment call, not a derived quantity.

| Dimension | Weight | Option A | Option B | Option C | Option D |
|-----------|--------|----------|----------|----------|----------|
| Evidence respect | 0.25 | 6 (T4 only) | 8 (isolates auditability) | 10 (epistemically pure) | 7 (template-only commitment) |
| Framework consistency | 0.20 | 9 (full standardization) | 6 (partial standardization) | 2 (no change) | 4 (forward-only) |
| Migration cost | 0.15 | 3 (78 recs) | 5 (78 recs, less text) | 10 (zero) | 9 (3 recs) |
| Auditability gain | 0.15 | 9 (consequence docs everywhere) | 9 (consequence docs everywhere) | 1 (no change) | 5 (new agents only) |
| Phase 2 baseline safety | 0.15 | 4 (must sequence carefully) | 5 (must sequence carefully) | 10 (no contamination risk) | 9 (existing agents preserved) |
| Reversibility | 0.10 | 8 (additive text) | 9 (no vocabulary commitment) | 10 (nothing to reverse) | 9 (template only) |
| **Weighted Score** | **1.00** | **6.50** | **7.00** | **7.05** | **6.90** |

**Arithmetic verification (H-15):**
- Option A: (6x0.25)+(9x0.20)+(3x0.15)+(9x0.15)+(4x0.15)+(8x0.10) = 1.50+1.80+0.45+1.35+0.60+0.80 = **6.50**
- Option B: (8x0.25)+(6x0.20)+(5x0.15)+(9x0.15)+(5x0.15)+(9x0.10) = 2.00+1.20+0.75+1.35+0.75+0.90 = **7.00**
- Option C: (10x0.25)+(2x0.20)+(10x0.15)+(1x0.15)+(10x0.15)+(10x0.10) = 2.50+0.40+1.50+0.15+1.50+1.00 = **7.05**
- Option D: (7x0.25)+(4x0.20)+(9x0.15)+(5x0.15)+(9x0.15)+(9x0.10) = 1.75+0.80+1.35+0.75+1.35+0.90 = **6.90**

**Option C has the highest weighted score (7.05).** This reflects that deferral maximizes evidence respect, migration cost avoidance, baseline safety, and reversibility simultaneously. The decision to choose a hybrid of Option A and Option D over Option C is addressed in the [Decision](#decision) section.

---

## Decision

**Chosen: Hybrid of Option A (conditional) and Option D (immediate), with Phase 2 gate.**

### Why Not the Highest-Scoring Single Option?

**Option C (defer entirely) has the highest weighted score at 7.05.** The hybrid is preferred over Option C for three reasons:

1. **Option C's score is dominated by dimensions that reward inaction.** Option C scores 10 on three dimensions (evidence respect, migration cost, baseline safety) and 10 on a fourth (reversibility) precisely because it does nothing. These four dimensions account for 0.65 of the total weight. The two dimensions that measure positive framework improvement -- framework consistency (0.20) and auditability gain (0.15) -- give Option C scores of 2 and 1 respectively. Option C is the optimal choice only if the cost of continued inconsistency and absent consequence documentation is zero, which the Forces analysis contradicts ("Framework consistency -- Favors adoption"; "Auditability of consequence documentation -- Favors adoption regardless of framing").

2. **The hybrid captures Option D's cost-benefit advantage without Option C's zero-gain profile.** Option D (6.90) produces framework improvement at minimal cost (3 template changes, fully reversible). The hybrid's Phase 5A component is functionally Option D: it updates the template and schema without touching existing artifacts. Unlike Option C, the hybrid produces measurable improvement (new-agent quality floor, migration visibility) at near-zero risk.

3. **Option C defers consequence documentation that has framing-independent value.** The Inversion Analysis (S-013) establishes that consequence documentation is structurally bound to prohibition framing -- there is no natural positive-framing equivalent to "what breaks when violated." Deferring this structural improvement gains nothing that Phase 2 results would inform, because consequence documentation's auditability value does not depend on framing effectiveness.

**Option B (7.00) is the second-highest scorer.** Option B's Phase 5A equivalent would be "add consequence documentation without mandating NEVER vocabulary." The hybrid's Phase 5A component achieves this: the template update recommends but does not require NEVER vocabulary (the format guidance uses SHOULD, not MUST). The hybrid additionally provides the VIOLATION label convention and schema tracking field that Option B does not specify. The hybrid is Option B's consequence-documentation benefit plus Option D's forward-looking template standard, with Option A's full adoption available conditionally after Phase 2.

The decision is structured as two phases with an explicit dependency gate:

### Phase 5A: Immediate (Before Phase 2) -- Template and Schema Updates Only

**Sub-Decision 1: Update agent-development-standards.md guardrails template (D-001, REC-F-001 through REC-F-003)**

**DECIDE: YES.** Update the guardrails template minimum example from NPT-014 to NPT-009 format. Add VIOLATION label format guidance. Add tier-differentiated consequence guidance for T2+ agents.

**Rationale:** The template change costs 3 modifications in one file. It is illustrative, not schema-enforced -- existing agents are not invalidated. Consequence documentation has independent auditability value regardless of Phase 2 framing outcome (TASK-011 PG-003 contingency assessment). New agents created after this change follow NPT-009 format automatically. The change is fully reversible under PG-003 null finding (the minimum example reverts to positive framing if desired, but consequence documentation component is retained).

**Sub-Decision 2: Add forbidden_action_format tracking field to governance schema (D-003, REC-YAML-001)**

**DECIDE: YES.** Add an optional `forbidden_action_format` enum field (`NPT-009-complete`, `NPT-009-partial`, `NPT-014`) to `agent-governance-v1.schema.json`.

**Rationale:** The tracking field is an additive optional schema extension. It provides upgrade-path visibility for the 30+ agent migration regardless of framing outcome. Audit tracking of NPT format level remains valuable even under a null framing finding (TASK-011 PG-003 assessment: "Retain recommendation unchanged"). The field MUST be optional to avoid breaking existing agent file validation.

**Sub-Decision 3: Add schema description field recommendation for forbidden_actions format (D-006, REC-YAML-002)**

**DECIDE: YES.** Add a pattern recommendation to the schema `$comment` or description field for `forbidden_actions` items: "RECOMMENDED format: `{TYPE} VIOLATION: NEVER {action} -- Consequence: {impact}`. Minimum: `{description} ({principle-reference})`."

**Rationale:** Documentation-only change with zero validation impact. Communicates the recommended format to agent authors without enforcement. Fully reversible.

### Phase 5B: Conditional (After Phase 2) -- Full Adoption or Contingency

**MUST NOT execute Phase 5B until Phase 2 experimental results are available.**

**Sub-Decision 4: NPT-013 constitutional triplet in SKILL.md files (all 13 skills)**

**DECIDE: CONDITIONAL YES, gated on Phase 2.**

- If Phase 2 confirms framing effect at ranks 9-11 (GO verdict): Implement NPT-013 NEVER-framed constitutional triplet in all 13 SKILL.md files per TASK-010 recommendations.
- If Phase 2 finds null framing effect (PG-003 triggered): Implement consequence documentation only (the structural NPT-009 component). NEVER-framing becomes convention-alignment only, not effectiveness-motivated. The decision to use NEVER vs. positive framing defaults to convention consistency with existing high-maturity agents.

**Sub-Decision 5: NPT-009 VIOLATION label format in agent guardrails (27 agent-level recs)**

**DECIDE: CONDITIONAL YES, gated on Phase 2.**

- Sequencing (D-002 resolution): **New-agent-first, then backfill by maturity tier.**
  - Tier 1 (immediate after Phase 2): Mid-maturity agents (ps-analyst, ps-researcher, ps-critic, orch-planner, nse-verification) -- these already have partial VIOLATION labels; the gap is consequence documentation only.
  - Tier 2 (subsequent): Low-maturity agents (eng-architect, eng-security, red-lead, red-recon, adv-executor, adv-scorer, sb-voice) -- these require VIOLATION label addition + consequence documentation.
  - Tier 3 (last): High-maturity agents (nse-requirements, ts-parser, wt-auditor) -- these are already NPT-009 compliant. MUST NOT degrade these agents during normalization.

**Sub-Decision 6: PG-003 contingency gate (D-005)**

**DECIDE: YES (incorporated into Phase 2 Dependency Gate).**

D-005 governs whether Phase 2 data is available before this ADR is finalized. This sub-decision is operationalized by the [Phase 2 Dependency Gate](#phase-2-dependency-gate) section (G-001/G-002/G-003 conditions) and the [Decision Matrix Based on Phase 2 Outcome](#decision-matrix-based-on-phase-2-outcome) table, which specifies per-outcome actions for all Phase 5B sub-decisions. Under a null framing finding, all framing-motivated recommendations are reclassified to convention-alignment per PG-003 (barrier-2/synthesis.md ST-4). Source: TASK-011 agents-update-analysis D-005 definition.

**Sub-Decision 7: Structural refactor of eng-team/red-team agents (D-004)**

**DECIDE: OUT OF SCOPE.** The structural refactor from flat markdown to XML-tagged sections is a structural alignment task, not a negative prompting upgrade. It MUST NOT be bundled with framing-motivated changes. If pursued, it requires a separate enabler work item with its own justification.

**Rationale:** The cost of structural refactoring 8+ agent files (eng-team: 4 agents, red-team: 4+ agents) exceeds the NPT benefit. The NPT-009 VIOLATION label upgrade can be applied to flat markdown sections without requiring structural migration. Bundling structural and framing changes would confound any assessment of the framing change's impact.

**Sub-Decision 8: NPT-010/NPT-011 in rule files (D-007, TASK-012 recommendations)**

**DECIDE: CONDITIONAL YES, gated on Phase 2.**

- 4 NPT-010 additions (paired prohibition with positive alternative) to selected HARD rules
- 2 NPT-011 additions (justified prohibition with reason clause) to critical HARD rules

Implementation is additive text appended to existing rule entries. NEVER delete existing prohibition text; ONLY append positive alternative and justification clauses.

#### Provisional NPT-010/NPT-011 Candidate Rules

The following candidates are drawn from TASK-012 rules-update-analysis (Finding 5, Cross-File Pattern X-3, Phase 5 Downstream Inputs item 5). These are provisional -- final selection is subject to Phase 2 confirmation and implementation-time feasibility review.

**NPT-010 candidates (4 instances -- paired prohibition with positive alternative):**

| Target Rule | File | Current Form | Proposed NPT-010 Addition | Source |
|-------------|------|-------------|---------------------------|--------|
| H-01 (P-003) | `quality-enforcement.md` | "No recursive subagents (max 1 level)" | "NEVER spawn recursive subagents. Instead: delegate via single-level Task tool invocation from orchestrator to worker." | TASK-012 X-3 priority target |
| H-05 | `python-environment.md` | "MUST use `uv run`... NEVER use `python`/`pip`/`pip3` directly." | "NEVER use python/pip/pip3 directly. Instead: use `uv run` for execution, `uv add` for dependencies." | TASK-012 R-PE-001 (existing best NPT-010 example in L2-REINJECT; extend to body rule) |
| H-20 | `testing-standards.md` | "BDD test-first Red phase" | "NEVER write implementation code before a failing test exists. Instead: write the BDD scenario first, observe Red, then implement." | TASK-012 X-3 priority target |
| H-07 | `architecture-standards.md` | "Architecture layer isolation" | "NEVER import from infrastructure or interface layers in domain code. Instead: depend on ports defined in the domain layer." | TASK-012 R-ADS-003 |

**NPT-011 candidates (2 instances -- justified prohibition with reason clause):**

| Target Rule | File | Current Form | Proposed NPT-011 Addition | Source |
|-------------|------|-------------|---------------------------|--------|
| H-13 | `quality-enforcement.md` | "Quality threshold >= 0.92 for C2+ deliverables" | "NEVER accept a C2+ deliverable scoring below 0.92. Reason: the 0.92 threshold balances rigor with iteration cost; below this, defect density exceeds acceptable review burden." | TASK-012 Finding 5 (zero NPT-011 instances; H-13 is highest-impact quality gate) |
| H-31 | `quality-enforcement.md` | "Clarify before acting when requirements are ambiguous" | "NEVER assume intent when multiple valid interpretations exist. Reason: incorrect assumptions are the most expensive failure mode -- one clarifying question costs seconds; wrong-direction work costs hours." | TASK-012 Finding 5 (H-31 already contains the Reason text; NPT-011 formalizes it in the rule table) |

> **Evidence tier for all candidates:** AGREE-8 Moderate (NPT-010), AGREE-9 Moderate (NPT-011), T4 observational, UNTESTED causal comparison against positive equivalents. Phase 2 confirmation required before implementation. Under PG-003 null finding, the positive alternative component of NPT-010 and the justification component of NPT-011 retain structural value as implementation guidance regardless of framing effectiveness.

---

## L1: Technical Implementation

### Phase 5A Implementation (Immediate -- Before Phase 2)

#### 1. Template Update (REC-F-001)

**File:** `.context/rules/agent-development-standards.md`

**Current (NPT-014):**
```yaml
capabilities:
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Misrepresent capabilities or confidence (P-022)"
```

**Proposed (NPT-009):**
```yaml
capabilities:
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn recursive subagents -- Consequence: recursive delegation makes output provenance untraceable and violates H-01 audit trail"
    - "P-020 VIOLATION: NEVER override user decisions or proceed without explicit approval on destructive operations -- Consequence: unauthorized actions erode user trust and violate constitutional authority principle"
    - "P-022 VIOLATION: NEVER misrepresent capabilities, confidence levels, or actions taken -- Consequence: deceptive output undermines framework integrity and makes quality assessment unreliable"
```

#### 2. VIOLATION Label Format Guidance (REC-F-002)

**Add to agent-development-standards.md Guardrails Template section:**

```markdown
### Forbidden Actions Format Standard

`forbidden_actions` entries SHOULD use the following format:

`{VIOLATION-TYPE} VIOLATION: NEVER {action} -- Consequence: {operational impact}`

Where:
- `{VIOLATION-TYPE}` = the constitutional principle ID (P-003, P-020, P-022) or domain-specific violation type
- `{action}` = the prohibited behavior, scoped to the agent's domain
- `{operational impact}` = what breaks, degrades, or becomes unrecoverable if the violation occurs
```

#### 3. Tier-Differentiated Guidance (REC-F-003)

**Add to agent-development-standards.md Guardrails Template section:**

```markdown
### Tier-Differentiated Consequence Requirements

| Agent Tool Tier | Consequence Requirement | Rationale |
|----------------|------------------------|-----------|
| T1 (Read-Only) | MAY use NPT-014 minimum | Read-only agents have no state-affecting tools; consequence scope is limited |
| T2+ (Read-Write and above) | SHOULD use NPT-009 complete format with consequence documentation | State-affecting tools require documented impact of violation for audit trail |
| T5 (Full -- delegation capability) | MUST use NPT-009 complete format with domain-specific entries beyond constitutional triplet | Delegation-capable agents have the highest violation impact surface |
```

#### 4. Schema Update (REC-YAML-001)

**File:** `docs/schemas/agent-governance-v1.schema.json`

Add optional field:
```json
{
  "forbidden_action_format": {
    "type": "string",
    "enum": ["NPT-009-complete", "NPT-009-partial", "NPT-014"],
    "description": "Tracks the negative prompting pattern level of forbidden_actions entries. NPT-009-complete = VIOLATION label + scope + consequence. NPT-009-partial = VIOLATION label + scope. NPT-014 = blunt prohibition without structured format."
  }
}
```

**MUST NOT require this field at schema validation level.** The field is optional and tracking-only. Making it required would cause all existing agents to fail H-34 validation.

#### 5. Schema Description Update (REC-YAML-002)

**File:** `docs/schemas/agent-governance-v1.schema.json`

Add to `forbidden_actions` items definition:
```json
{
  "items": {
    "type": "string",
    "description": "RECOMMENDED format: '{TYPE} VIOLATION: NEVER {action} -- Consequence: {impact}'. Minimum: '{description} ({principle-reference})'"
  }
}
```

### Phase 5B Implementation (After Phase 2)

#### NPT-013 SKILL.md Constitutional Triplet

For each of 13 SKILL.md files, update the Constitutional Compliance section from:

**Current (positive framing in most skills):**
```markdown
### Constitutional Compliance
| Principle | Application |
|-----------|-------------|
| P-003 | Single-level agent only |
| P-020 | User authority respected |
| P-022 | Transparent about capabilities |
```

**Proposed (NPT-013 NEVER framing):**
```markdown
### Constitutional Compliance
| Principle | Constraint | Consequence |
|-----------|-----------|-------------|
| P-003 | NEVER spawn recursive subagents; this agent operates as a single-level worker only | Output provenance becomes untraceable; H-01 audit trail violated |
| P-020 | NEVER override user intent; NEVER proceed with destructive operations without explicit approval | Unauthorized action erodes trust; constitutional authority violated |
| P-022 | NEVER misrepresent actions taken, capabilities available, or confidence in findings | Quality assessment becomes unreliable; framework integrity undermined |
```

**PG-003 Null Finding Variant:** If Phase 2 finds null framing effect at ranks 9-11, the SKILL.md Constitutional Compliance section retains consequence documentation but replaces NEVER-framed constraints with positive-imperative equivalents:

```markdown
### Constitutional Compliance
| Principle | Constraint | Consequence if Violated |
|-----------|-----------|------------------------|
| P-003 | Operate as a single-level worker only; delegate via Task tool to orchestrator | Output provenance becomes untraceable; H-01 audit trail violated |
| P-020 | Respect user intent; obtain explicit approval before destructive operations | Unauthorized action erodes trust; constitutional authority violated |
| P-022 | Report actions taken, capabilities available, and confidence in findings accurately | Quality assessment becomes unreliable; framework integrity undermined |
```

Under this variant, the three-column table format (Principle/Constraint/Consequence) is retained -- only the verb framing changes from "NEVER X" to "Do Y." The consequence column is preserved because it has independent auditability value (Inversion Analysis finding).

#### NPT-009 Agent Forbidden Actions Upgrade

**Sequencing order (D-002 resolution):**

1. **Mid-maturity agents first** (partial VIOLATION labels already present -- gap is consequence documentation):
   - ps-analyst, ps-researcher, ps-critic: Add `-- Consequence: {impact}` to existing VIOLATION entries
   - orch-planner, nse-verification: Same pattern

2. **Low-maturity agents second** (structural VIOLATION label addition required):
   - eng-architect, eng-security: Convert "What You Do NOT Do" sections to VIOLATION format
   - red-lead, red-recon: Same pattern
   - adv-executor, adv-scorer: Convert inline prose prohibitions to VIOLATION format
   - sb-voice: Add VIOLATION labels to NEVER-list format

3. **High-maturity agents last** (verification only -- MUST NOT degrade):
   - nse-requirements, ts-parser, wt-auditor: Verify existing NPT-009 format; add any missing consequence clauses

**Tier advancement criteria:**
- **Tier 1 complete when:** All 5 mid-maturity agents have `forbidden_action_format: NPT-009-complete` in their `.governance.yaml` file AND CI validation (`agent-governance-v1.schema.json`) passes for all 5 files.
- **Tier 2 begins after:** Tier 1 is complete. Tier 2 complete when all 7 low-maturity agents have `forbidden_action_format: NPT-009-complete` OR `NPT-009-partial` (for agents where flat markdown structure limits full NPT-009 compliance, pending D-004 structural refactor).
- **Tier 3 begins after:** Tier 2 is complete. Tier 3 complete when all 3 high-maturity agents pass verification audit confirming no consequence clauses were lost or degraded during normalization.

#### NPT-010/NPT-011 Rule File Additions

**NPT-010 additions (4 instances -- paired prohibition with positive alternative):**

Pattern:
```markdown
| H-XX | NEVER {prohibited action}. Instead: {positive alternative}. | {consequence} |
```

Provisional targets (from Sub-Decision 8 candidate table): H-01 (`quality-enforcement.md`), H-05 (`python-environment.md`), H-20 (`testing-standards.md`), H-07 (`architecture-standards.md`). Each adds an "Instead:" clause to the existing HARD rule entry. NEVER modify the existing prohibition text; ONLY append the positive alternative.

**NPT-011 additions (2 instances -- justified prohibition):**

Pattern:
```markdown
| H-XX | NEVER {prohibited action}. Reason: {why this constraint exists}. | {consequence} |
```

Provisional targets (from Sub-Decision 8 candidate table): H-13 (`quality-enforcement.md`), H-31 (`quality-enforcement.md`). Each adds a "Reason:" clause to the existing HARD rule entry. H-31 already contains the justification text in its expanded definition; NPT-011 would formalize this into the rule table's concise entry.

> **All 6 candidates are provisional pending Phase 2 confirmation.** Implementation-time review should verify that each candidate's proposed text is accurate and non-conflicting with the rule's existing content. See Sub-Decision 8 for the full candidate table with current form and proposed additions.

---

## L2: Architectural Implications

### Long-Term Evolution Path

This ADR establishes the second tier of a three-tier constraint upgrade architecture:

| Tier | ADR | Scope | Evidence Gate | Status |
|------|-----|-------|--------------|--------|
| 1 | ADR-001 | NPT-014 elimination (blunt prohibition upgrade) | T1+T3, unconditional | Separate ADR |
| **2** | **ADR-002** | **Constitutional triplet + high-framing upgrades** | **T4 observational, Phase 2 conditional** | **This ADR** |
| 3 | ADR-004 | Context compaction resilience | T4 LOW, failure-mode-motivated | Future ADR |

The three-tier architecture ensures that:
- Tier 1 changes (unconditional) proceed regardless of Phase 2 outcome
- Tier 2 changes (conditional) are gated on experimental evidence
- Tier 3 changes (failure-mode-motivated) address operational risks independently

### Systemic Consequences

**1. Template-as-Standard-Setter:**
Phase 5A's template update creates a "pull" mechanism: every new agent created after the template change follows NPT-009 format. Over time, the proportion of NPT-009-compliant agents increases without requiring manual backfill. The `forbidden_action_format` tracking field enables visibility into migration progress.

**2. Convention Lock-In Risk:**
If this ADR is accepted and implemented, NEVER-framed prohibitions become the documented standard. Even if Phase 2 finds a null framing effect, the convention is established. The PG-003 contingency plan addresses this: under null finding, the framing vocabulary becomes "convention-alignment only, not effectiveness-motivated" -- but the convention persists. This is an acceptable trade-off because (a) consequence documentation has independent auditability value, and (b) consistency across agent families has independent readability value.

**3. Schema Evolution:**
REC-YAML-001 adds the first NPT-aware field to the governance schema. This establishes a pattern: future NPT-related tracking (e.g., NPT-010 paired-prohibition presence, NPT-011 justification presence) can follow the same optional-enum pattern. The schema remains backward-compatible because all new fields are optional.

**4. Relationship to L2-REINJECT Architecture:**
This ADR explicitly excludes L2-REINJECT changes from agent scope (per TASK-011 finding). L2-REINJECT operates at the rule-file layer, not the agent-definition layer. Agent `.md` files are loaded at invocation (Tier 2 progressive disclosure), not re-injected per-prompt. Any future consideration of per-agent L2 mechanisms requires a separate architectural analysis.

### Pre-Mortem Analysis (S-004)

**Scenario: It is 6 months after implementation. What went wrong?**

| Failure Mode | Probability | Impact | Detection | Mitigation |
|-------------|------------|--------|-----------|------------|
| Phase 2 finds null framing effect; NPT-009 VIOLATION format is already standard | MEDIUM | LOW | Phase 2 results analysis | PG-003 contingency: reclassify rationale from "effectiveness" to "auditability"; consequence documentation retained |
| Migration fatigue: 78 recommendations create backlog that is never completed | MEDIUM | MEDIUM | `forbidden_action_format` tracking field shows stalled migration | Tier-based sequencing (mid-maturity first) reduces backlog by addressing highest-ROI agents first |
| New agent authors ignore template guidance; continue creating NPT-014 agents | LOW | LOW | Schema tracking field shows NPT-014 for new agents | CI gate on `forbidden_action_format` field for T2+ agents (future enhancement) |
| Consequence documentation becomes boilerplate; loses specificity over time | MEDIUM | MEDIUM | Quality review of consequence clauses during creator-critic cycles | Require domain-specific consequence language, not copy-paste from template |
| eng-team/red-team structural refactor is deferred indefinitely; agents remain flat markdown | HIGH | LOW | Agent maturity tracking | Explicitly out of scope (D-004); separate enabler if needed |

### Inversion Analysis (S-013)

**What if we deliberately chose the opposite -- positive-only framing for all constitutional constraints?**

If we replaced all NEVER statements with positive directives ("Always respect user authority" instead of "NEVER override user decisions"), the framework would:
- Lose alignment with observed vendor self-practice (VS-003, VS-004) -- Anthropic uses prohibitive framing for HARD constraints
- Gain alignment with some published literature suggesting positive framing is more effective (but this literature primarily studies blunt prohibition, not structured negative constraints -- the Type 1 vs. Type 2-4 distinction from IG-002)
- Lose the auditability benefit of consequence documentation (positive framing does not naturally include "what breaks if violated" because there is no violation concept)
- Create a framework that looks different from the production systems it is designed to govern

The inversion reveals that the consequence documentation component is the strongest independent motivator -- it is structurally bound to the prohibition framing (you document what happens when something is violated; there is no equivalent "what happens when something is followed" pattern for positive directives).

---

## Consequences

### Positive

1. **Framework consistency** [T4-motivated]: Eliminates the maturity-level quality gradient where high-maturity agents use NPT-009 and low-maturity agents use NPT-014, creating a clear "what good looks like" standard.

2. **Auditability improvement** [Framing-independent]: Consequence documentation makes it explicit what breaks when a constraint is violated. This helps human reviewers, not just LLMs.

3. **Vendor self-practice alignment** [T4, VS-003/VS-004]: Brings Jerry's constraint expression in line with observed Anthropic production practices for HARD-tier enforcement.

4. **New-agent quality floor** [Template effect]: Phase 5A template update immediately raises the quality floor for all newly created agents without requiring migration effort.

5. **Migration visibility** [Schema tracking]: The `forbidden_action_format` tracking field provides quantitative migration progress monitoring.

### Negative

1. **Migration burden** [78 recommendations]: Full implementation requires changes across 13 SKILL.md files, 27 agent-level updates, and 6 rule file modifications. This is a significant coordination effort.

2. **Convention lock-in** [Risk if null framing effect]: If Phase 2 finds that NEVER framing has no causal advantage over positive framing, the framework will have committed to a convention that is not effectiveness-motivated. Mitigation: PG-003 contingency reclassifies rationale.

3. **Phase 2 contamination risk** [If sequencing fails]: Any Phase 5B implementation that occurs before Phase 2 baseline capture makes experimental conditions unreproducible. Mitigation: Explicit Phase 2 dependency gate in this ADR.

4. **Boilerplate risk** [Consequence quality degradation]: If consequence documentation becomes formulaic copy-paste, the auditability benefit degrades. Mitigation: Require domain-specific consequence language.

5. **Evidence-exceeding commitment** [T4 observational only]: The framing component of this decision relies on T4 observational evidence, not T1 causal evidence. NEVER present this decision as experimentally validated.

### Neutral

1. **Schema extension precedent**: REC-YAML-001 establishes a pattern for adding NPT-aware tracking fields. Future fields (NPT-010 tracking, NPT-011 tracking) can follow the same pattern.

2. **eng-team/red-team structural refactor deferred**: Explicitly out of scope (D-004). Neither a benefit nor a cost of this ADR -- the decision to defer is a separate concern.

3. **AGREE-5 hierarchy status unchanged**: This ADR does not validate or invalidate the 12-level effectiveness hierarchy. AGREE-5 remains an internally generated synthesis product.

---

## Risks

| Risk ID | Risk | Likelihood | Impact | Severity | Mitigation |
|---------|------|-----------|--------|----------|------------|
| R-001 | Phase 2 finds null framing effect; convention already established by Phase 5A template | MEDIUM | LOW | LOW | PG-003 contingency: reclassify from effectiveness to convention-alignment; consequence documentation retained |
| R-002 | Phase 5B implementation contaminates Phase 2 baseline | LOW (if gate respected) | HIGH | MEDIUM | BLOCKING dependency gate; this ADR explicitly prohibits Phase 5B before Phase 2 |
| R-003 | Migration backlog stalls; partial adoption creates new inconsistency | MEDIUM | MEDIUM | MEDIUM | Tier-based sequencing; `forbidden_action_format` tracking; mid-maturity agents first (lowest cost, highest visibility) |
| R-004 | Schema change (REC-YAML-001) breaks existing agent validation | LOW | HIGH | MEDIUM | Field is optional; additive-only schema extension; no required field changes |
| R-005 | Consequence documentation becomes generic boilerplate | MEDIUM | MEDIUM | MEDIUM | Require domain-specific language; quality review in creator-critic cycles |
| R-006 | eng-team/red-team agents remain permanently at low maturity | HIGH | LOW | LOW | Explicitly deferred (D-004); separate enabler work item if maturity gap becomes blocking |

---

## PG-003 Reversibility Assessment

**PG-003 (barrier-2/synthesis.md ST-4):** If Phase 2 finds a null framing effect at ranks 9-11, vocabulary choice becomes convention-determined, not effectiveness-determined. Phase 4 design MUST be reversible on the vocabulary dimension.

| Sub-Decision | ID | Reversible? | Action Under Null Finding | What Is Retained |
|-------------|-----|-------------|--------------------------|------------------|
| Template update (REC-F-001-F-003) | D-001 | YES | Reclassify rationale from "effectiveness" to "convention-alignment and auditability" | Consequence documentation (auditability value); VIOLATION label (convention value) |
| Schema tracking field (REC-YAML-001) | D-003 | YES | Retain unchanged -- audit tracking valuable regardless of framing outcome | Full field retained |
| Schema description (REC-YAML-002) | D-006 | YES | Modify "RECOMMENDED format" rationale from "effectiveness" to "convention-alignment" | Documentation retained with modified rationale |
| PG-003 contingency gate | D-005 | N/A | D-005 IS the contingency gate -- it operationalizes this assessment | Gate mechanism retained |
| NPT-013 SKILL.md triplet (conditional) | Sub-4 | YES | Implement with consequence documentation only; NEVER-framing becomes convention-choice (see [PG-003 Null Finding Variant](#npt-013-skillmd-constitutional-triplet)) | Consequence column retained; NEVER verb becomes optional |
| NPT-009 VIOLATION agent labels (conditional) | Sub-5 | YES | Implement consequence documentation; VIOLATION label becomes convention-choice | Consequence text retained |
| Structural refactor (eng-team/red-team) | D-004 | N/A | Out of scope -- not affected by framing finding | N/A |
| NPT-010/NPT-011 rule file additions (conditional) | D-007 | YES | Implement positive alternatives and justification clauses regardless of framing verb | Positive alternative and justification text retained (these are independently valuable) |

**Assessment: All 8 sub-decisions are fully reversible on the vocabulary dimension (or N/A for scope exclusions and the gate itself).** NEVER-framing verb can be replaced with positive framing verb in all cases without losing the structural additions (consequence documentation, positive alternatives, justification clauses). The structural additions have independent value (auditability, readability) that is preserved under PG-003 null finding.

---

## Phase 2 Dependency Gate

### BLOCKING Prerequisites

| Gate | Condition | Evidence Required |
|------|-----------|-------------------|
| G-001 | C1-C7 pilot conditions executed (n=30) | Pilot execution report with per-condition data |
| G-002 | GO/NO-GO criteria evaluated | Primary: pi_d in 0.10-0.50 range; <= 4 execution failures; kappa >= 0.70 |
| G-003 | PG-003 contingency assessment completed | Explicit determination: framing effect confirmed, null, or inconclusive |

### Decision Matrix Based on Phase 2 Outcome

| Phase 2 Outcome | Phase 5A (Template/Schema) | Phase 5B Sub-Decisions 4-5, 7-8 | PG-003 Status |
|-----------------|---------------------------|--------------------------------|---------------|
| GO + framing effect confirmed | Already implemented | Implement in full as described | Not triggered |
| GO + null framing effect | Already implemented; reclassify rationale | Implement consequence documentation; NEVER-framing becomes convention-choice | Triggered -- reclassify all rationale |
| NO-GO (pilot fails calibration) | Already implemented; no change | DEFER until full experiment (n~268) completes | Pending |
| Inconclusive (pilot underpowered, power=0.17) | Already implemented; no change | DEFER until full experiment | Pending |

### What MUST NOT Happen Before Phase 2

1. MUST NOT modify any existing agent `forbidden_actions` entries (Phase 5B, Sub-Decision 5)
2. MUST NOT modify any existing SKILL.md Constitutional Compliance sections (Phase 5B, Sub-Decision 4)
3. MUST NOT modify any existing rule file HARD rules (Phase 5B, Sub-Decision 8)
4. MUST NOT create implementation tickets for Phase 5B changes

Phase 5A changes (template update, schema additions) are permitted before Phase 2 because they affect only the standard/template, not existing artifacts that serve as Phase 2 baseline.

---

## Evidence Register

All evidence cited in this ADR with tier labels and scope constraints.

| Evidence ID | Source | Tier | Scope Constraint | Cited For | Source Task |
|-------------|--------|------|-----------------|-----------|-------------|
| A-15 | DeCRIM, EMNLP 2024 | T1 | Compliance rate (+7.3-8.0%) relative to structurally equivalent monolithic constraint baseline; absolute baseline: GPT-4 fails constraints on 21%+ of instructions (Ferraz et al. source paper), meaning the improvement is from a ~79% baseline to ~86-87%; NOT hallucination rate; measures atomic decomposition benefit, not framing polarity | Structured constraint pairing improves compliance | Phase 1 (barrier-1/synthesis.md) |
| A-20 | AAAI 2026 | T1 | Instruction hierarchy failure in task-following | Blunt prohibition underperforms structured alternatives | Phase 1 (barrier-1/synthesis.md) |
| A-23 | Barreto & Jana, EMNLP 2025 Findings | T1 (Findings track -- shorter format, typically non-archival; consider T1-minus weight relative to full EMNLP proceedings papers) | Negation reasoning accuracy (+25.14%), NOT hallucination rate | Warning-based prompts improve negation accuracy | Phase 1 (barrier-1/synthesis.md) |
| A-31 | Bsharat et al., arXiv | T3 | Reasoning tasks; 55% improvement signal on GPT-4 | Affirmative directives outperform blunt prohibition | Phase 1 (barrier-1/synthesis.md) |
| VS-001 | supplemental-vendor-evidence.md | T4 | 33 NEVER/MUST NOT instances across 10 Claude Code rule files; Anthropic-heavy concentration | Vendor uses structured negative framing at scale | Phase 1 (barrier-1/supplemental-vendor-evidence.md) |
| VS-002 | supplemental-vendor-evidence.md | T4 | Three competing causal explanations | Vendor divergence from literature is ambiguous | Phase 1 (barrier-1/supplemental-vendor-evidence.md) |
| VS-003 | supplemental-vendor-evidence.md | T4 | HARD tier = prohibitive vocabulary (design fact) | Tier vocabulary alignment observation | Phase 1 (barrier-1/supplemental-vendor-evidence.md) |
| VS-004 | supplemental-vendor-evidence.md | T4 | Constitutional constraints as NEVER statements | Constitutional triplet framing observation | Phase 1 (barrier-1/supplemental-vendor-evidence.md) |
| AGREE-5 | barrier-1/synthesis.md | Internal synthesis (0.953 PASS) | 12-level effectiveness hierarchy; NOT externally validated | Taxonomy backbone -- NEVER cite as externally validated | Phase 1 (barrier-1/synthesis.md) |
| PG-001 | barrier-2/synthesis.md ST-4 | T1+T3, unconditional | NEVER use standalone blunt prohibition | Baseline requirement (ADR-001 scope, referenced here) | Phase 2 design (barrier-2/synthesis.md) |
| PG-003 | barrier-2/synthesis.md ST-4 | T4 observational, MEDIUM | Pair enforcement-tier constraints with consequences; reversible if null framing effect | Contingency planning for null Phase 2 outcome | Phase 2 design (barrier-2/synthesis.md) |
| PG-004 | barrier-2/synthesis.md ST-4 | T4, unconditional by failure mode logic | Test context compaction before deployment | Referenced but not in scope (ADR-004) | Phase 2 design (barrier-2/synthesis.md) |
| E-007 | AGREE-9 cross-survey | Moderate (2-of-3 practitioner consensus) | Contrastive example pairing | Referenced for NPT-008 context only | Phase 1 (barrier-1/synthesis.md) |

### Internal Recommendation Provenance

| Recommendation ID | Generated By | Sub-Decision | Description |
|-------------------|-------------|-------------|-------------|
| REC-F-001 | TASK-011 (agents-update-analysis) | D-001 | Update guardrails template from NPT-014 to NPT-009 |
| REC-F-002 | TASK-011 (agents-update-analysis) | D-001 | Add VIOLATION label format guidance |
| REC-F-003 | TASK-011 (agents-update-analysis) | D-001 | Add tier-differentiated consequence requirements |
| REC-YAML-001 | TASK-011 (agents-update-analysis) | D-003 | Add `forbidden_action_format` tracking field to governance schema |
| REC-YAML-002 | TASK-011 (agents-update-analysis) | D-006 | Add schema description field recommendation for forbidden_actions format |

**NEVER cite A-11.** A-11 is a confirmed hallucinated citation (TASK-013, barrier-4/synthesis.md Section 6). It does not exist.

---

## Related Decisions

| ADR | Relationship | Status |
|-----|-------------|--------|
| ADR-001 (NPT-014 Elimination) | Prerequisite -- ADR-001's unconditional NPT-014 upgrade is the foundation that ADR-002 builds upon | PROPOSED (separate Phase 5 ADR) |
| ADR-003 (Routing Disambiguation) | Sibling -- shares Phase 2 dependency gate; NPT-010 "MUST NOT use when:" sections overlap with this ADR's NPT-010 scope | PROPOSED (separate Phase 5 ADR) |
| ADR-004 (Context Compaction Resilience) | Downstream -- context compaction testing (PG-004) should verify that NPT-009/NPT-010/NPT-011 patterns survive compaction | PROPOSED (separate Phase 5 ADR) |
| ADR-PROJ007-001 (Agent Definition Format) | Upstream -- established the agent definition schema that this ADR proposes to extend | ACCEPTED |

---

## FMEA Analysis (S-012)

| Failure Mode | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN | Mitigation |
|-------------|-----------------|-------------------|-------------------|-----|------------|
| Template update produces agents with generic boilerplate consequences | 4 | 6 | 5 | 120 | Quality review in creator-critic cycles; domain-specific consequence requirement |
| Phase 2 gate bypassed; agents modified before baseline capture | 8 | 2 | 3 | 48 | Explicit BLOCKING gate in ADR; orchestration directive 6 enforcement |
| Schema field causes validation failure in existing agents | 7 | 1 | 2 | 14 | Optional field; additive schema extension; CI regression test |
| Migration creates inconsistent hybrid state (some agents upgraded, some not) | 3 | 7 | 4 | 84 | Tier-based sequencing; `forbidden_action_format` tracking; accept hybrid state as transitional |
| Consequence documentation diverges from actual operational impact | 5 | 4 | 6 | 120 | Periodic audit of consequence accuracy against observed failure modes |

---

## Compliance

### Constitutional Compliance

| Principle | This ADR's Compliance |
|-----------|----------------------|
| P-001 (Truth) | All evidence tier labels documented; T4 vs. T1 distinction maintained throughout; UNTESTED claims labeled |
| P-002 (Persistence) | ADR persisted to file at `phase-5/ADR-002-constitutional-upgrades.md` |
| P-003 (No Recursion) | N/A -- ADR does not involve agent spawning |
| P-004 (Provenance) | All 7 input analyses cited with quality gate scores; evidence register with tier labels |
| P-011 (Evidence-Based) | 4 options evaluated with weighted scoring; alternatives steelmanned (S-003) |
| P-020 (User Authority) | Status PROPOSED; MUST NOT advance without user approval |
| P-022 (No Deception) | Negative consequences documented (5 items); evidence gaps acknowledged; AGREE-5 labeled as internally generated |

### Adversarial Quality Strategies Applied

| Strategy | Application |
|----------|-------------|
| S-002 (Devil's Advocate) | **General challenge:** "What if our assumption that consequence documentation has independent value is wrong?" -- Addressed: even formulaic consequence documentation provides grep-able audit trail that positive framing does not naturally produce. **Hybrid-specific challenge (Phase 5A non-contamination):** "What evidence supports the claim that template-only changes in Phase 5A do not alter the baseline distribution of constraint expressions in existing artifacts, thereby contaminating Phase 2 conditions?" -- Addressed: Phase 5A modifies three locations: (1) the guardrails template minimum example in `agent-development-standards.md`, (2) an optional enum field in `agent-governance-v1.schema.json`, and (3) a description field recommendation in the same schema file. None of these modify existing agent `.md` files, existing `.governance.yaml` files, or existing rule files. The template is illustrative (it shows what new agents SHOULD look like), not enforced via CI validation on existing files. The schema field is optional and defaults to absent. No existing artifact that would serve as a Phase 2 baseline condition is touched. The contamination risk would arise only if Phase 5A changes triggered automated reformatting of existing files (they do not) or if agent authors retroactively updated existing agents to match the new template before Phase 2 baseline capture (mitigated by the explicit "What MUST NOT Happen Before Phase 2" checklist, item 1: "MUST NOT modify any existing agent `forbidden_actions` entries"). Residual risk: an agent author could voluntarily update an existing agent to NPT-009 before Phase 2. This is a process-discipline risk, not an architectural contamination, and is bounded by the BLOCKING gate's 4-item prohibition list. |
| S-003 (Steelman) | All 4 options steelmanned before comparative assessment; Option C (defer entirely) given strongest epistemological case |
| S-004 (Pre-Mortem) | 5 failure modes identified with probability/impact assessment |
| S-010 (Self-Refine) | H-15 self-review completed before output; checked: evidence tier labels, PG-003 contingency coverage, Phase 2 gate explicitness, A-11 exclusion, AGREE-5 origin disclosure |
| S-012 (FMEA) | 5 failure modes analyzed with RPN scoring |
| S-013 (Inversion) | "What if we chose positive-only framing?" analysis reveals consequence documentation is structurally bound to prohibition framing |

---

## PS Integration

- **PS ID:** PROJ-014
- **Entry ID:** TASK-016
- **Artifact Path:** `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-002-constitutional-upgrades.md`
- **Decision:** Adopt hybrid approach: Phase 5A (template/schema updates) immediate; Phase 5B (full adoption) conditional on Phase 2
- **Status:** PROPOSED
- **Next Agent Hint:** ps-critic for adversarial quality review at C4 threshold (>= 0.95)

### Key Findings

1. The hybrid approach (Option A conditional + Option D immediate) is chosen over Option C (highest weighted score at 7.05) because Option C's score is dominated by dimensions that reward inaction while scoring 2/10 and 1/10 on the two improvement dimensions
2. All 8 sub-decisions (D-001 through D-007 plus D-005 PG-003 gate) are fully reversible under PG-003 null framing finding
3. Phase 5A template changes cost 3 modifications in 1 file; Phase 5B requires 78 modifications across all artifact layers
4. The `forbidden_action_format` tracking field provides migration visibility regardless of Phase 2 outcome
5. eng-team/red-team structural refactor is explicitly out of scope (D-004)
6. Provisional NPT-010/NPT-011 candidate rules identified from TASK-012: H-01, H-05, H-07, H-20 for NPT-010; H-13, H-31 for NPT-011

### Confidence

0.82 -- HIGH for the decision structure and sequencing; MEDIUM for the Phase 2-conditional framing recommendations (T4 evidence only for framing component; consequence documentation component has independent structural justification).

---

## Self-Review Checklist (H-15)

### I1 Self-Review

- [x] P-001: Are option evaluations factually accurate? YES -- evidence tier labels on all claims; T4 vs. T1 distinction maintained
- [x] P-002: Is ADR persisted to file? YES -- written to phase-5/ADR-002-constitutional-upgrades.md
- [x] P-004: Are context and rationale documented? YES -- 7 input analyses cited with quality gate scores
- [x] P-011: Are alternatives evaluated? YES -- 4 options with weighted comparative assessment
- [x] P-020: Is status PROPOSED (not ACCEPTED)? YES
- [x] P-022: Are negative consequences documented? YES -- 5 negative consequences; evidence gaps acknowledged
- [x] A-11 exclusion verified? YES -- A-11 not cited; exclusion documented in Evidence Register
- [x] AGREE-5 origin disclosed? YES -- labeled as "internally generated synthesis, NOT externally validated" in Evidence Register and L0
- [x] Phase 2 dependency gate explicit? YES -- BLOCKING gate with decision matrix
- [x] PG-003 reversibility assessed per sub-decision? YES -- all 8 sub-decisions assessed
- [x] All constraint language uses NEVER/MUST NOT framing? YES -- per orchestration directive

### I2 Revision Self-Review (v2.0.0)

- [x] Arithmetic errors corrected? YES -- Option A: 6.55 -> 6.50; Option C: 6.35 -> 7.05; arithmetic verification block added
- [x] Decision rationale addresses highest scorer? YES -- "Why Not the Highest-Scoring Single Option?" section added; explains why hybrid is preferred over Option C (7.05) and Option B (7.00)
- [x] NPT-010/NPT-011 provisional candidates identified? YES -- 4 NPT-010 candidates (H-01, H-05, H-07, H-20) and 2 NPT-011 candidates (H-13, H-31) from TASK-012
- [x] Scoring rubric documented? YES -- ordinal judgment scale (0-10) with calibration anchors; weight derivation rationale added
- [x] A-23 Findings track qualification added? YES -- T1 with "Findings track -- shorter format, typically non-archival; consider T1-minus weight"
- [x] A-15 baseline context added? YES -- "relative to structurally equivalent monolithic constraint baseline"
- [x] REC-F-001 through REC-YAML-002 source tasks documented? YES -- Internal Recommendation Provenance table added
- [x] D-005 numbering gap resolved? YES -- D-005 (PG-003 contingency gate) added as Sub-Decision 6; renumbered subsequent sub-decisions
- [x] PG-003 null-finding SKILL.md template variant provided? YES -- before/after added with positive-imperative equivalent
- [x] Tier advancement criteria added? YES -- per-tier completion criteria with CI gate trigger
- [x] Forces table Phase 2 contamination risk annotated? YES -- "Resolved for Phase 5A" annotation added
- [x] Devil's Advocate challenge for hybrid added? YES -- hybrid-specific S-002 challenge in Compliance section
- [x] No new issues introduced? Verified by systematic review of all changes against existing content
- [x] A-11 not cited in any revision content? YES -- verified
- [x] AGREE-5 not cited as T1/T3? YES -- no new AGREE-5 references introduced

### I3 Revision Self-Review (v2.1.0)

- [x] Weight derivation traceability closed? YES -- comparative assessment preamble now explicitly states "author judgment (no external source)" and notes that alternative weighting schemes would change the ordinal ranking
- [x] A-15 absolute baseline compliance rate added? YES -- Evidence Register A-15 scope constraint now includes "GPT-4 fails constraints on 21%+ of instructions (Ferraz et al. source paper), meaning the improvement is from a ~79% baseline to ~86-87%"
- [x] S-002 hybrid challenge independence established? YES -- replaced Option B/C comparison (which repeated "Why Not Highest Scorer?" section) with independent attack on Phase 5A non-contamination assumption; new challenge addresses whether template-only changes can truly proceed without contaminating Phase 2 baselines
- [x] No new content beyond I2 scorer's 3 improvement recommendations? YES -- only fixes 1-3 (priority 1, 2, 3) from adversary-adr002-i2.md applied
- [x] A-11 not cited? YES -- verified
- [x] AGREE-5 not cited as T1/T3? YES -- no new AGREE-5 references
- [x] No new arithmetic introduced? YES -- no scoring changes; only textual additions to existing sections
