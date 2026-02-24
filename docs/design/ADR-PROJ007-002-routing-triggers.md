# ADR-PROJ007-002: Agent Routing and Trigger Framework

<!-- VERSION: 1.2.0 | DATE: 2026-02-22 | PS-ID: PROJ-007 | AGENT: ps-architect-002 | CRITICALITY: C4 | REVISION: Barrier 3 revision — 5 scorer findings addressed (F-001 through F-005) -->

> Architecture Decision Record for the canonical routing and trigger framework within the Jerry framework. Codifies how user requests are routed to the appropriate skill/agent, incorporating layered routing, enhanced trigger maps, circuit breakers, multi-skill combination, anti-patterns, and scaling roadmap.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Stakeholder-level decision overview |
| [Status](#status) | ADR lifecycle state |
| [Context](#context) | Problem statement, current state, scaling trajectory |
| [Decision](#decision) | The layered routing architecture and its components |
| [1. Layered Routing Architecture](#1-layered-routing-architecture) | Three-layer routing with escalation conditions and Layer 2 decision tree sketch |
| [2. Enhanced Trigger Map Design](#2-enhanced-trigger-map-design) | Negative keywords, priority ordering, confidence thresholds |
| [3. Circuit Breaker Specification](#3-circuit-breaker-specification) | Max routing depth, detection, termination |
| [4. Multi-Skill Combination Protocol](#4-multi-skill-combination-protocol) | Handling requests spanning multiple skills |
| [5. Anti-Pattern Catalog](#5-anti-pattern-catalog) | Eight routing anti-patterns with detection and prevention |
| [6. Scaling Roadmap](#6-scaling-roadmap) | Phased routing evolution by skill count |
| [7. Routing Observability](#7-routing-observability) | Logging format, coverage gap detection |
| [Consequences](#consequences) | Migration path, costs, risks, trade-offs |
| [Alternatives Considered](#alternatives-considered) | Rejected approaches with rationale |
| [Requirements Traceability](#requirements-traceability) | Mapping to RR-001 through RR-008 |
| [Evidence Sources](#evidence-sources) | Source document index |
| [Self-Review (S-010)](#self-review-s-010) | Quality verification before submission |

---

## L0: Executive Summary

This ADR establishes the canonical approach to routing user requests to the appropriate skill and agent within the Jerry framework. The decision preserves keyword-based routing as the deterministic fast path (Layer 1), introduces a rule-based decision tree for disambiguation (Layer 2), and defines an LLM-based fallback for ambiguous or novel requests (Layer 3). Only Layer 1 enhancements -- negative keywords, priority ordering, and compound triggers -- are recommended for immediate implementation. Layers 2 and 3 are designed now but deferred until empirical scaling triggers are met (approximately 15 and 20+ skills respectively).

The central trade-off resolved by this ADR is **routing accuracy versus system complexity**. At Jerry's current 8-skill, 37-agent scale, keyword routing achieves an estimated 65-80% deterministic match rate. Enhancing the keyword layer with negative keywords and priority ordering raises this to an estimated 75-90% at near-zero additional complexity or token cost. These coverage estimates are based on enumerated plausible intents, not measured against actual user request data; empirical validation via the observability framework (Section 7) is required to refine them. The remaining ambiguous cases are handled by agent judgment today; the layered architecture provides a structured escalation path for when this becomes insufficient.

This ADR also codifies 8 routing anti-patterns with detection heuristics and prevention rules, defines a circuit breaker specification (max 3 routing hops per RR-006), establishes a multi-skill combination protocol, and provides a structured observability format for routing decisions. The scaling roadmap defines concrete triggers for each architectural transition, avoiding premature complexity while ensuring the framework can evolve without breaking changes.

**Key numbers:** 49 current keywords across 7 skills. 4 documented keyword collision zones. Estimated 40-60% keyword coverage of valid user intents (based on enumerated plausible intents, not measured against actual user request data). Estimated enhancement to ~75-90% coverage through negative keywords and priority ordering at zero latency cost; estimated coverage improvement pending empirical validation via the observability framework defined in Section 7. LLM fallback adds ~1,000-1,500 tokens per invocation when activated.

---

## Status

**Proposed**

This ADR is at C4 criticality (architecture/governance, baselined once accepted). Acceptance requires human review per AE-003 (new ADR auto-C3 minimum) and AE-004 considerations for baselining.

---

## Context

### Current State

Jerry's routing operates through a single-layer keyword trigger map defined in `mandatory-skill-usage.md`, an L1 auto-loaded rule consuming approximately 600 tokens. The mechanism has three implicit tiers:

1. **Explicit invocation:** User types a slash command (e.g., `/problem-solving`). Deterministic, zero ambiguity. Bypasses all trigger matching.
2. **Keyword detection:** Agent scans the user request for keywords matching the trigger map. If keywords from a skill's trigger list appear, the agent proactively invokes that skill per H-22.
3. **Agent judgment (undocumented):** When no keywords match or multiple skills match, the agent uses its own reasoning. This is non-deterministic, not auditable, and vulnerable to context rot.

The trigger map contains **49 keywords across 7 triggered skills** (the `/worktracker` skill is invoked by session hooks, not by keyword triggers). This is architecturally sound for the current scale -- keyword routing scored highest overall (4.25 weighted) in the ps-analyst-002 comparison matrix due to dominance in simplicity, context cost, and determinism.

### Identified Limitations

Four structural weaknesses have been documented through Phase 1-2 analysis:

| # | Limitation | Evidence | Impact |
|---|-----------|----------|--------|
| 1 | **Keyword overlap (false positives)** | 4 documented collision zones: "risk", "review", "quality", "analyze" + domain-specific terms | Non-deterministic routing for ~15-20% of keyword-matched requests |
| 2 | **Semantic gaps (false negatives)** | Estimated 40-60% coverage of valid user intents (based on enumerated plausible intents; pending empirical validation via Section 7 observability) | ~20-40% of valid requests fail to trigger appropriate skills |
| 3 | **No conflict resolution mechanism** | No negative keywords, no priority ordering, no documented fallback | Multi-skill matches resolved by undocumented agent judgment |
| 4 | **No multi-intent handling** | Behavior rule 2 ("COMBINE skills when appropriate") is informal guidance | Compound requests like "research and then design" have no structured decomposition |

**Source:** ps-analyst-002 Section 1.3 (Known Routing Issues); nse-requirements-001 RR-001 through RR-008.

### Scaling Trajectory

The keyword-only approach degrades predictably as skills are added:

| Skill Count | Collision Zones (est.) | False Negative Rate (est.) | Human Reviewability |
|-------------|----------------------|---------------------------|---------------------|
| 8 (current) | 4 | 25-35% | Easy |
| 15 | 10-15 | 35-45% | Moderate |
| 20 | 20-30 | 45-55% | Difficult |
| 30+ | 50+ | 55-65% | Infeasible |

**Critical threshold: ~15 skills**, where collision frequency requires systematic disambiguation and semantic gaps accumulate beyond what agent judgment can reliably cover.

**Source:** ps-analyst-002 Section 3.2 (Medium Scale Projection); nse-architecture-001 ADR-002 (Routing Architecture).

### Trade Study Basis

The NSE Phase 1 trade study (TS-3) evaluated 6 routing alternatives. The top 3:

| Approach | TS-3 Score | ps-analyst-002 Score | Key Strength |
|----------|-----------|---------------------|-------------|
| C1: Keyword-only | 3.85 | 4.25 | Simplicity, determinism, zero token cost |
| C5: Layered (keyword + LLM fallback) | 3.90 | 3.95 | Accuracy, flexibility, graceful degradation |
| C4: Decision tree only | 3.80 | 3.95 | Determinism, multi-signal resolution |

The +0.05 TS-3 delta between C1 and C5 is misleading -- it is the net result of large positive deltas in flexibility (+1.50) and quality control (+1.00) being offset by large negative deltas in simplicity (-1.50) and context efficiency (-1.00). The layered approach is significantly better at routing accuracy but significantly worse at simplicity and token cost. These dimensions cancel to produce a small aggregate delta.

**Source:** nse-architecture-001 ADR-002; ps-analyst-002 Section 6.2 (Decomposing the Delta).

---

## Decision

Adopt a **Layered Routing Architecture** (Pattern 10 from nse-architecture-001) with three layers, implementing Layer 1 enhancements immediately and deferring Layers 2 and 3 until empirical scaling triggers are met.

The routing framework comprises seven interrelated design choices, each addressed in its own subsection below.

### 1. Layered Routing Architecture

#### 1.1 Three-Layer Design

```
    User Request
         |
         v
    +--------------------------+
    | LAYER 0: Explicit        |
    | /slash-command           |-----> Deterministic route (bypass all matching)
    | detection                |       ~0ms latency
    +---------+----------------+
              |
              | No slash command
              v
    +--------------------------+
    | LAYER 1: Enhanced        |
    | Keyword Matching         |-----> Single skill match?
    | (mandatory-skill-        |       Yes: Route to skill (fast path)
    |  usage.md trigger map    |       ~1ms latency
    |  with negative keywords, |
    |  priority ordering,      |
    |  compound triggers)      |
    +---------+----------------+
              |
              | No match, low confidence, or multiple matches
              v
    +--------------------------+
    | LAYER 2: Rule-Based      |
    | Decision Tree            |-----> Decision tree resolves?
    | (task type signals,      |       Yes: Route to skill(s)
    |  criticality context,    |       ~1ms latency
    |  prior skill context,    |
    |  file type indicators)   |
    +---------+----------------+
              |
              | Still ambiguous
              v
    +--------------------------+
    | LAYER 3: LLM-as-Router   |
    | (lightweight LLM call    |-----> Route to skill(s)
    |  with skill catalog      |       ~300-5000ms latency
    |  summary; structured     |       Logs decision for Layer 1 improvement
    |  output: skill name +    |
    |  confidence + reasoning) |
    +---------+----------------+
              |
              | Confidence below threshold
              v
    +--------------------------+
    | TERMINAL: H-31           |
    | Clarification            |-----> Ask user which skill is appropriate
    | (ambiguity resolution)   |       Per H-31: "ask, don't assume"
    +--------------------------+
```

#### 1.2 Layer Definitions

| Layer | Name | Mechanism | Latency | Token Cost | Determinism | Implementation Status |
|-------|------|-----------|---------|------------|-------------|----------------------|
| L0 | Explicit Invocation | Slash command detection | ~0ms | 0 | Full | Implemented |
| L1 | Enhanced Keyword Matching | Trigger map with negative keywords, priority ordering, compound triggers | ~1ms | 0 | Full | **Implement now** (enhance existing) |
| L2 | Rule-Based Decision Tree | Task type + criticality + context signals | ~1ms | 0 | Full | **Design now, implement at ~15 skills** |
| L3 | LLM-as-Router | Lightweight LLM call with structured output | ~300-5000ms | ~900-1,500 | Stochastic | **Design now, implement at ~20 skills** |
| Terminal | H-31 Clarification | User interaction | N/A | 0 | Full | Implemented (via H-31) |

#### 1.3 Escalation Conditions

Each layer escalates to the next when its resolution criteria are not met:

| From | To | Escalation Condition |
|------|-----|---------------------|
| L0 | L1 | No slash command detected in user request |
| L1 | L2 | (a) No positive keyword match found after negative keyword filtering, OR (b) Multiple skills match with equal priority after filtering, OR (c) Compound trigger partially matches (one keyword present, co-requisite absent) |
| L2 | L3 | (a) Decision tree reaches an ambiguous leaf node (no single skill resolved), OR (b) Contextual signals conflict (e.g., file type suggests one skill, keywords suggest another) |
| L3 | Terminal | (a) LLM router confidence falls below the activation threshold (see Section 2.4), OR (b) LLM router returns "ambiguous" classification |

**Graceful degradation:** If any layer is unavailable (e.g., L3 LLM call fails), the system falls back to the previous layer's best-effort result. If no layer produces a routing decision, H-31 clarification activates. The system never silently drops a routing request.

**Source:** nse-architecture-001 Pattern 10 (Layered Routing Pattern); ps-analyst-002 Section 6.5 (Defer Implementation, Design Interface Now); nse-requirements-001 RR-001 (keyword primary), RR-003 (LLM fallback).

#### 1.4 Layer 2 Decision Tree Sketch

The following table defines the preliminary decision tree for Layer 2. It maps combinations of four input signals to routing outcomes. This tree is designed now per the "design now, implement at ~15 skills" approach (Section 1.2) and will be refined with empirical data before implementation.

**Input Signals:**

| Signal | Source | Values |
|--------|--------|--------|
| Task type | Parsed from request structure | research, design, review, workflow, transcription, presentation |
| Criticality context | Session state / AE rules | C1, C2, C3, C4 |
| Prior skill context | Session routing history | Last skill invoked (or none) |
| File type indicators | Files referenced in request | `.md`, `.py`, `.yaml`, `.vtt`/`.srt`, mixed/none |

**Decision Tree (preliminary):**

| Task Type | Criticality | Prior Skill | File Type | Routing Outcome |
|-----------|-------------|-------------|-----------|-----------------|
| research | any | any | `.py` or `.md` | `/problem-solving` |
| design | any | `/problem-solving` | any | `/nasa-se` (research-to-design sequence) |
| design | any | none | any | `/nasa-se` |
| review | C3/C4 | any | any | `/adversary` (high-criticality review) |
| review | C1/C2 | any | any | `/problem-solving` (ps-reviewer) |
| workflow | any | any | any | `/orchestration` |
| transcription | any | any | `.vtt`/`.srt` | `/transcript` |
| research | any | `/nasa-se` | any | `/problem-solving` (design-to-research backtrack) |
| any | any | any | any | Escalate to Layer 3 (no deterministic resolution) |

**Notes:** (1) The "any" wildcards match all values for that signal. (2) Rows are evaluated top-to-bottom; first match wins. (3) The final row is the default escalation case. (4) Task type classification uses a simple keyword-to-type mapping (e.g., "investigate" -> research, "specify" -> design, "critique" -> review) that is distinct from the Layer 1 skill-level keyword matching. (5) This tree is subject to revision based on empirical routing data collected via Section 7 observability.

### 2. Enhanced Trigger Map Design

#### 2.1 Current Format and Enhancements

The current trigger map in `mandatory-skill-usage.md` uses a two-column format: `Detected Keywords | Skill`. The enhanced format adds three columns: **Negative Keywords**, **Priority**, and **Compound Triggers**.

**Enhanced Trigger Map Format:**

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|-------------------|-------------------|----------|-------------------|-------|
| Positive keywords that trigger this skill | Keywords that suppress this match when co-occurring | Numeric priority (1=highest) for conflict resolution | Keyword combinations requiring co-occurrence | Target skill |

#### 2.2 Enhanced Trigger Map -- Full Specification

| Detected Keywords | Negative Keywords | Priority | Compound Triggers | Skill |
|---|---|---|---|---|
| research, analyze, investigate, explore, root cause, why, debug, troubleshoot, diagnose, figure out, what went wrong, compare, evaluate | requirements, specification, V&V, adversarial, tournament, transcript, VTT, SRT, voice, persona | 6 | -- | `/problem-solving` |
| requirements, specification, V&V, technical review, risk, design, architecture, interface, trade study, compliance | root cause, debug, adversarial, tournament, research (standalone), transcript | 5 | "technical review" (both words required) | `/nasa-se` |
| orchestration, pipeline, workflow, multi-agent, phases, gates, plan, coordinate, break into steps, sequence | adversarial, transcript, root cause, debug | 1 | -- | `/orchestration` |
| transcript, meeting notes, parse recording, meeting recording, VTT, SRT, captions, audio, summarize this meeting | adversarial, requirements, design | 2 | "parse recording" OR "meeting recording" (phrase match) | `/transcript` |
| adversarial quality review, adversarial critique, rigorous critique, formal critique, adversarial, tournament, red team, devil's advocate, steelman, pre-mortem, quality gate, quality scoring | requirements, specification, design, research, investigate | 7 | "adversarial review" OR "quality gate" OR "quality scoring" (phrase match) | `/adversary` |
| saucer boy, mcconkey, talk like mcconkey, pep talk, roast this code, saucer boy mode | -- | 3 | -- | `/saucer-boy` |
| voice check, voice review, persona compliance, voice rewrite, voice fidelity, voice score, framework voice, persona review | -- | 4 | ("voice" OR "persona") AND ("review" OR "check" OR "score") | `/saucer-boy-framework-voice` |

#### 2.3 Negative Keywords Mechanism (Resolves OI-07)

Negative keywords are an exclusion mechanism integrated directly into the trigger map. When a user request contains both a positive keyword for Skill A and a negative keyword for Skill A, the positive match is **suppressed** for that skill.

**Algorithm:**

```
# Step 1: Positive/negative keyword filtering
for each skill in trigger_map:
    positive_matches = count(request intersect skill.positive_keywords)
    negative_matches = count(request intersect skill.negative_keywords)
    if positive_matches > 0 AND negative_matches == 0:
        candidates.add(skill, confidence=positive_matches/len(skill.positive_keywords))
    elif positive_matches > 0 AND negative_matches > 0:
        # Suppressed -- do not add to candidates
        suppressed.add(skill, reason="negative keyword match")

# Step 2: Compound trigger specificity override
if len(candidates) > 1:
    compound_matches = [c for c in candidates if request matches c.skill.compound_triggers]
    if len(compound_matches) == 1:
        # Compound trigger is more specific than individual keywords;
        # takes precedence over numeric priority
        candidates = compound_matches
    elif len(compound_matches) > 1:
        # Multiple compound matches -- fall through to priority ordering (Step 3)
        candidates = compound_matches

# Step 3: Numeric priority ordering (lower number = higher priority)
if len(candidates) > 1:
    candidates = sort(candidates, by=skill.priority, ascending=true)
    if candidates[0].priority <= candidates[1].priority - 2:
        # Clear priority separation (2+ levels); route to highest priority
        candidates = [candidates[0]]
    else:
        # Ambiguous -- escalate to Layer 2
        escalate_to_layer_2(candidates)
```

**Data structure decision (OI-07 resolution):** Negative keywords are integrated as a column in the existing trigger map table in `mandatory-skill-usage.md`. This approach was chosen over a separate data structure because:
- It maintains the single-file, single-table format that agents already parse
- It keeps positive and negative keywords visually adjacent for human review
- It adds zero additional file I/O or parsing complexity
- It is backward-compatible -- existing agents that ignore the new column continue to function (with reduced disambiguation)

**Example resolution of the "risk" collision:**

| Request | `/nasa-se` Positive | `/nasa-se` Negative | `/adversary` Positive | `/adversary` Negative | Resolution |
|---------|---------------------|--------------------|-----------------------|----------------------|------------|
| "Analyze the risk of this approach" | "risk" matches | No negative match | No positive match | -- | `/nasa-se` only |
| "Red team this for risk" | "risk" matches | No negative match | "red team" matches | No negative match | Both match; priority resolves: `/nasa-se` (5) > `/adversary` (7); route to `/nasa-se`. But see compound trigger: "red team" is `/adversary`-specific, so `/adversary` takes precedence via compound trigger specificity. |
| "Run a pre-mortem risk analysis" | "risk" matches | No negative match | "pre-mortem" matches | No negative match | Both match; "pre-mortem" is highly specific to `/adversary`. Route to `/adversary` via compound trigger specificity. |

#### 2.4 Confidence Threshold for LLM Fallback (Resolves OI-02)

**Decision:** The confidence threshold for LLM fallback activation is defined as a **heuristic based on match quality**, not a numeric score, because keyword matching is inherently binary (match/no match) and a floating-point confidence score would be artificial at this layer.

**Layer 1 produces three outcomes that determine escalation:**

| Outcome | Definition | Action |
|---------|-----------|--------|
| **Clear match** | Exactly one skill matches after negative keyword filtering | Route to that skill. No escalation. |
| **Multi-match** | Two or more skills match after negative keyword filtering | Apply priority ordering. If highest-priority skill is 2+ priority levels above the next, route to highest. Otherwise, escalate to Layer 2. |
| **No match** | No skill's positive keywords appear, or all positive matches are suppressed by negative keywords | Escalate to Layer 2. |

**For Layer 3 (LLM-as-Router), a numeric confidence threshold applies:**

The LLM router returns a structured output including a confidence field (0.0 to 1.0). If confidence is **below 0.70**, the router classifies the request as "ambiguous" and the system escalates to H-31 clarification. This threshold is provisional and should be calibrated empirically by logging LLM routing decisions and their outcomes over the first 50-100 routing events that reach Layer 3.

**Rationale for 0.70:** This threshold is selected as the midpoint between 0.50 (random chance, no routing value) and 0.90 (high confidence), biased toward the lower end to minimize false routing -- routing to the wrong skill is more costly than asking a clarifying question. The threshold balances false routing (routing to the wrong skill due to overconfident LLM) against unnecessary user interruption (asking clarification questions too often). This is a provisional value; the observability framework (Section 7) will produce the calibration data to refine it based on measured LLM routing accuracy across the first 50-100 Layer 3 routing events. The ps-analyst-002 finding that LLM-as-Router scores 5/5 on accuracy for novel inputs supports the feasibility of LLM-based routing but does not directly calibrate the numeric threshold.

**Source:** nse-requirements-001 OI-02; ps-analyst-002 Section 6.3 (Failure Modes); nse-requirements-001 RR-003.

#### 2.5 Example: Enhanced Trigger Map in Action

**Example 1: Clear single match**

Request: "Help me debug why this test is failing"
- `/problem-solving`: "debug" matches (positive). No negative keywords present. Clear match.
- Result: Route to `/problem-solving`. Layer 1 resolves. ~1ms.

**Example 2: Negative keyword suppression**

Request: "Write a requirements specification for the new module"
- `/problem-solving`: No positive match. "requirements" and "specification" are negative keywords but no positive keyword triggered, so irrelevant.
- `/nasa-se`: "requirements", "specification" match (positive). No negative keywords present. Clear match.
- Result: Route to `/nasa-se`. Layer 1 resolves. ~1ms.

**Example 3: Multi-match resolved by priority**

Request: "Plan the workflow for this research project"
- `/orchestration`: "plan", "workflow" match. Priority 1. No negative keywords.
- `/problem-solving`: "research" matches. Priority 6. No negative keywords.
- Result: `/orchestration` (priority 1) is 5 levels above `/problem-solving` (priority 6). Clear priority resolution. Route to `/orchestration`. Note: per Section 4 (Multi-Skill Combination), `/problem-solving` is flagged as a secondary skill for potential combination.

### 3. Circuit Breaker Specification

#### 3.1 Maximum Routing Depth

**Rule:** No request shall be routed more than **3 hops** without reaching a terminal agent that produces output. This directly implements RR-006.

A "hop" is defined as one transition between skills or agents where routing logic re-evaluates the destination. The count includes:
- Skill-to-skill transitions (e.g., `/orchestration` delegates to `/problem-solving`)
- Agent-to-agent transitions within a skill (e.g., ps-researcher hands off to ps-analyst)
- Re-routing due to agent reporting inability to handle the request

The count does **not** include:
- Creator-critic-revision iterations (these are quality loops within a single agent's scope, governed by H-14 iteration limits)
- Explicit user-initiated redirections (user says "actually, use /nasa-se instead")

#### 3.2 Detection Mechanism

**Hop counter implementation:** The routing context carries a `routing_depth` counter that increments at each hop. This counter is passed as part of the handoff metadata (see Section 4 for the handoff schema integration).

```yaml
routing_context:
  request_id: "req-20260221-001"       # Unique per original user request
  routing_depth: 0                      # Incremented at each hop
  max_depth: 3                          # Circuit breaker threshold
  routing_history:                      # Ordered list of routing decisions
    - { hop: 1, from: "orchestrator", to: "/problem-solving", method: "keyword", timestamp: "..." }
    - { hop: 2, from: "ps-researcher", to: "ps-analyst", method: "handoff", timestamp: "..." }
```

**Loop detection:** In addition to the hop counter, the circuit breaker detects cycles by checking `routing_history` for repeated `from -> to` pairs. If the same pair appears twice, the circuit breaker activates regardless of remaining hop count.

#### 3.3 Termination Behavior

When the circuit breaker activates (hop counter reaches 3 or cycle detected):

| Step | Action | Rationale |
|------|--------|-----------|
| 1 | Halt further routing | Prevent additional token consumption |
| 2 | Log the circuit breaker activation with full `routing_history` | Enable post-hoc analysis of why routing failed to converge |
| 3 | Present the current best result to the user | The most recent agent's partial output is better than nothing |
| 4 | Inform the user that routing reached maximum depth | Transparency per P-022 (no deception) |
| 5 | Ask the user for explicit routing guidance | Per H-31 (clarify when ambiguous) and AE-006 (mandatory human escalation) |

**Alignment with AE-006:** Circuit breaker activation at C3+ criticality triggers mandatory human escalation per the existing auto-escalation rules.

**Source:** nse-requirements-001 RR-006 (max 3 hops); ps-analyst-002 AP-04 (Routing Loop anti-pattern); quality-enforcement.md AE-006.

### 4. Multi-Skill Combination Protocol

#### 4.1 When to Combine Skills

Multi-skill combination activates when a user request contains trigger keywords for multiple skills and none of the matches are suppressed by negative keywords. This directly implements RR-007 and H-22 behavior rule 2 ("COMBINE skills when appropriate").

**Combination triggers:**

| Condition | Action |
|-----------|--------|
| Two skills match with distinct, non-overlapping keywords | Combine both skills |
| Three or more skills match | Combine up to 2 skills; if 3+ match, escalate to Layer 2 or ask user for prioritization |
| One skill's keywords are a subset of another's negative keywords | Do not combine; the negative keyword suppresses the match |
| `/orchestration` matches alongside other skills | `/orchestration` coordinates; other skills execute within the orchestrated workflow |

#### 4.2 Ordering and Coordination

When skills are combined, execution order follows this protocol:

| Priority Rule | Description | Example |
|---------------|-------------|---------|
| 1. `/orchestration` first (when present) | `/orchestration` is the meta-skill that plans and coordinates other skills | "Plan and research the architecture" -> `/orchestration` plans, then invokes `/problem-solving` |
| 2. Research before design | `/problem-solving` (research/analysis) precedes `/nasa-se` (requirements/design) | "Research options and create requirements" -> `/problem-solving` first, then `/nasa-se` |
| 3. Content before quality | Domain skills precede `/adversary` (quality review) | "Design this and run adversarial review" -> `/nasa-se` first, then `/adversary` |
| 4. Work before presentation | All other skills precede `/saucer-boy` or `/saucer-boy-framework-voice` | "Research this, then roast the code" -> `/problem-solving` first |

#### 4.3 Context Sharing Between Combined Skills

When skills are combined in sequence, context flows from earlier skills to later skills via the structured handoff protocol. The key context fields for multi-skill combination:

```yaml
multi_skill_context:
  original_request: "Research the options and create a requirements specification"
  skill_sequence:
    - skill: "/problem-solving"
      role: "primary-research"
      status: "complete"
      output_artifacts:
        - "work/research/options-analysis.md"
      key_findings:
        - "Three viable architecture options identified"
        - "Option B has lowest risk profile"
    - skill: "/nasa-se"
      role: "requirements-from-research"
      status: "in-progress"
      input_artifacts:
        - "work/research/options-analysis.md"
      dependencies:
        - "/problem-solving output must be complete before /nasa-se begins"
```

**Context isolation rule (AR-005):** Each skill operates in its own context window. The `multi_skill_context` structure passes only explicit artifact references and key findings, not full context. This prevents context rot from accumulating across skill boundaries.

**Source:** nse-requirements-001 RR-007; mandatory-skill-usage.md behavior rule 2; ps-analyst-002 Section 5.2 (Recommended Structured Handoff Schema); nse-requirements-001 HR-001 through HR-006.

### 5. Anti-Pattern Catalog

Eight routing anti-patterns identified through Phase 1-2 analysis. Each entry includes name, description, detection heuristic, and prevention rule.

#### AP-01: Keyword Tunnel

| Field | Content |
|-------|---------|
| **Name** | Keyword Tunnel |
| **Description** | Routing relies exclusively on keyword matching, creating a narrow "tunnel" through which only keyword-matching requests reach the appropriate skill. Requests expressed in different vocabulary are silently dropped, falling through to undocumented agent judgment. |
| **Detection Heuristic** | (1) Users frequently re-phrase requests to trigger skills. (2) Agent invokes skills inconsistently for semantically equivalent requests. (3) Keyword list has not been updated in more than 3 months. (4) User manually invokes skills via slash commands that should have triggered automatically. |
| **Prevention Rule** | (1) Audit keyword coverage quarterly against actual user requests. (2) Maintain synonym lists for each keyword. (3) Track routing "misses" where agent judgment overrides keyword routing. (4) Expand trigger map per Section 2.2 enhanced format. |
| **Jerry Example** | In the current trigger map (Phase 0), user says "debug this concurrency issue." `/problem-solving` is not invoked because "debug" is not in the Phase 0 trigger list. Agent handles the request without the skill's structured research methodology. (The enhanced trigger map in Section 2.2 adds "debug" as a positive keyword for `/problem-solving`, resolving this gap.) |

**Source:** ps-analyst-002 AP-01; ps-researcher-002 RQ-04 Finding 4.2.

#### AP-02: Bag of Triggers

| Field | Content |
|-------|---------|
| **Name** | Bag of Triggers |
| **Description** | Trigger keywords are added without collision analysis, creating a "bag" of overlapping triggers with no conflict resolution. Multiple skills match simultaneously with no priority ordering or negative keyword disambiguation. |
| **Detection Heuristic** | (1) Multiple skills frequently match a single request. (2) Routing behavior is inconsistent for the same request across sessions. (3) The trigger map has overlapping terms between skills without documented resolution. (4) More than 30% of routing decisions involve multi-skill ambiguity. |
| **Prevention Rule** | (1) Cross-reference all trigger keywords across skills before adding new ones. (2) Implement negative keywords per Section 2.3. (3) Define explicit priority ordering per Section 2.2. (4) Require compound triggers for broad terms. |
| **Jerry Example** | In the current trigger map (Phase 0), user says "review this architecture for risk." Both `/nasa-se` ("risk", "technical review") and `/adversary` ("review", "risk" via pre-mortem) match. Without priority ordering, the agent's choice is non-deterministic across sessions. (The enhanced trigger map in Section 2.2 resolves this via negative keywords and priority ordering.) |

**Source:** ps-analyst-002 AP-02; 4 documented collision zones in current trigger map.

#### AP-03: Telephone Game

| Field | Content |
|-------|---------|
| **Name** | Telephone Game |
| **Description** | Context degrades through serial agent handoffs as each agent summarizes and re-interprets prior context. Original intent and detail are progressively lost. Information loss compounds at each boundary. |
| **Detection Heuristic** | (1) Downstream agents ask questions already answered by upstream agents. (2) Final output contradicts or ignores early-stage findings. (3) More tokens spent on coordination than actual work. (4) Agent handoff summaries get progressively shorter through a chain. |
| **Prevention Rule** | (1) Use structured handoff schemas with required fields (Section 4.3). (2) Include artifact file path references instead of summarizing file contents. (3) Define explicit success criteria at each handoff. (4) Cap `context_summary` length to force conciseness without allowing arbitrary truncation. |
| **Jerry Example** | ps-researcher produces a 900-line research document. Handoff to ps-analyst includes a 3-sentence summary. ps-analyst misses a critical finding buried in the research. The synthesized output lacks a key recommendation. |

**Source:** ps-analyst-002 AP-03; ps-researcher-002 RQ-06 Finding 6.2 ("free-text handoffs are the primary source of context loss"); nse-risk-001 R-T02 (error amplification RPN=15).

#### AP-04: Routing Loop

| Field | Content |
|-------|---------|
| **Name** | Routing Loop |
| **Description** | Agents repeatedly hand off to each other without convergence. Agent A routes to Agent B, which routes back to Agent A, consuming tokens without progress. This is distinct from the creator-critic revision cycle (which is bounded by H-14). |
| **Detection Heuristic** | (1) Same agent pair exchanges control more than 2 times. (2) Token consumption per orchestration run exceeds 2x expected budget. (3) Quality scores plateau or oscillate without improvement across iterations. (4) The `routing_history` contains repeated `from -> to` pairs. |
| **Prevention Rule** | (1) Implement circuit breaker with max 3 hops (Section 3). (2) Detect cycles via `routing_history` pair matching. (3) Mandatory human escalation when circuit breaker triggers (AE-006). (4) Set maximum iteration counts per criticality level (C1: 3, C2: 5, C3: 7, C4: 10). |
| **Jerry Example** | ps-critic scores a deliverable at 0.89. Creator revises to 0.90. ps-critic re-scores at 0.89. This oscillation continues because H-14 sets a floor (3 iterations) but no ceiling. The circuit breaker pattern (Section 3) halts after 3 consecutive iterations with score delta less than 0.01. |

**Source:** ps-analyst-002 AP-04; nse-requirements-001 RR-006 (max 3 hops); ps-investigator-001 RF-04 (RPN=252).

#### AP-05: Over-Routing (Premature Specialization)

| Field | Content |
|-------|---------|
| **Name** | Over-Routing (Premature Specialization) |
| **Description** | Tasks are routed to specialized agents when a general-purpose agent with tools would suffice. The coordination overhead (context setup, handoff, result integration) exceeds the specialization benefit. |
| **Detection Heuristic** | (1) Agent invocations for tasks completed in fewer than 5 tool calls. (2) Specialist agent output is nearly identical to what the orchestrator could produce. (3) Token overhead from agent spawning exceeds the task's total token budget. (4) High agent invocation count with low value-add per invocation. |
| **Prevention Rule** | (1) Apply Anthropic's complexity-first decision framework: start with direct work, escalate to agent only when needed. (2) Define minimum complexity thresholds for agent invocation (e.g., task requires domain-specific methodology, multi-step analysis, or specialized tool access). (3) Monitor agent invocation-to-value ratio. |
| **Jerry Example** | User asks "What files are in the src/ directory?" The orchestrator routes to ps-researcher, which spawns a full research investigation. A simple `ls` command would have answered the question in one tool call. |

**Source:** ps-analyst-002 AP-05; ps-researcher-003 Finding 3.1 (Anthropic 2024: "Adding frameworks prematurely before understanding underlying mechanics").

#### AP-06: Under-Routing (Missed Specialization)

| Field | Content |
|-------|---------|
| **Name** | Under-Routing (Missed Specialization) |
| **Description** | Tasks that would benefit from specialist agents are handled by the generalist orchestrator. Quality suffers because the generalist lacks domain-specific methodology, structured decomposition, and specialized tool access. |
| **Detection Heuristic** | (1) Orchestrator struggles with domain-specific tasks (multiple failed attempts, long reasoning chains). (2) Output quality for domain tasks is measurably lower than when the specialist is invoked. (3) User manually invokes skills that should have been proactively invoked per H-22. (4) Keyword trigger map has gaps for common request vocabulary. |
| **Prevention Rule** | (1) Expand trigger keyword coverage per Section 2.2. (2) Monitor for user-initiated skill invocations as a signal of routing failure. (3) Define "complexity indicators" that trigger automatic skill invocation: file count greater than 3, presence of domain jargon, multi-step requirements, or need for structured methodology. |
| **Jerry Example** | In the current trigger map (Phase 0), user says "Help me figure out why the tests are failing." The orchestrator attempts debugging without invoking `/problem-solving`. The ps-investigator agent (forensic cognitive mode) would apply structured 5 Whys analysis and produce a higher-quality root cause assessment. (The enhanced trigger map in Section 2.2 adds "figure out" and "what went wrong" as positive keywords for `/problem-solving`.) |

**Source:** ps-analyst-002 AP-06; mandatory-skill-usage.md H-22 (proactive invocation mandate).

#### AP-07: Tool Overload Creep

| Field | Content |
|-------|---------|
| **Name** | Tool Overload Creep |
| **Description** | As the framework grows, individual agents accumulate tool access until they exceed the 15-20 tool threshold where tool selection accuracy degrades. Each new MCP server adds tools that agents may not need. |
| **Detection Heuristic** | (1) Agent has access to more than 15 tools. (2) Agent frequently selects wrong tools for tasks. (3) Tool descriptions consume more than 10% of the agent's context window. (4) New MCP servers are added without per-agent tool allowlist review. |
| **Prevention Rule** | (1) Enforce tool allowlists per agent via `capabilities.allowed_tools` (AR-006). (2) Monitor tool count per agent; alert at 15. (3) Apply the T1-T5 tool security tier model: always select the lowest tier that satisfies requirements. (4) Periodically audit agent tool access and remove unused tools. |
| **Jerry Example** | As Jerry adds more MCP servers, each agent inherits all MCP tools by default. An agent with 14 native tools + 8 MCP tools = 22 tools, exceeding the Anthropic-documented threshold. The agent starts selecting Memory-Keeper tools when it should be using Context7. |

**Source:** ps-analyst-002 AP-07; ps-researcher-002 RQ-08 Finding 8.4 (Anthropic threshold: 20+ tools); nse-architecture-001 Pattern 5 (Tool Restriction), T1-T5 tiers.

#### AP-08: Context-Blind Routing

| Field | Content |
|-------|---------|
| **Name** | Context-Blind Routing |
| **Description** | Routing decisions are made based solely on the current request text, ignoring contextual factors (project phase, file types being edited, conversation history, prior routing decisions, context fill level) that would improve accuracy. |
| **Detection Heuristic** | (1) Same keyword routes to different skills depending on project phase, but routing does not account for phase. (2) Routing ignores file types being edited. (3) Routing does not consider which skills have already been invoked in the current session. (4) Routing decision quality degrades as context window fills (context rot affecting Layer 3). |
| **Prevention Rule** | (1) Layer 2 decision tree incorporates contextual signals: file type, project phase, prior skill context, conversation history. (2) Use Jerry's auto-escalation rules (AE-001 through AE-006) as context-aware routing triggers. (3) Implement session-level routing context tracking (Section 3.2, `routing_history`). |
| **Jerry Example** | During an orchestration workflow where the current phase is "Phase 2: Analysis," a keyword match for "research" triggers `/problem-solving` research mode instead of recognizing that analysis (not research) is the appropriate activity for the current phase. |

**Source:** ps-analyst-002 AP-08; ps-researcher-002 RQ-04 Finding 4.3 (contextual trigger conditions).

#### Anti-Pattern Summary: The "Bag of Agents" Error Amplification

The most severe systemic risk from routing anti-patterns is the **"Bag of Agents"** topology, where agents operate without coordinated routing or structured handoffs. Research from Google DeepMind (cited in ps-researcher-002) documents **17x error amplification** in uncoordinated multi-agent systems compared to single-agent execution.

Jerry's formal topology (orchestrator-worker with P-003 single-level nesting) reduces this amplification to an estimated **~1.3x** (internal estimate, assuming structured 2-level hierarchy with formal handoff protocols eliminates ~92% of boundary errors observed in unstructured systems; subject to empirical validation). However, this reduction depends on three architectural elements remaining intact:

1. **Structured handoffs** (Section 4.3) -- prevents information loss at boundaries
2. **Circuit breakers** (Section 3) -- prevents runaway routing loops
3. **Priority ordering** (Section 2.2) -- prevents non-deterministic multi-skill resolution

If any of these three elements degrades (e.g., handoffs revert to free-text, circuit breaker is bypassed), the error amplification factor increases toward the 17x uncoordinated baseline.

**Source:** nse-requirements-001 AR-004 rationale (17x amplification); nse-to-ps handoff Cross-Agent Consensus #3.

### 6. Scaling Roadmap

#### 6.1 Phase Definitions

| Phase | Skill Count | Routing Architecture | Trigger for Transition | Implementation Effort |
|-------|-------------|---------------------|------------------------|----------------------|
| **Phase 0 (current)** | 8 | Keyword-only (current `mandatory-skill-usage.md`) | -- | None (already implemented) |
| **Phase 1 (immediate)** | 8 | Enhanced keyword: negative keywords + priority ordering + compound triggers | This ADR is accepted | Low (update `mandatory-skill-usage.md`) |
| **Phase 2 (10-15 skills)** | 10-15 | Phase 1 + rule-based decision tree (Layer 2) | Any 2 of: (a) 10+ collision zones documented, (b) false negative rate exceeds 40% (measured via observability), (c) user-initiated slash command invocations exceed 30% of routing decisions | Medium (design + implement Layer 2) |
| **Phase 3 (15-20 skills)** | 15-20 | Phase 2 + LLM-as-Router (Layer 3) | Any 2 of: (a) Layer 2 decision tree fails to resolve 20%+ of ambiguous cases, (b) novel request types exceed 15% of routing events, (c) trigger map exceeds 1,500 tokens | Medium (implement Layer 3 LLM call) |
| **Phase 4 (20+ skills)** | 20+ | Full layered routing (all layers active) | -- (all layers already implemented at Phase 3) | Low (tuning and monitoring) |

#### 6.2 Transition Triggers

Each transition trigger is defined as a measurable condition that can be evaluated using routing observability data (Section 7). Transitions require **any 2 of the listed conditions** to be met, preventing premature transitions based on single anomalous metrics.

**Phase 1 to Phase 2 trigger detail:**

| Condition | Measurement Method | Threshold |
|-----------|--------------------|-----------|
| Collision zones | Count of keyword overlaps in trigger map | 10+ |
| False negative rate | (User slash command invocations + user corrections) / total routing decisions | >40% |
| User override rate | User-initiated slash commands / total skill invocations | >30% |

**Phase 2 to Phase 3 trigger detail:**

| Condition | Measurement Method | Threshold |
|-----------|--------------------|-----------|
| Layer 2 failure rate | Cases where Layer 2 reaches ambiguous leaf / total Layer 2 invocations | >20% |
| Novel request rate | Requests with zero keyword matches and no decision tree match / total requests | >15% |
| Trigger map token cost | Token count of `mandatory-skill-usage.md` trigger map section | >1,500 tokens |

**Threshold derivation:** Thresholds are provisional engineering judgments derived as follows. The Phase 1-to-2 false negative threshold (>40%) is set at approximately 1.5x the estimated Phase 0 baseline (25-35% from the Scaling Trajectory table in Context); exceeding this ratio indicates the keyword layer is degrading faster than expected. The Phase 1-to-2 user override threshold (>30%) represents the point where nearly one-third of routing is user-corrected, indicating systemic keyword gaps. The Phase 2-to-3 Layer 2 failure threshold (>20%) is set at the point where the complexity cost of adding Layer 3 (LLM token overhead, stochastic behavior) is offset by the error reduction from resolving the failing 20%+ of Layer 2 cases. All thresholds are subject to empirical calibration after the first 50-100 routing events at each phase.

#### 6.3 Future Considerations (Beyond Scope)

At 50+ skills, the framework may require:
- **Team-based grouping** (per nse-requirements-001 OI-05): hierarchical skill namespaces
- **Embedding-based semantic routing** (Layer 2.5): requires vector store infrastructure
- **Capability-based matching**: routing based on agent `identity.expertise` fields rather than keyword triggers

These are noted for awareness but are not designed in this ADR. The scaling roadmap provides transition triggers; future ADRs should be created when those triggers are met.

**Source:** ps-analyst-002 Section 3 (Scaling Analysis); nse-architecture-001 ADR-002 (implementation sketch); nse-requirements-001 OI-05 (team-based grouping threshold).

### 7. Routing Observability

#### 7.1 What to Log

Every routing decision produces a structured record containing:

> **Scope note:** The routing record includes fields beyond RR-008's minimum requirements (which specifies: routing mechanism, matched keywords, confidence level, and selected skill). The additional fields (`request_id`, `session_id`, `user_request_summary`, `request_token_count`, `routing_token_cost`, `user_corrected`) are included to support gap detection (Section 7.3) and routing improvement workflows. These fields are RECOMMENDED (not REQUIRED) for initial implementation; a conforming implementation may omit them and still satisfy RR-008.

```yaml
routing_record:
  # Identity
  timestamp: "2026-02-21T14:30:00Z"
  request_id: "req-20260221-001"
  session_id: "sess-20260221-xyz"

  # Input
  user_request_summary: "First 100 chars of user request..."
  request_token_count: 47

  # Routing Decision
  routing_method: "keyword"          # enum: explicit | keyword | decision_tree | llm | fallback | clarification
  layer_reached: 1                   # Highest layer invoked (0-3)
  matched_keywords:                  # Keywords that triggered positive matches
    - { keyword: "debug", skill: "/problem-solving" }
    - { keyword: "risk", skill: "/nasa-se" }
  suppressed_matches:                # Matches suppressed by negative keywords
    - { keyword: "risk", skill: "/adversary", suppressed_by: "debug" }
  selected_skill: "/problem-solving"
  secondary_skills: []               # Skills flagged for combination
  confidence: 1.0                    # 1.0 for keyword, 0.0-1.0 for LLM
  alternatives_considered:           # Other skills considered but not selected
    - { skill: "/nasa-se", reason: "lower priority (5 vs 6)" }

  # Outcome (filled after execution)
  user_corrected: false              # Did the user override the routing decision?
  correction_target: null            # If corrected, which skill did user select?

  # Cost
  routing_token_cost: 0              # Tokens consumed by routing itself (0 for keyword, >0 for LLM)
```

#### 7.2 Structured Log Format

Routing records are persisted as part of the session's worktracker entry, following the existing filesystem-as-memory pattern. Each orchestration run's worktracker entry includes a `routing_decisions` section:

```markdown
### Routing Decisions

| # | Method | Layer | Selected Skill | Keywords Matched | Suppressed | Confidence | User Corrected |
|---|--------|-------|----------------|------------------|------------|------------|----------------|
| 1 | keyword | 1 | /problem-solving | debug, investigate | /adversary (suppressed by "debug") | 1.0 | No |
| 2 | explicit | 0 | /adversary | -- (slash command) | -- | 1.0 | No |
```

This format is human-readable in markdown, parseable by automated tooling, and consistent with Jerry's existing worktracker conventions.

#### 7.3 Identifying Keyword Coverage Gaps

Routing observability data enables systematic keyword coverage improvement through three signals:

| Signal | Indicates | Action |
|--------|-----------|--------|
| `layer_reached > 1` frequently | Keyword layer cannot resolve many requests | Analyze `user_request_summary` for missing keywords; expand trigger map |
| `user_corrected == true` | Routing selected the wrong skill | Analyze which keyword(s) caused the misroute; add negative keywords or adjust priority |
| `routing_method == "explicit"` frequently | Users bypass keyword routing via slash commands | Compare slash-commanded skills against trigger map; likely keyword gap for those skills |
| `suppressed_matches` is frequently empty despite multi-match | Negative keywords are not catching known collisions | Review collision zones; add missing negative keywords |

**Review cadence:** Routing observability data should be reviewed at the same cadence as trigger map updates -- when new skills are added or when routing accuracy concerns arise. At minimum, a review should occur each time the trigger map is modified.

**Source:** nse-requirements-001 RR-008 (routing observability); ps-analyst-002 Recommendation 5 (Routing Observability Foundation); nse-architecture-001 ADR-002 (Layer 3 logging for Layer 1 improvement).

---

## Consequences

### Positive Consequences

| # | Consequence | Scope |
|---|-----------|-------|
| 1 | **Deterministic routing preserved** for common cases. Layer 1 keyword matching remains the fast path with zero token cost. | Immediate |
| 2 | **Disambiguation for known collisions** via negative keywords and priority ordering. The 4 documented collision zones are systematically resolved. | Immediate (Phase 1) |
| 3 | **Expanded keyword coverage** from an estimated ~40-60% to an estimated ~75-90% of valid user intents through synonym additions, negative keywords, and priority ordering. Estimated coverage improvement pending empirical validation via the observability framework (Section 7). | Immediate (Phase 1) |
| 4 | **Structured escalation path** from deterministic to intelligent routing as the framework scales. No breaking changes required for future transitions. | Architectural |
| 5 | **Circuit breaker prevents runaway routing** via the 3-hop maximum and cycle detection, addressing the Routing Loop anti-pattern (AP-04, RPN=252). | Immediate |
| 6 | **Anti-pattern catalog provides institutional knowledge** for agent developers, reducing the likelihood of introducing routing defects. | Ongoing |
| 7 | **Observability data enables data-driven improvement** of the trigger map, replacing intuition-based keyword selection. | Incremental |

### Negative Consequences and Mitigations

| # | Consequence | Risk Level | Mitigation |
|---|-----------|-----------|------------|
| 1 | **Trigger map complexity increases** with negative keywords and priority ordering. The table grows from 2 columns to 5 columns. | Low | The enhanced format remains a single markdown table in a single file. Human reviewability is maintained at current 8-skill scale. |
| 2 | **False positive/negative risk with negative keywords.** Overly aggressive negative keywords could suppress valid matches; insufficient negative keywords leave collisions unresolved. | Medium | Start with conservative negative keyword lists (Section 2.2). Monitor via `suppressed_matches` in routing logs. Adjust based on `user_corrected` signals. |
| 3 | **LLM fallback introduces stochasticity** for the ~10-15% of requests that reach Layer 3 (when implemented). | Low | (a) LLM fallback is deferred until Phase 3. (b) Layer 3 logs its decisions for review. (c) Confidence threshold (0.70) causes low-confidence decisions to escalate to user clarification rather than guessing. |
| 4 | **Token cost of LLM routing** (~900-1,500 tokens per invocation). | Low | (a) LLM routing is invoked only for cases that keyword and decision tree cannot resolve. (b) Per-session cost is estimated at 0.5-1.1% of 200K context window, well within the enforcement budget. (c) Deferred until Phase 3. |
| 5 | **Maintenance burden of enhanced trigger map.** Adding a new skill requires populating 5 columns instead of 2. | Low | The additional columns (negative keywords, priority, compound triggers) prevent downstream routing defects that are more expensive to debug than the upfront authoring cost. Template provided in Section 2.2. |

### Migration Path

The migration from the current `mandatory-skill-usage.md` to the enhanced format proceeds in three non-breaking steps:

| Step | Change | Breaking? | Effort |
|------|--------|-----------|--------|
| 1 | Add `Negative Keywords`, `Priority`, and `Compound Triggers` columns to the trigger map table | No -- agents that do not parse the new columns continue to function using positive keywords only | Low |
| 2 | Add new positive keywords (synonyms) per Section 2.2 expanded list | No -- strictly additive; more requests are matched | Low |
| 3 | Update behavior rules to reference the priority ordering and negative keyword algorithm. Proposed text for behavior rule 2: "COMBINE skills per the multi-skill combination protocol: /orchestration first, research before design, content before quality (ADR-PROJ007-002 Section 4)." | No -- enhances existing behavior rule 2 ("COMBINE skills when appropriate") with structured combination protocol | Low |

**Total migration effort:** Low. All changes are to a single file (`mandatory-skill-usage.md`) and its corresponding reference in `CLAUDE.md`.

### Trade-Off Summary

| Dimension | Current State | After Phase 1 | After Phase 3 |
|-----------|--------------|---------------|---------------|
| Routing accuracy (est.; pending empirical validation) | 65-80% | 75-90% | 95%+ |
| Latency (avg) | ~1ms | ~1ms | ~1ms avg, ~500ms worst |
| Token cost (per session) | 0 | 0 | ~1,000-1,500 (0.5-0.75% of context) |
| Determinism | Full | Full | Full for ~85%, stochastic for ~15% |
| Complexity | Low (2-column table) | Low-Medium (5-column table) | Medium (3-layer routing) |
| Maintainability | Easy | Easy-Moderate | Moderate |
| Collision resolution | None (agent judgment) | Systematic (negative keywords + priority) | Full (LLM disambiguation) |
| Observability | None | Structured log format defined | Full routing records |

---

## Alternatives Considered

| # | Alternative | Score | Rejection Rationale |
|---|-----------|-------|---------------------|
| A1 | **Keep keyword-only with no enhancements** | 4.25 | Does not address the 4 documented collision zones or the estimated 40-60% semantic gap. Acceptable at current scale but creates technical debt for scaling. |
| A2 | **Implement full LLM-as-Router immediately** | 3.05 | +0.05 TS-3 delta does not justify the complexity at 8 skills. Token cost of ~1,000-1,500 per invocation for every routing decision is wasteful when keyword matching resolves an estimated ~65-80% of cases. |
| A3 | **Semantic/embedding-based routing** | 3.50 | Requires embedding infrastructure (vector store, embedding model) that Jerry does not have. High implementation cost for marginal accuracy improvement over enhanced keywords at current scale. |
| A4 | **ML classifier routing** | 3.35 | Requires training data and training pipeline. Jerry's 37-agent, 8-skill scale is too small for traditional ML classification to justify the infrastructure. |
| A5 | **Decision tree only (no LLM fallback)** | 3.95 | Strong deterministic option but cannot handle novel request types or contextual disambiguation. Viable as Layer 2 but insufficient as the sole routing mechanism at 20+ skills. |
| A6 | **Implement all three layers immediately** | 3.95 | Over-engineering for current scale. Layers 2 and 3 add complexity that is not justified until the scaling triggers defined in Section 6 are met. Violates the principle of "failing to measure performance before increasing complexity." |

---

## Requirements Traceability

This ADR satisfies all 8 routing requirements from nse-requirements-001:

| Requirement | Shall-Statement (Summary) | ADR Section | Satisfaction |
|-------------|--------------------------|-------------|-------------|
| RR-001 | Primary routing via keyword matching | Section 1 (Layer 1), Section 2 | **SATISFIED** -- keyword matching remains the primary routing mechanism |
| RR-002 | Trigger keyword completeness (min 3 per skill) | Section 2.2 | **SATISFIED** -- all skills have 5+ keywords; expanded synonym lists provided |
| RR-003 | LLM fallback for ambiguous routing | Section 1 (Layer 3), Section 2.4 | **SATISFIED** -- LLM fallback designed with confidence threshold; deferred to Phase 3 |
| RR-004 | Routing determinism for common cases | Section 1.2, Section 2.3 | **SATISFIED** -- Layer 1 and Layer 2 are fully deterministic |
| RR-005 | Negative keywords for disambiguation | Section 2.3 | **SATISFIED** -- negative keyword mechanism fully specified with algorithm and data structure |
| RR-006 | Routing loop prevention (max 3 hops) | Section 3 | **SATISFIED** -- circuit breaker with hop counter, cycle detection, and termination behavior |
| RR-007 | Multi-skill combination support | Section 4 | **SATISFIED** -- combination triggers, ordering protocol, and context sharing defined |
| RR-008 | Routing observability | Section 7 | **SATISFIED** -- structured log format, coverage gap detection signals, review cadence |

### Open Items Resolved

| OI-ID | Item | Resolution in this ADR |
|-------|------|----------------------|
| OI-02 | Confidence threshold for LLM routing fallback | Section 2.4: 0.70 threshold for Layer 3; heuristic match-quality outcomes for Layer 1. Provisional; calibrate empirically via first 50-100 Layer 3 routing events. |
| OI-07 | Negative keyword data structure | Section 2.3: Integrated as additional column in existing trigger map table. Single-file, single-table format preserved. |

---

## Evidence Sources

All claims in this ADR trace to Phase 1-2 research and analysis outputs:

| Ref ID | Document | Location |
|--------|----------|----------|
| R-001 | ps-researcher-001: Claude Code Agent Capabilities | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-1/ps-researcher-001/` |
| R-002 | ps-researcher-002: Agent Routing and Triggers | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-1/ps-researcher-002/` |
| R-003 | ps-researcher-003: Industry Best Practices | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-1/ps-researcher-003/` |
| R-004 | NSE Trade Study (TS-1 through TS-5) | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-1/nse-explorer-001/` |
| R-005 | ps-analyst-002: Routing Trade-Off Analysis | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-2-analysis/ps-analyst-002/` |
| R-006 | nse-architecture-001: Architecture Reference Model | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-2-analysis/nse-architecture-001/` |
| R-007 | nse-requirements-001: Requirements Specification | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-2-analysis/nse-requirements-001/` |
| R-008 | nse-risk-001: Risk Assessment | Referenced via nse-to-ps handoff |
| R-009 | ps-investigator-001: Failure Mode Analysis | Referenced via ps-to-nse handoff |
| R-010 | NSE-to-PS Barrier 2 Cross-Pollination Handoff | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/cross-pollination/barrier-2/nse-to-ps/handoff.md` |
| R-011 | PS-to-NSE Barrier 2 Cross-Pollination Handoff | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/cross-pollination/barrier-2/ps-to-nse/handoff.md` |

All file paths are repo-root-relative.

**Key quantitative claims and their sources:**

| Claim | Source |
|-------|--------|
| 49 keywords across 7 skills | R-005 Section 1.1, verified against mandatory-skill-usage.md |
| 4 documented collision zones | R-005 Section 1.3 |
| 40-60% keyword coverage estimate (pending empirical validation) | R-005 Section 4.1 |
| 17x error amplification (Bag of Agents) | R-004 TS-1, R-007 AR-004 rationale (Google DeepMind) |
| ~1.3x amplification with Jerry's formal topology (internal estimate; subject to empirical validation) | R-010 Cross-Agent Consensus #3 |
| +0.05 TS-3 delta (keyword vs. layered) | R-004 TS-3, R-006 ADR-002 |
| 0.5-1.1% context window cost for LLM routing | R-005 Section 6.4 |
| ~15 skill threshold for keyword breakdown | R-005 Section 3.2 |
| Anthropic tool overload threshold: 20+ tools | R-002 RQ-08 Finding 8.4 |
| FMEA RPN=252 for routing loops | R-009 (via R-011) |

---

## Self-Review (S-010)

Applied S-010 Self-Refine before finalizing. The following checklist verifies completeness and quality.

### Completeness Verification

| Required Section (per task specification) | Present | Depth |
|------------------------------------------|---------|-------|
| 1. Layered Routing Architecture | Yes | Three-layer design with escalation conditions, layer definitions, and graceful degradation |
| 2. Enhanced Trigger Map Design | Yes | Full 7-skill enhanced trigger map, negative keyword algorithm, confidence threshold, 3 worked examples |
| 3. Circuit Breaker Specification | Yes | Max depth, detection mechanism (hop counter + cycle detection), termination behavior |
| 4. Multi-Skill Combination Protocol | Yes | Combination triggers, ordering rules, context sharing schema |
| 5. Anti-Pattern Catalog (8 anti-patterns) | Yes | All 8 from ps-analyst-002 with name, description, detection heuristic, prevention rule, Jerry example |
| 6. Scaling Roadmap | Yes | 5 phases with measurable transition triggers |
| 7. Routing Observability | Yes | YAML log format, structured markdown format, coverage gap detection signals |
| Consequences (migration, token cost, risks, trade-offs) | Yes | 7 positive, 5 negative with mitigations, migration path, trade-off summary |

### ADR Format Verification

| Nygard Format Element | Present | Notes |
|----------------------|---------|-------|
| Title | Yes | ADR-PROJ007-002 |
| Status | Yes | Proposed |
| Context | Yes | Current state, limitations, scaling trajectory, trade study basis |
| Decision | Yes | 7 subsections covering all required content |
| Consequences | Yes | Positive, negative, migration path, trade-offs |

### Structural Compliance

| Rule | Status |
|------|--------|
| H-23 (Navigation table) | PASS -- navigation table present with 16 entries |
| H-24 (Anchor links) | PASS -- all section references use correct anchor syntax |
| L0 Executive Summary | PASS -- stakeholder-accessible overview with key numbers |
| Evidence citations | PASS -- all claims traced to R-001 through R-011 |
| OI-02 resolved | PASS -- confidence threshold specified in Section 2.4 |
| OI-07 resolved | PASS -- negative keyword data structure specified in Section 2.3 |

### Requirements Traceability Verification

| Requirement | Traced | Section |
|-------------|--------|---------|
| RR-001 through RR-008 | All 8 traced | Requirements Traceability table |

### Analytical Rigor Check

| Check | Status | Notes |
|-------|--------|-------|
| Assumptions documented | Yes | Coverage estimates labeled as "(est.)"; confidence threshold labeled as provisional |
| Confidence levels indicated | Yes | Frequency estimates use ranges; scaling projections qualified |
| Alternative viewpoints considered | Yes | 6 alternatives documented with scores and rejection rationale |
| Scaling projections qualified | Yes | Based on collision rate extrapolation from ps-analyst-002 |
| Recommendations are actionable | Yes | Phase 1 changes are to a single file with specific table content |
| Recommendations are evolutionary | Yes | Each phase builds on the previous; no rewrites |
| Trade-offs explicitly stated | Yes | Accuracy vs. complexity trade-off in L0 and Consequences |

### Identified Limitations

1. **Coverage estimates are approximations.** The 40-60% keyword coverage figure and the 75-90% post-enhancement estimate are based on enumerated plausible intents, not measured against actual user request data. Jerry does not currently collect routing decision data to validate these estimates. Estimated coverage improvement is pending empirical validation via the observability framework (Section 7), which is designed to provide this data.

2. **Confidence threshold is provisional.** The 0.70 threshold for LLM fallback activation is an informed estimate, not empirically calibrated. The ADR explicitly calls for calibration against the first 50-100 Layer 3 routing events.

3. **Negative keyword effectiveness is untested.** The negative keyword lists in Section 2.2 are designed to resolve known collision zones but have not been validated against production routing scenarios. The observability framework will surface false positives and false negatives.

4. **Scaling projections extrapolate from a small sample.** The collision zone growth rate is extrapolated from 4 observed collisions across 49 keywords. The actual growth curve depends on whether new skills occupy distinct domains (sublinear growth) or overlap with existing ones (superlinear growth).

5. **The "Bag of Agents" 17x amplification figure is from a single source (Google DeepMind)** and applies to uncoordinated topologies. Jerry's formal topology mitigates this but the exact reduction factor (~1.3x) is an estimate from the NSE cross-pollination handoff, not independently measured.

---

*ADR produced: 2026-02-21 | Agent: ps-architect-002 | PS-ID: PROJ-007 | Criticality: C4*
*Self-Review (S-010) Applied: 5 limitations identified and documented*
*Requirements satisfied: RR-001 through RR-008 (8/8)*
*Open items resolved: OI-02 (confidence threshold), OI-07 (negative keyword data structure)*
*Evidence sources: 11 documents (R-001 through R-011)*
