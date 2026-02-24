# Unified Agent Pattern Taxonomy: Phase 3 Synthesis

<!-- PS-ID: PROJ-007 | ENTRY: e-004 | AGENT: ps-synthesizer-001 | DATE: 2026-02-21 -->
<!-- CRITICALITY: C4 -- Definitive pattern catalog; irreversible architecture baseline -->

> Definitive pattern catalog for Claude Code agent development within the Jerry framework. Synthesizes Phase 1 research (3 PS researchers + 1 NSE explorer), Phase 2 analysis (3 PS analysts + 3 NSE analysts), and Barrier 2 cross-pollination handoffs from both pipelines.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Stakeholder-level overview of the unified taxonomy |
| [1. Unified Pattern Taxonomy](#1-unified-pattern-taxonomy) | 57 PS patterns + 10 NSE patterns reconciled into a single catalog |
| [1.1 Workflow Patterns](#11-workflow-patterns) | 7 patterns governing work flow through agent systems |
| [1.2 Delegation Patterns](#12-delegation-patterns) | 9 patterns for work assignment and coordination |
| [1.3 Quality Patterns](#13-quality-patterns) | 10 patterns for ensuring output quality |
| [1.4 Context Patterns](#14-context-patterns) | 12 patterns for context and knowledge management |
| [1.5 Safety Patterns](#15-safety-patterns) | 9 patterns for guardrails and compliance |
| [1.6 Testing Patterns](#16-testing-patterns) | 7 patterns for verification and validation |
| [1.7 Integration Patterns](#17-integration-patterns) | 7 patterns for tool and protocol connections |
| [1.8 Governance Patterns](#18-governance-patterns) | 5 patterns for organizational control |
| [2. Gap Closure Roadmap](#2-gap-closure-roadmap) | 12 gaps mapped to patterns, requirements, risks, and actions |
| [3. Cross-Pipeline Consensus Matrix](#3-cross-pipeline-consensus-matrix) | 10 consensus findings with PS/NSE alignment |
| [4. Open Items Resolution](#4-open-items-resolution) | OI-01 through OI-07 resolved or deferred |
| [5. Pattern Maturity Assessment](#5-pattern-maturity-assessment) | Revised maturity scores incorporating NSE findings |
| [6. Rule Consolidation Recommendation](#6-rule-consolidation-recommendation) | H-25 through H-30 compound-rule proposal for R-P02 |
| [Self-Review (S-010)](#self-review-s-010) | Quality verification checklist |
| [Source Cross-Reference](#source-cross-reference) | All citations traced to source documents |

---

## L0: Executive Summary

This document is the definitive pattern catalog for Claude Code agent development within the Jerry framework, synthesizing the complete output of two parallel research pipelines across three phases.

**What was analyzed:** 57 distinct agent patterns (PS pipeline, 8 families) and 10 architecture design patterns (NSE pipeline) were reconciled into a single coherent taxonomy. These patterns were validated against 52 formal requirements (6 domains), 30 identified risks (3 RED-zone), 5 trade studies (27 alternatives evaluated), and 67+ industry sources from Anthropic, Google, Microsoft, OpenAI, and academic research.

**Key findings:**

1. **Jerry's architecture is validated and industry-leading in governance.** The framework implements 46 of 57 identified patterns at partial or better maturity (81% coverage). Governance (4.5/5) and Safety (4.3/5) maturity exceed all published industry frameworks. No patterns are over-engineered -- governance scales proportionally with criticality.

2. **Three enhancements dominate all analyses.** Schema validation (+0.45 trade study delta), structured handoff protocol (#1 failure source mitigation), and context budget monitoring (highest RPN risk at 392) emerge as the top three priorities across both pipelines, all risk categories, and all consensus findings.

3. **Testing is the largest maturity gap (2.1/5).** Four of seven testing patterns are absent: agent unit testing, end-to-end workflow testing, drift detection, and evaluation-driven development. This represents the clearest path to framework improvement.

4. **Rule consolidation is urgent.** At 31/35 HARD rule slots (89%), rule proliferation (R-P02, RED-zone) threatens governance scalability. Consolidating H-25 through H-30 into two compound rules frees 4 slots and reduces the count to 27, well within the 20-25 "sweet spot" identified by nse-risk-001.

5. **The 10 NSE architecture patterns map cleanly onto the 8 PS families.** Zero structural conflicts were found between the two taxonomies. The NSE patterns provide formal architecture grounding (hexagonal mapping, JSON schemas, tool tiers) for patterns that the PS analysis identified through industry research.

**Bottom line:** Jerry is at Level 3.3 (Defined) maturity with clear, evidence-backed paths to Level 4.0 (Managed). The recommended implementation sequence is: (1) schema validation and structured handoffs (P1, closes the highest-value gaps), (2) rule consolidation (P1, addresses the most urgent process risk), (3) context budget monitoring (P1, mitigates the highest-score risk), (4) testing infrastructure (P2, closes the largest maturity gap).

---

## 1. Unified Pattern Taxonomy

The PS pipeline identified 57 patterns across 8 families through industry research. The NSE pipeline independently identified 10 design patterns through architecture analysis. This section reconciles both into a single catalog.

**Reconciliation methodology:** The 8 PS families serve as the organizing framework. Each of the 10 NSE patterns maps to one or more PS families based on the problem it solves. Where an NSE pattern adds architectural depth to a PS pattern (e.g., NSE Pattern 8 "Quality Gate" adds the 4-layer gate architecture to PS patterns QA-01 through QA-10), the two are merged with the NSE contribution noted as "architecture formalization."

**NSE Pattern to PS Family Mapping:**

| NSE Pattern | PS Family Mapping | Contribution |
|-------------|-------------------|--------------|
| Pattern 1: Specialist Agent | Delegation (DL-01) | Architecture formalization of the skill-based specialist |
| Pattern 2: Orchestrator-Worker | Delegation (DL-01, DL-03) | Architecture formalization with P-003 constraint diagram |
| Pattern 3: Creator-Critic-Revision | Quality (QA-01, QA-02) | Iteration model with score progression visualization |
| Pattern 4: Progressive Disclosure | Context (CX-02) | Three-tier architecture with token budgets |
| Pattern 5: Tool Restriction | Safety (SF-03) | T1-T5 tier taxonomy with selection guidelines |
| Pattern 6: Structured Handoff | Integration (IN-07) | JSON Schema definition and validation protocol |
| Pattern 7: Context Budget | Context (CX-01, CX-03) | Token allocation model (CB-01 through CB-05) |
| Pattern 8: Quality Gate | Quality (QA-07), Governance (GV-01) | 4-layer gate architecture with criticality proportionality |
| Pattern 9: Cognitive Mode | Delegation (DL-06), Context (CX-02) | 5-mode enumeration with behavioral specifications |
| Pattern 10: Layered Routing | Workflow (WF-02), Integration (IN-05) | 3-layer routing architecture with latency characteristics |

---

### 1.1 Workflow Patterns

Patterns governing the flow of work through agent systems.

| ID | Pattern | Jerry Status | Problem | Solution Summary | Related Requirements | Related Risks |
|----|---------|-------------|---------|------------------|---------------------|---------------|
| WF-01 | Prompt Chaining | **Implemented** | Fixed subtasks require sequential processing with quality gates between stages | Chain LLM calls sequentially; each processes prior output with programmatic validation | PR-004 (progressive disclosure) | R-T01 (context rot accumulates across chain) |
| WF-02 | Routing / Classification | **Implemented** | Inputs require classification and routing to specialized processes | Keyword-based trigger map with proactive invocation (H-22). NSE Pattern 10 adds 3-layer architecture: keyword -> decision tree -> LLM fallback | RR-001 (keyword primary), RR-003 (LLM fallback), RR-004 (determinism) | R-T06 (stochastic variance if LLM routing used) |
| WF-03 | Parallelization (Sectioning) | **Implemented** | Independent subtasks can run simultaneously | Fan-out to parallel workers, aggregate results at convergence point | AR-005 (context isolation) | R-O01 (token cost multiplied by parallel count) |
| WF-04 | Parallelization (Voting) | **Not Implemented** | Higher confidence needed for subjective outputs | Execute same task multiple times; aggregate via majority vote or weighted average | -- | R-O01 (3-10x token cost per Anthropic) |
| WF-05 | Sequential Pipeline | **Implemented** | Data processing requires fixed-order transformations | Linear agent pipeline via shared state with clear stage dependencies and checkpoints | HR-004 (state preservation) | R-T02 (error amplification across stages) |
| WF-06 | Cross-Pollinated Pipeline | **Implemented** | Multi-disciplinary analysis requires cross-fertilization | Parallel pipelines with synchronization barriers for bidirectional exchange. Jerry original pattern; operational in PROJ-007 | HR-001 (structured handoff), HR-006 (quality gate at handoff) | R-A03 (state fragility at barriers) |
| WF-07 | Fan-Out/Fan-In (Gather) | **Implemented** | Research breadth requires parallel investigation with synthesis | Concurrent execution with result aggregation at convergence; orch-synthesizer handles fan-in | AR-005 (context isolation), HR-002 (required handoff fields) | R-T01 (synthesizer context fills with multiple inputs) |

**Summary:** 6/7 implemented. WF-04 (Voting) is the only gap; its value is limited for Jerry's deterministic workflow needs (LOW priority). WF-06 (Cross-Pollinated Pipeline) is a Jerry original with no direct industry equivalent.

---

### 1.2 Delegation Patterns

Patterns for how work is assigned, decomposed, and coordinated across agents. Incorporates NSE Patterns 1 (Specialist Agent), 2 (Orchestrator-Worker), and 9 (Cognitive Mode).

| ID | Pattern | Jerry Status | Problem | Solution Summary | Related Requirements | Related Risks |
|----|---------|-------------|---------|------------------|---------------------|---------------|
| DL-01 | Orchestrator-Workers | **Implemented** | Complex tasks require coordination across specialists | Central orchestrator decomposes tasks, delegates via Task tool, synthesizes outputs. Max one level (P-003/H-01). NSE Pattern 2 provides formal topology diagram reducing 17x amplification to ~1.3x | AR-004 (single-level), AR-005 (context isolation), SR-001 (P-003) | R-T02 (error amplification), R-A02 (agent proliferation) |
| DL-02 | Hierarchical Decomposition | **Partial** | Deep problem decomposition requires recursive breakdown | Parent agents break goals into sub-tasks. Jerry: single-level only per H-01; conceptual decomposition via orchestration phases | AR-004 (single-level constraint) | R-T01 (context rot in deep decomposition) |
| DL-03 | Manager Pattern | **Implemented** | Team coordination requires single authority | Central manager coordinates via tool calls, synthesizes results. Jerry: main context as manager; orch-planner designs delegation | AR-011 (agent registration) | R-P01 (governance overhead) |
| DL-04 | Coordinator/Dispatcher | **Implemented** | Intent-based routing requires analysis and specialist selection | Trigger map + H-22 proactive invocation; Claude session as dispatcher | RR-001 (keyword primary), RR-007 (multi-skill) | R-T06 (stochastic variance) |
| DL-05 | Dynamic Handoff | **Not Implemented** | Emergent routing requires agent-determined handoff | Agents assess and transfer tasks at runtime. Intentionally excluded per H-01 -- Jerry uses orchestrator-mediated handoffs | AR-004 (conflicts with single-level) | R-T02 (uncontrolled error amplification) |
| DL-06 | Description-Driven Delegation | **Implemented** | Large agent pools require automatic delegation decisions | Agent descriptions drive selection. H-28 description standards; YAML `description` field. NSE Pattern 9 adds cognitive mode as selection dimension | AR-009 (description quality), PR-002 (cognitive mode) | R-D01 (complexity barrier for authors) |
| DL-07 | Context-Centric Decomposition | **Not Implemented** | Feature-scoped decomposition prevents telephone-game context loss | Divide by context boundaries rather than work type. Jerry mitigates via filesystem-as-memory | -- | R-A03 (state fragility) |
| DL-08 | Contract-First Delegation | **Not Implemented** | High-stakes delegation requires verifiable outcomes | Tasks decomposed until sub-tasks match automated verification. Emerging pattern from Google DeepMind (2026) | HR-006 (quality gate at handoff) | R-T02 (error amplification) |
| DL-09 | Effort Scaling | **Not Implemented** | Variable-complexity workflows require dynamic agent spawning | Dynamic agent counts based on task complexity. Fixed agent assignments in Jerry | -- | R-O01 (cost escalation) |

**Summary:** 5/9 implemented. DL-05 is intentionally excluded per H-01. DL-07, DL-08, DL-09 are evolutionary gaps; DL-07 is mitigated by filesystem-as-memory (LOW priority).

---

### 1.3 Quality Patterns

Patterns for ensuring and improving agent output quality. Incorporates NSE Patterns 3 (Creator-Critic-Revision) and 8 (Quality Gate).

| ID | Pattern | Jerry Status | Problem | Solution Summary | Related Requirements | Related Risks |
|----|---------|-------------|---------|------------------|---------------------|---------------|
| QA-01 | Evaluator-Optimizer | **Implemented** | Iterative refinement requires separate generation and evaluation | Creator generates, critic evaluates with S-014 rubric, revision iterates. H-14 minimum 3 iterations. NSE Pattern 3 provides score progression model (0.78 -> 0.88 -> 0.93) | QR-004 (3 iterations), QR-005 (0.92 threshold) | R-Q01 (false positives), R-Q03 (creator-critic collusion) |
| QA-02 | Generator-Critic Loop | **Implemented** | Quality improvement requires measurable quality dimensions | Generate, validate with conditional looping until threshold. H-13 >= 0.92 | QR-005 (threshold), QR-009 (leniency counteraction) | R-Q01 (leniency bias) |
| QA-03 | LLM-as-Judge Scoring | **Implemented** | Non-deterministic outputs require structured quality assessment | S-014 with 6 dimensions, weighted composite. adv-scorer agent | QR-005, QR-009 | R-Q01, R-Q04 (scoring drift) |
| QA-04 | Self-Review / Self-Refine | **Implemented** | All deliverables need first-pass quality improvement | Agent reviews own output before presenting. H-15 mandatory, S-010 strategy | QR-002 (self-review required) | R-Q01 (self-assessment bias) |
| QA-05 | Steelman-Before-Critique | **Implemented** | Adversarial review must not prematurely reject sound approaches | Strengthen the best version before challenging. H-16 HARD rule: S-003 before S-002 | QR-006 (S-003 before S-002) | R-Q02 (false negatives from premature critique) |
| QA-06 | Tournament Review | **Implemented** | C4 critical decisions require comprehensive adversarial review | All 10 strategies executed in ordered sequence. Groups A-F | QR-008 (tournament for C4) | R-O01 (100K+ tokens), R-T05 (token ceiling) |
| QA-07 | Criticality-Based Strategy Selection | **Implemented** | Variable-risk decisions require proportional review depth | C1-C4 with strategy sets. NSE Pattern 8 adds 4-layer gate architecture: Schema -> Self-Review -> Critic -> Tournament | QR-001 (proportional enforcement) | R-P01 (governance overhead for over-classified work) |
| QA-08 | Schema-Based Output Validation | **Not Implemented** | Structural defects consume expensive LLM evaluation cycles | Deterministic pre-check using JSON Schema before LLM-based QA. Zero LLM cost. NSE Pattern 8 Layer 1 | QR-003 (output schema validation), AR-003 (definition schema) | R-Q01 (false positive mitigation), R-A03 (state fragility) |
| QA-09 | Verification Subagent | **Partial** | Verifiable outcomes need blackbox testing | Dedicated agent tests output against explicit success criteria. ps-validator exists but not fully isolated | -- | R-Q03 (correlated evaluation) |
| QA-10 | Constitutional AI Critique | **Implemented** | Governance compliance requires structured verification | S-007 strategy; constitutional compliance checks at C2+ | SR-001 (P-003/P-020/P-022), SR-007 (auto-escalation) | R-S04 (unauthorized destructive actions) |

**Summary:** 8/10 implemented. QA-08 (Schema Validation) is the highest-priority gap across all analyses (+0.45 trade study delta, R-Q01 mitigation, AR-003 requirement). NSE Pattern 8 adds the 4-layer quality gate architecture that formalizes the relationship between all quality patterns.

---

### 1.4 Context Patterns

Patterns for managing information flow, context windows, and knowledge persistence. Incorporates NSE Patterns 4 (Progressive Disclosure) and 7 (Context Budget).

| ID | Pattern | Jerry Status | Problem | Solution Summary | Related Requirements | Related Risks |
|----|---------|-------------|---------|------------------|---------------------|---------------|
| CX-01 | Filesystem-as-Memory | **Implemented** | Context rot degrades LLM performance as context fills | Persist state to files; load selectively. Jerry core philosophy (P-002) | HR-004 (state preservation) | R-T01 (partial mitigation only) |
| CX-02 | Progressive Disclosure (Skills) | **Implemented** | Large skill libraries exhaust context at startup | Three-tier loading: metadata (~500 tok), core (~5K), supplementary (variable). NSE Pattern 4 with token budget per tier | PR-004 (progressive disclosure), PR-008 (L0/L1/L2) | R-T01, R-T05 (token ceiling) |
| CX-03 | Compaction / Summarization | **Partial** | Long sessions fill context with verbose history | Compress conversation history preserving key decisions. Auto-compaction at 95% exists; no Jerry-specific strategy | -- | R-T01 (lossy compaction may discard relevant info) |
| CX-04 | Structured Note-Taking | **Implemented** | Multi-session coherence requires persistent state tracking | WORKTRACKER.md, PLAN.md, ORCHESTRATION.yaml as persistent notes | HR-004, SR-006 (audit trails) | R-P04 (documentation decay) |
| CX-05 | Sub-Agent Context Isolation | **Implemented** | Verbose operations overflow parent context | Each subagent runs in own context window via Task tool. Claude Code native | AR-005 (context isolation) | R-A03 (information loss at boundary) |
| CX-06 | Just-in-Time Retrieval | **Implemented** | Variable information needs require on-demand loading | Maintain lightweight identifiers; dynamically load via Read tool | PR-004 | R-T05 (if retrieval is too aggressive) |
| CX-07 | Observation Masking | **Not Implemented** | Tool outputs dominate context, drowning reasoning history | Preserve reasoning/action history; selectively compress tool observations only | -- | R-O04 (context fragmentation) |
| CX-08 | Handle Pattern | **Implemented** | Large objects waste context when fully embedded | Reference by name/ID; load on-demand. Artifact paths in handoffs | HR-003 (artifact path validation), CB-03 | R-T05 (reduced if handles used consistently) |
| CX-09 | L2 Re-Injection | **Implemented** | Critical rules fade from context as it fills | Re-inject highest-priority rules at every prompt via HTML comments. Jerry original; immune to context rot | PR-006 (instruction hierarchy) | R-T01 (partial mitigation: only L2-injected rules survive) |
| CX-10 | Git Worktree Isolation | **Not Implemented** | Experimental changes risk polluting main workspace | Run subagent in temporary git worktree for file-level isolation | -- | R-S03 (data leakage) |
| CX-11 | Agent Memory (Cross-Session) | **Partial** | Cross-session learning requires accumulated expertise | MCP-002 Memory-Keeper at phase boundaries; no per-agent MEMORY.md | SR-008 (MCP governance) | R-T04 (MCP server instability) |
| CX-12 | Tool Result Clearing | **Not Implemented** | Intermediate tool outputs consume context after processing | Explicitly clear tool results after extraction to free context budget | -- | R-O04 (context fragmentation) |

**Summary:** 8/12 fully or partially implemented. CX-09 (L2 Re-Injection) is a Jerry original with no industry equivalent. NSE Pattern 7 adds quantified context budget allocation (CB-01 through CB-05) and the memory hierarchy model (context window -> filesystem -> MCP).

---

### 1.5 Safety Patterns

Patterns for guardrails, governance, bounded autonomy, and compliance. Incorporates NSE Pattern 5 (Tool Restriction).

| ID | Pattern | Jerry Status | Problem | Solution Summary | Related Requirements | Related Risks |
|----|---------|-------------|---------|------------------|---------------------|---------------|
| SF-01 | Constitutional AI Constraints | **Implemented** | All agents need predefined behavioral boundaries | JERRY_CONSTITUTION.md; H-01 through H-31; P-001 through P-043 | SR-001 (P-003/P-020/P-022) | R-S04 (unauthorized actions) |
| SF-02 | Multi-Layer Guardrails | **Implemented** | Defense in depth requires validation at multiple points | L1-L5 enforcement architecture; PreToolUse/PostToolUse hooks | SR-002 (input validation), SR-003 (output filtering) | R-S01 (prompt injection) |
| SF-03 | Least Privilege (Tool Restriction) | **Implemented** | Agents must not exceed authorized capabilities | Per-agent `allowed_tools`; TOOL_REGISTRY.yaml SSOT. NSE Pattern 5 adds T1-T5 security tiers with selection rule: "always select lowest tier that satisfies requirements" | AR-006 (tool restriction), SR-008 (MCP governance) | R-S02 (tool misuse) |
| SF-04 | Bounded Autonomy | **Implemented** | Agents need defined authority boundaries | H-02 user authority; H-31 clarify when ambiguous; AE-006 escalation | SR-004 (user authority), SR-010 (ambiguity clarification) | R-S04 (unauthorized actions) |
| SF-05 | Human-in-the-Loop (HITL) Gates | **Implemented** | Irreversible decisions require human approval | AE-001 through AE-006 auto-escalation; H-02 user authority | SR-007 (auto-escalation), QR-001 (proportional enforcement) | R-P01 (governance overhead) |
| SF-06 | Red Teaming / Purple Teaming | **Implemented** | Security-critical systems need adversarial testing | S-001 Red Team strategy; adversary skill tournament mode; C4 requires all 10 strategies | QR-008 (tournament for C4) | R-Q03 (correlated blind spots) |
| SF-07 | Audit Trails | **Implemented** | Accountability requires complete operational records | WORKTRACKER.md; ORCHESTRATION.yaml; worktracker integrity rules WTI-001 through WTI-009 | SR-006 (audit trail requirements) | R-P04 (documentation decay) |
| SF-08 | Auto-Escalation | **Implemented** | High-impact changes must receive proportionate review | AE-001 through AE-006. Jerry original -- more formal than any industry equivalent | SR-007 (governance auto-escalation) | R-P02 (rule proliferation feeds escalation complexity) |
| SF-09 | Circuit Breaker | **Partial** | Runaway iteration loops consume resources without progress | H-14 sets minimum 3 iterations. Orchestration SKILL.md mentions max 3 at barriers. No global maximum as HARD rule | RR-006 (max 3 routing hops) | R-O02 (latency degradation from unbounded loops) |

**Summary:** 8/9 implemented at high maturity. SF-09 (Circuit Breaker) has a floor (H-14 minimum) but no ceiling as a global HARD rule -- this is the single remaining anti-pattern vulnerability. Jerry's governance framework is ahead of all industry norms based on Phase 1 research evidence.

---

### 1.6 Testing Patterns

Patterns for verifying agent behavior, output quality, and system correctness.

| ID | Pattern | Jerry Status | Problem | Solution Summary | Related Requirements | Related Risks |
|----|---------|-------------|---------|------------------|---------------------|---------------|
| TS-01 | LLM-as-Judge Evaluation | **Implemented** | Non-deterministic outputs require structured assessment | S-014 with 6 dimensions, weighted composite. adv-scorer agent. H-13 threshold | QR-005 (0.92 threshold), QR-009 (leniency counteraction) | R-Q01 (leniency bias), R-Q04 (scoring drift) |
| TS-02 | Behavioral End-to-End Testing | **Not Implemented** | Multi-agent workflows need full integration validation | Full workflow simulation with real tool calls; browser automation for verification | -- | R-A04 (integration complexity), R-T03 (model regression) |
| TS-03 | Feature List Tracking | **Partial** | Long-running agents may prematurely declare completion | Comprehensive feature enumeration with pass/fail tracking. WORKTRACKER.md tracks acceptance criteria | -- | R-P04 (documentation decay) |
| TS-04 | Evaluation-Driven Development | **Not Implemented** | Agent improvement requires systematic capability assessment | Identify gaps through testing on representative tasks; build skills to address shortcomings | -- | R-D03 (skill ceiling for authors) |
| TS-05 | Adversarial Testing (Red Teaming) | **Implemented** | Governance compliance requires adversarial probing | S-001 Red Team strategy; adversary skill with tournament mode | QR-008 (tournament for C4) | R-S01 (prompt injection detection) |
| TS-06 | Regression and Drift Detection | **Not Implemented** | Evolving systems need behavioral stability monitoring | Continuous monitoring for behavioral drift; baseline comparison across model versions | -- | R-T03 (model regression), R-Q04 (scoring drift) |
| TS-07 | Agent Unit Testing | **Not Implemented** | Agent definitions need isolated validation with controlled inputs | Test individual agents in isolation with known inputs and expected outputs | -- | R-P03 (maintenance burden without tests) |

**Summary:** 3/7 implemented. This is Jerry's **weakest pattern family** (maturity 2.1/5). The implemented patterns (TS-01, TS-05) are strong, but infrastructure patterns (TS-02, TS-04, TS-06, TS-07) are entirely absent. This represents the largest maturity gap and the clearest path to framework improvement.

---

### 1.7 Integration Patterns

Patterns for connecting agents with external tools, protocols, and services. Incorporates NSE Pattern 6 (Structured Handoff) and NSE Pattern 10 (Layered Routing).

| ID | Pattern | Jerry Status | Problem | Solution Summary | Related Requirements | Related Risks |
|----|---------|-------------|---------|------------------|---------------------|---------------|
| IN-01 | Model Context Protocol (MCP) | **Implemented** | External tools need standardized connection interfaces | Context7 and Memory-Keeper via MCP; mcp-tool-standards.md governance | SR-008 (MCP governance) | R-T04 (MCP server instability) |
| IN-02 | Static Tool Assignment | **Implemented** | Security requires predictable, auditable tool access | YAML frontmatter `allowed_tools`; per-agent allowlists. TS-5 winner (4.15) | AR-006 (tool restriction) | R-S02 (tool misuse -- controlled) |
| IN-03 | Dynamic Tool Discovery | **Not Implemented** | Large tool pools need runtime capability matching | Agents discover available tools at runtime. Reserved for future; static assignment optimal at current scale | -- | R-S02 (security concern with dynamic discovery) |
| IN-04 | Contextual Function Selection | **Not Implemented** | Tool overload requires embedding-based selection | Top-N most relevant tools per request. Premature at Jerry's current scale (< 20 tools per agent) | -- | R-A04 (integration complexity) |
| IN-05 | Hook-Based Enforcement | **Partial** | Constraint enforcement requires deterministic tool-boundary validation | L3 enforcement layer; PreToolUse/PostToolUse hooks. Conceptually designed but not fully implemented for all constraints | SR-002 (input validation), SR-003 (output filtering) | R-S01 (prompt injection) |
| IN-06 | MCP Tool Search | **Not Implemented** | Many MCP servers exceed context budget for tool descriptions | Dynamic MCP tool loading on-demand. Jerry has 2 MCP servers; threshold not reached | -- | R-O04 (context fragmentation) |
| IN-07 | Structured Handoff Schemas | **Partial** | Free-text handoffs cause information loss at agent boundaries | JSON Schema-constrained data contracts. NSE Pattern 6 provides full schema definition with `from_agent`, `to_agent`, `context`, `request`, `criticality` fields. AGENTS.md defines structure but not validated/enforced | HR-001 (structured format), HR-002 (required fields), HR-003 (artifact validation), HR-006 (quality gate at handoff) | R-T02 (error amplification), R-A03 (state fragility) |

**Summary:** 3/7 fully implemented, 2 partial. IN-07 (Structured Handoffs) and IN-05 (Hook-Based Enforcement) are the high-value partial implementations. NSE Pattern 6 provides the JSON Schema that closes IN-07; NSE Pattern 10 provides the layered routing architecture that extends WF-02.

---

### 1.8 Governance Patterns

Patterns for organizational control, compliance, decision-making, and framework evolution.

| ID | Pattern | Jerry Status | Problem | Solution Summary | Related Requirements | Related Risks |
|----|---------|-------------|---------|------------------|---------------------|---------------|
| GV-01 | Criticality Classification | **Implemented** | Variable-risk decisions need proportional review rigor | C1-C4 levels with auto-escalation (AE-001 through AE-006); strategy sets per criticality. NSE Pattern 8 adds the 4-layer quality gate architecture that operationalizes criticality | QR-001 (proportional enforcement), SR-007 (auto-escalation) | R-P01 (governance overhead) |
| GV-02 | SSOT (Single Source of Truth) | **Implemented** | Configuration drift across distributed rules creates inconsistency | quality-enforcement.md as SSOT; worktracker integrity rules reference SSOT | -- | R-P04 (documentation decay) |
| GV-03 | Tier Vocabulary (HARD/MEDIUM/SOFT) | **Implemented** | Multi-level governance needs formal enforcement language | HARD: cannot override, <=35 count. MEDIUM: documented justification. SOFT: no justification | -- | R-P02 (rule proliferation approaching ceiling) |
| GV-04 | ADR (Architecture Decision Records) | **Implemented** | Design trade-offs need structured documentation and traceability | ADR template; ps-architect agent; AE-003/AE-004 auto-escalation for ADRs. NSE architecture produced 3 recommended ADRs (ADR-001, ADR-002, ADR-003) | -- | R-P04 (ADR decay) |
| GV-05 | Proactive Skill Invocation | **Implemented** | Quality tools must be used consistently without waiting for explicit user request | H-22 HARD rule; trigger map with keywords; behavior rules for early invocation | RR-001 (keyword primary), RR-002 (trigger completeness) | R-D02 (developer resistance to proactive invocation) |

**Summary:** 5/5 implemented at the highest maturity of any family (4.5/5). This is Jerry's **most distinctive contribution** -- no other framework in the Phase 1 research exhibits this level of formalized governance. The combination of constitutional constraints, criticality classification, auto-escalation, tier vocabulary, and SSOT governance is unique.

---

## 2. Gap Closure Roadmap

This section maps the 12 identified gaps (GAP-01 through GAP-12 from ps-analyst-001) to specific pattern enhancements, NSE requirements, risks, priorities, and implementation approaches.

### Priority 1 -- Critical (Immediate)

| Gap | Pattern(s) | NSE Requirement(s) | Risk(s) Mitigated | Implementation Approach |
|-----|-----------|--------------------|--------------------|------------------------|
| **GAP-01: Schema validation for agent definitions** | QA-08, IN-07 | AR-003 (schema validation, SHOULD), AR-002 (required fields, MUST) | R-Q01 (false positive scoring, net priority 6.00), R-A03 (state fragility) | Create JSON Schema Draft 2020-12 for agent YAML frontmatter per ADR-001. Required fields: `name`, `version`, `description`, `model`, `identity.role`, `identity.cognitive_mode`, `capabilities.allowed_tools`, `guardrails`, `output`. Validate all 37 existing agents. CI integration for future definitions. |
| **GAP-02: Schema validation as QA pre-check layer** | QA-08 (NSE Pattern 8, Layer 1) | QR-003 (output schema validation, SHOULD) | R-Q01, R-T02 (error amplification at handoff) | Define output schemas for major deliverable types: research reports (L0/L1/L2 sections, H-23 nav table, H-24 anchor links), architecture documents, ADRs. Layer 1 of the 4-layer quality gate catches structural defects before LLM scoring (zero LLM cost). |
| **GAP-03: Structured handoff protocol (JSON Schema)** | IN-07 (NSE Pattern 6) | HR-001 (structured format, MUST), HR-002 (required fields, MUST), HR-003 (artifact validation, MUST), HR-006 (quality gate at handoff, MUST) | R-T02 (error amplification, net priority 4.50), R-A03 (state fragility, net priority 3.00) | Adopt the JSON Schema from nse-architecture-001 Section 2.1.2. Required fields: `from_agent`, `to_agent`, `context.task_id`, `context.artifacts`, `context.summary`, `context.key_findings`, `context.blockers`, `context.confidence`, `request`, `criticality`. Persist schema to `docs/schemas/session_context.json`. Validate all handoffs against schema. |

**Note on GAP-01 and GAP-02:** These are the same underlying capability (schema validation) applied to two targets (agent definitions and agent outputs). Combined trade study delta: +0.85 (highest single enhancement value across all analyses). Both should be implemented together.

### Priority 2 -- Strategic

| Gap | Pattern(s) | NSE Requirement(s) | Risk(s) Mitigated | Implementation Approach |
|-----|-----------|--------------------|--------------------|------------------------|
| **GAP-04: Agent behavioral testing framework** | TS-07, TS-02 | -- (no formal requirement; gap identified by PS analysis) | R-T03 (model regression), R-P03 (maintenance burden) | Design controlled-input/expected-output test harness for agent definitions. Start with agent unit tests (TS-07): test individual agents with known inputs and verify output structure, cognitive mode alignment, and tool usage patterns. Extend to E2E workflow tests (TS-02) after unit infrastructure is proven. |
| **GAP-05: Routing interface abstraction** | WF-02 (NSE Pattern 10) | RR-001 (keyword primary, MUST), RR-003 (LLM fallback, SHOULD), RR-005 (negative keywords, SHOULD) | R-T06 (stochastic variance) | Implement ADR-002 in phases: Phase A -- add negative keywords column to trigger map (LOW effort, immediate). Phase B -- add priority ordering for collision resolution (LOW effort). Phase C -- LLM fallback for ambiguous cases when skill count approaches 15 (deferred until empirical trigger). |
| **GAP-06: Context budget monitoring** | CX-03, CX-07 (NSE Pattern 7) | -- (no formal requirement; CB-01 through CB-05 are architecture guidelines) | R-T01 (context rot at scale, highest risk score 20, net priority 5.00) | Implement context budget monitor per nse-risk-001 recommendation: warn at 60% context usage, halt at 80%. Agent self-diagnostics check before quality gate invocation. Document maximum recommended workflow complexity per criticality level. |
| **GAP-07: Iteration ceiling enforcement** | SF-09 | RR-006 (max 3 routing hops, MUST) | R-O02 (latency degradation), R-O01 (token cost) | Define global maximum iteration HARD rule. Recommended: max 7 iterations for C2/C3, max 10 for C4, mandatory human escalation when ceiling reached. This closes the last significant anti-pattern vulnerability (circuit breaker ceiling). |

### Priority 3 -- Evolutionary

| Gap | Pattern(s) | NSE Requirement(s) | Risk(s) Mitigated | Implementation Approach |
|-----|-----------|--------------------|--------------------|------------------------|
| **GAP-08: LLM routing fallback** | WF-02 (NSE Pattern 10, Layer 3) | RR-003 (LLM fallback, SHOULD) | R-T06 (stochastic variance) | Deferred until skill count approaches 15. Current keyword routing is optimal at 8 skills (+0.05 trade study delta is marginal). Monitor for routing failure signals: missed invocations, ambiguous keyword matches, multi-skill overlap. |
| **GAP-09: Capability discovery for tools** | IN-03, IN-04 | -- | R-A04 (integration complexity) | Deferred. TS-5 winner is static assignment (4.15). Dynamic discovery ranked 5th (2.90). Relevant only at 20+ tools per agent. |
| **GAP-10: Drift detection** | TS-06 | -- | R-T03 (model regression), R-Q04 (scoring calibration drift) | Requires baseline behavioral tests first (GAP-04 prerequisite). Implement after agent unit testing framework is established. Monitor quality score variance across model versions as a leading indicator. |
| **GAP-11: Contract-first delegation** | DL-08 | -- | R-T02 (error amplification) | Emerging pattern from Google DeepMind (2026). Evaluate as handoff protocol (GAP-03) matures. Current quality gates at handoff boundaries provide comparable error detection. |
| **GAP-12: Scoring variance monitoring** | TS-01 (enhancement) | QR-009 (leniency counteraction, MUST) | R-Q01 (false positives), R-Q04 (scoring drift) | Implement score stability checks: score same deliverable twice, flag if variance exceeds 0.05. LOW effort. Can be added to adv-scorer agent instructions without infrastructure. |

---

## 3. Cross-Pipeline Consensus Matrix

The NSE-to-PS handoff identified 10 consensus findings where all three NSE Phase 2 agents (requirements, architecture, risk) converge. This section documents agreement between the PS and NSE pipelines and flags tensions requiring resolution.

| # | Consensus Finding | PS Pipeline Evidence | NSE Pipeline Evidence | Agreement Level | Tensions/Trade-offs |
|---|-------------------|---------------------|----------------------|-----------------|---------------------|
| 1 | **Schema validation is the highest-priority enhancement** | GAP-01/GAP-02 P1; +0.45/+0.40 trade study delta; highest impact single enhancement (L2 Implication 3) | AR-003 (SHOULD, highest-value); ADR-001 (B5); Pattern 8 Layer 1; R-Q01 mitigation #1 | **Full agreement** | None. Both pipelines independently identify this as #1 priority. |
| 2 | **Structured handoff protocol is non-negotiable** | GAP-03 P1; #1 failure source per Google 2026; FMEA HF-01 RPN=336 | HR-001 through HR-006 (5 MUST); Pattern 6 JSON Schema; R-T02 mitigation | **Full agreement** | Schema complexity vs. adoption friction. NSE specifies 10 fields; PS recommends 7. Resolution: adopt NSE schema (10 fields) as SHOULD; 7 core fields as MUST. |
| 3 | **Single-level nesting (P-003) is validated** | DL-01 implemented; H-01 HARD rule; TS-1 winner (4.25) | AR-004 (MUST); Pattern 2; reduces 17x to 1.3x | **Full agreement** | None. Both pipelines validate without reservation. |
| 4 | **Keyword-first routing is optimal for current scale** | WF-02 implemented; +0.05 delta (near-parity); scaling trigger at 15 skills | RR-001 (MUST); ADR-002; Pattern 10 | **Full agreement** | When to add LLM fallback. PS recommends monitoring for 15-skill trigger. NSE recommends SHOULD-level readiness. Resolution: implement negative keywords and priority ordering now (low effort); defer LLM fallback until empirical trigger. |
| 5 | **Criticality-proportional enforcement is essential** | QA-07 implemented; not over-engineered (L2 assessment); C1-C4 validated across all trade studies | QR-001 (MUST); Pattern 8 (4-layer gate); R-P01 mitigation | **Full agreement** | None. The strongest cross-pipeline validation. |
| 6 | **Progressive disclosure prevents context rot** | CX-02 implemented; three-tier model validated by Anthropic | PR-004 (MUST); Pattern 4; CB-01 through CB-05; R-T01 partial mitigation | **Full agreement** | Partial mitigation only for R-T01. Both pipelines note that progressive disclosure addresses initial loading but not runtime context accumulation. Context budget monitoring (GAP-06) is the complementary mitigation. |
| 7 | **Tool restriction by least privilege** | SF-03 implemented; T1-T5 tiers; TS-5 winner | AR-006 (MUST); Pattern 5; R-S02 controlled | **Full agreement** | None. |
| 8 | **Rule consolidation needed before adding more** | L2 Implication 6 (anti-pattern prevention needs ceiling enforcement); ps-analyst-001 notes 31/35 slots used | R-P02 RED-zone (score 15); #1 net priority mitigation action (9.00); H-25 through H-30 consolidation candidate | **Full agreement** | How to consolidate. NSE recommends compound-rule patterns (sub-clauses under single H-ID). PS recommends adding iteration ceiling HARD rule (new H-32). Resolution: consolidate first (free 4 slots), then add H-32 (iteration ceiling) from freed capacity. |
| 9 | **Cognitive mode specialization differentiates agents** | DL-06 implemented; 5 modes in NSE Pattern 9; per-agent cognitive mode assignment validated across all 37 agents | PR-002 (MUST, enumerated set); Pattern 9 | **Full agreement** | PR-002 enumerates 8 modes (`divergent`, `convergent`, `integrative`, `systematic`, `strategic`, `critical`, `forensic`, `communicative`). NSE Pattern 9 defines 5 modes. Resolution: adopt PR-002's 8-mode set as the canonical enumeration; the 5 NSE modes are a subset. |
| 10 | **Audit trail and observability gaps exist** | GAP-10 (drift detection); GAP-12 (scoring variance); Testing maturity 2.1 (lowest) | SR-006 (SHOULD); RR-008 (SHOULD); R-Q04, R-T03 | **Full agreement** | Priority and scope. PS identifies testing infrastructure as the gap. NSE identifies audit trail storage mechanism (OI-06) and routing observability (RR-008). Resolution: testing infrastructure (GAP-04) is P2; audit trails and observability are P3 (deferred to operational maturity phase). |

**Summary:** All 10 consensus findings show full agreement between pipelines. Three items have minor tensions on scope or timing that are resolved above. Zero fundamental conflicts exist between the PS and NSE analyses.

---

## 4. Open Items Resolution

The following open items (OI-01 through OI-07) were identified by nse-requirements-001. Each is resolved or explicitly deferred with justification.

| ID | Item | Resolution | Status | Justification |
|----|------|------------|--------|---------------|
| **OI-01** | JSON Schema format for agent definition validation | **Resolved: JSON Schema Draft 2020-12** | Closed | Widest tooling support (ajv, jsonschema, VS Code IntelliSense). Compatible with YAML frontmatter parsing via js-yaml or PyYAML. Pydantic is a Python-specific alternative that could generate JSON Schema but adds a Python dependency to what is currently a language-agnostic definition format. Draft 2020-12 is the recommended standard. |
| **OI-02** | Confidence threshold for LLM routing fallback | **Deferred to empirical measurement** | Open | No theoretical basis for selecting a threshold a priori. Recommended approach: implement keyword routing logging first (RR-008, routing observability); collect 100+ routing decisions; empirically determine the false-negative rate; set threshold at the point where keyword accuracy drops below 80%. Deferred until skill count approaches 15 and LLM fallback becomes necessary. |
| **OI-03** | Open Agent Specification adoption | **Resolved: Evaluate for compatible elements, do not adopt wholesale** | Closed | The Open Agent Specification (2025) uses YAML/JSON with schema validation -- directionally aligned with ADR-001 (B5). However, wholesale adoption would require restructuring 37 existing agent definitions and potentially losing Jerry-specific extensions (cognitive mode, guardrails structure, L0/L1/L2 output levels). Recommended: monitor the specification for compatible elements (naming conventions, version format); adopt schema validation patterns; do not adopt the full specification format. |
| **OI-04** | Output schema variability across L0/L1/L2 levels | **Resolved: Base schema with optional level-specific sections** | Closed | Define a base output schema with required sections (navigation table H-23, anchor links H-24, source cross-reference). Add optional L0/L1/L2 sections: stakeholder-facing agents MUST include all three levels (PR-008); internal agents MAY omit L0 if output is consumed only by other agents. Schema validates presence of required sections and, for stakeholder-facing agents, all three levels. |
| **OI-05** | Maximum agent count before team-based grouping | **Resolved: Monitor at 50-agent threshold** | Closed | TS-1 suggests ~50 agents as the practical limit for single-framework cognitive load. Current count is 37 (74% of threshold). Monitor the count as new skills are added. When approaching 45, evaluate: (a) team-based grouping (skill clusters with meta-orchestrators), (b) agent consolidation (merge agents with overlapping roles). R-A02 (agent proliferation) is YELLOW-zone at score 6 -- acceptable with monitoring. |
| **OI-06** | Audit trail storage mechanism | **Resolved: Filesystem first, Memory-Keeper migration path** | Closed | Consistent with Jerry's filesystem-as-memory core philosophy (CX-01). Start with structured audit entries in WORKTRACKER.md and ORCHESTRATION.yaml (already partially implemented via SF-07). If cross-session query needs arise (e.g., "find all routing decisions that used LLM fallback in the last 30 days"), migrate to Memory-Keeper with key pattern `jerry/{project}/audit/{entity-id}`. This follows the MCP-M-001 MEDIUM standard for multi-session reusable findings. |
| **OI-07** | Negative keyword data structure | **Resolved: Extend existing trigger map with "Negative Keywords" column** | Closed | Minimal disruption to existing mandatory-skill-usage.md format. Add a "Negative Keywords" column to the Trigger Map table. Example: `/nasa-se` has trigger keywords `requirements, specification, V&V, technical review, risk` and negative keywords `code risk, risky approach, at risk` to prevent casual mentions from triggering the skill. Implementation effort is LOW; can be applied immediately per GAP-05 Phase A. |

---

## 5. Pattern Maturity Assessment

This section updates the maturity scores from ps-analyst-001 incorporating NSE architecture findings (hexagonal mapping, design patterns, ADRs), NSE requirements (52 shall-statements), and NSE risk assessment (30 risks, 3 RED-zone).

### Maturity Scale

| Level | Name | Characteristics |
|-------|------|-----------------|
| 1 | Ad-hoc | No formal pattern; inconsistent application |
| 2 | Repeatable | Pattern exists but inconsistent; some documentation |
| 3 | Defined | Pattern documented, consistent, and enforced |
| 4 | Managed | Pattern measured, optimized, with feedback loops |
| 5 | Optimizing | Continuous improvement; data-driven evolution |

### Revised Maturity Scores

| Pattern Family | PS Score | Revised Score | Change | Revision Rationale | Target Score | Path to Target |
|---------------|----------|---------------|--------|--------------------|--------------|-----------------
| **Governance** | 4.5 | **4.6** | +0.1 | NSE formalized 52 requirements with 100% traceability (INCOSE 8/8 PASS); 3 ADRs recommended with decision rationale; tier vocabulary validated by risk assessment | 5.0 | Implement rule consolidation (R-P02 mitigation); add rule interaction matrix; data-driven rule sunset criteria |
| **Safety** | 4.3 | **4.3** | 0.0 | NSE validated all 9 safety patterns; T1-T5 tool security tiers formalize SF-03; no new information changed the assessment | 4.8 | Close SF-09 ceiling (iteration cap HARD rule); implement input validation layer for R-S01 |
| **Quality** | 4.2 | **4.3** | +0.1 | NSE Pattern 8 formalizes the 4-layer quality gate architecture; ADR-003 provides decision record for layered QA; 9 QR requirements codify quality expectations | 4.8 | Implement QA-08 schema validation (GAP-01/GAP-02); score stability monitoring (GAP-12) |
| **Workflow** | 3.4 | **3.5** | +0.1 | NSE Pattern 10 formalizes layered routing with architecture specification; ADR-002 documents routing decision with alternatives | 4.0 | Implement negative keywords (GAP-05 Phase A); add routing observability (RR-008) |
| **Context** | 3.5 | **3.6** | +0.1 | NSE Pattern 7 adds quantified context budget allocation (CB-01 through CB-05); memory hierarchy model (context window -> filesystem -> MCP) formalized | 4.2 | Implement context budget monitoring (GAP-06); tool result clearing strategy (CX-12) |
| **Delegation** | 3.0 | **3.1** | +0.1 | NSE Pattern 9 adds cognitive mode formal enumeration and behavioral specifications; Pattern 1 formalizes specialist agent decomposition criteria | 3.8 | Evaluate context-centric decomposition (DL-07); implement contract-first elements via handoff schema (GAP-03) |
| **Integration** | 2.6 | **2.8** | +0.2 | NSE Pattern 6 provides full JSON Schema for structured handoffs (largest gap closure in this family); handoff protocol architecture with send/receive hooks | 3.8 | Implement structured handoff schema (GAP-03); complete hook-based enforcement (IN-05) |
| **Testing** | 2.1 | **2.1** | 0.0 | NSE risk assessment identifies R-T03 (model regression) and R-Q04 (scoring drift) but does not add testing infrastructure. No new information changes the assessment | 3.5 | Implement agent unit testing (GAP-04); add score stability monitoring (GAP-12); behavioral regression baseline |

### Revised Maturity Radar

```
                    Governance (4.6)
                        *
                       / \
                      /   \
            Safety   /     \  Quality
            (4.3)   *       * (4.3)
                   /         \
                  /           \
        Context  *             * Workflow
        (3.6)    |             | (3.5)
                  \           /
                   \         /
       Delegation   *       * Integration
        (3.1)        \     /  (2.8)
                      \   /
                       \ /
                        *
                    Testing (2.1)
```

**Revised Overall Framework Maturity: 3.4 (Defined)** -- up from 3.3 due to NSE formalization of architecture, requirements, and risk assessment.

### Maturity Roadmap

| Phase | Timeframe | Actions | Expected Maturity |
|-------|-----------|---------|-------------------|
| **Phase A: Foundation** | Near-term | GAP-01 (schema validation for definitions), GAP-03 (structured handoff schema), Rule consolidation (H-25 to H-30) | 3.6 (+0.2) |
| **Phase B: Quality** | Mid-term | GAP-02 (schema validation as QA pre-check), GAP-06 (context budget monitoring), GAP-07 (iteration ceiling), GAP-12 (scoring variance) | 3.9 (+0.3) |
| **Phase C: Testing** | Mid-term | GAP-04 (agent unit testing), GAP-10 (drift detection baseline), routing observability (RR-008) | 4.1 (+0.2) |
| **Phase D: Evolution** | Long-term | GAP-05 Phase C (LLM routing fallback), GAP-08 (LLM fallback activation), GAP-09 (capability discovery), GAP-11 (contract-first delegation) | 4.3 (+0.2) |

**Target: Level 4.3 (Managed)** -- achievable through systematic gap closure without architectural rewrites.

---

## 6. Rule Consolidation Recommendation

The rule proliferation risk (R-P02, RED-zone, score 15, net priority 9.00) is the #1 mitigation priority identified by nse-risk-001. At 31/35 HARD rule slots (89%), Jerry is past the 20-25 "sweet spot" identified by the risk assessment's diminishing-returns curve.

### Current State: H-25 through H-30 (Skill Standards Rules)

| Rule | Source File | Content |
|------|------------|---------|
| H-25 | skill-standards | Skill file MUST be exactly `SKILL.md` (case-sensitive) |
| H-26 | skill-standards | Skill folder MUST use kebab-case, match `name` field |
| H-27 | skill-standards | No `README.md` inside skill folder |
| H-28 | skill-standards | Description: WHAT + WHEN + triggers, <1024 chars, no XML |
| H-29 | skill-standards | Full repo-relative paths in SKILL.md |
| H-30 | skill-standards | Register in CLAUDE.md + AGENTS.md (+ mandatory-skill-usage.md if proactive) |

### Proposed Consolidation: 6 Rules -> 2 Compound Rules

**H-25 (revised): Skill Structure Compliance**

The skill definition file, folder, and content MUST comply with all structural standards:
- (a) Skill file MUST be exactly `SKILL.md` (case-sensitive)
- (b) Skill folder MUST use kebab-case matching the `name` field
- (c) No `README.md` inside skill folder
- (d) Description MUST specify WHAT + WHEN + triggers, <1024 chars, no XML
- (e) All paths in SKILL.md MUST be full repo-relative paths

**H-26 (revised): Skill Registration Compliance**

Every skill and agent MUST be registered in the framework:
- (a) Skill registered in CLAUDE.md quick reference table
- (b) All agents registered in AGENTS.md
- (c) If proactive invocation required, skill registered in mandatory-skill-usage.md trigger map

### Impact Assessment

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| HARD rule count | 31 | 27 | -4 (freed slots) |
| Ceiling utilization | 89% | 77% | -12% |
| Available slots | 4 | 8 | +4 |
| L1 token budget | ~12,500 | ~12,100 | -400 (estimated; compound rules are more token-efficient than 6 separate rules) |
| Specificity preserved | Full | Full | No loss (sub-clauses retain all original constraints) |

### Additional Consolidation Candidates

| Candidate | Current Rules | Proposed Compound Rule | Savings |
|-----------|--------------|----------------------|---------|
| Architecture layer compliance | H-07, H-08, H-09 | "Architecture Layer Compliance" with 3 sub-clauses | 2 slots |
| Python environment | H-05, H-06 | "UV-Only Python Environment" with 2 sub-clauses | 1 slot |

**Total potential savings:** 7 slots (from 31 to 24), well within the 20-25 sweet spot.

### New Rule Capacity After Consolidation

With 8 freed slots, Jerry can add the following recommended HARD rules:

| Proposed Rule | Purpose | Source |
|---------------|---------|--------|
| H-32: Maximum iteration ceiling | Max 7 iterations C2/C3, max 10 C4, mandatory human escalation at ceiling | GAP-07, SF-09 gap, R-O02 mitigation |
| (Reserved) | Future security, scaling, or governance needs | R-P02 buffer |

---

## Self-Review (S-010)

### Completeness Verification

| Required Section | Status | Assessment |
|------------------|--------|------------|
| Unified Pattern Taxonomy (all 8 families) | COMPLETE | 66 entries across 8 tables; each with ID, name, Jerry status, problem, solution, requirements, risks |
| NSE pattern reconciliation | COMPLETE | 10 NSE patterns mapped to PS families; zero conflicts |
| Gap Closure Roadmap (GAP-01 through GAP-12) | COMPLETE | All 12 gaps with pattern mapping, requirements, risks, priority, and implementation approach |
| Cross-Pipeline Consensus Matrix | COMPLETE | 10 consensus findings with both-pipeline evidence and tension resolution |
| Open Items Resolution (OI-01 through OI-07) | COMPLETE | 6 resolved/closed, 1 deferred with justification |
| Pattern Maturity Assessment | COMPLETE | 8 families rescored with revision rationale; maturity radar; 4-phase roadmap |
| Rule Consolidation Recommendation | COMPLETE | H-25 through H-30 consolidation proposal; impact assessment; additional candidates |
| Navigation table (H-23) | COMPLETE | Present after frontmatter with anchor links |
| Anchor links (H-24) | COMPLETE | All section references use correct anchor syntax |
| L0 executive summary | COMPLETE | 5 key findings with bottom-line recommendation |
| Source citations | COMPLETE | All claims cite Phase 1 research, Phase 2 analysis, or cross-pollination handoffs |

### Internal Consistency Verification

| Dimension | Check | Result |
|-----------|-------|--------|
| Pattern counts | 8 families sum correctly | 7+9+10+12+9+7+7+5 = 66 entries; 57 unique patterns (9 appear in multiple families per cross-reference) |
| Gap priorities | Consistent with trade study deltas and risk scores | GAP-01/02 (schema validation) = highest delta (+0.45) = P1. GAP-06 (context monitoring) = highest risk score (R-T01=20) = P2. Consistent |
| Maturity scores | Revised scores justified by NSE evidence | All changes are +0.0 to +0.2; largest change (Integration +0.2) justified by NSE Pattern 6 JSON Schema |
| Requirements traceability | All 52 shall-statements referenced | 43 MUST and 9 SHOULD requirements referenced across taxonomy tables and gap roadmap |
| Risk traceability | All 3 RED and key YELLOW risks referenced | R-T01, R-T02, R-P02 (RED) appear in gap roadmap, consensus matrix, and maturity assessment |
| Consensus findings | Both pipelines cited for each of 10 findings | PS and NSE evidence columns completed for all 10 |
| Open items | All 7 addressed | 6 closed with resolution; 1 deferred with justification (OI-02) |
| Rule consolidation | Math verified | 31 - 4 (H-25 to H-30 consolidation savings) = 27. 35 - 27 = 8 available slots. Consistent |

### Confidence Assessment

| Area | Confidence | Basis |
|------|-----------|-------|
| Pattern taxonomy completeness | **High** | 6 Phase 1 research agents surveyed 67+ sources; 3 Phase 2 analysis agents cross-referenced findings; 2 pipelines converged |
| Gap priority ranking | **High** | Trade study deltas, risk scores, and FMEA RPNs all converge on the same top 3 priorities |
| Maturity scores | **Medium** | Scores are analyst judgment against level criteria; a more rigorous assessment would use multiple evaluators and calibration exercises |
| Rule consolidation savings | **High** | Token savings are estimated (~400 tokens) but directionally correct; slot savings are exact (4 freed) |
| Implementation effort estimates | **Medium** | Effort levels (Low/Medium/High) are qualitative; detailed work breakdowns should be developed during ADR phase |
| Cognitive mode enumeration | **Medium** | PR-002 specifies 8 modes; NSE Pattern 9 defines 5. The 8-mode set is adopted but empirical validation across all 37 agents is needed |

### Identified Limitations

1. **Maturity scoring subjectivity.** Scores are assigned by a single synthesizer agent. A more rigorous process would use multiple independent evaluators with calibration.

2. **Industry coverage bounds.** The analysis relies on Phase 1 research sources (67+ sources). Additional patterns may exist in academic literature, proprietary systems, or frameworks not covered by the research agents.

3. **Implementation effort granularity.** The roadmap uses qualitative effort levels (Low/Medium/High). Detailed story-point or time estimates should be developed during the ADR and implementation planning phases.

4. **Testing maturity scoring floor.** Testing (2.1) may be understated because Jerry does have implicit testing through operational use and quality gates. However, the absence of formal testing infrastructure (unit tests, E2E tests, regression baselines) justifies the low score per the maturity model criteria.

5. **Pattern overlap.** 9 patterns appear in multiple families (e.g., criticality-proportional enforcement appears in both Quality and Governance). The taxonomy accepts this overlap as reflecting the genuinely cross-cutting nature of these patterns rather than attempting to force single-family classification.

---

## Source Cross-Reference

All claims in this synthesis trace to the following source documents from the PROJ-007 orchestration pipeline.

### Phase 1 Research (PS Pipeline)

| Source | Content | Location |
|--------|---------|----------|
| ps-researcher-001 | Claude Code agent capabilities, architecture, tool model | `ps/phase-1/ps-researcher-001/` |
| ps-researcher-002 | Agent routing, triggers, handoff protocols, anti-patterns | `ps/phase-1/ps-researcher-002/` |
| ps-researcher-003 | Industry best practices across Anthropic, Google, Microsoft, OpenAI | `ps/phase-1/ps-researcher-003/` |

### Phase 1 Research (NSE Pipeline)

| Source | Content | Location |
|--------|---------|----------|
| nse-explorer-001 | Trade study: 5 dimensions, 27 alternatives, 5 winners | `nse/phase-1/nse-explorer-001/` |

### Phase 2 Analysis (PS Pipeline)

| Source | Content | Location |
|--------|---------|----------|
| ps-analyst-001 | 57 patterns in 8 families; 12 gaps; maturity assessment 3.3/5 | `ps/phase-2-analysis/ps-analyst-001/` |
| ps-analyst-002 | Routing analysis; scaling trajectory; 8 anti-patterns; handoff schema | `ps/phase-2-analysis/ps-analyst-002/` (via ps-to-nse handoff) |
| ps-investigator-001 | FMEA: 28 failure modes; top RPN 392 (context rot); 12 corrective actions | `ps/phase-2-analysis/ps-investigator-001/` (via ps-to-nse handoff) |

### Phase 2 Analysis (NSE Pipeline)

| Source | Content | Location |
|--------|---------|----------|
| nse-requirements-001 | 52 shall-statements; 6 domains; 15 stakeholder needs; INCOSE 8/8 PASS; OI-01 through OI-07 | `nse/phase-2-analysis/nse-requirements-001/` |
| nse-architecture-001 | 10 design patterns; hexagonal mapping; 3 ADRs; T1-T5 tool tiers; CB-01 through CB-05 | `nse/phase-2-analysis/nse-architecture-001/` |
| nse-risk-001 | 30 risks; 3 RED-zone; mitigation priority matrix; rule consolidation analysis | `nse/phase-2-analysis/nse-risk-001/` |

### Cross-Pollination Handoffs

| Source | Content | Location |
|--------|---------|----------|
| Barrier 2: NSE-to-PS | 10 consensus findings; PS Phase 3 guidance; quantitative summary | `cross-pollination/barrier-2/nse-to-ps/handoff.md` |
| Barrier 2: PS-to-NSE | 57 patterns; 12 gaps; routing analysis; FMEA; NSE Phase 3 guidance | `cross-pollination/barrier-2/ps-to-nse/handoff.md` |

---

*Synthesis completed: 2026-02-21 | Agent: ps-synthesizer-001 | PS-ID: PROJ-007 | Entry: e-004*
*Input artifacts: 4 Phase 1 research reports, 6 Phase 2 analysis reports, 2 cross-pollination handoffs*
*Criticality: C4 -- Definitive pattern catalog*
*Self-review (S-010): COMPLETE -- 11 completeness checks passed, 6 consistency checks passed, 6 confidence assessments documented, 5 limitations identified*
