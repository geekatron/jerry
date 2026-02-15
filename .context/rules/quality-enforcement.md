# Quality Enforcement -- Single Source of Truth

<!-- VERSION: 1.2.0 | DATE: 2026-02-14 | SOURCE: EPIC-002 Final Synthesis, ADR-EPIC002-001, ADR-EPIC002-002 -->

> Canonical constants for the quality framework. All hooks, rules, and skills MUST reference this file.

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rule Index](#hard-rule-index) | H-01 through H-24 |
| [Quality Gate](#quality-gate) | Threshold, dimensions, weights, consequences |
| [Criticality Levels](#criticality-levels) | C1-C4 decision classification with strategy sets |
| [Tier Vocabulary](#tier-vocabulary) | HARD/MEDIUM/SOFT enforcement language |
| [Auto-Escalation Rules](#auto-escalation-rules) | AE-001 through AE-006 |
| [Enforcement Architecture](#enforcement-architecture) | L1-L5 layer definitions |
| [Strategy Catalog](#strategy-catalog) | S-001 through S-015 (selected and excluded) |
| [References](#references) | Source document traceability |

---

## HARD Rule Index

> These are the authoritative HARD rules. Each rule CANNOT be overridden. See source files for consequences.

<!-- L2-REINJECT: rank=1, tokens=50, content="Constitutional: No recursive subagents (P-003). User decides, never override (P-020). No deception (P-022). These are HARD constraints that CANNOT be overridden." -->

<!-- L2-REINJECT: rank=2, tokens=90, content="Quality gate >= 0.92 weighted composite for C2+ deliverables (H-13). Creator-critic-revision cycle REQUIRED, minimum 3 iterations (H-14). Below threshold = REJECTED." -->

<!-- L2-REINJECT: rank=3, tokens=25, content="UV only for Python (H-05/H-06). NEVER use python/pip directly." -->

<!-- L2-REINJECT: rank=4, tokens=30, content="LLM-as-Judge scoring (S-014): Apply strict rubric. Leniency bias must be actively counteracted." -->

<!-- L2-REINJECT: rank=5, tokens=30, content="Self-review REQUIRED before presenting any deliverable (H-15, S-010)." -->

<!-- L2-REINJECT: rank=8, tokens=40, content="Governance escalation REQUIRED per AE rules (H-19). Touches .context/rules/ = auto-C3. Touches constitution = auto-C4." -->

| ID | Rule | Source |
|----|------|--------|
| H-01 | No recursive subagents (max 1 level) | P-003 |
| H-02 | User authority -- never override | P-020 |
| H-03 | No deception about actions/capabilities | P-022 |
| H-04 | Active project REQUIRED | CLAUDE.md |
| H-05 | UV only for Python execution | python-environment |
| H-06 | UV only for dependencies | python-environment |
| H-07 | Domain layer: no external imports | architecture-standards |
| H-08 | Application layer: no infra/interface imports | architecture-standards |
| H-09 | Composition root exclusivity | architecture-standards |
| H-10 | One class per file | file-organization |
| H-11 | Type hints REQUIRED on public functions | coding-standards |
| H-12 | Docstrings REQUIRED on public functions | coding-standards |
| H-13 | Quality threshold >= 0.92 for C2+ | quality-enforcement |
| H-14 | Creator-critic-revision cycle (3 min) | quality-enforcement |
| H-15 | Self-review before presenting (S-010) | quality-enforcement |
| H-16 | Steelman before critique (S-003) | quality-enforcement |
| H-17 | Quality scoring REQUIRED for deliverables | quality-enforcement |
| H-18 | Constitutional compliance check (S-007) | quality-enforcement |
| H-19 | Governance escalation per AE rules | quality-enforcement |
| H-20 | Test before implement (BDD Red phase) | testing-standards |
| H-21 | 90% line coverage REQUIRED | testing-standards |
| H-22 | Proactive skill invocation | mandatory-skill-usage |
| H-23 | Navigation table REQUIRED (NAV-001) | markdown-navigation |
| H-24 | Anchor links REQUIRED (NAV-006) | markdown-navigation |

---

## Quality Gate

<!-- L2-REINJECT: rank=6, tokens=100, content="Criticality levels: C1 Routine (reversible 1 session, HARD only). C2 Standard (reversible 1 day, HARD+MEDIUM). C3 Significant (>1 day, all tiers). C4 Critical (irreversible, all tiers + tournament). AE-002: .context/rules/ = auto-C3. AE-001/AE-004: constitution/baselined ADR = auto-C4." -->

**Threshold:** >= 0.92 weighted composite score (C2+ deliverables)

**Below threshold:** Deliverable REJECTED; revision required per H-13.

**Scoring mechanism:** S-014 (LLM-as-Judge) with dimension-level rubrics (ADR-EPIC002-001)

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

**Minimum cycle count:** 3 iterations (creator -> critic -> revision)

### Operational Score Bands

Below-threshold deliverables are subdivided into operational bands for workflow guidance:

| Band | Score Range | Outcome | Workflow Action |
|------|------------|---------|-----------------|
| PASS | >= 0.92 | Accepted | Deliverable meets quality gate |
| REVISE | 0.85 - 0.91 | Rejected (H-13) | Near threshold — targeted revision likely sufficient |
| REJECTED | < 0.85 | Rejected (H-13) | Significant rework required |

> **Note:** Both REVISE and REJECTED trigger the revision cycle per H-13. The REVISE band is an operational workflow label to distinguish near-threshold deliverables from those requiring significant rework. It is NOT a distinct acceptance state.

---

## Criticality Levels

| Level | Name | Scope | Enforcement | Required Strategies | Optional |
|-------|------|-------|-------------|---------------------|----------|
| C1 | Routine | Reversible in 1 session, <3 files | HARD only | S-010 | S-003, S-014 |
| C2 | Standard | Reversible in 1 day, 3-10 files | HARD + MEDIUM | S-007, S-002, S-014 | S-003, S-010 |
| C3 | Significant | >1 day to reverse, >10 files, API changes | All tiers | C2 + S-004, S-012, S-013 | S-001, S-003, S-010, S-011 |
| C4 | Critical | Irreversible, architecture/governance/public | All tiers + tournament | All 10 selected | None |

---

## Tier Vocabulary

| Tier | Keywords | Override | Max Count |
|------|----------|----------|-----------|
| **HARD** | MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL | Cannot override | <= 25 |
| **MEDIUM** | SHOULD, RECOMMENDED, PREFERRED, EXPECTED | Documented justification | Unlimited |
| **SOFT** | MAY, CONSIDER, OPTIONAL, SUGGESTED | No justification needed | Unlimited |

---

## Auto-Escalation Rules

| ID | Condition | Escalation |
|----|-----------|------------|
| AE-001 | Touches `docs/governance/JERRY_CONSTITUTION.md` | Auto-C4 |
| AE-002 | Touches `.context/rules/` or `.claude/rules/` | Auto-C3 minimum |
| AE-003 | New or modified ADR | Auto-C3 minimum |
| AE-004 | Modifies baselined ADR | Auto-C4 |
| AE-005 | Security-relevant code | Auto-C3 minimum |
| AE-006 | Token exhaustion at C3+ (context compaction triggered) | Mandatory human escalation |

---

## Enforcement Architecture

| Layer | Timing | Function | Context Rot | Tokens |
|-------|--------|----------|-------------|--------|
| L1 | Session start | Behavioral foundation via rules | Vulnerable | ~12,500 |
| L2 | Every prompt | Re-inject critical rules | Immune | ~600/prompt |
| L3 | Before tool calls | Deterministic gating (AST) | Immune | 0 |
| L4 | After tool calls | Output inspection, self-correction | Mixed | 0-1,350 |
| L5 | Commit/CI | Post-hoc verification | Immune | 0 |

**Context Rot:** Vulnerable = degrades with context fill. Immune = unaffected. Mixed = deterministic gating immune, self-correction vulnerable.

**Total enforcement budget:** ~15,100 tokens (7.6% of 200K context)

---

## Strategy Catalog

**Selected** (10 active strategies, ranked by composite score from ADR-EPIC002-001):

| ID | Strategy | Score | Family |
|----|----------|-------|--------|
| S-014 | LLM-as-Judge | 4.40 | Iterative Self-Correction |
| S-003 | Steelman Technique | 4.30 | Dialectical Synthesis |
| S-013 | Inversion Technique | 4.25 | Structured Decomposition |
| S-007 | Constitutional AI Critique | 4.15 | Iterative Self-Correction |
| S-002 | Devil's Advocate | 4.10 | Role-Based Adversarialism |
| S-004 | Pre-Mortem Analysis | 4.10 | Role-Based Adversarialism |
| S-010 | Self-Refine | 4.00 | Iterative Self-Correction |
| S-012 | FMEA | 3.75 | Structured Decomposition |
| S-011 | Chain-of-Verification | 3.75 | Structured Decomposition |
| S-001 | Red Team Analysis | 3.35 | Role-Based Adversarialism |

**Excluded** (reconsideration conditions in ADR-EPIC002-001):

| ID | Strategy | Exclusion Reason |
|----|----------|------------------|
| S-005 | Dialectical Inquiry | RED risk -- requires cross-model LLM |
| S-006 | Analysis of Competing Hypotheses | Redundant with S-013 + S-004 |
| S-008 | Socratic Method | Requires interactive multi-turn dialogue |
| S-009 | Multi-Agent Debate | RED risk -- requires cross-model LLM |
| S-015 | Prompt Adversarial Examples | RED risk -- adversarial prompt injection concern |

---

## References

| Source | Content |
|--------|---------|
| ADR-EPIC002-001 | Strategy selection, composite scores, exclusion rationale |
| ADR-EPIC002-002 | 5-layer enforcement architecture, token budgets |
| EPIC-002 Final Synthesis | Consolidated design, auto-escalation rules, per-criticality sets |
