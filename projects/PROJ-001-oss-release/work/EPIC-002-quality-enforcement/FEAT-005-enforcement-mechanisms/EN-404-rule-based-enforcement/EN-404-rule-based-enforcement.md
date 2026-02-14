# EN-404: Rule-Based Enforcement Enhancement

<!--
TEMPLATE: Enabler
VERSION: 2.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
UPDATED: 2026-02-13 (Claude) — Enriched with ADR-EPIC002-002 decisions, Barrier-1 adv→enf handoff inputs, and ADR-derived requirements
PURPOSE: Enhance .claude/rules/ files with HARD enforcement language and tiered enforcement strategy
-->

> **Type:** enabler
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-005
> **Owner:** —
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Input from ADR-EPIC002-002](#input-from-adr-epic002-002) | Ratified enforcement architecture decisions constraining L1 rule design |
| [Input from Barrier-1 ADV-to-ENF Handoff](#input-from-barrier-1-adv-to-enf-handoff) | Adversarial strategy requirements that rules must support |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Functional Requirements](#functional-requirements) | What the rules must do |
| [Non-Functional Requirements](#non-functional-requirements) | Quality attributes and constraints |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Agent Assignments](#agent-assignments) | Which agents are used |
| [Related Items](#related-items) | Dependencies |
| [History](#history) | Change log |

---

## Summary

Enhance `.claude/rules/` files with HARD enforcement language that prevents Claude from bypassing the quality framework. Implement tiered enforcement based on task complexity aligned with the decision criticality levels (C1-C4) from ADR-EPIC002-001. Add explicit quality gate requirements to rule files. Optimize total rule token budget from the current ~25,700 tokens down to the ADR-EPIC002-002 target of ~12,476 tokens (a 51.5% reduction), while maintaining or increasing enforcement effectiveness.

Rules constitute the L1 (Static Context) layer of the 5-layer hybrid enforcement architecture ratified in ADR-EPIC002-002. L1 is the foundation of all enforcement -- it sets the behavioral baseline at session start. However, L1 is the only layer VULNERABLE to context rot (degrades after ~20K tokens), which makes token efficiency critical: every unnecessary token in L1 accelerates rot onset.

Rules must also encode the adversarial strategy requirements from the Barrier-1 ADV-to-ENF handoff, specifically S-007 (Constitutional AI -- rules ARE the constitution), S-003 (Steelman), S-010 (Self-Refine), S-014 (LLM-as-Judge), S-002 (Devil's Advocate), and S-013 (Inversion).

## Problem Statement

Current `.claude/rules/` files provide guidance but lack HARD enforcement language that prevents Claude from bypassing quality requirements. Without explicit enforcement tiers and quality gate requirements embedded in rule files, Claude may skip mandatory quality steps during complex tasks. The rules need to distinguish between simple tasks (where lightweight enforcement suffices) and complex tasks (where full quality framework engagement is mandatory).

The ratified ADR-EPIC002-002 identifies critical issues with the current L1 layer:

- **Token budget overrun:** Current rules consume ~25,700 tokens (15.7% of 200K context window). The ADR target is ~12,476 tokens (7.6%), requiring a 51.5% reduction. Every excess token in L1 accelerates context rot onset.
- **No HARD/MEDIUM/SOFT enforcement tiers:** Current rules do not distinguish between constraints that are absolute (HARD -- cannot be overridden), advisory (MEDIUM -- can be overridden with justification), and aspirational (SOFT -- best practice guidance).
- **No context reinforcement support:** L1 rules do not identify which content is most critical for L2 (Per-Prompt Reinforcement via V-024) to re-inject when context rot degrades L1. Rules must tag their most critical content for L2 consumption.
- **82.5% token concentration risk:** 82.5% of enforcement tokens (12,476 of 15,126 total) are allocated to L1. This makes L1 optimization the single highest-leverage activity for the entire enforcement framework.

Additionally, the Barrier-1 ADV-to-ENF handoff requires that rules encode six adversarial strategies (S-007, S-003, S-010, S-014, S-002, S-013) as static enforcement language.

---

## Input from ADR-EPIC002-002

**Status:** ACCEPTED (ratified 2026-02-13)
**Location:** `EN-402-enforcement-priority-analysis/TASK-005-enforcement-ADR.md`

### L1 Layer Specification

| Property | Value | Implication for EN-404 |
|----------|-------|----------------------|
| Layer | L1: Static Context | Rules loaded at session start via `.claude/rules/` and `CLAUDE.md` |
| Timing | Session start | One-time load; no refresh until next session |
| Context Rot | VULNERABLE (CRR=1-2) | Only enforcement layer that degrades; optimize for minimal token footprint |
| Token Budget Target | ~12,476 tokens (7.6% of 200K) | Must reduce from current ~25,700 -- a 51.5% reduction |
| Compensated By | L2 (Per-Prompt Reinforcement via V-024) | Rules must identify critical content for L2 re-injection |

### Rule-Family Vectors from Priority Matrix

| Vector | Name | WCS | Tier | Description |
|--------|------|-----|------|-------------|
| V-008 | CLAUDE.md navigation | 3.82 | Tier 2 | Top-level behavioral anchoring document |
| V-009 | Constitution reference | 3.82 | Tier 2 | JERRY_CONSTITUTION.md governance reference |
| V-010 | Critical constraints block | 3.82 | Tier 2 | HARD rules: P-003, P-020, P-022 |
| V-015 | Coding standards rules | 3.56 | Tier 2 | Type hints, docstrings, naming conventions |
| V-016 | Architecture standards rules | 3.56 | Tier 2 | Hexagonal architecture, layer boundaries |
| V-017 | Testing standards rules | 3.56 | Tier 2 | Test pyramid, BDD cycle, coverage |
| V-026 | Rule file enforcement language | 3.56 | Tier 2 | HARD/MEDIUM/SOFT enforcement tiers |

### Token Budget Optimization Target

| Component | Current | Target | Reduction |
|-----------|---------|--------|-----------|
| CLAUDE.md | ~3,200 | ~2,000 | 37.5% |
| .claude/rules/ (7 files) | ~22,500 | ~10,476 | 53.4% |
| **Total L1** | **~25,700** | **~12,476** | **51.5%** |

### Defense-in-Depth Context for L1

| Layer | Compensates For | Compensated By |
|-------|----------------|----------------|
| **L1 (Static Context) -- THIS ENABLER** | N/A (foundation layer) | L2 (V-024 re-injects critical rules when L1 degrades) |
| L2 (Per-Prompt Reinforcement) | L1 context rot | L3 (deterministic blocking) |

**Key architectural property:** L1 degradation is EXPECTED and DESIGNED FOR. The architecture does not rely on L1 remaining effective throughout long sessions. However, L1 effectiveness in the first ~20K tokens establishes the behavioral foundation that L2 then maintains.

### Implementation Phase

- **Phase 1 (Foundation):** L1 rules + L5 CI -- **this enabler is Phase 1 core work**
- Rules must be optimized BEFORE Phase 3 (L2 enhancement), because L2 (V-024) depends on knowing which L1 content is most critical for re-injection

---

## Input from Barrier-1 ADV-to-ENF Handoff

**Source:** `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/adv-to-enf/barrier-1-adv-to-enf-handoff.md`
**Confidence:** HIGH -- all data traceable to EN-301/EN-302

### Adversarial Strategies to Encode as Rules

| Strategy | Rule Integration Requirement | Priority |
|----------|------------------------------|----------|
| S-007 (Constitutional AI) | The rules themselves ARE the constitution. Enhance existing rules with HARD enforcement language requiring principle-by-principle evaluation. | HARD |
| S-003 (Steelman) | Add rule requiring charitable reconstruction before critique. "Before criticizing any proposal, first present the strongest version of the argument." | HARD |
| S-010 (Self-Refine) | Add rule requiring self-review before submitting outputs. "Review your own output for completeness, accuracy, and quality before presenting it." | HARD |
| S-014 (LLM-as-Judge) | Add rule requiring explicit quality scoring. "All deliverables must include a quality score against defined rubrics. Target: >= 0.92." | HARD |
| S-002 (Devil's Advocate) | Add rule requiring consideration of counterarguments. "Before finalizing any decision or recommendation, explicitly consider and document the strongest counterargument." | MEDIUM |
| S-013 (Inversion) | Add rule for failure mode consideration. "Before proposing any solution, identify at least 3 ways it could fail." | MEDIUM |

### Quality Gate Integration via Rules

- **0.92 quality threshold** must be stated as a HARD rule in the quality enforcement rule file
- **Creator-critic-revision cycle** (minimum 3 iterations) must be encoded as a HARD rule for C2+ decisions
- **Decision criticality levels (C1-C4)** must be defined in rules with enforcement tier mapping
- **Mandatory escalation** for governance/constitution artifacts must be encoded as HARD rule

### Enforcement Tier Language (from ADR)

Rules must use consistent enforcement language:

| Tier | Language | Meaning | Example |
|------|----------|---------|---------|
| **HARD** | "MUST", "SHALL", "NEVER", "FORBIDDEN" | Cannot be overridden. Violations will be blocked. | "Domain layer MUST NOT import infrastructure." |
| **MEDIUM** | "SHOULD", "RECOMMENDED", "PREFER" | Can be overridden with documented justification. | "Tests SHOULD follow AAA pattern." |
| **SOFT** | "MAY", "CONSIDER", "OPTIONAL" | Best practice guidance. | "MAY use property-based testing for edge cases." |

### Token Budget Awareness for Strategy Encoding

- All 6 strategies must be encoded within the ~10,476 token budget for `.claude/rules/`
- Prefer ultra-compact phrasing: one-sentence HARD rules over paragraph explanations
- Strategy encoding MUST be additive to existing rule content, not duplicative
- L2 reinforcement (V-024) will re-inject the most critical rules at ~600 tokens/session, so rules must tag which content is highest priority for re-injection

---

## Technical Approach

1. **Audit existing `.claude/rules/` files** to identify enforcement gaps where Claude could bypass quality requirements. **Audit must measure current token count per file and identify reduction opportunities to reach the ~12,476 total target.**
2. **Define a tiered enforcement strategy** that distinguishes simple vs complex tasks. **Must align with C1-C4 decision criticality levels from ADR-EPIC002-001 and HARD/MEDIUM/SOFT enforcement tiers from ADR-EPIC002-002.**
3. **Design HARD enforcement language patterns** that are unambiguous and non-overridable. **Must use the enforcement tier language (HARD/MEDIUM/SOFT) consistently across all rule files.**
4. **Enhance mandatory-skill-usage.md** with stronger enforcement directives. **Must encode S-003 (Steelman), S-010 (Self-Refine), S-014 (LLM-as-Judge), S-002 (Devil's Advocate), and S-013 (Inversion) as rule-based directives.**
5. **Enhance project-workflow.md** with quality gate checkpoints. **Must encode the 0.92 quality threshold, creator-critic-revision cycle, and C1-C4 escalation as HARD rules.**
6. **Create a new quality-enforcement.md rule file** that codifies the enforcement framework. **Must include: enforcement tier definitions, quality gate thresholds, decision criticality levels, adversarial strategy trigger conditions, and context reinforcement tagging for L2 consumption.**
7. **Optimize token budget** across all rule files to achieve the ~12,476 token target. **Must identify and eliminate: redundant content, verbose explanations that can be replaced with concise HARD rules, and low-value content that does not contribute to enforcement.**
8. **Tag critical content for L2 re-injection** so that EN-403 (UserPromptSubmit hook delivering V-024) knows which rules are highest priority for context reinforcement.
9. **Subject all changes to adversarial review** (Red Team + Strawman) to identify bypass vectors. **Red Team must specifically attempt: exploiting MEDIUM/SOFT rules to override HARD rules, finding gaps in enforcement tier coverage, and testing context rot scenarios where rules degrade.**
10. **Revise based on adversarial findings** and verify against requirements.

## Functional Requirements

| ID | Requirement | Source | Priority |
|----|-------------|--------|----------|
| FR-001 | All `.claude/rules/` files SHALL use consistent HARD/MEDIUM/SOFT enforcement tier language | ADR-EPIC002-002 (V-026) | HARD |
| FR-002 | Total L1 token budget (CLAUDE.md + all rules) SHALL NOT exceed ~12,476 tokens | ADR-EPIC002-002 (Token Budget) | HARD |
| FR-003 | Rules SHALL encode S-007 (Constitutional AI) as HARD enforcement requiring principle-by-principle evaluation | Barrier-1 ADV-to-ENF (Rules Integration) | HARD |
| FR-004 | Rules SHALL encode S-003 (Steelman) requiring charitable reconstruction before critique | Barrier-1 ADV-to-ENF (Rules Integration) | HARD |
| FR-005 | Rules SHALL encode S-010 (Self-Refine) requiring self-review before presenting outputs | Barrier-1 ADV-to-ENF (Rules Integration) | HARD |
| FR-006 | Rules SHALL encode S-014 (LLM-as-Judge) requiring explicit quality scoring with >= 0.92 threshold | Barrier-1 ADV-to-ENF (Rules Integration) | HARD |
| FR-007 | Rules SHALL encode S-002 (Devil's Advocate) requiring counterargument consideration for decisions | Barrier-1 ADV-to-ENF (Rules Integration) | MEDIUM |
| FR-008 | Rules SHALL encode S-013 (Inversion) requiring failure mode identification for proposed solutions | Barrier-1 ADV-to-ENF (Rules Integration) | MEDIUM |
| FR-009 | Rules SHALL define decision criticality levels C1-C4 with enforcement tier mapping | ADR-EPIC002-001 (Decision Criticality) | HARD |
| FR-010 | Rules SHALL define the creator-critic-revision cycle (minimum 3 iterations) as HARD enforcement for C2+ decisions | ADR-EPIC002-001 (Quality Gate Integration) | HARD |
| FR-011 | Rules SHALL define mandatory escalation to C3+ for artifacts touching `docs/governance/` or `.claude/rules/` | ADR-EPIC002-001 (Enforcement Touchpoints) | HARD |
| FR-012 | Rules SHALL tag highest-priority content for L2 re-injection via V-024 context reinforcement | ADR-EPIC002-002 (L2 dependency on L1) | HARD |
| FR-013 | A new quality-enforcement.md rule file SHALL be created codifying the enforcement framework | EN-404 original scope | HARD |
| FR-014 | All existing rule files SHALL be audited for enforcement gaps with findings documented | EN-404 original scope | HARD |

## Non-Functional Requirements

| ID | Requirement | Source | Priority |
|----|-------------|--------|----------|
| NFR-001 | Total token count for all L1 content SHALL NOT exceed 12,476 tokens (7.6% of 200K context window) | ADR-EPIC002-002 (R-SYS-002) | HARD |
| NFR-002 | Token reduction from current ~25,700 to target ~12,476 SHALL NOT reduce enforcement effectiveness -- must maintain or increase it | ADR-EPIC002-002 (Token Budget Optimization) | HARD |
| NFR-003 | Rules SHALL be context-rot-aware: most critical rules placed earliest in each file (recency bias mitigation) and tagged for L2 re-injection | ADR-EPIC002-002 (R-SYS-001) | HARD |
| NFR-004 | Enforcement language SHALL be unambiguous: HARD rules must have no interpretive wiggle room for Claude to rationalize non-compliance | ADR-EPIC002-002 (V-026) | HARD |
| NFR-005 | Rules SHALL NOT worsen the context rot + token exhaustion feedback loop (R-SYS-004): prefer concise HARD rules over verbose explanations | ADR-EPIC002-002 (R-SYS-004) | MEDIUM |
| NFR-006 | All rules SHALL be 100% platform-portable (plain text markdown, no platform-specific directives) | Barrier-1 ENF-to-ADV (Platform Portability) | HARD |
| NFR-007 | HARD enforcement rules SHALL be distinguishable from MEDIUM/SOFT rules both visually (formatting) and semantically (language) | ADR-EPIC002-002 (V-026) | MEDIUM |
| NFR-008 | Rule optimization SHALL preserve the existing navigation table standard (NAV-001 through NAV-006) in all modified files | Jerry markdown-navigation-standards | MEDIUM |

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Define requirements for rule-based enforcement | pending | DESIGN | nse-requirements |
| TASK-002 | Audit existing .claude/rules/ files for enforcement gaps | pending | RESEARCH | ps-investigator |
| TASK-003 | Design tiered enforcement strategy (simple vs complex tasks) | pending | DESIGN | ps-architect |
| TASK-004 | Design HARD enforcement language patterns | pending | DESIGN | ps-architect |
| TASK-005 | Implement enhanced mandatory-skill-usage.md | pending | DEVELOPMENT | ps-architect |
| TASK-006 | Implement enhanced project-workflow.md | pending | DEVELOPMENT | ps-architect |
| TASK-007 | Create new quality-enforcement.md rule file | pending | DEVELOPMENT | ps-architect |
| TASK-008 | Adversarial review (ps-critic with Red Team + Strawman) | pending | TESTING | ps-critic |
| TASK-009 | Creator revision | pending | DEVELOPMENT | ps-architect |
| TASK-010 | Verification against requirements | pending | TESTING | nse-verification |

### Task Dependencies

```
TASK-001 ──► TASK-002 ──► TASK-003 ──► TASK-004
                                          │
                                          ▼
                              ┌─── TASK-005
                              ├─── TASK-006
                              └─── TASK-007
                                      │
                                      ▼
                                  TASK-008 ──► TASK-009 ──► TASK-010
```

### Task Enrichment Notes (from ADR/Barrier-1 Inputs)

**TASK-001 (Requirements):**
- Requirements MUST incorporate all FR-001 through FR-014 and NFR-001 through NFR-008 defined in this enabler
- Requirements MUST trace to ADR-EPIC002-002 vectors (V-008, V-009, V-010, V-015, V-016, V-017, V-026) and the L1 layer specification
- Requirements MUST include the token budget target (~12,476 total, ~10,476 for rules, ~2,000 for CLAUDE.md)
- Requirements MUST include adversarial strategy encoding requirements from Barrier-1 ADV-to-ENF
- Reference: ADR-EPIC002-002, Barrier-1 ADV-to-ENF Section "Rules (Static Context) -- EN-404"

**TASK-002 (Audit):**
- Audit MUST measure token count per rule file (current state)
- Audit MUST identify: redundant content, verbose explanations replaceable with concise rules, low-value content, missing HARD enforcement language, missing adversarial strategy encoding
- Audit MUST map each existing rule to an enforcement tier (HARD/MEDIUM/SOFT)
- Audit MUST identify content suitable for tagging as L2 re-injection priority
- Reference: ADR-EPIC002-002 Section "Token Budget Optimization Target"

**TASK-003 (Tiered Enforcement Design):**
- Tiers MUST align with C1-C4 decision criticality from ADR-EPIC002-001
- Design MUST define: what enforcement level applies at each criticality tier, which adversarial strategies are mandatory vs optional at each tier, and what the token budget allocation is per tier
- Design MUST include the mandatory escalation rule for governance/constitution artifacts (auto-C3+)
- Reference: ADR-EPIC002-001 Section "Decision Criticality Escalation", Barrier-1 ADV-to-ENF Section "Quality Gate Integration"

**TASK-004 (HARD Language Design):**
- Language patterns MUST use the HARD/MEDIUM/SOFT vocabulary from ADR-EPIC002-002 consistently
- Patterns MUST be compact (one-sentence rules preferred) to support token budget target
- Patterns MUST be unambiguous: no room for interpretive rationalization by Claude
- Must define visual formatting conventions that distinguish HARD from MEDIUM/SOFT rules
- Reference: ADR-EPIC002-002 Section "Enforcement Tier Language"

**TASK-005 (Mandatory Skill Usage Enhancement):**
- MUST encode S-003 (Steelman), S-010 (Self-Refine), S-014 (LLM-as-Judge), S-002 (Devil's Advocate), S-013 (Inversion) as mandatory skill directives
- MUST use HARD enforcement language for mandatory strategies and MEDIUM for recommended strategies
- MUST stay within the per-file token budget allocation from TASK-002 audit
- Reference: Barrier-1 ADV-to-ENF Section "Rules (Static Context) -- EN-404"

**TASK-006 (Project Workflow Enhancement):**
- MUST encode the 0.92 quality gate threshold as a HARD rule
- MUST encode the creator-critic-revision cycle (minimum 3 iterations for C2+) as a HARD rule
- MUST encode C1-C4 decision criticality with quality layer mapping
- MUST stay within the per-file token budget allocation
- Reference: ADR-EPIC002-001 Section "Quality Gate Integration"

**TASK-007 (Quality Enforcement Rule File):**
- New file MUST codify: enforcement tier definitions (HARD/MEDIUM/SOFT), quality gate thresholds (0.92), decision criticality levels (C1-C4), adversarial strategy trigger conditions, context reinforcement tagging scheme for L2/V-024
- File MUST be concise enough to fit within the remaining token budget after optimization of existing files
- File MUST be the single authoritative source for enforcement framework definitions (avoid duplication across other rule files)
- Reference: ADR-EPIC002-002, Barrier-1 ADV-to-ENF Section "Quality Gate Integration"

**TASK-008 (Adversarial Review):**
- Red Team MUST specifically attempt: exploiting MEDIUM/SOFT rules to override HARD rules, finding gaps in enforcement tier coverage, testing whether Claude can rationalize bypassing HARD rules via creative interpretation, testing context rot scenarios where L1 rules degrade and identifying which rules degrade first
- Strawman MUST test: whether enforcement language is genuinely unambiguous, whether token budget target is achievable without reducing effectiveness, whether L2 re-injection tagging is sufficient
- Must verify that the 4 RED systemic risks (R-SYS-001 through R-SYS-004) are addressed in the rule design
- Reference: Barrier-1 ENF-to-ADV Section "Risk Summary"

**TASK-009 (Creator Revision):**
- Revision MUST address all findings from adversarial review
- Revision MUST verify token budget compliance (re-measure total token count)
- Revision MUST confirm all 6 adversarial strategies are encoded

**TASK-010 (Verification):**
- Verification MUST confirm total L1 token count is within ~12,476 target
- Verification MUST confirm all FR/NFR requirements are satisfied
- Verification MUST confirm enforcement effectiveness is maintained or improved (comparison against pre-optimization baseline)
- Verification MUST confirm L2 re-injection tags are present and correctly prioritized

## Acceptance Criteria

| # | Criterion | Source | Verified |
|---|-----------|--------|----------|
| 1 | All `.claude/rules/` files audited for enforcement gaps with findings documented, including per-file token counts | EN-404 original + ADR-EPIC002-002 | [ ] |
| 2 | Tiered enforcement strategy defined aligning with C1-C4 decision criticality levels | ADR-EPIC002-001 | [ ] |
| 3 | HARD/MEDIUM/SOFT enforcement language patterns documented and applied consistently across all rule files | ADR-EPIC002-002 (V-026) | [ ] |
| 4 | mandatory-skill-usage.md enhanced with adversarial strategy directives (S-003, S-010, S-014, S-002, S-013) | Barrier-1 ADV-to-ENF | [ ] |
| 5 | project-workflow.md enhanced with quality gate checkpoints (0.92 threshold, creator-critic-revision cycle, C1-C4) | ADR-EPIC002-001 + Barrier-1 ADV-to-ENF | [ ] |
| 6 | New quality-enforcement.md rule file created with enforcement framework definitions | EN-404 original scope | [ ] |
| 7 | Total L1 token budget (CLAUDE.md + all rules) does not exceed ~12,476 tokens | ADR-EPIC002-002 | [ ] |
| 8 | Token reduction does not reduce enforcement effectiveness (maintained or improved) | ADR-EPIC002-002 | [ ] |
| 9 | Critical rule content tagged for L2 re-injection via V-024 context reinforcement | ADR-EPIC002-002 (L2 dependency) | [ ] |
| 10 | S-007 (Constitutional AI) encoded as HARD enforcement in rules | Barrier-1 ADV-to-ENF | [ ] |
| 11 | Adversarial review completed with no unmitigated bypass vectors, including enforcement tier exploitation and context rot scenarios | EN-404 original + Barrier-1 risks | [ ] |
| 12 | All changes verified against defined FR/NFR requirements with traceability to ADR-EPIC002-001, ADR-EPIC002-002, and Barrier-1 handoffs | Traceability | [ ] |
| 13 | Mandatory escalation rule encoded for governance/constitution artifacts (auto-C3+) | ADR-EPIC002-001 | [ ] |

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| ps-architect | problem-solving | Creator - designs and implements enforcement enhancements | DESIGN, DEVELOPMENT |
| ps-critic | problem-solving | Adversarial reviewer - Red Team + Strawman analysis | TESTING |
| ps-investigator | problem-solving | Gap auditor - audits existing rules for enforcement weaknesses | RESEARCH |
| nse-requirements | nasa-se | Requirements engineer - defines enforcement requirements | DESIGN |
| nse-verification | nasa-se | Verification engineer - validates against requirements | TESTING |

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-005](../FEAT-005-enforcement-mechanisms.md)

### Dependencies
| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-402 | Enforcement priority analysis must be completed to inform rule enhancement strategy |
| depends_on | ADR-EPIC002-002 | Ratified enforcement prioritization -- L1 layer specification, token budget target, enforcement tier language |
| depends_on | Barrier-1 ADV-to-ENF | Adversarial strategy encoding requirements (S-007, S-003, S-010, S-014, S-002, S-013) |
| blocks | EN-403 | Hook-based enforcement (L2) depends on L1 identifying critical content for V-024 re-injection |
| related_to | EN-405 | Session context enforcement -- overlaps on session-start quality context |

### Cross-Pipeline References
| Artifact | Path | Content Used |
|----------|------|-------------|
| Barrier-1 ADV-to-ENF Handoff | `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/adv-to-enf/barrier-1-adv-to-enf-handoff.md` | Adversarial strategy rule integration requirements (6 strategies), quality gate integration, enforcement tier language, token budget awareness |
| Barrier-1 ENF-to-ADV Handoff | `orchestration/epic002-crosspoll-20260213-001/cross-pollination/barrier-1/enf-to-adv/barrier-1-enf-to-adv-handoff.md` | Token budget concentration risk (82.5% in L1), 4 RED systemic risks, defense-in-depth chain (L2 compensates L1 rot) |

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with task decomposition. |
| 2026-02-13 | Claude | in_progress | Enriched with ADR-EPIC002-002 (ACCEPTED) inputs: L1 layer specification (token budget ~12,476 target, 51.5% reduction from ~25,700), rule-family vectors (V-008/V-009/V-010/V-015-V-017/V-026), HARD/MEDIUM/SOFT enforcement tier language, token budget optimization targets per component, defense-in-depth chain (L2 compensates L1 rot). Added Barrier-1 ADV-to-ENF handoff inputs: 6 adversarial strategies to encode as rules (S-007/S-003/S-010/S-014/S-002/S-013), quality gate integration (0.92 threshold, creator-critic-revision cycle, C1-C4 escalation), enforcement tier language definitions, L2 re-injection tagging requirement. Added FR-001 through FR-014, NFR-001 through NFR-008. Expanded acceptance criteria from 8 to 13 items. Enriched all task descriptions with ADR/Barrier-1 references. Updated navigation table. |
