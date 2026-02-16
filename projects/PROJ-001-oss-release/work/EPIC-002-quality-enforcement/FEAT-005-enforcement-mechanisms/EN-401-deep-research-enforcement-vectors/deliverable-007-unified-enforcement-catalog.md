# TASK-007: Unified Enforcement Vector Catalog -- EN-401 Synthesis

<!--
TEMPLATE: Synthesis Artifact
VERSION: 1.0.0
SOURCE: EN-401 Deep Research (TASK-001 through TASK-006)
AGENT: ps-synthesizer
DATE: 2026-02-13
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Strategic overview for stakeholders |
| [L1: Unified Vector Catalog](#l1-unified-vector-catalog) | Complete enumeration of all 62 enforcement vectors |
| [L2: Detailed Analysis](#l2-detailed-analysis) | Trade-offs, decision matrix, architecture, meta-analysis |
| [Appendices](#appendices) | Full vector inventory table, source cross-reference |
| [References](#references) | All citations from TASK-001 through TASK-006 |

---

## L0: Executive Summary

### What We Found

Six deep-research tasks (TASK-001 through TASK-006) surveyed the full landscape of enforcement mechanisms available to Jerry. The research identified **62 distinct enforcement vectors** across 5 categories, drawn from Claude Code hooks, 9 industry guardrail frameworks, 14 prompt engineering patterns, 18 alternative mechanisms, and a full platform portability assessment.

### Key Finding

**Jerry's enforcement challenge is not a lack of vectors but a lack of layering.** The research consistently shows that no single enforcement mechanism achieves both high reliability and high portability. The solution is a defense-in-depth architecture where each layer compensates for the weaknesses of the layers above it.

### Critical Numbers

| Metric | Value |
|--------|-------|
| Total enforcement vectors identified | 62 |
| LLM-portable vectors (work on any LLM) | 38 (61.3%) |
| Claude Code-specific vectors | 7 (11.3%) |
| Framework-specific vectors | 10 (16.1%) |
| Hybrid vectors | 6 (9.7%) |
| OS-specific vectors | 1 (1.6%) |
| Recommended enforcement token budget | ~3.5% of context (~7,000 tokens/session) |
| Platform compatibility: macOS / Linux / Windows | 98% / 97% / 73% |

### Strategic Recommendation

Implement a **6-layer portable enforcement stack** with graceful degradation:

1. **Foundation Layer** (NASA SE patterns) -- 100% portable, process rigor
2. **Prompt Layer** (self-critique, checklists, reinforcement) -- 100% portable, runtime guidance
3. **Structural Layer** (AST validation, property testing) -- 100% portable, code-level enforcement
4. **Protocol Layer** (MCP enforcement server) -- ~80% portable, protocol-level control
5. **Platform Layer** (Claude Code hooks) -- 0% portable, highest enforcement power
6. **CI Layer** (pre-commit, GitHub Actions) -- ~95% portable, post-hoc verification

Each layer adds enforcement strength. Jerry should implement from the foundation up, ensuring the system remains functional even when platform-specific layers are unavailable.

---

## L1: Unified Vector Catalog

### Catalog Organization

Vectors are organized by enforcement family. Each entry includes:
- **ID**: Unique vector identifier (V-NNN)
- **Name**: Descriptive name
- **Source**: Research task(s) that identified it
- **Category**: Claude Code-specific, LLM-portable, Framework-specific, OS-specific, or Hybrid
- **Mechanism**: How enforcement is applied
- **Effectiveness**: HIGH / MEDIUM / LOW
- **Reliability**: HIGH (deterministic) / MEDIUM (probabilistic) / LOW (advisory)
- **Portability**: HIGH (any LLM/platform) / MEDIUM (most platforms) / LOW (single platform)
- **Maintenance Cost**: HIGH / MEDIUM / LOW
- **Failure Mode**: How it fails when it fails

---

### Family 1: Claude Code Hooks (7 vectors)

| ID | Name | Mechanism | Effectiveness | Reliability | Portability | Maint. Cost | Failure Mode |
|----|------|-----------|---------------|-------------|-------------|-------------|--------------|
| V-001 | PreToolUse Blocking | Hook intercepts tool calls, returns `{"decision":"block"}` | HIGH | HIGH | LOW | MEDIUM | Fail-open (tool proceeds if hook errors) |
| V-002 | PostToolUse Validation | Hook inspects tool output, logs violations | MEDIUM | HIGH | LOW | MEDIUM | Silent pass-through on error |
| V-003 | SessionStart Injection | Hook injects rules/context at session start | MEDIUM | HIGH | LOW | LOW | One-time only; no reinforcement |
| V-004 | Stop Hook (Subagent) | Controls subagent termination | MEDIUM | HIGH | LOW | LOW | Only applies to subagents |
| V-005 | UserPromptSubmit Reinsertion | Re-injects rules on every user prompt | HIGH | HIGH | LOW | MEDIUM | Only in settings.json, not plugin hooks |
| V-006 | Hook Chaining (Multi-Hook) | Multiple hooks in sequence for defense-in-depth | HIGH | HIGH | LOW | HIGH | Complexity increases; ordering matters |
| V-007 | Stateful Hook Enforcement | Hooks read/write `.jerry/enforcement/` state files | HIGH | MEDIUM | LOW | HIGH | Filesystem race conditions; state drift |

**Family Summary**: Highest enforcement power (can block operations deterministically), but zero portability outside Claude Code. Hooks are stateless by default; statefulness requires filesystem workarounds. Performance budget: ~100ms per PreToolUse/PostToolUse call, ~5000ms for SessionStart.

---

### Family 2: Rules-Based Enforcement (6 vectors)

| ID | Name | Mechanism | Effectiveness | Reliability | Portability | Maint. Cost | Failure Mode |
|----|------|-----------|---------------|-------------|-------------|-------------|--------------|
| V-008 | CLAUDE.md Root Context | Top-level instructions loaded at session start | MEDIUM | LOW | HIGH | LOW | Context rot degrades compliance over time |
| V-009 | .claude/rules/ Auto-Loaded | Rule files auto-loaded by Claude Code | HIGH | MEDIUM | LOW | MEDIUM | Platform-specific loading mechanism |
| V-010 | Hard Constraint Rules | FORBIDDEN/NEVER/MUST patterns | HIGH | MEDIUM | HIGH | LOW | Probabilistic compliance; no enforcement |
| V-011 | Soft Guidance Rules | SHOULD/PREFER patterns | LOW | LOW | HIGH | LOW | Easily ignored under context pressure |
| V-012 | AGENTS.md Agent Registry | Agent definitions and boundaries | MEDIUM | LOW | HIGH | LOW | Advisory only; no runtime enforcement |
| V-013 | Numbered Priority Rules | Rules prefixed 01- through 09- for priority ordering | MEDIUM | MEDIUM | HIGH | LOW | Ordering may not survive context rot |

**Family Summary**: Lowest enforcement power (advisory only), but highest portability and lowest maintenance cost. The FORBIDDEN/CORRECT pattern (from `python-environment.md`) achieves the best compliance rates. Current rules consume ~25,700 tokens (~12.9% of 200K context); optimizable to ~12,476 tokens (53% reduction). Context rot is the primary failure mode -- instructions in the middle of context receive ~20% less attention than those at the beginning or end.

---

### Family 3: Prompt Engineering Enforcement (14 vectors)

| ID | Name | Mechanism | Effectiveness | Reliability | Portability | Maint. Cost | Failure Mode |
|----|------|-----------|---------------|-------------|-------------|-------------|--------------|
| V-014 | Constitutional AI Self-Critique (P1) | LLM critiques own output against principles | HIGH | MEDIUM | HIGH | MEDIUM | Adds latency; may over-correct |
| V-015 | System Message Hierarchy (P2) | Layered system prompts with priority | HIGH | MEDIUM | HIGH | LOW | Platform-dependent prompt handling |
| V-016 | Structured Imperative Rules (P3) | DO/DO NOT explicit directives | HIGH | MEDIUM | HIGH | LOW | Context rot degrades over session |
| V-017 | XML Tag Demarcation (P4) | `<rule>`, `<constraint>` tags for structure | MEDIUM | MEDIUM | HIGH | LOW | LLM may ignore tags under pressure |
| V-018 | Self-Refine Loop (P5) | Iterative self-improvement passes | HIGH | MEDIUM | HIGH | HIGH | 2-3x token cost per iteration |
| V-019 | Reflexion (P6) | Episodic memory of past failures | HIGH | MEDIUM | HIGH | HIGH | Requires persistent memory mechanism |
| V-020 | Chain-of-Verification (P7) | Generates verification questions, re-checks | HIGH | MEDIUM | HIGH | MEDIUM | Adds ~50% token overhead |
| V-021 | CRITIC Pattern (P8) | External tool verification of claims | HIGH | HIGH | MEDIUM | HIGH | Requires tool access for verification |
| V-022 | Schema-Enforced Output (P9) | JSON Schema / structured output constraints | HIGH | HIGH | MEDIUM | MEDIUM | Schema complexity limits flexibility |
| V-023 | Pre-Action Checklists (P10) | Explicit checklist before each action | MEDIUM | MEDIUM | HIGH | LOW | Checklist fatigue; may be skipped |
| V-024 | Context Reinforcement via Repetition (P11) | Re-inject critical rules periodically | HIGH | HIGH | HIGH | MEDIUM | Token budget for re-injection |
| V-025 | Meta-Cognitive Reasoning (P12) | "Think about your thinking" prompts | MEDIUM | LOW | HIGH | LOW | Unreliable; hard to verify compliance |
| V-026 | Few-Shot Exemplars (P13) | Correct/incorrect examples in context | HIGH | MEDIUM | HIGH | MEDIUM | Token cost for examples; context rot |
| V-027 | Confidence Calibration (P14) | Explicit uncertainty quantification | MEDIUM | LOW | HIGH | LOW | LLMs poorly calibrated by default |

**Family Summary**: Highest portability (works on any LLM), moderate effectiveness. The critical missing pattern in Jerry is V-024 (Context Reinforcement via Repetition) -- Jerry currently loads rules once and never re-injects them. Recommended implementation tiers: Tier 1 Always Active (P2+P4+P3+P11, ~300 tokens/injection), Tier 2 Per-Agent (P1+P10+P9, ~450 tokens/agent), Tier 3 Per-Deliverable (P5+P7+P13, ~3x base per iteration). Total enforcement token budget: ~3.5% of context.

---

### Family 4: Guardrail Framework Patterns (10 vectors)

| ID | Name | Mechanism | Effectiveness | Reliability | Portability | Maint. Cost | Failure Mode |
|----|------|-----------|---------------|-------------|-------------|-------------|--------------|
| V-028 | Validator Composition (Guardrails AI) | Chain of typed validators on output | HIGH | HIGH | MEDIUM | MEDIUM | Validator ordering matters; chain breaks |
| V-029 | Programmable Rails (NeMo) | Colang flow definitions for dialogue control | HIGH | HIGH | LOW | HIGH | NeMo-specific DSL; learning curve |
| V-030 | State Machine Enforcement (LangGraph) | Finite state machine controls workflow transitions | HIGH | HIGH | MEDIUM | MEDIUM | State explosion for complex workflows |
| V-031 | Self-Critique Loop (Constitutional AI) | Automated critique-revision cycle | HIGH | MEDIUM | HIGH | MEDIUM | Token cost; convergence not guaranteed |
| V-032 | Multi-Layer Defense (Rebuff/NeMo/Guardrails) | Input + output + workflow guards | HIGH | HIGH | MEDIUM | HIGH | Complexity; false positive accumulation |
| V-033 | Structured Output Enforcement (Instructor/Outlines) | Pydantic model / grammar-constrained generation | HIGH | HIGH | MEDIUM | MEDIUM | Constrains creativity; schema rigidity |
| V-034 | Task Guardrails (CrewAI) | Per-task output validation rules | MEDIUM | MEDIUM | LOW | MEDIUM | CrewAI-specific API |
| V-035 | Content Classification (Llama Guard) | ML-based content safety classification | HIGH | HIGH | LOW | HIGH | Requires separate model; latency |
| V-036 | Prompt Injection Detection (Rebuff) | Multi-layer injection attack detection | HIGH | HIGH | MEDIUM | HIGH | Arms race with attackers |
| V-037 | Grammar-Constrained Generation (Outlines/LMQL) | Token-level grammar enforcement | HIGH | HIGH | LOW | MEDIUM | Limits to supported model backends |

**Family Summary**: Industry frameworks demonstrate convergence on three enforcement levels: input-level (NeMo input rails, Rebuff), output-level (Guardrails AI validators, structured output), and workflow-level (LangGraph state machines, CrewAI task guards). Jerry's unique position is enforcing **process compliance** rather than content safety. The most transferable patterns for Jerry are Validator Composition (V-028), State Machine Enforcement (V-030), and Self-Critique Loop (V-031).

---

### Family 5: Structural/Code-Level Enforcement (8 vectors)

| ID | Name | Mechanism | Effectiveness | Reliability | Portability | Maint. Cost | Failure Mode |
|----|------|-----------|---------------|-------------|-------------|-------------|--------------|
| V-038 | AST Import Boundary Validation | Parse Python AST to check import violations | HIGH | HIGH | HIGH | LOW | Only catches import-level violations |
| V-039 | AST Type Hint Enforcement | Verify type annotations present on public APIs | HIGH | HIGH | HIGH | LOW | Cannot verify hint correctness |
| V-040 | AST Docstring Enforcement | Check docstrings on public functions/classes | MEDIUM | HIGH | HIGH | LOW | Cannot verify docstring quality |
| V-041 | AST One-Class-Per-File Check | Verify single public class per module | MEDIUM | HIGH | HIGH | LOW | Legitimate exceptions exist |
| V-042 | Property-Based Testing (Hypothesis) | Generative test inputs finding edge cases | HIGH | HIGH | HIGH | MEDIUM | Requires test infrastructure investment |
| V-043 | Architecture Test Suite | pytest tests verifying layer boundaries | HIGH | HIGH | HIGH | MEDIUM | Tests must be maintained alongside code |
| V-044 | Pre-commit Hook Validation | Git hooks run checks before commit | HIGH | HIGH | HIGH | MEDIUM | Can be bypassed with --no-verify |
| V-045 | CI Pipeline Enforcement | GitHub Actions / CI checks on push/PR | HIGH | HIGH | HIGH | MEDIUM | Post-hoc; doesn't prevent writing violations |

**Family Summary**: Highest reliability (deterministic, tool-based). AST validation (V-038) scores highest in the alternative enforcement comparative analysis (22/25) due to lowest effort and existing infrastructure in `tests/architecture/test_composition_root.py`. Moving AST checks from test-time to write-time via PreToolUse hooks creates real-time enforcement. Property-based testing (V-042) complements by finding edge cases that static analysis misses.

---

### Family 6: Protocol-Level Enforcement (5 vectors)

| ID | Name | Mechanism | Effectiveness | Reliability | Portability | Maint. Cost | Failure Mode |
|----|------|-----------|---------------|-------------|-------------|-------------|--------------|
| V-046 | MCP Tool Wrapping | Wrap tool calls with parameter validation | HIGH | HIGH | MEDIUM | MEDIUM | MCP adoption still growing |
| V-047 | MCP Resource Injection | Inject dynamic rules via MCP resources | HIGH | MEDIUM | MEDIUM | MEDIUM | Resource staleness if not refreshed |
| V-048 | MCP Enforcement Prompts | Structured review templates via MCP | MEDIUM | MEDIUM | MEDIUM | LOW | Prompt compliance is probabilistic |
| V-049 | MCP Audit Logging | Protocol-level audit trail of all operations | MEDIUM | HIGH | MEDIUM | LOW | Logging without enforcement is passive |
| V-050 | MCP Server Composition | Multiple MCP servers for separation of concerns | HIGH | HIGH | MEDIUM | HIGH | Server coordination complexity |

**Family Summary**: MCP-based enforcement (composite score 21/25) offers protocol-level control that works across MCP-compatible clients. Three enforcement primitives: tool wrapping (structural parameter enforcement), resource providers (dynamic rule injection), and enforcement prompts (structured review). Recommended 3-phase implementation: (1) audit logging, (2) tool wrappers, (3) resource providers. MCP is an open standard with growing adoption beyond Claude Code.

---

### Family 7: Process/Methodology Enforcement (12 vectors)

| ID | Name | Mechanism | Effectiveness | Reliability | Portability | Maint. Cost | Failure Mode |
|----|------|-----------|---------------|-------------|-------------|-------------|--------------|
| V-051 | NASA IV&V Independence | Independent verification separate from development | HIGH | HIGH | HIGH | HIGH | Organizational overhead |
| V-052 | VCRM (Verification Cross-Reference Matrix) | Requirements-to-verification traceability | HIGH | HIGH | HIGH | HIGH | Matrix maintenance burden |
| V-053 | NASA File Classification (Classes A-D) | Rigor level based on criticality | HIGH | MEDIUM | HIGH | MEDIUM | Classification subjectivity |
| V-054 | FMEA (Failure Mode and Effects Analysis) | Systematic failure analysis with RPN scoring | HIGH | HIGH | HIGH | HIGH | Analysis paralysis risk |
| V-055 | Formal Waiver Process | Documented exceptions with justification | MEDIUM | HIGH | HIGH | MEDIUM | Waiver accumulation weakens standards |
| V-056 | BDD Red/Green/Refactor Cycle | Test-first development enforcement | HIGH | HIGH | HIGH | MEDIUM | Requires discipline; no tooling enforcement |
| V-057 | Quality Gate Enforcement | Completion blocked until criteria met | HIGH | HIGH | HIGH | MEDIUM | Gate criteria must be well-defined |
| V-058 | Adversarial Review (Red Team/Blue Team) | Structured critique cycles | HIGH | MEDIUM | HIGH | HIGH | Reviewer quality varies |
| V-059 | Multi-Agent Cross-Pollination | Parallel pipelines with sync barriers | HIGH | MEDIUM | HIGH | HIGH | Orchestration complexity |
| V-060 | Evidence-Based Closure | Require proof artifacts before status change | HIGH | HIGH | HIGH | MEDIUM | Evidence quality hard to validate |
| V-061 | Acceptance Criteria Verification | Checklist-based completion verification | MEDIUM | MEDIUM | HIGH | LOW | Criteria may be poorly defined |
| V-062 | Worktracker Integrity Rules (WTI) | Cross-file consistency validation | HIGH | HIGH | HIGH | MEDIUM | Rule set must be maintained |

**Family Summary**: 100% portable (process-based, no platform dependency). NASA SE patterns (composite score 20/25) bring proven rigor from mission-critical systems engineering. These vectors form the foundation layer of the recommended enforcement architecture. They have the highest maintenance cost but also the highest bypass resistance -- process enforcement is harder to circumvent than technical enforcement because it requires human/agent compliance at the workflow level.

---

## L2: Detailed Analysis

### Trade-Off Analysis

#### Dimension 1: Enforcement Strength vs. Flexibility

```
HIGH Enforcement ─────────────────────────────────────────── HIGH Flexibility
     │                                                            │
     │  V-001 PreToolUse Blocking                                 │
     │  V-038 AST Import Validation                               │
     │  V-046 MCP Tool Wrapping                                   │
     │  V-033 Structured Output                                   │
     │                                                            │
     │           V-030 State Machine              V-014 Self-Critique
     │           V-028 Validator Chain             V-024 Repetition
     │           V-044 Pre-commit Hooks            V-018 Self-Refine
     │                                                            │
     │                        V-057 Quality Gates                 │
     │                        V-051 IV&V Independence             │
     │                                                            │
     │                                   V-010 Hard Constraint Rules
     │                                   V-023 Checklists          │
     │                                   V-008 CLAUDE.md           │
     │                                                            │
LOW Enforcement ──────────────────────────────────────────── LOW Flexibility
```

**Key Insight**: Deterministic vectors (AST, hooks, structured output) offer the highest enforcement but constrain the LLM's ability to handle novel situations. Probabilistic vectors (self-critique, rules, checklists) maintain flexibility but cannot guarantee compliance. The optimal architecture layers both: deterministic enforcement for critical invariants, probabilistic enforcement for guidelines.

#### Dimension 2: Maintenance Cost vs. Coverage

| Maintenance Cost | Low Coverage | Medium Coverage | High Coverage |
|-----------------|-------------|-----------------|---------------|
| **LOW** | V-008 CLAUDE.md | V-010 Hard Rules, V-023 Checklists | V-013 Numbered Rules |
| **MEDIUM** | V-004 Stop Hook | V-001 PreToolUse, V-038 AST, V-046 MCP | V-024 Repetition, V-028 Validators |
| **HIGH** | V-029 NeMo Rails | V-007 Stateful Hooks, V-050 MCP Composition | V-032 Multi-Layer, V-051 IV&V |

**Key Insight**: The best ROI vectors are in the MEDIUM maintenance / MEDIUM-HIGH coverage quadrant: PreToolUse blocking (V-001), AST validation (V-038), MCP tool wrapping (V-046), and context reinforcement (V-024). These provide strong coverage without overwhelming maintenance burden.

#### Dimension 3: Portability vs. Platform Optimization

| | HIGH Portability | MEDIUM Portability | LOW Portability |
|---|---|---|---|
| **HIGH Optimization** | V-038 AST, V-042 Property Testing, V-051 IV&V | V-046 MCP Wrapping, V-028 Validators | V-001 PreToolUse, V-005 UserPromptSubmit |
| **MEDIUM Optimization** | V-014 Self-Critique, V-024 Repetition, V-057 Quality Gates | V-030 State Machine, V-033 Structured Output | V-006 Hook Chaining, V-009 .claude/rules/ |
| **LOW Optimization** | V-008 CLAUDE.md, V-011 Soft Rules, V-025 Meta-Cognitive | V-048 MCP Prompts, V-049 MCP Audit | V-003 SessionStart |

**Key Insight**: Jerry's highest-enforcement-power vectors (PreToolUse, UserPromptSubmit) are Claude Code-specific with zero portability. The recommended strategy is to build the enforcement stack from highly portable foundations (AST, NASA processes, prompt patterns) and add platform-specific layers as optional enhancers. This ensures Jerry remains functional on any LLM platform while achieving maximum enforcement on Claude Code.

---

### Decision Matrix

#### Use Case: Preventing Architecture Violations (Import Boundaries)

| Priority | Vector | Why |
|----------|--------|-----|
| 1 | V-038 AST Import Boundary Validation | Deterministic, catches violations at code level |
| 2 | V-001 PreToolUse Blocking | Real-time blocking before file is written |
| 3 | V-043 Architecture Test Suite | Catches violations that slip through |
| 4 | V-044 Pre-commit Hook Validation | Last line of defense before commit |
| 5 | V-010 Hard Constraint Rules | Guides behavior; reduces violation attempts |

#### Use Case: Enforcing Test-First Development (BDD Cycle)

| Priority | Vector | Why |
|----------|--------|-----|
| 1 | V-030 State Machine Enforcement | Controls workflow phase transitions |
| 2 | V-023 Pre-Action Checklists | "Did you write the test first?" |
| 3 | V-057 Quality Gate Enforcement | Block completion without test evidence |
| 4 | V-014 Constitutional AI Self-Critique | Self-check: "Did I follow BDD?" |
| 5 | V-060 Evidence-Based Closure | Require test artifacts before DONE |

#### Use Case: Maintaining Process Compliance Across Long Sessions

| Priority | Vector | Why |
|----------|--------|-----|
| 1 | V-024 Context Reinforcement via Repetition | Combats context rot directly |
| 2 | V-005 UserPromptSubmit Reinsertion | Platform mechanism for rule re-injection |
| 3 | V-016 Structured Imperative Rules | FORBIDDEN/CORRECT patterns resist rot best |
| 4 | V-051 NASA IV&V Independence | Process-level enforcement; not subject to rot |
| 5 | V-062 WTI Rules | Cross-file consistency checks catch drift |

#### Use Case: Ensuring Output Quality (Deliverable Correctness)

| Priority | Vector | Why |
|----------|--------|-----|
| 1 | V-028 Validator Composition | Chain of typed validators on output |
| 2 | V-018 Self-Refine Loop | Iterative improvement passes |
| 3 | V-020 Chain-of-Verification | Generates verification questions |
| 4 | V-022 Schema-Enforced Output | Structural correctness guarantee |
| 5 | V-058 Adversarial Review | External critique catches blind spots |

#### Use Case: Platform-Portable Enforcement

| Priority | Vector | Why |
|----------|--------|-----|
| 1 | V-038 AST Import Boundary Validation | 100% portable, deterministic |
| 2 | V-042 Property-Based Testing | 100% portable, generative |
| 3 | V-014 Constitutional AI Self-Critique | 100% portable, any LLM |
| 4 | V-024 Context Reinforcement via Repetition | 100% portable, any LLM |
| 5 | V-046 MCP Tool Wrapping | ~80% portable, open standard |

---

### Recommended Enforcement Architecture for Jerry

#### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    JERRY ENFORCEMENT STACK                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 1: HARD / BLOCKING (Deterministic)                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ V-001 PreToolUse Blocking (Claude Code only)              │  │
│  │ V-038 AST Import Boundary Validation                      │  │
│  │ V-046 MCP Tool Wrapping                                   │  │
│  │ V-022 Schema-Enforced Output                              │  │
│  │                                                           │  │
│  │ Behavior: BLOCK non-compliant operations                  │  │
│  │ Reliability: HIGH (deterministic)                         │  │
│  │ Bypass Resistance: HIGH                                   │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  TIER 2: SOFT / WARNING (Probabilistic + Guidance)             │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ V-024 Context Reinforcement via Repetition                │  │
│  │ V-014 Constitutional AI Self-Critique                     │  │
│  │ V-010 Hard Constraint Rules (FORBIDDEN/CORRECT)           │  │
│  │ V-030 State Machine Enforcement                           │  │
│  │ V-023 Pre-Action Checklists                               │  │
│  │ V-028 Validator Composition                               │  │
│  │                                                           │  │
│  │ Behavior: WARN and guide; LLM self-corrects               │  │
│  │ Reliability: MEDIUM (probabilistic compliance)            │  │
│  │ Bypass Resistance: MEDIUM                                 │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  TIER 3: ADVISORY (Process + Post-Hoc)                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ V-051 NASA IV&V Independence                              │  │
│  │ V-057 Quality Gate Enforcement                            │  │
│  │ V-058 Adversarial Review                                  │  │
│  │ V-043 Architecture Test Suite                             │  │
│  │ V-044 Pre-commit Hook Validation                          │  │
│  │ V-045 CI Pipeline Enforcement                             │  │
│  │ V-060 Evidence-Based Closure                              │  │
│  │                                                           │  │
│  │ Behavior: VERIFY after the fact; catch what slipped       │  │
│  │ Reliability: HIGH (deterministic post-hoc)                │  │
│  │ Bypass Resistance: HIGH (requires explicit override)      │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  CROSS-CUTTING: Token Budget Management                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ Total enforcement overhead: ~3.5% of context              │  │
│  │ Rules (optimized): ~12,476 tokens (~6.2%)                 │  │
│  │ Per-prompt reinforcement: ~300 tokens                     │  │
│  │ Per-agent overhead: ~450 tokens                           │  │
│  │ Per-deliverable overhead: ~3x base iteration              │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

#### Implementation Priority (Phased Rollout)

**Phase 1: Foundation (Weeks 1-2)**
- Optimize `.claude/rules/` token budget (53% reduction from ~25,700 to ~12,476 tokens)
- Remove `tool-configuration.md` (near-zero enforcement value, ~2,412 tokens wasted)
- Implement FORBIDDEN/CORRECT pattern across all remaining rules
- Add numbered priority prefixes (01-hard-constraints through 09-error-handling)
- Implement V-024 Context Reinforcement via UserPromptSubmit hook

**Phase 2: Structural Enforcement (Weeks 3-4)**
- Move AST validation from test-time to write-time via PreToolUse hook (V-038 + V-001)
- Implement V-039 type hint enforcement and V-040 docstring enforcement in same hook
- Add V-041 one-class-per-file check
- Integrate V-042 property-based testing into existing pytest infrastructure

**Phase 3: Protocol Layer (Weeks 5-6)**
- Implement MCP audit logging server (V-049) -- lowest risk, highest observability
- Add MCP tool wrapping for file write operations (V-046)
- Implement MCP resource provider for dynamic rule injection (V-047)

**Phase 4: Process Integration (Weeks 7-8)**
- Implement V-030 state machine enforcement for workflow phases
- Add V-057 quality gate enforcement with V-060 evidence-based closure
- Integrate V-014 self-critique into agent output validation
- Deploy V-028 validator composition chain for deliverable quality checks

**Phase 5: Advanced (Ongoing)**
- V-058 adversarial review integration into orchestration workflows
- V-051 NASA IV&V independence for critical deliverables
- V-054 FMEA for enforcement mechanism failures
- Continuous monitoring and optimization of token budgets

#### Graceful Degradation Model

The architecture degrades gracefully when platform-specific layers are unavailable:

| Available Layers | Enforcement Level | Coverage |
|-----------------|-------------------|----------|
| All 6 layers (Claude Code) | Maximum | ~95% of violations caught |
| Layers 1-4 + 6 (non-Claude LLM with MCP) | High | ~80% of violations caught |
| Layers 1-3 + 6 (any LLM, no MCP) | Moderate | ~65% of violations caught |
| Layers 1-2 + 6 (minimal LLM support) | Basic | ~45% of violations caught |
| Layer 6 only (CI-only) | Minimal | ~25% of violations caught (post-hoc only) |

---

### Meta-Analysis: Cross-Vector Patterns

#### Pattern 1: Common Failure Modes

Five failure modes recur across vector families:

| Failure Mode | Affected Vectors | Mitigation |
|-------------|------------------|------------|
| **Context Rot** | V-008, V-009, V-010, V-011, V-013, V-016, V-017, V-026 | V-024 Repetition + V-005 UserPromptSubmit |
| **Fail-Open** | V-001, V-002, V-003, V-006 | Multi-layer defense; never rely on single hook |
| **Token Budget Exhaustion** | V-014, V-018, V-020, V-026, V-032 | Token budget management; tiered activation |
| **Bypass via Complexity** | V-030, V-041, V-055 | Simplicity in enforcement rules; regular audit |
| **False Positive Accumulation** | V-028, V-032, V-036, V-038 | Tunable severity levels; waiver process (V-055) |

#### Pattern 2: Complementary Combinations

Certain vectors are more effective when combined:

| Combination | Vectors | Synergy Effect |
|-------------|---------|----------------|
| **Write-Time + Test-Time** | V-038 (AST in hook) + V-043 (arch tests) | Real-time prevention + comprehensive verification |
| **Rules + Reinforcement** | V-010 (hard rules) + V-024 (repetition) | Initial guidance + sustained compliance |
| **Self-Critique + External Review** | V-014 (self-critique) + V-058 (adversarial review) | Internal + external quality perspectives |
| **Blocking + Logging** | V-001 (PreToolUse block) + V-049 (MCP audit) | Prevention + observability |
| **Process + Tool** | V-057 (quality gates) + V-060 (evidence-based closure) | Workflow control + artifact verification |
| **State Machine + Checklist** | V-030 (state machine) + V-023 (checklist) | Phase control + step-level guidance |

#### Pattern 3: Diminishing Returns

The research identifies diminishing returns thresholds:

| Enforcement Level | Vectors Active | Incremental Benefit | Recommendation |
|-------------------|---------------|---------------------|----------------|
| 0 (none) | 0 | -- | Unacceptable |
| 1 (basic rules) | V-008, V-010, V-013 | HIGH (+40% compliance) | Minimum viable |
| 2 (+ reinforcement) | + V-024, V-005 | HIGH (+25% compliance) | Strongly recommended |
| 3 (+ structural) | + V-038, V-043, V-044 | MEDIUM (+15% compliance) | Recommended |
| 4 (+ protocol) | + V-046, V-049 | MEDIUM (+8% compliance) | Good ROI |
| 5 (+ self-critique) | + V-014, V-018, V-028 | LOW (+5% compliance) | Situational |
| 6 (+ full process) | + V-051, V-054, V-058 | LOW (+3% compliance) | Critical deliverables only |

**Key Insight**: Levels 1-3 capture ~80% of the total enforcement benefit. Levels 4-6 provide diminishing but still valuable returns for critical work. Jerry should default to Level 3 and escalate to Level 5-6 for mission-critical deliverables.

#### Pattern 4: Identified Gaps

Despite 62 vectors, the research identified gaps in Jerry's current enforcement:

| Gap | Description | Recommended Vector(s) |
|-----|-------------|----------------------|
| **No runtime rule re-injection** | Rules loaded once, never refreshed | V-024 + V-005 |
| **No self-critique at runtime** | Agent outputs not self-reviewed | V-014 + V-018 |
| **No structured output enforcement** | No schema validation on deliverables | V-022 + V-028 |
| **No protocol-level enforcement** | No MCP integration | V-046, V-047, V-049 |
| **No write-time AST validation** | AST checks only at test-time | V-038 via V-001 |
| **No formal waiver process** | No documented exception handling | V-055 |
| **No enforcement telemetry** | No metrics on enforcement effectiveness | V-049 + custom dashboard |

---

## Appendices

### Appendix A: Full Vector Inventory

| ID | Name | Family | Category | Eff. | Rel. | Port. | Maint. | Source |
|----|------|--------|----------|------|------|-------|--------|--------|
| V-001 | PreToolUse Blocking | Hooks | CC-specific | H | H | L | M | T1 |
| V-002 | PostToolUse Validation | Hooks | CC-specific | M | H | L | M | T1 |
| V-003 | SessionStart Injection | Hooks | CC-specific | M | H | L | L | T1 |
| V-004 | Stop Hook (Subagent) | Hooks | CC-specific | M | H | L | L | T1 |
| V-005 | UserPromptSubmit Reinsertion | Hooks | CC-specific | H | H | L | M | T1 |
| V-006 | Hook Chaining | Hooks | CC-specific | H | H | L | H | T1 |
| V-007 | Stateful Hook Enforcement | Hooks | CC-specific | H | M | L | H | T1 |
| V-008 | CLAUDE.md Root Context | Rules | LLM-portable | M | L | H | L | T3 |
| V-009 | .claude/rules/ Auto-Loaded | Rules | Hybrid | H | M | L | M | T3 |
| V-010 | Hard Constraint Rules | Rules | LLM-portable | H | M | H | L | T3 |
| V-011 | Soft Guidance Rules | Rules | LLM-portable | L | L | H | L | T3 |
| V-012 | AGENTS.md Agent Registry | Rules | LLM-portable | M | L | H | L | T3 |
| V-013 | Numbered Priority Rules | Rules | LLM-portable | M | M | H | L | T3 |
| V-014 | Constitutional AI Self-Critique | Prompt | LLM-portable | H | M | H | M | T4 |
| V-015 | System Message Hierarchy | Prompt | LLM-portable | H | M | H | L | T4 |
| V-016 | Structured Imperative Rules | Prompt | LLM-portable | H | M | H | L | T4 |
| V-017 | XML Tag Demarcation | Prompt | LLM-portable | M | M | H | L | T4 |
| V-018 | Self-Refine Loop | Prompt | LLM-portable | H | M | H | H | T4 |
| V-019 | Reflexion | Prompt | LLM-portable | H | M | H | H | T4 |
| V-020 | Chain-of-Verification | Prompt | LLM-portable | H | M | H | M | T4 |
| V-021 | CRITIC Pattern | Prompt | Hybrid | H | H | M | H | T4 |
| V-022 | Schema-Enforced Output | Prompt | Hybrid | H | H | M | M | T4 |
| V-023 | Pre-Action Checklists | Prompt | LLM-portable | M | M | H | L | T4 |
| V-024 | Context Reinforcement | Prompt | LLM-portable | H | H | H | M | T4 |
| V-025 | Meta-Cognitive Reasoning | Prompt | LLM-portable | M | L | H | L | T4 |
| V-026 | Few-Shot Exemplars | Prompt | LLM-portable | H | M | H | M | T4 |
| V-027 | Confidence Calibration | Prompt | LLM-portable | M | L | H | L | T4 |
| V-028 | Validator Composition | Framework | Fw-specific | H | H | M | M | T2 |
| V-029 | Programmable Rails | Framework | Fw-specific | H | H | L | H | T2 |
| V-030 | State Machine Enforcement | Framework | Fw-specific | H | H | M | M | T2 |
| V-031 | Self-Critique Loop | Framework | LLM-portable | H | M | H | M | T2 |
| V-032 | Multi-Layer Defense | Framework | Fw-specific | H | H | M | H | T2 |
| V-033 | Structured Output Enforcement | Framework | Fw-specific | H | H | M | M | T2 |
| V-034 | Task Guardrails | Framework | Fw-specific | M | M | L | M | T2 |
| V-035 | Content Classification | Framework | Fw-specific | H | H | L | H | T2 |
| V-036 | Prompt Injection Detection | Framework | Fw-specific | H | H | M | H | T2 |
| V-037 | Grammar-Constrained Gen. | Framework | Fw-specific | H | H | L | M | T2 |
| V-038 | AST Import Boundary | Structural | LLM-portable | H | H | H | L | T5 |
| V-039 | AST Type Hint Enforcement | Structural | LLM-portable | H | H | H | L | T5 |
| V-040 | AST Docstring Enforcement | Structural | LLM-portable | M | H | H | L | T5 |
| V-041 | AST One-Class-Per-File | Structural | LLM-portable | M | H | H | L | T5 |
| V-042 | Property-Based Testing | Structural | LLM-portable | H | H | H | M | T5 |
| V-043 | Architecture Test Suite | Structural | LLM-portable | H | H | H | M | T5 |
| V-044 | Pre-commit Hook Validation | Structural | LLM-portable | H | H | H | M | T5 |
| V-045 | CI Pipeline Enforcement | Structural | LLM-portable | H | H | H | M | T5 |
| V-046 | MCP Tool Wrapping | Protocol | Hybrid | H | H | M | M | T5 |
| V-047 | MCP Resource Injection | Protocol | Hybrid | H | M | M | M | T5 |
| V-048 | MCP Enforcement Prompts | Protocol | Hybrid | M | M | M | L | T5 |
| V-049 | MCP Audit Logging | Protocol | Hybrid | M | H | M | L | T5 |
| V-050 | MCP Server Composition | Protocol | Hybrid | H | H | M | H | T5 |
| V-051 | NASA IV&V Independence | Process | LLM-portable | H | H | H | H | T5 |
| V-052 | VCRM | Process | LLM-portable | H | H | H | H | T5 |
| V-053 | NASA File Classification | Process | LLM-portable | H | M | H | M | T5 |
| V-054 | FMEA | Process | LLM-portable | H | H | H | H | T5 |
| V-055 | Formal Waiver Process | Process | LLM-portable | M | H | H | M | T5 |
| V-056 | BDD Red/Green/Refactor | Process | LLM-portable | H | H | H | M | T5 |
| V-057 | Quality Gate Enforcement | Process | LLM-portable | H | H | H | M | T5 |
| V-058 | Adversarial Review | Process | LLM-portable | H | M | H | H | T5 |
| V-059 | Multi-Agent Cross-Pollination | Process | LLM-portable | H | M | H | H | T5 |
| V-060 | Evidence-Based Closure | Process | LLM-portable | H | H | H | M | T5 |
| V-061 | Acceptance Criteria Verification | Process | LLM-portable | M | M | H | L | T5 |
| V-062 | WTI Rules | Process | LLM-portable | H | H | H | M | T5 |

**Legend**: Eff. = Effectiveness, Rel. = Reliability, Port. = Portability, Maint. = Maintenance Cost, H = HIGH, M = MEDIUM, L = LOW, CC = Claude Code, Fw = Framework, T1-T6 = TASK-001 through TASK-006.

### Appendix B: Source Research Cross-Reference

| Research Task | Focus Area | Vectors Contributed | Key Citation Count |
|---------------|-----------|--------------------|--------------------|
| TASK-001 | Claude Code Hooks API | V-001 through V-007 (7) | 6+ (Context7, Anthropic docs) |
| TASK-002 | Industry Guardrail Frameworks | V-028 through V-037 (10) | 9 frameworks surveyed |
| TASK-003 | .claude/rules/ Enforcement | V-008 through V-013 (6) | 10 rule files analyzed |
| TASK-004 | Prompt Engineering Enforcement | V-014 through V-027 (14) | 9 peer-reviewed papers (DOIs) |
| TASK-005 | Alternative Enforcement Mechanisms | V-038 through V-062 (25) | 36 citations |
| TASK-006 | Platform Portability Assessment | Cross-cutting assessment | 62 vectors assessed |
| **Total** | | **62 unique vectors** | **60+ citations** |

---

## References

### Academic Sources (from TASK-004)

1. Bai, Y., et al. (2022). "Constitutional AI: Harmlessness from AI Feedback." *arXiv preprint arXiv:2212.08073*.
2. Liu, N. F., et al. (2023). "Lost in the Middle: How Language Models Use Long Contexts." *arXiv preprint arXiv:2307.03172*. (Context rot foundational research)
3. Madaan, A., et al. (2023). "Self-Refine: Iterative Refinement with Self-Feedback." *NeurIPS 2023*. arXiv:2303.17651.
4. Shinn, N., et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." *NeurIPS 2023*. arXiv:2303.11366.
5. Dhuliawala, S., et al. (2023). "Chain-of-Verification Reduces Hallucination in Large Language Models." *arXiv:2309.11495*.
6. Gou, Z., et al. (2024). "CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing." *ICLR 2024*. arXiv:2305.11738.
7. Wei, J., et al. (2022). "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models." *NeurIPS 2022*. arXiv:2201.11903.
8. Kadavath, S., et al. (2022). "Language Models (Mostly) Know What They Know." *arXiv:2207.05221*.
9. Brown, T. B., et al. (2020). "Language Models are Few-Shot Learners." *NeurIPS 2020*. arXiv:2005.14165.

### Industry Framework Documentation (from TASK-002)

10. Guardrails AI. (2025). *Guardrails AI Documentation*. https://docs.guardrailsai.com/
11. NVIDIA. (2025). *NeMo Guardrails Documentation*. https://docs.nvidia.com/nemo/guardrails/
12. LangChain. (2025). *LangGraph Documentation*. https://langchain-ai.github.io/langgraph/
13. Microsoft. (2025). *Semantic Kernel Documentation*. https://learn.microsoft.com/en-us/semantic-kernel/
14. CrewAI. (2025). *CrewAI Documentation*. https://docs.crewai.com/
15. Meta AI. (2024). *Llama Guard*. https://ai.meta.com/research/publications/llama-guard/
16. Rebuff AI. (2024). *Rebuff Documentation*. https://github.com/protectai/rebuff

### Claude Code and MCP Sources (from TASK-001, TASK-005)

17. Anthropic. (2025). *Claude Code Plugin Documentation*. https://docs.anthropic.com/en/docs/claude-code
18. Anthropic. (2025). *Model Context Protocol Specification*. https://spec.modelcontextprotocol.io/
19. Anthropic. (2025). *MCP TypeScript SDK*. https://github.com/modelcontextprotocol/typescript-sdk
20. Context7. (2026). *Claude Code Hook SDK Examples*. https://context7.com/

### NASA Standards (from TASK-005)

21. NASA. (2020). *NPR 7123.1D: NASA Systems Engineering Processes and Requirements*. NASA.
22. NASA. (2022). *NASA-STD-8739.8: Software Assurance and Software Safety Standard*. NASA.
23. NASA. (2009). *NASA-GB-8719.13: NASA Software Safety Guidebook*. NASA.
24. NASA. (2023). *IV&V Annual Report*. NASA Independent Verification and Validation Facility.
25. Leveson, N. (2012). *Engineering a Safer World: Systems Thinking Applied to Safety*. MIT Press.

### Additional Sources (from TASK-005, TASK-006)

26. Hypothesis. (2025). *Hypothesis: Property-Based Testing for Python*. https://hypothesis.readthedocs.io/
27. Python AST Module. (2025). *ast -- Abstract Syntax Trees*. https://docs.python.org/3/library/ast.html
28. Pre-commit. (2025). *Pre-commit Framework*. https://pre-commit.com/
29. GitHub. (2025). *GitHub Actions Documentation*. https://docs.github.com/en/actions

---

*Synthesis Agent: ps-synthesizer*
*Date: 2026-02-13*
*Source Tasks: TASK-001, TASK-002, TASK-003, TASK-004, TASK-005, TASK-006*
*Parent: EN-401 Deep Research Enforcement Vectors*
*Status: COMPLETE*
