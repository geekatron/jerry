# EN-303: Situational Applicability Mapping

<!--
TEMPLATE: Enabler
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
UPDATED: 2026-02-13 (Claude) — Enriched with ADR-EPIC002-001 decisions, Barrier-1 enf→adv handoff inputs, and ADR-derived requirements
PURPOSE: Map each selected adversarial strategy to specific contexts with use/avoid guidance and a decision tree
-->

> **Type:** enabler
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Enabler Type:** architecture
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-004
> **Owner:** —
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Input from ADR-EPIC002-001](#input-from-adr-epic002-001) | Ratified strategy selection decisions that constrain this enabler |
| [Input from Barrier-1 ENF-to-ADV Handoff](#input-from-barrier-1-enf-to-adv-handoff) | Enforcement constraints that inform strategy mapping |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Functional Requirements](#functional-requirements) | What the mapping must do |
| [Non-Functional Requirements](#non-functional-requirements) | Quality attributes and constraints |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Agent Assignments](#agent-assignments) | Which agents are used |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Change log |

---

## Summary

Map each of the 10 selected adversarial strategies (from EN-302, ratified via ADR-EPIC002-001) to specific usage contexts within Jerry. For each strategy, define: when to use it, when to avoid it, complementary strategy pairings, preconditions that must hold, and expected outcomes. The deliverable includes per-strategy applicability profiles and a strategy selection decision tree that guides agents and users to the right strategy for a given situation.

This mapping must account for the 5-layer enforcement architecture (from ADR-EPIC002-002 and Barrier-1 ENF-to-ADV handoff), platform portability constraints, token budget awareness, and the defense-in-depth compensation chain. The mapping transforms abstract strategy knowledge into actionable, context-aware guidance that is directly consumable by Jerry's agent architecture and enforcement mechanisms.

## Problem Statement

Knowing which 10 strategies to support is necessary but insufficient. Without situational guidance, agents and users face a paradox of choice: given a review task, which adversarial strategy should be applied? The wrong choice wastes effort (e.g., applying Red Team to a well-established design that needs refinement, not fundamental challenge) or misses critical issues (e.g., applying Blue Team when foundational assumptions need challenging). Furthermore, some strategies are complementary (Red Team followed by Blue Team) while others are redundant or counterproductive when combined. A formal applicability mapping with a decision tree eliminates guesswork and enables automated or semi-automated strategy selection.

Additionally, the ENF pipeline has established concrete enforcement constraints that this mapping must respect:
- **5-layer enforcement architecture** with distinct temporal firing order (L1 Static Context through L5 Post-Hoc Verification plus Process cross-cutting)
- **Platform portability gaps** (7 Family 1 Hook vectors are Claude Code-exclusive; core enforcement is 100% portable)
- **Token budget ceiling** (~12,476 tokens for L1 static context; ~600 tokens/session for L2 reinforcement)
- **4 RED systemic risks** (context rot, token budget, platform migration, rot+exhaustion feedback loop)
- **Defense-in-depth compensation chain** (each layer compensates for the failure mode of the layer above)

The mapping must produce strategy recommendations that are feasible within these constraints.

---

## Input from ADR-EPIC002-001

**Status:** ACCEPTED (ratified 2026-02-13)
**Location:** `EN-302-strategy-selection-framework/TASK-005-selection-ADR.md`

### Selected 10 Strategies (Authoritative Input)

| Rank | ID | Strategy | Score | Mechanistic Family | Token Budget |
|------|-----|----------|-------|--------------------|-------------|
| 1 | S-014 | LLM-as-Judge | 4.40 | Iterative Self-Correction | 2,000 (Ultra-Low) |
| 2 | S-003 | Steelman Technique | 4.30 | Dialectical Synthesis | 1,600 (Ultra-Low) |
| 3 | S-013 | Inversion Technique | 4.25 | Structured Decomposition | 2,100 (Ultra-Low) |
| 4 | S-007 | Constitutional AI Critique | 4.15 | Iterative Self-Correction | 8,000-16,000 (Medium) |
| 5 | S-002 | Devil's Advocate | 4.10 | Role-Based Adversarialism | 4,600 (Low) |
| 6 | S-004 | Pre-Mortem Analysis | 4.10 | Role-Based Adversarialism | 5,600 (Low) |
| 7 | S-010 | Self-Refine | 4.00 | Iterative Self-Correction | 2,000 (Ultra-Low) |
| 8 | S-012 | FMEA | 3.75 | Structured Decomposition | 9,000 (Medium) |
| 9 | S-011 | Chain-of-Verification (CoVe) | 3.75 | Structured Decomposition | 6,000 (Medium) |
| 10 | S-001 | Red Team Analysis | 3.35 | Role-Based Adversarialism | 7,000 (Medium) |

### 5 Excluded Strategies

- S-008 (Socratic Method, 3.25) -- Multi-turn complexity, partial coverage by S-002/S-007
- S-006 (ACH, 3.25) -- Specialized diagnostic, highest cognitive load
- S-005 (Dialectical Inquiry, 2.85) -- RED context window risk, 3-agent sync barriers
- S-009 (Multi-Agent Debate, 2.70) -- Highest risk in catalog, shared-model-bias limitation
- S-015 (PAE, 2.70) -- Reclassified as orchestration pattern (EN-307), not adversarial strategy

### Key ADR Properties Constraining This Mapping

- **Zero RED risks** in selected set -- mapping need not include risk mitigation for excluded strategies
- **14 SYN pairs, 26 COM pairs, 3 TEN pairs, 0 CON pairs** -- mapping must document these synergy/tension relationships
- **All 4 mechanistic families covered** -- mapping should leverage family diversity for complementary pairing
- **9/10 strategies stable** across 12 sensitivity configurations -- mapping can treat selection as stable
- **User note:** Revisit Option C (expanded strategy set with cross-model LLM involvement) in future epic

### Quality Layer Composition (from ADR)

| Quality Layer | Strategies Applied | Target Score Range | Trigger Level |
|---------------|-------------------|--------------------|---------------|
| L0: Self-Check | S-010 (Self-Refine) | ~0.60 to ~0.75 | Always |
| L1: Light Review | S-003 + S-010 + S-014 | ~0.75 to ~0.85 | C1 (Routine) |
| L2: Standard Critic | S-007 + S-002 + S-014 | ~0.85 to ~0.92+ | C2 (Standard) -- target operating layer |
| L3: Deep Review | L2 + S-004 + S-012 + S-013 | ~0.92 to ~0.96 | C3 (Significant) |
| L4: Tournament | L3 + S-001 + S-011 | ~0.96+ | C4 (Critical) |

---

## Input from Barrier-1 ENF-to-ADV Handoff

**Source:** `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/enf-to-adv/barrier-1-enf-to-adv-handoff.md`
**Confidence:** HIGH -- all data traceable to EN-402 TASK-001 through TASK-009

### 5-Layer Enforcement Architecture (Must Align Strategy Mapping)

| Layer | Timing | Context Rot | Token Cost | Strategy Mapping Implication |
|-------|--------|-------------|------------|------------------------------|
| L1: Static Context | Session start | VULNERABLE | ~12,476 | Strategies encoded as rules degrade with context rot; use only for foundational guidance |
| L2: Per-Prompt Reinforcement | Every prompt | IMMUNE by design | ~600/session | Strategies delivered via V-024 must be ultra-compact; budget is severely constrained |
| L3: Pre-Action Gating | Before tool calls | IMMUNE (external) | 0 | Strategies mapped to hooks are context-rot-immune; prefer this layer for mandatory enforcement |
| L4: Post-Action Validation | After tool calls | MIXED | 0-1,350 | Strategies requiring output inspection can leverage this layer |
| L5: Post-Hoc Verification | Commit/CI time | IMMUNE (external) | 0 | Strategies mapped to CI checks are deterministic and fully reliable |
| Process | Workflow level | IMMUNE | 0 | Strategy enforcement via process gates is the most reliable long-session mechanism |

### Platform Portability Constraints

- **100% portable:** L1 (rules), L5 (pre-commit, CI), Process vectors
- **Claude Code-specific:** L3/L4 hooks (V-001 PreToolUse, V-002 PostToolUse, V-003 SessionStart, V-005 UserPromptSubmit)
- **Windows:** 73% compatibility estimated; Claude Code hooks require WSL
- **Implication for mapping:** Strategy recommendations must NOT depend solely on Claude Code hooks; portable fallbacks required for every strategy

### Enforcement Gaps Where Adversarial Strategies Are Sole Defense

| Gap | Why Enforcement Cannot Fill It | ADV Strategy Opportunity |
|-----|-------------------------------|--------------------------|
| Semantic quality | AST checks structure, not meaning | Adversarial review patterns (S-002, S-003, S-007) |
| Context rot prevention | Inherent LLM limitation | Session management strategies, context hygiene |
| Novel violation types | AST rules are pre-defined | Adversarial exploration (S-001 Red Team) |
| Social engineering bypass | User can disable hooks (`--no-verify`) | Human-in-the-loop enforcement awareness |

### 4 RED Systemic Risks (Must Inform Strategy Mapping)

| Risk ID | Description | Mapping Constraint |
|---------|-------------|-------------------|
| R-SYS-001 | Context rot degrades VULNERABLE vectors (correlated failure) | Strategies must account for 40-60% effectiveness degradation at 50K+ tokens |
| R-SYS-002 | Token budget not optimized (25,700 vs. 12,476 target) | Strategies consuming tokens must be budgeted against enforcement envelope |
| R-SYS-003 | Platform migration renders hooks inoperative | Strategies must have portable fallbacks; cannot rely solely on hooks |
| R-SYS-004 | Context rot + token exhaustion negative feedback loop | Aggressive in-context adversarial patterns can worsen feedback loop; prefer token-efficient strategies |

### Feasibility Constraints for Strategy-to-Mechanism Mapping

| Mechanism Type | CAN Enforce | CANNOT Enforce |
|----------------|-------------|----------------|
| Automated (Hooks, CI, AST) | Deterministic rules, pattern-matchable violations, testable properties | Context-dependent judgments, semantic correctness |
| Process (Rules, Procedures) | Evidence collection, multi-step review, cross-agent validation | Real-time blocking, fully subjective assessment |
| Hybrid (Auto trigger + Agent execution) | Auto-triggered code review, completion gates, continuous self-critique | Full autonomy without any human/process checkpoint |

---

## Technical Approach

1. **Context Taxonomy** -- Define the dimensions that determine strategy applicability: review target type (code, architecture, requirements, research), review phase (early exploration, design, implementation, validation), risk level (critical, high, medium, low), artifact maturity (draft, reviewed, approved), and team composition (single agent, multi-agent, human-in-loop). **Must align with the decision criticality levels C1-C4 from ADR-EPIC002-001 and the 5-layer enforcement architecture from ADR-EPIC002-002.**
2. **Requirements Engineering** -- Define formal requirements for what the situational mapping must cover, ensuring completeness and traceability back to FEAT-004 objectives. **Must incorporate enforcement feasibility constraints from the Barrier-1 ENF-to-ADV handoff.**
3. **Per-Strategy Mapping** -- For each of the 10 selected strategies, create an applicability profile: recommended contexts (when to use), contraindicated contexts (when to avoid), complementary pairings (strategies that work well together), preconditions (what must be true before applying), and expected outcomes (what the strategy produces). **Each profile must include enforcement layer mapping (which enforcement layers can deliver this strategy) and platform portability classification.**
4. **Decision Tree Construction** -- Build a decision tree that takes context inputs (target type, phase, risk level, maturity, decision criticality C1-C4) and recommends one or more strategies. The tree must handle multi-strategy recommendations and fallback paths. **Must include token budget awareness (recommend lower-token strategies when budget is constrained) and platform-aware fallback paths (portable alternatives when hooks unavailable).**
5. **Adversarial Review** -- Apply Blue Team strategy to stress-test the decision tree for gaps, ambiguities, and edge cases. **Must specifically test: context rot scenarios (long sessions), platform portability scenarios (no Claude Code hooks), token budget exhaustion scenarios, and the 3 TEN (tension) strategy pairs.**

## Functional Requirements

| ID | Requirement | Source | Priority |
|----|-------------|--------|----------|
| FR-001 | Mapping SHALL cover all 10 selected strategies from ADR-EPIC002-001 | ADR-EPIC002-001 | HARD |
| FR-002 | Each strategy profile SHALL include: when to use, when to avoid, complementary pairings, preconditions, expected outcomes | EN-303 original scope | HARD |
| FR-003 | Each strategy profile SHALL include enforcement layer mapping indicating which of the 5 enforcement layers can deliver the strategy | Barrier-1 ENF-to-ADV | HARD |
| FR-004 | Decision tree SHALL accept decision criticality level (C1-C4) as input and map to quality layers L0-L4 | ADR-EPIC002-001 | HARD |
| FR-005 | Decision tree SHALL include platform-aware fallback paths for when Claude Code hooks (L3/L4) are unavailable | Barrier-1 ENF-to-ADV (Platform Constraints) | HARD |
| FR-006 | Decision tree SHALL include token budget awareness, recommending lower-token strategies when budget is constrained | Barrier-1 ENF-to-ADV (R-SYS-002, R-SYS-004) | HARD |
| FR-007 | Mapping SHALL document the 14 SYN pairs, 26 COM pairs, and 3 TEN pairs from ADR-EPIC002-001 with explicit pairing guidance | ADR-EPIC002-001 | MEDIUM |
| FR-008 | Mapping SHALL identify enforcement gaps where adversarial strategies are the sole defense (semantic quality, novel violations, context rot) | Barrier-1 ENF-to-ADV (Implementation Capabilities) | HARD |
| FR-009 | Decision tree SHALL handle the creator-critic-revision cycle (minimum 3 iterations) with strategy assignments per iteration | ADR-EPIC002-001 (Quality Gate Integration) | HARD |
| FR-010 | Each strategy profile SHALL include a portable delivery mechanism that does not depend on Claude Code hooks | Barrier-1 ENF-to-ADV (R-SYS-003) | HARD |
| FR-011 | Decision tree SHALL support mandatory escalation for artifacts touching `docs/governance/JERRY_CONSTITUTION.md` or `.claude/rules/` (auto-C3+) | ADR-EPIC002-001 (Enforcement Touchpoints) | MEDIUM |

## Non-Functional Requirements

| ID | Requirement | Source | Priority |
|----|-------------|--------|----------|
| NFR-001 | Strategy recommendations SHALL account for context rot: strategies targeting L1-dependent enforcement have diminished returns beyond ~20K tokens | Barrier-1 ENF-to-ADV (R-SYS-001) | HARD |
| NFR-002 | Token budget for in-context strategy guidance SHALL not exceed the enforcement envelope (~12,476 tokens for L1 + ~600/session for L2) | Barrier-1 ENF-to-ADV (R-SYS-002) | HARD |
| NFR-003 | All strategy recommendations SHALL be platform-portable at MODERATE enforcement level (L1 + L5 + Process) even without Claude Code hooks | Barrier-1 ENF-to-ADV (R-SYS-003) | HARD |
| NFR-004 | Mapping SHOULD avoid recommending aggressive in-context adversarial patterns that worsen the context rot + token exhaustion feedback loop (R-SYS-004) | Barrier-1 ENF-to-ADV (R-SYS-004) | MEDIUM |
| NFR-005 | Decision tree response time SHALL be O(1) -- lookup or traversal, not iterative computation | Design constraint | MEDIUM |
| NFR-006 | Mapping SHALL be consumable by both human users and automated agent orchestration systems | EN-303 original scope | HARD |
| NFR-007 | All strategy recommendations SHALL include traceability back to ADR-EPIC002-001 strategy IDs and Barrier-1 handoff sections | Traceability | MEDIUM |

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Define applicability dimensions and context taxonomy | pending | DESIGN | ps-architect |
| TASK-002 | Define requirements for situational mapping | pending | DESIGN | nse-requirements |
| TASK-003 | Map each strategy to contexts with use/avoid guidance | pending | DESIGN | ps-architect |
| TASK-004 | Create strategy selection decision tree | pending | DESIGN | ps-architect |
| TASK-005 | Adversarial review (Blue Team) | pending | TESTING | ps-critic |
| TASK-006 | Creator revision and final validation | pending | DEVELOPMENT | ps-architect, ps-validator |

### Task Dependencies

```
TASK-001 ──┐
            ├──> TASK-003 ──> TASK-004 ──> TASK-005 ──> TASK-006
TASK-002 ──┘
```

### Task Enrichment Notes (from ADR/Barrier-1 Inputs)

**TASK-001 (Context Taxonomy):**
- Taxonomy dimensions MUST include decision criticality levels C1-C4 from ADR-EPIC002-001
- Taxonomy MUST include enforcement layer availability as a context dimension (which of L1-L5 + Process are available in the current environment)
- Taxonomy SHOULD include token budget state (available vs. constrained) as a dimension
- Reference: ADR-EPIC002-001 Section "Decision Criticality Escalation", Barrier-1 ENF-to-ADV Section "5-Layer Enforcement Architecture"

**TASK-002 (Requirements):**
- Requirements MUST incorporate all FR-001 through FR-011 and NFR-001 through NFR-007 defined in this enabler
- Requirements MUST include traceability to both ADR-EPIC002-001 and ADR-EPIC002-002
- Requirements MUST address enforcement gap coverage (where adversarial strategies are sole defense)
- Reference: Barrier-1 ENF-to-ADV Section "Feasibility Constraints for Adversarial Strategy Mapping"

**TASK-003 (Per-Strategy Mapping):**
- Each of the 10 strategy profiles MUST include enforcement layer mapping from Barrier-1 ADV-to-ENF Section "Integration Requirements for ENF"
- Profiles MUST document which hooks/rules/CI checks deliver the strategy and which are portable fallbacks
- Profiles MUST document the 14 SYN + 26 COM + 3 TEN pairings from ADR-EPIC002-001
- Token budget per strategy must reference the Ultra-Low/Low/Medium tiers from ADR-EPIC002-001
- Reference: Barrier-1 ADV-to-ENF Sections "Integration Requirements for ENF" and "Enforcement Touchpoints"

**TASK-004 (Decision Tree):**
- Tree inputs MUST include decision criticality (C1-C4), platform context, and token budget state
- Tree MUST map C1→L0/L1, C2→L2, C3→L3, C4→L4 as primary quality layers
- Tree MUST include fallback paths for platform portability (no hooks → use rules + process only)
- Tree MUST implement the creator-critic-revision cycle strategy assignments per iteration
- Tree MUST enforce automatic escalation to C3+ for governance/constitution artifacts
- Reference: ADR-EPIC002-001 Sections "Quality Layer Composition" and "Decision Criticality Escalation"

**TASK-005 (Adversarial Review):**
- Blue Team MUST specifically test: context rot scenarios (50K+ tokens), platform portability (no Claude Code hooks), token budget exhaustion, the 3 TEN strategy pairs, and the 4 RED systemic risks
- Blue Team MUST verify that every strategy has a portable delivery mechanism (not solely dependent on hooks)
- Reference: Barrier-1 ENF-to-ADV Section "Risk Summary"

**TASK-006 (Revision and Validation):**
- Validation MUST confirm all FR/NFR requirements are satisfied
- Validation MUST confirm traceability to both ADRs and both Barrier-1 handoffs
- Validation MUST confirm the decision tree produces correct recommendations for at least 5 representative scenarios spanning C1-C4

## Acceptance Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| 1 | Context taxonomy defines at least 4 applicability dimensions, including decision criticality (C1-C4) and enforcement layer availability | EN-303 original + ADR-EPIC002-001 | [ ] |
| 2 | All 10 selected strategies from ADR-EPIC002-001 have complete applicability profiles | ADR-EPIC002-001 | [ ] |
| 3 | Each profile includes: when to use, when to avoid, pairings, preconditions, outcomes, enforcement layer mapping, platform portability classification | EN-303 original + Barrier-1 ENF-to-ADV | [ ] |
| 4 | Strategy selection decision tree is complete and covers all context combinations including C1-C4 criticality levels | ADR-EPIC002-001 | [ ] |
| 5 | Decision tree handles multi-strategy recommendations with quality layer composition (L0-L4) | ADR-EPIC002-001 | [ ] |
| 6 | Decision tree has fallback paths for ambiguous contexts AND platform portability fallbacks (no hooks available) | Barrier-1 ENF-to-ADV (R-SYS-003) | [ ] |
| 7 | Decision tree includes token budget awareness and does not recommend strategies that exceed available budget | Barrier-1 ENF-to-ADV (R-SYS-002, R-SYS-004) | [ ] |
| 8 | Mapping accounts for 5-layer enforcement architecture and identifies which layers deliver each strategy | Barrier-1 ENF-to-ADV | [ ] |
| 9 | Mapping identifies enforcement gaps where adversarial strategies are the sole defense (semantic quality, novel violations) | Barrier-1 ENF-to-ADV | [ ] |
| 10 | Blue Team adversarial review completed with documented feedback, including context rot, portability, and token budget scenarios | EN-303 original + Barrier-1 risks | [ ] |
| 11 | Requirements traceability to FEAT-004 objectives, ADR-EPIC002-001, ADR-EPIC002-002, and Barrier-1 handoffs confirmed | Traceability | [ ] |
| 12 | All strategy recommendations have portable delivery mechanisms (not solely dependent on Claude Code hooks) | Barrier-1 ENF-to-ADV (R-SYS-003) | [ ] |
| 13 | Final validation confirms all FR/NFR requirements met | Validation | [ ] |

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| ps-architect | /problem-solving | Creator -- taxonomy, mapping, decision tree, revision | TASK-001, TASK-003, TASK-004, TASK-006 |
| ps-critic | /problem-solving | Adversarial -- Blue Team review of decision tree | TASK-005 |
| nse-requirements | /nasa-se | Requirements engineering -- formal requirements definition | TASK-002 |
| ps-validator | /problem-solving | Validation -- final quality gate | TASK-006 |

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-004](../FEAT-004-adversarial-strategy-research.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-302 | Requires the selected 10 strategies as input (ADR-EPIC002-001 ACCEPTED) |
| depends_on | ADR-EPIC002-001 | Ratified strategy selection -- authoritative input for all 10 strategy profiles |
| depends_on | ADR-EPIC002-002 | Ratified enforcement prioritization -- 5-layer architecture constrains strategy mapping |
| depends_on | Barrier-1 ENF-to-ADV | Enforcement constraints, platform portability, token budget, 4 RED systemic risks |
| depends_on | Barrier-1 ADV-to-ENF | Strategy-to-enforcement integration requirements, enforcement touchpoints |
| blocks | EN-304 | Skill enhancement depends on situational mapping and decision tree |

### Cross-Pipeline References
| Artifact | Path | Content Used |
|----------|------|-------------|
| Barrier-1 ADV-to-ENF Handoff | `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/adv-to-enf/barrier-1-adv-to-enf-handoff.md` | Strategy-to-enforcement mapping, integration requirements, enforcement touchpoints, quality gate integration |
| Barrier-1 ENF-to-ADV Handoff | `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/enf-to-adv/barrier-1-enf-to-adv-handoff.md` | Priority matrix, 5-layer architecture, platform constraints, feasibility constraints, 4 RED systemic risks |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with task decomposition. Depends on EN-302 strategy selection. |
| 2026-02-13 | Claude | in_progress | Enriched with ADR-EPIC002-001 (ACCEPTED) inputs: 10 selected strategies, quality layer composition, decision criticality levels, synergy/tension pairs. Added Barrier-1 ENF-to-ADV handoff inputs: 5-layer enforcement architecture, platform portability constraints, token budget ceilings, 4 RED systemic risks, enforcement gaps, feasibility constraints. Added FR-001 through FR-011, NFR-001 through NFR-007. Expanded acceptance criteria from 9 to 13 items. Enriched all task descriptions with ADR/Barrier-1 references. Updated navigation table. |
