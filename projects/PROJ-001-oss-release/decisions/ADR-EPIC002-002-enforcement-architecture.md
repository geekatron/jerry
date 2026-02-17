# ADR-EPIC002-002: Enforcement Vector Prioritization for Jerry Quality Framework

<!--
DOCUMENT-ID: FEAT-005:EN-402-TASK-005-ENFORCEMENT-ADR
TEMPLATE: Architecture Decision Record (ADR)
VERSION: 1.1.0
SOURCE: TASK-001 (Evaluation Criteria), TASK-002 (Risk Assessment), TASK-003 (Trade Study), TASK-004 (Priority Matrix)
AGENT: ps-architect (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-402 (Enforcement Priority Analysis & Decision)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
CONSUMERS: TASK-006 (execution plans), TASK-007 (ps-critic adversarial review), EN-403/404/405 (implementation)
RELATED-ADR: ADR-EPIC002-001 (adversarial strategy selection -- ACCEPTED)
RATIFIED-BY: User (P-020) on 2026-02-13
-->

> **Version:** 1.2.0
> **Agent:** ps-architect (Claude Opus 4.6)
> **Status:** ACCEPTED (ratified by user on 2026-02-13 per P-020)
> **Created:** 2026-02-13
> **Supersedes:** N/A
> **Superseded By:** N/A

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Problem statement, constraints, and decision drivers |
| [Decision](#decision) | Tiered vector prioritization, top 3 execution targets, excluded vectors |
| [Options Considered](#options-considered) | Four architecture alternatives with pros/cons |
| [Detailed Decision Rationale](#detailed-decision-rationale) | Evidence-based justification for each decision element |
| [Consequences](#consequences) | Positive, negative, and monitoring outcomes |
| [Evidence Base](#evidence-base) | Summary of TASK-001 through TASK-004 findings |
| [Sensitivity and Robustness](#sensitivity-and-robustness) | Weight sensitivity analysis results |
| [Token Budget Feasibility](#token-budget-feasibility) | Budget allocation and verification |
| [Compliance](#compliance) | Constitutional principle alignment |
| [Risks](#risks) | Systemic and per-vector risks with mitigations |
| [Implementation Roadmap](#implementation-roadmap) | Phased deployment sequence |
| [Related Decisions](#related-decisions) | Links to upstream/downstream ADRs and enablers |
| [References](#references) | All citations with traceability |

---

## Context

### Problem Statement

Jerry's enforcement of quality framework standards currently relies almost exclusively on `.claude/rules/` text files loaded at session start (Family 2: Rules-Based Enforcement). This approach suffers from three critical weaknesses identified through the EN-401 research program:

1. **Context rot vulnerability.** Rules loaded at session start degrade as the LLM context window fills. At 50K+ tokens, effectiveness drops to 40-60% per the "Lost in the Middle" research (Liu et al., 2023). All 6 Family 2 vectors share this failure mode and degrade simultaneously (correlated failure, R-SYS-001 from TASK-002, score 20 RED).

2. **Token budget pressure.** The current rules consume approximately 25,700 tokens (12.9% of the 200K context window). This leaves less context capacity for productive work and paradoxically accelerates context rot by filling the window faster (R-SYS-002, score 16 RED).

3. **Single-layer fragility.** With enforcement concentrated in a single architectural layer (text-based rules), there is no defense-in-depth. If context rot degrades the rules layer, no independent enforcement mechanism remains active.

### Decision Scope

EN-401 produced a comprehensive catalog of 62 enforcement vectors across 7 families. EN-402 evaluated these vectors to determine:

- Which vectors to implement and in what order (prioritization)
- How to compose selected vectors into a coherent architecture (composition)
- What vectors to exclude and why (exclusions)
- How to allocate the constrained token budget (resource allocation)

### Decision Drivers

Five user-confirmed priorities govern this decision (validated during EN-401):

| Priority | Description | Impact on Decision |
|----------|-------------|-------------------|
| #1 | TASK-009 (EN-401 Revised Catalog v1.1) is the authoritative data source | Constrains all scoring inputs |
| #2 | Prioritize the 38 LLM-Portable vectors; support Windows adaptations | Drives portability weighting (18%) |
| #3 | Token budget envelope of approximately 25,700 tokens (target: 12,476 optimized) | Constrains in-context vector selection |
| #4 | Reference adversary model for enforcement robustness | Drives bypass resistance scoring |
| #5 | Prioritize context-rot-resilient vectors | Drives CRR as highest-weighted criterion (25%) |

### Constraints

| ID | Constraint | Source | Impact |
|----|------------|--------|--------|
| C-001 | No recursive subagents; max ONE level of delegation | P-003 (Jerry Constitution) | Limits multi-agent enforcement depth |
| C-002 | Filesystem as persistence layer; persist state to files | P-002 (Jerry Constitution) | Favors file-based enforcement vectors |
| C-003 | Cross-platform portability (macOS, Linux, Windows) | User priority #2; TASK-006 | Windows at 73% compatibility |
| C-004 | Token budget: 15,126 tokens maximum for enforcement (7.6% of 200K) | User priority #3; TASK-009 Appendix B | Hard constraint on in-context vectors |
| C-005 | Context rot degrades correlated vector groups simultaneously | TASK-009 Appendix C; TASK-002 R-SYS-001 | Requires independent immune layers |
| C-006 | User authority over all decisions; never override | P-020 (Jerry Constitution) | Enforcement must not silently suppress user intent |

---

## Decision

### 1. Adopt a 5-Layer Hybrid Enforcement Architecture

We adopt a layered enforcement architecture consisting of 5 execution layers plus a cross-cutting process layer. Layers fire in strict temporal order following the "prevent, then detect, then verify" principle (NASA-STD-8739.8). The architecture follows a "deterministic skeleton with probabilistic guidance" pattern: context-rot-immune vectors (AST, CI, hooks, processes) form the enforcement skeleton; context-dependent vectors (rules, prompts) provide guidance within that skeleton.

| Layer | Timing | Function | Context Rot | Token Cost |
|-------|--------|----------|-------------|------------|
| L1: Static Context | Session start | Set behavioral foundation via optimized rules | VULNERABLE (compensated by L2) | ~12,476 |
| L2: Per-Prompt Reinforcement | Every prompt | Re-inject critical rules to counteract rot | IMMUNE by design | ~600/session |
| L3: Pre-Action Gating | Before tool calls | Deterministically block non-compliant operations | IMMUNE (external) | 0 |
| L4: Post-Action Validation | After tool calls | Inspect outputs; trigger self-correction | MIXED | 0-1,350 |
| L5: Post-Hoc Verification | Commit/CI time | Catch all violations that escaped runtime layers | IMMUNE (external) | 0 |
| Process | Workflow level | Governance, evidence-based completion | IMMUNE (process-based) | 0 |

**Key architectural property:** Four of five enforcement layers are entirely context-rot-immune. The sole vulnerable layer (L1) is immediately compensated by L2 (Per-Prompt Reinforcement). Under full context rot, 4 of 5 layers remain fully effective.

### 2. Tier 1 Vectors: 16 Vectors for Immediate Implementation

Sixteen vectors score WCS >= 4.00 and are recommended for immediate implementation:

| Rank | Vector | Name | WCS | Family | Layer |
|------|--------|------|-----|--------|-------|
| 1 | V-038 | AST Import Boundary Validation | 4.92 | F5 | L3/L5 |
| 2 | V-045 | CI Pipeline Enforcement | 4.86 | F5 | L5 |
| 3 | V-044 | Pre-commit Hook Validation | 4.80 | F5 | L5 |
| 4 | V-043 | Architecture Test Suite | 4.80 | F5 | L5 |
| 5 | V-039 | AST Type Hint Enforcement | 4.72 | F5 | L3/L5 |
| 6 | V-041 | AST One-Class-Per-File Check | 4.72 | F5 | L3/L5 |
| 7 | V-040 | AST Docstring Enforcement | 4.72 | F5 | L3/L5 |
| 8 | V-042 | Property-Based Testing | 4.50 | F5 | L5 |
| 9 | V-057 | Quality Gate Enforcement | 4.38 | F7 | Process |
| 10 | V-060 | Evidence-Based Closure | 4.38 | F7 | Process |
| 11 | V-061 | Acceptance Criteria Verification | 4.22 | F7 | Process |
| 12 | V-024 | Context Reinforcement via Repetition | 4.11 | F3 | L2 |
| 13 | V-055 | Formal Waiver Process | 4.02 | F7 | Process |
| 14 | V-053 | NASA File Classification | 4.02 | F7 | Process |
| 15 | V-056 | BDD Red/Green/Refactor Cycle | 4.02 | F7 | Process |
| 16 | V-062 | WTI Rules | 4.02 | F7 | Process |

**Composition:** Family 5 (Structural) contributes 8 vectors; Family 7 (Process) contributes 7; Family 3 (Prompt) contributes 1 (V-024, the context rot countermeasure). All 16 Tier 1 vectors are context-rot-immune. All are zero-token except V-024 (600 tokens/session).

### 3. Tier 2 Vectors: 16 Vectors for Near-Term Implementation

Sixteen vectors score WCS 3.50-3.99 and are recommended for implementation in subsequent phases:

| Rank | Vector | Name | WCS | Family | Layer |
|------|--------|------|-----|--------|-------|
| 17 | V-001 | PreToolUse Blocking | 3.99 | F1 | L3 |
| 18 | V-021 | CRITIC Pattern | 3.91 | F3 | L4 |
| 19 | V-051 | NASA IV&V Independence | 3.90 | F7 | Process |
| 20 | V-052 | VCRM | 3.82 | F7 | Process |
| 21 | V-054 | FMEA | 3.82 | F7 | Process |
| 22 | V-015 | System Message Hierarchy | 3.74 | F3 | L1 |
| 23 | V-017 | XML Tag Demarcation | 3.74 | F3 | L1 |
| 24 | V-049 | MCP Audit Logging | 3.74 | F6 | L4 |
| 25 | V-002 | PostToolUse Validation | 3.72 | F1 | L4 |
| 26 | V-005 | UserPromptSubmit Hook | 3.72 | F1 | L2 |
| 27 | V-058 | Adversarial Review | 3.72 | F7 | Process |
| 28 | V-059 | Multi-Agent Cross-Pollination | 3.72 | F7 | Process |
| 29 | V-003 | SessionStart Injection | 3.54 | F1 | L1 |
| 30 | V-004 | Stop Hook (Subagent) | 3.54 | F1 | L1 |
| 31 | V-016 | Structured Imperative Rules | 3.52 | F3 | L1 |
| 32 | V-026 | Few-Shot Exemplars | 3.52 | F3 | L1 |

**Composition:** Tier 2 spans Families 1 (5 vectors), 3 (5 vectors), 6 (1 vector), and 7 (5 vectors). This provides breadth across all architectural layers that Tier 1 does not cover independently (particularly L2 delivery mechanism V-005, L3 blocking V-001, and L4 detection V-002).

**Note on V-005:** Although V-005 (UserPromptSubmit Hook) scores Tier 2 due to its PORT=1 (Claude Code-specific), it is the mandatory delivery mechanism for V-024 (Tier 1, the context rot countermeasure). V-005 should be implemented concurrently with V-024 as a paired deployment. On non-Claude-Code platforms, V-024 content is portable; only the injection mechanism requires platform-specific adaptation.

### 4. Top 3 Priority Vectors for Detailed Execution Plans

Three vectors are designated for detailed execution planning in TASK-006, based on highest WCS scores and implementation readiness:

#### Priority 1: V-038 -- AST Import Boundary Validation (WCS 4.92)

| Attribute | Value |
|-----------|-------|
| **WCS** | 4.92 (highest in catalog) |
| **Scores** | CRR=5, EFF=5, PORT=5, TOK=5, BYP=5, COST=4, MAINT=5 |
| **TRL** | 6 -- `tests/architecture/test_composition_root.py` already implements AST import validation |
| **Effort** | ~1 day (move existing logic from test infrastructure to PreToolUse hook and pre-commit) |
| **Architecture** | L3 (Pre-Action Gating via V-001) + L5 (Pre-commit via V-044 + CI via V-045) |
| **Key Risk** | FM-038-02: dynamic imports via `importlib`/`__import__` bypass static AST (RPN=98). Mitigation: supplementary grep-based detection |
| **Why #1** | Best-in-class across all 7 dimensions. Immune, deterministic, portable, zero-token, self-maintaining. Existing infrastructure reduces cost. |

#### Priority 2: V-045 -- CI Pipeline Enforcement (WCS 4.86)

| Attribute | Value |
|-----------|-------|
| **WCS** | 4.86 |
| **Scores** | CRR=5, EFF=5, PORT=5, TOK=5, BYP=5, COST=3, MAINT=5 |
| **TRL** | 4 -- GitHub Actions is mature; Jerry needs `.github/workflows/ci.yml` configuration |
| **Effort** | ~1-3 days (create CI workflow with ruff, mypy, pytest, architecture tests) |
| **Architecture** | L5 (Post-Hoc Verification). Ultimate backstop. Runs V-038-V-043 in deterministic pipeline. |
| **Key Risk** | FM-045-01: CI configured as optional (RPN=36). Mitigation: required status checks in branch protection. |
| **Why #2** | Near-impossible to bypass (requires admin access). Catches everything that slipped through all runtime layers. |

#### Priority 3: V-044 -- Pre-commit Hook Validation (WCS 4.80)

| Attribute | Value |
|-----------|-------|
| **WCS** | 4.80 |
| **Scores** | CRR=5, EFF=5, PORT=5, TOK=5, BYP=4, COST=4, MAINT=4 |
| **TRL** | 5 -- pre-commit framework is mature; Jerry needs `.pre-commit-config.yaml` |
| **Effort** | ~1 day (configure pre-commit with ruff, mypy, AST boundary checks) |
| **Architecture** | L5 (Post-Hoc Verification). Immediate feedback before CI. |
| **Key Risk** | FM-044-01: `--no-verify` bypass (RPN=63). Mitigation: CI (V-045) as mandatory backup catches violations. |
| **Why #3** | Universal (git hooks work on any platform). Provides immediate developer feedback at commit time, faster than CI. |

### 5. Excluded Vectors: 3 Vectors with Rationale

Three vectors are excluded from scoring per TASK-002 risk-based recommendations:

| Vector | Name | Exclusion Rationale |
|--------|------|---------------------|
| V-035 | Content Classification (Llama Guard) | RED integration risk (R-035-IGR, score 16). Requires separate ML model deployment. Jerry enforces process compliance, not content safety. Architecturally misaligned -- Jerry's enforcement domain is code quality and workflow compliance, not content moderation. |
| V-029 | Programmable Rails (NeMo Guardrails) | HIGH integration risk (R-029-IGR, score 12) combined with HIGH portability risk (R-029-PPR, score 15). NeMo's Colang DSL creates framework lock-in. The transferable concept (programmable dialogue control) is captured by V-030 (State Machine Enforcement) without the NeMo dependency. |
| V-037 | Grammar-Constrained Generation (Outlines/LMQL) | HIGH portability risk (R-037-PPR, score 15). Requires specific model backends for token-level control. Jerry does not control token-level generation -- this vector is architecturally misaligned with Jerry's role as an orchestration and quality framework. |

---

## Options Considered

### Option A: Hybrid Layered Approach (CHOSEN)

**Description:** Deploy a 5-layer enforcement stack combining rules (L1), per-prompt reinforcement (L2), hooks (L3), post-action validation (L4), and post-hoc verification (L5), with a cross-cutting process layer. Static rules provide portable guidance; deterministic external processes provide immune enforcement. Claude Code hooks add optional platform-specific blocking power.

| Criterion | Assessment |
|-----------|------------|
| Context Rot Resilience | **STRONG.** 4 of 5 layers are fully immune. L1 (VULNERABLE) is compensated by L2 (IMMUNE by design). Under context rot, effective independent layers drop from 5 to 4 -- acceptable. |
| Effectiveness | **STRONG.** Deterministic blocking at L3 (hooks, AST). Comprehensive detection at L5 (pre-commit, CI). No single-point-of-failure. |
| Portability | **STRONG.** Core stack (L1, L5, Process) is 100% portable. L2 content is portable; mechanism is platform-specific. L3 hooks are Claude Code-specific but optional. |
| Token Efficiency | **STRONG.** 15,126 tokens total (7.6% of 200K). 82.5% of budget in L1 rules (optimizable). L3-L5 are zero-token. |
| Bypass Resistance | **STRONG.** IMMUNE layers survive all 4 adversary scenarios. L5 (CI) is near-impossible to bypass. |
| Implementation Cost | **MODERATE.** Leverages existing infrastructure (AST tests, hook scripts). New components: UserPromptSubmit hook, CI pipeline, pre-commit configuration. |
| Maintainability | **MODERATE.** External-process vectors (L3-L5) are self-maintaining. Rules (L1) need quarterly review. Reinforcement content (L2) must track rule changes. |

**Pros:**
- Satisfies ALL user priorities simultaneously
- Defense-in-depth with 4 independent immune layers
- Graceful degradation: removing hooks reduces enforcement from "blocking" to "advisory" but does not eliminate it
- Token budget fits within target (7.6%)

**Cons:**
- Implementation spans multiple infrastructure types (hooks, CI, process)
- More components to coordinate than simpler approaches
- V-005 (UserPromptSubmit) is at TRL 3, the lowest readiness of any recommended vector

### Option B: Rules-Only Approach

**Description:** Rely exclusively on `.claude/rules/` text files and CLAUDE.md for enforcement. Optimize rule content for maximum effectiveness. No hooks, no CI pipeline, no external process enforcement.

| Criterion | Assessment |
|-----------|------------|
| Context Rot Resilience | **WEAK.** ALL enforcement is VULNERABLE to context rot. At 50K+ tokens, enforcement degrades to 40-60% effectiveness. No immune layers exist. |
| Effectiveness | **WEAK.** Advisory only. LLM compliance is probabilistic, not deterministic. No blocking mechanism. |
| Portability | **STRONG.** 100% portable. Text-based rules work on any LLM, any OS. |
| Token Efficiency | **WEAK.** 25,700 tokens current (12.9%); 12,476 optimized (6.2%). Entire budget consumed by rules with degrading returns. |
| Bypass Resistance | **WEAK.** Bypassed by prompt injection, context manipulation, and emergent LLM behavior. |
| Implementation Cost | **STRONG.** Already exists. Zero additional development needed. |
| Maintainability | **STRONG.** Low maintenance. Text files updated annually. |

**Pros:**
- Zero implementation cost (already deployed)
- Maximum portability
- Simplest mental model

**Cons:**
- Correlated failure: ALL enforcement degrades simultaneously under context rot (R-SYS-001)
- No deterministic enforcement for any violation type
- Single-layer fragility provides zero defense-in-depth
- Highest token cost per unit of enforcement value

**Pugh Score vs. Baseline (Hybrid): -0.30** (INFERIOR)

### Option C: Hooks-Heavy Approach

**Description:** Maximize use of Claude Code hooks (PreToolUse, PostToolUse, UserPromptSubmit, SessionStart) as the primary enforcement mechanism. Minimal rules. All enforcement decisions made by external hook scripts.

| Criterion | Assessment |
|-----------|------------|
| Context Rot Resilience | **STRONG.** Hooks are external processes, fully immune to context rot. |
| Effectiveness | **STRONG.** Deterministic blocking on every tool call. Highest enforcement power available. |
| Portability | **WEAK.** Zero portability. All hooks are Claude Code-specific. Platform migration renders entire enforcement stack inoperative (R-SYS-003). |
| Token Efficiency | **STRONG.** Zero context tokens. All enforcement is external. |
| Bypass Resistance | **STRONG.** External processes survive prompt injection and context manipulation. |
| Implementation Cost | **MODERATE-HIGH.** Requires developing comprehensive hook validation logic for all enforcement rules. |
| Maintainability | **MODERATE-HIGH.** Hook scripts require quarterly review for API compatibility. Complex hook chains are fragile. |

**Pros:**
- Maximum enforcement power on Claude Code
- Zero token cost
- Full context rot immunity

**Cons:**
- Zero portability (violates user priority #2)
- Complete vendor lock-in to Claude Code
- Platform migration risk (R-SYS-003, score 16 RED)
- Complex hook chains create maintenance burden

**Pugh Score vs. Baseline (Hybrid): +0.16** (MARGINAL improvement on enforcement, but fails portability)

### Option D: CI-Only Approach

**Description:** Rely exclusively on CI pipeline and pre-commit hooks for enforcement. No runtime enforcement during LLM sessions. All violations detected post-hoc at commit/push time.

| Criterion | Assessment |
|-----------|------------|
| Context Rot Resilience | **STRONG.** CI and pre-commit are external processes, fully immune. |
| Effectiveness | **MODERATE.** Deterministic but post-hoc. Violations are written before detection. Remediation cost is higher. |
| Portability | **STRONG.** Git hooks and CI providers work universally. |
| Token Efficiency | **STRONG.** Zero context tokens. |
| Bypass Resistance | **MODERATE.** `--no-verify` bypasses pre-commit; CI requires admin override to bypass. |
| Implementation Cost | **MODERATE.** CI configuration and pre-commit setup. |
| Maintainability | **STRONG.** CI infrastructure is stable. |

**Pros:**
- High portability
- Zero token cost
- Deterministic enforcement
- Well-understood infrastructure

**Cons:**
- NO real-time enforcement during sessions. Violations exist in code until commit time.
- No guidance or prevention. LLM receives no enforcement rules.
- Architecturally incomplete: "detect after the fact" without "prevent before it happens"
- Higher violation remediation cost (code already written, must be rewritten)

**Pugh Score vs. Baseline (Hybrid): +0.32** (comparable on quantitative metrics but architecturally incomplete)

### Decision Rationale for Option A

Option A (Hybrid Layered) is selected because it is the only option that satisfies ALL decision drivers simultaneously:

1. **Portability (priority #2):** Core enforcement (L1, L5, Process) is 100% portable. Options B and D match, but Option C fails.
2. **Token budget (priority #3):** 15,126 tokens (7.6%). Options C and D use zero tokens, but Option A is within budget while also providing runtime guidance.
3. **Bypass resistance (priority #4):** 4 independent immune layers. Options B and D lack runtime enforcement.
4. **Context rot resilience (priority #5):** 4 of 5 layers immune. Option B has zero immune layers. Options C and D are immune but sacrifice guidance (C) or prevention (D).
5. **Defense-in-depth:** Only Option A provides enforcement at every stage of the violation lifecycle (prevent-detect-verify-govern).

---

## Detailed Decision Rationale

### Why Context Rot Resilience Receives Highest Weight (25%)

TASK-009 Appendix C demonstrates that context rot is not merely an individual vector concern but a **correlated systemic failure mode**. All 13 VULNERABLE vectors (Families 2-3, partial) degrade simultaneously because they share a common root cause: dependence on instructions persisting in the LLM's attention span. The correlated failure analysis (TASK-009 Section L2) shows that when context rot triggers, Jerry loses 3 of its 6 conceptual enforcement layers in a single failure event.

CRR also has the widest discrimination spread of any dimension: 48.4% of vectors are IMMUNE while 11.3% are HIGHLY VULNERABLE. This makes it the most powerful differentiator for separating high-value from low-value vectors (TASK-001 Design Principle DP-2).

### Why Family 5 (Structural) Dominates Tier 1

All 8 Family 5 vectors score Tier 1. This is not a scoring artifact -- it reflects genuine structural advantages:

- **Context rot immunity:** All external Python processes (AST, pytest). CRR=5 for all 8.
- **Zero token cost:** Execute outside the context window. TOK=5 for all 8.
- **Universal portability:** Python stdlib + git + CI. PORT=5 for all 8.
- **Deterministic enforcement:** AST analysis and test assertions produce binary pass/fail. EFF=4-5 for all 8.
- **All-GREEN risk profile:** TASK-002 found no RED risks and only 1 YELLOW across the entire family.

### Why V-024 (Context Reinforcement) Is in Tier 1 Despite Being Prompt-Based

V-024 is the sole prompt-based vector in Tier 1. It earns this position because:

1. **It is IMMUNE to context rot by design.** Unlike other prompt vectors (which load once and degrade), V-024 re-injects critical rules on every prompt via the UserPromptSubmit hook. Fresh injection counteracts the "Lost in the Middle" degradation.
2. **It is the primary mitigation for R-SYS-001** (correlated context rot failure, score 20 RED). Without V-024, the entire L1 rules layer degrades with no compensation.
3. **TASK-009 identifies V-024 as "the single highest-priority implementation recommendation."**
4. **Synergistic with multiple vectors:** V-024 + V-010 (sustains hard rules); V-024 + V-014 (sustains self-critique); V-024 + V-005 (delivery mechanism).

### Why Family 2 (Rules) Scores Lowest

The 6 Family 2 vectors average WCS 2.61 (lowest of all families). This reflects:

- CRR=1 for 5 of 6 vectors (HIGH context rot vulnerability)
- EFF=1-2 at 50K+ tokens (advisory only, no enforcement mechanism)
- BYP=1 for 5 of 6 vectors (easily bypassed by injection and context manipulation)

This does NOT mean rules should be removed. V-009/V-010 (rules infrastructure) are essential as L1 foundation -- they provide the initial behavioral guidance that all other layers enforce. The low scores reflect that rules alone are insufficient and must be supplemented by immune enforcement layers.

---

## Consequences

### Positive

| # | Consequence | Mechanism |
|---|------------|-----------|
| P-1 | Jerry's enforcement survives context rot. | 4 of 5 layers are immune; V-024 compensates the sole vulnerable layer. Under context rot, effective enforcement drops from 5 layers to 4, not from 1 layer to 0. |
| P-2 | Jerry's enforcement is portable across LLM platforms. | Core stack (L1 rules + L5 CI/pre-commit + Process) works on any platform. Hooks are optional enhancers. |
| P-3 | Token budget is sustainable. | 15,126 tokens (7.6% of 200K) vs. current 25,700 (12.9%). Phase 1 rule optimization saves 13,224 tokens (51.5% reduction). |
| P-4 | Critical invariants are enforced deterministically. | Architecture boundary violations are caught by AST (L3) and CI (L5). No reliance on probabilistic LLM compliance for the most important rules. |
| P-5 | Defense-in-depth provides redundancy. | Each layer compensates for the failure mode of the adjacent layer (TASK-003 defense-in-depth pattern). No single-point-of-failure. |
| P-6 | Existing infrastructure is leveraged. | V-038 builds on `tests/architecture/test_composition_root.py`. V-001 extends `scripts/pre_tool_use.py`. Implementation cost is reduced. |
| P-7 | Evidence-based decision with quantified rationale. | 62 vectors evaluated across 7 dimensions with 4 sensitivity tests. Decision is traceable to empirical data, not opinion. |

### Negative

| # | Consequence | Mitigation |
|---|------------|------------|
| N-1 | Implementation spans multiple infrastructure types (hooks, CI, process). | Phase implementation: start with Phase 1 (5 core vectors), expand incrementally. |
| N-2 | L2 (Per-Prompt Reinforcement) depends on Claude Code-specific V-005 (UserPromptSubmit). | V-024 content is portable text. Non-Claude-Code platforms need custom injection middleware. Document alternative integration paths. |
| N-3 | Rule optimization (25,700 to 12,476 tokens) requires significant editorial effort. | TASK-003 provides specific file-by-file reduction targets. Phase 1 prerequisite. |
| N-4 | Four MEDIUM-priority FMEA items require active mitigation. | FM-010-01 (context rot, RPN=168): mitigated by V-024. FM-024-01 (stale content, RPN=126): automated content sync. FM-024-02 (mechanism unavailable, RPN=120): graceful degradation. FM-001-03 (false negatives, RPN=108): layered defense. |
| N-5 | Process vectors (Family 7) require organizational discipline to be effective. | Integrate process enforcement with worktracker; automate quality gates where possible. |

### Monitoring

| # | What to Monitor | Metric | Threshold | Action if Exceeded |
|---|----------------|--------|-----------|-------------------|
| M-1 | Context rot degradation in long sessions | Enforcement compliance rate at 50K+ tokens | < 80% compliance | Increase V-024 reinforcement frequency; add more vectors to reinforcement content |
| M-2 | Token budget utilization | Total enforcement tokens per session | > 17,026 (critical max) | Disable optional prompt patterns (V-018, V-020); optimize rule content further |
| M-3 | False positive rate from AST checks | Blocked operations per session that were valid | > 5% false positive rate | Expand allowlist; adjust validation rules; review V-055 waiver process |
| M-4 | CI pipeline pass rate | Architecture test failures per PR | > 10% of PRs fail on architecture | Review test strictness; update tests for legitimate patterns |
| M-5 | Platform portability coverage | Enforcement test pass rate on Windows | < 90% | Address platform-specific issues identified in TASK-006 |

### Outcome-Based Monitoring

The activity-based metrics above (M-1 through M-5) measure enforcement *process health* (are the vectors running?). The following outcome-based metrics measure enforcement *effectiveness* (are architecture standards being maintained?):

| # | Outcome Metric | KPI | Target | Measurement Method | Review Cadence |
|---|----------------|-----|--------|-------------------|----------------|
| OM-1 | Architecture boundary violation escape rate | Architecture violations merged to main despite enforcement | 0 escapes/quarter | Post-merge CI scan of main branch; compare boundary violations in main vs. total PRs | Quarterly |
| OM-2 | Enforcement-prevented rework | PRs that would have required rework without enforcement (caught pre-merge) | >= 5% of PRs caught | Count pre-commit + CI rejections on architecture-specific checks; track corrected-before-merge rate | Quarterly |
| OM-3 | Developer friction index | Developer complaints or --no-verify usage rate | < 10% of commits use --no-verify | Git hook audit log (if available); developer survey (quarterly) | Quarterly |
| OM-4 | Context rot survival rate | Enforcement compliance in sessions exceeding 100K tokens | >= 60% compliance at 100K+ | Sample long sessions; measure enforcement artifact quality (evidence presence, quality gate compliance) | Semi-annual |
| OM-5 | Enforcement stack health score | Composite score: (layers active / layers total) * (vectors passing / vectors deployed) | >= 0.80 | Automated health check script aggregating CI results, hook status, and process compliance metrics | Monthly |

### Enforcement Lifecycle Management

| Lifecycle Event | Trigger | Action | Owner |
|----------------|---------|--------|-------|
| **Vector retirement** | Vector consistently scores OM-5 < 0.50 for 2 consecutive quarters | Evaluate for removal or replacement; document in ADR amendment | Enforcement maintainer |
| **Threshold recalibration** | Operational data shows > 30% of metrics consistently above/below thresholds | Recalibrate M-1 through M-5 and OM-1 through OM-5 thresholds based on actual distribution | Enforcement maintainer |
| **New vector onboarding** | New enforcement vector added to the stack | Add corresponding M-x and OM-x metrics; establish baseline over first quarter | Vector implementer |
| **ADR status promotion** | OM-1 through OM-5 all meet targets for 2 consecutive quarters post-deployment | Promote ADR status from PROPOSED to ACCEPTED | Architecture team |

### Review Cadence

| Review Type | Frequency | Scope | Decision Authority |
|------------|-----------|-------|--------------------|
| Operational health check | Monthly | M-1 through M-5 activity metrics | Enforcement maintainer |
| Outcome review | Quarterly | OM-1 through OM-5 outcome metrics + threshold recalibration | Architecture team |
| Strategic review | Semi-annual | Full ADR review including vector retirement/addition | Project lead + architecture team |

---

## Evidence Base

### TASK-001: Evaluation Criteria and Weighting Methodology

**Key Output:** 7-dimension evaluation framework with weighted composite scoring.

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Context Rot Resilience (CRR) | 25% | Highest differentiation; correlated failure makes this the most consequential discriminator |
| Effectiveness (EFF) | 20% | Core purpose of enforcement; scored under degraded conditions (50K+ tokens) |
| Platform Portability (PORT) | 18% | User priority #2; 38 LLM-Portable vectors prioritized |
| Token Efficiency (TOK) | 13% | 25,700 token envelope is a hard constraint |
| Bypass Resistance (BYP) | 10% | Adversary model identifies 4 bypass scenarios |
| Implementation Cost (COST) | 8% | One-time investment amortized over framework lifetime |
| Maintainability (MAINT) | 6% | Periodic cost; well-designed vectors correlate with maintainability |

**Scoring Scale:** 1-5 integer scale (not 1-10) to avoid false precision. Maps naturally to TASK-009 qualitative ratings (IMMUNE/LOW/MEDIUM/HIGH for CRR; HIGH/MEDIUM/LOW for effectiveness).

**Confidence:** HIGH -- methodology grounded in user-confirmed priorities and EN-401 empirical analysis.

### TASK-002: Risk Assessment

**Key Output:** 62-vector risk assessment across 7 risk categories; FMEA for 6 Tier 1-2 candidate vectors; 4 correlated risk scenarios.

| Finding | Impact on Decision |
|---------|-------------------|
| R-SYS-001: Context rot cascade (score 20 RED) | Validates V-024 as mandatory mitigation; requires 4+ immune layers |
| R-SYS-002: Token budget exhaustion (score 16 RED) | Validates Phase 1 rule optimization as prerequisite |
| R-SYS-003: Platform migration (score 16 RED) | Validates portable-foundation architecture; hooks as optional enhancers |
| Family 5 all-GREEN risk profile | Validates Family 5 as enforcement foundation |
| 4 MEDIUM-priority FMEA items (RPN 108-168) | All addressable through existing mitigation strategies |
| 0 HIGH-priority FMEA items (RPN >200) | No showstopper risks in Tier 1-2 vectors |

### TASK-003: Architecture Trade Study

**Key Output:** 5-layer enforcement architecture; vector composition matrix; integration architecture mapping to Jerry's hexagonal architecture; Pugh matrix evaluation of 4 architecture alternatives.

| Finding | Impact on Decision |
|---------|-------------------|
| 7 families decompose into 5 execution layers | Defines the temporal enforcement pipeline |
| Only 15-20 vectors should be actively deployed | Supports Tier 1 (16) + selected Tier 2 target |
| "Deterministic skeleton with probabilistic guidance" pattern | Governs the architecture: immune vectors form skeleton; rules provide guidance |
| Token budget: 82.5% goes to L1 rules | Rule optimization has highest token ROI |
| Hybrid approach strictly dominates alternatives | Pugh matrix confirms Option A superiority |

### TASK-004: Priority Matrix

**Key Output:** 59 vectors scored and ranked by WCS; 3 excluded; sensitivity analysis; token budget verification; layer coverage verification.

| Finding | Impact on Decision |
|---------|-------------------|
| 16 Tier 1 vectors (WCS >= 4.00) | Defines immediate implementation set |
| 16 Tier 2 vectors (WCS 3.50-3.99) | Defines near-term implementation set |
| Family 5 averages WCS 4.72 (highest) | Confirms structural enforcement as foundation |
| Family 2 averages WCS 2.61 (lowest) | Confirms rules alone are insufficient |
| Sensitivity: all 4 tests share 9-10/10 top vectors | Prioritization is robust to weight changes |
| Token budget: 15,126 tokens (7.6%) | FEASIBLE -- matches TASK-009 target exactly |

---

## Sensitivity and Robustness

The TASK-001 weighting scheme was stress-tested through four sensitivity tests defined in the evaluation framework:

| Test | Weight Change | Baseline Overlap | Threshold | Result |
|------|--------------|------------------|-----------|--------|
| Test 1: Equal Weights | All dimensions at 14.3% | 10/10 top-10 overlap | >= 7 | **ROBUST** |
| Test 2: Swap CRR/EFF | CRR=20%, EFF=25% | 9/10 top-10 overlap | >= 7 | **ROBUST** |
| Test 3: Double COST | COST=16%, CRR=17% | 10/10 top-10 overlap | >= 7 | **ROBUST** |
| Test 4: Remove PORT | PORT=0%, CRR=30%, EFF=26% | 9/10 top-10 overlap | >= 7 | **ROBUST** |

**Stable vectors (never change tier across all tests):** V-038, V-045, V-044, V-043, V-039, V-041, V-040, V-042, V-060, V-057 (10 vectors).

**Sensitive vectors:** V-024 fluctuates between ranks 8-11 depending on CRR vs. EFF weighting but remains Tier 1 in all scenarios. V-001 enters top-10 only when portability weight is removed (Test 4), confirming that its Tier 2 placement is driven by portability, not enforcement weakness.

**Robustness conclusion:** The top 7 vectors (all Family 5) are absolutely stable. The prioritization would require a radical reweighting (e.g., eliminating both CRR and EFF as criteria) to change the Tier 1 composition significantly.

---

## Token Budget Feasibility

### Standard Enforcement Budget

| Component | Source Vector(s) | Tokens | % of 200K | Layer |
|-----------|-----------------|--------|-----------|-------|
| Optimized .claude/rules/ | V-009, V-010 | 12,476 | 6.24% | L1 |
| Context reinforcement | V-024 | 600 | 0.30% | L2 |
| Self-critique | V-014 | 450 | 0.23% | L4 |
| Schema enforcement | V-022 | 300 | 0.15% | L4 |
| Meta-cognitive reasoning | V-025 | 600 | 0.30% | L4 |
| Few-shot exemplars | V-026 | 400 | 0.20% | L1 |
| CLAUDE.md + system prompt | V-008 | 300 | 0.15% | L1 |
| **Total** | | **15,126** | **7.56%** | |

### Critical Deliverable Budget (Tiered Activation)

| Additional Component | Tokens | Trigger |
|---------------------|--------|---------|
| Self-Refine Loop (V-018) | +900/iteration | Critical deliverables only |
| CoVe + Reflexion (V-019, V-020) | +1,000/deliverable | Critical deliverables only |
| **Critical Max** | **17,026** | **8.51% of 200K** |

### Budget Verification

- Standard budget (15,126 tokens) matches TASK-009 "Full enforcement (amortized)" target exactly.
- Critical max (17,026 tokens) adds 0.95% context cost for approximately 5% incremental compliance benefit (TASK-007 Pattern 3 diminishing returns).
- Zero-token vectors (L3, L5, Process) provide enforcement without any context cost.
- Phase 1 rule optimization (25,700 to 12,476 tokens) is a prerequisite for budget feasibility.

**Token budget concentration acknowledgment:** 82.5% of the enforcement token budget (12,476 of 15,126 tokens) is allocated to L1 (Static Context), which is the layer most vulnerable to context rot (CRR=1-2 per TASK-001). This creates a structural exposure identified as R-SYS-004 (Score 16 RED per TASK-002 v1.1). The concentration is an inherent property of the rules-based enforcement model, not a flaw in budget allocation -- rules must be loaded at session start and consume tokens regardless of whether they remain effective. The defense-in-depth architecture ensures that L1 degradation does not cause complete enforcement failure: L2 (V-024) compensates, and L3/L5/Process layers are immune. See TASK-003 v1.1 "Token budget concentration risk" for detailed analysis.

---

## Compliance

| Principle | ID | Requirement | How This Decision Complies |
|-----------|----|-------------|---------------------------|
| File Persistence | P-002 | Filesystem as infinite memory; persist state to files | Evidence-based closure (V-060) requires file-based proof artifacts. Quality gates (V-057) check file-based criteria. WTI rules (V-062) validate cross-file consistency. Acceptance criteria (V-061) stored in worktracker files. |
| No Recursive Subagents | P-003 | Max ONE level: orchestrator -> worker | NASA IV&V (V-051) implemented via multi-agent separation at one level, not recursive sub-workers. Adversarial review (V-058) uses independent reviewer agents at the same orchestration level. |
| User Authority | P-020 | User decides; never override; ask before destructive ops | Formal waiver process (V-055) enables user-authorized exceptions. PreToolUse hooks (V-001) block operations but do not override user intent -- users can authorize via waiver. All enforcement is transparent (V-049 audit logging). |
| No Deception | P-022 | Never deceive about actions, capabilities, or confidence | Evidence-based closure (V-060) requires proof artifacts, preventing unsubstantiated completion claims. Confidence scores on all TASK-004 ratings. FMEA analysis (TASK-002) transparently documents failure modes. |
| Context Rot Resilience | P-043 | Persist to files to survive context rot | V-024 specifically counteracts context rot. Architecture ensures 4 of 5 layers are immune. File-based vectors (V-060, V-061, V-062) use filesystem persistence per P-002. |

---

## Risks

### Systemic Risks (from TASK-002)

| Risk ID | Description | Score | Level | Mitigation | Residual |
|---------|-------------|-------|-------|------------|----------|
| R-SYS-001 | Context rot degrades all VULNERABLE vectors simultaneously, reducing effective layers from 5 to 2-3 | 20 | RED | V-024 implementation (Tier 1); IMMUNE vectors in L3-L5 provide structural minimum; architecture designed so 4 layers survive rot | YELLOW (10) |
| R-SYS-002 | Token budget not optimized from 25,700 to 12,476 tokens; enforcement competes with productive work | 16 | RED | Phase 1 rule optimization is prerequisite for all other enforcement deployment; tiered prompt activation limits concurrent consumption | GREEN (6) |
| R-SYS-003 | Platform migration renders Claude Code hooks inoperative; enforcement loses L3 blocking | 16 | RED | Architecture ensures L1, L5, and Process layers are 100% portable; hooks are optional enhancers; graceful degradation from HIGH to MODERATE enforcement | YELLOW (8) |
| R-SYS-004 | Combined context rot + token budget exhaustion creates negative feedback loop (logically dependent on R-SYS-001) | 16 | RED | Token optimization reduces base load from 25,700 to ~12,476; tiered activation limits concurrent consumption; session refresh before degradation; IMMUNE layers continue functioning regardless | YELLOW (8) |

### FMEA Summary for Tier 1-2 Vectors

| Vector | Highest RPN | Failure Mode | Priority | Mitigation |
|--------|-------------|-------------|----------|------------|
| V-010 | 168 | Context rot degrades FORBIDDEN/NEVER at 50K+ | MEDIUM | V-024 reinforcement; deterministic layers as backup |
| V-024 | 126 | Stale reinforcement content (rules changed, content not updated) | MEDIUM | Automated content generation from source rule files |
| V-024 | 120 | Injection mechanism (V-005) disabled or unavailable | MEDIUM | Detect at session start; degrade to per-agent injection |
| V-001 | 108 | False negatives (hook misses violation) | MEDIUM | Layered defense: CI (V-045) catches what hooks miss |

**No HIGH-priority FMEA items (RPN > 200) exist for any Tier 1-2 vector.** All 4 MEDIUM items are addressable through existing mitigation strategies.

---

## Implementation Roadmap

### Phase 1: Foundation (Prerequisite)

**Objective:** Optimize token budget and establish context rot countermeasure.

| Vector | Action | Effort | Dependency |
|--------|--------|--------|------------|
| V-009/V-010 | Optimize .claude/rules/ from 25,700 to 12,476 tokens | 2-3 days | None |
| V-024 + V-005 | Implement UserPromptSubmit hook with context reinforcement | 1-3 days | None |
| V-013 | Apply numbered priority prefixes to rule files | < 1 hour | V-009 optimization |

### Phase 2: Structural Foundation

**Objective:** Deploy deterministic, zero-token enforcement foundation.

| Vector | Action | Effort | Dependency |
|--------|--------|--------|------------|
| V-038 | Move AST import validation from tests to PreToolUse hook + pre-commit | 1 day | Existing test_composition_root.py |
| V-044 | Configure .pre-commit-config.yaml with ruff, mypy, AST checks | 1 day | V-038 |
| V-045 | Create .github/workflows/ci.yml with full test suite | 1-3 days | V-044 |
| V-043 | Extend architecture test suite for full boundary coverage | 1-2 days | V-038 |

### Phase 3: Extended Structural + Process

**Objective:** Deploy remaining Tier 1 structural and process vectors.

| Vector | Action | Effort | Dependency |
|--------|--------|--------|------------|
| V-039, V-040, V-041 | Extend AST checks for type hints, docstrings, one-class-per-file | 2-3 days | V-038 |
| V-042 | Add Hypothesis property-based testing infrastructure | 2-3 days | V-045 |
| V-057, V-060 | Implement quality gates and evidence-based closure in worktracker | 3-5 days | Worktracker infrastructure |
| V-056 | Integrate BDD cycle enforcement with quality gates | 1-2 days | V-057 |

### Phase 4: Claude Code Enhancement

**Objective:** Deploy platform-specific blocking vectors for Claude Code users.

| Vector | Action | Effort | Dependency |
|--------|--------|--------|------------|
| V-001 | Extend PreToolUse hook with AST validation for write operations | 1-2 days | V-038 |
| V-002 | Implement PostToolUse validation hook | 1-2 days | V-001 |

### Phase 5+: MCP and Advanced Process

**Objective:** Build MCP infrastructure and advanced process enforcement.

| Vector | Action | Effort | Dependency |
|--------|--------|--------|------------|
| V-049 | First MCP server: audit logging | 1-2 weeks | MCP specification study |
| V-051 | NASA IV&V via independent reviewer agents | 1-2 weeks | Adversarial review infrastructure |
| V-046 | MCP tool wrapping enforcement | 2+ weeks | V-049 (MCP competence) |

---

## Related Decisions

| Decision | Relationship | Status |
|----------|-------------|--------|
| ADR-EPIC002-001: Adversarial Strategy Selection | Upstream: defines adversary model referenced in bypass resistance scoring | Future (planned) |
| EN-401: Enforcement Vector Catalog | Upstream: produces the 62-vector catalog that this ADR prioritizes | COMPLETE |
| EN-402 TASK-001: Evaluation Criteria | Input: defines the 7-dimension scoring framework | COMPLETE |
| EN-402 TASK-002: Risk Assessment | Input: provides FMEA analysis and systemic risk scenarios | COMPLETE |
| EN-402 TASK-003: Architecture Trade Study | Input: defines the 5-layer architecture and composition analysis | COMPLETE |
| EN-402 TASK-004: Priority Matrix | Input: provides the 59-vector ranked matrix with sensitivity analysis | COMPLETE |
| EN-402 TASK-006: Execution Plans | Downstream: consumes top 3 vector profiles for detailed implementation | PLANNED |
| EN-402 TASK-007: Adversarial Review | Downstream: ps-critic stress-tests this ADR | PLANNED |
| EN-403: Rule Optimization | Downstream: implements Phase 1 rule optimization (25,700 to 12,476) | PLANNED |
| EN-404: Structural Enforcement Implementation | Downstream: implements Phase 2 structural vectors (V-038, V-044, V-045) | PLANNED |
| EN-405: Process Enforcement Implementation | Downstream: implements Phase 3 process vectors (V-057, V-060) | PLANNED |

---

## References

### Primary Sources (Direct Input to This ADR)

| # | Citation | Used For |
|---|----------|----------|
| 1 | TASK-001: Evaluation Criteria and Weighting Methodology v1.0 (EN-402) | 7-dimension weights, scoring rubrics, tie-breaking rules, sensitivity test definitions |
| 2 | TASK-002: Risk Assessment for Enforcement Vectors v1.0 (EN-402) | FMEA analysis, 4 systemic risk scenarios (R-SYS-001 through R-SYS-004), risk-based exclusions, per-vector risk scores |
| 3 | TASK-003: Architecture Trade Study v1.0 (EN-402) | 5-layer architecture, composition matrix, token budget allocation, Pugh matrix, integration architecture |
| 4 | TASK-004: Priority Matrix and Composite Scoring v1.0 (EN-402) | 59-vector ranked matrix, sensitivity analysis (4 tests), top 3 profiles, family-level analysis, token budget verification, layer coverage verification |
| 5 | TASK-009: Revised Unified Enforcement Vector Catalog v1.1 (EN-401) | Authoritative 62-vector catalog, context rot vulnerability matrix (Appendix C), token budget (Appendix B), adversary model (Section L2), effectiveness ratings |

### Jerry Framework Sources

| # | Citation | Used For |
|---|----------|----------|
| 6 | `.claude/rules/architecture-standards.md` | Hexagonal architecture rules; layer boundary definitions |
| 7 | `tests/architecture/test_composition_root.py` | Existing AST validation infrastructure (TRL evidence for V-038) |
| 8 | `scripts/pre_tool_use.py` | Existing PreToolUse hook infrastructure (TRL evidence for V-001) |
| 9 | `scripts/session_start_hook.py` | Existing SessionStart hook (TRL evidence for V-003) |
| 10 | `docs/governance/JERRY_CONSTITUTION.md` | Constitutional principles P-002, P-003, P-020, P-022 |

### Methodology Sources

| # | Citation | Used For |
|---|----------|----------|
| 11 | NASA NPR 7123.1D: Systems Engineering Processes and Requirements | Trade study methodology (Process 17: Decision Analysis) |
| 12 | NASA NPR 8000.4C: Agency Risk Management Procedural Requirements | 5x5 risk matrix; risk level classification |
| 13 | NASA-STD-8739.8: Software Assurance and Software Safety Standard | Prevent-detect-verify enforcement principle |
| 14 | IEC 60812:2018: Failure Mode and Effects Analysis (FMEA/FMECA) | FMEA methodology, RPN scoring, severity/occurrence/detection scales |

### Research Sources (Via TASK-009)

| # | Citation | Used For |
|---|----------|----------|
| 15 | Liu, N. F., et al. (2023). "Lost in the Middle: How Language Models Use Long Contexts." arXiv:2307.03172 | Empirical basis for context rot vulnerability assessments; 40-60% effectiveness degradation at 50K+ tokens |

---

**DISCLAIMER:** This ADR is AI-generated based on NASA Systems Engineering standards and IEC 60812 FMEA methodology. It is advisory only and does not constitute official NASA or IEC guidance. All architecture decisions require human review and professional engineering judgment. Not for use in mission-critical decisions without SME validation.

---

*Agent: ps-architect (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-402 Enforcement Priority Analysis & Decision*
*Status: PROPOSED (pending adversarial review iteration 2; see lifecycle note below)*

**Lifecycle note:** This ADR has status PROPOSED per the ADR lifecycle (PROPOSED -> ACCEPTED -> SUPERSEDED/DEPRECATED). The PROPOSED status means this decision has been documented and analyzed but not yet ratified through operational validation. TASK-006 (execution plans) consumes this ADR as input but should be understood as **provisionally dependent** -- if the adversarial review (TASK-007/TASK-008 iteration cycle) or subsequent operational data causes material changes to this ADR, TASK-006 execution plans must be updated accordingly. The ADR status promotion criteria are defined in the Enforcement Lifecycle Management section above: all OM-1 through OM-5 metrics must meet targets for 2 consecutive quarters post-deployment before promoting to ACCEPTED.
*Quality Target: >= 0.92*
*Consumers: TASK-006 (execution plans), TASK-007 (adversarial review), EN-403/404/405 (implementation)*
