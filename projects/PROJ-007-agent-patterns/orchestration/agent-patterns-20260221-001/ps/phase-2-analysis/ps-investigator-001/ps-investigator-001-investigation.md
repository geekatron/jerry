# PS-Investigator-001: Agent Failure Mode Investigation

<!-- PS-ID: PROJ-007 | ENTRY: e-004 | AGENT: ps-investigator-001 | DATE: 2026-02-21 -->

> Comprehensive failure mode investigation of Claude Code agent systems. Covers FMEA, root cause analysis (5 Whys, Ishikawa), anti-pattern catalog, Jerry-specific vulnerability assessment, and corrective action plan.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | ELI5 overview of investigation findings |
| [L1: Detailed Investigation](#l1-detailed-investigation) | Full FMEA, root cause analysis, Ishikawa diagrams |
| [1. FMEA Table](#1-failure-mode-and-effects-analysis-fmea) | Systematic failure mode catalog with RPN scoring |
| [2. Root Cause Analysis](#2-root-cause-analysis-5-whys) | 5 Whys for top 5 highest-RPN failure modes |
| [3. Ishikawa Diagrams](#3-ishikawa-diagram-analysis) | Fishbone diagrams for top 3 failure modes |
| [4. Anti-Pattern Catalog](#4-anti-pattern-catalog) | Comprehensive catalog from Phase 1 research |
| [L2: Jerry-Specific Assessment](#l2-jerry-specific-assessment) | Vulnerability mapping to Jerry architecture |
| [5. Jerry Vulnerability Assessment](#5-jerry-specific-vulnerability-assessment) | Protected vs. exposed failure modes |
| [6. Corrective Action Plan](#6-corrective-action-plan) | Prioritized fixes with verification methods |
| [Source Traceability](#source-traceability) | All findings traced to Phase 1 research |
| [Self-Review (S-010)](#self-review-s-010) | Pre-delivery quality check |

---

## L0: Executive Summary

This investigation identifies **28 distinct failure modes** across 7 categories in Claude Code agent systems, scored using Failure Mode and Effects Analysis (FMEA) with Risk Priority Numbers (RPN). The top 5 highest-risk failure modes are: (1) context rot causing instruction-following degradation (RPN 392), (2) free-text handoff information loss (RPN 336), (3) prompt drift eroding agent persona fidelity (RPN 288), (4) quality gate false positive scoring (RPN 280), and (5) routing loops without circuit breakers (RPN 252).

Jerry's existing architecture provides strong protection against several critical failure modes through its H-01 single-level constraint (preventing recursive agent cascades), H-14 creator-critic-revision cycle (preventing unreviewed output), and L1-L5 enforcement architecture (providing layered defense against context rot). However, the investigation identifies **9 failure modes where Jerry is currently exposed**, with the most significant being: lack of maximum iteration caps on revision cycles, absence of structured handoff schemas (relying on implicit file-based context passing), no deterministic enforcement of routing rules via hooks (relying on prompt-level instruction following), and vulnerability to quality gate bypass through critic-creator collusion.

The corrective action plan proposes 12 specific interventions organized by priority: 4 immediate actions (implementable within current PROJ-007 scope), 5 root-cause structural fixes (requiring new rules or guides), and 3 prevention mechanisms (requiring hook-based enforcement or tooling). Each intervention includes a verification method. The investigation draws on evidence from all three Phase 1 researchers, the NSE cross-pollination handoff, and Jerry's existing rule corpus.

---

## L1: Detailed Investigation

### 1. Failure Mode and Effects Analysis (FMEA)

#### FMEA Scoring Criteria

| Factor | 1-3 (Low) | 4-6 (Medium) | 7-10 (High) |
|--------|-----------|--------------|-------------|
| **Severity** | Minor quality degradation; easily caught | Moderate quality impact; rework required | Critical failure; wrong output; data loss |
| **Occurrence** | Rare; requires unusual conditions | Occasional; happens in normal operation | Frequent; expected in most sessions |
| **Detection** | Always caught by existing mechanisms | Sometimes caught; depends on context fill | Rarely caught; silent failure mode |

**RPN = Severity x Occurrence x Detection** (Range: 1-1000; Higher = more critical)

---

#### 1.1 Context Failures

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Root Cause | Mitigation |
|----|-------------|----------|------------|-----------|-----|------------|------------|
| CF-01 | **Context rot** -- instruction-following degrades as context fills beyond ~60% capacity | 8 | 7 | 7 | **392** | Transformer attention requires n-squared pairwise relationships; signal-to-noise ratio decreases as irrelevant context accumulates [R1-F5.3, R3-RQ7] | L2 re-injection of critical rules; subagent isolation for verbose operations; compaction at phase boundaries |
| CF-02 | **Context overflow** -- auto-compaction triggers at ~95% capacity, losing conversation nuance | 7 | 5 | 5 | 175 | Long sessions with extensive tool output fill context window faster than useful work progresses [R1-F5.3] | MCP-002 phase boundary persistence; subagent delegation for high-output tasks; session segmentation |
| CF-03 | **Stale context** -- agent operates on outdated information after file modifications by other agents | 6 | 6 | 6 | 216 | Parallel agents modifying shared files without synchronization; subagent context does not reflect main session changes [R1-F4.1] | File-based coordination with explicit re-read instructions; git worktree isolation for parallel work [R1-F4.2] |
| CF-04 | **Context pollution** -- irrelevant tool output consumes context budget, displacing useful information | 7 | 7 | 4 | 196 | Large tool outputs (test results, file listings, search results) not filtered before entering context [R1-F4.1, R3-RQ7] | Subagent isolation for verbose operations; result truncation; observation masking [R3-RQ7] |

---

#### 1.2 Routing Failures

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Root Cause | Mitigation |
|----|-------------|----------|------------|-----------|-----|------------|------------|
| RF-01 | **Misrouting** -- request sent to wrong agent/skill, producing irrelevant output | 6 | 5 | 5 | 150 | Keyword overlap between skills (e.g., "analyze" triggers both /problem-solving and /nasa-se); semantic variations not captured [R2-F4.2, R2-F8.4] | Negative keywords; priority ordering; compound trigger requirements [R2-F4.2] |
| RF-02 | **No-route (under-routing)** -- request matches no trigger, handled by generalist without specialist benefit | 5 | 4 | 6 | 120 | Trigger map has finite keyword coverage; semantic variations not in keyword list; novel request types [R2-F8.4] | Semantic similarity layer (L3); LLM fallback router (L4) [R2-L2-R1]; periodic trigger map review |
| RF-03 | **Multi-route ambiguity** -- request matches multiple skills with no resolution mechanism | 5 | 4 | 5 | 100 | No priority ranking between skills; no negative keywords for disambiguation [R2-F5.1] | Priority ordering; confidence scoring; H-31 clarification fallback [R2-L2-R3] |
| RF-04 | **Routing loops** -- agents hand off to each other without convergence | 8 | 4 | 8 | **252** | No circuit breaker or maximum handoff count; unclear acceptance criteria for iterative patterns [R2-F8.3] | Maximum iteration caps; circuit breaker after N no-improvement cycles; mandatory human escalation [R2-L2-R4] |

---

#### 1.3 Prompt Failures

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Root Cause | Mitigation |
|----|-------------|----------|------------|-----------|-----|------------|------------|
| PF-01 | **Prompt drift** -- agent persona and instructions erode as context fills; behavior diverges from system prompt | 8 | 6 | 6 | **288** | System prompt influence decreases relative to accumulated conversation context; recency bias in attention [R1-F6.1, R3-RQ7] | L2 re-injection (immune to context rot); subagent spawning for long tasks; session segmentation |
| PF-02 | **Persona bleed** -- agent adopts characteristics from context rather than its defined persona | 5 | 4 | 7 | 140 | Subagent receives conversation context that includes other personas; cross-contamination from handoff data [R1-F4.1] | Strict context isolation (subagent receives only system prompt + environment); explicit persona reminders |
| PF-03 | **Instruction-following degradation** -- complex multi-rule constraints are partially followed or selectively ignored | 7 | 6 | 5 | 210 | Rule count exceeds practical compliance capacity; competing rules create cognitive load; no deterministic enforcement [R1-F5.4] | Reduce rule count per agent; deterministic L3 enforcement via hooks; prioritize rules by severity |
| PF-04 | **Over-prescriptive prompting** -- excessively detailed prompts that constrain agent reasoning capability | 4 | 3 | 4 | 48 | Well-intentioned attempts to control agent behavior through exhaustive instructions backfire by reducing model flexibility [R3-RQ4, R1-F7.1] | "Right Altitude" principle; balance specificity with flexibility; test prompt effectiveness empirically [R3-RQ7] |

---

#### 1.4 Tool Failures

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Root Cause | Mitigation |
|----|-------------|----------|------------|-----------|-----|------------|------------|
| TF-01 | **Tool misuse** -- agent selects wrong tool for task (e.g., Write instead of Edit, Bash instead of Grep) | 5 | 5 | 4 | 100 | Tool descriptions insufficiently distinct; tool overlap not addressed; no poka-yoke design [R1-F7.2, R3-RQ5] | Improve tool descriptions; restrict tool access per agent; use PreToolUse hooks for validation [R1-F2.2] |
| TF-02 | **Tool unavailability** -- MCP server fails or background agent cannot access MCP tools | 6 | 3 | 3 | 54 | Background subagents cannot use MCP tools; MCP server timeout or unavailability [R1-F5.2, MCP error handling] | MCP fallback to `work/.mcp-fallback/`; foreground-only for MCP-dependent agents [R1-F5.2] |
| TF-03 | **Tool result misinterpretation** -- agent misinterprets tool output, leading to incorrect conclusions | 6 | 4 | 7 | 168 | Tool output format ambiguous; large outputs overwhelm agent reasoning; source quality bias [R1-F5.4] | Structured tool output formats; result validation; source quality heuristics [R1-F5.4] |
| TF-04 | **Tool proliferation** -- agent has access to too many tools (20+), causing selection accuracy degradation | 5 | 3 | 5 | 75 | Skill/tool count growth without corresponding access restriction; all tools available by default [R2-F8.4, R3-RQ5] | Per-agent tool allowlists; contextual function selection for top-N relevant tools [R2-L2-R6] |

---

#### 1.5 Quality Failures

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Root Cause | Mitigation |
|----|-------------|----------|------------|-----------|-----|------------|------------|
| QF-01 | **Quality gate bypass** -- deliverable presented to user without required quality scoring | 7 | 4 | 5 | 140 | No deterministic enforcement of H-17 quality scoring requirement; relies on prompt-level instruction following [QE H-17] | PreToolUse hook blocking output without score; L3 deterministic gating [QE L3] |
| QF-02 | **False positive scoring** -- critic/scorer assigns passing score to substandard deliverable (leniency bias) | 8 | 5 | 7 | **280** | LLM-as-Judge inherent leniency bias; same-model self-evaluation; insufficient rubric specificity [QE S-014, R3-RQ6] | Strict rubric enforcement; anti-leniency instructions in scorer prompt; multi-dimension scoring with per-dimension thresholds [QE S-014] |
| QF-03 | **Critic-creator collusion** -- critic and creator are same model instance, producing superficial critique cycles | 6 | 5 | 7 | 210 | Single-model critique inherently limited in adversarial capability; critic may share creator's blind spots [R3-RQ6] | S-003 steelman before S-002 devil's advocate (H-16); tournament mode for C4; structured critique templates [QE strategy catalog] |
| QF-04 | **Score inflation across iterations** -- scores monotonically increase without proportional quality improvement | 5 | 4 | 6 | 120 | Each iteration adds context confirming "improvement"; no independent baseline re-evaluation; anchoring bias [QE S-014] | Fresh scorer context per iteration; comparison against original baseline; dimension-level regression detection |

---

#### 1.6 Handoff Failures

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Root Cause | Mitigation |
|----|-------------|----------|------------|-----------|-----|------------|------------|
| HF-01 | **Free-text information loss** -- critical details lost during agent-to-agent handoff through summarization | 8 | 7 | 6 | **336** | Handoffs rely on implicit context passing through files and summaries; no structured schema; summarization drops critical details [R2-F6.2, NSE handoff guidance] | Structured handoff schemas (JSON); explicit required fields; handoff validation [R2-L2-R2] |
| HF-02 | **Format mismatch** -- receiving agent cannot parse or use output format of sending agent | 5 | 3 | 3 | 45 | No standardized inter-agent output format; agents produce varied markdown structures [AGENTS.md handoff protocol] | Standardized output templates per agent type; schema validation for handoff payloads [NSE TS-2, TS-4] |
| HF-03 | **State corruption** -- shared state (files, worktracker) modified concurrently by parallel agents | 7 | 3 | 6 | 126 | Parallel write operations without coordination; git merge conflicts from simultaneous file edits [R1-F9.1] | Git worktree isolation; file ownership boundaries per agent; serialized write access to shared state files |
| HF-04 | **Telephone game degradation** -- information fidelity degrades through serial multi-agent handoffs | 7 | 5 | 7 | 245 | Problem-centric decomposition (split by work type) forces serial handoffs through multiple agents; each summarization step loses resolution [R2-F8.2] | Context-centric decomposition (split by context boundary); minimize handoff chain length; file-based artifact passing [R2-L2-R5] |

---

#### 1.7 Orchestration Failures

| ID | Failure Mode | Severity | Occurrence | Detection | RPN | Root Cause | Mitigation |
|----|-------------|----------|------------|-----------|-----|------------|------------|
| OF-01 | **Cascade failure** -- one agent failure propagates through dependent agents in pipeline | 7 | 4 | 5 | 140 | Sequential pipeline without error isolation; downstream agents operate on corrupted upstream output [R2-F9.1, R3-RQ1] | Quality gates between pipeline stages; error isolation with fallback; circuit breakers [R2-L2-R4] |
| OF-02 | **Agent starvation** -- orchestrator spawns maximum concurrent agents (7), blocking new agent creation | 4 | 2 | 3 | 24 | Orchestration plan spawns too many parallel agents; no backpressure mechanism [R1-F9.1] | Respect 7-agent concurrency limit in orchestration planning; batch parallel work within limit |
| OF-03 | **Bag of Agents** -- multiple agents without formal coordination topology amplify errors 17x | 9 | 2 | 8 | 144 | Agents connected without hierarchy, gatekeeper, or compartmentalized information flow; error amplification across interactions [R2-F8.1] | H-01 single-level constraint; explicit coordination topology in AGENTS.md; gated handoffs [R2-F8.1] |
| OF-04 | **Premature specialization** -- creating separate agents when single agent with tools suffices | 4 | 3 | 4 | 48 | Over-engineering agent decomposition; specialization overhead exceeds benefit for simple tasks [R2-F8.4, R3-RQ1] | Complexity-first decision framework; start simple, add agents when measurement shows benefit [R3-L2] |

---

#### FMEA Summary -- Top 10 by RPN

| Rank | ID | Failure Mode | RPN | Category |
|------|-----|-------------|-----|----------|
| 1 | CF-01 | Context rot (instruction-following degradation) | 392 | Context |
| 2 | HF-01 | Free-text handoff information loss | 336 | Handoff |
| 3 | PF-01 | Prompt drift (persona erosion) | 288 | Prompt |
| 4 | QF-02 | Quality gate false positive scoring | 280 | Quality |
| 5 | RF-04 | Routing loops without circuit breakers | 252 | Routing |
| 6 | HF-04 | Telephone game degradation | 245 | Handoff |
| 7 | CF-03 | Stale context from parallel agents | 216 | Context |
| 8 | PF-03 | Instruction-following degradation | 210 | Prompt |
| 9 | QF-03 | Critic-creator collusion | 210 | Quality |
| 10 | CF-04 | Context pollution from tool output | 196 | Context |

---

### 2. Root Cause Analysis (5 Whys)

#### 2.1 RCA-01: Context Rot (CF-01, RPN 392)

**Symptom:** Agent stops following system prompt rules after extended operation; quality of output degrades progressively through a session.

| Level | Why? | Finding |
|-------|------|---------|
| Why 1 | Why does agent behavior degrade during long sessions? | The system prompt's influence is diluted by accumulated conversation context. The model exhibits recency bias -- recent tokens receive proportionally more attention weight than earlier tokens. |
| Why 2 | Why does accumulated context dilute the system prompt? | Transformer attention operates over all n tokens with n-squared pairwise comparisons. As context grows, each token (including system prompt tokens) receives a smaller fraction of total attention budget. Signal-to-noise ratio decreases. |
| Why 3 | Why does context grow to problematic levels? | Tool outputs (test results, file contents, search results) generate large volumes of tokens that persist in context. Each agent interaction adds both the request and the full response. There is no selective eviction of low-value tokens. |
| Why 4 | Why are low-value tokens not evicted? | Claude Code's compaction mechanism is a blunt instrument -- it triggers at ~95% capacity and summarizes the entire conversation. There is no priority-based retention that preserves high-value tokens (rules, decisions) while discarding low-value tokens (verbose tool output). |
| Why 5 | Why is there no priority-based token retention? | Context management is a platform-level concern (handled by Claude Code's auto-compaction), not an application-level concern (controlled by the framework). The framework cannot control which tokens the model attends to or which are evicted during compaction. |

**Systemic Root Cause:** Context rot is an inherent property of transformer-based language models operating in long sessions. It cannot be eliminated, only mitigated through architectural patterns.

**Structural Fix:** Multi-layer defense combining: (a) L2 re-injection of critical rules at every prompt (immune to context rot), (b) subagent isolation to keep verbose operations out of main context, (c) proactive session segmentation before context fill exceeds ~60%, (d) filesystem-as-memory to externalize state and reload selectively.

**Evidence:** [R1-F5.3] compounding error risk, [R3-RQ7] Anthropic context engineering guide, [R1-F3.2] session persistence.

---

#### 2.2 RCA-02: Free-Text Handoff Information Loss (HF-01, RPN 336)

**Symptom:** Agent B produces lower-quality output than expected because it lacks critical context that Agent A had when generating the handoff.

| Level | Why? | Finding |
|-------|------|---------|
| Why 1 | Why does Agent B lack critical context? | The handoff from Agent A is a free-text summary that omits details Agent A considered important but did not explicitly include in the summary. |
| Why 2 | Why does the summary omit important details? | Summarization is a lossy operation. The model must decide what to include and exclude, and it lacks explicit guidance on which fields are required for the downstream agent's task. |
| Why 3 | Why is there no explicit guidance on required handoff fields? | Inter-agent handoffs are treated as informal communication rather than structured API contracts. There is no handoff schema that mandates specific fields (task, context, constraints, success criteria). |
| Why 4 | Why are handoffs not treated as API contracts? | The framework's handoff protocol (AGENTS.md) defines a JSON structure conceptually but does not enforce it. There is no validation step that checks whether a handoff payload contains all required fields before the receiving agent begins work. |
| Why 5 | Why is there no handoff validation? | Handoff validation requires a deterministic gating mechanism (L3 layer) that inspects the handoff payload structure. This enforcement layer is defined architecturally (L3 in quality-enforcement.md) but not yet implemented for handoff payloads. |

**Systemic Root Cause:** Inter-agent handoffs are treated as informal communication rather than structured, validated API contracts.

**Structural Fix:** (a) Define mandatory handoff schemas per agent-pair or agent-role with required fields (task, context.files, context.prior_findings, success_criteria, criticality, constraints), (b) implement schema validation in PreToolUse hook for Task tool calls, (c) write handoff payloads to filesystem as structured artifacts for auditability.

**Evidence:** [R2-F6.2] "Free-text handoffs are the main source of context loss" (Google, 2026), [NSE handoff guidance] schema validation as high-priority enhancement, [AGENTS.md] existing conceptual handoff protocol.

---

#### 2.3 RCA-03: Prompt Drift (PF-01, RPN 288)

**Symptom:** Agent gradually abandons its defined persona and behavioral constraints, producing output that would be inconsistent with its system prompt if evaluated in isolation.

| Level | Why? | Finding |
|-------|------|---------|
| Why 1 | Why does the agent abandon its persona? | As conversation progresses, the model's behavior is increasingly influenced by the pattern of recent interactions rather than the initial system prompt. |
| Why 2 | Why do recent interactions override the system prompt? | The system prompt is a fixed set of tokens at the beginning of the context. As the context grows, these tokens represent a decreasing fraction of the total input. The model's effective "operating instructions" shift toward the most recent and most frequently reinforced patterns. |
| Why 3 | Why is the system prompt not periodically reinforced? | In the current architecture, the system prompt is set once at agent creation. Subagents receive their system prompt from the markdown body of their definition file (Finding 6.1, R1). There is no mechanism to re-inject persona instructions mid-conversation. |
| Why 4 | Why is there no mid-conversation persona reinforcement? | Subagent contexts are isolated and short-lived (completing a single task), which mitigates drift. The main conversation context, however, persists across multiple tasks and has no persona re-injection mechanism at the application level. |
| Why 5 | Why does the main conversation lack persona re-injection? | The main conversation is the orchestrator, and its persona is defined by CLAUDE.md plus .claude/rules/. The L2 re-injection mechanism addresses critical rules but does not cover the full persona/behavioral profile. The re-injection budget is limited (~600 tokens/prompt) to avoid context bloat. |

**Systemic Root Cause:** Persona fidelity is a function of system prompt token fraction relative to total context. As context grows, persona influence diminishes. Re-injection addresses critical rules but not the full behavioral profile.

**Structural Fix:** (a) Keep subagent tasks focused and short-lived (limiting context accumulation), (b) increase L2 re-injection coverage for behavioral constraints (not just HARD rules), (c) implement session segmentation (start fresh subagent when context exceeds threshold), (d) use evaluation-based drift detection (compare output against persona criteria periodically).

**Evidence:** [R1-F6.1] system prompt mechanism, [R3-RQ4] persona prompting research, [QE] L2 enforcement layer design.

---

#### 2.4 RCA-04: Quality Gate False Positive Scoring (QF-02, RPN 280)

**Symptom:** The quality scorer (adv-scorer / ps-critic) assigns a passing score (>= 0.92) to a deliverable that objectively does not meet quality standards, allowing a substandard deliverable to pass the quality gate.

| Level | Why? | Finding |
|-------|------|---------|
| Why 1 | Why does the scorer assign a passing score to a substandard deliverable? | LLM-as-Judge exhibits inherent leniency bias. Models tend to rate generously, especially when evaluating text produced by the same model family. |
| Why 2 | Why is leniency bias not counteracted? | The scoring rubric (S-014) defines 6 dimensions with weights, but the per-dimension scoring criteria may not be sufficiently granular to force the model to identify specific deficiencies. A vague rubric enables vague (generous) scoring. |
| Why 3 | Why are per-dimension criteria not more granular? | Rubric design must balance between over-specification (which constrains the scorer's ability to evaluate novel content) and under-specification (which enables leniency). The current rubric optimizes for generality across deliverable types at the cost of specificity. |
| Why 4 | Why is there no independent validation of scores? | Quality scoring is a single-pass operation: the scorer evaluates, assigns a score, and the system accepts it. There is no meta-evaluation step that checks whether the score is calibrated against known-quality examples. |
| Why 5 | Why is there no score calibration mechanism? | Score calibration requires a reference corpus of pre-scored deliverables (ground truth) that the system can use to detect scorer drift. Building and maintaining this corpus is a significant effort that has not been prioritized. |

**Systemic Root Cause:** LLM-as-Judge scoring without calibration or independent validation is susceptible to systematic leniency bias, especially when evaluator and creator share the same model architecture.

**Structural Fix:** (a) Add explicit anti-leniency instructions to scorer prompts ("Your default tendency is to score too high; actively look for deficiencies"), (b) require per-dimension justification with specific evidence citations, (c) implement calibration checks against reference-scored examples, (d) fresh scorer context for each evaluation (preventing anchoring to prior scores).

**Evidence:** [QE S-014] LLM-as-Judge strategy, [R3-RQ6] quality assurance patterns, [R2-F9.2] verification subagent superficial testing risk.

---

#### 2.5 RCA-05: Routing Loops (RF-04, RPN 252)

**Symptom:** Agent A routes a task to Agent B, which routes it back to Agent A (or through a chain that returns to A), consuming tokens and time without producing useful output.

| Level | Why? | Finding |
|-------|------|---------|
| Why 1 | Why do agents route tasks back to each other? | Each agent determines that the task is better suited for the other agent based on its own evaluation of the task description. Neither agent recognizes that the other has already declined or deferred the task. |
| Why 2 | Why does neither agent recognize the prior routing history? | Routing decisions are made independently by each agent based on its current context. Routing history (which agents have already handled this task) is not passed as part of the handoff metadata. |
| Why 3 | Why is routing history not included in handoff metadata? | The handoff protocol (AGENTS.md) does not define a routing history field. Each handoff is treated as a fresh delegation rather than a step in a routing chain. |
| Why 4 | Why is there no maximum routing depth or circuit breaker? | The framework defines minimum iteration counts (H-14: 3 for creator-critic) but not maximum iteration counts. There is no architectural mechanism to detect and break routing loops. |
| Why 5 | Why was maximum routing depth not implemented? | The primary concern during framework design was ensuring sufficient quality iteration (preventing premature termination), not preventing excessive iteration. The failure mode of "too many iterations" was not prioritized relative to the failure mode of "too few iterations." |

**Systemic Root Cause:** The framework enforces minimum iteration bounds but lacks maximum bounds and routing loop detection.

**Structural Fix:** (a) Add maximum iteration caps per criticality level (5 for C2, 7 for C3, 10 for C4), (b) include routing history in handoff metadata, (c) implement circuit breaker: halt after 3 consecutive "no improvement" iterations, (d) mandatory human escalation when circuit breaker triggers (aligned with AE-006).

**Evidence:** [R2-F8.3] routing loop anti-pattern, [R2-L2-R4] routing loop prevention recommendation, [QE H-14] minimum iteration count.

---

### 3. Ishikawa Diagram Analysis

#### 3.1 Ishikawa: Context Rot (CF-01)

```
                            CONTEXT ROT
                                |
    ============================================================
    |           |           |           |           |           |
  METHOD     MACHINE     MATERIAL   MEASUREMENT  MANPOWER    MOTHER
  (Process)  (LLM)       (Context)  (Metrics)    (Prompts)   NATURE
    |           |           |           |           |           |
    |           |           |           |           |           |
  No proactive  Transformer  Verbose     No context   System     Stochastic
  session       attention    tool        fill %       prompt     attention
  segmentation  n-squared    outputs     monitoring   fixed at   patterns
    |           scaling       |           |           session     |
    |           |           Large file   No per-      start      Non-
  Sequential   Recency      reads not    dimension    |          deterministic
  task          bias in      isolated     quality     L2 budget  compaction
  processing    long         via sub-     tracking    limited    behavior
    |          contexts     agents       at fill      (~600       |
    |           |           |           levels       tokens)    Auto-compact
  No phase     200K token   Search       |           |          timing
  boundary     hard limit   results      No early    No mid-    unpredictable
  checkpointing|           not          warning      session     |
    |          No priority  truncated   system       persona    Model
  Missing      token         |                      refresh     version
  effort       retention    Conversation              |         differences
  scaling      mechanism    history                  Rule count  in rot
  guidelines                 accumulation             exceeds    susceptibility
                             unchecked                practical
                                                      limit
```

**Key Contributing Factors:**

- **Method:** No proactive session segmentation; sequential processing fills context linearly; no effort scaling to match task complexity with context budget.
- **Machine (LLM):** Transformer attention scales quadratically; inherent recency bias; 200K token hard limit; no user-controllable priority retention.
- **Material (Context):** Verbose tool outputs; large file reads; search results all enter context without filtering; conversation history accumulates indefinitely until compaction.
- **Measurement:** No monitoring of context fill percentage; no quality tracking at different fill levels; no early warning system for degradation.
- **Manpower (Prompts):** System prompt is fixed at session start; L2 re-injection budget is small; rule count may exceed practical compliance capacity.
- **Mother Nature (Stochasticity):** Attention patterns are non-deterministic; compaction timing is unpredictable; different model versions may have different rot susceptibility.

---

#### 3.2 Ishikawa: Free-Text Handoff Information Loss (HF-01)

```
                    HANDOFF INFORMATION LOSS
                                |
    ============================================================
    |           |           |           |           |           |
  METHOD     MACHINE     MATERIAL   MEASUREMENT  MANPOWER    MOTHER
  (Process)  (LLM)       (Context)  (Metrics)    (Prompts)   NATURE
    |           |           |           |           |           |
    |           |           |           |           |           |
  No structured Summarization Heterogeneous No handoff  Agent       Variable
  handoff      is inherently agent output  quality    prompts     summarization
  schema       lossy        formats      metrics    don't       quality
    |           |           |           |          specify      across
    |          Model cannot  No schema   No         required    invocations
  No handoff   predict      validation   comparison handoff      |
  validation   what the     for payloads of pre/    fields     Non-
  step         receiver       |         post-       |          deterministic
    |          needs        Mixed       handoff    No explicit  detail
    |           |          markdown/    output     "what NOT    selection
  Problem-     Information  JSON/text   quality    to omit"     during
  centric      triage       in handoff   |         instructions summarization
  decomposition is implicit, data       No first-    |           |
  forces        not explicit  |         contact    Handoff     Context
  serial        |          Critical    resolution  protocol    sensitivity
  handoffs     Context not  metadata   rate        in AGENTS.md of LLM
    |          scoped to    not         tracking   is conceptual, determines
  Too many     receiver's   distinguished           not enforced which details
  handoff      needs        from verbose                        are preserved
  steps                     output
```

**Key Contributing Factors:**

- **Method:** No structured schema; no validation; problem-centric decomposition creates long handoff chains.
- **Machine (LLM):** Summarization is inherently lossy; model cannot predict what receiver needs; information triage is implicit.
- **Material (Context):** Heterogeneous output formats; no distinction between critical metadata and verbose output; mixed data types.
- **Measurement:** No handoff quality metrics; no pre/post-handoff quality comparison; no first-contact resolution tracking.
- **Manpower (Prompts):** Agent prompts lack specific handoff field requirements; handoff protocol is conceptual, not enforced.
- **Mother Nature (Stochasticity):** Summarization quality varies non-deterministically; context sensitivity determines which details survive.

---

#### 3.3 Ishikawa: Quality Gate False Positive Scoring (QF-02)

```
                    FALSE POSITIVE SCORING
                                |
    ============================================================
    |           |           |           |           |           |
  METHOD     MACHINE     MATERIAL   MEASUREMENT  MANPOWER    MOTHER
  (Process)  (LLM)       (Context)  (Metrics)    (Prompts)   NATURE
    |           |           |           |           |           |
    |           |           |           |           |           |
  Single-pass  Inherent    Creator and  No score   Rubric      Stochastic
  scoring      leniency    scorer share calibration insufficiently scoring
  without      bias in     same model   corpus     specific    variance
  validation   LLM-as-     architecture  |           |           |
    |          Judge        |          No meta-    No anti-    Scores
    |           |          Scorer has  evaluation  leniency    fluctuate
  No calibra-  Same-model  context of  of scorer   instructions across
  tion against self-eval   creation    accuracy    in scorer   invocations
  reference    less        process      |          prompt       |
  corpus       adversarial  (anchoring) No per-      |         Temperature
    |          than cross-   |         dimension  No explicit  and sampling
    |          model        Prior      threshold   evidence    affect
  No inde-      |          scores      enforcement requirement scoring
  pendent      Anchoring   in context   |         for each     consistency
  score        bias from   influence   Composite   dimension    |
  validation   recent      next score  score masks  score      Model
    |          context       |         weak         |          version
  Monotonic     |          Score       dimensions  Creator-    updates
  scoring      Confirmation inflation   |         critic same  change
  assumption   bias in     over        No score   model bias   calibration
  (each        iteration   iterations  regression              baseline
  revision      cycles                 detection
  must improve)
```

**Key Contributing Factors:**

- **Method:** Single-pass scoring; no calibration; no independent validation; assumption that each revision improves.
- **Machine (LLM):** Leniency bias; same-model self-evaluation; anchoring bias; confirmation bias.
- **Material (Context):** Shared model architecture between creator and scorer; prior scores in context influencing subsequent scores; creation process context creating anchoring.
- **Measurement:** No calibration corpus; no meta-evaluation; composite score masks weak dimensions; no regression detection.
- **Manpower (Prompts):** Rubric insufficiently specific; no anti-leniency instructions; no per-dimension evidence requirements.
- **Mother Nature (Stochasticity):** Score variance across invocations; temperature affects consistency; model version changes affect calibration.

---

### 4. Anti-Pattern Catalog

#### AP-01: Bag of Agents

| Attribute | Detail |
|-----------|--------|
| **Name** | Bag of Agents |
| **Description** | Multiple agents assembled without formal coordination topology. Every agent has an open line to every other agent. No hierarchy, gatekeeper, or compartmentalized information flow. |
| **Symptoms** | Error amplification (17x in Google DeepMind research); unpredictable agent interactions; agents undoing each other's work; excessive token consumption with diminishing returns. |
| **Root Cause** | Focus on adding agents for capability without designing the coordination topology. System robustness depends on *how* agents are arranged, not *how many* exist. |
| **Consequences** | 17x error amplification across agent interactions; unpredictable failure modes; debugging becomes intractable; cost escalation. |
| **Prevention Rule** | Every multi-agent system MUST have a defined coordination topology (hierarchical, sequential, parallel, or hybrid). Each agent MUST have a defined role in the topology with explicit input/output boundaries. |
| **Jerry Applicability** | **PROTECTED.** Jerry's H-01 constraint (max 1 level: orchestrator -> worker) and explicit agent registry (AGENTS.md) prevent the bag-of-agents topology. The skill-based grouping provides compartmentalized information flow. |

---

#### AP-02: Telephone Game

| Attribute | Detail |
|-----------|--------|
| **Name** | Telephone Game |
| **Description** | Information degrades through serial agent handoffs. Each summarization step drops critical details. Context loses fidelity with each transfer. |
| **Symptoms** | Agent output quality degrades as handoff chain length increases; final output omits critical details from early-chain agents; more tokens spent on coordination than actual work. |
| **Root Cause** | Problem-centric decomposition (splitting by work type: code, tests, review) forces serial handoffs through multiple agents. Each agent summarizes, losing resolution. |
| **Consequences** | Output quality inversely proportional to handoff chain length; critical context lost; rework required when downstream agents make incorrect assumptions. |
| **Prevention Rule** | PREFER context-centric decomposition (split by context boundary, not work type). An agent handling a feature SHOULD also handle its tests. Minimize handoff chain length. Use file-based artifact passing for complex data. |
| **Jerry Applicability** | **PARTIALLY EXPOSED.** Jerry's orchestration model can create multi-step handoff chains (researcher -> analyst -> synthesizer). The file-based artifact approach mitigates but does not eliminate the problem. Structured handoff schemas (not yet implemented) would further reduce information loss. |

---

#### AP-03: Over-Routing

| Attribute | Detail |
|-----------|--------|
| **Name** | Over-Routing |
| **Description** | Routing to specialized agents for tasks they do not meaningfully improve. Adding agents that do not provide meaningful specialization beyond what the orchestrator could handle directly. |
| **Symptoms** | High agent invocation count with low value-add; coordination overhead exceeds specialization benefit; simple tasks taking disproportionately long; excessive token usage. |
| **Root Cause** | Indiscriminate application of agent specialization without measuring whether the specialist produces better output than the generalist for the specific task. |
| **Consequences** | Token waste; latency increase; coordination overhead; system complexity without proportional quality improvement. |
| **Prevention Rule** | APPLY the complexity-first decision framework: start with simplest solution, add agents only when measurement shows improvement. Direct model calls should be used for single-step tasks; single agent with tools for within-domain tasks; multi-agent only for cross-domain or parallel specialization. |
| **Jerry Applicability** | **PARTIALLY EXPOSED.** Jerry's H-22 mandates proactive skill invocation based on keyword triggers, which could cause over-routing for simple tasks. The trigger map does not distinguish task complexity -- "analyze" triggers /problem-solving regardless of whether the analysis is trivial or complex. |

---

#### AP-04: Under-Routing

| Attribute | Detail |
|-----------|--------|
| **Name** | Under-Routing |
| **Description** | Failing to route to a specialist when one would meaningfully improve output quality. Generalist agent struggles with domain-specific tasks. |
| **Symptoms** | Generalist agent producing lower-quality output for domain-specific tasks; longer processing time as generalist compensates for lack of specialization; inconsistent output quality across task domains. |
| **Root Cause** | Trigger map has finite keyword coverage; semantic variations of trigger keywords not captured; novel request types not mapped to any skill. |
| **Consequences** | Suboptimal output quality; missed specialist knowledge; inconsistent performance across task types. |
| **Prevention Rule** | REVIEW trigger map periodically for coverage gaps. ADD semantic similarity layer to catch keyword variations. IMPLEMENT LLM fallback router for unmatched requests. |
| **Jerry Applicability** | **PARTIALLY EXPOSED.** Jerry's keyword-only routing (mandatory-skill-usage.md) misses semantic variations. "Debug this issue" does not contain any /problem-solving trigger keyword, yet investigation is the appropriate skill. NSE trade study TS-3 shows layered routing closes this gap (+0.05 delta). |

---

#### AP-05: Routing Loops Without Circuit Breakers

| Attribute | Detail |
|-----------|--------|
| **Name** | Routing Loops Without Circuit Breakers |
| **Description** | Agents repeatedly hand off to each other without convergence. Particularly common in handoff and iterative patterns without clear acceptance criteria. |
| **Symptoms** | Token consumption escalates; no output produced; agents passing same task back and forth; maker-checker loops without convergence. |
| **Root Cause** | No maximum routing depth; no circuit breaker; unclear acceptance criteria; routing history not tracked in handoff metadata. |
| **Consequences** | Token budget exhaustion; no useful output; session timeout; potential for context overflow triggering compaction and further degradation. |
| **Prevention Rule** | IMPLEMENT maximum iteration caps (5/C2, 7/C3, 10/C4). ADD circuit breaker: halt after 3 consecutive "no improvement" iterations. INCLUDE routing history in handoff metadata. MANDATE human escalation when circuit breaker triggers. |
| **Jerry Applicability** | **EXPOSED.** Jerry's H-14 sets minimum iterations (3) but no maximum. No circuit breaker mechanism exists. No routing history tracking in handoff metadata. AE-006 mandates human escalation for context exhaustion at C3+ but does not cover iterative loop exhaustion specifically. |

---

#### AP-06: Monolithic Agent

| Attribute | Detail |
|-----------|--------|
| **Name** | Monolithic Agent Attempting Everything |
| **Description** | Single agent with access to all tools and all knowledge, attempting to handle every type of request without specialization. |
| **Symptoms** | Tool overload (20+ tools causing selection errors); inconsistent quality across domains; long processing times; context filled with irrelevant tool descriptions. |
| **Root Cause** | Failure to decompose capabilities into specialized agents; all-access tool configuration; no task routing. |
| **Consequences** | Tool selection accuracy degrades; context window consumed by tool descriptions (MCP Tool Search activates at 10% context); domain confusion between tasks. |
| **Prevention Rule** | DECOMPOSE into specialized agents when tool count exceeds 15-20 per agent. USE tool allowlists to restrict per-agent access. IMPLEMENT routing to direct tasks to appropriate specialists. |
| **Jerry Applicability** | **PROTECTED.** Jerry's skill-based architecture with 37 specialized agents prevents monolithic design. Agent definitions specify tool allowlists. Current tool count per agent is well below the 20-tool threshold. |

---

#### AP-07: Free-Text Handoffs

| Attribute | Detail |
|-----------|--------|
| **Name** | Free-Text Handoffs |
| **Description** | Agent-to-agent communication via unstructured natural language summaries rather than structured data contracts. |
| **Symptoms** | Information loss during handoffs; receiving agent makes incorrect assumptions; handoff quality varies non-deterministically; debugging handoff failures is difficult. |
| **Root Cause** | Inter-agent communication treated as informal conversation rather than API boundary. No schema validation for handoff payloads. |
| **Consequences** | Primary source of agent system failures (Google, 2026). Context loss accumulates through multi-step workflows. Downstream agents operate on incomplete information. |
| **Prevention Rule** | DEFINE structured handoff schemas with required fields per agent pair. VALIDATE handoff payloads against schema before delivering to receiving agent. WRITE handoff payloads to filesystem for auditability. |
| **Jerry Applicability** | **EXPOSED.** AGENTS.md defines a conceptual handoff JSON structure but does not enforce it. Actual handoffs are implicit (file-based artifact passing + orchestrator instructions). No schema validation exists. |

---

#### AP-08: Missing Quality Gates Between Agents

| Attribute | Detail |
|-----------|--------|
| **Name** | Missing Quality Gates Between Agents |
| **Description** | Output passes directly from one agent to the next without quality verification. Errors from upstream agents propagate unchecked through the pipeline. |
| **Symptoms** | Cascade failures; downstream agents produce garbage from garbage input; no checkpoint for error isolation; debugging requires tracing through entire chain. |
| **Root Cause** | Quality gates (H-13, H-14, H-17) are defined for final deliverables but not for intermediate agent outputs within a pipeline. |
| **Consequences** | Cascade failure propagation; error amplification; wasted tokens processing corrupted intermediate artifacts. |
| **Prevention Rule** | ADD quality gates at pipeline stage boundaries (not just final deliverable). IMPLEMENT lightweight validation for intermediate outputs (schema check, completeness check). ENABLE error isolation via fallback at each stage. |
| **Jerry Applicability** | **PARTIALLY EXPOSED.** Jerry's quality gate (H-13: >= 0.92 for C2+) applies to final deliverables. Intermediate outputs within an orchestration pipeline do not receive quality scoring. The orchestration skill tracks phase completion but does not validate phase output quality. |

---

#### AP-09: Context Window Stuffing

| Attribute | Detail |
|-----------|--------|
| **Name** | Context Window Stuffing |
| **Description** | Filling the context window with large amounts of data before the agent begins processing, reducing available context for reasoning and tool use. |
| **Symptoms** | Agent runs out of context before completing task; auto-compaction triggers mid-task; instruction following degrades; agent "forgets" earlier instructions. |
| **Root Cause** | Loading large files, extensive system prompts, many tool descriptions, or verbose reference materials into context before task execution begins. |
| **Consequences** | Reduced effective context for reasoning; premature compaction; context rot acceleration; instruction-following degradation. |
| **Prevention Rule** | USE progressive disclosure (load metadata first, then details on demand). DELEGATE large-output operations to subagents. PREFER just-in-time retrieval over pre-loading. NEVER read canonical-transcript.json (~930KB). |
| **Jerry Applicability** | **PARTIALLY PROTECTED.** Jerry's progressive disclosure (skill three-tier loading) and H-05/python-environment large file handling rules provide some protection. The enforcement budget (~15,100 tokens / 7.6% of 200K) is consciously managed. However, no mechanism prevents an agent from reading excessively large files into context. |

---

#### AP-10: Tool Proliferation Without Restriction

| Attribute | Detail |
|-----------|--------|
| **Name** | Tool Proliferation Without Restriction |
| **Description** | Agents given access to all available tools regardless of their specific task needs. Tool count per agent grows without corresponding restriction. |
| **Symptoms** | Tool selection errors increase; agent uses wrong tool for task; tool descriptions consume significant context budget; MCP Tool Search activates at 10% context threshold. |
| **Root Cause** | Default configuration gives agents unrestricted tool access. No governance process for tool-to-agent assignment. |
| **Consequences** | Tool selection accuracy degrades at 15-20+ tools (Anthropic threshold); context budget consumed by tool descriptions; security risk from unrestricted tool access. |
| **Prevention Rule** | EVERY agent MUST have explicit tool allowlist (principle of least privilege). REVIEW tool assignments when adding new tools or agents. MONITOR tool selection accuracy as tool count grows. IMPLEMENT contextual function selection at 15+ tools per agent. |
| **Jerry Applicability** | **PARTIALLY PROTECTED.** Jerry's agent definitions include tool fields with allowlists. The MCP tool integration matrix restricts MCP tools to specific agents. However, enforcement is at the prompt level -- there is no hook-based validation of tool access restrictions for non-MCP tools. |

---

## L2: Jerry-Specific Assessment

### 5. Jerry-Specific Vulnerability Assessment

#### 5.1 Protected Failure Modes

Jerry's existing architecture provides structural protection against these failure modes:

| Failure Mode | Protection Mechanism | Citation |
|-------------|---------------------|----------|
| **Bag of Agents (OF-03)** | H-01 max 1 level nesting; explicit agent registry in AGENTS.md; skill-based compartmentalization | P-003, AGENTS.md |
| **Recursive agent cascades** | Hard architectural constraint in Claude Code -- subagents cannot spawn subagents | R1-F5.1, H-01 |
| **Monolithic agent (AP-06)** | 37 specialized agents across 8 skills; tool allowlists per agent | AGENTS.md |
| **Context overflow without recovery (CF-02)** | MCP-002 phase boundary persistence; Memory-Keeper store at orchestration boundaries; filesystem-as-memory | mcp-tool-standards.md |
| **Unreviewed output (QF-01 partial)** | H-14 creator-critic-revision cycle (3 min iterations); H-15 self-review; H-17 quality scoring required | quality-enforcement.md |
| **Governance bypass** | Auto-escalation rules AE-001 through AE-006; constitutional compliance check S-007 | quality-enforcement.md |
| **Tool unavailability (TF-02)** | MCP fallback to `work/.mcp-fallback/` on server failure; documented fallback chain | mcp-tool-standards.md |
| **Agent starvation (OF-02)** | 7-agent concurrency limit documented; orchestration planning accounts for limit | R1-F9.1 |
| **Context window stuffing (AP-09, partial)** | Progressive disclosure for skills; enforcement budget managed at ~7.6% of context; large file restrictions | python-environment.md, CLAUDE.md |

#### 5.2 Exposed Failure Modes

Jerry lacks structural protection against these failure modes, listed by priority:

| Priority | Failure Mode | ID | RPN | Current Gap | Impact |
|----------|-------------|-----|-----|-------------|--------|
| **P1** | Routing loops without circuit breakers | RF-04 | 252 | H-14 sets min iterations but no max; no circuit breaker; no routing history tracking | Token budget exhaustion; no output; potential context overflow |
| **P2** | Free-text handoff information loss | HF-01 | 336 | AGENTS.md handoff protocol is conceptual, not enforced; no schema validation; implicit file-based passing | Primary source of agent system failures; information loss accumulates |
| **P3** | Quality gate false positive scoring | QF-02 | 280 | No anti-leniency enforcement; no score calibration; no independent validation | Substandard deliverables pass quality gate; quality assurance credibility undermined |
| **P4** | No deterministic routing enforcement | RF-01 | 150 | Routing rules in mandatory-skill-usage.md are prompt-level only; no hook-based validation | Routing compliance degrades with context rot |
| **P5** | Missing intermediate quality gates | AP-08 | -- | Quality gates apply to final deliverables only; intermediate pipeline outputs are unchecked | Cascade failures; corrupted intermediate artifacts propagate |
| **P6** | Critic-creator collusion | QF-03 | 210 | Single-model critique with shared blind spots; H-16 mitigates but does not eliminate | Superficial critique cycles; quality gate becomes ceremonial |
| **P7** | Telephone game degradation | HF-04 | 245 | No guideline for context-centric vs. problem-centric decomposition | Information fidelity degrades through serial handoffs |
| **P8** | Over-routing for simple tasks | AP-03 | -- | H-22 mandates proactive invocation without complexity assessment | Token waste; latency for trivial tasks |
| **P9** | Under-routing for semantic variations | AP-04 | -- | Keyword-only trigger map; no semantic or LLM fallback layer | Specialist knowledge not applied when needed |

#### 5.3 Vulnerability Priority Matrix

```
HIGH IMPACT + HIGH LIKELIHOOD (Address Immediately):
  [P1] Routing loops      -- no max iteration cap exists
  [P2] Free-text handoffs -- identified as #1 failure source industry-wide
  [P3] False positive scores -- undermines entire quality framework

HIGH IMPACT + MEDIUM LIKELIHOOD (Address in PROJ-007):
  [P5] Missing intermediate QG -- cascade failure risk
  [P6] Critic-creator collusion -- quality credibility risk
  [P7] Telephone game -- information loss over multi-step workflows

MEDIUM IMPACT + MEDIUM LIKELIHOOD (Address After PROJ-007):
  [P4] Non-deterministic routing -- hook implementation needed
  [P8] Over-routing -- complexity assessment needed
  [P9] Under-routing -- semantic layer needed
```

---

### 6. Corrective Action Plan

#### 6.1 Immediate Actions (Within PROJ-007 Scope)

##### IA-01: Maximum Iteration Caps

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | P1 -- Routing loops without circuit breakers (RF-04, RPN 252) |
| **Immediate Action** | Define maximum iteration caps as a new HARD rule in the agent pattern guide. Specify caps per criticality level: C1=3, C2=5, C3=7, C4=10. |
| **Root Cause Fix** | Implement circuit breaker logic: halt after 3 consecutive iterations where quality score does not improve. Mandatory human escalation when circuit breaker triggers (extending AE-006). |
| **Prevention Mechanism** | Include routing history (list of agents that have handled this task and their outcomes) in handoff metadata. Orchestration planner validates iteration count before spawning next agent. |
| **Verification Method** | Test with orchestration scenarios that deliberately produce non-converging outputs. Verify that circuit breaker halts execution and escalates to human. |

##### IA-02: Structured Handoff Schema Specification

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | P2 -- Free-text handoff information loss (HF-01, RPN 336) |
| **Immediate Action** | Define mandatory handoff schema fields in the agent pattern guide. Minimum required fields: `task`, `context.files`, `context.prior_findings`, `context.constraints`, `success_criteria`, `criticality`, `routing_history`. |
| **Root Cause Fix** | Create standardized handoff templates per agent-role category (researcher -> analyst, analyst -> synthesizer, etc.). Handoff payloads written to filesystem as structured JSON artifacts for auditability. |
| **Prevention Mechanism** | Agent prompts include explicit instructions to populate all required handoff fields. Guide specifies that free-text summaries are insufficient for inter-agent handoffs. |
| **Verification Method** | Review handoff artifacts in orchestration output directories. Verify all required fields are populated. Compare information completeness against source agent's full output. |

##### IA-03: Anti-Leniency Scoring Instructions

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | P3 -- Quality gate false positive scoring (QF-02, RPN 280) |
| **Immediate Action** | Add explicit anti-leniency instructions to the scoring guide: "Your default tendency is to score too high. Actively look for deficiencies. Scores above 0.95 require extraordinary justification. The majority of first-pass deliverables should score between 0.75 and 0.88." |
| **Root Cause Fix** | Require per-dimension evidence citations: each dimension score must reference a specific section/paragraph of the deliverable with concrete deficiency or strength identified. Prohibit composite-only scoring -- all 6 dimensions must be individually justified. |
| **Prevention Mechanism** | Fresh scorer context for each evaluation iteration (spawn new scorer subagent rather than continuing in same context). Score regression detection: flag if dimension scores increase without corresponding textual changes. |
| **Verification Method** | Evaluate scoring calibration by applying scorer to known-quality reference deliverables. Compare score distributions against expected ranges. Check that per-dimension evidence citations are present and specific. |

##### IA-04: Context-Centric Decomposition Guideline

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | P7 -- Telephone game degradation (HF-04, RPN 245) |
| **Immediate Action** | Include decomposition strategy guidance in the agent pattern guide. PREFER context-centric decomposition (divide by context boundary) over problem-centric decomposition (divide by work type). |
| **Root Cause Fix** | When possible, assign complete scopes to single agents (feature + tests + review). Minimize handoff chain length by grouping related work that shares context. |
| **Prevention Mechanism** | Orchestration planner evaluates decomposition strategy. Flag decompositions that create handoff chains longer than 3 steps for the same context domain. |
| **Verification Method** | Review orchestration plans for handoff chain length. Track information completeness at each handoff step. Compare final output quality against handoff chain length. |

---

#### 6.2 Root Cause Structural Fixes (New Rules/Guides)

##### SF-01: Intermediate Quality Gates

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | P5 -- Missing intermediate quality gates |
| **Fix** | Define lightweight quality checks for intermediate pipeline outputs. Not full S-014 scoring (too expensive for intermediates), but schema validation + completeness check + constraint verification. |
| **Rule Type** | MEDIUM (overridable with justification for C1 tasks) |
| **Verification** | Test with orchestration pipeline where intermediate output is deliberately corrupted. Verify that downstream agents either reject or flag the corrupted input. |

##### SF-02: Critic Independence Enhancement

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | P6 -- Critic-creator collusion (QF-03, RPN 210) |
| **Fix** | Strengthen critic independence through: (a) H-16 enforcement (steelman before devil's advocate), (b) critic prompt includes explicit instruction to identify at least 3 deficiencies regardless of overall quality, (c) for C3+, critic receives only the deliverable without the creator's self-assessment to prevent anchoring. |
| **Rule Type** | HARD (for C3+) / MEDIUM (for C2) |
| **Verification** | Compare critique quality when critic has vs. lacks access to creator's self-assessment. Track number of deficiencies identified per critique iteration. |

##### SF-03: Routing Enhancement -- Negative Keywords and Priority

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | P4 -- Non-deterministic routing; P8 -- Over-routing; P9 -- Under-routing |
| **Fix** | Enhance mandatory-skill-usage.md trigger map with: (a) negative keywords per skill (disambiguation signals), (b) priority ordering (when positive keywords match multiple skills), (c) complexity assessment guidance (simple tasks should not trigger multi-agent orchestration). |
| **Rule Type** | MEDIUM |
| **Verification** | Create test corpus of 50 representative requests. Measure routing accuracy before and after trigger map enhancement. Target: >90% correct first-route. |

##### SF-04: Effort Scaling Guidelines

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | CF-01 context rot; AP-03 over-routing |
| **Fix** | Define effort scaling guidelines: simple queries use single agent with 3-10 tool calls; moderate tasks use 2-3 focused agents; complex research uses multi-agent orchestration. Match task complexity to agent investment. Include context budget estimation in orchestration planning. |
| **Rule Type** | MEDIUM |
| **Verification** | Track token consumption per orchestration run. Compare against estimated budget. Identify runs where actual consumption exceeds 2x estimate. |

##### SF-05: Session Segmentation Protocol

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | CF-01 context rot; PF-01 prompt drift |
| **Fix** | Define proactive session segmentation protocol: when estimated context fill exceeds 60%, spawn new subagent with clean context for remaining work. Persist critical state to filesystem before segmentation. Reload only essential state in new context. |
| **Rule Type** | MEDIUM |
| **Verification** | Monitor output quality across context fill levels. Compare output quality before and after session segmentation. |

---

#### 6.3 Prevention Mechanisms (Hook-Based / Tooling)

##### PM-01: PreToolUse Hook for UV Enforcement

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | Gap identified in R1-L2 (hook-based enforcement not yet implemented) |
| **Fix** | Implement PreToolUse hook for Bash tool that validates H-05/H-06 (UV only). Exit code 2 blocks non-UV Python/pip commands. This is the first L3 layer implementation. |
| **Rule Type** | HARD (H-05, H-06 already exist; this adds deterministic enforcement) |
| **Verification** | Test with deliberate `python` and `pip install` commands. Verify hook blocks execution with informative error message. |

##### PM-02: PostToolUse Hook for Handoff Validation

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | P2 -- Free-text handoff information loss |
| **Fix** | Implement PostToolUse hook for Task tool that inspects subagent output for required handoff fields. Warn (not block) when handoff payload is missing required fields. Log missing fields for quality tracking. |
| **Rule Type** | MEDIUM (warning rather than blocking to avoid disrupting existing workflows during transition) |
| **Verification** | Test with deliberately incomplete handoff payloads. Verify warning is generated with specific missing field identification. |

##### PM-03: Context Fill Monitoring

| Attribute | Detail |
|-----------|--------|
| **Vulnerability** | CF-01 context rot; CF-04 context pollution |
| **Fix** | Implement context fill estimation in orchestration planning. Before spawning agents or loading large files, estimate context impact. Flag when estimated fill exceeds 60% threshold. Recommend subagent delegation for high-output operations. |
| **Rule Type** | MEDIUM |
| **Verification** | Track correlation between estimated context fill and actual output quality. Validate that 60% threshold is appropriate (may need adjustment based on empirical data). |

---

#### 6.4 Corrective Action Priority Summary

| Priority | Action | Vulnerability | Type | Effort |
|----------|--------|--------------|------|--------|
| **Immediate** | IA-01: Max iteration caps | P1: Routing loops | Rule | Low |
| **Immediate** | IA-02: Structured handoff schema | P2: Handoff info loss | Guide | Medium |
| **Immediate** | IA-03: Anti-leniency scoring | P3: False positives | Guide | Low |
| **Immediate** | IA-04: Decomposition guideline | P7: Telephone game | Guide | Low |
| **Structural** | SF-01: Intermediate quality gates | P5: Cascade failures | Rule | Medium |
| **Structural** | SF-02: Critic independence | P6: Collusion | Rule | Medium |
| **Structural** | SF-03: Routing enhancement | P4/P8/P9: Routing gaps | Rule | Medium |
| **Structural** | SF-04: Effort scaling | CF-01/AP-03 | Guide | Low |
| **Structural** | SF-05: Session segmentation | CF-01/PF-01 | Guide | Medium |
| **Prevention** | PM-01: UV enforcement hook | L3 gap | Hook | Medium |
| **Prevention** | PM-02: Handoff validation hook | P2: Handoff quality | Hook | High |
| **Prevention** | PM-03: Context fill monitoring | CF-01: Context rot | Tooling | High |

---

## Source Traceability

All findings in this investigation are traced to Phase 1 research sources and Jerry rule references:

| Citation Key | Full Reference |
|-------------|---------------|
| R1-F1.2 | ps-researcher-001, Finding 1.2: Orchestrator-Worker Architecture |
| R1-F2.2 | ps-researcher-001, Finding 2.2: Tool Restriction Mechanisms |
| R1-F3.2 | ps-researcher-001, Finding 3.2: Session Persistence and Resumption |
| R1-F4.1 | ps-researcher-001, Finding 4.1: Subagent Context Independence |
| R1-F4.2 | ps-researcher-001, Finding 4.2: Git Worktree Isolation |
| R1-F5.1 | ps-researcher-001, Finding 5.1: No Recursive Subagents |
| R1-F5.2 | ps-researcher-001, Finding 5.2: Background Subagent Limitations |
| R1-F5.3 | ps-researcher-001, Finding 5.3: Context Window Constraints |
| R1-F5.4 | ps-researcher-001, Finding 5.4: Compounding Error Risk |
| R1-F6.1 | ps-researcher-001, Finding 6.1: Subagent System Prompt Mechanism |
| R1-F7.1 | ps-researcher-001, Finding 7.1: Anthropic Core Principles |
| R1-F7.2 | ps-researcher-001, Finding 7.2: Tool Design as Prompt Engineering |
| R1-F9.1 | ps-researcher-001, Finding 9.1: Task Tool Architecture |
| R1-L2 | ps-researcher-001, L2: Strategic Implications (Gap Analysis) |
| R2-F4.2 | ps-researcher-002, Finding 4.2: Keyword Trigger Design Principles |
| R2-F5.1 | ps-researcher-002, Finding 5.1: Ambiguity Resolution Strategies |
| R2-F6.2 | ps-researcher-002, Finding 6.2: Structured Handoffs as API Contracts |
| R2-F8.1 | ps-researcher-002, Finding 8.1: Bag of Agents Anti-Pattern |
| R2-F8.2 | ps-researcher-002, Finding 8.2: Telephone Game Anti-Pattern |
| R2-F8.3 | ps-researcher-002, Finding 8.3: Routing Loop Anti-Pattern |
| R2-F8.4 | ps-researcher-002, Finding 8.4: Over-Routing and Under-Routing |
| R2-F9.1 | ps-researcher-002, Finding 9.1: Fallback Strategy Hierarchy |
| R2-F9.2 | ps-researcher-002, Finding 9.2: Verification Subagent Pattern |
| R2-L2-R1 | ps-researcher-002, L2 Recommendation 1: Layered Routing Architecture |
| R2-L2-R2 | ps-researcher-002, L2 Recommendation 2: Structured Handoff Schemas |
| R2-L2-R3 | ps-researcher-002, L2 Recommendation 3: Negative Keywords and Priority |
| R2-L2-R4 | ps-researcher-002, L2 Recommendation 4: Routing Loop Prevention |
| R2-L2-R5 | ps-researcher-002, L2 Recommendation 5: Context-Centric Decomposition |
| R2-L2-R6 | ps-researcher-002, L2 Recommendation 6: Contextual Function Selection |
| R3-RQ1 | ps-researcher-003, RQ-1: Established Agent Design Patterns |
| R3-RQ4 | ps-researcher-003, RQ-4: Prompt Engineering for Personas |
| R3-RQ5 | ps-researcher-003, RQ-5: Tool Use and Function Calling |
| R3-RQ6 | ps-researcher-003, RQ-6: Quality Assurance Patterns |
| R3-RQ7 | ps-researcher-003, RQ-7: Context Management Strategies |
| R3-L2 | ps-researcher-003, L2: Strategic Analysis |
| NSE | nse-to-ps cross-pollination handoff (TS-1 through TS-5 results) |
| QE | quality-enforcement.md (H-13 through H-19, S-014, AE rules) |
| AGENTS.md | Agent registry and handoff protocol |
| MSU | mandatory-skill-usage.md (H-22, trigger map) |

---

## Self-Review (S-010)

### Completeness Check

| Required Section | Status | Coverage |
|-----------------|--------|----------|
| FMEA Table | COMPLETE | 28 failure modes across 7 categories with RPN scoring |
| Root Cause Analysis (5 Whys) | COMPLETE | Top 5 highest-RPN modes analyzed to systemic root cause |
| Ishikawa Diagrams | COMPLETE | Top 3 modes with 6-category fishbone analysis |
| Anti-Pattern Catalog | COMPLETE | 10 anti-patterns with full attribute tables |
| Jerry Vulnerability Assessment | COMPLETE | 9 protected + 9 exposed modes identified with priority |
| Corrective Action Plan | COMPLETE | 12 actions (4 immediate, 5 structural, 3 prevention) |

### Quality Verification

| Criterion | Assessment |
|-----------|------------|
| **Source Traceability** | All failure modes traced to Phase 1 research sources (R1, R2, R3, NSE, QE). 34 citation keys mapped to specific findings. |
| **FMEA Methodology** | Standard FMEA scoring (Severity x Occurrence x Detection = RPN). Scoring criteria defined with Low/Medium/High ranges. |
| **Root Cause Depth** | All 5 RCA analyses reach systemic level (5th Why). Structural fixes address root causes, not symptoms. |
| **Ishikawa Completeness** | All 3 diagrams cover 6 categories (Method, Machine, Material, Measurement, Manpower, Mother Nature). Multiple contributing factors per category. |
| **Actionability** | All corrective actions include: vulnerability reference, immediate action, root cause fix, prevention mechanism, and verification method. |
| **Jerry Specificity** | All anti-patterns assessed for Jerry applicability. Protection mechanisms cite specific rules/constraints. Gaps cite specific missing mechanisms. |
| **L0/L1/L2 Structure** | L0 (executive summary), L1 (detailed investigation with FMEA, RCA, Ishikawa, anti-patterns), L2 (Jerry assessment + corrective actions). |
| **Navigation** | H-23 compliant navigation table with H-24 anchor links. |

### Identified Limitations

1. **FMEA Scoring Subjectivity:** Severity, Occurrence, and Detection scores are based on expert judgment informed by research findings, not empirical measurement. Scores should be validated against actual incident data as Jerry matures.
2. **Anti-Pattern Coverage:** The catalog covers the most cited anti-patterns from Phase 1 research. Additional anti-patterns may exist that were not covered by the research scope (e.g., security-specific anti-patterns, data privacy anti-patterns).
3. **Corrective Action Feasibility:** Implementation effort estimates (Low/Medium/High) are qualitative. Detailed implementation planning may reveal dependencies or constraints not identified in this investigation.
4. **Context Rot Quantification:** The 60% context fill threshold cited for degradation onset is an estimate based on Anthropic's guidance ("accuracy in recalling information decreases as context window size increases"). The exact threshold varies by model version and task type.

---

*Investigation completed: 2026-02-21 | Agent: ps-investigator-001 | PS-ID: PROJ-007 | Entry: e-004*
