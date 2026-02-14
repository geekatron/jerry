# Quality Enforcement — Single Source of Truth

> Canonical constants for the quality framework. All hooks, rules, and skills MUST reference this file.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Criticality Levels](#criticality-levels) | C1-C4 decision classification |
| [Quality Gate](#quality-gate) | Threshold, dimensions, weights |
| [Tier Vocabulary](#tier-vocabulary) | HARD/MEDIUM/SOFT enforcement language |
| [Strategy Catalog](#strategy-catalog) | S-001 through S-014 adversarial strategies |
| [Auto-Escalation Rules](#auto-escalation-rules) | AE-001 through AE-006 |
| [Enforcement Architecture](#enforcement-architecture) | L1-L5 layer definitions |
| [HARD Rule Index](#hard-rule-index) | H-01 through H-24 |

---

## Criticality Levels

| Level | Name | Scope | Enforcement | Review |
|-------|------|-------|-------------|--------|
| C1 | Routine | Reversible in 1 session, <3 files, no external deps | HARD only | Self-check |
| C2 | Standard | Reversible in 1 day, 3-10 files, no API changes | HARD + MEDIUM | Standard critic |
| C3 | Significant | >1 day to reverse, >10 files, API/interface changes | All tiers | Deep review |
| C4 | Critical | Irreversible, architecture/governance/public release | All tiers + tournament | Full tournament |

---

## Quality Gate

**Threshold:** >= 0.92 weighted composite score (C2+ deliverables)

**Scoring mechanism:** S-014 (LLM-as-Judge) with dimension-level rubrics

| Dimension | Weight |
|-----------|--------|
| Completeness | 0.20 |
| Internal Consistency | 0.20 |
| Methodological Rigor | 0.20 |
| Evidence Quality | 0.15 |
| Actionability | 0.15 |
| Traceability | 0.10 |

**Minimum cycle count:** 3 iterations (creator -> critic -> revision)

---

## Tier Vocabulary

| Tier | Keywords | Override | Max Count |
|------|----------|----------|-----------|
| **HARD** | MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL | Cannot override | <= 25 |
| **MEDIUM** | SHOULD, RECOMMENDED, PREFERRED, EXPECTED | Documented justification | Unlimited |
| **SOFT** | MAY, CONSIDER, OPTIONAL, SUGGESTED | No justification needed | Unlimited |

---

## Strategy Catalog

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

---

## Auto-Escalation Rules

| ID | Condition | Escalation |
|----|-----------|------------|
| AE-001 | Touches `docs/governance/JERRY_CONSTITUTION.md` | Auto-C4 |
| AE-002 | Touches `.context/rules/` or `.claude/rules/` | Auto-C3 minimum |
| AE-003 | New or modified ADR | Auto-C3 minimum |
| AE-004 | Modifies baselined ADR | Auto-C4 |
| AE-005 | Security-relevant code | Auto-C3 minimum |
| AE-006 | Token exhaustion at C3+ | Mandatory human escalation |

---

## Enforcement Architecture

| Layer | Timing | Function | Context Rot | Tokens |
|-------|--------|----------|-------------|--------|
| L1 | Session start | Behavioral foundation via rules | Vulnerable | ~12,500 |
| L2 | Every prompt | Re-inject critical rules | Immune | ~600/prompt |
| L3 | Before tool calls | Deterministic gating (AST) | Immune | 0 |
| L4 | After tool calls | Output inspection, self-correction | Mixed | 0-1,350 |
| L5 | Commit/CI | Post-hoc verification | Immune | 0 |

**Total enforcement budget:** ~15,100 tokens (7.6% of 200K context)

---

## HARD Rule Index

| ID | Rule | Source |
|----|------|--------|
| H-01 | No recursive subagents (max 1 level) | P-003 |
| H-02 | User authority — never override | P-020 |
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
