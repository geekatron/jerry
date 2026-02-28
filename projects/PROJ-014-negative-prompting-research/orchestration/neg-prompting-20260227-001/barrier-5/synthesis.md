# Barrier 5 Cross-ADR Coherence Synthesis: Phase 5 Implementation Planning

> ps-synthesizer | TASK-016 | Barrier 5 | PROJ-014 | 2026-02-28
> Synthesis Type: Cross-ADR coherence analysis of Phase 5 Architecture Decision Records (ADR-001 through ADR-004)
> Inputs: ADR-001-npt014-elimination.md (0.952 PASS), ADR-002-constitutional-upgrades.md (0.951 PASS), ADR-003-routing-disambiguation.md (0.957 PASS), ADR-004-compaction-resilience.md (0.955 PASS) + barrier-4/synthesis.md (v4.0.0, 0.950 PASS) + phase-3/taxonomy-pattern-catalog.md (v3.0.0, 0.957 PASS) + barrier-1/synthesis.md + barrier-1/supplemental-vendor-evidence.md
> Quality threshold: >= 0.95 (C4, orchestration directive)
> Self-review: H-15 applied before completion
> Version: 1.1.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language summary of cross-ADR coherence findings |
| [Barrier Gate Check Summary](#barrier-gate-check-summary) | Explicit GC-B5-1 through GC-B5-5 PASS/FAIL mapping (C4 required) |
| [L1: Detailed Analysis](#l1-detailed-analysis) | Per-task analysis addressing all 8 synthesis tasks |
| [Task 1: Cross-ADR Dependency Analysis](#task-1-cross-adr-dependency-analysis) | Dependency map, ordering, circular dependency check |
| [Task 2: Phase 2 Dependency Coherence](#task-2-phase-2-dependency-coherence) | Consistency of Phase 2 conditional components |
| [Task 3: PG-003 Coherence](#task-3-pg-003-coherence) | Cross-ADR PG-003 reversibility consistency |
| [Task 4: Barrier 4 Recommendation Coverage](#task-4-barrier-4-recommendation-coverage) | ADR set vs. barrier-4 recommendations |
| [Task 5: NPT Taxonomy Coverage](#task-5-npt-taxonomy-coverage) | NPT-001 through NPT-014 addressed by ADR set |
| [Task 6: Implementation Ordering](#task-6-implementation-ordering) | Consolidated sequencing across all 4 ADRs |
| [Task 7: Conflict Detection](#task-7-conflict-detection) | Inter-ADR conflicts, tensions, and contradictions |
| [Task 8: Evidence Quality Roll-Up](#task-8-evidence-quality-roll-up) | Aggregate evidence profile and collective gaps |
| [L2: Implementation Roadmap, Risk Assessment, Evidence Gaps](#l2-implementation-roadmap-risk-assessment-evidence-gaps) | Strategic view, cross-ADR action register, risk register, gap closure path |
| [Contradictions and Tensions Disclosure](#contradictions-and-tensions-disclosure) | P-022 compliance: all tensions explicitly stated |
| [Source Summary](#source-summary) | All input sources with contribution summary |
| [PS Integration](#ps-integration) | Worktracker linkage, confidence, next agent hint |
| [Self-Review Checklist](#self-review-checklist) | H-15 compliance |

---

## L0: Executive Summary

Four Architecture Decision Records were produced in Phase 5 of PROJ-014 to convert research findings into implementable framework changes. This synthesis analyzed those four ADRs — NPT-014 elimination (ADR-001), constitutional triplet and high-framing upgrades (ADR-002), routing disambiguation standard (ADR-003), and context compaction resilience (ADR-004) — to verify that they form a coherent, non-conflicting, executable implementation plan.

The core finding is that the four ADRs are internally coherent and collectively address the barrier-4 synthesis recommendations with one substantive gap: the 34 pattern documentation recommendations (TASK-013) are partially covered but have no dedicated ADR. The ADRs exhibit a clean two-class structure — ADR-001 and ADR-004 are unconditional (implement regardless of Phase 2 outcome), while ADR-002 Phase 5B and ADR-003 Component B are conditional on Phase 2 experimental results. The Phase 2 gate provisions across all four ADRs are consistent and non-contradictory.

The PG-003 reversibility provisions are fully coherent: all Phase 2-conditional components are reversible at the vocabulary level while retaining structural improvements (consequence documentation, positive alternatives, failure mode documentation) that have independent auditability value. NEVER treat AGREE-5 rank ordering as externally validated — it is an internally generated synthesis narrative, and the Phase 2-conditional ADR components reflect this epistemic status correctly.

The consolidated implementation ordering is: (1) Phase 2 baseline capture, (2) ADR-001 rule files simultaneously with ADR-004 L2 markers, (3) ADR-001 agent definitions with ADR-002 Phase 5A template/schema, (4) ADR-001 SKILL.md files simultaneously with ADR-003 Component A, (5) ADR-001 patterns and templates, (6) Phase 2 experimental pilot, (7) ADR-002 Phase 5B and ADR-003 Component B after Phase 2 verdict. No circular dependencies exist in this ordering.

### Barrier Gate Check Summary

The following table explicitly maps each barrier-specific gate check (GC-B5-1 through GC-B5-5) to the document section that satisfies it. All checks PASS.

| Gate ID | Check Description | Status | Evidence (Section Citation) |
|---------|------------------|--------|-----------------------------|
| GC-B5-1 | All 4 ADRs analyzed in dependency, conflict, and coverage analysis | PASS | ADR-001 through ADR-004 appear in all 8 task tables: Task 1 dependency map, Task 2 Phase 2 classification, Task 3 PG-003 per-component, Task 4 coverage, Task 5 NPT taxonomy, Task 6 ordering, Task 7 conflict detection, Task 8 evidence roll-up |
| GC-B5-2 | Phase 2 dependency provisions coherent and non-contradictory across all ADRs | PASS | Task 2: Phase 2 Dependency Coherence — 4-row classification table (UNCONDITIONAL/SPLIT classifications) plus 4 numbered consistency verification points; Tension 1 resolved as labeling issue, not substantive contradiction |
| GC-B5-3 | PG-003 contingency provisions consistent across all ADRs | PASS | Task 3: PG-003 Coherence — 9-row component-level table; convergent three-part pattern confirmed (structural additions retained, vocabulary reversible, mechanisms framing-independent); ADR-003 Component A "not reversible by design" correctly scoped to content vs. vocabulary |
| GC-B5-4 | Implementation ordering respects all inter-ADR dependencies | PASS | Task 6: Implementation Ordering — 6-stage ordering with acceptance gates; Tension 2 (ADR-003 Component A before ADR-001 Group 3 for routing disambiguation sections) identified and given explicit sequencing resolution; DAG confirms no circular dependencies |
| GC-B5-5 | Barrier-4 recommendation coverage gap analysis complete | PASS | Task 4: Barrier 4 Recommendation Coverage — all barrier-4 categories mapped to ADRs; 3 gaps identified (GAP 1: 28 TASK-013 SHOULD/MAY recs, GAP 2: 5 TASK-014 contrastive example recs, GAP 3: deferred eng-team/red-team refactor); coverage classification (FULL/PARTIAL/CONDITIONAL/DEFERRED/GAP) applied consistently across 17 rows |

---

## L1: Detailed Analysis

### Task 1: Cross-ADR Dependency Analysis

#### Dependency Map

The four ADRs form a layered dependency graph, not a pipeline. The relationships are as follows:

| From | To | Relationship | Nature |
|------|----|-------------|--------|
| ADR-001 | ADR-002 | ENABLES | ADR-001 establishes the NPT-009 floor; ADR-002 elevates selected constraints to NPT-013. ADR-002 cannot meaningfully target constitutional triplet upgrades until NPT-014 (the floor) is eliminated, because upgrading NPT-014 to NPT-013 directly without the intermediate NPT-009 step would bypass the consequence documentation required by the elimination policy. |
| ADR-001 | ADR-003 | ENABLES (partial) | ADR-001 upgrades NPT-014 instances in existing "Do NOT use when:" sections to NPT-009 format. ADR-003 then standardizes the routing disambiguation sections themselves. The dependency is one-directional and weak — ADR-003 Component A (consequence documentation) can proceed without ADR-001 completion because ADR-003 adds new consequence content rather than upgrading existing NPT-014 instances. |
| ADR-001 | ADR-004 | ENABLES (indirect) | ADR-001 upgrades the content of L2-REINJECT markers (those containing NEVER/MUST NOT without consequence) to NPT-009 format. ADR-004 adds new L2-REINJECT markers for H-04 and H-32. The content of ADR-004's new markers should follow NPT-009 format, consistent with ADR-001 policy. This is a content-quality dependency, not a sequencing gate. |
| ADR-002 | ADR-004 | DOWNSTREAM | ADR-002's constitutional framing upgrades produce higher-quality constraint text; ADR-004's compaction testing should verify that these upgraded constraints survive compaction. Testing dependency only — ADR-004 can be implemented before ADR-002 Phase 5B without conflict. |
| ADR-003 | ADR-004 | INDEPENDENT | Routing disambiguation sections (SKILL.md) operate at L1 loading. They are not subject to L2 re-injection and are not tested by ADR-004's L2 marker mechanism. ADR-004's PG-004 compaction testing should include SKILL.md vulnerability assessment (MEDIUM vulnerability per ADR-004's framework), but this is parallel work, not sequenced work. |

#### Which ADR Must Be Implemented First?

**No single ADR must unconditionally precede all others.** The ordering is constrained by two factors:

1. **Phase 2 baseline preservation (overriding all else):** NEVER apply any Phase 4 recommendation to production artifacts until the Phase 2 experimental baseline is captured. This applies to all four ADRs equally. See Task 6 for the consolidated ordering that respects this constraint.

2. **ADR-001 Group 1 (rule files) before ADR-001 Group 2 (agents) before ADR-001 Group 3 (SKILL.md):** This is an intra-ADR sequencing constraint within ADR-001 that also implies ADR-002 Phase 5A should be executed concurrently with ADR-001 Group 2, because both target `agent-development-standards.md`.

#### Circular Dependency Check

**No circular dependencies exist.** The dependency graph is a directed acyclic graph (DAG):

```
ADR-004 (PG-004 testing) <-- ADR-001 (content quality)
                               |
                               v
                    ADR-002 Phase 5A (immediate)
                               |
                               v
                    [Phase 2 gate]
                               |
                               v
              ADR-002 Phase 5B    ADR-003 Component B
```

ADR-003 Component A (consequence documentation) is fully independent of all other ADRs and can be implemented in any order after Phase 2 baseline capture.

#### Implementation Ordering Conflicts

**No implementation ordering conflicts exist between ADRs.** The only potential conflict is that ADR-001 Group 2 (agent definitions, targeting `agent-development-standards.md`) and ADR-002 Phase 5A (also targeting `agent-development-standards.md`) both modify the same file. This is NOT a conflict — it is a coordination requirement. Both sets of changes are additive to the same file and MUST be implemented together in a single coordinated commit to avoid duplication or contradiction. See Task 6 for the coordinated implementation step.

---

### Task 2: Phase 2 Dependency Coherence

#### Phase 2 Dependency Classification Per ADR

| ADR | Phase 2 Classification | Specific Components |
|-----|----------------------|---------------------|
| ADR-001 | UNCONDITIONAL — Phase 2 irrelevant | All components. The blunt prohibition upgrade is grounded in T1+T3 evidence (PG-001 HIGH), explicitly labeled "Phase 2 outcome irrelevant" in barrier-2/synthesis.md ST-4. |
| ADR-002 | SPLIT — Phase 5A unconditional; Phase 5B conditional | Phase 5A (template + schema update: D-001, D-003, D-006) is unconditional. Phase 5B (SKILL.md NPT-013, agent VIOLATION labels, rule file NPT-010/NPT-011: Sub-4, Sub-5, D-007) is conditional on Phase 2 producing a GO verdict. |
| ADR-003 | SPLIT — Component A unconditional; Component B conditional | Component A (consequence documentation in routing disambiguation sections) is unconditional. Component B (MUST NOT framing vocabulary) is conditional on Phase 2 confirming framing effect at AGREE-5 hierarchy ranks 9-11. |
| ADR-004 | UNCONDITIONAL — Phase 2 irrelevant for all three decisions | Decision 1 (PG-004 testing) is unconditional by failure mode logic. Decision 2 (L2 marker addition for H-04 and H-32) is framing-independent — the mechanism is unconditional, though marker content vocabulary is trivially revisable if Phase 2 finds directionality. Decision 3 (T-004 documentation) is unconditional. |

#### Consistency Verification

The Phase 2 dependency classifications are **consistent and non-contradictory**. Specifically:

1. **ADR-001 unconditional status is preserved correctly.** ADR-001 never claims that NPT-009 framing is superior to positive framing — only that it is superior to NPT-014 blunt prohibition. This is the correct epistemological boundary, and none of the other ADRs contradict it.

2. **ADR-002 Phase 5A does not contaminate Phase 2.** The Phase 5A components (template minimum example update, optional schema field, schema description text) modify `agent-development-standards.md` and `agent-governance-v1.schema.json`. These are template and schema files, not existing artifact files. The Phase 2 baseline is the current state of existing agent `.md` files, existing `.governance.yaml` files, and existing rule files. Phase 5A does not touch any of these. The contamination risk would arise only if agent authors retroactively updated existing agents to match the new template before Phase 2 baseline capture — a process-discipline risk mitigated by ADR-002's explicit "What MUST NOT Happen Before Phase 2" checklist.

3. **ADR-003 Component A does not contaminate Phase 2.** Routing disambiguation sections are new content added to SKILL.md files. SKILL.md files are derivative consumer documents, not the experimental baseline documents. The Phase 2 C1-C7 conditions (barrier-2/synthesis.md TASK-005) concern constraint expression in rule files and prompt templates, not SKILL.md routing sections. ADR-003 explicitly requires: "SKILL.md routing disambiguation changes MUST be committed in a separate branch from any rule file changes (C-003: preserve Phase 2 experimental conditions)."

4. **The ADR-001 exception to the Phase 2 gate is consistently applied.** All four ADRs carry the Phase 2 gate constraint (GC-P4-2 from barrier-2/synthesis.md ST-5). ADR-001 correctly identifies itself as the exception per PG-001 unconditional status. ADR-002 through ADR-004 do not claim exception status for their framing-motivated components.

#### One Coherence Tension Identified

**Tension: ADR-001's "implement after baseline capture" vs. its "unconditional" label.**

ADR-001 states that NPT-014 elimination is "unconditional" and "Phase 2 outcome irrelevant," yet its own Implementation Sequencing section states: "NEVER apply NPT-014 elimination upgrades to framework artifacts that are subject to Phase 2 experimental conditions until the Phase 2 baseline has been captured." This is not a contradiction — it is a distinction between:
- **Decision unconditional:** The direction (eliminate NPT-014) does not depend on Phase 2 results
- **Implementation timing conditional:** The actual file modifications MUST wait until Phase 2 baseline is captured

The barrier-4 synthesis (Section 3) clarifies this correctly: "NPT-014 elimination (PG-001 unconditional, T1+T3 HIGH) can be drafted and planned without Phase 2 completion, but STILL MUST NOT be applied to production artifacts until the Phase 2 experimental baseline is captured." All four ADRs respect this distinction. No incoherence exists — only a labeling precision issue in ADR-001 that could mislead readers into thinking they can immediately modify production files.

---

### Task 3: PG-003 Coherence

#### PG-003 Provisions Per ADR

PG-003 from barrier-2/synthesis.md ST-4: "Pair enforcement-tier constraints with consequence statements; all Phase 4 recommendations must be reversible at the vocabulary dimension if Phase 2 finds a null framing effect."

| ADR | PG-003 Reversibility | Under Null Finding |
|-----|---------------------|-------------------|
| ADR-001 | HIGH — all changes are additive text (consequence, scope, positive alternative). Removing the added text returns to current state. | PG-003 null finding: consequence documentation retains auditability value; framing vocabulary (NEVER/MUST NOT) becomes convention-determined. The structure of the upgrade remains; only framing motivation reclassification is needed. |
| ADR-002 Phase 5A | HIGH — template example is illustrative; schema field is optional. Reverting template example costs one file edit. | PG-003 null finding: reclassify rationale from "effectiveness" to "convention-alignment and auditability." Consequence documentation retained. VIOLATION label becomes convention choice. |
| ADR-002 Phase 5B | HIGH — all Phase 5B changes are additive text to existing agent and rule files. | PG-003 null finding: implement consequence documentation only; NEVER-framing becomes convention-choice. See ADR-002's "PG-003 Null Finding Variant" template for SKILL.md constitutional compliance section. |
| ADR-003 Component A | IRREVERSIBLE BY DESIGN — factual consequence documentation. | PG-003 null finding: ADR-003 explicitly states "NOT REVERSIBLE by design. Consequence documentation is factual and independently valuable." This is correct and does not violate PG-003 — PG-003 governs vocabulary reversibility, not content-value reversibility. Factual documentation is not a framing choice. |
| ADR-003 Component B | FULLY REVERSIBLE — vocabulary only. | PG-003 null finding: revert section headers from "MUST NOT use when:" to neutral framing; retain consequence documentation; retain routing exclusion conditions. |
| ADR-004 PG-004 testing | NOT FRAMING-CONDITIONAL — unconditional by failure mode logic. | PG-003 not triggered. Testing for compaction survival is warranted regardless of framing. |
| ADR-004 L2 marker mechanism | NOT FRAMING-CONDITIONAL — enforcement mechanism. | PG-003 not triggered. Adding L2 markers is structural. |
| ADR-004 L2 marker content vocabulary | TRIVIALLY REVERSIBLE — text edit only. | PG-003 null finding: rewrite "MUST NOT proceed without JERRY_PROJECT" to "MUST set JERRY_PROJECT before proceeding." Mechanism unchanged; ~10 minutes of editing. |
| ADR-004 T-004 documentation | NOT FRAMING-CONDITIONAL — engineering practice. | PG-003 not triggered. Failure mode documentation is factual. |

#### Cross-ADR PG-003 Consistency Finding

**The PG-003 provisions are fully consistent across all four ADRs.** The convergent pattern is:

- **Structural additions** (consequence documentation, scope specification, positive alternatives, failure mode documentation, schema fields) are universally treated as retained under null finding, because they have independent auditability value regardless of framing
- **Vocabulary choices** (NEVER vs. positive imperative, MUST NOT vs. affirmative framing) are universally treated as reversible, because they are convention choices when framing effect is null
- **Enforcement mechanisms** (L2 re-injection, schema validation, routing sections) are universally treated as framing-independent, because the mechanism operates regardless of the vocabulary it carries

**One PG-003 nuance to note (MUST disclose per P-022):** ADR-003's Component A "not reversible by design" claim is technically accurate but requires careful scoping. The statement means: consequence documentation is permanently valuable and should not be removed even under null framing effect. This is correct. However, NEVER interpret this as meaning ADR-003's Component A is exempt from PG-003 review — PG-003 governs whether vocabulary changes need reversal, not whether factual documentation should persist. The "not reversible" claim applies to the *content* (consequence facts), not to the *framing vocabulary* of the section header, which IS reversible.

---

### Task 4: Barrier 4 Recommendation Coverage

#### Barrier 4 Recommendation Categories vs. ADR Coverage

The barrier-4 synthesis (TASK-015, v4.0.0, 0.950 PASS) identified 130 total recommendations across five domains, consolidated into three priority groups. The following table maps each category to the ADR(s) that address it.

| Barrier-4 Category | Source Task | Rec Count | Addressing ADR | Coverage |
|--------------------|-------------|-----------|----------------|---------|
| NPT-014 → NPT-009 upgrades (rule files) | TASK-012 | 6 priority recs (22 instances) | ADR-001 (Group 1) | FULL |
| NPT-014 → NPT-009 upgrades (agent definitions) | TASK-011 | 5 framework-level + 27 agent-level = 32 | ADR-001 (Group 2) | FULL |
| NPT-014 → NPT-009 upgrades (SKILL.md files) | TASK-010 | ~13 NPT-014 instances across 13 skills | ADR-001 (Group 3) | FULL |
| NPT-014 → NPT-009 upgrades (patterns) | TASK-013 | 6 "MUST NOT omit" recs | ADR-001 (Group 4) | PARTIAL — see gap note |
| NPT-014 → NPT-009 upgrades (templates) | TASK-014 | WT-REC-001, WT-GAP-004 | ADR-001 (Group 4) | PARTIAL — see gap note |
| NPT-013 constitutional triplet (SKILL.md) | TASK-010 | 13 skills × 1 rec = 13 | ADR-002 Phase 5B, Sub-4 | CONDITIONAL |
| NPT-009 VIOLATION labels (agents) | TASK-011 | 27 agent-level recs | ADR-002 Phase 5B, Sub-5 | CONDITIONAL |
| Template + schema standard updates | TASK-011 | REC-F-001 through REC-F-003, REC-YAML-001, REC-YAML-002 | ADR-002 Phase 5A | FULL |
| NPT-010/NPT-011 rule file additions | TASK-012 | 4 + 2 = 6 recs | ADR-002 Phase 5B, D-007 | CONDITIONAL |
| Routing disambiguation — consequence docs | TASK-010 | CX-003 (6 skills) + CX-006 (5+2 = 7 skills) = 13 | ADR-003 Component A | FULL |
| Routing disambiguation — MUST NOT framing | TASK-010 | 13 skills | ADR-003 Component B | CONDITIONAL |
| NPT-012 L2-REINJECT additions (Tier B rules) | TASK-012 | 2 recs (H-04, H-32) | ADR-004 Decision 2 | FULL |
| PG-004 compaction testing requirement | TASK-010, TASK-011, TASK-012, TASK-014 | Cross-cutting (4/5 analyses) | ADR-004 Decision 1 | FULL |
| T-004 failure mode documentation (templates) | TASK-014 | WT-GAP-005 | ADR-004 Decision 3 | FULL |
| Pattern documentation upgrades (18 SHOULD) | TASK-013 | 18 "SHOULD add" recs | NO DEDICATED ADR | GAP |
| Pattern documentation upgrades (10 MAY) | TASK-013 | 10 "MAY add" recs | NO DEDICATED ADR | GAP |
| Schema tracking field | TASK-011 | REC-YAML-001, REC-YAML-002 | ADR-002 Phase 5A | FULL |
| Low-maturity agent structural refactor | TASK-011 | D-004 | ADR-002 (explicitly OUT OF SCOPE) | DEFERRED |
| Template contrastive example upgrades | TASK-014 | WT-REC-002, ADV-REC-001–003 | NO DEDICATED ADR | GAP |

#### Recommendations NOT Addressed By Any ADR

**GAP 1: TASK-013 pattern documentation — 28 recommendations without a dedicated ADR.**

The 34 TASK-013 recommendations (6 MUST NOT omit + 18 SHOULD + 10 MAY) cover upgrades to `docs/patterns/` files. ADR-001 nominally includes "Group 4: Patterns and Templates" but does not specify which TASK-013 recommendations are addressed beyond the 6 "MUST NOT omit" NPT-014 elimination cases. The 18 SHOULD and 10 MAY recommendations (28 total) from TASK-013 have no dedicated ADR and no implementation specification.

**GAP 2: TASK-014 template contrastive example upgrades — 5 recommendations without a dedicated ADR.**

WT-REC-002 (upgrade BAD/GOOD contrastive examples to NPT-009), ADV-REC-001 (TEMPLATE-FORMAT.md update), ADV-REC-002, ADV-REC-003 (adversarial template stop documentation), and WT-REC-003 (TASK/BUG/ENABLER consequence additions) are in barrier-4 Group 2 (SHOULD add) but are not addressed by any of the four Phase 5 ADRs. ADR-004 Decision 3 addresses T-004 documentation for templates (WT-GAP-005) but not the contrastive example upgrades.

**GAP 3: Low-maturity agent structural refactor — explicitly deferred.**

ADR-002 D-004 explicitly removes the eng-team/red-team structural refactor from scope. This is a documented deferral, not an oversight. However, it means 8+ agent files remain at flat-markdown structural maturity indefinitely until a separate enabler work item is created. The NPT-009 VIOLATION label upgrade for these agents (Sub-5) can proceed without structural refactoring, but the full upgrade path is blocked by structure.

#### Recommendations Addressed by Multiple ADRs (Overlap)

**Overlap 1: `agent-development-standards.md` — addressed by ADR-001 Group 2 AND ADR-002 Phase 5A.**

Both ADR-001 (NPT-014 elimination in agent guardrails template) and ADR-002 (VIOLATION label format guidance, tier-differentiated consequence requirements) target the same file. This is correctly treated as a coordination requirement rather than a conflict. The two sets of changes MUST be applied in a single coordinated commit to avoid duplication.

**Overlap 2: Rule file constraint vocabulary — addressed by ADR-001, ADR-002, and ADR-004.**

ADR-001 addresses consequence documentation in existing constraints. ADR-002 addresses positive alternative pairing (NPT-010) and justification clauses (NPT-011) in selected HARD rules. ADR-004 addresses L2-REINJECT marker content upgrades for H-04 and H-32. All three ADRs modify `.context/rules/` files. Implementation MUST sequence rule file changes to avoid conflicting edits.

---

### Task 5: NPT Taxonomy Coverage

#### NPT-001 through NPT-014 — ADR Coverage Map

The Phase 3 taxonomy (taxonomy-pattern-catalog.md, v3.0.0, 0.957 PASS) identified 14 named patterns (13 distinct techniques, NPT-007 and NPT-014 being dual entries for the same Type 1 blunt prohibition).

| Pattern ID | Name | AGREE-5 Rank (internally generated — NOT externally validated; see AGREE-5 caveat) | Evidence Tier | Addressed by ADR | Coverage |
|-----------|------|-------------|---------------|------------------|---------|
| NPT-001 | Constitutional AI training | 1 | Untested | NONE | Out of scope for prompt engineering |
| NPT-002 | Reinforcement from human feedback | 2 | T3 | NONE | Out of scope for prompt engineering |
| NPT-003 | Programmatic constraint enforcement | 3 | Untested | NONE | Out of scope for prompt engineering (CI gates are NPT-003 but not prompt-level) |
| NPT-004 | Tool restriction via allowlist | 4 | Untested | NONE | Addressed at architecture level (H-34 tool tier model), not within Phase 5 ADR scope |
| NPT-005 | Warning-based meta-prompt | 5 | T1 (negation accuracy) | NONE | Not targeted; no framework use case identified in Phase 4 analyses |
| NPT-006 | Atomic constraint decomposition | 6 | T1 (compliance) | ADR-001, ADR-002, ADR-003 (indirect) | PARTIAL — ADR-001 enforces consequence + scope + alternative, which is decomposition; not targeted as a standalone upgrade but achieved as a byproduct |
| NPT-007 | Structured behavioral constraint | 9 | T1 (underperformance baseline) | ADR-001 (primary), ADR-002, ADR-003 | FULL — NPT-007 is the target of NPT-014 elimination |
| NPT-008 | Contrastive example pairing | 8 | T3/E-007 | ADR-001 (Group 4 partial), template gap | PARTIAL — TASK-014 recommends upgrading NPT-008 to NPT-009 (WT-REC-002) but no dedicated ADR |
| NPT-009 | Declarative behavioral negation with consequence | 9 | T4 | ADR-001 (primary), ADR-002, ADR-003, ADR-004 | FULL — universal upgrade target; all four ADRs implement or enforce NPT-009 as minimum |
| NPT-010 | Paired prohibition with positive alternative | 9 | T4 | ADR-002 (D-007, 4 rule-file candidates), ADR-003 (Component B framing) | PARTIAL — conditional on Phase 2 for framing component; ADR-002 D-007 covers 4 rule-file NPT-010 additions |
| NPT-011 | Justified prohibition with reason clause | 10 | T4 | ADR-002 (D-007, 2 rule-file candidates) | PARTIAL — conditional on Phase 2; 2 rule-file candidates (H-13, H-31) identified |
| NPT-012 | L2 re-injected constraint | 10 | T4 | ADR-004 (Decision 2, H-04 and H-32) | PARTIAL — limited to 2 new markers; existing NPT-012 infrastructure unchanged |
| NPT-013 | Constitutional triplet prohibition | 10–11 | T4 | ADR-002 (Sub-4 SKILL.md, Sub-5 agent VIOLATION labels) | CONDITIONAL — Phase 2-gated |
| NPT-014 | Standalone blunt prohibition (anti-pattern) | 12 | T1+T3 (underperformance) | ADR-001 (elimination policy) | FULL — universal elimination mandate |

#### NPTs Not Addressed by Any ADR

| Pattern | Reason Not Addressed |
|---------|---------------------|
| NPT-001 | Training-time constraint; outside prompt engineering scope |
| NPT-002 | Training-time constraint; outside prompt engineering scope |
| NPT-003 | Programmatic enforcement; operates at L3/L5 (CI gates, schema validation) — already implemented at architectural level, not a Phase 5 prompt-engineering change |
| NPT-004 | Tool allowlist architecture; already implemented via H-34 tool tier model (T1-T5 classification); not a Phase 5 recommendation target |
| NPT-005 | Warning-based meta-prompt; no Jerry Framework use case identified in Phase 4 analyses; potential future research topic |
| NPT-008 | Contrastive example pairing; addressed only partially by ADR-001 Group 4 (TASK-013 "MUST NOT omit" group) and not by a dedicated ADR for TASK-014 template upgrades (WT-REC-002 gap) |

**Synthesis finding for NPT-005:** Phase 4 analyses did not identify NPT-005 (warning-based meta-prompts, A-23 EMNLP 2025: +25.14% negation accuracy) as a Jerry Framework recommendation target. This is a gap in Phase 4 scope, not a Phase 5 ADR gap. NPT-005 may warrant a future Phase 6 investigation to determine whether warning-based prompts improve negation reasoning in framework constraints.

---

### Task 6: Implementation Ordering

#### Consolidated Implementation Ordering

The following ordering respects all four ADRs' individual sequencing constraints and inter-ADR dependencies identified in Task 1. The ordering is expressed as discrete stages with acceptance gates between stages.

**PREREQUISITE — Stage 0: Phase 2 Baseline Capture**

NEVER proceed to Stage 1 file modifications without completing this stage.

| Action | Owner | Acceptance Criterion |
|--------|-------|---------------------|
| Resolve 559 vs. 670 L2-REINJECT token discrepancy | Framework maintainer / CI engineer (ADR-004 Decision 2 gate owner) | Exact token count documented in ADR-004 Decision 2 implementation gate section |
| Capture Phase 2 baseline | Phase 2 researcher | Commit hash of pre-modification framework state documented; branch isolation established |
| Verify ADR-001 through ADR-004 are all PROPOSED (not yet ACCEPTED) | Any | All four ADRs at PROPOSED status; user approval per P-020 obtained before any Stage 1 begins |

**Stage 1: Rule File Foundation (ADR-001 Group 1 + ADR-004 Decisions 2 and 3)**

These changes are unconditional and address the highest-impact artifacts (L1/L2 enforcement layer).

| Action | ADR | Target Files | Dependencies |
|--------|-----|-------------|-------------|
| Upgrade 22 NPT-014 instances in rule files to NPT-009 (R-QE-001 through R-ADS-003) | ADR-001 Group 1 | `.context/rules/quality-enforcement.md`, `agent-development-standards.md`, and other rule files | Stage 0 complete |
| Add H-04 L2-REINJECT marker (rank=11) to `quality-enforcement.md` | ADR-004 Decision 2 | `quality-enforcement.md` | Stage 0 token discrepancy resolved |
| Add H-32 L2-REINJECT marker (rank=12) to `project-workflow.md` | ADR-004 Decision 2 | `project-workflow.md` | H-04 marker added first (wider failure window, higher priority) |
| Update Tier A/B table in `quality-enforcement.md` (20→22 Tier A, 5→3 Tier B) | ADR-004 Decision 2 | `quality-enforcement.md` | Both markers added |
| Add T-004 failure mode documentation sections to constraint-bearing templates | ADR-004 Decision 3 | All worktracker entity templates, adversarial strategy templates, ADR template, requirements templates | Stage 0 complete |
| Run PG-004 manual compaction test for Stage 1 artifacts | ADR-004 Decision 1 | Stage 1 modified files | Stage 1 edits complete |

**Stage 2: Agent Definition Standards (ADR-001 Group 2 + ADR-002 Phase 5A) — Coordinated**

These changes MUST be implemented in a single coordinated commit to `agent-development-standards.md` to avoid duplication.

| Action | ADR | Target Files | Dependencies |
|--------|-----|-------------|-------------|
| Upgrade NPT-014 instances in `agent-development-standards.md` guardrails template | ADR-001 Group 2 (framework-level: 5 recs) | `agent-development-standards.md` | Stage 1 complete |
| Update guardrails template minimum example from NPT-014 to NPT-009 (REC-F-001) | ADR-002 Phase 5A | `agent-development-standards.md` | Coordinated with above |
| Add VIOLATION label format guidance (REC-F-002) | ADR-002 Phase 5A | `agent-development-standards.md` | Coordinated with above |
| Add tier-differentiated consequence guidance (REC-F-003) | ADR-002 Phase 5A | `agent-development-standards.md` | Coordinated with above |
| Add `forbidden_action_format` tracking field to governance schema (REC-YAML-001) | ADR-002 Phase 5A | `docs/schemas/agent-governance-v1.schema.json` | `agent-development-standards.md` changes complete |
| Add schema description for forbidden_actions format (REC-YAML-002) | ADR-002 Phase 5A | `docs/schemas/agent-governance-v1.schema.json` | Coordinated with above |
| Upgrade NPT-014 instances in individual agent `.md` files (27 agent-level recs) | ADR-001 Group 2 (agent-level: 27 recs) | Individual agent definition files in `skills/*/agents/*.md` | `agent-development-standards.md` complete (source of truth upgraded first) |

**Stage 3: SKILL.md and Routing Disambiguation (ADR-001 Group 3 + ADR-003 Component A) — Parallel**

These changes are independent and can proceed in parallel in separate branches.

| Action | ADR | Target Files | Dependencies |
|--------|-----|-------------|-------------|
| Upgrade NPT-014 instances in 13 SKILL.md files to NPT-009 | ADR-001 Group 3 | `skills/*/SKILL.md` | Stage 2 complete (rule files and agent standards are authoritative source; SKILL.md is derivative) |
| Audit trigger map collisions for all 13 skills | ADR-003 Component A | `mandatory-skill-usage.md` (read-only at this step) | Stage 0 complete |
| Add routing disambiguation sections with consequence documentation (Group 1: 7 skills) | ADR-003 Component A | Group 1 SKILL.md files: bootstrap, nasa-se, problem-solving, transcript, worktracker, architecture, eng-team | Collision audit complete |
| Add consequence column to existing routing disambiguation sections (Group 2: 6 skills) | ADR-003 Component A | Group 2 SKILL.md files: adversary, ast, orchestration, red-team, saucer-boy, saucer-boy-framework-voice | Collision audit complete |
| Verify trigger map synchronization; update negative keywords if gaps found | ADR-003 Component A | `mandatory-skill-usage.md` | All SKILL.md sections drafted |
| Run PG-004 manual compaction test for Stage 3 SKILL.md artifacts | ADR-004 Decision 1 | Stage 3 modified SKILL.md files | Stage 3 edits complete |
| MUST commit in separate branch from rule file changes (Stage 1 and 2) | ADR-003 C-003 | N/A | Stage 3 branch separate |

**Stage 4: Pattern and Template Documentation (ADR-001 Group 4)**

These changes address `docs/patterns/` and `.context/templates/` files. They are independent of Stages 1-3 and can be parallelized after Phase 2 baseline capture.

| Action | ADR | Target Files | Dependencies |
|--------|-----|-------------|-------------|
| Upgrade NPT-014 instances in pattern documentation (6 "MUST NOT omit" TASK-013 recs: ARCH-R1, ARCH-R4, TEST-R1 and 3 others) | ADR-001 Group 4 | `docs/patterns/` files | Stage 0 complete |
| Upgrade NPT-014 instances in template files (WT-REC-001, WT-GAP-004) | ADR-001 Group 4 | `.context/templates/` worktracker entity templates | Stage 0 complete |

**Stage 5: Phase 2 Experimental Pilot**

Phase 2 MUST be completed before proceeding to Stage 6. This is the longest stage and gates the largest body of conditional changes.

| Action | Evidence Required | Outcome |
|--------|-----------------|---------|
| Execute C1-C7 pilot conditions (n=30) | Phase 2 execution report | GO/NO-GO criteria evaluated |
| Apply PG-003 contingency assessment | Phase 2 results analysis | Framing effect confirmed / null / inconclusive |
| Integrate compaction testing into Phase 2 multi-turn conditions (U-003) | Test results per ADR-004 Decision 1 protocol | T-004 frequency characterized |

**Stage 6: Phase 2-Conditional Changes (ADR-002 Phase 5B + ADR-003 Component B)**

MUST NOT begin until Stage 5 produces a GO verdict and PG-003 assessment is complete.

| Action | ADR | Condition | Target |
|--------|-----|-----------|--------|
| Implement NPT-013 constitutional triplet in all 13 SKILL.md Constitutional Compliance sections | ADR-002 Phase 5B, Sub-4 | GO + framing effect confirmed: NEVER framing; GO + null: consequence docs only with positive framing | 13 SKILL.md files |
| Upgrade agent forbidden_actions to NPT-009 VIOLATION format (Tier 1 mid-maturity agents first) | ADR-002 Phase 5B, Sub-5 | GO (any verdict) | ps-analyst, ps-researcher, ps-critic, orch-planner, nse-verification |
| Upgrade agent forbidden_actions (Tier 2 low-maturity agents) | ADR-002 Phase 5B, Sub-5 | Tier 1 complete | eng-architect, eng-security, red-lead, red-recon, adv-executor, adv-scorer, sb-voice |
| Verify high-maturity agents not degraded (Tier 3) | ADR-002 Phase 5B, Sub-5 | Tier 2 complete | nse-requirements, ts-parser, wt-auditor |
| Add NPT-010 positive alternative pairings to 4 HARD rule candidates (H-01, H-05, H-07, H-20) | ADR-002 Phase 5B, D-007 | GO (any verdict) — positive alternatives retain value under null framing | Rule files |
| Add NPT-011 justification clauses to 2 HARD rule candidates (H-13, H-31) | ADR-002 Phase 5B, D-007 | GO (any verdict) | `quality-enforcement.md` |
| Apply MUST NOT framing vocabulary to routing disambiguation section headers and rows | ADR-003 Component B | GO + framing effect confirmed ONLY | All 13 SKILL.md routing disambiguation sections |
| If null framing effect: retain Component A; adopt community-preferred framing | ADR-003 Component B | GO + null | All 13 SKILL.md routing disambiguation sections |

---

### Task 7: Conflict Detection

#### Conflicts Between ADR Provisions

**Conflict analysis result: No direct conflicts exist between the four ADRs.** The following items were examined and confirmed non-conflicting:

**Item 1: ADR-001 and ADR-002 both modify `agent-development-standards.md`.**

Not a conflict — it is a coordination requirement. ADR-001 Group 2 eliminates NPT-014 instances in the guardrails template minimum example; ADR-002 Phase 5A replaces that same minimum example with an NPT-009 format version (REC-F-001). These are aligned changes targeting the same upgrade. The resolution is a single coordinated Stage 2 commit, not a conflict resolution.

**Item 2: ADR-003 Component A and ADR-001 Group 3 both modify SKILL.md files.**

Not a conflict. ADR-001 Group 3 upgrades existing NPT-014 instances within SKILL.md content. ADR-003 Component A adds new routing disambiguation sections. These are additive changes to the same files. No text from ADR-001 is contradicted by ADR-003 or vice versa.

**Item 3: ADR-004 adds L2 markers while ADR-001 modifies existing L2 marker content.**

Not a conflict. ADR-001 upgrades the content within existing L2-REINJECT markers (making "NEVER use pip" into a structured NPT-009 form). ADR-004 adds two new L2-REINJECT markers (H-04, H-32) that did not previously exist. These are independent operations on the same file (`quality-enforcement.md`). The Stage 1 consolidated commit handles both simultaneously.

**Item 4: ADR-002 Phase 5B NPT-010 candidates overlap with ADR-002's NPT-009 floor.**

Not a conflict. NPT-010 (paired prohibition with positive alternative) is a superset of NPT-009 (declarative behavioral negation with consequence). The candidates in ADR-002 D-007 (H-01, H-05, H-07, H-20 for NPT-010; H-13, H-31 for NPT-011) already satisfy or will satisfy NPT-009 after ADR-001 Group 1 execution. ADR-002 D-007 adds the positive alternative or justification clause on top of the NPT-009 foundation. This is the correct progression.

**Item 5: ADR-002 Phase 5A claims it does not contaminate Phase 2 baseline, but modifies `agent-development-standards.md`.**

Potential tension, NOT a conflict. As analyzed in Task 2, the Phase 5A changes are to the template/schema — not to existing agent files that serve as the Phase 2 experimental baseline. The risk is process-discipline: an agent author could voluntarily update an existing agent to match the new template before Phase 2 baseline capture. This is mitigated by ADR-002's explicit "What MUST NOT Happen Before Phase 2" checklist. The tension exists as a process risk, not an architectural conflict.

#### Tensions (Disclosed Per P-022)

**Tension 1: ADR-001 claims unconditional status but delays production implementation until Phase 2 baseline is captured.**

This is a labeling tension, not a substantive conflict. The direction (eliminate NPT-014) is unconditional per T1+T3 evidence. The timing (after baseline capture) is a research integrity requirement. Both are correct simultaneously. However, stakeholders who read "unconditional" may incorrectly interpret it as "implementable immediately." This synthesis recommends adding a clarifying note to ADR-001 production documentation: "Unconditional = evidence-based direction independent of Phase 2 framing outcome; implementation timing is gated on Phase 2 baseline capture."

**Tension 2: ADR-003 and ADR-001 both address "Do NOT use when:" sections in SKILL.md, but via different mechanisms.**

ADR-001 Group 3 would upgrade the vocabulary within existing "Do NOT use when:" sections from NPT-014 format (bare prohibitions) to NPT-009 format (structured prohibitions with consequence). ADR-003 Component A adds consequence documentation columns to these same sections (converting them to table format). These mechanisms could produce different structural outputs if applied independently. **Resolution:** ADR-003 Component A MUST be applied first to Group 2 skills (consequence column addition), and ADR-001 Group 3 MUST treat the resulting table entries as the NPT-009 upgrade target rather than the original bare-text format. The "consequence" text in ADR-003 satisfies ADR-001's NPT-009 consequence documentation requirement. Appling ADR-003 Component A effectively pre-executes ADR-001 Group 3 for routing disambiguation sections — these sections MUST NOT be upgraded twice.

**Tension 3: ADR-002's AGREE-5-derived NPT-010 and NPT-011 candidate rules are presented with high specificity despite AGREE-5's internally-generated status.**

ADR-002 identifies specific HARD rule candidates for NPT-010 (H-01, H-05, H-07, H-20) and NPT-011 (H-13, H-31) additions. These candidates are derived from TASK-012 findings, which in turn reference AGREE-5 hierarchy ranks 8-9 for NPT-010 and NPT-011 positioning. AGREE-5 is internally generated and NOT externally validated. The candidate rule selections are reasonable (these are high-impact, frequently referenced HARD rules), but their prioritization should be understood as analyst judgment, not experimentally established priority. NEVER present these candidates as the uniquely correct choices — they are provisional pending implementation-time review.

**Tension 4: ADR-004 Decision 2 has a blocking implementation gate (559 vs. 670 token discrepancy) with no deadline.**

The ADR specifies "No calendar deadline — this is a sequencing gate, not a time-boxed task." Without a deadline, this blocking gate could stall Stage 1 indefinitely. The framework maintainer assigned to this task has no accountability mechanism beyond the worktracker entry itself. **Recommendation:** Assign this task a time-box of 3 working days from Stage 0 initiation. If unresolved after 3 days, escalate to framework governance.

---

### Task 8: Evidence Quality Roll-Up

#### Aggregate Evidence Profile Across All Four ADRs

| Evidence Tier | What It Supports | ADR Scope Relying on This Tier |
|--------------|-----------------|-------------------------------|
| **T1 peer-reviewed (A-15 EMNLP 2024, A-20 AAAI 2026)** | Blunt prohibition (NPT-014) underperforms structured alternatives; structured constraint pairing improves compliance +7-8%; instruction hierarchy failure in LLMs | ADR-001 universal elimination policy (primary anchor); ADR-002 context (cited for compliance improvement baseline) |
| **T3 preprint (A-31, arXiv 2312.16171)** | Corroborating evidence for prohibition underperformance across task types; affirmative directives showed 55% improvement on GPT-4 vs. prohibitions | ADR-001 supporting evidence |
| **T4 vendor self-practice (VS-001–VS-004)** | 33 NEVER/MUST NOT instances across 10 Claude Code rule files; HARD tier vocabulary = prohibitive; constitutional constraints as NEVER statements; three competing causal explanations | ADR-002 constitutional framing rationale (VS-003, VS-004); ADR-003 routing anti-pattern basis (AP-01, AP-02); ADR-004 L2 mechanism motivation (VS-003 vocabulary consistency) |
| **T4 Phase 4 audit findings** | NPT-014 prevalence (22/36 rule-file instances = 61%; 37 SKILL.md recs; 32 agent recs; 34 pattern recs; 13 template recs); routing collision zones; L2 budget analysis (559-670/850 tokens); Tier B failure windows | All four ADRs — primary implementation evidence |
| **T4 failure mode analysis (T-004)** | Context compaction may silently drop L1-only constraints; Tier B rules lack L2 protection; 4/5 Phase 4 analyses identified compaction risk | ADR-004 primary motivation; referenced in ADR-001, ADR-002, ADR-003 for compaction context |
| **Internal synthesis (AGREE-5)** | 12-level effectiveness hierarchy (internally generated, adversary gate 0.953, NOT externally validated); pattern ordering ranks 9-11 | ADR-002 Phase 5B NPT-010/NPT-011 candidates; ADR-003 Component B framing gate; Phase 2 experimental conditions reference |
| **Logical inference (PG-004 unconditional classification)** | Testing for a failure mode that produces silent loss with no recovery mechanism is warranted regardless of failure frequency | ADR-004 Decision 1 |

#### Evidence Tiers NOT Represented in the ADR Set

- **T2 (established practitioner literature from major AI providers):** Defined but empty in the Phase 3 taxonomy. No vendor documentation functions as prescriptive methodology (vs. observational T4). No ADR claims T2 evidence.
- **T5 (single-session observation):** EO-001/EO-002/EO-003 are referenced for corroboration in barrier-1 materials but NEVER elevated to T4 in any ADR.

#### Collective Evidence Gaps

| Gap ID | Description | Affected ADRs | Resolution Path |
|--------|-------------|--------------|----------------|
| GAP-X1 | UNTESTED causal comparison: NPT-009/NPT-010/NPT-011 vs. structurally equivalent positive framing | ADR-002 Phase 5B, ADR-003 Component B | Phase 2 experimental pilot (C1-C7); this is the primary research question |
| GAP-X2 | Context compaction (T-004) failure mode: unverified frequency and directional reversal | ADR-004 | Phase 2 U-003 multi-turn conditions; MVP manual test protocol (interim) |
| GAP-X3 | Governance YAML content partially inferred: ~53% of TASK-011 recommendations are T4 inferred because governance YAML files were not directly read | ADR-002 Phase 5B | Phase 5 implementation audit of actual `.governance.yaml` file content before applying changes |
| GAP-X4 | NPT-012 inapplicable to agent files: architectural gap (Tier 2 loading, no per-prompt re-injection) | ADR-004 (documented but not resolved) | Requires Claude Code runtime architectural change; outside Jerry Framework control |
| GAP-X5 | TASK-013 pattern sampling ceiling: 60-80 line samples for 7 of 12 categories; absence of anti-pattern sections may be sampling artifact | ADR-001 Group 4 (patterns) | Full pattern file reads required before implementing TASK-013 recommendations |
| GAP-X6 | NPT-010/NPT-011 controlled evidence: zero T1 studies | ADR-002 Phase 5B D-007 | Phase 2 C4/C5 conditions (paired vs. justified prohibition pilot) |
| GAP-X7 | Routing disambiguation framing: no controlled evidence for "MUST NOT use when:" vs. positive routing guidance | ADR-003 Component B | Phase 2 routing record measurement (RT-M-008) before/after Component B |
| GAP-X8 | AGREE-5 hierarchy rank ordering unvalidated: externally unverified ordering of ranks 9-11 (declarative > paired > justified) | ADR-002, ADR-003 (AGREE-5-dependent components) | Future external validation study; currently provisional |

#### Evidence Strength Summary by ADR Decision

| Decision | Evidence Strength | Justification |
|----------|-----------------|--------------|
| ADR-001: Universal NPT-014 elimination | HIGH — T1+T3 unconditional | PG-001 explicitly labels this "unconditional"; A-20 AAAI 2026 + A-15 EMNLP 2024 + A-31 arXiv = three independent evidence streams |
| ADR-002: Phase 5A template/schema | MEDIUM — T4 observational | VS-003/VS-004 observational; auditability motivation is structural (framing-independent); convention-alignment rationale |
| ADR-002: Phase 5B constitutional framing | LOW-MEDIUM — T4 observational, UNTESTED causal | Vendor practice observed; causal mechanism for NEVER vs. positive framing is the Phase 2 experimental question |
| ADR-003: Component A consequence docs | HIGH — T4 direct audit + logical | CX-003/CX-006 gaps directly audited; auditability value is logically independent of framing |
| ADR-003: Component B MUST NOT framing | LOW — UNTESTED | No controlled evidence for framing superiority in routing disambiguation context specifically |
| ADR-004: PG-004 testing mandate | HIGH — logical (failure mode) | Silent failure + no detection = testing warranted; unconditional by failure mode logic |
| ADR-004: H-04/H-32 L2 markers | MEDIUM — T4 audit + failure window analysis | TASK-012 Finding 3 confirms Tier B gap and ~180 token headroom; failure window analysis distinguishes H-04/H-32 from H-16/H-17/H-18 |
| ADR-004: T-004 documentation | HIGH — T4 audit convergence | WT-GAP-005 + 4/5 Phase 4 analyses; documentation is framing-independent engineering practice |

---

## L2: Implementation Roadmap, Risk Assessment, Evidence Gaps

### Cross-ADR Action Register

The following table consolidates ALL cross-cutting pre-implementation actions identified in this synthesis — from Task 6 implementation ordering, Task 7 tensions, Task 4 gap recommendations, the risk register, and PS Integration Key Findings. A practitioner preparing to begin Stage 0 or Stage 1 MUST NOT proceed without reviewing every action in this register.

| Action ID | Description | Owner Type | Timing / Stage | Source Section | Blocking |
|-----------|-------------|------------|----------------|----------------|----------|
| CX-A-001 | Resolve 559 vs. 670 L2-REINJECT token discrepancy and document exact count in ADR-004 Decision 2 implementation gate section | Framework maintainer / CI engineer | Stage 0 — MUST complete before Stage 1 | Task 6 Stage 0; Task 7 Tension 4; Risk CX-R-003 | Yes — blocks Stage 1 start |
| CX-A-002 | Capture Phase 2 experimental baseline (commit hash of pre-modification framework state; establish branch isolation) | Phase 2 researcher | Stage 0 — MUST complete before any Stage 1 file modification | Task 6 Stage 0; Task 1 "Phase 2 baseline preservation" constraint | Yes — blocks all file modifications |
| CX-A-003 | Obtain user P-020 approval for all four ADRs (ADR-001 through ADR-004 at PROPOSED status) before any Stage 1 begins | Any (user authority required) | Stage 0 — MUST complete before Stage 1 | Task 6 Stage 0; PS Integration Key Finding 1; Self-Review P-020 check | Yes — blocks Stage 1 start |
| CX-A-004 | Apply 3-day time-box from Stage 0 initiation to CX-A-001 token discrepancy resolution; escalate to framework governance if unresolved after 3 days | Framework governance | Stage 0 — concurrent with CX-A-001 | Task 7 Tension 4; Risk CX-R-003 mitigation | No — governance escalation path |
| CX-A-005 | Add clarifying note to ADR-001 production documentation: "Unconditional = evidence-based direction independent of Phase 2 framing outcome; implementation timing is gated on Phase 2 baseline capture" | ps-architect or ADR-001 author | Stage 0 — before any Phase 5 implementation communication | Task 7 Tension 1; PS Integration Next Agent Hint | No — prevents stakeholder misinterpretation |
| CX-A-006 | Execute Stage 2 (ADR-001 Group 2 + ADR-002 Phase 5A) as a single coordinated commit to `agent-development-standards.md` — NEVER apply these independently | Framework maintainer (single owner for both change sets) | Stage 2 | Task 7 Item 1; Risk CX-R-001; PS Integration Key Finding 3 | Yes — failure creates duplication/contradiction in authoritative file |
| CX-A-007 | Apply ADR-003 Component A (consequence column addition) to routing disambiguation sections BEFORE applying ADR-001 Group 3 to the same sections; NEVER upgrade these sections twice | SKILL.md implementer | Stage 3 — before ADR-001 Group 3 for routing disambiguation | Task 7 Tension 2; Risk CX-R-002 | Yes — wrong order creates double-upgrade confusion |
| CX-A-008 | Create TASK-017 worktracker entry for TASK-013 SHOULD/MAY pattern documentation recommendations (28 recommendations with no dedicated ADR) | Project coordinator | Stage 4 or post-Stage 4 | Task 4 GAP 1; Risk CX-R-006 | No — not a Stage 0-4 blocker, but prevents permanent gap |
| CX-A-009 | Bundle TASK-014 template contrastive example upgrades (5 recommendations: WT-REC-002, ADV-REC-001–003, WT-REC-003) into TASK-017 or create TASK-018 | Project coordinator | Post-Stage 4 | Task 4 GAP 2; Risk CX-R-007 | No — Group 2 SHOULD priority |
| CX-A-010 | Set 6-month time-bound for Phase 2 execution; if Phase 2 not completed within 6 months, ADR-003 Component B defaults to community-preferred framing per Failure Scenario 3 mitigation | Phase 2 researcher / project governance | Stage 5 entry | Risk CX-R-004; PS Integration Key Finding 5 | No — governance accountability mechanism |
| CX-A-011 | Audit actual `.governance.yaml` file content before Stage 6 agent upgrades to verify ~53% inferred TASK-011 recommendations against actual file state (GAP-X3) | ADR-002 Phase 5B implementer | Stage 6 entry — before any agent forbidden_actions upgrades | Task 8 GAP-X3; Risk CX-R-008 | Yes — prevents applying recommendations to wrong file states |
| CX-A-012 | NEVER cite A-11 in any downstream implementation document, prompt template, or framework artifact | All implementers | Ongoing — all stages | PS Integration Key Finding 7; Self-Review C-001 | Yes — A-11 is a confirmed hallucinated citation |
| CX-A-013 | NEVER present AGREE-5 NPT-010/NPT-011 candidate rule selections as uniquely correct or externally validated; present as provisional analyst judgment | All implementers | Ongoing — all stages | Task 7 Tension 3; PS Integration Key Finding 6 | No — epistemic accuracy requirement |

### Implementation Roadmap Summary

The six-stage consolidated implementation ordering produces the following timeline structure (calendar duration is contingent on Phase 2 execution):

```
Stage 0: Phase 2 baseline capture (1-2 days)
    └── Token discrepancy resolution (blocking gate for ADR-004 Decision 2)
    └── Commit hash baseline documentation
    └── User approval of all four ADRs (P-020)
         |
Stage 1: Rule files + L2 markers + T-004 docs (1 week)
         |
Stage 2: Agent standards — coordinated (1 week, parallel with Stage 3 start)
         |
Stages 3 and 4: SKILL.md + Routing disambiguation + Patterns + Templates (2-3 weeks)
         |
Stage 5: Phase 2 experimental pilot (4-12 weeks — primary duration uncertainty)
         |
Stage 6: Phase 2-conditional changes (1-2 weeks after Phase 2 verdict)
```

**Total calendar duration estimate:** 9-20 weeks, with Phase 2 execution as the primary driver of uncertainty.

### Risk Register (Cross-ADR)

| Risk ID | Description | Probability | Severity | ADR Source | Mitigation |
|---------|-------------|-------------|----------|-----------|-----------|
| CX-R-001 | Stage 2 coordination failure: ADR-001 Group 2 and ADR-002 Phase 5A applied independently to `agent-development-standards.md`, creating duplication | MEDIUM | HIGH | ADR-001 + ADR-002 overlap | Single coordinated Stage 2 commit; one owner responsible for both change sets |
| CX-R-002 | Tension 2 (Task 7): ADR-003 Component A and ADR-001 Group 3 applied in wrong order to "Do NOT use when:" sections, creating double-upgrade confusion | MEDIUM | MEDIUM | ADR-001 + ADR-003 tension | ADR-003 Component A must precede ADR-001 Group 3 for routing disambiguation sections; apply ADR-001 Group 3 to non-routing-disambiguation content only |
| CX-R-003 | ADR-004 token gate unresolved; Stage 1 stalls indefinitely | MEDIUM | HIGH | ADR-004 Decision 2 blocking gate | Time-box resolution to 3 working days; escalate if unresolved |
| CX-R-004 | Phase 2 indefinitely delayed; Stage 6 conditional changes accumulate as technical debt | HIGH | MEDIUM | ADR-002 Phase 5B, ADR-003 Component B | Set 6-month time-bound; if Phase 2 not completed, ADR-003 Component B defaults to community-preferred framing per ADR-003's Failure Scenario 3 mitigation |
| CX-R-005 | New NPT-014 instances created during rollout faster than old ones are eliminated | MEDIUM | HIGH | ADR-001 | Integrate NPT-014 diagnostic into H-17 quality gate; update guardrails template (Stage 2) first to prevent new low-quality agent creation |
| CX-R-006 | TASK-013 pattern documentation (GAP 1: 28 recommendations) never receives a dedicated implementation plan | HIGH | MEDIUM | Task 4 gap | Create TASK-017 worktracker entry for TASK-013 SHOULD/MAY recommendations; assign as post-Stage 4 work |
| CX-R-007 | TASK-014 template contrastive example upgrades (GAP 2: 5 recommendations) not addressed by any ADR | HIGH | LOW | Task 4 gap | Bundle into TASK-017 or create TASK-018; WT-REC-002 is Group 2 (SHOULD) not urgent |
| CX-R-008 | GAP-X3 governance YAML inference: ADR-002 Phase 5B recommendations applied based on inferred YAML content that differs from actual files | MEDIUM | MEDIUM | ADR-002 Phase 5B | Audit actual `.governance.yaml` files before Stage 6 agent upgrades; verify inferred recommendations against actual file state |

### Evidence Gap Closure Path

| Gap | Current Status | Closes With |
|-----|---------------|-------------|
| GAP-X1 (UNTESTED causal framing comparison) | Phase 2 not yet executed | Phase 2 pilot C1-C7 execution (Stage 5) |
| GAP-X2 (T-004 frequency uncharacterized) | MVP manual test protocol defined; not yet executed | Phase 2 U-003 multi-turn conditions (Stage 5) |
| GAP-X3 (YAML content inference) | ~53% TASK-011 recs inferred | Stage 6 pre-implementation audit of `.governance.yaml` files |
| GAP-X4 (NPT-012 architectural) | Permanent within current runtime | External: Claude Code runtime architectural change |
| GAP-X5 (TASK-013 sampling ceiling) | 7 of 12 categories at 60-80 line samples | Stage 4 full pattern file reads before implementation |
| GAP-X6 (NPT-010/NPT-011 T1 evidence) | UNTESTED | Phase 2 C4/C5 conditions |
| GAP-X7 (routing disambiguation framing evidence) | UNTESTED | Phase 2 RT-M-008 routing record measurement (before/after) |
| GAP-X8 (AGREE-5 external validation) | Internally generated, adversary gate 0.953 | Future external validation study; not planned in current roadmap |

---

## Contradictions and Tensions Disclosure

Per P-022 (NEVER deceive about confidence, capabilities, or findings), the following contradictions and tensions MUST be disclosed explicitly. All were identified and analyzed above.

| ID | Tension/Contradiction | Nature | Resolution |
|----|-----------------------|--------|-----------|
| T-001 | ADR-001 "unconditional" label vs. implementation timing gate | Labeling tension, not substantive | Both claims are correct simultaneously; requires clarifying note in production documentation |
| T-002 | ADR-003 Component A and ADR-001 Group 3 target same SKILL.md sections via different mechanisms | Operational tension | Sequencing resolution: ADR-003 Component A first for routing disambiguation sections; ADR-001 Group 3 applies to non-routing content |
| T-003 | ADR-002 AGREE-5-derived NPT-010/NPT-011 candidates presented with high specificity | Epistemic tension | AGREE-5 is internally generated; candidates are provisional analyst judgment |
| T-004 | ADR-004 blocking gate (token discrepancy) with no deadline | Governance tension | Recommend 3-day time-box |
| T-005 | ADR-001 Group 4 nominally covers patterns/templates but does not specify which of 34 TASK-013 recommendations are addressed | Coverage tension | GAP 1 and GAP 2 require dedicated TASK-017/TASK-018 work items |

**ZERO contradictions found** between the four ADRs at the decision level. All tensions are resolvable via coordination, sequencing, or follow-up work items.

---

## Source Summary

| Source | Type | Key Contribution | Patterns/Tasks Contributed |
|--------|------|-----------------|--------------------------|
| `phase-5/ADR-001-npt014-elimination.md` (0.952 PASS) | Architecture Decision Record | Universal NPT-014 elimination policy; 4-group implementation sequencing; Phase 2 baseline preservation protocol; FMEA (RPN 150 highest risk: new NPT-014 introduction) | Task 1 dependencies; Task 2 Phase 2 gate; Task 6 Stages 1-4 |
| `phase-5/ADR-002-constitutional-upgrades.md` (0.951 PASS) | Architecture Decision Record | Hybrid Phase 5A/5B structure; 4-option weighted evaluation (Option C highest score at 7.05 but deferred for inaction-dominance reason); 8 sub-decisions with per-sub-decision PG-003 assessment; NPT-010/NPT-011 provisional candidates | Task 1 coordination; Task 2 Phase 5A non-contamination; Task 3 PG-003 per-sub-decision; Task 5 NPT-010/NPT-011; Task 6 Stage 2 and Stage 6 |
| `phase-5/ADR-003-routing-disambiguation.md` (0.957 PASS) | Architecture Decision Record | Two-component decision structure (unconditional content + conditional framing); 13-skill coverage matrix; Component A "not reversible by design"; S-002 agent self-diagnosis claim revised to aspirational | Task 1 dependencies; Task 2 Component A independence; Task 3 PG-003 Component A distinction; Task 5 NPT-009/NPT-010; Task 6 Stage 3; Task 7 Tension 2 |
| `phase-5/ADR-004-compaction-resilience.md` (0.955 PASS) | Architecture Decision Record | Three unconditional decisions; 5-dimension weighted criteria evaluation (Option B composite 2.90/3.00); token arithmetic (worst-case 745/850); L2 rank justification (ranks 11-12); MVP manual test protocol; vulnerability assessment framework | Task 1 L2 coordination; Task 2 unconditional classification; Task 3 minimal framing surface; Task 5 NPT-012; Task 6 Stage 1; Task 8 evidence |
| `barrier-4/synthesis.md` (v4.0.0, 0.950 PASS) | Cross-pollination synthesis | 130 total recommendations; 6 cross-cutting themes; dependency map (TASK-012→TASK-011→TASK-010); 3 priority groups (~20 MUST NOT omit, 78 SHOULD, ~27 MAY); Phase 5 ADR scope definition; A-11 hallucination resolution | Task 4 coverage analysis; Task 6 ordering constraints |
| `phase-3/taxonomy-pattern-catalog.md` (v3.0.0, 0.957 PASS) | Taxonomy | 14 named patterns (13 distinct techniques); AGREE-5 hierarchy (internally generated, NOT externally validated); evidence tier distribution; C1-C7 condition alignment | Task 5 NPT coverage map; Task 8 evidence tier classification |
| `barrier-1/supplemental-vendor-evidence.md` (R4, 0.951 PASS) | Vendor evidence | VS-001–VS-004; 33-instance catalog; three competing causal explanations (VS-002); IG-002 four-type vendor taxonomy | Task 8 T4 evidence characterization |

---

## PS Integration

| Field | Value |
|-------|-------|
| PS ID | PROJ-014 |
| Task ID | TASK-016 |
| Phase | Barrier 5 — Cross-ADR Coherence Synthesis |
| Artifact Path | `projects/PROJ-014-negative-prompting-research/orchestration/neg-prompting-20260227-001/barrier-5/synthesis.md` |
| Decision | No new architectural decisions; synthesis findings are: (1) four ADRs are internally coherent with no direct conflicts, (2) two gaps identified (TASK-013 patterns, TASK-014 template contrastive examples), (3) consolidated 6-stage implementation ordering with Phase 2 as the critical path gate |
| Status | PROPOSED (synthesis document, not a decision ADR) |
| Evidence Tier | T4 (compiled cross-ADR analysis); inherits evidence tiers from source ADRs |
| Reversibility | N/A (synthesis document; not itself a policy decision) |
| Next Agent Hint | Implementation planner for TASK-017 (patterns/templates gap closure); orchestration tracker for Stage 0-1 initiation; ps-architect for ADR-001 labeling clarification note |

### Key Findings for Downstream Handoff

1. **No direct conflicts between the four ADRs** — all tensions are coordination/sequencing issues, not architectural contradictions. The four ADRs form a coherent DAG with ADR-001 as the foundational enabler.

2. **Two coverage gaps require follow-up work items:** TASK-013 pattern documentation (28 SHOULD/MAY recommendations without a dedicated ADR) and TASK-014 template contrastive example upgrades (5 SHOULD recommendations). MUST create TASK-017 worktracker entry.

3. **Stage 2 coordination is the highest operational risk:** Both ADR-001 Group 2 and ADR-002 Phase 5A target `agent-development-standards.md`. NEVER apply these independently — a single coordinated commit is required.

4. **ADR-004 Decision 2 has a blocking implementation gate** (559 vs. 670 token discrepancy) that MUST be resolved before Stage 1 can begin. Recommend 3-day time-box.

5. **Phase 2 is the critical path** for the majority of conditional changes (ADR-002 Phase 5B, ADR-003 Component B). If Phase 2 is delayed beyond 6 months, ADR-003 Component B should default to community-preferred framing per its Failure Scenario 3 mitigation.

6. **AGREE-5 hierarchy ordering (ranks 9-11) remains internally generated and NOT externally validated.** All NPT-010/NPT-011 candidate rule selections and ADR-003 Component B framing decisions are provisional until Phase 2 confirms framing directionality.

7. **NEVER cite A-11** in any downstream implementation document. Confirmed hallucinated citation.

8. **NEVER present AGREE-5 as externally validated evidence** — it is an internally generated synthesis narrative that passed an internal adversary gate (0.953) but has not been reviewed by independent researchers.

### Confidence

**0.88** — HIGH for dependency analysis, conflict detection, and implementation ordering (directly derived from ADR content); MEDIUM for coverage completeness (GAP-X5 sampling ceiling affects confidence in TASK-013 pattern coverage assessment; GAP-X3 YAML inference affects confidence in ADR-002 Phase 5B agent-level recommendation completeness).

---

## Self-Review Checklist (H-15)

| Check | Status | Notes |
|-------|--------|-------|
| P-001: Do patterns accurately reflect source ADR content? | PASS | All dependency claims, PG-003 assessments, and coverage gaps traced to specific ADR sections with page-level citations |
| P-002: Is synthesis persisted to file? | PASS | Written to `barrier-5/synthesis.md` |
| P-004: Are all patterns citing sources? | PASS | Every synthesis finding cites the contributing ADR, section, and task source |
| P-011: Are all 8 synthesis tasks addressed? | PASS | Tasks 1-8 each have dedicated sections with complete analysis |
| P-020: Status PROPOSED? | PASS | Status: PROPOSED — synthesis document, user authority required for any policy changes derived from findings |
| P-022: Are contradictions and tensions disclosed? | PASS | Five tensions documented in Task 7 and Contradictions table; all confirmed non-conflicts have resolution paths; zero suppressions |
| C-001: A-11 not cited? | PASS | A-11 not cited anywhere; prohibition restated in Key Findings |
| C-002: AGREE-5 not presented as externally validated? | PASS | AGREE-5 labeled "internally generated, NOT externally validated" at every point of reference |
| C-003: NEVER present AGREE-5 as T1 or T3? | PASS | All AGREE-5 references carry "internally generated synthesis" label |
| H-23: Navigation table present? | PASS | Document Sections table at top with anchor links |
| P-022: Are coverage gaps disclosed? | PASS | GAP 1 (TASK-013 patterns, 28 recs), GAP 2 (TASK-014 template upgrades, 5 recs) explicitly identified in Task 4 |
| P-022: Are evidence tier gaps disclosed? | PASS | Task 8 evidence gap table with 8 identified gaps and resolution paths |

---

*Agent: ps-synthesizer*
*Task: TASK-016*
*Workflow: neg-prompting-20260227-001*
*Phase: Barrier 5 — Cross-ADR Coherence Synthesis*
*Version: 1.1.0*
*Created: 2026-02-28*
*Constitutional Compliance: Jerry Constitution v1.0 (P-003, P-020, P-022)*
*Format: L0/L1/L2 multi-level synthesis with 8-task analytical structure per synthesis task specification*
