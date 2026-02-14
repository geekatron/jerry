# Barrier 1 Cross-Pollination Handoff: ENF to ADV

<!--
DOCUMENT-ID: EPIC002-CROSSPOLL-B1-ENF-TO-ADV
TYPE: Cross-Pollination Handoff Artifact
VERSION: 1.0.0
SOURCE: ENF Pipeline Phase 1 (EN-402: Enforcement Priority Analysis)
TARGET: ADV Pipeline Phase 2 (EN-303: Situational Applicability Mapping)
BARRIER: 1
DIRECTION: ENF -> ADV
DATE: 2026-02-13
PROJECT: PROJ-001-oss-release
EPIC: EPIC-002 (Quality Framework Enforcement)
-->

> **From:** ENF Pipeline (FEAT-005: Enforcement Mechanisms), Phase 1 complete
> **To:** ADV Pipeline (FEAT-004: Adversarial Strategy Research), Phase 2 (EN-303)
> **Barrier:** 1
> **Date:** 2026-02-13
> **Confidence:** HIGH -- all data traceable to EN-402 TASK-001 through TASK-009

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | What ENF Phase 1 produced and what ADV Phase 2 needs |
| [Top 3 Priority Enforcement Vectors](#top-3-priority-enforcement-vectors) | Highest-scoring vectors with layer assignments |
| [5-Layer Enforcement Architecture](#5-layer-enforcement-architecture) | Hybrid layered approach summary |
| [Platform Constraints](#platform-constraints) | Portable vs. platform-specific capabilities |
| [Implementation Capabilities](#implementation-capabilities) | What enforcement CAN and CANNOT do |
| [Feasibility Constraints for Adversarial Strategy Mapping](#feasibility-constraints-for-adversarial-strategy-mapping) | Which enforcement mechanisms map to which adversarial strategies |
| [Risk Summary](#risk-summary) | Key risks affecting adversarial strategy integration |
| [ADR Reference](#adr-reference) | Link to ADR-EPIC002-002 |
| [Source Traceability](#source-traceability) | Full citation chain |

---

## Executive Summary

### What ENF Phase 1 Produced

EN-402 (Enforcement Priority Analysis & Decision) completed all 10 tasks with a final adversarial review quality score of 0.923 (PASS, threshold 0.85). The analysis produced:

1. **A 7-dimension weighted composite scoring (WCS) framework** -- Dimensions: Context Rot Resilience (25%), Effectiveness (20%), Platform Portability (18%), Token Efficiency (13%), Bypass Resistance (10%), Implementation Cost (8%), Maintainability (6%).

2. **A 59-vector priority matrix** -- All 62 vectors from EN-401 scored and ranked. 3 vectors excluded pre-scoring due to RED risk profiles (V-035 Llama Guard, V-029 NeMo Guardrails, V-037 Grammar-Constrained Generation). Distribution: 16 Tier 1, 16 Tier 2, 15 Tier 3, 9 Tier 4, 3 Tier 5.

3. **A 5-layer hybrid enforcement architecture** -- Deterministic skeleton (AST, CI, hooks, processes) with probabilistic guidance (rules, prompts). 4 of 5 layers are context-rot-immune.

4. **A formal ADR (ADR-EPIC002-002)** -- Status: PROPOSED, pending user ratification per P-020. Recommends phased implementation across 5 phases.

5. **Risk assessment** -- 4 RED systemic risks identified; all mitigable. No HIGH-priority FMEA items (RPN > 200) for any Tier 1-2 vector.

### What ADV Phase 2 (EN-303) Needs

EN-303 (Situational Applicability Mapping) must determine which adversarial strategies apply to which enforcement mechanisms and in what situations. This handoff provides:

- **The enforcement mechanisms that exist** (32 Tier 1-2 vectors across 5 layers) so ADV can map adversarial strategies to concrete enforcement targets.
- **What each mechanism CAN and CANNOT enforce** so ADV can identify gaps where adversarial strategies are the sole defense.
- **Platform constraints** so ADV can map strategy applicability to different deployment contexts (Claude Code vs. generic LLM).
- **Risk exposure points** so ADV can prioritize adversarial strategies that address the 4 RED systemic risks.

---

## Top 3 Priority Enforcement Vectors

These are the three highest-scoring vectors designated for detailed execution planning (TASK-006). All three are context-rot-immune, zero-token, universally portable, and deterministic.

| Rank | Vector ID | Name | WCS | Family | Layer(s) | Phase |
|------|-----------|------|-----|--------|----------|-------|
| 1 | V-038 | AST Import Boundary Validation | 4.92 | F5 (Structural) | L3 (Pre-Action) + L5 (Post-Hoc) | Phase 2 |
| 2 | V-045 | CI Pipeline Enforcement | 4.86 | F5 (Structural) | L5 (Post-Hoc) | Phase 2 |
| 3 | V-044 | Pre-commit Hook Validation | 4.80 | F5 (Structural) | L5 (Post-Hoc) | Phase 2 |

### Scoring Breakdown

| Vector | CRR (0.25) | EFF (0.20) | PORT (0.18) | TOK (0.13) | BYP (0.10) | COST (0.08) | MAINT (0.06) |
|--------|------------|------------|-------------|------------|------------|-------------|--------------|
| V-038 | 5 | 5 | 5 | 5 | 5 | 4 | 5 |
| V-045 | 5 | 5 | 5 | 5 | 5 | 3 | 5 |
| V-044 | 5 | 5 | 5 | 5 | 4 | 4 | 4 |

### Full Tier 1 Vectors (16 total, WCS >= 4.00)

| Vector | Name | WCS | Family | Layer |
|--------|------|-----|--------|-------|
| V-038 | AST Import Boundary Validation | 4.92 | F5 | L3/L5 |
| V-045 | CI Pipeline Enforcement | 4.86 | F5 | L5 |
| V-044 | Pre-commit Hook Validation | 4.80 | F5 | L5 |
| V-043 | Architecture Test Suite | 4.80 | F5 | L5 |
| V-039 | AST Type Hint Enforcement | 4.72 | F5 | L3/L5 |
| V-041 | AST One-Class-Per-File Check | 4.72 | F5 | L3/L5 |
| V-040 | AST Docstring Enforcement | 4.72 | F5 | L3/L5 |
| V-042 | Property-Based Testing | 4.50 | F5 | L5 |
| V-057 | Quality Gate Enforcement | 4.38 | F7 | Process |
| V-060 | Evidence-Based Closure | 4.38 | F7 | Process |
| V-061 | Acceptance Criteria Verification | 4.22 | F7 | Process |
| V-024 | Context Reinforcement via Repetition | 4.11 | F3 | L2 |
| V-055 | Formal Waiver Process | 4.02 | F7 | Process |
| V-053 | NASA File Classification | 4.02 | F7 | Process |
| V-056 | BDD Red/Green/Refactor Cycle | 4.02 | F7 | Process |
| V-062 | WTI Rules | 4.02 | F7 | Process |

**Key pattern for ADV:** Family 5 (Structural) dominates with 8 of 16 Tier 1 vectors. Family 7 (Process) contributes 7. All 16 are context-rot-immune. Only V-024 consumes context tokens (600/session).

---

## 5-Layer Enforcement Architecture

The architecture follows a "deterministic skeleton with probabilistic guidance" pattern, firing in strict temporal order per the "prevent, then detect, then verify" principle (NASA-STD-8739.8).

### Layer Summary

| Layer | Timing | Function | Context Rot | Token Cost | Key Vectors |
|-------|--------|----------|-------------|------------|-------------|
| **L1: Static Context** | Session start | Set behavioral foundation via optimized rules | VULNERABLE (compensated by L2) | ~12,476 | V-008, V-009, V-010, V-015-V-017, V-026 |
| **L2: Per-Prompt Reinforcement** | Every prompt | Re-inject critical rules to counteract rot | IMMUNE by design | ~600/session | V-024, V-005 |
| **L3: Pre-Action Gating** | Before tool calls | Deterministically block non-compliant operations | IMMUNE (external) | 0 | V-001, V-038-V-041 |
| **L4: Post-Action Validation** | After tool calls | Inspect outputs; trigger self-correction | MIXED | 0-1,350 | V-002, V-021, V-043, V-049 |
| **L5: Post-Hoc Verification** | Commit/CI time | Catch all violations that escaped runtime layers | IMMUNE (external) | 0 | V-044, V-045, V-042 |
| **Process** | Workflow level | Governance, evidence-based completion | IMMUNE (process-based) | 0 | V-057, V-060, V-056, V-061, V-062 |

### Defense-in-Depth Compensation Chain

Each layer compensates for the failure mode of the layer above it:

| Layer | Primary Failure Mode | Compensated By |
|-------|---------------------|----------------|
| L1 (Static Context) | Context rot after ~20K tokens | L2 re-injects critical rules |
| L2 (Per-Prompt Reinforcement) | LLM ignores re-injected rules | L3 deterministically blocks regardless of LLM state |
| L3 (Pre-Action Gating) | Fail-open on hook error | L4 detects violations in output |
| L4 (Post-Action Validation) | Self-critique degraded by context rot | L5 catches violations at commit/CI |
| L5 (Post-Hoc Verification) | Violations already in codebase | Process blocks task closure without evidence |

**Key architectural property:** 4 of 5 layers remain fully effective under context rot. Only L1 degrades, and it is immediately compensated by L2.

---

## Platform Constraints

### Portability Matrix

| Capability | macOS | Linux | Windows | Notes |
|------------|-------|-------|---------|-------|
| L1: .claude/rules/ (Static Context) | YES | YES | YES | 100% portable text files |
| L2: V-024 content | YES | YES | YES | Portable content; V-005 delivery mechanism is Claude Code-specific |
| L3: Claude Code hooks (V-001) | YES | YES | PARTIAL | Claude Code supports macOS/Linux natively; Windows via WSL |
| L3: AST checks (V-038-V-041) | YES | YES | YES | Pure Python, no OS dependency |
| L4: Claude Code hooks (V-002) | YES | YES | PARTIAL | Same as L3 hooks |
| L5: Pre-commit (V-044) | YES | YES | YES | git hooks are universal |
| L5: CI Pipeline (V-045) | YES | YES | YES | GitHub Actions runs on all platforms |
| Process: V-057, V-060, etc. | YES | YES | YES | Process enforcement is platform-independent |

### Hook Availability by Platform

| Hook | Claude Code | Cursor | Windsurf | Generic LLM |
|------|------------|--------|----------|-------------|
| PreToolUse (V-001) | YES | NO | NO | NO |
| PostToolUse (V-002) | YES | NO | NO | NO |
| SessionStart (V-003) | YES | NO | NO | NO |
| UserPromptSubmit (V-005) | YES | NO | NO | NO |

**Key constraint for ADV:** 7 Family 1 (Hook) vectors are Claude Code-exclusive (PORT=1). However, these hooks are optional enhancers, not required enforcement. The core enforcement stack (L1, L5, Process) is 100% portable. Architecture degrades gracefully from HIGH to MODERATE enforcement without hooks.

### Windows-Specific Considerations

- Overall Windows compatibility estimated at 73% (TASK-003)
- `fcntl` replaced with `filelock` for Windows compatibility (commit `f89f7ff`)
- `splitlines()` used for CRLF compatibility (commit `49a708e`)
- Claude Code hooks require WSL on Windows

---

## Implementation Capabilities

### What Enforcement CAN Do (Automated + Process)

| Category | Mechanism | Examples | Enforcement Type |
|----------|-----------|---------|-----------------|
| **Import boundaries** | AST analysis (V-038) | Domain layer cannot import infrastructure | Deterministic, automated |
| **Code structure** | AST checks (V-039-V-041) | Type hints required, one-class-per-file, docstrings | Deterministic, automated |
| **Code quality** | Pre-commit + CI (V-044, V-045) | ruff, mypy, pytest pass required | Deterministic, automated |
| **Architecture compliance** | Test suite (V-043) | Layer boundary enforcement | Deterministic, automated |
| **Quality gates** | Process (V-057) | Completion requires evidence | Process-enforced |
| **Evidence-based closure** | Process (V-060) | No task completion without proof artifacts | Process-enforced |
| **Acceptance criteria** | Process (V-061) | All ACs must be verified before closure | Process-enforced |
| **Context rot countermeasure** | Per-prompt injection (V-024) | Critical rules re-injected every prompt | Automated (with V-005) |

### What Enforcement CANNOT Do

| Gap | Why | Current Mitigation | ADV Opportunity |
|-----|-----|-------------------|-----------------|
| **Prevent context rot** | Inherent LLM limitation; context window degrades with length | V-024 compensates but cannot eliminate | Adversarial strategies for session management, context hygiene |
| **Enforce semantic quality** | AST checks structure, not meaning; "correct code" != "good code" | Process vectors (reviews, BDD) provide indirect checks | Adversarial review patterns, semantic validators |
| **Prevent social engineering** | User can disable hooks, bypass pre-commit (`--no-verify`) | CI (V-045) as mandatory backstop; requires branch protection | Adversarial strategies for human-in-the-loop enforcement |
| **Control token-level generation** | Jerry does not control LLM token generation | N/A -- architecturally out of scope | Not applicable |
| **Enforce across LLM platforms** | Hooks are Claude Code-specific | Portable L1/L5/Process stack provides baseline | Adversarial strategies that are platform-agnostic |
| **Detect novel violation types** | AST rules are pre-defined; cannot catch unknown patterns | Property-based testing (V-042) catches some edge cases | Adversarial exploration for unknown violation categories |

---

## Feasibility Constraints for Adversarial Strategy Mapping

This section maps enforcement mechanism types to adversarial strategy applicability, to guide EN-303 situational mapping.

### Automated Enforcement (Hooks, CI, AST)

These mechanisms fire without human intervention and can enforce adversarial strategies that are:

| Characteristic | Feasible? | Examples |
|---------------|-----------|---------|
| Deterministic rules | YES | Import boundary violations, missing type hints |
| Pattern-matchable violations | YES | File naming conventions, one-class-per-file |
| Testable properties | YES | Code compiles, tests pass, coverage thresholds |
| Context-dependent judgments | NO | "Is this the right abstraction?" |
| Semantic correctness | NO | "Does this logic match the requirement?" |

**Adversarial strategies that CAN be automated:**
- Mutation testing (V-042 property-based testing)
- Boundary violation detection (V-038 AST)
- Regression detection (V-045 CI)
- Structure enforcement (V-039-V-041 AST)

### Process Enforcement (Rules, Procedures)

These mechanisms require human or LLM agent triggers and can enforce strategies that need:

| Characteristic | Feasible? | Examples |
|---------------|-----------|---------|
| Evidence collection | YES | Quality gates requiring proof artifacts (V-057, V-060) |
| Multi-step review | YES | Adversarial review with creator/critic pattern (V-058) |
| Cross-agent validation | YES | Independent verification by separate agent (V-051) |
| Subjective assessment | PARTIAL | Requires structured rubrics to reduce subjectivity |
| Real-time blocking | NO | Process gates fire at workflow transitions, not real-time |

**Adversarial strategies that need process enforcement:**
- Steelman/Devil's Advocate review patterns
- NASA IV&V independence (V-051)
- FMEA risk analysis (V-054)
- Evidence-based completion verification

### Hybrid (Automated Trigger, Human/Agent Execution)

| Mechanism | Trigger | Execution | Example |
|-----------|---------|-----------|---------|
| V-001 PreToolUse + V-058 Adversarial Review | Hook detects write operation | Agent performs adversarial critique | Auto-triggered code review |
| V-057 Quality Gate + V-060 Evidence | Worktracker state change | Agent verifies evidence artifacts | Completion gate with proof check |
| V-024 Context Reinforcement + V-021 CRITIC | Per-prompt injection | Agent applies CRITIC pattern | Continuous self-critique reinforcement |

---

## Risk Summary

### 4 RED Systemic Risks

| Risk ID | Description | Score | Impact on Adversarial Strategy Integration |
|---------|-------------|-------|-------------------------------------------|
| **R-SYS-001** | Context rot degrades all VULNERABLE vectors simultaneously (correlated failure). Effective layers drop from 5 to 2-3. | 20 (RED) | ADV strategies must account for 40-60% effectiveness degradation at 50K+ tokens. Strategies targeting L1-dependent enforcement have diminished returns in long sessions. |
| **R-SYS-002** | Token budget not optimized (25,700 vs. target 12,476 tokens). Enforcement competes with productive work. | 16 (RED) | Adversarial strategies that consume tokens (prompt patterns, self-critique loops) must be budgeted against the 15,126 token enforcement envelope. |
| **R-SYS-003** | Platform migration renders Claude Code hooks inoperative. L3 blocking lost. | 16 (RED) | Adversarial strategies must have portable fallbacks. Cannot rely on Claude Code hooks as sole enforcement for any strategy. |
| **R-SYS-004** | Context rot + token exhaustion negative feedback loop. More enforcement content accelerates rot. | 16 (RED) | Adversarial strategies must be token-efficient. Aggressive in-context adversarial patterns can worsen this feedback loop. |

### Token Budget Concentration Risk

- **82.5% of enforcement tokens** (12,476 of 15,126) are allocated to L1 (Static Context)
- L1 is the layer MOST VULNERABLE to context rot (CRR=1-2)
- This is an inherent property of rules-based enforcement, not a flaw in allocation
- Defense-in-depth ensures L1 degradation does not cause total enforcement failure
- **ADV implication:** Adversarial strategies should preferentially target immune layers (L3, L5, Process) rather than token-heavy vulnerable layers (L1)

### FMEA Summary (No HIGH-Priority Items)

| Vector | Highest RPN | Failure Mode | Priority |
|--------|-------------|-------------|----------|
| V-010 | 168 | Context rot degrades FORBIDDEN/NEVER at 50K+ | MEDIUM |
| V-024 | 126 | Stale reinforcement content | MEDIUM |
| V-024 | 120 | Injection mechanism (V-005) disabled | MEDIUM |
| V-001 | 108 | False negatives (hook misses violation) | MEDIUM |

All MEDIUM-priority items are addressable through existing mitigation strategies. No RPN > 200 exists for any Tier 1-2 vector.

---

## ADR Reference

**ADR-EPIC002-002: Enforcement Vector Prioritization for Jerry Quality Framework**

| Attribute | Value |
|-----------|-------|
| **Status** | PROPOSED (pending user ratification per P-020) |
| **Location** | `FEAT-005-enforcement-mechanisms/EN-402-enforcement-priority-analysis/TASK-005-enforcement-ADR.md` |
| **Decision** | Adopt 5-layer hybrid enforcement architecture with 16 Tier 1 vectors for immediate implementation |
| **Architecture** | Option A: Hybrid Layered Approach (chosen over Rules-Only, Hooks-Heavy, CI-Only) |
| **Quality Score** | Adversarial review: 0.850 (iter 1) -> 0.923 (iter 2, PASS) |
| **Ratification** | Requires user approval before promotion from PROPOSED to ACCEPTED |
| **Downstream** | EN-403 (Rule Optimization), EN-404 (Structural Enforcement), EN-405 (Process Enforcement) |

**Note for ADV pipeline:** This ADR is PROPOSED, not ACCEPTED. ADV Phase 2 should treat it as the best-available decision but acknowledge that user ratification may introduce modifications. Any adversarial strategy mapping should be robust to minor changes in vector prioritization or layer assignments.

---

## Source Traceability

### ENF Phase 1 Artifacts Consumed

| Artifact | Document ID | Key Data Extracted |
|----------|-------------|-------------------|
| EN-402 Enabler | FEAT-005:EN-402 | Task completion status, AC verification (7/7 pass) |
| TASK-001: Evaluation Criteria | FEAT-005:EN-402-TASK-001 | 7-dimension WCS formula, weights, sensitivity tests |
| TASK-002: Risk Assessment | FEAT-005:EN-402-TASK-002 | 4 RED systemic risks, FMEA for Tier 1-2 vectors, risk portfolio (4 RED / 13 YELLOW / 45 GREEN) |
| TASK-003: Trade Study | FEAT-005:EN-402-TASK-003 | 5-layer architecture, composition matrix, Pugh matrix, defense-in-depth pattern |
| TASK-004: Priority Matrix | FEAT-005:EN-402-TASK-004 | 59-vector ranked matrix, tier distribution, top 3 profiles, token budget verification, layer coverage verification |
| TASK-005: Enforcement ADR | FEAT-005:EN-402-TASK-005 (ADR-EPIC002-002) | Architecture decision, implementation roadmap (5 phases), compliance mapping, options considered |

### ADV Phase 2 Target

| Artifact | Expected Consumer Use |
|----------|----------------------|
| EN-303: Situational Applicability Mapping | Map adversarial strategies to enforcement layers, identify gaps where adversarial review is sole defense, determine platform-specific applicability |

---

*Handoff Agent: Worker (Claude Opus 4.6)*
*Date: 2026-02-13*
*Barrier: 1*
*Direction: ENF -> ADV*
*Quality: Data fully traced to EN-402 TASK-001 through TASK-005*
