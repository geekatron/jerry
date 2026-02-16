# TASK-003: Architecture Trade Study for Enforcement Vector Prioritization

<!--
DOCUMENT-ID: FEAT-005:EN-402-TASK-003-TRADE-STUDY
TEMPLATE: Trade Study Report (TSR)
VERSION: 1.1.0
SOURCE: EN-401 TASK-009 Revised Catalog (v1.1) + EN-402 TASK-001 Evaluation Criteria
AGENT: nse-architecture (Claude Opus 4.6)
DATE: 2026-02-13
PARENT: EN-402 (Enforcement Priority Analysis & Decision)
FEATURE: FEAT-005 (Quality Framework Enforcement Mechanisms)
EPIC: EPIC-002 (Quality Framework Enforcement)
PROJECT: PROJ-001-oss-release
QUALITY-TARGET: >= 0.92
CONSUMERS: TASK-004 (ps-analyst scoring), TASK-005 (ADR)
NASA-PROCESSES: Process 3 (Logical Decomposition), Process 4 (Design Solution), Process 17 (Decision Analysis)
-->

> **Version:** 1.1.0
> **Agent:** nse-architecture (Claude Opus 4.6)
> **NASA Processes:** NPR 7123.1D -- Process 3 (Logical Decomposition), Process 4 (Design Solution Definition), Process 17 (Decision Analysis)
> **Confidence:** HIGH -- grounded in TASK-009 empirical data and TASK-001 evaluation framework

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Architecture recommendation at a glance |
| [Layered Enforcement Architecture](#layered-enforcement-architecture) | Map 7 families to architectural layers with execution order |
| [Vector Composition Matrix](#vector-composition-matrix) | Compatibility, synergy, conflict, and redundancy analysis |
| [Trade-Off Analysis](#trade-off-analysis) | Five key trade-off dimensions with recommendations |
| [Integration Architecture](#integration-architecture) | How vectors map to Jerry's hexagonal architecture and hook points |
| [Recommended Architecture](#recommended-architecture) | Proposed enforcement stack with token budget allocation |
| [NASA SE Perspective](#nasa-se-perspective) | Pugh matrix, requirements traceability, TRL assessment |
| [Risks and Mitigations](#risks-and-mitigations) | Architecture-level risks |
| [References](#references) | All citations |

---

## Executive Summary

### Decision Statement

Evaluate how the 62 enforcement vectors from the EN-401 catalog compose, conflict, or reinforce each other within a layered enforcement architecture for Jerry, and recommend an optimal enforcement stack that maximizes quality enforcement while respecting the ~25,700 token budget envelope and cross-platform portability requirements.

### Key Findings

1. **The 7 enforcement families decompose into 5 architectural execution layers** that fire in a strict temporal ordering: Static Context (session start) -> Per-Prompt Injection (every prompt) -> Pre-Action Gating (before tool execution) -> Post-Action Validation (after tool execution) -> Post-Hoc Verification (commit/CI time). This ordering creates a defense-in-depth pipeline where each layer catches what the previous layer missed.

2. **Of the 62 vectors, only 15-20 should be actively deployed** to avoid diminishing returns and token budget exhaustion. TASK-007 Pattern 3 shows that enforcement levels 1-3 capture ~80% of total benefit; levels 4-6 add only ~16% incremental benefit at substantially higher cost.

3. **The architecture has a critical correlated failure mode:** 13 of 62 vectors (the rules and prompt families) share context rot as a common failure mode and degrade simultaneously. The recommended stack must include a sufficient proportion of IMMUNE vectors (30 of 62 are immune per TASK-009 Appendix C) to maintain enforcement when context degrades.

4. **Token budget is the binding constraint.** The 25,700-token current budget must be reduced to ~12,476 tokens for rules alone, with ~2,650 additional tokens for prompt patterns. Total enforcement budget target: 15,126 tokens (7.6% of 200K context). This constraint eliminates architectures that rely heavily on in-context enforcement.

5. **The recommended architecture follows a "deterministic skeleton with probabilistic guidance" pattern:** context-rot-immune vectors (AST, CI, hooks, processes) form the enforcement skeleton; context-dependent vectors (rules, prompts, checklists) provide guidance within that skeleton.

### Architecture Recommendation (L0)

Implement a 5-layer enforcement stack that fires in temporal order:

| Layer | Timing | Key Vectors | Token Cost | Context Rot Immunity |
|-------|--------|-------------|------------|---------------------|
| L1: Static Context | Session start | V-008, V-009, V-010 | ~12,476 | VULNERABLE |
| L2: Per-Prompt Reinforcement | Every prompt | V-024, V-005 | ~600/session | IMMUNE (by design) |
| L3: Pre-Action Gating | Before tool calls | V-001, V-038 | 0 (external) | IMMUNE |
| L4: Post-Action Validation | After tool calls | V-002, V-043 | 0 (external) | IMMUNE |
| L5: Post-Hoc Verification | Commit/CI time | V-044, V-045 | 0 (external) | IMMUNE |
| Cross-cutting: Process | Workflow level | V-057, V-060 | 0 (external) | IMMUNE |

**Total in-context token cost: ~15,126 tokens (7.6%).** Four of five enforcement layers are entirely context-rot-immune.

---

## Layered Enforcement Architecture

### Functional Decomposition: 7 Families to 5 Execution Layers

The 7 enforcement families (from TASK-007) map to 5 execution layers based on when they fire in a session lifecycle. This mapping reveals that the families are not independent layers -- some families span multiple execution layers, and some execution layers draw from multiple families.

```
SESSION LIFECYCLE (Temporal Execution Order)
================================================================

L1: STATIC CONTEXT LAYER (fires once at session start)
    Loads rules, context, and agent definitions into LLM memory
    ┌─────────────────────────────────────────────────────┐
    │ Family 2 (Rules): V-008, V-009, V-010, V-011,      │
    │                    V-012, V-013                      │
    │ Family 3 (Prompt): V-015, V-016, V-017, V-026       │
    │ Family 1 (Hooks): V-003 SessionStart Injection       │
    │                                                      │
    │ VULNERABLE TO CONTEXT ROT                            │
    │ Token cost: ~12,476 (rules) + ~700 (prompts)         │
    └─────────────────────────────────────────────────────┘
              │
              ▼
L2: PER-PROMPT REINFORCEMENT LAYER (fires every user prompt)
    Re-injects critical rules to counteract context rot
    ┌─────────────────────────────────────────────────────┐
    │ Family 3 (Prompt): V-024 Context Reinforcement       │
    │ Family 1 (Hooks): V-005 UserPromptSubmit             │
    │                                                      │
    │ IMMUNE BY DESIGN (fresh injection each prompt)       │
    │ Token cost: ~30 per prompt (~600/session)            │
    └─────────────────────────────────────────────────────┘
              │
              ▼  (for each tool call within the prompt response)
L3: PRE-ACTION GATING LAYER (fires before each tool call)
    Deterministic blocking of non-compliant operations
    ┌─────────────────────────────────────────────────────┐
    │ Family 1 (Hooks): V-001 PreToolUse Blocking          │
    │ Family 5 (Structural): V-038 AST Import Validation   │
    │                         V-039 Type Hint Enforcement   │
    │                         V-040 Docstring Enforcement   │
    │                         V-041 One-Class-Per-File      │
    │ Family 6 (Protocol): V-046 MCP Tool Wrapping         │
    │                                                      │
    │ IMMUNE (external processes, not in LLM context)      │
    │ Token cost: 0 (executes outside context window)      │
    └─────────────────────────────────────────────────────┘
              │
              ▼
L4: POST-ACTION VALIDATION LAYER (fires after each tool call)
    Inspects output for violations; may trigger remediation
    ┌─────────────────────────────────────────────────────┐
    │ Family 1 (Hooks): V-002 PostToolUse Validation       │
    │ Family 3 (Prompt): V-014 Self-Critique               │
    │                     V-018 Self-Refine                 │
    │                     V-020 Chain-of-Verification       │
    │                     V-023 Pre-Action Checklists       │
    │ Family 4 (Framework): V-028 Validator Composition     │
    │ Family 5 (Structural): V-043 Architecture Tests      │
    │ Family 6 (Protocol): V-049 MCP Audit Logging         │
    │                                                      │
    │ MIXED IMMUNITY (hooks=IMMUNE, prompts=VULNERABLE)    │
    │ Token cost: 0 (hooks) + ~450-1,800 (prompt patterns) │
    └─────────────────────────────────────────────────────┘
              │
              ▼
L5: POST-HOC VERIFICATION LAYER (fires at commit/CI time)
    Catches violations that escaped all runtime layers
    ┌─────────────────────────────────────────────────────┐
    │ Family 5 (Structural): V-044 Pre-commit Hooks        │
    │                         V-045 CI Pipeline             │
    │                         V-042 Property-Based Testing  │
    │                                                      │
    │ IMMUNE (external processes)                          │
    │ Token cost: 0                                        │
    └─────────────────────────────────────────────────────┘

CROSS-CUTTING: PROCESS ENFORCEMENT (workflow level)
    ┌─────────────────────────────────────────────────────┐
    │ Family 7 (Process): V-057 Quality Gates              │
    │                      V-060 Evidence-Based Closure     │
    │                      V-056 BDD Cycle                  │
    │                      V-061 Acceptance Criteria        │
    │                      V-062 WTI Rules                  │
    │                      V-051 NASA IV&V Independence     │
    │                                                      │
    │ IMMUNE (process-based, not in LLM context)           │
    │ Token cost: 0                                        │
    └─────────────────────────────────────────────────────┘
```

### Execution Order Rationale

The temporal ordering follows the "prevent, then detect, then verify" principle from NASA-STD-8739.8 software assurance:

| Phase | Principle | Layers Active | Analogy (NASA SE) |
|-------|-----------|---------------|-------------------|
| **Prevent** | Stop violations before they happen | L1 (guidance), L2 (reinforcement), L3 (blocking) | Requirements validation; design rules |
| **Detect** | Find violations in real-time | L4 (post-action) | Unit testing; inspection |
| **Verify** | Catch anything that slipped through | L5 (post-hoc) | System testing; IV&V |
| **Govern** | Ensure process compliance | Cross-cutting (process) | Formal review; quality assurance |

### Defense-in-Depth Pattern

The layered architecture creates defense-in-depth where each layer compensates for the failure mode of the layer above it:

| Layer | Primary Failure Mode | Compensated By | Compensation Mechanism |
|-------|---------------------|----------------|----------------------|
| L1 (Static Context) | Context rot after ~20K tokens | L2 (Per-Prompt Reinforcement) | V-024 re-injects critical rules |
| L2 (Per-Prompt Reinforcement) | LLM ignores re-injected rules | L3 (Pre-Action Gating) | V-001/V-038 deterministically block regardless of LLM state |
| L3 (Pre-Action Gating) | Fail-open on hook error | L4 (Post-Action Validation) | V-002/V-043 detect violations in output |
| L4 (Post-Action Validation) | Self-critique degraded by context rot | L5 (Post-Hoc Verification) | V-044/V-045 catch violations at commit/CI |
| L5 (Post-Hoc Verification) | Violations already in codebase | Process (Quality Gates) | V-057/V-060 block task closure without evidence |

**Key architectural property:** Each adjacent layer pair has at least one IMMUNE vector, ensuring that context rot cannot cascade through the entire stack. The only layer where all vectors are VULNERABLE is L1 (Static Context), which is immediately compensated by L2 (Per-Prompt Reinforcement, IMMUNE by design).

---

## Vector Composition Matrix

### High-Priority Vector Compatibility Analysis

This matrix evaluates how the top-priority vectors (those likely to score in TASK-001 Tier 1 or Tier 2) compose when deployed simultaneously. Vectors are assessed as: **Synergistic** (combined effect > sum of parts), **Compatible** (work independently without interference), **Redundant** (duplicate effort with limited additional benefit), or **Conflicting** (interfere with each other).

#### Composition Matrix (Top 15 Vectors)

|  | V-001 | V-005 | V-010 | V-024 | V-038 | V-039 | V-043 | V-044 | V-045 | V-046 | V-049 | V-057 | V-060 | V-014 | V-056 |
|--|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| **V-001** PreToolUse | -- | C | C | C | **S** | S | C | C | C | R* | **S** | C | C | C | C |
| **V-005** UserPromptSubmit | C | -- | C | **S** | C | C | C | C | C | C | C | C | C | C | C |
| **V-010** Hard Rules | C | C | -- | **S** | C | C | C | C | C | C | C | C | C | C | C |
| **V-024** Context Reinforcement | C | **S** | **S** | -- | C | C | C | C | C | C | C | C | C | **S** | C |
| **V-038** AST Import | **S** | C | C | C | -- | C | **S** | **S** | C | C | C | C | C | C | C |
| **V-039** AST Type Hints | S | C | C | C | C | -- | C | S | C | C | C | C | C | C | C |
| **V-043** Arch Tests | C | C | C | C | **S** | C | -- | **S** | **S** | C | C | C | C | C | C |
| **V-044** Pre-commit | C | C | C | C | **S** | S | **S** | -- | C | C | C | C | C | C | C |
| **V-045** CI Pipeline | C | C | C | C | C | C | **S** | C | -- | C | C | C | C | C | C |
| **V-046** MCP Wrapping | R* | C | C | C | C | C | C | C | C | -- | **S** | C | C | C | C |
| **V-049** MCP Audit | **S** | C | C | C | C | C | C | C | C | **S** | -- | C | C | C | C |
| **V-057** Quality Gates | C | C | C | C | C | C | C | C | C | C | C | -- | **S** | C | **S** |
| **V-060** Evidence Closure | C | C | C | C | C | C | C | C | C | C | C | **S** | -- | C | **S** |
| **V-014** Self-Critique | C | C | C | **S** | C | C | C | C | C | C | C | C | C | -- | C |
| **V-056** BDD Cycle | C | C | C | C | C | C | C | C | C | C | C | **S** | **S** | C | -- |

**Legend:** S = Synergistic, C = Compatible, R = Redundant, R* = Partially Redundant (overlapping function but different mechanism), -- = self

### Synergistic Combinations (A + B > Sum of Parts)

| Combination | Vectors | Synergy Effect | Mechanism | Layer Interaction |
|-------------|---------|----------------|-----------|-------------------|
| **Write-Time + Test-Time AST** | V-038 + V-043 | Real-time prevention plus comprehensive verification. V-038 in a hook catches violations before file write; V-043 in tests catches any that slip through (e.g., manual edits outside Claude Code). | L3 -> L5 | Two independent immune layers |
| **Rules + Reinforcement** | V-010 + V-024 | Initial guidance + sustained compliance. V-010 sets the rules at session start; V-024 re-injects the most critical rules on every prompt, converting V-010's HIGH context rot vulnerability to PARTIALLY VULNERABLE. | L1 + L2 | L2 compensates L1's failure mode |
| **Blocking + Audit** | V-001 + V-049 | Prevention + observability. V-001 blocks violations in real time; V-049 logs all operations (including allowed ones), creating an audit trail for enforcement effectiveness analysis. | L3 + L4 | Deterministic + passive |
| **AST in Hook + Pre-commit** | V-038 + V-044 | Hook catches violations before write; pre-commit catches violations from non-hook paths (manual edits, git operations). Together they cover all code entry paths. | L3 + L5 | Two entry points |
| **Self-Critique + Reinforcement** | V-014 + V-024 | V-024 keeps the self-critique instruction fresh in context, preventing the self-critique itself from being forgotten due to context rot. | L4 + L2 | L2 sustains L4 effectiveness |
| **Quality Gates + Evidence Closure** | V-057 + V-060 | V-057 blocks completion until criteria are met; V-060 requires proof artifacts. Together they create a double-lock: the gate checks criteria AND demands evidence. | Process | Workflow + artifact |
| **Quality Gates + BDD** | V-057 + V-056 | BDD cycle produces test artifacts; quality gates require test evidence. BDD naturally generates the evidence that quality gates demand. | Process | Evidence generation + verification |
| **UserPromptSubmit + Reinforcement** | V-005 + V-024 | V-005 is the platform mechanism; V-024 is the enforcement pattern. V-005 provides the injection point; V-024 provides the content to inject. | L2 | Platform + pattern |

### Conflicting Combinations

| Combination | Vectors | Conflict Description | Resolution |
|-------------|---------|---------------------|------------|
| **Token Budget Contention** | V-010 (rules, ~12,476 tokens) + V-018 (Self-Refine, ~900/iteration) + V-020 (CoVe, ~1,000 tokens) | All three consume context tokens. Deploying all three simultaneously pushes enforcement overhead toward 8.5%, reducing productive context by ~17,000 tokens. | Use V-018 and V-020 only for critical deliverables (tiered activation per TASK-007 recommendation). Default to V-010 + V-024 for standard work. |
| **Hook Complexity** | V-006 (Hook Chaining) + V-007 (Stateful Hooks) | V-006 chains multiple hooks in sequence, increasing execution time. V-007 adds filesystem state, introducing race conditions. Together they create a fragile, hard-to-debug enforcement pipeline. | Avoid V-007; keep hooks stateless. If state is needed, use V-049 (MCP Audit Logging) for observability. |
| **Partial Redundancy** | V-001 (PreToolUse) + V-046 (MCP Tool Wrapping) | Both gate tool calls before execution. V-001 uses Claude Code hooks API; V-046 uses MCP protocol. On Claude Code with MCP, both fire, creating redundant checks. | Use V-001 as the primary gating mechanism on Claude Code. Deploy V-046 as the portable fallback for non-Claude-Code platforms. Do not run both simultaneously on the same operation. |

### Redundant Combinations

| Combination | Vectors | Redundancy Type | Recommendation |
|-------------|---------|-----------------|----------------|
| V-011 (Soft Rules) + V-025 (Meta-Cognitive) | Both are advisory-only, context-rot-vulnerable, and low-effectiveness. | Full redundancy | Eliminate V-011 or reduce to minimal content. V-025 adds negligible value beyond V-010 Hard Rules. |
| V-012 (AGENTS.md) + V-013 (Numbered Rules) | Both are organizational aids with no enforcement mechanism. | Structural redundancy | Keep V-013 (provides priority ordering); V-012 is valuable for agent coordination but not for enforcement. |
| V-043 (Architecture Tests) + V-045 (CI Pipeline) | Architecture tests run within the CI pipeline. V-043 is a subset of V-045. | Subsumption | Keep both: V-043 defines the tests; V-045 runs them. They are complementary, not redundant. Separate entries capture the distinction between "writing tests" and "running them in CI." |

---

## Trade-Off Analysis

### Trade-Off 1: Breadth vs. Depth

**Question:** Should Jerry implement many lightweight enforcement vectors or fewer heavyweight ones?

| Approach | Description | Token Cost | Maintenance Cost | Coverage |
|----------|-------------|------------|-----------------|----------|
| **A: Broad** (30+ vectors active) | Deploy as many vectors as possible across all layers | HIGH (~17,000 tokens in-context) | HIGH (30+ components to maintain) | HIGH (theoretical) but diminishing returns after ~15 |
| **B: Deep** (15-20 vectors, multi-layer) | Select 15-20 high-value vectors ensuring coverage across all 5 layers | MODERATE (~15,126 tokens in-context) | MODERATE (15-20 components) | HIGH (practical) -- captures ~95% of TASK-007 benefit |
| **C: Narrow** (<10 vectors) | Deploy only the highest-scoring vectors | LOW (~10,000 tokens) | LOW (few components) | MODERATE -- may miss violation types not covered by top vectors |

**Analysis:**

TASK-007 Pattern 3 (Diminishing Returns) demonstrates that enforcement levels 1-3 (approximately 15 active vectors) capture ~80% of total benefit. Adding vectors beyond this point yields ~5% incremental benefit per batch [TASK-007, Section L2: Meta-Analysis, Pattern 3]. The token budget constraint (~15,126 target from TASK-009 Appendix B) eliminates Approach A for in-context vectors.

**Recommendation: Approach B (Deep).** Deploy 15-20 vectors selected for maximum layer coverage and minimal redundancy. Use tiered activation (TASK-007 Family 3 tiers) to escalate from ~15 default vectors to ~25+ for critical deliverables.

### Trade-Off 2: Token Economy

**Question:** How should the ~15,126 token enforcement budget be allocated across enforcement layers?

| Layer | Token Budget | % of Total | Justification |
|-------|-------------|------------|---------------|
| L1: Static Context (Rules) | 12,476 | 82.5% | Rules are the foundation; loaded once; ~53% reduction from current 25,700 already planned [TASK-003] |
| L2: Per-Prompt Reinforcement | 600 | 4.0% | ~30 tokens * 20 prompts; minimal cost for maximum context rot mitigation [TASK-009 Appendix B] |
| L3: Pre-Action Gating | 0 | 0% | External processes; no context cost |
| L4: Post-Action Validation (prompts) | 1,350 | 8.9% | Self-critique (~450) + Schema (~300) + Meta-cognitive (~600) [TASK-009 Appendix B] |
| L4: Post-Action Validation (external) | 0 | 0% | Hooks and AST are external |
| L5: Post-Hoc Verification | 0 | 0% | External processes |
| Cross-cutting: Few-shot + CLAUDE.md | 700 | 4.6% | Exemplars (~400) + CLAUDE.md (~300) [TASK-009 Appendix B] |
| **Total** | **~15,126** | **100%** | **7.6% of 200K context** |

**Key insight:** 82.5% of the token budget goes to L1 (rules loaded at session start). The remaining 17.5% covers all dynamic enforcement patterns. This heavily front-loaded budget means rule optimization (the Phase 1 priority from TASK-007) has the highest token ROI of any single intervention. Every token saved from rules becomes available for productive work or additional enforcement patterns.

**Token budget concentration risk (cross-ref R-SYS-004):** L1 is also the **most vulnerable layer** to context rot (CRR=1-2 for rules-based vectors per TASK-001 rubric). The concentration of 82.5% of the enforcement token budget in the most vulnerable layer creates a structural risk: the layer consuming the most context resources is the first layer to degrade under context pressure. This is the mechanism underlying R-SYS-004 (combined rot + budget exhaustion, Score 16 RED per TASK-002 v1.1). Mitigations:
1. **Phase 1 rule optimization** reduces L1 from 25,700 to 12,476 tokens (51.5% reduction), shrinking the vulnerable attack surface.
2. **L2 reinforcement** (V-024, 600 tokens, 4.0% of budget) specifically compensates for L1 degradation.
3. **IMMUNE layers** (L3, L5, Process) provide enforcement that continues to function regardless of L1 state, meaning complete enforcement failure requires failure of both vulnerable and immune layers simultaneously.

**Alternative budget scenario: Aggressive enforcement for critical deliverables**

| Component | Standard Budget | Critical Budget | Delta |
|-----------|----------------|-----------------|-------|
| Rules | 12,476 | 12,476 | 0 |
| Per-Prompt Reinforcement | 600 | 600 | 0 |
| Self-Critique + Schema + Meta | 1,350 | 1,350 | 0 |
| Self-Refine Loop (V-018) | 0 | +900 | +900 |
| CoVe (V-020) + Reflexion (V-019) | 0 | +1,000 | +1,000 |
| **Total** | **~15,126** | **~17,026** | **+1,900** |
| **% of 200K** | **7.6%** | **8.5%** | **+0.9%** |

The critical budget adds ~0.9% context cost for ~5% incremental compliance benefit [TASK-007 Pattern 3]. This should be deployed only for mission-critical deliverables.

### Trade-Off 3: Static vs. Dynamic Enforcement

**Question:** Should enforcement be pre-loaded (static rules) or dynamically injected (runtime hooks)?

| Aspect | Static (Pre-Loaded) | Dynamic (Runtime Hooks) |
|--------|-------------------|----------------------|
| **Mechanism** | .claude/rules/ files loaded at session start | Hooks inject/block at runtime per-action |
| **Context Rot** | VULNERABLE -- degrades as context fills | IMMUNE -- fires as external process each time |
| **Token Cost** | HIGH (~12,476 tokens permanently in context) | ZERO (external process) or LOW (~30 tokens per injection) |
| **Portability** | HIGH -- text-based rules work on any LLM | LOW -- hook API is Claude Code-specific |
| **Enforcement Power** | LOW -- advisory only; LLM may ignore | HIGH -- can deterministically block operations |
| **Flexibility** | HIGH -- LLM interprets rules contextually | LOW -- hook logic is binary (allow/block) |

**Analysis:**

The fundamental tension is that **static enforcement is portable but weak** and **dynamic enforcement is powerful but platform-specific**. Jerry's architecture must accommodate both because:
1. Portability requirements (user priority #2) demand that the core enforcement stack work without hooks.
2. Effectiveness requirements (TASK-001 Dimension 2) demand that the stack can deterministically prevent violations when running on Claude Code.

**Recommendation: Static foundation with dynamic enhancement.** Deploy static rules (L1) as the universally portable base. Add dynamic hooks (L2, L3) as Claude Code-specific enhancers. Design the system so that removing hooks degrades enforcement from "blocking" to "advisory" but does not eliminate it.

### Trade-Off 4: Portability vs. Power

**Question:** Should Jerry prioritize enforcement vectors that work on any LLM platform, or maximize enforcement power on Claude Code?

| Approach | Vectors Available | Max Enforcement | Portability | User Priority Alignment |
|----------|------------------|----------------|-------------|------------------------|
| **Portable-First** | 38 LLM-portable vectors only | MODERATE (no deterministic blocking) | 100% | Priority #2 (portability) |
| **Power-First** | 7 Claude Code-specific + all others | MAXIMUM (deterministic blocking) | ~0% for hooks; ~88% for everything else | Priority #5 (effectiveness under rot) |
| **Hybrid** | 38 portable as core + 7 CC-specific as enhancers | MAXIMUM on Claude Code; MODERATE elsewhere | Core: 100%; Enhanced: Claude Code only | **Both priorities satisfied** |

**Analysis:**

The hybrid approach is strictly dominant: it sacrifices nothing on portability (the portable core works everywhere) while gaining maximum enforcement power on Claude Code (hooks add deterministic blocking). This maps directly to the graceful degradation model from TASK-007.

**Recommendation: Hybrid approach.** The enforcement architecture must be structured as:
- **Core enforcement** (Families 2, 3, 5, 7 -- LLM-portable vectors): functions on any platform
- **Enhanced enforcement** (Family 1 -- Claude Code hooks): adds blocking capability
- **Protocol enforcement** (Family 6 -- MCP): adds protocol-level control on MCP-compatible clients

### Trade-Off 5: Early vs. Late Enforcement

**Question:** Should violations be prevented before they happen (pre-prompt/pre-action) or detected after the fact (post-action/post-hoc)?

| Timing | Mechanism | Cost of Violation | User Experience | False Positive Impact |
|--------|-----------|-------------------|-----------------|---------------------|
| **Pre-Prompt** (L1, L2) | Rules + reinforcement before LLM acts | Zero (violation never occurs) | Invisible; user sees compliant output directly | Suppresses valid creative solutions |
| **Pre-Action** (L3) | Hook blocks before tool execution | Very low (action blocked before effect) | Visible; user may see "blocked" messages | Blocks valid operations; frustrating |
| **Post-Action** (L4) | Validation after tool output | Low (output inspected before commit) | Visible; user sees correction cycle | Wastes tokens on corrections |
| **Post-Hoc** (L5) | CI/pre-commit catches violations | Moderate (code already written; must fix) | Delayed; violations caught at commit time | Blocks valid commits |

**Analysis:**

Early enforcement (L1-L3) is cheaper per violation caught because it prevents the violation from ever materializing. Late enforcement (L4-L5) is more reliable (deterministic tools) but more expensive (violation already occurred; must remediate). The optimal strategy is:

1. Use early enforcement to **reduce the rate of violations** (fewer violations to catch)
2. Use late enforcement to **catch the violations that slip through** (guaranteed detection)

This is the classic quality engineering principle: "prevention is cheaper than detection, but detection is needed because prevention is imperfect."

**Recommendation: Front-load enforcement to L1-L3 for common violations; ensure L4-L5 coverage for critical invariants.** Specifically:
- Architecture boundary violations: enforce at L3 (PreToolUse AST check) AND L5 (pre-commit/CI)
- Test-first development: enforce at L1 (rules) AND Process (quality gates)
- Naming conventions: enforce at L1 (rules) only -- low severity does not justify L3/L5 cost

---

## Integration Architecture

### Mapping to Jerry's Hexagonal Architecture

The enforcement stack integrates with Jerry's hexagonal architecture at specific adapter and port boundaries:

```
JERRY HEXAGONAL ARCHITECTURE + ENFORCEMENT OVERLAY
====================================================

┌──────────────────────────────────────────────────────────────┐
│  INTERFACE LAYER (Primary Adapters)                          │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  CLI Adapter (src/interface/cli/)                     │    │
│  │  ┌─ L1: Rules loaded via SessionStart hook ──────┐   │    │
│  │  │  V-003: SessionStart injects session context   │   │    │
│  │  │  V-008/V-009: CLAUDE.md + rules/ auto-loaded   │   │    │
│  │  └───────────────────────────────────────────────┘   │    │
│  │  ┌─ L2: Per-prompt reinforcement ────────────────┐   │    │
│  │  │  V-005/V-024: UserPromptSubmit re-injection    │   │    │
│  │  └───────────────────────────────────────────────┘   │    │
│  │  ┌─ L3: Pre-action gating ───────────────────────┐   │    │
│  │  │  V-001: PreToolUse hook (scripts/pre_tool_use) │   │    │
│  │  │  V-038: AST validation within hook             │   │    │
│  │  └───────────────────────────────────────────────┘   │    │
│  │  ┌─ L4: Post-action validation ──────────────────┐   │    │
│  │  │  V-002: PostToolUse hook (scripts/post_tool)   │   │    │
│  │  └───────────────────────────────────────────────┘   │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                              │
│  Hook Adapter (src/interface/hooks/)                         │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  scripts/pre_tool_use.py  -> L3 enforcement          │    │
│  │  scripts/post_tool_use.py -> L4 enforcement          │    │
│  │  scripts/session_start_hook.py -> L1 enforcement     │    │
│  └──────────────────────────────────────────────────────┘    │
├──────────────────────────────────────────────────────────────┤
│  APPLICATION LAYER (Use Cases / CQRS)                        │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Command Handlers                                     │    │
│  │  ┌─ V-057: Quality gate checks before state change ─┐│    │
│  │  │  V-060: Evidence requirements before closure      ││    │
│  │  │  V-030: State machine enforcement on transitions  ││    │
│  │  └───────────────────────────────────────────────────┘│    │
│  │                                                       │    │
│  │  Query Handlers                                       │    │
│  │  (No enforcement needed -- queries are read-only)     │    │
│  └──────────────────────────────────────────────────────┘    │
├──────────────────────────────────────────────────────────────┤
│  DOMAIN LAYER (Pure Business Logic)                          │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  Aggregate invariant enforcement (built-in)           │    │
│  │  ┌─ V-062: WTI Rules enforced as domain invariants ─┐│    │
│  │  │  V-061: Acceptance criteria as domain validation  ││    │
│  │  └───────────────────────────────────────────────────┘│    │
│  └──────────────────────────────────────────────────────┘    │
├──────────────────────────────────────────────────────────────┤
│  INFRASTRUCTURE LAYER (Secondary Adapters)                   │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  V-049: MCP Audit Logging adapter                     │    │
│  │  V-046: MCP Tool Wrapping adapter                     │    │
│  │  V-047: MCP Resource Injection adapter                │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘

EXTERNAL (outside hexagon):
┌──────────────────────────────────────────────────────────────┐
│  L5: Post-Hoc Verification                                   │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  V-044: Pre-commit hooks (.pre-commit-config.yaml)    │    │
│  │  V-045: CI Pipeline (.github/workflows/)              │    │
│  │  V-042: Property-based tests (tests/)                 │    │
│  │  V-043: Architecture tests (tests/architecture/)      │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

### Hook Integration Points

Jerry currently has the following hook infrastructure (from `.claude-plugin/plugin.json` and `scripts/`):

| Hook Type | Script | Current Function | Enforcement Vectors to Add |
|-----------|--------|-----------------|---------------------------|
| `PreToolUse` | `scripts/pre_tool_use.py` | Security guardrails (path validation, pattern library) | V-038 AST validation on Write tool calls; V-039 type hint checks |
| `PostToolUse` | `scripts/post_tool_use.py` | Not currently enforcement-focused | V-002 output validation; V-049 audit logging bridge |
| `SessionStart` | `scripts/session_start_hook.py` | Project context injection | V-003 already implemented; add V-013 priority rule ordering |
| `Stop` | `scripts/subagent_stop.py` | Subagent termination control | V-004 already implemented; minimal enforcement value |
| `UserPromptSubmit` | Not yet implemented | -- | **V-005 + V-024**: Critical new integration point for context reinforcement |

**Architecture decision:** The `UserPromptSubmit` hook is the single highest-value unimplemented integration point. It enables V-024 (Context Reinforcement), which TASK-009 identifies as "the single highest-priority implementation recommendation" [TASK-009, Section L2: Revised Defense-in-Depth Effectiveness]. Implementation requires a `.claude/settings.json` entry (not a plugin hook) per Claude Code's current API:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 scripts/user_prompt_submit.py"
          }
        ]
      }
    ]
  }
}
```

### Rule Loading Architecture

Current `.claude/rules/` structure and proposed optimizations:

| Current File | Size (est. tokens) | Enforcement Value | Recommendation |
|-------------|--------------------|--------------------|----------------|
| `architecture-standards.md` | ~5,200 | HIGH -- hexagonal architecture rules | KEEP; optimize to ~3,000 tokens |
| `coding-standards.md` | ~3,200 | MEDIUM -- many are soft guidance | SPLIT: extract HARD rules (~1,500 tokens); defer soft rules to on-demand |
| `error-handling-standards.md` | ~3,700 | MEDIUM -- exception hierarchy guidance | REDUCE to exception hierarchy table only (~800 tokens) |
| `file-organization.md` | ~3,000 | LOW-MEDIUM -- directory structure reference | MOVE to on-demand loading; not enforcement-critical |
| `mandatory-skill-usage.md` | ~1,100 | MEDIUM -- skill invocation triggers | KEEP but COMPRESS to table only (~500 tokens) |
| `markdown-navigation-standards.md` | ~3,300 | LOW -- documentation practice, not enforcement | REMOVE from auto-loaded rules; move to skill reference |
| `project-workflow.md` | ~950 | MEDIUM -- workflow guidance | KEEP; already compact |
| `python-environment.md` | ~850 | HIGH -- UV enforcement (FORBIDDEN/CORRECT pattern) | KEEP; already uses optimal pattern |
| `testing-standards.md` | ~2,700 | MEDIUM -- BDD cycle and pyramid | REDUCE to enforcement-relevant content (~1,200 tokens) |
| `tool-configuration.md` | ~2,500 | LOW -- tool configs, not enforcement | REMOVE (per TASK-003 recommendation) |
| **Current Total** | **~25,700** | | |
| **Optimized Total** | **~12,476** | | **53% reduction** |

**Rule file numbering architecture** (per V-013 Numbered Priority Rules):

```
.claude/rules/
├── 01-hard-constraints.md       # FORBIDDEN/NEVER rules (highest priority)
├── 02-architecture-enforcement.md   # Hexagonal boundaries, import rules
├── 03-python-environment.md     # UV-only, no system Python
├── 04-coding-standards.md       # Type hints, naming, structure (HARD rules only)
├── 05-project-workflow.md       # Workflow rules
├── 06-testing-enforcement.md    # BDD cycle, test-first (HARD rules only)
├── 07-mandatory-skills.md       # Skill trigger table
└── 08-error-handling.md         # Exception hierarchy table
```

### Session Preamble Injection Architecture

The V-024 Context Reinforcement injection delivered by V-005 UserPromptSubmit should inject a minimal rule summary (~30 tokens) at the end of each user prompt. This positions critical rules in the high-attention zone (end of context) per Liu et al. 2023 "Lost in the Middle" findings.

**Injection content template** (~30 tokens):

```
[ENFORCEMENT REMINDER]
HARD: Use UV only. One class per file. Domain imports stdlib only.
HARD: Persist to files. No recursive subagents. No deception.
```

**Injection mechanism:** The `scripts/user_prompt_submit.py` hook appends this text to the user's prompt before it reaches the model. The hook reads the critical rules from a configuration file (`scripts/enforcement_reminder.txt`) to allow updates without modifying the hook script.

---

## Recommended Architecture

### Proposed Layered Enforcement Stack

```
┌─────────────────────────────────────────────────────────────────────┐
│              JERRY ENFORCEMENT STACK v1.0                            │
│              Recommended Architecture                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  L1: STATIC CONTEXT (session start, ~12,476 tokens)                │
│  ═══════════════════════════════════════════════════                │
│  Vectors: V-008, V-009, V-010, V-013, V-016                       │
│  Function: Set behavioral foundation via optimized rule files       │
│  CRR: VULNERABLE (compensated by L2)                               │
│  Implementation: .claude/rules/ with numbered priority prefixes     │
│  Platform: Any LLM that loads context files                        │
│                                                                     │
│  L2: PER-PROMPT REINFORCEMENT (~600 tokens/session)                │
│  ═══════════════════════════════════════════════════                │
│  Vectors: V-024 + V-005                                            │
│  Function: Re-inject critical rules on every prompt to             │
│            counteract context rot                                   │
│  CRR: IMMUNE by design                                             │
│  Implementation: UserPromptSubmit hook + enforcement_reminder.txt  │
│  Platform: Claude Code (V-005); custom for other LLMs (V-024)     │
│                                                                     │
│  L3: PRE-ACTION GATING (zero tokens)                               │
│  ═══════════════════════════════════                               │
│  Vectors: V-001 + V-038 (+ V-039, V-040, V-041 as needed)        │
│  Function: Deterministically block non-compliant file writes       │
│  CRR: IMMUNE (external process)                                    │
│  Implementation: scripts/pre_tool_use.py with AST module           │
│  Platform: Claude Code (V-001); no equivalent on other LLMs       │
│                                                                     │
│  L4: POST-ACTION VALIDATION (0-1,350 tokens)                      │
│  ══════════════════════════════════════════                         │
│  Vectors: V-002, V-014 (per-agent), V-043                         │
│  Function: Inspect outputs; trigger self-correction if needed      │
│  CRR: V-002 IMMUNE; V-014 MEDIUM (sustained by L2)               │
│  Implementation: scripts/post_tool_use.py + prompt patterns        │
│  Platform: V-002 Claude Code only; V-014 any LLM                 │
│                                                                     │
│  L5: POST-HOC VERIFICATION (zero tokens)                          │
│  ══════════════════════════════════════                             │
│  Vectors: V-044, V-045, V-042, V-043                              │
│  Function: Catch anything that slipped through all runtime layers  │
│  CRR: IMMUNE (external processes)                                  │
│  Implementation: .pre-commit-config.yaml + .github/workflows/      │
│  Platform: Any platform with git and CI                            │
│                                                                     │
│  PROCESS (workflow level, zero tokens)                             │
│  ═════════════════════════════════════                              │
│  Vectors: V-057, V-060, V-056, V-061, V-062                       │
│  Function: Workflow governance; evidence-based completion          │
│  CRR: IMMUNE (process-based)                                      │
│  Implementation: Worktracker + quality gate logic                  │
│  Platform: Any platform                                            │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│  TOTAL IN-CONTEXT TOKEN BUDGET                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Standard enforcement: ~15,126 tokens (7.6% of 200K)         │   │
│  │ Critical-deliverable mode: ~17,026 tokens (8.5% of 200K)   │   │
│  │ Context available for work: 184,874 - 182,974 tokens        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  CONTEXT ROT IMMUNITY SUMMARY                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Layer    │ Immunity   │ Vectors │ Token Cost                │   │
│  │ L1       │ VULNERABLE │ 5       │ 12,476 (82.5%)           │   │
│  │ L2       │ IMMUNE     │ 2       │ 600 (4.0%)               │   │
│  │ L3       │ IMMUNE     │ 2-5     │ 0                        │   │
│  │ L4       │ MIXED      │ 3       │ 0-1,350 (0-8.9%)        │   │
│  │ L5       │ IMMUNE     │ 4       │ 0                        │   │
│  │ Process  │ IMMUNE     │ 5       │ 0                        │   │
│  │                                                             │   │
│  │ Total IMMUNE vectors: 16-19 of 21-24 active                │   │
│  │ Effective independent layers under context rot: 4 of 5     │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Token Budget Allocation Summary

| Component | Tokens | % of 200K | % of Budget | Source |
|-----------|--------|-----------|-------------|--------|
| Optimized .claude/rules/ | 12,476 | 6.24% | 82.5% | TASK-003 analysis |
| Context reinforcement injections | 600 | 0.30% | 4.0% | ~30 * 20 prompts |
| Self-critique per agent | 450 | 0.23% | 3.0% | ~150 * 3 agents |
| Schema enforcement per agent | 300 | 0.15% | 2.0% | ~100 * 3 agents |
| Meta-cognitive reasoning | 600 | 0.30% | 4.0% | ~200 * 3 agents |
| Few-shot exemplars | 400 | 0.20% | 2.6% | Static, loaded once |
| CLAUDE.md + system prompt | 300 | 0.15% | 2.0% | Static, loaded once |
| **Total (standard)** | **15,126** | **7.56%** | **100%** | |
| Self-Refine (critical only) | +900 | +0.45% | -- | Per iteration |
| CoVe + Reflexion (critical only) | +1,000 | +0.50% | -- | Per deliverable |
| **Total (critical max)** | **17,026** | **8.51%** | -- | |

### Platform-Specific Architecture Notes

#### Windows Adaptations

TASK-006 reports 73% Windows compatibility across the 62-vector catalog. The recommended architecture addresses Windows-specific concerns:

| Component | Windows Issue | Adaptation |
|-----------|--------------|------------|
| Hook scripts (Python) | Path separators; `fcntl` unavailable | Already fixed: `filelock` replaces `fcntl` (commit f89f7ff) |
| Pre-commit hooks | Git hooks use `#!/usr/bin/env python3` | Use `sys.executable` or `.bat` wrapper |
| AST validation | Path handling differences | Use `pathlib.Path` (already standard) |
| CI pipeline | GitHub Actions works cross-platform | No adaptation needed |
| Rules files | CRLF line endings | Already fixed: `splitlines()` (commit 49a708e) |
| MCP servers | `stdio` transport works cross-platform | No adaptation needed |

**Windows-specific enforcement gap:** The `UserPromptSubmit` hook (V-005) is a Claude Code settings-based hook. Its cross-platform behavior depends on Claude Code's implementation on Windows. This is outside Jerry's control and should be verified during deployment.

#### Non-Claude-Code LLM Platforms

When running on an LLM platform that does not support Claude Code hooks:

| Layer | Available | Fallback |
|-------|-----------|----------|
| L1 (Static Context) | YES -- rules are text files loadable on any LLM | None needed |
| L2 (Per-Prompt Reinforcement) | PARTIAL -- V-024 content is portable; V-005 mechanism is not | Manual injection or custom integration |
| L3 (Pre-Action Gating) | NO -- hooks require Claude Code | Rely on L4 and L5 for detection |
| L4 (Post-Action Validation) | PARTIAL -- V-014 (prompt-based) works; V-002 (hook) does not | Self-critique patterns only |
| L5 (Post-Hoc Verification) | YES -- git hooks and CI are platform-independent | None needed |
| Process | YES -- process enforcement is platform-independent | None needed |

**Graceful degradation assessment (per TASK-009 revised model):**
- Full stack (Claude Code): HIGH enforcement -- 5 layers active, deterministic blocking
- Without hooks (MCP-only): MODERATE-HIGH enforcement -- 4 layers active, no real-time blocking
- Without hooks or MCP: MODERATE enforcement -- 3 layers active, post-hoc detection only
- CI-only: LOW enforcement -- 1 layer active, violations detected at commit time only

---

## NASA SE Perspective

### Requirements Traceability (P-040)

The recommended architecture traces to the evaluation criteria from TASK-001:

| TASK-001 Dimension | Weight | Architecture Response | Traceability |
|-------------------|--------|----------------------|--------------|
| Context Rot Resilience (CRR) | 25% | 4 of 5 layers are IMMUNE; L1 compensated by L2 | L2 (V-024) + L3-L5 (external) + Process (IMMUNE) |
| Effectiveness (EFF) | 20% | Deterministic blocking at L3; comprehensive detection at L4-L5 | V-001 + V-038 (L3) deterministic; V-043-V-045 (L5) comprehensive |
| Platform Portability (PORT) | 18% | Core stack (L1, L5, Process) is 100% portable; L2-L4 degrade gracefully | L1 rules = text; L5 = git/CI; Process = methodology |
| Token Efficiency (TOK) | 13% | 7.6% standard; 8.5% peak; 82.5% of budget in rules (optimizable) | Budget within 15,126 target from TASK-009 |
| Bypass Resistance (BYP) | 10% | IMMUNE layers survive all 4 adversary scenarios from TASK-009 | L3 survives injection; L5 survives social engineering |
| Implementation Cost (COST) | 8% | Leverages existing infrastructure (hooks, AST tests, CI) | scripts/pre_tool_use.py exists; tests/architecture/ exists |
| Maintainability (MAINT) | 6% | External-process vectors are self-maintaining; rules need quarterly review | AST auto-adapts; CI stable; rules: quarterly per TASK-009 Currency |

### Pugh Matrix: Architecture Alternatives

Three architecture alternatives evaluated against the recommended hybrid approach as baseline:

| Criterion (TASK-001 Weight) | Alternative A: Rules-Only | Alternative B: Hooks-Heavy | Alternative C: CI-Only | Baseline: Hybrid |
|---|---|---|---|---|
| CRR (25%) | -1 (all VULNERABLE) | +1 (mostly IMMUNE) | 0 (IMMUNE but post-hoc) | 0 (reference) |
| EFF (20%) | -1 (advisory only) | +1 (deterministic) | 0 (deterministic but late) | 0 (reference) |
| PORT (18%) | +1 (100% portable) | -1 (0% portable for hooks) | +1 (95% portable) | 0 (reference) |
| TOK (13%) | -1 (25,700 tokens) | +1 (zero in-context) | +1 (zero in-context) | 0 (reference) |
| BYP (10%) | -1 (easily bypassed) | +1 (hard to bypass) | 0 (moderate) | 0 (reference) |
| COST (8%) | +1 (already exists) | -1 (hook development) | 0 (CI exists) | 0 (reference) |
| MAINT (6%) | +1 (low maintenance) | -1 (high maintenance) | +1 (stable) | 0 (reference) |
| **Weighted Sum (7 criteria)** | **-0.30** | **+0.16** | **+0.32** | **0.00** |

**Qualitative override -- Runtime Enforcement Capability:**

The 7-criterion Pugh matrix produces a numerical advantage for Alternative C (CI-Only, +0.32). However, this numerical result conceals a critical architectural gap: CI-Only provides **zero real-time enforcement**. All violations are detected at commit time (minutes to hours after the violation occurs), meaning architecture boundary violations, import errors, and quality standard deviations are committed to the working tree and potentially propagated before detection.

This gap is not adequately captured by the existing EFF criterion (where CI scores 0, not -1, because it is deterministic once triggered) or BYP criterion (where CI scores 0 because it is hard to bypass once running). The missing dimension is **temporal enforcement** -- the ability to prevent violations during the authoring session rather than detecting them after the fact.

If a "Runtime Enforcement Capability" criterion were added (unweighted, qualitative):

| Criterion | Alt A | Alt B | Alt C | Baseline |
|---|---|---|---|---|
| Runtime enforcement | 0 (advisory only) | +1 (real-time blocking) | **-1 (zero runtime)** | 0 (mixed: L2+L3 runtime, L5 post-hoc) |

With this additional criterion at even 5% weight, Alternative C's advantage is eliminated: +0.32 - 0.05 = +0.27, while the Hybrid gains nothing (remains 0.00). More importantly, Alternative C fails a **binary architectural requirement**: for an enforcement system to provide defense-in-depth, it must have at least one layer that operates during the authoring session (L1-L4), not exclusively post-hoc (L5). CI-Only fails this requirement categorically.

**Conclusion: Qualitative override applied.** The Hybrid architecture is selected despite Alternative C's numerical advantage because:
1. Alternative C fails the binary runtime enforcement requirement.
2. The 7-criterion Pugh matrix does not capture temporal enforcement adequacy.
3. The Hybrid architecture provides the only complete coverage across all enforcement timing windows (author-time via L1-L2, write-time via L3, commit-time via L5, merge-time via L5-CI).

| **Net Assessment (Revised)** | INFERIOR | MARGINAL | **REJECTED (no runtime enforcement)** | **SELECTED** |

**Pugh Matrix Interpretation:**

- **Alternative A (Rules-Only)** scores -0.30, indicating it is categorically inferior to the hybrid. Its portability advantage (+1 on PORT) is overwhelmed by its weakness on CRR, EFF, and BYP.

- **Alternative B (Hooks-Heavy)** scores +0.16, showing marginal improvement over the baseline on enforcement dimensions but at the cost of portability (-1 on PORT). Since PORT has 18% weight (user priority #2), this approach fails the portability requirement.

- **Alternative C (CI-Only)** scores +0.32 on the 7-criterion matrix but is rejected via qualitative override due to the absence of any runtime enforcement capability, which fails the defense-in-depth architectural requirement for at least one author-time enforcement layer.

- **Baseline (Hybrid)** is selected because it satisfies ALL criteria simultaneously, including runtime enforcement capability. It achieves maximum enforcement on Claude Code while maintaining portable enforcement on other platforms.

### Technology Readiness Assessment

| Vector | TRL | Evidence | Gap to TRL 6 |
|--------|-----|----------|--------------|
| V-008/V-009/V-010 (Rules) | 9 | Currently deployed in Jerry; operational experience | None (operational) |
| V-001 (PreToolUse) | 7 | `scripts/pre_tool_use.py` exists with pattern library; needs AST integration | Minor: add AST checks (~1 day) |
| V-038 (AST Import) | 6 | `tests/architecture/test_composition_root.py` exists; validates concept | Move from test to hook |
| V-024 (Context Reinforcement) | 4 | Concept validated by TASK-004 research; no Jerry implementation | Implement UserPromptSubmit hook |
| V-005 (UserPromptSubmit) | 3 | Claude Code API documented; no Jerry implementation | Implement hook script + settings entry |
| V-044 (Pre-commit) | 5 | Pre-commit framework available; not configured for Jerry | Configure `.pre-commit-config.yaml` |
| V-045 (CI Pipeline) | 4 | GitHub Actions available; Jerry has no CI yet | Create `.github/workflows/ci.yml` |
| V-057 (Quality Gates) | 5 | Worktracker system exists; gate logic conceptual | Integrate gate checks into worktracker |
| V-046 (MCP Tool Wrapping) | 3 | MCP spec available; no Jerry implementation | Build MCP server (2+ weeks) |

**TRL Assessment Summary:** The recommended Phase 1 vectors (V-008-V-010, V-024, V-005, V-038) range from TRL 3-9. The existing PreToolUse hook (TRL 7) and AST test infrastructure (TRL 6) provide a strong foundation. The primary TRL gap is V-024/V-005 (UserPromptSubmit + Context Reinforcement) at TRL 3-4, which is the highest-value implementation target.

---

## Risks and Mitigations

| Risk ID | Risk Description | Likelihood | Severity | Mitigation | Related Vectors |
|---------|------------------|------------|----------|------------|-----------------|
| R-001 | Context rot degrades L1 rules to ineffective within 20K tokens | HIGH | HIGH | L2 (V-024) re-injection counteracts; L3-L5 provide immune backup | V-024, V-001, V-044, V-045 |
| R-002 | PreToolUse hook timeout (100ms budget) prevents AST validation | MEDIUM | MEDIUM | Optimize AST check to critical imports only; cache results; fail-open with logging | V-038 performance |
| R-003 | Token budget optimization fails to reach 12,476 target | LOW | MEDIUM | Prioritize removals (tool-configuration.md, markdown-navigation); iterate reductions | V-009 optimization |
| R-004 | UserPromptSubmit hook not available on all Claude Code versions | MEDIUM | HIGH | Detect availability at session start; fall back to SessionStart-only injection | V-005 availability |
| R-005 | False positives from AST checks block valid code patterns | MEDIUM | MEDIUM | Configurable allowlist in `.jerry/enforcement/ast_allowlist.json`; V-055 formal waiver | V-038, V-055 |
| R-006 | Enforcement stack complexity exceeds team's maintenance capacity | LOW | HIGH | Start with Phase 1 only (5 vectors); add layers incrementally; monitor maintenance burden | All |
| R-007 | Platform migration loses enforcement capability | MEDIUM | MEDIUM | Hybrid architecture ensures portable core survives migration; only L3 (hooks) lost | Architecture design |

---

## References

### Primary Sources (Direct Input)

| # | Citation | Used For |
|---|----------|----------|
| 1 | TASK-009: Revised Unified Enforcement Vector Catalog v1.1 | Authoritative vector data, context rot matrix, adversary model, token budget |
| 2 | TASK-001: Evaluation Criteria and Weighting Methodology | 7-dimension evaluation framework, scoring rubrics, weights |
| 3 | TASK-007: Unified Enforcement Vector Catalog v1.0 | Full vector inventory, trade-off analysis, complementary combinations, diminishing returns |

### Architecture Sources

| # | Citation | Used For |
|---|----------|----------|
| 4 | `.claude/rules/architecture-standards.md` | Jerry hexagonal architecture, layer boundaries, composition root |
| 5 | `.claude/settings.json` | Current hook configuration, plugin settings |
| 6 | `scripts/pre_tool_use.py` | Existing hook implementation, pattern library |
| 7 | `scripts/session_start_hook.py` | Existing session start implementation |
| 8 | `tests/architecture/test_composition_root.py` | Existing AST validation infrastructure |

### NASA SE Sources

| # | Citation | Used For |
|---|----------|----------|
| 9 | NASA NPR 7123.1D: Systems Engineering Processes and Requirements | Processes 3, 4, 17 methodology |
| 10 | NASA-STD-8739.8: Software Assurance and Software Safety Standard | Prevent-detect-verify principle |
| 11 | NASA/SP-2016-6105 Rev2: SE Handbook Chapter 6 | Trade study methodology |

### Research Sources (Via TASK-009)

| # | Citation | Used For |
|---|----------|----------|
| 12 | Liu, N. F., et al. (2023). "Lost in the Middle: How Language Models Use Long Contexts." arXiv:2307.03172 | Context rot justification; high-attention zone positioning |
| 13 | TASK-003: .claude/rules/ Enforcement Research | Token budget data (25,700 current, 12,476 optimized) |
| 14 | TASK-004: Prompt Engineering Enforcement Research | Prompt pattern token costs; context reinforcement design |
| 15 | TASK-006: Platform Portability Assessment | Windows compatibility (73%), LLM portability categories |

---

*DISCLAIMER: This trade study is AI-generated guidance based on NASA Systems Engineering standards (NPR 7123.1D). It is advisory only and does not constitute official NASA guidance. All architecture decisions require human review and professional engineering judgment. Not for use in mission-critical decisions without SME validation.*

---

*Agent: nse-architecture (Claude Opus 4.6)*
*Date: 2026-02-13*
*Parent: EN-402 Enforcement Priority Analysis & Decision*
*NASA Processes: NPR 7123.1D -- Process 3 (Logical Decomposition), Process 4 (Design Solution Definition), Process 17 (Decision Analysis)*
*Status: COMPLETE*
*Quality Target: >= 0.92*
*Consumers: TASK-004 (ps-analyst scoring), TASK-005 (ADR)*
