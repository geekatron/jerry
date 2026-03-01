# Agent Routing Standards

<!-- VERSION: 1.1.0 | DATE: 2026-02-21 | SOURCE: ADR-PROJ007-002, PROJ-007 Phase 3 Synthesis, V&V Plan | REVISION: Barrier 4 quality gate revisions (7 items) -- derivations for H-36, H-37, priority ordering, 2-level gap; migration path; failure propagation; FMEA measurability status -->

> Canonical standards for agent routing, trigger map design, circuit breakers, multi-skill combination, anti-pattern prevention, and routing observability within the Jerry Framework. All routing decisions MUST reference this file.

<!-- L2-REINJECT: rank=6, content="Routing: keyword-first (Layer 1, deterministic). Enhanced trigger map: 5 columns (keywords, negative keywords, priority, compound triggers, skill). Circuit breaker: max 3 hops per request (H-36). Keyword-first routing REQUIRED below 20 skills (H-37). Multi-skill combination: /orchestration first, research before design, content before quality. 8 anti-patterns documented (AP-01 through AP-08). H-31 terminal: ask user when all layers fail." -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Routing constraints H-36, H-37 |
| [MEDIUM Standards](#medium-standards) | Overridable routing standards with documented justification |
| [Layered Routing Architecture](#layered-routing-architecture) | Three-layer routing with escalation conditions |
| [Enhanced Trigger Map](#enhanced-trigger-map) | Five-column format with negative keywords, priority, compound triggers |
| [Routing Algorithm](#routing-algorithm) | Three-step resolution: filter, specificity, priority |
| [Circuit Breaker](#circuit-breaker) | Maximum routing depth, cycle detection, termination behavior |
| [Multi-Skill Combination](#multi-skill-combination) | Ordering protocol and context sharing |
| [Anti-Pattern Catalog](#anti-pattern-catalog) | Eight routing anti-patterns with detection and prevention |
| [Routing Observability](#routing-observability) | Structured log format, coverage gap detection |
| [Scaling Roadmap](#scaling-roadmap) | Phased routing evolution by skill count |
| [Verification](#verification) | How compliance is verified per enforcement layer |
| [References](#references) | Source document traceability |

---

## HARD Rules

> These rules CANNOT be overridden. Violations will be blocked.

| ID | Rule | Consequence | Source Requirements | Verification |
|----|------|-------------|---------------------|--------------|
| H-36 | (a) Circuit breaker: No request SHALL be routed more than 3 hops without reaching a terminal agent that produces output. A hop is one transition between skills or agents where routing logic re-evaluates the destination. Cycle detection: if the same `from -> to` agent pair appears twice in `routing_history`, the circuit breaker activates regardless of remaining hop count. When the circuit breaker fires: (1) halt further routing, (2) log the full `routing_history`, (3) present current best result to user, (4) inform user routing reached maximum depth per P-022, (5) ask user for explicit guidance per H-31. At C3+ criticality, circuit breaker activation triggers mandatory human escalation per AE-006. (b) Keyword-first routing: REQUIRED below 20 skills; keyword match layer MUST be attempted before any scoring or ML-based routing. | Runaway routing loop. Token exhaustion. Degraded latency. Stochastic routing for deterministic cases. Token waste. Loss of routing auditability. | RR-006 (routing loop prevention, MUST), SR-004 (user authority), SR-005 (no deception), RR-001 (keyword primary, MUST), RR-004 (routing determinism, MUST), RR-008 (routing observability, SHOULD) | L4 (post-tool): Inspect routing_history for depth and cycles. L3 (pre-tool): Check routing_depth counter before invoking new agent. L1 (session start): mandatory-skill-usage.md trigger map loaded. L2 (every prompt): H-22 proactive invocation re-injected. |
| H-37 (retired -> H-36b) | Primary routing MUST use keyword matching (Layer 1) as the deterministic fast path. Keyword matching MUST remain the first routing mechanism evaluated for every non-slash-command request. LLM-based routing (Layer 3) MUST NOT be used as the sole or primary routing mechanism at any scale below 20 skills. When Layer 3 is activated, it MUST log its decision (matched skill, confidence score, reasoning) for Layer 1 improvement. | Stochastic routing for deterministic cases. Token waste. Loss of routing auditability. | RR-001 (keyword primary, MUST), RR-004 (routing determinism, MUST), RR-008 (routing observability, SHOULD) | L1 (session start): mandatory-skill-usage.md trigger map loaded. L2 (every prompt): H-22 proactive invocation re-injected. |

**Note:** H-37 is registered in `quality-enforcement.md` HARD Rule Index as H-36(b). This file retains H-37 as the section heading for the keyword-first routing specification.

**H-37 threshold derivation:** 20 skills is selected as the upper bound of the Phase 2-to-Phase 3 transition range (15-20 skills) because: (a) below 15 skills, keyword-only routing provides sufficient coverage (Phase 0/1 architecture); (b) between 15-20, the rule-based decision tree (Layer 2) supplements keywords; (c) at 20, the trigger map's token footprint and collision density reach levels where LLM-based routing adds value per the scaling roadmap transition triggers. H-37 uses the upper bound (20) to ensure deterministic routing is not prematurely abandoned.

**HARD Rule Budget:** H-36 and H-37 are consolidated into compound H-36 in `quality-enforcement.md` HARD Rule Index (H-37 retired as sub-item b). Current budget: 25/25 rules at ceiling.

---

## MEDIUM Standards

> Override requires documented justification.

### Trigger Map Standards

| ID | Standard | Guidance | Source Requirements |
|----|----------|----------|---------------------|
| RT-M-001 | Every skill with > 5 positive keywords SHOULD define negative keywords to prevent false-positive routing. | Negative keywords suppress positive matches when co-occurring. See [Enhanced Trigger Map](#enhanced-trigger-map) for data structure. | RR-005 (negative keywords, SHOULD) |
| RT-M-002 | Every skill SHOULD have at minimum 3 positive trigger keywords. | Ensures sufficient routing coverage. Skills with < 3 keywords are likely under-triggering (AP-01 Keyword Tunnel). | RR-002 (trigger completeness) |
| RT-M-003 | The trigger map SHOULD use the enhanced 5-column format: Detected Keywords, Negative Keywords, Priority, Compound Triggers, Skill. | The 5-column format enables systematic disambiguation without increasing latency or token cost. | RR-005 (negative keywords), RR-004 (determinism) |
| RT-M-004 | When new keywords are added to the trigger map, they SHOULD be cross-referenced against all existing skills to identify collisions. | Prevents AP-02 (Bag of Triggers). Document new collision zones and add corresponding negative keywords. | RR-002 (trigger completeness), AP-02 prevention |
| RT-M-005 | LLM-based routing (Layer 3) SHOULD use a confidence threshold of 0.70. Requests below this threshold SHOULD escalate to H-31 clarification. | The 0.70 threshold is provisional and SHOULD be calibrated empirically via the first 50-100 Layer 3 routing events. | RR-003 (LLM fallback, SHOULD), OI-02 resolution |

### Combination Standards

| ID | Standard | Guidance | Source Requirements |
|----|----------|----------|---------------------|
| RT-M-006 | When multiple skills match a request, skill combination SHOULD follow the ordering protocol: (1) `/orchestration` first, (2) research before design, (3) content before quality, (4) work before presentation. | See [Multi-Skill Combination](#multi-skill-combination) for full protocol. | RR-007 (multi-skill combination, SHOULD) |
| RT-M-007 | Multi-skill combinations exceeding 2 skills SHOULD escalate to Layer 2 or request user prioritization. | Limits coordination complexity. Three-or-more skill combinations typically indicate a request that should be decomposed via `/orchestration`. | RR-007, AP-05 (Over-Routing prevention) |

### Observability Standards

| ID | Standard | Guidance | Source Requirements |
|----|----------|----------|---------------------|
| RT-M-008 | Every routing decision SHOULD produce a structured routing record containing: routing method, layer reached, matched keywords, suppressed matches, selected skill, confidence score, and whether the user corrected the decision. | See [Routing Observability](#routing-observability) for full format. | RR-008 (routing observability, SHOULD) |
| RT-M-009 | Routing observability data SHOULD be reviewed when new skills are added or when routing accuracy concerns arise. At minimum, review when the trigger map is modified. | Signals to monitor: `layer_reached > 1` frequently, `user_corrected == true`, `routing_method == "explicit"` frequently, empty `suppressed_matches` despite multi-match. | RR-008 |

### Iteration Ceiling Standards

| ID | Standard | Guidance | Source Requirements |
|----|----------|----------|---------------------|
| RT-M-010 | Creator-critic-revision iterations SHOULD NOT exceed criticality-proportional ceilings: C1=3, C2=5, C3=7, C4=10. When the ceiling is reached without passing the quality gate (H-13, >= 0.92), the agent SHOULD escalate to the user with the current best result and critic findings. | Works in tandem with H-14 (minimum 3 iterations). These ceilings provide the maximum complement to H-14's minimum. Plateau detection: delta < 0.01 for 3 consecutive iterations triggers early halt. | SF-09 (circuit breaker ceiling), AP-04 (Routing Loop prevention) |

### FMEA Monitoring Thresholds

> Operational observability thresholds derived from FMEA analysis. These are monitoring indicators, not pass/fail compliance rules.

| ID | Metric | Normal | Alert | Escalation | FMEA Source |
|----|--------|--------|-------|------------|-------------|
| RT-M-011 | Context usage at handoff boundaries | < 50% | > 60% | > 80% | CF-01 (Context Rot, RPN 392) |
| RT-M-012 | Quality score variance within session | < 0.05 | > 0.08 | > 0.12 | QF-02 (False Positive Scoring, RPN 280) |
| RT-M-013 | Handoff schema validation pass rate | 100% | < 100% | N/A (any failure is actionable) | HF-01 (Handoff Info Loss, RPN 336) |
| RT-M-014 | Circuit breaker activation rate | < 1% | > 3% | > 5% | RF-04 (Routing Loops, RPN 252) |
| RT-M-015 | Average routing hops per request | < 1.5 | > 2.0 | > 2.5 | RF-04 |

**Measurability status:** RT-M-013 (handoff schema validation pass rate) and RT-M-014 (circuit breaker activation rate) are measurable with current infrastructure (L3/L4 enforcement layers). RT-M-011 (context usage), RT-M-012 (quality score variance), and RT-M-015 (average routing hops) require observability tooling defined in [Routing Observability](#routing-observability); these thresholds will become actionable when routing record persistence is implemented.

---

## Layered Routing Architecture

The routing framework uses three layers with graceful escalation. Only Layer 0 (explicit) and Layer 1 (keyword) are implemented at current scale (8 skills). Layers 2 and 3 are designed for future activation per the [Scaling Roadmap](#scaling-roadmap).

```
    User Request
         |
         v
    +--------------------------+
    | LAYER 0: Explicit        |
    | /slash-command           |----> Deterministic route (bypass all matching)
    | detection                |      ~0ms latency, 0 tokens
    +---------+----------------+
              |
              | No slash command
              v
    +--------------------------+
    | LAYER 1: Enhanced        |
    | Keyword Matching         |----> Single skill match?
    | (trigger map with        |      Yes: Route to skill (fast path)
    |  negative keywords,      |      ~1ms latency, 0 tokens
    |  priority ordering,      |
    |  compound triggers)      |
    +---------+----------------+
              |
              | No match, or multiple matches
              v
    +--------------------------+
    | LAYER 2: Rule-Based      |
    | Decision Tree            |----> Decision tree resolves?
    | (task type signals,      |      Yes: Route to skill(s)
    |  criticality context,    |      ~1ms latency, 0 tokens
    |  prior skill context)    |
    +---------+----------------+
              |
              | Still ambiguous
              v
    +--------------------------+
    | LAYER 3: LLM-as-Router   |
    | (lightweight LLM call    |----> Route to skill(s)
    |  with skill catalog;     |      ~300-5000ms latency
    |  structured output)      |      ~900-1,500 tokens
    +---------+----------------+
              |
              | Confidence below threshold (0.70)
              v
    +--------------------------+
    | TERMINAL: H-31           |
    | Clarification            |----> Ask user which skill is appropriate
    | (ambiguity resolution)   |
    +--------------------------+
```

### Layer Definitions

| Layer | Name | Determinism | Token Cost | Status |
|-------|------|-------------|------------|--------|
| L0 | Explicit Invocation | Full | 0 | Implemented |
| L1 | Enhanced Keyword Matching | Full | 0 | **Implement now** (enhance existing trigger map) |
| L2 | Rule-Based Decision Tree | Full | 0 | Design now, implement at ~15 skills |
| L3 | LLM-as-Router | Stochastic | ~900-1,500 | Design now, implement at ~20 skills |
| Terminal | H-31 Clarification | Full (user decides) | 0 | Implemented |

### Escalation Conditions

| From | To | Condition |
|------|-----|-----------|
| L0 | L1 | No slash command detected |
| L1 | L2 | (a) No positive keyword match after negative filtering, OR (b) Multiple skills match with equal priority, OR (c) Compound trigger partially matches |
| L2 | L3 | (a) Decision tree reaches ambiguous leaf, OR (b) Contextual signals conflict |
| L3 | Terminal | (a) LLM confidence below 0.70, OR (b) LLM returns "ambiguous" classification |

**Graceful degradation:** If any layer is unavailable, the system falls back to the previous layer's best-effort result. The system guarantees that every routing request reaches either a terminal agent or the H-31 clarification fallback. Silent drops are a routing failure -- if no layer can resolve the request, the system escalates to user clarification rather than discarding the request.

---

## Enhanced Trigger Map

The trigger map extends the current 2-column format in `mandatory-skill-usage.md` to a 5-column format. This is a backward-compatible enhancement -- agents that do not parse the new columns continue to function using positive keywords only.

### Format Specification

| Column | Purpose | Required |
|--------|---------|----------|
| **Detected Keywords** | Positive keywords that trigger routing to this skill | Yes |
| **Negative Keywords** | Keywords that suppress this match when co-occurring with positive keywords | Recommended for skills with > 5 keywords (RT-M-001) |
| **Priority** | Numeric priority (1 = highest) for conflict resolution when multiple skills match | Recommended |
| **Compound Triggers** | Keyword combinations requiring co-occurrence for higher-specificity matching | Optional |
| **Skill** | Target skill to route to | Yes |

### Reference Trigger Map

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| research, analyze, investigate, explore, root cause, why, debug, troubleshoot, diagnose, figure out, what went wrong, compare, evaluate | requirements, specification, V&V, adversarial, tournament, transcript, VTT, SRT, voice, persona | 6 | -- | `/problem-solving` |
| requirements, specification, V&V, technical review, risk, design, architecture, interface, trade study, compliance | root cause, debug, adversarial, tournament, research (standalone), transcript | 5 | "technical review" (both words required) | `/nasa-se` |
| orchestration, pipeline, workflow, multi-agent, phases, gates, plan, coordinate, break into steps, sequence | adversarial, transcript, root cause, debug | 1 | -- | `/orchestration` |
| transcript, meeting notes, parse recording, meeting recording, VTT, SRT, captions, audio, summarize this meeting | adversarial, requirements, design | 2 | "parse recording" OR "meeting recording" (phrase match) | `/transcript` |
| adversarial quality review, adversarial critique, rigorous critique, formal critique, adversarial, tournament, red team, devil's advocate, steelman, pre-mortem, quality gate, quality scoring | requirements, specification, design, research, investigate | 7 | "adversarial review" OR "quality gate" OR "quality scoring" (phrase match) | `/adversary` |
| saucer boy, mcconkey, talk like mcconkey, pep talk, roast this code, saucer boy mode | -- | 3 | -- | `/saucer-boy` |
| voice check, voice review, persona compliance, voice rewrite, voice fidelity, voice score, framework voice, persona review | -- | 4 | ("voice" OR "persona") AND ("review" OR "check" OR "score") | `/saucer-boy-framework-voice` |

**Priority ordering rationale:** 1=`/orchestration` (coordinates other skills; must route first per RT-M-006 ordering protocol). 2=`/transcript` (narrow, specific domain; false positives rare). 3-4=`/saucer-boy` variants (conversational; rarely conflict with analytical skills). 5=`/nasa-se` (broad domain; many keyword overlaps with `/problem-solving`). 6=`/problem-solving` (broadest scope; default research/analysis skill). 7=`/adversary` (specialized; invoked primarily for quality assessment; highest priority number ensures it does not capture general analysis requests).

### Migration from Phase 0 to Phase 1

Migration from Phase 0 (2-column) to Phase 1 (5-column): Update `mandatory-skill-usage.md` Trigger Map section to use the 5-column format shown in [Reference Trigger Map](#reference-trigger-map). Existing consumers that parse only columns 1 and 5 (keywords and skill) continue to function without modification. This migration is a single-file change and SHOULD be the first implementation action after this standard is accepted.

---

## Routing Algorithm

The routing algorithm resolves user requests through a three-step process within Layer 1.

### Step 1: Positive/Negative Keyword Filtering

For each skill in the trigger map:
1. Count positive keyword matches against the user request.
2. Count negative keyword matches against the user request.
3. If positive matches > 0 AND negative matches == 0: add skill to candidates with confidence = positive_matches / total_positive_keywords.
4. If positive matches > 0 AND negative matches > 0: suppress the skill (do not add to candidates).

### Step 2: Compound Trigger Specificity Override

If multiple candidates remain:
1. Check each candidate for compound trigger matches.
2. If exactly one candidate has a compound trigger match: route to that candidate (compound triggers are more specific than individual keywords and take precedence over numeric priority).
3. If multiple candidates have compound trigger matches: fall through to Step 3.

### Step 3: Numeric Priority Ordering

If multiple candidates remain after Step 2:
1. Sort candidates by priority (ascending: 1 = highest priority).
2. If the highest-priority candidate is 2+ priority levels above the next: route to highest priority (clear separation).
3. If priority gap is < 2: escalate to Layer 2 (ambiguous).

**2-level gap derivation:** The 2-level gap threshold is a conservative starting value: with 7 skills spanning priority 1-7, a 1-level gap is common between adjacent skills; requiring a 2-level gap ensures meaningful separation rather than arbitrary adjacency ordering. This threshold SHOULD be recalibrated when the skill count changes or routing accuracy data from the observability framework becomes available (RT-M-009).

### Routing Outcomes

| Outcome | Definition | Action |
|---------|-----------|--------|
| **Clear match** | Exactly one skill matches after filtering | Route to that skill. No escalation. |
| **Priority resolved** | Multiple skills match; highest priority is 2+ levels above next | Route to highest priority. Flag lower-priority skills for potential combination. |
| **Ambiguous** | Multiple skills match with close priority, or no match at all | Escalate to Layer 2. |

---

## Circuit Breaker

The circuit breaker prevents runaway routing loops and enforces resource bounds (H-36).

### Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Maximum routing hops | 3 | RR-006. Derivation: (a) the orchestrator-worker topology (H-01/P-003) creates a natural maximum of 2 hops for single-skill invocation (user -> orchestrator -> worker); (b) 3 provides one additional hop for routing correction or multi-skill coordination; (c) observed multi-skill combinations in the current framework require at most 2 skill transitions (see Multi-Skill Combination: max 2 skills before escalation, RT-M-007). The 3-hop limit thus accommodates all current patterns with one hop of error budget. |
| Cycle detection | Same `from -> to` pair appears twice | Catches oscillating handoffs regardless of hop count. |
| Plateau detection | Score delta < 0.01 for 3 consecutive iterations | Detects quality score stagnation in creator-critic loops. |
| Iteration ceilings | C1=3, C2=5, C3=7, C4=10 (RT-M-010) | Criticality-proportional bounds complementing H-14 minimum. |

### Hop Counter

The routing context carries a `routing_depth` counter incremented at each hop:

```yaml
routing_context:
  request_id: "req-{YYYYMMDD}-{NNN}"
  routing_depth: 0          # Incremented at each hop
  max_depth: 3              # Circuit breaker threshold (H-36)
  routing_history:
    - { hop: 1, from: "orchestrator", to: "/problem-solving", method: "keyword" }
    - { hop: 2, from: "ps-researcher", to: "ps-analyst", method: "handoff" }
```

### What Counts as a Hop

| Counts as a hop | Does NOT count as a hop |
|-----------------|------------------------|
| Skill-to-skill transition | Creator-critic-revision iterations (H-14 loops) |
| Agent-to-agent transition within a skill | Explicit user-initiated redirections |
| Re-routing due to agent inability | Quality gate retry within same agent |

### Termination Behavior

When the circuit breaker activates:

| Step | Action | Rationale |
|------|--------|-----------|
| 1 | Halt further routing | Prevent additional token consumption |
| 2 | Log circuit breaker activation with full `routing_history` | Post-hoc analysis of routing failure |
| 3 | Present current best result to user | Partial output is better than nothing |
| 4 | Inform user that routing reached maximum depth | P-022 (no deception, H-03) |
| 5 | Ask user for explicit routing guidance | H-31 (clarify when ambiguous) |
| 6 | At C3+: mandatory human escalation | AE-006 alignment |

---

## Multi-Skill Combination

Multi-skill combination activates when a request triggers multiple skills and none are suppressed by negative keywords (RR-007).

### Combination Triggers

| Condition | Action |
|-----------|--------|
| Two skills match with distinct, non-overlapping keywords | Combine both skills |
| Three or more skills match | Combine up to 2; if 3+ match, escalate to Layer 2 or ask user (RT-M-007) |
| One skill's keywords are a subset of another's negative keywords | Do not combine; negative keyword suppresses |
| `/orchestration` matches alongside other skills | `/orchestration` coordinates; other skills execute within the workflow |

### Ordering Protocol

| Priority | Rule | Example |
|----------|------|---------|
| 1 | `/orchestration` first (when present) | "Plan and research the architecture" -> `/orchestration` plans, then invokes `/problem-solving` |
| 2 | Research before design | "Research options and create requirements" -> `/problem-solving` first, then `/nasa-se` |
| 3 | Content before quality | "Design this and run adversarial review" -> `/nasa-se` first, then `/adversary` |
| 4 | Work before presentation | "Research this, then roast the code" -> `/problem-solving` first, then `/saucer-boy` |

### Context Sharing Between Combined Skills

Each skill operates in its own context window (AR-005 context isolation). The `multi_skill_context` structure passes only explicit artifact references and key findings:

```yaml
multi_skill_context:
  original_request: "{user's original request}"
  skill_sequence:
    - skill: "/problem-solving"
      role: "primary-research"
      status: "complete"
      output_artifacts: ["work/research/options-analysis.md"]
      key_findings: ["Finding 1", "Finding 2"]
    - skill: "/nasa-se"
      role: "requirements-from-research"
      status: "in-progress"
      input_artifacts: ["work/research/options-analysis.md"]
```

### Failure Propagation

If a skill in the sequence fails (status: `failed`), subsequent skills in the sequence SHOULD NOT execute unless the orchestrator explicitly decides to proceed with partial results. The `multi_skill_context` entry for the failed skill SHOULD include a `failure_reason` field. The orchestrator SHOULD present the partial result to the user and ask for guidance per H-31.

```yaml
# Example: failure propagation in multi_skill_context
multi_skill_context:
  skill_sequence:
    - skill: "/problem-solving"
      role: "primary-research"
      status: "failed"
      failure_reason: "Context budget exceeded during research; partial findings only"
      output_artifacts: ["work/research/partial-options.md"]
      key_findings: ["Finding 1 (partial)"]
    - skill: "/nasa-se"
      role: "requirements-from-research"
      status: "blocked"        # Blocked due to upstream failure
```

---

## Anti-Pattern Catalog

Eight routing anti-patterns identified through Phase 1-2 analysis. Each entry includes detection heuristic and prevention rule.

### AP-01: Keyword Tunnel (V&V RAP-01)

| Aspect | Description |
|--------|-------------|
| **Problem** | Routing relies exclusively on keyword matching, creating a narrow "tunnel." Requests expressed in different vocabulary are silently dropped to undocumented agent judgment. |
| **Detection** | (1) Users frequently re-phrase requests to trigger skills. (2) Agent invokes skills inconsistently for equivalent requests. (3) Keyword list not updated in > 3 months. (4) Users manually invoke via slash commands that should trigger automatically. |
| **Prevention** | (1) Audit keyword coverage quarterly. (2) Maintain synonym lists. (3) Track routing "misses." (4) Expand trigger map per enhanced format. |

### AP-02: Bag of Triggers (V&V RAP-02)

| Aspect | Description |
|--------|-------------|
| **Problem** | Keywords added without collision analysis. Multiple skills match with no conflict resolution. |
| **Detection** | (1) Multiple skills frequently match a single request. (2) Inconsistent routing across sessions. (3) Overlapping terms without resolution. (4) > 30% of routing decisions involve multi-skill ambiguity. |
| **Prevention** | (1) Cross-reference all keywords before adding. (2) Implement negative keywords (RT-M-001). (3) Define priority ordering. (4) Require compound triggers for broad terms (RT-M-004). |

### AP-03: Telephone Game (V&V RAP-03)

| Aspect | Description |
|--------|-------------|
| **Problem** | Context degrades through serial handoffs. Each agent summarizes and re-interprets. Original intent progressively lost. |
| **Detection** | (1) Downstream agents ask questions already answered upstream. (2) Final output contradicts early findings. (3) More tokens on coordination than work. (4) Handoff summaries get shorter through chain. |
| **Prevention** | (1) Use structured handoff schemas with required fields (see `agent-development-standards.md` [Handoff Protocol]). (2) Include artifact file paths instead of summarizing content (CP-01). (3) Define explicit success criteria at each handoff. (4) Cap `key_findings` to 3-5 bullets (CP-02). |

### AP-04: Routing Loop (V&V RAP-04)

| Aspect | Description |
|--------|-------------|
| **Problem** | Agents repeatedly hand off to each other without convergence. Token consumption without progress. |
| **Detection** | (1) Same agent pair exchanges control > 2 times. (2) Token consumption exceeds 2x budget. (3) Quality scores plateau or oscillate. (4) `routing_history` contains repeated pairs. |
| **Prevention** | (1) Circuit breaker with max 3 hops (H-36). (2) Cycle detection via pair matching. (3) Mandatory human escalation at C3+ (AE-006). (4) Iteration ceilings per criticality (RT-M-010). |

### AP-05: Over-Routing (Premature Specialization) (V&V RAP-05)

| Aspect | Description |
|--------|-------------|
| **Problem** | Tasks routed to specialized agents when a general-purpose agent would suffice. Coordination overhead exceeds specialization benefit. |
| **Detection** | (1) Agent invocations for tasks completed in < 5 tool calls. (2) Specialist output nearly identical to orchestrator capability. (3) Token overhead from spawning exceeds task budget. |
| **Prevention** | (1) Apply complexity-first decision framework: (a) attempt task with orchestrator context alone, (b) escalate to specialized agent only when task requires > 3 tool calls, domain expertise outside orchestrator scope, or multi-step methodology; the threshold is: if the orchestrator can handle it in a single turn with available tools, it does not need an agent. (2) Define minimum complexity thresholds for agent invocation. (3) Monitor invocation-to-value ratio. |

### AP-06: Under-Routing (Missed Specialization) (V&V RAP-06)

| Aspect | Description |
|--------|-------------|
| **Problem** | Tasks that would benefit from specialists handled by generalist orchestrator. Quality suffers from missing domain methodology. |
| **Detection** | (1) Orchestrator struggles with domain tasks (multiple failed attempts). (2) Lower output quality for domain tasks vs. specialist invocation. (3) Users manually invoke skills per H-22. (4) Trigger map has gaps for common vocabulary. |
| **Prevention** | (1) Expand trigger keywords per enhanced trigger map. (2) Monitor user-initiated invocations as routing failure signal. (3) Define complexity indicators triggering auto-invocation: file count > 3, domain jargon present, multi-step requirements. |

### AP-07: Tool Overload Creep (V&V RAP-07)

| Aspect | Description |
|--------|-------------|
| **Problem** | Agents accumulate tool access until exceeding 15-20 tool threshold where selection accuracy degrades. |
| **Detection** | (1) Agent has > 15 tools. (2) Frequent wrong tool selection. (3) Tool descriptions consume > 10% of context. (4) New MCP servers added without per-agent allowlist review. |
| **Prevention** | (1) Enforce `capabilities.allowed_tools` per agent (AR-006). (2) Monitor tool count per agent; alert at 15. (3) Apply T1-T5 tier model: lowest tier satisfying requirements (see `agent-development-standards.md` [Tool Security Tiers]). (4) Periodically audit and remove unused tools. |

### AP-08: Context-Blind Routing (V&V RAP-08)

| Aspect | Description |
|--------|-------------|
| **Problem** | Routing based solely on current request text, ignoring project phase, file types, conversation history, prior routing decisions, context fill level. |
| **Detection** | (1) Same keyword routes to different skills depending on phase, but routing ignores phase. (2) Routing ignores file types. (3) Prior skill invocations not considered. (4) Routing quality degrades as context fills. |
| **Prevention** | (1) Layer 2 decision tree incorporates contextual signals. (2) Use auto-escalation rules (AE-001 through AE-006) as context-aware triggers. (3) Session-level routing context tracking via `routing_history`. |

---

## Routing Observability

Every routing decision SHOULD produce a structured record (RT-M-008). This enables systematic keyword coverage improvement.

### Routing Record Format

```yaml
routing_record:
  timestamp: "2026-02-21T14:30:00Z"
  request_id: "req-{YYYYMMDD}-{NNN}"
  routing_method: "keyword"          # enum: explicit | keyword | decision_tree | llm | clarification
  layer_reached: 1                   # Highest layer invoked (0-3)
  matched_keywords:
    - { keyword: "debug", skill: "/problem-solving" }
  suppressed_matches:
    - { keyword: "risk", skill: "/adversary", suppressed_by: "debug" }
  selected_skill: "/problem-solving"
  secondary_skills: []
  confidence: 1.0                    # 1.0 for keyword, 0.0-1.0 for LLM
  user_corrected: false
  correction_target: null
  routing_token_cost: 0
```

### Coverage Gap Detection Signals

| Signal | Indicates | Action |
|--------|-----------|--------|
| `layer_reached > 1` frequently | Keyword layer cannot resolve many requests | Analyze requests for missing keywords; expand trigger map |
| `user_corrected == true` | Routing selected wrong skill | Analyze which keywords caused misroute; add negative keywords or adjust priority |
| `routing_method == "explicit"` frequently | Users bypass keyword routing via slash commands | Compare slash-commanded skills against trigger map; likely keyword gap |
| `suppressed_matches` frequently empty despite multi-match | Negative keywords not catching collisions | Review collision zones; add missing negative keywords |

### Persistence

Routing records are persisted as part of the session's worktracker entry in a `Routing Decisions` section:

```markdown
### Routing Decisions

| # | Method | Layer | Selected Skill | Keywords Matched | Suppressed | Confidence | User Corrected |
|---|--------|-------|----------------|------------------|------------|------------|----------------|
| 1 | keyword | 1 | /problem-solving | debug, investigate | /adversary (suppressed) | 1.0 | No |
```

---

## Scaling Roadmap

The routing architecture evolves through four phases, each triggered by measurable conditions.

| Phase | Skill Count | Architecture | Transition Trigger | Effort |
|-------|-------------|-------------|-------------------|--------|
| **Phase 0** (current) | 8 | Keyword-only (current mandatory-skill-usage.md) | -- | None |
| **Phase 1** (immediate) | 8 | Enhanced keyword: negative keywords + priority + compound triggers | This standard is accepted | Low |
| **Phase 2** (10-15 skills) | 10-15 | Phase 1 + rule-based decision tree (Layer 2) | Any 2 of: 10+ collision zones, false negative rate > 40%, user override rate > 30% | Medium |
| **Phase 3** (15-20 skills) | 15-20 | Phase 2 + LLM-as-Router (Layer 3) | Any 2 of: Layer 2 failure rate > 20%, novel request rate > 15%, trigger map > 1,500 tokens | Medium |

### Transition Trigger Measurement

**Phase 1 to Phase 2:**

| Condition | Measurement | Threshold |
|-----------|-------------|-----------|
| Collision zones | Count keyword overlaps in trigger map | 10+ |
| False negative rate | (User slash commands + user corrections) / total routing decisions | > 40% |
| User override rate | User slash commands / total skill invocations | > 30% |

**Phase 2 to Phase 3:**

| Condition | Measurement | Threshold |
|-----------|-------------|-----------|
| Layer 2 failure rate | Ambiguous leaf cases / total Layer 2 invocations | > 20% |
| Novel request rate | Zero-match requests / total requests | > 15% |
| Trigger map token cost | Token count of trigger map section | > 1,500 tokens |

### Future Considerations (Beyond Scope)

At 50+ skills:
- Team-based grouping (hierarchical skill namespaces)
- Embedding-based semantic routing
- Capability-based matching via `identity.expertise` fields

These require future ADRs when transition triggers are met.

---

## Verification

Each standard maps to an enforcement layer for compliance checking.

| Enforcement Layer | Standards Verified | Mechanism | Context Rot Immunity |
|-------------------|-------------------|-----------|---------------------|
| L1 (Session start) | Trigger map loaded via mandatory-skill-usage.md | Rule auto-loading | Vulnerable |
| L2 (Every prompt) | H-36, H-37 re-injection via L2-REINJECT comments | HTML comment re-injection | Immune |
| L3 (Pre-tool) | Routing depth check before agent invocation | `routing_depth` counter inspection | Immune |
| L4 (Post-tool) | Routing history cycle detection, anti-pattern detection | Output inspection of `routing_history` | Mixed |
| L5 (CI/commit) | Trigger map collision analysis, keyword coverage audit | Automated trigger map analysis | Immune |

### Pass/Fail Criteria

| Standard | PASS | FAIL |
|----------|------|------|
| H-36 (Circuit breaker) | No request exceeds 3 hops. No cycles in routing_history. Circuit breaker fires and escalates correctly at C3+. | Request routed > 3 hops. Cycle undetected. Circuit breaker bypassed or fails to escalate. |
| H-37 (Keyword-first routing) | Layer 1 keyword matching evaluated first for every non-slash request. LLM routing not used as sole mechanism below 20 skills. All Layer 3 decisions logged. | LLM routing bypasses keyword layer. LLM used as primary router below threshold. Layer 3 decisions not logged. |
| RT-M-001 through RT-M-015 | Standard followed or deviation documented with justification. | Standard violated without documented justification. |

---

## References

| Source | Content | Location |
|--------|---------|----------|
| ADR-PROJ007-002 | Layered routing architecture, enhanced trigger map, circuit breaker, anti-patterns, scaling roadmap | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-3-synthesis/ps-architect-002/` |
| Phase 3 Synthesis | Unified pattern taxonomy (WF-02, DL-04, SF-09, IN-05, IN-07), consensus findings #4 (keyword-first routing superiority at current scale), #8 (3-hop circuit breaker necessity from error amplification analysis) | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-3-synthesis/ps-synthesizer-001/` |
| V&V Plan | Anti-pattern detection heuristics (RAP-01 through RAP-08), FMEA monitoring thresholds, circuit breaker specifications | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-3-synthesis/nse-verification-001/` |
| Integration Patterns | Enhanced routing format, routing resolution algorithm, multi-skill combination protocol, context passing conventions | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-3-synthesis/nse-integration-001/` |
| Barrier 3 NSE-to-PS Handoff | Routing enhancement rules, anti-pattern codification guidance | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/cross-pollination/barrier-3/nse-to-ps/handoff.md` |
| quality-enforcement.md | H-13, H-14, H-31, criticality levels, AE-006, enforcement architecture | `.context/rules/quality-enforcement.md` |
| mandatory-skill-usage.md | H-22 proactive invocation, current trigger map (Phase 0 baseline) | `.context/rules/mandatory-skill-usage.md` |
| agent-development-standards.md | H-34 (compound), tool tiers, handoff protocol, guardrails template | `.context/rules/agent-development-standards.md` |

---

<!-- VERSION: 1.1.0 | DATE: 2026-02-21 | SOURCE: ADR-PROJ007-002, PROJ-007 Phase 3 Synthesis | REVISION: Barrier 4 QG revisions -->
*Standards Version: 1.1.0*
*SSOT: `.context/rules/quality-enforcement.md` (H-36 compound registered, H-37 retired as sub-item)*
*Source: PROJ-007 Agent Patterns -- ADR-PROJ007-002, Phase 3 Synthesis, V&V Plan, Integration Patterns*
*Created: 2026-02-21*
*Agent: ps-architect-003*
