# Quality Enforcement -- Single Source of Truth

<!-- VERSION: 1.6.0 | DATE: 2026-02-21 | SOURCE: EPIC-002/EN-002/EN-001 — added H-34 (agent-dev), H-36 (agent-routing), consolidated H-20/H-21 -->

> Canonical constants for the quality framework. All hooks, rules, and skills MUST reference this file.

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rule Index](#hard-rule-index) | H-01 through H-36 (post-EN-001/EN-002 consolidation) |
| [Retired Rule IDs](#retired-rule-ids) | Tombstoned IDs from EN-002 consolidation |
| [Quality Gate](#quality-gate) | Threshold, dimensions, weights, consequences |
| [Criticality Levels](#criticality-levels) | C1-C4 decision classification with strategy sets |
| [Tier Vocabulary](#tier-vocabulary) | HARD/MEDIUM/SOFT enforcement language |
| [Two-Tier Enforcement Model](#two-tier-enforcement-model) | Tier A (L2-protected) vs Tier B (compensating controls) |
| [HARD Rule Ceiling Derivation](#hard-rule-ceiling-derivation) | Principled upper boundary (25 rules) |
| [HARD Rule Ceiling Exception Mechanism](#hard-rule-ceiling-exception-mechanism) | Controlled temporary expansion |
| [Auto-Escalation Rules](#auto-escalation-rules) | AE-001 through AE-006e (graduated context fill sub-rules) |
| [Enforcement Architecture](#enforcement-architecture) | L1-L5 layer definitions |
| [Strategy Catalog](#strategy-catalog) | S-001 through S-015 (selected and excluded) |
| [Implementation](#implementation) | Operational implementation via /adversary skill, skill routing decision table |
| [References](#references) | Source document traceability |

---

## HARD Rule Index

> These are the authoritative HARD rules. Each rule CANNOT be overridden. See source files for consequences.

<!-- L2-REINJECT: rank=1, content="Constitutional: No recursive subagents (P-003). User decides, never override (P-020). No deception (P-022). These are HARD constraints that CANNOT be overridden." -->

<!-- L2-REINJECT: rank=2, content="Quality gate >= 0.92 weighted composite for C2+ deliverables (H-13). Creator-critic-revision cycle REQUIRED, minimum 3 iterations (H-14). Below threshold = REJECTED." -->

<!-- L2-REINJECT: rank=2, content="Ambiguity resolution (H-31): When requirements have multiple valid interpretations, unclear scope, or imply destructive action -- MUST ask clarifying questions before proceeding. Do NOT assume. Do NOT ask when requirements are clear or answers are in the codebase." -->

<!-- L2-REINJECT: rank=3, content="UV only for Python (H-05). NEVER use python/pip directly. Use uv run for execution, uv add for deps." -->

<!-- L2-REINJECT: rank=4, content="LLM-as-Judge scoring (S-014): Apply strict rubric. Leniency bias must be actively counteracted." -->

<!-- L2-REINJECT: rank=5, content="Self-review REQUIRED before presenting any deliverable (H-15, S-010)." -->

<!-- L2-REINJECT: rank=8, content="Governance escalation REQUIRED per AE rules (H-19). Touches .context/rules/ = auto-C3. Touches constitution = auto-C4." -->

<!-- L2-REINJECT: rank=9, tokens=40, content="AE-006 graduated escalation: NOMINAL=no-op, WARNING=log+consider-checkpoint, CRITICAL=auto-checkpoint+reduce-verbosity, EMERGENCY=mandatory-checkpoint+warn-user, COMPACTION=human-escalation-C3+." -->

<!-- L2-REINJECT: rank=10, tokens=30, content="AST-based parsing REQUIRED for worktracker entity operations (H-33). Use jerry ast frontmatter and jerry ast validate CLI commands. NEVER use regex for frontmatter extraction." -->

| ID | Rule | Source |
|----|------|--------|
| H-01 | No recursive subagents (max 1 level) | P-003 |
| H-02 | User authority -- never override | P-020 |
| H-03 | No deception about actions/capabilities | P-022 |
| H-04 | Active project REQUIRED | CLAUDE.md |
| H-05 | UV-only Python environment (execution via `uv run`, dependencies via `uv add`) | python-environment |
| H-07 | Architecture layer isolation (domain imports, application imports, composition root) | architecture-standards |
| H-10 | One class per file | architecture-standards |
| H-11 | Public function signatures (type hints + docstrings REQUIRED) | coding-standards |
| H-13 | Quality threshold >= 0.92 for C2+ | quality-enforcement |
| H-14 | Creator-critic-revision cycle (3 min) | quality-enforcement |
| H-15 | Self-review before presenting (S-010) | quality-enforcement |
| H-16 | Steelman before critique (S-003) | quality-enforcement |
| H-17 | Quality scoring REQUIRED for deliverables | quality-enforcement |
| H-18 | Constitutional compliance check (S-007) | quality-enforcement |
| H-19 | Governance escalation per AE rules | quality-enforcement |
| H-20 | Testing standards (BDD test-first Red phase, 90% line coverage REQUIRED) | testing-standards |
| H-22 | Proactive skill invocation | mandatory-skill-usage |
| H-23 | Markdown navigation (navigation table NAV-001, anchor links NAV-006) | markdown-navigation |
| H-25 | Skill naming and structure (SKILL.md case, kebab-case folder, no README.md) | skill-standards |
| H-26 | Skill description, paths, and registration (WHAT+WHEN+triggers, repo-relative paths, CLAUDE.md+AGENTS.md) | skill-standards |
| H-31 | Clarify before acting when ambiguous (ask, don't assume) | quality-enforcement |
| H-32 | GitHub Issue parity for jerry repo work items | project-workflow |
| H-33 | AST-based parsing REQUIRED for worktracker entity ops | ast-enforcement |
| H-34 | Agent definition standards (YAML schema validation, constitutional compliance triplet) | agent-development-standards |
| H-36 | Agent routing standards (circuit breaker max 3 hops, keyword-first routing) | agent-routing-standards |

---

## Retired Rule IDs

> Rule IDs below were retired during EN-002 consolidation (2026-02-21). These IDs MUST NOT be reassigned. Consequence: reassignment breaks historical cross-references in ADRs, worktracker entries, and commit messages that cite the original rule ID; traceability chains become ambiguous. Instead: when consolidating rules, retire the old ID into the Retired Rule IDs table and document the mapping to its replacement.

| Retired ID | Consolidated Into | Original Rule | Date |
|------------|-------------------|---------------|------|
| H-08 | H-07 (sub-item b) | Application layer: no infra/interface imports | 2026-02-21 |
| H-09 | H-07 (sub-item c) | Composition root exclusivity | 2026-02-21 |
| H-27 | H-25 | No README.md inside skill folder | 2026-02-21 |
| H-28 | H-26 | Skill description: WHAT+WHEN+triggers, <1024 chars, no XML | 2026-02-21 |
| H-29 | H-26 | Full repo-relative paths in SKILL.md | 2026-02-21 |
| H-30 | H-26 | Register in CLAUDE.md + AGENTS.md | 2026-02-21 |
| H-06 | H-05 (sub-item b) | UV only for dependencies | 2026-02-21 |
| H-12 | H-11 (sub-item b) | Docstrings REQUIRED on public functions | 2026-02-21 |
| H-24 | H-23 (sub-item b) | Anchor links REQUIRED (NAV-006) | 2026-02-21 |
| H-21 | H-20 (sub-item b) | 90% line coverage REQUIRED | 2026-02-21 |
| H-35 | H-34 (sub-item b) | Constitutional compliance in agent definitions | 2026-02-21 |
| H-37 | H-36 (sub-item b) | Keyword-first routing below 20 skills | 2026-02-21 |

---

## Quality Gate

<!-- L2-REINJECT: rank=6, content="Criticality levels: C1 Routine (reversible 1 session, HARD only). C2 Standard (reversible 1 day, HARD+MEDIUM). C3 Significant (>1 day, all tiers). C4 Critical (irreversible, all tiers + tournament). AE-002: .context/rules/ = auto-C3. AE-001/AE-004: constitution/baselined ADR = auto-C4." -->

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

### Quality Gate Rule Definitions

| ID | Rule | Rationale | Consequence |
|----|------|-----------|-------------|
| H-13 | Quality threshold >= 0.92 for C2+ deliverables. Weighted composite score using S-014 dimensions. Below threshold = REJECTED, revision required. | Prevents substandard deliverables from bypassing review; the 0.92 threshold balances rigor with iteration cost. | Deliverable rejected. |
| H-14 | Creator-critic-revision cycle REQUIRED. Minimum 3 iterations for C2+ deliverables. | Multi-pass review catches blind spots that single-pass self-review cannot detect. | Quality gate bypass. |
| H-15 | Self-review (S-010) REQUIRED before presenting any deliverable to user or critic. | Early self-correction reduces reviewer burden and prevents obvious defects from consuming critic cycles. | Unreviewed output. |
| H-16 | Steelman (S-003) MUST be applied before Devil's Advocate (S-002). Canonical review pairing. | Strengthening ideas before attacking them prevents premature rejection of sound approaches. | Review protocol violation. |
| H-17 | Quality scoring via S-014 LLM-as-Judge REQUIRED for all C2+ deliverables. | Quantitative scoring provides objective progress tracking across revision iterations and enables threshold enforcement. | Unscored deliverable. |
| H-18 | Constitutional compliance check (S-007) REQUIRED for all C2+ deliverables. | Ensures deliverables do not violate governance constraints that could cascade into systemic issues. | Unchecked compliance. |
| H-19 | Governance escalation per AE rules REQUIRED. Auto-escalation conditions enforce minimum criticality. | Prevents high-impact changes from receiving insufficient review by enforcing minimum criticality classification. | Governance bypass. |
| H-31 | Clarify before acting when requirements are ambiguous. MUST ask when: (1) multiple valid interpretations exist, (2) scope is unclear, (3) destructive or irreversible action implied. MUST NOT ask when requirements are clear or answer is discoverable from codebase. | Prevents wrong-direction work — incorrect assumptions are the most expensive failure mode. One clarifying question costs seconds; wrong-direction work costs hours. | Wrong-direction work. |

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

### Two-Tier Enforcement Model

Rules are classified by their enforcement reliability:

**Tier A** — L2 engine-protected (per-prompt re-injection + compensating L3/L5 controls):

| Rules | L2 Source | Count |
|-------|-----------|-------|
| H-01, H-02, H-03 | quality-enforcement.md rank 1 | 3 |
| H-05 | python-environment.md rank 3 | 1 |
| H-07, H-10 | architecture-standards.md rank 4 | 2 |
| H-11 | coding-standards.md rank 7 | 1 |
| H-13, H-14, H-31 | quality-enforcement.md rank 2 | 3 |
| H-15 | quality-enforcement.md rank 5 | 1 |
| H-19 | quality-enforcement.md rank 8 | 1 |
| H-20 | testing-standards.md rank 5 | 1 |
| H-22 | mandatory-skill-usage.md rank 6 | 1 |
| H-23 | markdown-navigation.md rank 7 | 1 |
| H-25, H-26 | skill-standards.md rank 7 | 2 |
| H-33 | quality-enforcement.md rank 10 | 1 |
| H-34 | agent-development-standards.md rank 5 | 1 |
| H-36 | agent-routing-standards.md rank 6 | 1 |
| **Tier A Total** | | **20** |

**Tier B** — Structural L2 (L1 awareness only, compensating controls prevent bypass):

| Rule | Compensating Controls | Count |
|------|----------------------|-------|
| H-04 (active project) | SessionStart hook enforcement (L3), CLI validation | 1 |
| H-16 (steelman before critique) | /adversary skill enforcement, L1 rule awareness | 1 |
| H-17 (quality scoring) | /adversary + /problem-solving skill enforcement | 1 |
| H-18 (constitutional compliance) | S-007 strategy enforcement in /adversary skill | 1 |
| H-32 (GitHub Issue parity) | /worktracker skill enforcement, CI workflow | 1 |
| **Tier B Total** | | **5** |

**Total:** 25 HARD rules (20 Tier A + 5 Tier B)

> **Note:** Tier B rules are candidates for L2 marker addition pending effectiveness measurement (DEC-005). Current compensating controls provide adequate enforcement through deterministic mechanisms (hooks, skills, CI gates).

### HARD Rule Ceiling Derivation

The ceiling of 25 HARD rules is derived from three independent constraint families (EN-002, C4 derivation scored 0.95 PASS, 2 iterations):

1. **Cognitive Load** — LLM instruction-following reliability degrades when rule sets exceed ~20-25 items, consistent with chunking limits observed in structured prompt compliance benchmarks. At 25 rules, the framework operates at the practical upper bound; beyond this, enforcement reliability drops measurably.
2. **Enforcement Coverage** — L2 per-prompt re-injection operates within an 850-token budget. Current 25 rules consume 559/850 tokens (65.8%) via 16 L2-REINJECT markers. Each additional rule requires ~30-50 tokens of reinforcement capacity, leaving room for ~6 additional markers before budget exhaustion.
3. **Governance Burden** — Each HARD rule requires: (a) constitutional justification, (b) at least one enforcement mechanism (L2 marker, L3 AST gate, L5 CI check, or skill enforcement), and (c) ongoing maintenance. At 25 rules, governance overhead is manageable; beyond 28, the review burden for ceiling exceptions approaches the cost of the rules themselves.

**Convergence:** All three families independently converge on 25 as the practical upper bound. The absolute maximum (28) is enforced by an independent constant in the L5 gate script, preventing self-referential ceiling manipulation.

**Current count:** 25 HARD rules (post-EN-001/EN-002 consolidation). Zero headroom. H-34 (agent definition standards) and H-36 (agent routing standards) added via EN-001 with H-20/H-21 consolidation to stay at ceiling.

### HARD Rule Ceiling Exception Mechanism

Temporary ceiling expansion is permitted under controlled conditions:

| Condition | Requirement |
|-----------|-------------|
| Justification | C4-reviewed ADR documenting why the ceiling must be exceeded |
| Scope | Maximum N=3 additional slots (ceiling+3 = 28 absolute max) |
| Concurrency | Maximum 1 active exception at any time (M-09: no stacking) |
| Duration | 3 months maximum; consolidation plan required |
| Enforcement | L5 CI gate must be updated to reflect temporary ceiling |
| Reversion | Consolidation or demotion must restore count to <= 25 within 3 months |
| Tracking | Exception MUST be tracked as a worktracker entity with reversion deadline |

**Process:** File an ADR per AE-003/AE-004. If approved after C4 review, update the L5 CI gate ceiling parameter in quality-enforcement.md (the `_ABSOLUTE_MAX_CEILING` constant in `check_hard_rule_ceiling.py` enforces the absolute maximum independently). Track the temporary expansion in the worktracker with a reversion deadline. The L5 CI gate will automatically enforce the updated ceiling on every commit and in GitHub Actions CI.

**Reversion enforcement (C-03):** The L5 CI gate provides automated enforcement — when the exception expires, the ceiling value is reverted to 25 and any excess rules will cause CI failure. The worktracker reversion deadline provides human-visible tracking.

**EN-001 phasing note (C-02):** H-32 and H-33 were added by PROJ-005 via merge. EN-001 added H-34 (agent definition standards, compound: schema validation + constitutional compliance) and H-36 (agent routing standards, compound: circuit breaker + keyword-first routing) with H-20/H-21 testing consolidation. Current count: 25/25. H-35, H-37, H-21 retired into compound parents.

---

## Auto-Escalation Rules

| ID | Condition | Escalation |
|----|-----------|------------|
| AE-001 | Touches `docs/governance/JERRY_CONSTITUTION.md` | Auto-C4 |
| AE-002 | Touches `.context/rules/` or `.claude/rules/` | Auto-C3 minimum |
| AE-003 | New or modified ADR | Auto-C3 minimum |
| AE-004 | Modifies baselined ADR | Auto-C4 |
| AE-005 | Security-relevant code | Auto-C3 minimum |
| AE-006a | Context fill NOMINAL/LOW tier (< 0.70) | No action required |
| AE-006b | Context fill WARNING tier (>= 0.70) | Log warning + consider checkpoint |
| AE-006c | Context fill CRITICAL tier (>= 0.80) | Auto-checkpoint + reduce verbosity |
| AE-006d | Context fill EMERGENCY tier (>= 0.88) | Mandatory checkpoint + warn user + prepare handoff |
| AE-006e | Compaction event detected | Mandatory human escalation for C3+, auto-checkpoint, session restart recommended |

---

## Enforcement Architecture

| Layer | Timing | Function | Context Rot | Tokens |
|-------|--------|----------|-------------|--------|
| L1 | Session start | Behavioral foundation via rules | Vulnerable | ~12,500 |
| L2 | Every prompt | Re-inject critical rules | Immune | ~850/prompt |
| L3 | Before tool calls | Deterministic gating (AST) | Immune | 0 |
| L4 | After tool calls | Output inspection, self-correction | Mixed | 0-1,350 |
| L5 | Commit/CI | Post-hoc verification | Immune | 0 |

**Context Rot:** Vulnerable = degrades with context fill. Immune = unaffected. Mixed = deterministic gating immune, self-correction vulnerable.

**Total enforcement budget:** ~15,350 tokens (7.7% of 200K context)

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

## Implementation

**Operational Implementation:** The strategy catalog is implemented operationally via the `/adversary` skill. See `skills/adversary/SKILL.md` for:

- Strategy selection by criticality level (adv-selector agent)
- Strategy execution via templates (adv-executor agent)
- Quality scoring with S-014 rubric (adv-scorer agent)

**Strategy Templates:** All 10 selected strategies have execution templates in `.context/templates/adversarial/`:

- Template format standard: `.context/templates/adversarial/TEMPLATE-FORMAT.md`
- Individual strategy templates: `s-{NNN}-{strategy-slug}.md`

**Agent Implementation:** Three specialized agents in `skills/adversary/agents/`:

- `adv-selector.md` — Maps criticality to strategy sets, enforces H-16 ordering
- `adv-executor.md` — Loads and executes strategy templates against deliverables
- `adv-scorer.md` — Implements S-014 LLM-as-Judge with 6-dimension rubric

**Integration Points:**

- `/adversary` skill: Standalone adversarial reviews and tournament scoring
- `ps-critic` agent: Embedded adversarial quality within creator-critic-revision loops (H-14)
- Both use the same SSOT thresholds, dimensions, and strategy catalog

### Skill Routing Decision Table

Use this table to determine which skill or agent handles a given quality request:

| User Request | Skill / Agent | Rationale |
|---|---|---|
| "Review this code for bugs" | ps-reviewer | Routine defect detection |
| "Give me adversarial critique of this architecture" | /adversary (adv-executor) | Standalone adversarial review outside creator-critic loop |
| "Improve this deliverable iteratively" | /problem-solving (ps-critic) | Creator-critic-revision loop per H-14 |
| "Run tournament review for C4" | /adversary (all agents) | Full tournament mode with all 10 strategies |
| "Score this deliverable against quality gate" | /adversary (adv-scorer) | Standalone S-014 LLM-as-Judge scoring |
| "Red team this security design" | /adversary (adv-executor) | S-001 Red Team strategy application |
| "Check if this ADR meets constitutional constraints" | /adversary (adv-executor) | S-007 Constitutional AI Critique |
| "Help me research why this approach failed" | /problem-solving | Research and root-cause analysis |

> **Disambiguation rule:** If the request involves iterative improvement with revision cycles, use `/problem-solving` (ps-critic). If the request involves a one-shot adversarial assessment, strategy execution, or tournament scoring, use `/adversary`. See `mandatory-skill-usage.md` trigger map for keyword-level routing.

---

## References

| Source | Content |
|--------|---------|
| ADR-EPIC002-001 | Strategy selection, composite scores, exclusion rationale |
| ADR-EPIC002-002 | 5-layer enforcement architecture, token budgets |
| EPIC-002 Final Synthesis | Consolidated design, auto-escalation rules, per-criticality sets |
