# ADR-004: Context Compaction Resilience — PG-004 Testing Requirement, NPT-012 L2-REINJECT Additions for Tier B HARD Rules, T-004 Failure Mode Documentation

> ps-architect | TASK-016 | Phase 5 | PROJ-014 | 2026-02-28
> Criticality: C4 (auto-escalated per AE-003: new ADR + AE-002: touches .context/rules/ scope)
> Quality threshold: >= 0.95 (C4)
> Self-review: H-15 applied before completion
> Version: 2.1.0
> I2 Revision (2026-02-28): 6 targeted fixes from adversary-adr004-i1.md (score 0.874 REVISE -> target >= 0.95): (1) Options comparison replaced with weighted-criteria evaluation table; (2) Minimum Viable Manual Test Protocol added for PG-004; (3) Explicit implementation gate added for 559/670 token discrepancy; (4) Vulnerability assessment framework documented for per-artifact test conditions; (5) TASK-012 F3 confidence revised, PG-004 unconditional classification clarified; (6) L2-REINJECT rank=11/12 justification added with existing rank ordering context.
> I3 Revision (2026-02-28): 6 targeted fixes from adversary-adr004-i2.md (score 0.925 REVISE -> target >= 0.95): (1) Weight derivation note + T-004 Coverage scoring footnote + Force-to-Dimension mapping (MR 0.92->0.95); (2) PG-004 evidence entry split into two rows (EQ 0.90->0.93); (3) MVP test protocol executor role + Step 3 context-fill target (Completeness 0.93->0.95); (4) Force-to-Dimension mapping in weighting rationale (IC 0.93->0.95); (5) MVP executor and implementation gate owner relationship clarified (Actionability 0.93->0.95); (6) Force-to-Dimension traceability in weighting rationale (Traceability 0.94->0.95).

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Status](#status) | ADR status per P-020 |
| [L0: Executive Summary](#l0-executive-summary) | What we decided and why, in plain language |
| [Context](#context) | Problem and motivation |
| [Constraints](#constraints) | Inherited constraints from upstream phases |
| [Forces](#forces) | Tensions at play in this decision |
| [Options Considered](#options-considered) | Alternatives evaluated per P-011 |
| [Decision](#decision) | Chosen approach with rationale |
| [L1: Technical Implementation](#l1-technical-implementation) | Implementation details, token arithmetic, code patterns, MVP test protocol |
| [L2: Architectural Implications](#l2-architectural-implications) | Long-term evolution, systemic consequences |
| [Consequences](#consequences) | Positive, negative, and neutral outcomes |
| [Risks](#risks) | Identified risks with mitigation |
| [PG-003 Reversibility Assessment](#pg-003-reversibility-assessment) | What changes if Phase 2 finds null framing effect |
| [Evidence Summary](#evidence-summary) | All evidence cited with tier labels |
| [Related Decisions](#related-decisions) | Links to other ADRs and upstream artifacts |
| [Compliance](#compliance) | Constitutional and constraint compliance verification |
| [Self-Review Checklist](#self-review-checklist) | H-15 compliance |
| [I2 Fix Resolution Checklist](#i2-fix-resolution-checklist) | Resolution status for all 6 I1 adversary gate fixes |
| [I3 Fix Resolution Checklist](#i3-fix-resolution-checklist) | Resolution status for all 6 I2 adversary gate fixes |

---

## Status

**PROPOSED**

Per P-020 (user authority), this ADR remains PROPOSED until explicit user approval.

---

## L0: Executive Summary

The Jerry Framework enforces behavioral constraints through a five-layer architecture (L1 through L5). The most critical protection mechanism is L2 re-injection: HTML comment markers embedded in rule files that are re-injected into every prompt, making critical constraints immune to context compaction — the process where an LLM provider summarizes and discards earlier context to free up the context window. When context compaction occurs, any constraint that exists only in session-start rules (L1) may be silently dropped. The constraint is not violated — it simply ceases to exist in the model's working memory.

This ADR addresses a documented failure mode: 5 of 25 HARD rules (the "Tier B" rules: H-04, H-16, H-17, H-18, H-32) have no L2 re-injection protection. They rely entirely on compensating controls — hooks, skill enforcement, and CI workflows — that are deterministic but external to the LLM's context window. If those compensating controls fail to trigger (for example, if a skill is not invoked), the Tier B rules have no in-context defense against compaction loss.

This ADR makes three decisions:

1. **PG-004 testing requirement (unconditional):** All constraint-bearing artifacts MUST be tested for context compaction survival. This is warranted regardless of negative vs. positive framing — if a constraint can be lost, testing for that loss is prudent engineering regardless of how the constraint is worded. The evidence base is failure mode logic, not framing superiority claims.

2. **NPT-012 L2-REINJECT additions for Tier B HARD rules (timing conditional):** Add L2-REINJECT markers for 2 of the 5 Tier B rules (H-04 and H-32) now, where the compensating controls have the widest failure windows. The remaining 3 (H-16, H-17, H-18) are deferred pending DEC-005 effectiveness measurement because their compensating controls are tightly coupled to skill invocation and are therefore more reliable. This decision is framing-independent — L2 markers improve enforcement reliability regardless of constraint vocabulary. The ~180-token L2 budget headroom (confirmed by TASK-012) accommodates both additions.

3. **T-004 failure mode documentation (unconditional):** All constraint-bearing templates MUST document what happens when the template's constraints are lost during context compaction. This is a documentation standard, not a framing choice — it addresses the gap identified as WT-GAP-005 across 4 of 5 Phase 4 analyses.

---

## Context

### The Problem

The Jerry Framework's behavioral enforcement relies on constraints written into rule files, skill definitions, agent definitions, and templates. These constraints are loaded at various points during a session:

```
.context/rules/ (L1: session start, L2: per-prompt re-injection)
    |
    +--> skills/*/SKILL.md (L1: session start, no L2)
    |        |
    |        +--> skills/*/agents/*.md (Tier 2: loaded at agent invocation)
    |
    +--> .context/templates/ (instantiation-time, no L2)
```

**Context compaction** is the process where an LLM provider (Anthropic, OpenAI, etc.) summarizes and discards earlier parts of the conversation to free context window capacity. This is not under the framework's control — it is a provider-level operation that occurs transparently when the context window fills.

**The failure mode (T-004):** When context compaction occurs, L1-only constraints may be summarized away. The compaction algorithm has no knowledge of which text is a behavioral constraint versus general conversation. Constraints that appeared early in the session (at L1 load time) are the most vulnerable because they are the oldest content in the window.

**L2 re-injection** mitigates this by re-inserting critical constraints via HTML comment markers on every prompt. Because they are re-inserted per-prompt, they always appear as recent content and are therefore the last to be compacted. This makes L2-protected constraints functionally immune to compaction loss.

**The gap:** 5 of 25 HARD rules lack L2 protection. They are classified as "Tier B" in quality-enforcement.md and rely on compensating controls (hooks, skills, CI gates). These compensating controls are deterministic — they work correctly when triggered. But they require specific conditions to trigger (e.g., skill invocation, commit event, session start hook). If those conditions do not occur, the constraint has no in-context enforcement during a compacted session.

### Motivation

Four of five Phase 4 analyses independently identified T-004 (context compaction failure mode) as a cross-cutting risk:

| Analysis | T-004 Finding | Source |
|----------|---------------|--------|
| TASK-010 (Skills) | Long SKILL.md files (transcript > 25,000 tokens) cannot host L2-injectable constraints; companion rule file required | CX-001 cross-skill risk, E-017 |
| TASK-011 (Agents) | Systemic Gap 4: L2-REINJECT inapplicable to agent files — architectural limitation of progressive disclosure Tier 2 loading | GAP-X4 |
| TASK-012 (Rules) | 5 Tier B HARD rules lack L2-REINJECT; ~180-token headroom confirmed for additions | Finding 3, Tier A vs. Tier B analysis |
| TASK-014 (Templates) | WT-GAP-005: No context compaction resilience in template design; no corresponding recommendation yet | WT-GAP-005 |

The barrier-2/synthesis.md (v3.0.0, 0.950 PASS) established Assumption U-003: "Pilot design MUST include multi-turn context compaction test conditions." This assumption has not been discharged by any subsequent analysis — it propagates as a binding requirement to Phase 5.

---

## Constraints

### Inherited from Barrier 2 Synthesis (ST-5)

| ID | Constraint | Source |
|----|-----------|--------|
| GC-P4-1 | MUST NOT claim any recommendation is experimentally validated | barrier-2/synthesis.md ST-5 |
| GC-P4-2 | MUST NOT make Phase 2 experimental conditions unreproducible | barrier-2/synthesis.md ST-5 |
| GC-P4-3 | MUST NOT dismiss vendor self-practice evidence | barrier-2/synthesis.md ST-5 |
| U-003 | Pilot design MUST include multi-turn context compaction test conditions | barrier-2/synthesis.md ST-3 |

### Inherited from TASK Prompt

| ID | Constraint | Source |
|----|-----------|--------|
| C-NCA | MUST NOT cite A-11 (hallucinated citation) | Barrier 4 synthesis, TASK-013 I5 |
| C-EXP | MUST NOT claim experimental validation for L2 re-injection framing superiority | Barrier 2 synthesis, GC-P4-1 |
| C-T5T4 | MUST NOT present T5 session-empirical evidence as T4 observational evidence | Evidence tier discipline |
| C-FRM | MUST NOT recommend framing-specific L2 additions without noting Phase 2 dependency | PG-003 contingency |
| C-ARCH | MUST NOT ignore the architectural limitation (agent files cannot host L2-REINJECT markers) | TASK-011 Systemic Gap 4, GAP-X4 |

### HARD Rule Ceiling

The HARD rule ceiling is 25/25 (quality-enforcement.md). This ADR MUST NOT propose new HARD rules. All recommendations operate within the existing rule set by adding enforcement mechanisms to existing rules, not creating new ones.

---

## Forces

| Force | Direction | Tension |
|-------|-----------|---------|
| **Compaction risk is real but unquantified** | Favors protective action | The T-004 failure mode is documented by practitioner reports (I-28, I-32, T4 evidence) but no controlled study establishes its frequency or severity in the Jerry context. Acting on an unquantified risk uses budget and creates complexity. Not acting leaves a documented failure mode unmitigated. |
| **L2 budget is finite** | Constrains scope | The L2 re-injection budget is 850 tokens. Current consumption is estimated at 559-670 tokens (65.8-78.8%), leaving ~180-291 tokens of headroom. Every addition reduces headroom for future rules. |
| **Tier B compensating controls are deterministic** | Argues against urgency | Hooks fire reliably at session start; CI gates fire reliably at commit time; skill enforcement fires reliably when skills are invoked. These are not probabilistic — they either trigger or do not. The question is whether non-triggering scenarios are operationally significant. |
| **Phase 2 has not established framing directionality** | Constrains framing-specific claims | Whether the L2 markers should use NEVER/MUST NOT vocabulary (negative framing) versus MUST/REQUIRED vocabulary (positive framing) is an open research question. Adding L2 markers is framing-independent; choosing the vocabulary for those markers is framing-conditional. |
| **Template authors need compaction failure guidance now** | Favors T-004 documentation | Template authors creating new constraint-bearing templates have no guidance on what happens when context compaction drops their constraints. This gap exists regardless of Phase 2 outcomes. |

---

## Options Considered

### Option A: Full Tier B L2-REINJECT Coverage Now (All 5 Rules)

Add L2-REINJECT markers for all 5 Tier B HARD rules (H-04, H-16, H-17, H-18, H-32) immediately.

| Dimension | Assessment |
|-----------|-----------|
| Completeness | Closes the entire Tier B gap in one action |
| Token cost | ~150-250 tokens (5 markers at 30-50 tokens each); worst case: 670 + 250 = 920 tokens, exceeding 850 budget |
| Risk | Budget overflow under worst-case assumptions; reduces headroom to near-zero for future rules |
| Reversibility | HIGH — markers can be removed without side effects |
| Evidence | No T1 evidence that L2 re-injection is necessary for rules with strong compensating controls |

**Steelman (S-003):** This option maximizes defense-in-depth. Every HARD rule would have L2 protection, eliminating the Tier A/Tier B distinction entirely. The budget concern is manageable if the 559-token baseline (not the 670 worst-case) is accurate. If compensating controls ever degrade (hook removed, skill refactored), the L2 marker provides a safety net that would otherwise be absent.

**Why not chosen:** Token budget risk is unacceptable. Under worst-case assumptions (670 base + 250 new = 920 tokens), this exceeds the 850-token budget. Additionally, H-16, H-17, and H-18 are tightly coupled to /adversary skill invocation — their compensating controls fire reliably whenever the quality framework operates, which is precisely when these rules matter. Adding L2 markers for rules whose enforcement contexts already guarantee compensating control activation provides marginal benefit at significant budget cost.

### Option B: Selective Tier B L2-REINJECT (2 of 5 Rules) + PG-004 Testing + T-004 Documentation

Add L2-REINJECT markers for H-04 and H-32 only. Mandate PG-004 compaction testing for all constraint-bearing artifacts. Require T-004 failure mode documentation in templates.

| Dimension | Assessment |
|-----------|-----------|
| Completeness | Addresses the widest-failure-window Tier B rules; defers narrow-window rules to DEC-005 |
| Token cost | ~60-100 tokens (2 markers); worst case: 670 + 100 = 770 tokens, within budget |
| Risk | Leaves H-16/H-17/H-18 without L2 protection; acceptable given compensating controls |
| Reversibility | HIGH — markers removable; documentation standards persist regardless |
| Evidence | Failure mode logic (T-004) for testing requirement; budget analysis (TASK-012) for marker selection |

**Steelman (S-003):** This is the minimum effective response to T-004. It adds L2 protection where compensating controls have the widest failure windows (H-04 applies at session start only — if the hook fails, there is no subsequent trigger; H-32 applies at commit time — if no commit occurs, there is no enforcement during the session). It defers the remaining 3 rules pending DEC-005, which quality-enforcement.md already identifies as the decision gate for Tier B L2 additions.

### Option C: PG-004 Testing + T-004 Documentation Only (No L2 Additions)

Mandate compaction testing and failure mode documentation without adding any L2 markers. Defer all Tier B L2 additions to DEC-005.

| Dimension | Assessment |
|-----------|-----------|
| Completeness | Addresses testing and documentation gaps; does not address enforcement gap |
| Token cost | 0 new tokens |
| Risk | Tier B enforcement gap persists until DEC-005 resolves; no safety net for H-04/H-32 |
| Reversibility | HIGH |
| Evidence | Purely defensive; no evidence required for testing-only recommendation |

**Steelman (S-003):** This option is the most conservative. It adds zero token cost, creates zero budget risk, and defers enforcement changes to DEC-005 where they can be evaluated with effectiveness data from Phase 2. The testing requirement is unconditional and captures the most important outcome (knowing whether compaction affects constraints) without committing to a specific mitigation strategy. If Phase 2 reveals that compaction rarely occurs in typical Jerry sessions, the 0-cost approach would have been optimal.

**Why not chosen:** The gap analysis (TASK-012) established that H-04 and H-32 have the widest failure windows among Tier B rules. H-04 (active project) depends on SessionStart hook — if the hook fails or is bypassed, there is no subsequent enforcement trigger until the session ends. H-32 (GitHub Issue parity) depends on CI workflow — if no commit occurs, there is no enforcement during the session. These are not hypothetical failure windows; they are structural properties of the compensating control design. Adding 60-100 tokens of L2 protection for these two rules is a proportionate response that does not require Phase 2 completion to justify.

### Option D: Status Quo (No Action)

Take no action. Context compaction resilience is not a priority. Tier B rules continue with compensating controls only. Templates continue without compaction failure documentation.

| Dimension | Assessment |
|-----------|-----------|
| Completeness | No gaps addressed |
| Token cost | 0 |
| Risk | T-004 failure mode remains undocumented and untested; identified by 4 of 5 Phase 4 analyses |
| Reversibility | N/A |
| Evidence | N/A |

**Steelman (S-003):** The T-004 failure mode evidence is T4 LOW confidence. No Jerry session has documented a confirmed constraint loss due to context compaction. The failure mode is theoretical, drawn from practitioner reports (I-28, I-32) about other systems. Investing engineering effort in mitigating a theoretical risk with LOW confidence evidence could be premature when the framework has 130 other recommendations from Phase 4 competing for implementation bandwidth. The opportunity cost of acting on T-004 is the delay of higher-confidence, higher-impact recommendations.

**Why not chosen:** PG-004 is unconditional by failure mode logic. The confidence in T-004 as a failure mode is LOW, but the confidence that testing for it is prudent is HIGH — because the failure mode, if encountered, is silent (constraints disappear without error) and irreversible within the session (no mechanism to detect and restore dropped constraints). The asymmetry between detection cost (testing) and failure cost (silent constraint loss in production) makes inaction disproportionate even at LOW failure mode confidence.

### Options Comparison — Weighted Criteria Evaluation

The options comparison uses a five-dimension weighted-criteria framework derived from the five forces identified in the [Forces](#forces) section. Each dimension is weighted by its importance to the decision, and each option is scored 1-3 per dimension (1=poor, 2=adequate, 3=strong). The weighted composite determines the ranking.

**Weighting rationale:**

| Dimension | Weight | Force Derivation | Derivation |
|-----------|--------|------------------|------------|
| T-004 Coverage | 0.30 | Force 1 (compaction risk is real but unquantified) | Primary motivation: 4 of 5 Phase 4 analyses identified T-004 as cross-cutting risk. Highest weight because this ADR exists to address T-004. |
| Budget Safety | 0.25 | Force 2 (L2 budget is finite) | L2 budget is finite (850 tokens) and constrains all future enforcement decisions. Budget overflow is a hard failure. |
| Evidence Basis | 0.20 | Force 3 (Tier B compensating controls are deterministic) + Force 4 (Phase 2 has not established framing directionality) | Per GC-P4-1, recommendations without evidence basis carry implementation risk. Decisions grounded in failure mode logic or architectural fact are preferred over speculative mitigation. Force 3 supplies the compensating-control evidence; Force 4 constrains framing-specific claims. |
| Reversibility | 0.15 | Force 4 (Phase 2 has not established framing directionality) | Per PG-003, framing-conditional decisions must be reversible. Lower weight because all options score well on reversibility — this dimension differentiates poorly, reducing its discriminating value. |
| Implementation Cost | 0.10 | Force 5 (template authors need compaction failure guidance now) | Lowest weight: implementation effort is a one-time cost; the other dimensions have ongoing architectural impact. Force 5's urgency ("now") reduces the weight of implementation cost — delaying for cost reasons contradicts the urgency. |

**Weight derivation note:** The weight magnitudes (0.30, 0.25, 0.20, 0.15, 0.10) are architect judgment within the stated Force-to-Dimension mapping, not mechanically derived (e.g., via AHP pairwise comparison). The ordering rationale is: (1) T-004 Coverage is highest because the ADR exists to address T-004; (2) Budget Safety is second because budget overflow is a hard constraint, not a preference; (3) Evidence Basis is third because GC-P4-1 makes evidence grounding a binding constraint; (4) Reversibility is fourth because all options score well on it, reducing discriminating power; (5) Implementation Cost is lowest because it is a one-time cost with no ongoing architectural impact. Sensitivity: reasonable alternative weights (e.g., T-004 Coverage at 0.25-0.35, Budget Safety at 0.20-0.30) do not change the B > C ranking because Option B scores 3 on four of five dimensions — only a weight shift that simultaneously penalizes Budget Safety and Evidence Basis below 0.15 each could change the ranking, which would contradict the force analysis.

**Per-dimension scoring:**

| Dimension (Weight) | A: All 5 Tier B | B: Selective 2/5 | C: Testing + Docs Only | D: Status Quo |
|---------------------|-----------------|-------------------|------------------------|---------------|
| T-004 Coverage (0.30) | 3 (all Tier B + testing + docs) [1] | 3 (widest-window rules + testing + docs) [1] | 2 (testing + docs but no enforcement improvement) | 1 (no action) |
| Budget Safety (0.25) | 1 (worst-case 920/850 = overflow) | 3 (worst-case 745/850 = safe) | 3 (0 new tokens) | 3 (0 new tokens) |
| Evidence Basis (0.20) | 2 (strong for H-04/H-32; weak for H-16/H-17/H-18 — narrow-window rules lack evidence that L2 adds value over tightly-coupled compensating controls) | 3 (failure-window analysis distinguishes wide from narrow; selective action matches evidence strength) | 2 (testing is unconditional; deferral of enforcement lacks justification when budget allows action) | 1 (ignores 4/5 Phase 4 convergence) |
| Reversibility (0.15) | 3 (markers removable) | 3 (markers removable; docs persist regardless) | 3 (no enforcement change to reverse) | 3 (N/A) |
| Implementation Cost (0.10) | 1 (5 markers + testing + docs; highest effort) | 2 (2 markers + testing + docs; moderate effort) | 3 (testing + docs only; lowest effort) | 3 (zero effort) |

**Composite scores:**

| Option | Calculation | Composite | Rank |
|--------|-------------|-----------|------|
| A: All 5 Tier B | (3x0.30)+(1x0.25)+(2x0.20)+(3x0.15)+(1x0.10) | 0.90+0.25+0.40+0.45+0.10 = **2.10** | 3 |
| **B: Selective 2/5** | **(3x0.30)+(3x0.25)+(3x0.20)+(3x0.15)+(2x0.10)** | **0.90+0.75+0.60+0.45+0.20 = 2.90** | **1** |
| C: Testing + Docs Only | (2x0.30)+(3x0.25)+(2x0.20)+(3x0.15)+(3x0.10) | 0.60+0.75+0.40+0.45+0.30 = **2.50** | 2 |
| D: Status Quo | (1x0.30)+(3x0.25)+(1x0.20)+(3x0.15)+(3x0.10) | 0.30+0.75+0.20+0.45+0.30 = **2.00** | 4 |

**[1] T-004 Coverage scoring note (Options A and B parity):** Both Options A and B score 3 on T-004 Coverage because the dimension measures coverage of the *widest-failure-window* rules — the rules where compaction loss poses the greatest risk. Option A covers all 5 Tier B rules; Option B covers only H-04 and H-32. However, the 3 additional rules in Option A (H-16, H-17, H-18) have narrow failure windows: their compensating controls fire precisely when the rules matter (during adversary skill invocation). Covering narrow-window rules provides marginal T-004 risk reduction because those rules are already well-protected in their enforcement contexts. The T-004 Coverage dimension rewards coverage of the highest-risk rules, not total Tier B count — hence the parity.

**Chosen: Option B (composite 2.90/3.00)** — Selective Tier B L2-REINJECT (H-04, H-32) + PG-004 mandatory testing + T-004 failure mode documentation. Option B dominates because it scores 3 on four of five dimensions (T-004 Coverage, Budget Safety, Evidence Basis, Reversibility), losing only to Option C on Implementation Cost — a dimension with the lowest weight (0.10). Option C ranks second (2.50) but scores only 2 on T-004 Coverage and Evidence Basis because it defers enforcement improvement despite budget availability and evidence supporting selective action.

---

## Decision

This ADR decides three things. Each is assessed independently for its relationship to framing evidence.

### Decision 1: PG-004 Compaction Testing Requirement (Unconditional)

**All constraint-bearing artifacts MUST be tested for context compaction survival before deployment.**

This is unconditional — it does not depend on Phase 2 experimental outcomes or framing directionality findings. The rationale is failure mode logic: if a constraint can be silently lost during context compaction, testing for that loss is warranted regardless of how the constraint is worded (negative framing, positive framing, or structured alternatives). The testing requirement applies to:

- Rule files with L2-REINJECT markers (verify markers survive compaction)
- Rule files without L2-REINJECT markers (verify compensating controls fire)
- SKILL.md files with behavioral constraints (verify constraints survive L1 compaction)
- Agent definition files with guardrails (verify guardrails survive Tier 2 loading under compaction)
- Templates with creation constraints (verify constraints are present at instantiation time)

**Evidence basis:** T-004 failure mode (T4 LOW for directional reversal; unconditional by failure mode logic); PG-004 from barrier-2/synthesis.md ST-4; U-003 from barrier-2/synthesis.md ST-3.

**What this does NOT decide:** The specific test methodology, pass/fail thresholds, or test automation approach. These are implementation details for the pilot design that Phase 2 U-003 conditions will inform.

### Decision 2: NPT-012 L2-REINJECT Additions for H-04 and H-32 (Timing Conditional)

**Add L2-REINJECT markers for H-04 (active project REQUIRED) and H-32 (GitHub Issue parity).**

These two rules are selected from the 5 Tier B HARD rules because their compensating controls have the widest failure windows:

| Rule | Compensating Control | Failure Window |
|------|---------------------|----------------|
| **H-04** | SessionStart hook | If hook fails/bypasses, NO subsequent enforcement trigger exists until session end. Window = entire session. |
| **H-32** | /worktracker skill + CI workflow | If no commit occurs and /worktracker is not invoked, NO enforcement occurs. Window = entire session without commit. |
| H-16 | /adversary skill | Fires whenever adversary skill is invoked — which is precisely when H-16 matters. Window = narrow (non-adversarial work only). |
| H-17 | /adversary + /problem-solving | Fires whenever quality scoring is invoked — which is precisely when H-17 matters. Window = narrow. |
| H-18 | S-007 in /adversary | Fires whenever constitutional compliance is checked — which is precisely when H-18 matters. Window = narrow. |

The L2 additions are framing-independent — they improve enforcement reliability regardless of whether the marker content uses NEVER/MUST NOT vocabulary or MUST/REQUIRED vocabulary. The vocabulary choice for marker content is a separate decision that SHOULD await Phase 2 framing directionality data if the content will include prohibitive language beyond what already exists.

**Token budget arithmetic:**

| Component | Tokens | Source |
|-----------|--------|--------|
| Current L2 consumption (stated) | 559 | quality-enforcement.md |
| Current L2 consumption (estimated from audit) | ~670 | TASK-012 content audit |
| H-04 marker (estimated) | ~35 | "Active project REQUIRED. MUST NOT proceed without JERRY_PROJECT set. Consequence: session produces out-of-scope work." |
| H-32 marker (estimated) | ~40 | "GitHub Issue parity REQUIRED for jerry repo work items. MUST NOT close worktracker entity without corresponding GitHub Issue update. Consequence: external collaboration surface desyncs." |
| **Worst-case total** | **~745** | 670 + 35 + 40 |
| **Budget** | **850** | quality-enforcement.md |
| **Remaining headroom** | **~105** | 850 - 745 |

Under stated-baseline assumptions: 559 + 35 + 40 = 634 tokens (74.6% utilization, 216 tokens headroom).
Under worst-case assumptions: 670 + 35 + 40 = 745 tokens (87.6% utilization, 105 tokens headroom).

Both scenarios are within budget. The 559 vs. 670 discrepancy (documented in TASK-012) MUST be resolved before implementation by performing an exact token count of all current L2-REINJECT marker content.

**Deferred rules (H-16, H-17, H-18):** These remain Tier B pending DEC-005 effectiveness measurement, as documented in quality-enforcement.md. Their narrow failure windows (compensating controls fire precisely when the rule matters) make L2 addition lower priority. If DEC-005 determines that L2 markers provide measurable improvement for narrow-window rules, a follow-up ADR should add them within the remaining headroom.

**Evidence basis:** TASK-012 Finding 3 (token budget analysis); TASK-012 Tier A vs. Tier B analysis; quality-enforcement.md Two-Tier Enforcement Model and DEC-005 note.

### Decision 3: T-004 Failure Mode Documentation Requirement (Unconditional)

**All constraint-bearing templates MUST document what happens when the template's constraints are lost during context compaction.**

This addresses WT-GAP-005 from TASK-014, which identified that no entity template includes context compaction failure mode documentation. The documentation requirement is a new section in constraint-bearing templates that answers:

1. Which constraints in this template are vulnerable to context compaction?
2. What is the failure mode if those constraints are lost? (What goes wrong?)
3. What compensating controls exist? (L2 markers, hooks, CI gates, skill enforcement)
4. What is the detection mechanism? (How do you know the constraint was lost?)

This is unconditional — it does not depend on framing directionality. It is a documentation standard that improves operational awareness regardless of constraint vocabulary.

**Evidence basis:** TASK-014 WT-GAP-005; TASK-010 CX-001 (T-004 cross-skill risk); GAP-X2 (4 of 5 Phase 4 analyses identified this gap).

---

## L1: Technical Implementation

### Decision 1 Implementation: PG-004 Compaction Testing

**Testing approach (MEDIUM — implementer discretion with documented justification):**

A compaction survival test verifies that a constraint remains in-context after a simulated compaction event. The test structure is:

```
1. Load artifact (rule file, SKILL.md, agent definition, or template)
2. Simulate context fill (add sufficient content to trigger compaction)
3. Verify constraint presence after compaction
4. For L2-protected constraints: verify re-injection restores constraint
5. For non-L2 constraints: verify compensating control fires
```

**Vulnerability assessment framework:**

The per-artifact vulnerability levels (LOW, LOW-MEDIUM, MEDIUM) are derived from two factors: (1) the enforcement layer that protects the artifact's constraints, and (2) the temporal exposure window during which compaction could affect the artifact. The framework is defined below so that vulnerability assignments are reproducible.

| Vulnerability Level | Enforcement Layer | Temporal Exposure | Compaction Behavior |
|--------------------|--------------------|-------------------|---------------------|
| **LOW** | L2 per-prompt re-injection | None — constraint is re-inserted every prompt | Constraint is the *last* content to be compacted because it is always recent. Functionally immune to compaction under the current L2 architecture. |
| **LOW-MEDIUM** | Tier 2 (loaded at agent invocation) | Partial — constraint is loaded mid-session when the agent is invoked, so it is not the oldest content; however, it is not re-injected per-prompt | Constraint is newer than L1 content but older than L2 content. Vulnerable if the agent session itself triggers compaction, but less exposed than L1-only content because it enters the context window later. |
| **MEDIUM** | L1 session-start only, or instantiation-time | Full session — constraint is loaded once at session start (L1) or at template instantiation, then ages as context grows | Constraint is among the oldest content in the context window. First candidate for summarization during compaction. No re-injection mechanism restores it. |

**Per-artifact-type test conditions:**

| Artifact Type | Compaction Vulnerability | Vulnerability Derivation | Test Condition | Pass Criterion |
|---------------|------------------------|--------------------------|----------------|----------------|
| Rule files with L2 markers | LOW | L2 per-prompt re-injection; zero temporal exposure | Verify marker content present after simulated compaction | Marker content re-injected on next prompt |
| Rule files without L2 markers | MEDIUM | L1 session-start only; full-session temporal exposure; compensating controls may not trigger | Verify rule content present after extended multi-turn session | Compensating control fires when rule condition occurs |
| SKILL.md files | MEDIUM | L1 session-start only; SKILL.md is loaded at session start and not re-injected; full-session exposure | Verify constraints present after context fill | Constraint present in routing context |
| Agent definition files | LOW-MEDIUM | Tier 2 loaded at invocation; partial exposure (enters context mid-session, not at start) | Verify guardrails active after compaction during agent session | Guardrail violation detected and blocked |
| Templates | MEDIUM | Instantiation-time only; constraint text present at template creation but not re-injected; ages from point of instantiation | Verify creation constraints present when template is instantiated in a compacted session | Constraint text present in instantiated template |

**U-003 alignment:** The pilot design per barrier-2/synthesis.md MUST include multi-turn context compaction test conditions. These tests SHOULD be integrated into the Phase 2 pilot as multi-turn conditions (C7 equivalent or supplemental conditions) rather than run as a separate test suite.

#### Minimum Viable Manual Test Protocol (Interim)

Until Phase 2 automated tooling is available, the following 5-step manual protocol provides interim PG-004 coverage. This protocol is designed for a single practitioner testing a single constraint-bearing artifact per session. It will be superseded by the Phase 2 pilot test automation when available.

**Executor:** The implementer assigned to this ADR (role: framework maintainer or CI engineer). This is the same role as the Decision 2 implementation gate owner — both the token count resolution (Decision 2 gate) and the compaction testing (this protocol) SHOULD be performed by the same person before marking Decision 1 and Decision 2 complete.

| Step | Action | Duration | Output |
|------|--------|----------|--------|
| 1. Select artifact | Choose one constraint-bearing artifact (rule file, SKILL.md, agent definition, or template). Identify the specific constraints it contains by searching for MUST, MUST NOT, NEVER, REQUIRED, FORBIDDEN vocabulary. Record constraint count and text. | ~5 min | Constraint inventory for the artifact |
| 2. Establish baseline | In a fresh Claude Code session, load the artifact. Immediately ask the model to list all behavioral constraints it has received. Record the response as the baseline constraint set. | ~5 min | Baseline constraint set (expected = constraint inventory from Step 1) |
| 3. Simulate context fill | Continue the session with 15-20 substantive multi-turn exchanges (code review, analysis, research) designed to fill the context window until context usage exceeds 70% (approximately 140K tokens in a 200K-token window, corresponding to the AE-006b WARNING tier threshold). The exchanges should be on-topic for the project but unrelated to the constraints being tested. The goal is to push the constraint-bearing content toward the oldest portion of the context window. Track context usage via provider surface if available (e.g., Claude Code token counter). | ~30 min | Session with context fill at or above 70% (AE-006b WARNING tier) |
| 4. Post-fill constraint check | After the multi-turn exchanges, ask the model to list all behavioral constraints it is currently following. Compare the response to the baseline from Step 2. Record which constraints are present, absent, or partially recalled. | ~5 min | Post-fill constraint set; delta from baseline |
| 5. Document results | Record in a standard format: artifact tested, constraint count, constraints present at baseline, constraints present after fill, constraints lost, L2 marker status (present/absent), compensating control status (fires/does not fire in this scenario). File at `projects/{PROJECT}/research/pg004-manual-test-{artifact-slug}.md`. | ~10 min | Test result file |

**Pass criterion:** All L2-protected constraints are present after Step 4 (L2 re-injection restores them). For non-L2 constraints, the test documents the loss rate — there is no pass/fail for non-L2 constraints at this stage because the expected behavior (L1 content may be summarized away) is the failure mode being characterized, not a defect to prevent.

**Scope:** This interim protocol is sufficient for characterizing the T-004 failure mode frequency. It is deliberately manual and lightweight. The Phase 2 pilot SHOULD replace it with automated tooling that can test systematically across multiple artifacts and session lengths.

**Limitation:** Manual testing cannot control or observe the compaction algorithm directly (it is provider-internal). The protocol detects the *effect* of compaction (constraint loss) but cannot measure *when* compaction occurs. Phase 2 automated tooling may be able to infer compaction timing from token usage metrics if the provider exposes them.

### Decision 2 Implementation: L2-REINJECT Marker Content

**H-04 marker (to be added to project-workflow.md or quality-enforcement.md):**

```html
<!-- L2-REINJECT: rank=11, content="Active project REQUIRED (H-04). MUST NOT proceed without JERRY_PROJECT set. Consequence: session produces out-of-scope work; worktracker entities created in wrong project." -->
```

Estimated tokens: ~35
Placement: project-workflow.md (where H-04 is referenced) or quality-enforcement.md (where the HARD rule index lives). Recommendation: quality-enforcement.md, to maintain L2-REINJECT marker concentration in the governance SSOT.
Rank: 11 — see [L2-REINJECT Rank Justification](#l2-reinject-rank-justification) below for derivation relative to existing rank ordering.

**H-32 marker (to be added to project-workflow.md):**

```html
<!-- L2-REINJECT: rank=12, content="GitHub Issue parity REQUIRED for jerry repo work items (H-32). MUST NOT close worktracker entity without corresponding GitHub Issue update. Consequence: external collaboration surface desyncs from internal tracking." -->
```

Estimated tokens: ~40
Placement: project-workflow.md (where H-32 is defined).
Rank: 12 — see [L2-REINJECT Rank Justification](#l2-reinject-rank-justification) below for derivation relative to existing rank ordering.

**Vocabulary note:** The marker content above uses MUST NOT vocabulary (negative framing) because: (a) this is consistent with existing L2-REINJECT markers that use NEVER/MUST NOT vocabulary (5 of 11 files per TASK-012 finding); (b) quality-enforcement.md defines HARD tier vocabulary as including "MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL" — the markers use vocabulary appropriate to HARD tier. If Phase 2 finds a null framing effect for negative vs. positive vocabulary, the marker content vocabulary is trivially revisable without changing the enforcement mechanism. The markers themselves (as enforcement mechanism) are framing-independent.

**Implementation Gate (BLOCKING):**

> Decision 2 implementation is BLOCKED pending completion of the token discrepancy resolution task defined below. Steps 2-6 of the implementation sequence MUST NOT proceed until Step 1 produces an exact figure and the budget arithmetic is re-verified.

| Gate Field | Value |
|------------|-------|
| **Blocker** | 559 vs. ~670 token discrepancy for current L2-REINJECT consumption |
| **Owner** | The implementer assigned to this ADR (role: framework maintainer or CI engineer) |
| **Procedure** | Extract all L2-REINJECT marker `content=` field values from all `.context/rules/` files. Concatenate them. Count tokens using a known tokenizer (cl100k_base for Anthropic models, or the tokenizer documented in the enforcement architecture). Record the exact count. |
| **Verification** | The exact count MUST be recorded in this section (replace the placeholder below) before proceeding. If the exact count exceeds 750 tokens, the H-32 marker addition (Step 3) MUST be re-evaluated for budget safety — the H-04 marker (Step 2) takes priority because H-04 has the wider failure window. |
| **Deadline** | Before any implementation step begins. No calendar deadline — this is a sequencing gate, not a time-boxed task. |
| **Output** | Update the token budget table in Decision 2 with: `Exact current L2 consumption: [PENDING — replace with exact count]` |

**Exact current L2 consumption: [PENDING — replace with exact count before proceeding]**

**Implementation sequence:**

1. **[GATE]** Resolve the 559 vs. ~670 token discrepancy by exact counting of all current L2-REINJECT content (see Implementation Gate above)
2. Add H-04 marker to quality-enforcement.md with rank=11
3. Add H-32 marker to project-workflow.md with rank=12
4. Update quality-enforcement.md Tier A table to include H-04 and H-32 (move from Tier B to Tier A)
5. Update quality-enforcement.md Tier B table to remove H-04 and H-32 (3 remaining: H-16, H-17, H-18)
6. Update Tier A count: 20 -> 22; Tier B count: 5 -> 3

#### L2-REINJECT Rank Justification

The existing L2-REINJECT rank ordering (ranks 1-10) follows a priority principle: lower rank numbers indicate higher re-injection priority, meaning the content is more critical to behavioral compliance and more likely to be needed on every prompt. The table below shows the current rank assignments and the rationale for placing H-04 at rank=11 and H-32 at rank=12.

| Rank | Rule/Topic | File | Priority Rationale |
|------|-----------|------|--------------------|
| 1 | Constitutional triplet (P-003, P-020, P-022) | quality-enforcement.md | Highest priority: foundational governance constraints that apply to every agent action |
| 2 | Quality gate (H-13, H-14) + Ambiguity resolution (H-31) | quality-enforcement.md | Core quality framework: threshold, iteration cycle, and clarification behavior |
| 3 | UV Python environment (H-05) | quality-enforcement.md, python-environment.md | Environmental constraint: wrong toolchain corrupts execution environment |
| 4 | Architecture layer isolation (H-07, H-10) + LLM-as-Judge (S-014) | quality-enforcement.md, architecture-standards.md | Structural: code organization and scoring methodology |
| 5 | Self-review (H-15) + Agent definitions (H-34) + Testing (H-20) | quality-enforcement.md, agent-development-standards.md, testing-standards.md | Process: pre-output review, agent schema, test-first |
| 6 | Criticality levels + Routing (H-36) + Skill invocation (H-22) | quality-enforcement.md, agent-routing-standards.md, mandatory-skill-usage.md | Operational: classification, routing, and skill triggering |
| 7 | Markdown navigation (H-23) + Coding standards (H-11) + Skill standards (H-25, H-26) | markdown-navigation-standards.md, coding-standards.md, skill-standards.md | Standards: document structure, code style, skill conventions |
| 8 | Governance escalation (H-19) | quality-enforcement.md | Governance: auto-escalation triggers |
| 9 | AE-006 graduated escalation + MCP tools | quality-enforcement.md, mcp-tool-standards.md | Context management and external tool governance |
| 10 | AST-based parsing (H-33) | quality-enforcement.md | Worktracker entity operations: structural parsing |
| **11 (NEW)** | **Active project (H-04)** | **quality-enforcement.md** | **Session-scoping constraint. Placed after rank 10 because: (a) H-04 applies at session boundaries, not within every prompt's decision space — unlike ranks 1-10, which govern in-prompt behavior; (b) H-04's primary enforcement is the SessionStart hook (deterministic L3), so the L2 marker is a defense-in-depth backup, not the primary mechanism; (c) H-04 is a precondition for work, not a behavioral constraint during work — it is categorically different from constraints that guide reasoning quality (ranks 1-5) or operational patterns (ranks 6-10).** |
| **12 (NEW)** | **GitHub Issue parity (H-32)** | **project-workflow.md** | **Scoped to jerry repository only. Placed at lowest rank because: (a) H-32 applies only when working in the `geekatron/jerry` repository, not universally — making it the narrowest-scope L2 marker; (b) its primary enforcement is the CI workflow (deterministic L5) and /worktracker skill (L3), both of which are more reliable than L2 for this specific rule; (c) compared to H-04 (rank=11), H-32 has a narrower applicability scope (one repository vs. all sessions) and an additional compensating control (CI gate), justifying lower priority.** |

**Priority ordering principle:** Ranks 1-5 govern reasoning and quality behavior (applicable to every output). Ranks 6-10 govern operational patterns and specialized workflows. Ranks 11-12 govern session/repository scoping — preconditions and environmental constraints rather than behavioral constraints.

### Decision 3 Implementation: T-004 Failure Mode Documentation

**Template section to add (MEDIUM — recommended format, adaptable per template type):**

```markdown
## Context Compaction Resilience

| Constraint | Vulnerability | Failure Mode | Compensating Control | Detection |
|-----------|--------------|-------------|---------------------|-----------|
| {constraint text} | {L1-only / L2-protected / Tier 2} | {what goes wrong} | {hook / skill / CI / L2 marker} | {how to detect loss} |
```

**Applicable templates (per TASK-014 WT-GAP-005):**

- All worktracker entity templates (EPIC.md, FEATURE.md, STORY.md, TASK.md, BUG.md, ENABLER.md) — embed creation constraint (WTI-007) compaction failure mode
- Adversarial strategy templates (TEMPLATE-FORMAT.md, s-*.md) — document SSOT protection constraint compaction behavior
- ADR template — document consequence documentation constraint compaction behavior
- Requirements templates — document V&V constraint compaction behavior

**What this does NOT require:** Retrofitting every existing template immediately. The documentation requirement applies to new and modified templates. Existing templates SHOULD be updated as part of their next modification cycle.

---

## L2: Architectural Implications

### Implication 1: The Tier A/Tier B Distinction Narrows But Persists

After implementing Decision 2, the Tier A/Tier B distribution shifts:

| | Before | After |
|---|--------|-------|
| Tier A (L2-protected) | 20 rules | 22 rules |
| Tier B (compensating controls only) | 5 rules | 3 rules |
| L2 budget utilization (worst case) | ~670/850 (78.8%) | ~745/850 (87.6%) |

The remaining Tier B rules (H-16, H-17, H-18) are architecturally different from H-04 and H-32: their compensating controls are co-located with their enforcement contexts (adversary skill invocation). This is a structurally stronger position than H-04/H-32, where the compensating control (hook, CI) and the enforcement context (any session activity) are temporally separated.

**Long-term path:** If DEC-005 determines that L2 markers measurably improve enforcement for narrow-window rules, H-16/H-17/H-18 can be added within the remaining ~105-token headroom (estimated ~90-120 tokens for 3 markers at 30-40 tokens each). This would exhaust the L2 budget to ~93-100% utilization, which is operationally acceptable but leaves zero headroom for new HARD rules. Given the 25/25 HARD rule ceiling, zero headroom is consistent — there is no capacity for new rules regardless.

### Implication 2: The Architectural Limitation (GAP-X4) Remains

This ADR does NOT address GAP-X4 (L2-REINJECT inapplicable to agent files). Agent definition files are loaded at agent invocation (Tier 2 progressive disclosure), not via the per-prompt L2 mechanism. Applying L2-REINJECT to agent files would require architectural changes to the Claude Code runtime, which is outside the Jerry Framework's control.

**Mitigation within current architecture:** Critical agent-level constraints that must survive compaction SHOULD be expressed in companion rule files (Tier A, L2-injectable) rather than exclusively in agent definition files (Tier 2). The TASK-010 finding that long SKILL.md files cannot host L2-injectable constraints reinforces this — the companion rule file pattern is the architecturally correct solution within the current enforcement model.

### Implication 3: PG-004 Testing Creates a New Quality Gate Dimension

Compaction survival testing introduces a new dimension to the quality framework. Currently, quality is assessed along 6 dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability). Compaction resilience is not a scoring dimension — it is a binary pre-deployment gate:

- **PASS:** Constraint survives simulated compaction event (L2 re-injection restores it, or compensating control fires, or constraint is present at Tier 2 load time)
- **FAIL:** Constraint is lost after simulated compaction with no recovery mechanism

This gate operates at L5 (commit/CI) for rule file changes, and as a manual test protocol for skill/agent/template changes until automated compaction simulation tooling exists.

### Implication 4: The Constraint Propagation Hierarchy Is Now Explicit

This ADR, combined with the barrier-4 synthesis L2 strategic analysis, makes the constraint propagation hierarchy an explicit architectural property:

```
Layer 5: CI/commit gates (immune to compaction, post-hoc)
Layer 4: Post-tool output inspection (partially immune)
Layer 3: Pre-tool deterministic gates (immune, AST-based)
Layer 2: Per-prompt re-injection (immune, HTML comments)
Layer 1: Session-start rules (VULNERABLE to compaction)
Tier 2: Agent invocation loading (VULNERABLE if compaction occurs mid-agent)
```

Constraints MUST be placed at the highest immune layer that can host them. The PG-004 testing requirement ensures that placement decisions are validated, not assumed.

---

## Consequences

### Positive

1. **Silent constraint loss becomes detectable.** PG-004 testing transforms T-004 from "documented but untested failure mode" to "tested and characterized failure mode." Even a negative test result (constraints survive compaction in all tested scenarios) is valuable — it reduces the T-004 risk from "unknown frequency" to "not observed under conditions X."

2. **Widest-failure-window Tier B rules gain L2 protection.** H-04 and H-32 move from compensating-controls-only to L2+compensating-controls defense-in-depth. This is particularly significant for H-04 (active project) because the SessionStart hook is the only compensating control and it fires once.

3. **Template authors receive compaction failure guidance.** The T-004 documentation requirement gives template authors a structured framework for reasoning about compaction risks, rather than hoping they never encounter one.

4. **L2 budget utilization is explicitly tracked.** The token arithmetic in this ADR establishes a precedent for documenting L2 budget impact of any enforcement change.

### Negative

1. **L2 budget headroom decreases from ~180 to ~105 tokens (worst case).** This reduces capacity for future L2 additions. If additional L2-REINJECT needs arise (e.g., DEC-005 concludes H-16/H-17/H-18 should be promoted), the budget becomes extremely tight (~15 tokens remaining after all 5 Tier B rules). This constrains future enforcement architecture decisions.

2. **Testing overhead increases.** PG-004 compaction testing adds a new test category that does not currently exist. Until automated tooling is available, these tests require manual execution, which is time-consuming and may not be performed consistently. The risk is that the testing requirement becomes a documented-but-unenforced standard.

3. **Template documentation complexity increases.** Adding a "Context Compaction Resilience" section to every constraint-bearing template increases template length and maintenance burden. Template authors may view this as bureaucratic overhead for a theoretical failure mode.

4. **The 559 vs. 670 token discrepancy must be resolved before implementation.** This creates a blocking dependency — the L2 additions cannot be safely implemented until the actual current consumption is determined by exact counting. If the true consumption is higher than 670, the budget arithmetic changes and H-32 may need to be deferred.

### Neutral

1. **DEC-005 dependency remains open.** This ADR does not resolve DEC-005 (Tier B L2 effectiveness measurement). The remaining 3 Tier B rules (H-16, H-17, H-18) continue to await DEC-005 disposition. This ADR partially addresses the Tier B gap but does not close it.

2. **Phase 2 experimental conditions are preserved.** This ADR does not modify the content of any existing L2-REINJECT marker. It adds two new markers and a testing/documentation standard. No Phase 2 experimental condition (C1-C7) is affected by these changes. The positive-framing reference files (markdown-navigation-standards.md, mcp-tool-standards.md) are not touched.

3. **Framing-specific vocabulary choices are deferred.** The L2 marker content uses existing HARD tier vocabulary (MUST NOT). If Phase 2 establishes framing directionality, marker content vocabulary can be revised without changing the enforcement mechanism. This is a trivially reversible vocabulary choice, not an architectural decision.

---

## Risks

| Risk ID | Risk | Probability | Severity | Mitigation |
|---------|------|-------------|----------|------------|
| R-001 | L2 token budget overflow if 559-670 discrepancy resolves above 670 | Low | High | Resolve discrepancy with exact token count before implementation; defer H-32 marker if budget is insufficient for both |
| R-002 | PG-004 testing becomes documented-but-unenforced ("paper standard") | Medium | Medium | Integrate compaction tests into Phase 2 pilot (U-003 alignment); create CI-enforceable test where possible (L5 gate for rule file changes) |
| R-003 | Template compaction documentation becomes stale as enforcement architecture evolves | Medium | Low | Include compaction resilience in template review checklist; update when enforcement layers change |
| R-004 | Compensating control degradation for remaining Tier B rules (H-16/H-17/H-18) if skill architecture changes | Low | Medium | Track DEC-005 to completion; monitor skill refactoring for compensating control breakage |
| R-005 | Context compaction behavior varies by model/provider, making tests non-portable | Medium | Medium | Test across multiple models/providers in Phase 2 pilot; document model-specific compaction behavior as part of PG-004 test results |

### Pre-Mortem (S-004): "It is 6 months later and this decision failed — why?"

**Failure scenario 1: Compaction never occurs in practice.** Six months later, PG-004 testing has been implemented but no compaction event has been observed in any Jerry session. The testing infrastructure was built for a failure mode that does not manifest. **Consequence:** Engineering time was spent on a non-issue. **Probability:** Medium (compaction behavior depends on session length and context fill patterns, which may not reach compaction thresholds in typical Jerry usage). **Why this is still acceptable:** The testing infrastructure has near-zero ongoing cost once built, and the knowledge that compaction does not occur in typical usage is itself valuable for risk assessment.

**Failure scenario 2: L2 budget exhaustion blocks future enforcement needs.** Six months later, a new HARD rule needs L2 protection but the budget is exhausted. The decision to add H-04 and H-32 markers consumed budget that would have been needed for a higher-priority rule. **Consequence:** Future enforcement decision is constrained. **Probability:** Low (the HARD rule ceiling is 25/25 — no new rules can be added anyway, so new L2 needs would arise only from promoting existing non-L2 rules). **Why this is still acceptable:** The HARD rule ceiling and L2 budget are correlated constraints — both are at capacity, which is consistent.

**Failure scenario 3: Phase 2 finds that negative vocabulary in L2 markers actively harms compliance.** Six months later, Phase 2 data shows that MUST NOT vocabulary in L2 markers produces worse compliance than MUST vocabulary. The H-04 and H-32 markers, written with MUST NOT framing, need revision. **Consequence:** Marker content must be rewritten, but the mechanism (L2 re-injection) remains correct. **Probability:** Low (no evidence suggests L2 re-injection mechanism is framing-dependent; the mechanism is structural, not vocabulary-dependent). **Why this is still acceptable:** Marker content revision is a trivial text change. PG-003 reversibility applies.

---

## PG-003 Reversibility Assessment

PG-003 requires that all framing-motivated recommendations be reversible if Phase 2 finds a null framing effect. This ADR's three decisions have different reversibility profiles:

| Decision | Framing-Dependent? | Reversible? | What Changes Under Null Finding |
|----------|-------------------|-------------|----------------------------------|
| **PG-004 testing** | NO — unconditional by failure mode logic | N/A (not framing-conditional) | Nothing. Testing for compaction survival is warranted regardless of framing. |
| **H-04/H-32 L2 markers (mechanism)** | NO — L2 re-injection is an enforcement mechanism, not a framing choice | N/A (not framing-conditional) | Nothing. The decision to add L2 markers is structural. |
| **H-04/H-32 marker content vocabulary** | YES — MUST NOT vocabulary is a framing choice | YES — trivially reversible | Rewrite marker content from "MUST NOT proceed without JERRY_PROJECT" to "MUST set JERRY_PROJECT before proceeding." Mechanism unchanged; only text changes. |
| **T-004 documentation** | NO — failure mode documentation is engineering practice | N/A (not framing-conditional) | Nothing. Documenting what happens when constraints are lost is valuable regardless of framing. |

**Assessment:** This ADR has minimal framing-conditional surface area. The only framing-dependent component is the specific vocabulary used in marker content, which is trivially revisable (~10 minutes of editing, no architectural impact). The mechanisms (L2 re-injection, compaction testing, failure mode documentation) are all framing-independent.

---

## Evidence Summary

| Evidence ID | Description | Tier | Source | Confidence | Used For |
|-------------|-------------|------|--------|------------|----------|
| T-004 | Context compaction failure mode — constraints may be silently dropped during compaction | T4 (practitioner reports I-28, I-32) | barrier-2/synthesis.md ST-4, Finding O-1 | LOW for directional reversal | Motivates all three decisions |
| PG-004 (evidence) | Practitioner guidance: test context compaction before deployment | T4 (observational) | barrier-2/synthesis.md ST-4, Finding O-1 | MEDIUM for T-004 failure mode frequency | Decision 1 — motivates the testing requirement |
| PG-004 (inference) | Unconditional classification of the testing recommendation | Logical inference (not an evidence tier) | Derived from T-004 failure mode properties: silent failure + no detection mechanism = testing warranted regardless of constraint framing or failure frequency | CERTAINTY (logical) | Decision 1 — establishes that PG-004 is unconditional |
| U-003 | Assumption: pilot design MUST include multi-turn context compaction test conditions | Methodological (binding assumption) | barrier-2/synthesis.md ST-3 | Binding | Decision 1 test integration |
| EO-001 | L2 re-injection observed as primary enforcement mechanism in single session | T5 (single session, confounded) | supplemental-vendor-evidence.md, Evidence Category 3 | LOW (session observation) | Corroborating evidence for L2 importance |
| TASK-012 F3 | L2 budget analysis: 559-670/850 tokens; ~180 headroom; 5 Tier B rules without L2 | T4 (observational, verified by audit) | rules-update-analysis.md, Finding 3 | HIGH for structural finding (Tier B gap exists, 5 rules identified); MEDIUM-HIGH for exact figures (559 vs. ~670 discrepancy unresolved — stated count from quality-enforcement.md disagrees with content audit estimate) | Decision 2 token budget |
| TASK-010 CX-001 | Long SKILL.md files cannot host L2-injectable constraints | T4 (observational) | skills-update-analysis.md, Cross-Skill Patterns | HIGH (architectural fact) | L2 context; companion rule file pattern |
| TASK-011 Gap 4 | L2-REINJECT inapplicable to agent files (architectural limitation) | T4 (architectural fact) | agents-update-analysis.md, Systemic Gap 4 | HIGH (architectural fact) | GAP-X4 documentation |
| TASK-014 WT-GAP-005 | No context compaction resilience in template design | T4 (observational gap) | templates-update-analysis.md, Gap Analysis | HIGH for gap existence | Decision 3 |
| GAP-X2 | Context compaction failure mode identified across 4 of 5 Phase 4 analyses | Cross-analysis (4/5 convergence) | barrier-4/synthesis.md, Section 6 | HIGH for cross-analysis convergence | Motivates all three decisions |
| DEC-005 | Pending decision on Tier B L2 effectiveness measurement | Decision reference | quality-enforcement.md, Two-Tier Enforcement Model note | N/A (pending) | Deferred H-16/H-17/H-18 |
| VS-003 | Anthropic HARD tier vocabulary is prohibitive by design | T4 (direct observation) | supplemental-vendor-evidence.md, VS-003 | HIGH observational | Vocabulary choice for marker content |

**NEVER cite A-11 in any downstream document.** A-11 is a confirmed hallucinated citation (TASK-013 I5 resolution). This ADR does not reference A-11.

---

## Related Decisions

| Decision | Relationship | Status |
|----------|-------------|--------|
| ADR-001 (NPT-014 Elimination Policy) | ADR-001 upgrades blunt prohibitions; ADR-004 ensures upgraded constraints survive compaction | Phase 5 (co-developed) |
| ADR-002 (Constitutional Triplet Upgrade) | ADR-002 upgrades constitutional framing; ADR-004 ensures constitutional constraints have L2 protection | Phase 5 (co-developed) |
| ADR-003 (Routing Disambiguation) | Independent — routing disambiguation operates at L1; ADR-004 testing should verify routing constraints survive compaction | Phase 5 (co-developed) |
| DEC-005 (Tier B L2 Effectiveness) | ADR-004 partially resolves Tier B gap (2 of 5 rules); DEC-005 governs remaining 3 | OPEN (quality-enforcement.md) |
| quality-enforcement.md Two-Tier Enforcement Model | ADR-004 modifies Tier A/B boundary (22/3 from 20/5) | Existing (to be updated) |
| AE-006 (Context Fill Escalation) | AE-006 graduated escalation addresses context fill levels; ADR-004 addresses what happens when compaction occurs at CRITICAL/EMERGENCY levels | Existing |

---

## Compliance

### Constitutional Compliance

| Principle | Compliance | Evidence |
|-----------|-----------|---------|
| P-002 (File Persistence) | COMPLIANT | This ADR is persisted to file |
| P-003 (No Recursive Subagents) | N/A | No agent spawning in this ADR |
| P-011 (Evidence-Based) | COMPLIANT | 4 options evaluated with evidence citations |
| P-020 (User Authority) | COMPLIANT | Status is PROPOSED |
| P-022 (No Deception) | COMPLIANT | Negative consequences documented (L2 budget reduction, testing overhead, documentation complexity, blocking dependency) |

### Constraint Propagation Verification

| Constraint | Compliance | Evidence |
|-----------|-----------|---------|
| GC-P4-1 (no false validation claims) | COMPLIANT | NEVER claims experimental validation; all evidence labeled with tier |
| GC-P4-2 (Phase 2 reproducibility) | COMPLIANT | No existing L2 markers modified; positive-framing reference files not touched |
| GC-P4-3 (vendor evidence not dismissed) | COMPLIANT | VS-003 cited for vocabulary choice rationale |
| U-003 (compaction test in pilot) | COMPLIANT | Decision 1 explicitly requires PG-004 testing aligned with U-003 |
| C-NCA (no A-11 citation) | COMPLIANT | A-11 not cited; explicit NEVER-cite warning included |
| C-EXP (no experimental validation claim) | COMPLIANT | L2 re-injection described as enforcement mechanism, not framing superiority |
| C-T5T4 (no T5-as-T4) | COMPLIANT | EO-001 labeled T5 throughout |
| C-FRM (Phase 2 dependency for framing-specific) | COMPLIANT | Vocabulary choice noted as framing-conditional in PG-003 assessment |
| C-ARCH (architectural limitation acknowledged) | COMPLIANT | GAP-X4 documented; companion rule file pattern recommended |
| HARD rule ceiling | COMPLIANT | No new HARD rules proposed; 25/25 unchanged |

---

## Self-Review Checklist

- [x] P-001: Option evaluations factually accurate — token arithmetic verified against TASK-012; weighted-criteria scoring arithmetic verified (I2)
- [x] P-002: ADR persisted to file
- [x] P-004: Context and rationale documented with evidence citations and tier labels
- [x] P-011: 4 alternatives evaluated with steelman (S-003) applied to each; weighted-criteria table with reproducible scoring (I2)
- [x] P-020: Status PROPOSED (not ACCEPTED)
- [x] P-022: Negative consequences documented (4 items: budget reduction, testing overhead, documentation complexity, blocking dependency)
- [x] GC-P4-1: No false validation claims — all evidence labeled T4 or T5
- [x] GC-P4-2: Phase 2 experimental conditions preserved — no existing markers modified
- [x] U-003: Compaction test requirement aligned with barrier-2 assumption; MVP manual test protocol added (I2)
- [x] A-11: Not cited; explicit NEVER-cite warning present
- [x] Token budget arithmetic: worst-case calculated (745/850 = 87.6%); implementation gate added for exact count resolution (I2)
- [x] PG-003 reversibility: assessed per decision component; minimal framing-conditional surface
- [x] Unconditional vs. conditional: distinguished per decision (PG-004 unconditional; mechanism unconditional; vocabulary conditional); PG-004 "unconditional" clarified as logical inference not evidence tier (I2)
- [x] Architectural limitation: GAP-X4 documented and not contradicted
- [x] S-004 Pre-Mortem: 3 failure scenarios analyzed with probability and acceptability
- [x] S-002 Devil's Advocate: each option evaluated with strongest case (steelman) before dismissal
- [x] Cross-cutting themes: T-004 convergence across 4 of 5 analyses cited
- [x] Evidence tier discipline: every evidence citation includes tier label; TASK-012 F3 confidence split per structural vs. exact-figure (I2)
- [x] HARD rule ceiling: no new rules proposed
- [x] L2-REINJECT rank justification: rank=11 and rank=12 justified relative to existing ranks 1-10 with priority derivation (I2)
- [x] Vulnerability assessment framework: LOW/MEDIUM/LOW-MEDIUM defined by enforcement layer + temporal exposure (I2)
- [x] I2 fix resolution: all 6 I1 scorer items addressed; no new issues introduced; three core decisions unchanged (I2)
- [x] I3 fix resolution: all 6 I2 scorer items addressed — weight derivation note + Force-to-Dimension mapping (Fix 1/4/6); PG-004 evidence split into two rows (Fix 2); MVP executor role + Step 3 context-fill target (Fix 3); executor-owner relationship clarified (Fix 5); T-004 Coverage scoring footnote (Fix 1b) (I3)

---

## PS Integration

| Field | Value |
|-------|-------|
| PS ID | phase-5 |
| Entry ID | TASK-016 |
| Artifact Path | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/phase-5/ADR-004-compaction-resilience.md` |
| Decision | Three unconditional/conditional decisions: PG-004 testing (unconditional), H-04/H-32 L2 additions (timing conditional), T-004 documentation (unconditional) |
| Status | PROPOSED |
| Confidence | 0.85 (HIGH for testing/documentation decisions; MEDIUM for Tier B selection rationale given unresolved 559/670 discrepancy) |
| Next Agent Hint | ps-critic for adversarial quality review; then orch-tracker for state update |

### Key Findings (Downstream Handoff)

1. PG-004 compaction testing is unconditional by failure mode logic — it does not depend on Phase 2 framing directionality
2. H-04 and H-32 selected for L2 addition based on widest-failure-window analysis; H-16/H-17/H-18 deferred to DEC-005
3. L2 budget: worst-case 745/850 (87.6%) after additions; ~105 tokens remaining
4. T-004 failure mode documentation is a template standard, not a framing choice
5. Framing-conditional surface area is minimal (marker content vocabulary only); trivially reversible under PG-003

---

## I2 Fix Resolution Checklist

Resolution status for all 6 priority fixes from adversary-adr004-i1.md (score 0.874 REVISE):

| # | Priority | Dimension | Fix Description | Resolution | Section Modified |
|---|----------|-----------|-----------------|------------|------------------|
| 1 | CRITICAL | Methodological Rigor (0.85) | Replace opaque option scores (A=6, B=8, C=7, D=3) with weighted-criteria evaluation table | RESOLVED: Added 5-dimension weighted-criteria framework with explicit weights, per-dimension scores (1-3), arithmetic derivation, and ranking. Weighting rationale derived from Forces section. | [Options Comparison](#options-considered) |
| 2 | HIGH | Completeness (0.88) | Add minimum viable manual test protocol for PG-004 interim use | RESOLVED: Added 5-step manual test protocol with per-step actions, durations, outputs, pass criterion, scope, and limitations. Explicitly labeled as interim, to be superseded by Phase 2 automation. | [L1: Technical Implementation](#l1-technical-implementation) (Decision 1 Implementation) |
| 3 | HIGH | Actionability (0.87) | Add explicit implementation gate for 559/670 token discrepancy blocking dependency | RESOLVED: Added Implementation Gate table with blocker, owner (role-based), procedure, verification, deadline, and output fields. Added PENDING placeholder for exact count. Steps 2-6 explicitly gated on Step 1 completion. | [L1: Technical Implementation](#l1-technical-implementation) (Decision 2 Implementation) |
| 4 | HIGH | Methodological Rigor (0.85) | Document vulnerability assessment framework for per-artifact-type test conditions (LOW/MEDIUM/LOW-MEDIUM) | RESOLVED: Added vulnerability assessment framework table defining each level by enforcement layer, temporal exposure, and compaction behavior. Added "Vulnerability Derivation" column to per-artifact test conditions table linking each assessment to the framework. | [L1: Technical Implementation](#l1-technical-implementation) (Decision 1 Implementation) |
| 5 | MEDIUM | Evidence Quality (0.85) | Revise TASK-012 F3 confidence; clarify PG-004 unconditional classification | RESOLVED: TASK-012 F3 confidence split to "HIGH for structural finding; MEDIUM-HIGH for exact figures." PG-004 evidence entry rewritten to distinguish T4 evidence tier (for failure mode) from logical inference property (for unconditional classification), with explicit statement that "unconditional" is not an evidence tier. | [Evidence Summary](#evidence-summary) |
| 6 | MEDIUM | Traceability (0.90) | Add rank justification for L2-REINJECT rank=11 and rank=12 relative to existing rank 1-10 ordering | RESOLVED: Added L2-REINJECT Rank Justification section with complete rank 1-12 table showing all existing assignments, source files, and priority rationale. Rank=11 and rank=12 justified by categorical distinction (session/repository scoping vs. behavioral constraints) with explicit comparison to adjacent ranks. | [L1: Technical Implementation](#l1-technical-implementation) (Decision 2 Implementation) |

**Self-verification:** No new issues introduced. The three core decisions (PG-004 testing, H-04/H-32 L2 additions, T-004 documentation) are unchanged in substance. All fixes address presentation, evidence documentation, and methodological transparency.

---

## I3 Fix Resolution Checklist

Resolution status for all 6 priority fixes from adversary-adr004-i2.md (score 0.925 REVISE):

| # | I2 Priority | Dimension(s) | Fix Description | Resolution | Section Modified |
|---|-------------|-------------|-----------------|------------|------------------|
| 1 | 1 + 4 + 6 | MR (0.92), IC (0.93), Tr (0.94) | (a) Add weight derivation note declaring magnitudes as judgmental with ordering rationale; (b) Add footnote explaining why Options A and B both score 3 on T-004 Coverage; (c) Add Force-to-Dimension mapping table | RESOLVED: (a) Weight derivation note added with explicit "architect judgment" declaration, ordering rationale for all 5 magnitudes, and sensitivity analysis showing B > C ranking is robust. (b) Footnote [1] added to T-004 Coverage scores explaining widest-failure-window metric vs. total Tier B count. (c) "Force Derivation" column added to weighting rationale table mapping each dimension to its source force(s). Resolves Fix 1, Fix 4, and Fix 6 in one structural change. | [Options Comparison — Weighted Criteria Evaluation](#options-considered) |
| 2 | 2 | Evidence Quality (0.90) | Restructure PG-004 evidence entry to separate T4 evidence tier from logical inference classification | RESOLVED: Single PG-004 row split into two rows: "PG-004 (evidence)" with T4 tier, MEDIUM confidence for failure mode frequency; "PG-004 (inference)" with logical inference classification, CERTAINTY confidence. The Confidence column now uses a single calibrated value per row, consistent with all other entries. | [Evidence Summary](#evidence-summary) |
| 3 | 3 + 5 | Completeness (0.93), Actionability (0.93) | (a) Add named executor role to MVP test protocol; (b) Add context-fill target to Step 3; (c) Clarify executor-owner relationship | RESOLVED: (a) Executor role added: "framework maintainer or CI engineer" — same role as Decision 2 implementation gate owner. (b) Step 3 target: "until context usage exceeds 70%" (AE-006b WARNING tier, ~140K tokens in 200K window). (c) Explicit statement that MVP executor and implementation gate owner are the same person, with both tasks required before marking Decisions 1 and 2 complete. Resolves Fix 3 and Fix 5. | [Minimum Viable Manual Test Protocol](#l1-technical-implementation) (Decision 1 Implementation) |

**Self-verification:** No new issues introduced. The three core decisions (PG-004 testing, H-04/H-32 L2 additions, T-004 documentation) are unchanged in substance. All I3 fixes address second-order refinements: weight magnitude transparency, evidence table structural consistency, and role/target operationalization. No content contradicts I2 resolutions. A-11 remains absent. AGREE-5 is not presented as T1 or T3 evidence.
