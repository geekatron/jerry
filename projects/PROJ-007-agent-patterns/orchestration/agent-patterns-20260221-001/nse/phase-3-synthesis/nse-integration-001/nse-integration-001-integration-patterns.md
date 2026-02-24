---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Integration Patterns for Claude Code Agents in the Jerry Framework

> **Project:** PROJ-007-agent-patterns | **Agent:** nse-integration-001 v1.0.0
> **Date:** 2026-02-21 | **Status:** Draft | **Criticality:** C4
> **NASA Processes:** NPR 7123.1D Process 6 (Product Integration), Process 12 (Interface Management)
> **Cognitive Mode:** Convergent
> **Inputs:** PS Phase 2 Analysis (ps-analyst-002, ps-investigator-001), NSE Phase 2 Analysis (nse-architecture-001, nse-requirements-001), Barrier 2 Cross-Pollination Handoff

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language overview for stakeholders |
| [1. Handoff Protocol Standard](#1-handoff-protocol-standard) | Definitive JSON Schema for agent-to-agent handoffs |
| [2. Context Passing Conventions](#2-context-passing-conventions) | Standardized rules for context flow between agents |
| [3. Quality Gate Integration](#3-quality-gate-integration) | 4-layer quality architecture wired into the workflow |
| [4. Routing Integration](#4-routing-integration) | Layered routing with existing skill infrastructure |
| [5. Anti-Pattern Prevention](#5-anti-pattern-prevention) | Detection heuristics at integration points |
| [6. Circuit Breaker Design](#6-circuit-breaker-design) | Iteration ceilings and routing depth enforcement |
| [7. MCP Integration Patterns](#7-mcp-integration-patterns) | Context7 and Memory-Keeper usage standards |
| [8. N-Squared Interface Diagram](#8-n-squared-interface-diagram) | Interface matrix across skills, agents, quality gates, and MCP |
| [Traceability Matrix](#traceability-matrix) | Requirements to integration patterns mapping |
| [Self-Review (S-010)](#self-review-s-010) | Pre-delivery quality verification |
| [References](#references) | Source document list |

---

## L0: Executive Summary

This document defines the integration standards for Claude Code agents within the Jerry framework. It answers the question: **how do agents connect to each other, to tools, to quality gates, and to existing skill infrastructure?**

Eight integration domains are specified:

1. **Handoff Protocol.** A complete JSON Schema standardizes agent-to-agent handoffs with 9 required fields and 5 optional fields, replacing the current 4-field conceptual protocol in AGENTS.md. The schema treats handoffs as API contracts, not informal messages. Validation rules enforce completeness at send time and artifact existence at receive time.

2. **Context Passing.** Five conventions govern how context flows: artifacts over summaries (paths, never inline), key findings for orientation (3-5 bullets), confidence signaling (0-1 scale), criticality propagation (C-level flows through the chain), and blocker escalation (unresolved issues surfaced explicitly).

3. **Quality Gates.** The 4-layer quality architecture (schema validation, self-review, critic review, tournament mode) integrates at specific workflow points. The gate-at-handoff pattern requires quality verification BEFORE handoff delivery, preventing low-quality work from propagating downstream.

4. **Routing.** The layered routing architecture evolves `mandatory-skill-usage.md` with negative keywords, priority ordering, and an LLM fallback interface. The design is backward-compatible at current 8-skill scale and forward-compatible to 20+ skills.

5. **Anti-Pattern Prevention.** Detection heuristics for 8 routing anti-patterns and 2 structural anti-patterns are defined as integration-point checks. Each check is tied to a specific enforcement layer (L1-L5).

6. **Circuit Breakers.** Maximum iteration caps (C1:3, C2:5, C3:7, C4:10), quality score plateau detection (3 consecutive iterations with delta < 0.01), and maximum routing depth (3 hops) prevent unbounded resource consumption.

7. **MCP Integration.** Context7 and Memory-Keeper usage protocols are standardized with resolve-then-query and store-at-boundaries patterns. Filesystem fallback at `work/.mcp-fallback/` handles MCP server failures.

8. **N-Squared Diagram.** An interface matrix maps all inter-skill communication paths, quality gate insertion points, and MCP integration points across Jerry's 8-skill architecture.

These standards address the three consensus priorities from Phase 2 analysis: schema validation (highest single-impact enhancement), structured handoff protocol (addresses #1 failure source), and anti-pattern codification (10 anti-patterns with detection heuristics).

---

## 1. Handoff Protocol Standard

### 1.1 Design Rationale

Free-text handoffs are the #1 source of context loss in production multi-agent systems (Google, 2026; ps-analyst-002 Section 5). The existing AGENTS.md protocol defines a 4-field JSON structure (`from_agent`, `to_agent`, `context`, `request`) that is conceptually sound but insufficient: it lacks success criteria, criticality classification, iteration limits, and routing metadata.

This specification extends the AGENTS.md protocol into a validated API contract. It synthesizes:
- The ps-analyst-002 proposed schema (Section 5.2) with its `success_criteria`, `constraints`, and `routing_metadata` fields
- The nse-architecture-001 handoff schema (Section 2.1.2) with its `key_findings`, `blockers`, and `confidence` fields
- The nse-requirements-001 requirements HR-001 through HR-006 for structured handoff format, required fields, artifact path validation, state preservation, completeness verification, and handoff quality gates

### 1.2 Complete JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Jerry Agent Handoff Protocol v2",
  "description": "Structured handoff contract for agent-to-agent communication within the Jerry framework. Treats inter-agent handoffs as API boundaries, not informal messages.",
  "type": "object",
  "required": [
    "from_agent",
    "to_agent",
    "task",
    "success_criteria",
    "artifacts",
    "key_findings",
    "blockers",
    "confidence",
    "criticality"
  ],
  "properties": {
    "from_agent": {
      "type": "string",
      "description": "Sending agent identifier. Must match the agent's name field in its definition.",
      "pattern": "^[a-z]+-[a-z]+(-[a-z0-9]+)*$",
      "examples": ["ps-researcher-001", "nse-architecture-001"]
    },
    "to_agent": {
      "type": "string",
      "description": "Receiving agent identifier. Must match a registered agent in AGENTS.md.",
      "pattern": "^[a-z]+-[a-z]+(-[a-z0-9]+)*$",
      "examples": ["ps-analyst-001", "nse-integration-001"]
    },
    "task": {
      "type": "string",
      "description": "Clear, actionable description of what the receiving agent should accomplish. Scoped to a single deliverable.",
      "maxLength": 500,
      "minLength": 20
    },
    "success_criteria": {
      "type": "array",
      "description": "Explicit, verifiable conditions for task completion. Each criterion must be individually testable.",
      "items": {
        "type": "string",
        "minLength": 10
      },
      "minItems": 1,
      "maxItems": 7
    },
    "artifacts": {
      "type": "object",
      "description": "Input and output artifact references. All paths are repo-relative.",
      "required": ["input_files", "output_path"],
      "properties": {
        "input_files": {
          "type": "array",
          "description": "Files the receiving agent MUST read before starting work. Order indicates reading priority.",
          "items": { "type": "string" },
          "minItems": 1
        },
        "output_path": {
          "type": "string",
          "description": "Where the receiving agent MUST write its primary deliverable."
        },
        "reference_files": {
          "type": "array",
          "description": "Files the receiving agent MAY consult for additional context.",
          "items": { "type": "string" }
        }
      }
    },
    "key_findings": {
      "type": "array",
      "description": "Top 3-5 orientation bullets summarizing the sending agent's most important outputs. These prevent the cold-start problem where the receiving agent must read everything before understanding anything.",
      "items": {
        "type": "string",
        "minLength": 20
      },
      "minItems": 3,
      "maxItems": 5
    },
    "blockers": {
      "type": "array",
      "description": "Unresolved issues, open questions, or known limitations that the receiving agent should be aware of. Empty array is valid when no blockers exist.",
      "items": { "type": "string" }
    },
    "confidence": {
      "type": "number",
      "description": "Sender's self-assessed confidence in the quality and completeness of their output. 0.0 = no confidence, 1.0 = fully confident.",
      "minimum": 0,
      "maximum": 1
    },
    "criticality": {
      "type": "string",
      "description": "Deliverable criticality level per quality-enforcement.md. Determines quality gate rigor for the receiving agent's output.",
      "enum": ["C1", "C2", "C3", "C4"]
    },
    "constraints": {
      "type": "object",
      "description": "Boundaries and limitations for the receiving agent.",
      "properties": {
        "max_iterations": {
          "type": "integer",
          "description": "Maximum creator-critic-revision iterations before escalation. Defaults per criticality: C1=3, C2=5, C3=7, C4=10.",
          "minimum": 1,
          "maximum": 10
        },
        "scope_boundary": {
          "type": "string",
          "description": "What the receiving agent should NOT do. Explicit negative scope prevents scope creep."
        },
        "time_budget": {
          "type": "string",
          "description": "Approximate effort expectation.",
          "enum": ["single_pass", "focused_analysis", "thorough_investigation", "comprehensive_synthesis"]
        }
      }
    },
    "routing_metadata": {
      "type": "object",
      "description": "Metadata about how this handoff was triggered. Enables routing observability.",
      "properties": {
        "routing_method": {
          "type": "string",
          "description": "Which routing mechanism produced this handoff.",
          "enum": ["explicit", "keyword", "llm_fallback", "orchestration_plan"]
        },
        "routing_confidence": {
          "type": "number",
          "description": "Router's confidence in this routing decision.",
          "minimum": 0,
          "maximum": 1
        },
        "routing_history": {
          "type": "array",
          "description": "List of agents that have previously handled this task in the current chain. Used for loop detection.",
          "items": { "type": "string" }
        }
      }
    },
    "quality_context": {
      "type": "object",
      "description": "Quality-related context from prior iterations or upstream agents.",
      "properties": {
        "prior_score": {
          "type": "number",
          "description": "Quality score from the most recent S-014 evaluation, if applicable.",
          "minimum": 0,
          "maximum": 1
        },
        "iteration_count": {
          "type": "integer",
          "description": "Number of creator-critic-revision iterations completed so far.",
          "minimum": 0
        },
        "critic_findings": {
          "type": "array",
          "description": "Top deficiencies identified by the most recent critic evaluation.",
          "items": { "type": "string" }
        }
      }
    },
    "task_id": {
      "type": "string",
      "description": "Worktracker entry identifier for traceability.",
      "pattern": "^[A-Z]+-[0-9]+.*$"
    }
  }
}
```

### 1.3 Validation Rules

#### 1.3.1 Send-Side Validation (Before Handoff Delivery)

The sending agent or orchestrator MUST verify these conditions before delivering the handoff to the receiving agent:

| Rule ID | Check | Failure Action |
|---------|-------|----------------|
| SV-01 | All 9 required fields are present and non-empty | BLOCK: Do not deliver handoff; populate missing fields |
| SV-02 | `from_agent` matches a registered agent in AGENTS.md | BLOCK: Invalid sender identity |
| SV-03 | `to_agent` matches a registered agent in AGENTS.md | BLOCK: Invalid receiver identity |
| SV-04 | `key_findings` contains 3-5 items, each >= 20 characters | BLOCK: Insufficient orientation context |
| SV-05 | `confidence` is between 0.0 and 1.0 | BLOCK: Invalid confidence value |
| SV-06 | `criticality` is one of C1, C2, C3, C4 | BLOCK: Invalid criticality |
| SV-07 | `task` is between 20 and 500 characters | WARN: Task description too terse or verbose |
| SV-08 | `success_criteria` has at least 1 item | BLOCK: No definition of done |
| SV-09 | If `quality_context.prior_score` exists for C2+ and score < 0.92, critic_findings MUST be non-empty | WARN: Prior quality failure without documented deficiencies |

#### 1.3.2 Receive-Side Validation (Before Work Begins)

The receiving agent or orchestrator MUST verify these conditions before the receiving agent begins work:

| Rule ID | Check | Failure Action |
|---------|-------|----------------|
| RV-01 | All `artifacts.input_files` exist on the filesystem | BLOCK: Missing input artifacts; return to sender |
| RV-02 | `artifacts.output_path` parent directory exists (or can be created) | BLOCK: Invalid output location |
| RV-03 | If `routing_metadata.routing_history` is present, `to_agent` does not appear in the history | BLOCK: Routing loop detected (circuit breaker, see Section 6) |
| RV-04 | If `criticality` is C2+, `constraints.max_iterations` MUST be set | WARN: Set default per criticality table |
| RV-05 | `confidence` value is plausible relative to `blockers` (low confidence with zero blockers is suspicious) | WARN: Log for observability; do not block |

#### 1.3.3 Error Handling

| Failure Type | Response | Escalation |
|-------------|----------|------------|
| BLOCK on send-side | Return handoff to sender with specific missing-field list. Sender must populate fields before re-attempting. | After 2 consecutive BLOCK failures: escalate to orchestrator. |
| BLOCK on receive-side (missing artifacts) | Return to sender with list of missing file paths. Sender must verify and fix paths. | Immediate escalation if artifacts were expected to exist. |
| BLOCK on receive-side (routing loop) | Halt routing chain. Escalate to human per AE-006. | Mandatory. The task requires human disambiguation. |
| WARN | Log warning. Proceed with work. Include warning in receiving agent's context for awareness. | Accumulated WARNs above threshold (3 per handoff) trigger review. |

### 1.4 Handoff Examples

#### Example 1: Research-to-Analysis Handoff

```json
{
  "from_agent": "ps-researcher-001",
  "to_agent": "ps-analyst-001",
  "task": "Analyze the 57 identified agent patterns across 8 families and produce a gap analysis comparing Jerry's current implementation against industry best practices.",
  "success_criteria": [
    "Gap analysis covers all 8 pattern families with quantified implementation rates",
    "Each gap includes priority (P1/P2/P3), estimated effort, and impact assessment",
    "Traceability matrix maps each gap to its source research finding"
  ],
  "artifacts": {
    "input_files": [
      "projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-1/ps-researcher-001/ps-researcher-001-claude-code-agent-capabilities.md",
      "projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-1/ps-researcher-003/ps-researcher-003-industry-best-practices.md"
    ],
    "output_path": "projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-2-analysis/ps-analyst-001/ps-analyst-001-analysis.md",
    "reference_files": [
      "AGENTS.md",
      ".context/rules/quality-enforcement.md"
    ]
  },
  "key_findings": [
    "57 patterns identified across 8 families; Jerry implements 46/57 partially or fully (67% rate)",
    "Testing family has lowest maturity (2.1/5); Governance has highest (4.5/5)",
    "Schema validation is the highest-value single enhancement -- zero LLM cost, catches structural defects",
    "Free-text handoffs identified as #1 failure source in production multi-agent systems",
    "Context rot is the top FMEA risk (RPN 392) with no current monitoring"
  ],
  "blockers": [
    "Pattern count is approximation -- some patterns may be sub-patterns of others",
    "Industry benchmarks are from 2025-2026 sources; rapid evolution may change rankings"
  ],
  "confidence": 0.85,
  "criticality": "C3",
  "constraints": {
    "max_iterations": 7,
    "scope_boundary": "Do NOT propose implementation solutions -- scope is analysis and gap identification only",
    "time_budget": "thorough_investigation"
  },
  "routing_metadata": {
    "routing_method": "orchestration_plan",
    "routing_confidence": 1.0,
    "routing_history": ["ps-researcher-001"]
  },
  "task_id": "PROJ-007-e-002"
}
```

#### Example 2: Analysis-to-Synthesis Handoff (Post-Critic Iteration)

```json
{
  "from_agent": "ps-analyst-002",
  "to_agent": "ps-synthesizer-001",
  "task": "Synthesize the routing analysis and failure mode investigation into a unified recommendation set for the agent pattern guide, resolving any contradictions between the two analyses.",
  "success_criteria": [
    "Unified recommendation list with no internal contradictions",
    "Each recommendation traces to both routing analysis and FMEA findings",
    "Priority ordering justified with impact and effort estimates",
    "L0/L1/L2 output structure with executive summary"
  ],
  "artifacts": {
    "input_files": [
      "projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-2-analysis/ps-analyst-002/ps-analyst-002-analysis.md",
      "projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-2-analysis/ps-investigator-001/ps-investigator-001-investigation.md"
    ],
    "output_path": "projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-3-synthesis/ps-synthesizer-001/ps-synthesizer-001-synthesis.md",
    "reference_files": [
      "projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/cross-pollination/barrier-2/ps-to-nse/handoff.md"
    ]
  },
  "key_findings": [
    "Keyword routing scores highest (4.25) at current 8-skill scale but breaks at ~15 skills",
    "Structured handoff schema reduces information loss by estimated 40-60%",
    "Top 5 FMEA risks: context rot (RPN 392), handoff info loss (336), prompt drift (288), false positive scoring (280), routing loops (252)",
    "3 consensus priorities: schema validation, structured handoffs, anti-pattern codification"
  ],
  "blockers": [],
  "confidence": 0.88,
  "criticality": "C3",
  "constraints": {
    "max_iterations": 7,
    "scope_boundary": "Do NOT re-analyze or dispute the input findings -- scope is synthesis and harmonization only",
    "time_budget": "comprehensive_synthesis"
  },
  "routing_metadata": {
    "routing_method": "orchestration_plan",
    "routing_confidence": 1.0,
    "routing_history": ["ps-researcher-001", "ps-researcher-002", "ps-analyst-002", "ps-investigator-001"]
  },
  "quality_context": {
    "prior_score": 0.93,
    "iteration_count": 3,
    "critic_findings": [
      "Scaling projections lack sensitivity analysis for sublinear collision growth",
      "Token cost estimates should note model pricing may change"
    ]
  },
  "task_id": "PROJ-007-e-005"
}
```

---

## 2. Context Passing Conventions

### 2.1 Core Conventions

These five conventions govern how context flows between agents. All are HARD requirements for agent-to-agent communication.

| ID | Convention | Rule | Rationale | Violation Consequence |
|----|-----------|------|-----------|----------------------|
| CP-01 | Artifacts over summaries | Pass file paths in `artifacts.input_files`, NEVER inline file content in the handoff payload | Inline content inflates the handoff, duplicating tokens when the receiver reads the file anyway. Paths cost ~50 tokens; inline content costs ~5,000-50,000 tokens. | Context budget waste; potential context overflow before work begins |
| CP-02 | Key findings for orientation | Include 3-5 bullet points in `key_findings` summarizing the most important outputs | Prevents the "cold start" problem where the receiving agent must read all artifacts before understanding anything. 500-token orientation prevents 5,000-token cold read. | Receiver wastes context budget on unfocused reading |
| CP-03 | Confidence signaling | Include self-assessed `confidence` (0-1) on output quality | Allows downstream agents to allocate more scrutiny to low-confidence inputs. Confidence below 0.7 signals that the receiver should independently verify claims. | Receiver cannot prioritize validation effort |
| CP-04 | Criticality propagation | Propagate the `criticality` level (C1-C4) through the handoff chain. Criticality MUST NOT decrease through the chain. | Ensures quality gates are applied consistently. A C3 deliverable that passes through 3 agents must remain C3 at every handoff. Auto-escalation (AE-001 through AE-006) may increase but never decrease criticality. | Quality gate bypass; insufficient review of high-impact deliverables |
| CP-05 | Blocker escalation | List all unresolved issues in `blockers`. Mark persistent blockers (carried from prior handoffs) with `[PERSISTENT]` prefix. | Prevents silent information loss at handoff boundaries. Blockers that are not explicitly surfaced tend to disappear from downstream agents' awareness. | Unresolved issues silently dropped; downstream agents proceed on false assumptions |

### 2.2 Artifact Reference Standards

| Standard | Specification | Example |
|----------|---------------|---------|
| Path format | Repo-relative paths only. NEVER absolute system paths. | `projects/PROJ-007-agent-patterns/research/analysis.md` |
| File existence | All `input_files` MUST exist at handoff time (RV-01). | Validated by receive-side check |
| Ordering | `input_files` are listed in reading priority order (most important first). | The first file is the primary input; subsequent files provide supplementary context |
| Distinction | `input_files` = MUST read; `reference_files` = MAY consult | Input files are required for the task; reference files provide optional additional context |
| Content constraint | NEVER include raw file content in the handoff payload | Use paths. The receiving agent loads content selectively via Read tool. |

### 2.3 Confidence Interpretation Guide

| Confidence Range | Interpretation | Receiver Action |
|-----------------|----------------|-----------------|
| 0.90 - 1.00 | High confidence. Sender is satisfied with completeness and accuracy. | Normal processing. Trust key_findings for orientation. |
| 0.70 - 0.89 | Moderate confidence. Known gaps or uncertainties exist (documented in blockers). | Read input artifacts more carefully. Verify key claims independently. |
| 0.50 - 0.69 | Low confidence. Significant uncertainty. Results may be incomplete or partially validated. | Treat as preliminary. Cross-reference with other sources. Consider requesting additional research. |
| 0.00 - 0.49 | Very low confidence. Output is exploratory or speculative. | Do NOT rely on findings without independent verification. Escalate to orchestrator for guidance. |

### 2.4 Criticality Propagation Rules

| Scenario | Rule | Example |
|----------|------|---------|
| Normal chain | Criticality inherits from the initiating handoff and remains constant | C3 task -> C3 handoff -> C3 handoff |
| Auto-escalation trigger | If an agent's work triggers AE-001 through AE-006, criticality increases for all subsequent handoffs | Agent touches `.context/rules/` -> AE-002 fires -> escalate to C3 minimum |
| Multi-input merge | When a receiving agent receives inputs from multiple chains with different criticalities, adopt the HIGHEST | C2 input + C3 input = C3 for the merged deliverable |
| Decomposition | When a task is decomposed into subtasks, each subtask inherits the parent's criticality unless the parent is C4 and the subtask is provably independent | C3 parent -> C3 subtask; C4 parent -> C4 subtask (unless independence justified) |

---

## 3. Quality Gate Integration

### 3.1 4-Layer Quality Architecture

The quality enforcement architecture (quality-enforcement.md) defines 5 enforcement layers (L1-L5). Within the agent integration workflow, 4 quality gate layers operate at specific integration points:

```
+-----------------------------------------------------------------------+
|                   QUALITY GATE INTEGRATION MAP                        |
+-----------------------------------------------------------------------+
|                                                                       |
|  LAYER 1: SCHEMA VALIDATION (Deterministic, L3 enforcement layer)    |
|  +----------------------------------------------------------------+  |
|  |  WHEN: Before agent receives handoff (receive-side validation)  |  |
|  |  WHAT: JSON Schema validation of handoff payload                |  |
|  |        Artifact path existence check (RV-01)                    |  |
|  |        Routing loop detection (RV-03)                           |  |
|  |  COST: 0 tokens (deterministic check)                           |  |
|  |  IMMUNE TO CONTEXT ROT: Yes                                     |  |
|  +----------------------------------------------------------------+  |
|       |                                                               |
|       v  (handoff valid -- agent begins work)                         |
|                                                                       |
|  LAYER 2: SELF-REVIEW (Agent-internal, S-010)                        |
|  +----------------------------------------------------------------+  |
|  |  WHEN: Before agent produces final output (H-15)                |  |
|  |  WHAT: Completeness check against success_criteria               |  |
|  |        Structural compliance (H-23 nav tables, H-24 anchors)    |  |
|  |        Self-assessed quality against S-014 dimensions            |  |
|  |  COST: ~500-1,000 tokens (reasoning)                            |  |
|  |  IMMUNE TO CONTEXT ROT: Partially (degrades in deep context)    |  |
|  |  APPLIES TO: All criticality levels (C1-C4)                     |  |
|  +----------------------------------------------------------------+  |
|       |                                                               |
|       v  (self-review complete -- output ready for review)            |
|                                                                       |
|  LAYER 3: CRITIC REVIEW (Creator-Critic cycle, S-014)               |
|  +----------------------------------------------------------------+  |
|  |  WHEN: After agent completes output, before handoff delivery     |  |
|  |  WHAT: S-014 LLM-as-Judge 6-dimension scoring                   |  |
|  |        H-16 steelman before devil's advocate ordering            |  |
|  |        Per-dimension evidence citations                          |  |
|  |        Anti-leniency enforcement                                 |  |
|  |  COST: ~2,000-5,000 tokens per iteration                        |  |
|  |  IMMUNE TO CONTEXT ROT: Fresh scorer context per iteration       |  |
|  |  APPLIES TO: C2+ deliverables (H-14, minimum 3 iterations)      |  |
|  |  GATE: Score >= 0.92 weighted composite to pass (H-13)           |  |
|  +----------------------------------------------------------------+  |
|       |                                                               |
|       v  (quality gate passed -- handoff can be delivered)            |
|                                                                       |
|  LAYER 4: TOURNAMENT MODE (All 10 strategies, C4 only)              |
|  +----------------------------------------------------------------+  |
|  |  WHEN: After critic review converges for C4 deliverables         |  |
|  |  WHAT: All 10 selected adversarial strategies applied            |  |
|  |        S-001 Red Team, S-002 Devil's Advocate, S-003 Steelman,  |  |
|  |        S-004 Pre-Mortem, S-007 Constitutional AI Critique,       |  |
|  |        S-010 Self-Refine, S-011 Chain-of-Verification,           |  |
|  |        S-012 FMEA, S-013 Inversion, S-014 LLM-as-Judge          |  |
|  |  COST: ~15,000-30,000 tokens (full tournament)                   |  |
|  |  APPLIES TO: C4 only (irreversible, architecture/governance)     |  |
|  +----------------------------------------------------------------+  |
|                                                                       |
+-----------------------------------------------------------------------+
```

### 3.2 Gate-at-Handoff Pattern

Quality gates MUST pass BEFORE a handoff is delivered to the receiving agent. This is the core integration principle for quality:

```
Creator Agent                  Quality Gate                  Receiver Agent
     |                              |                              |
     |  1. Produce output           |                              |
     |----------------------------->|                              |
     |                              |                              |
     |  2. Self-review (S-010)      |                              |
     |  (internal to creator)       |                              |
     |                              |                              |
     |  3. Submit for scoring       |                              |
     |----------------------------->|                              |
     |                              |  4. Critic scores (S-014)    |
     |                              |                              |
     |  5a. Score >= 0.92 PASS      |                              |
     |<-----------------------------|                              |
     |                              |                              |
     |  6. Deliver handoff          |                              |
     |----------------------------->|----------------------------->|
     |                              |                              |
     |  5b. Score < 0.92 REJECT     |                              |
     |<-----------------------------|                              |
     |                              |                              |
     |  7. Revise based on          |                              |
     |     critic findings          |                              |
     |                              |                              |
     |  8. Re-submit (go to 3)      |                              |
     |----------------------------->|                              |
```

**Integration Rules:**

| Rule ID | Rule | Applies To |
|---------|------|------------|
| QGI-01 | Self-review (S-010) MUST complete before any external scoring or handoff delivery | All criticality levels |
| QGI-02 | Critic scoring (S-014) MUST produce a score >= 0.92 before handoff delivery | C2+ deliverables |
| QGI-03 | Quality score MUST be included in `quality_context.prior_score` when delivering the handoff | C2+ deliverables |
| QGI-04 | Critic findings from the final iteration MUST be included in `quality_context.critic_findings` | C2+ deliverables |
| QGI-05 | Tournament mode MUST complete before handoff delivery for C4 deliverables | C4 only |
| QGI-06 | If quality gate rejects after max_iterations, MUST escalate to human (AE-006 extension) | C2+ deliverables |

### 3.3 Quality Integration by Criticality

| Criticality | Layer 1 (Schema) | Layer 2 (Self-Review) | Layer 3 (Critic) | Layer 4 (Tournament) |
|-------------|------------------|----------------------|-------------------|---------------------|
| C1 (Routine) | REQUIRED | REQUIRED | OPTIONAL | N/A |
| C2 (Standard) | REQUIRED | REQUIRED | REQUIRED (3 min iterations) | N/A |
| C3 (Significant) | REQUIRED | REQUIRED | REQUIRED (3 min iterations) | N/A |
| C4 (Critical) | REQUIRED | REQUIRED | REQUIRED (3 min iterations) | REQUIRED |

### 3.4 Intermediate Quality Gates

For multi-agent pipelines (e.g., researcher -> analyst -> synthesizer), intermediate quality gates prevent cascade failures. These are lighter than full S-014 scoring:

| Gate Type | Check | Cost | Enforcement |
|-----------|-------|------|-------------|
| Completeness check | Are all required sections present in the intermediate output? | ~200 tokens | Orchestrator verifies before next handoff |
| Artifact existence | Do all referenced files exist? | 0 tokens (filesystem check) | Receive-side validation (RV-01) |
| Structural compliance | Does the output have H-23 navigation table and H-24 anchor links? | ~100 tokens (pattern match) | Schema validation |
| Constraint verification | Does the output respect `constraints.scope_boundary`? | ~300 tokens (reasoning check) | Self-review (Layer 2) |
| Blocker accumulation | Has the blocker count grown beyond threshold (> 5 unresolved)? | 0 tokens (count check) | Orchestrator review |

---

## 4. Routing Integration

### 4.1 Evolution of mandatory-skill-usage.md

The current trigger map in `mandatory-skill-usage.md` provides keyword-only routing. This section specifies how the trigger map evolves to support negative keywords, priority ordering, and LLM fallback without breaking the existing format.

#### 4.1.1 Enhanced Trigger Map Format

The trigger map evolves from a 2-column table (keywords, skill) to a 4-column table:

| Detected Keywords | Negative Keywords | Priority | Skill |
|-------------------|-------------------|----------|-------|
| research, analyze, investigate, explore, root cause, why, debug, troubleshoot, diagnose, compare | requirements, specification, V&V, adversarial, tournament, transcript, VTT, SRT | 6 | `/problem-solving` |
| requirements, specification, V&V, technical review, risk, design, architecture, trade study, compliance | root cause, debug, adversarial, tournament, research (when alone) | 5 | `/nasa-se` |
| orchestration, pipeline, workflow, multi-agent, phases, gates, plan, coordinate, sequence | adversarial, transcript, root cause | 1 | `/orchestration` |
| transcript, meeting notes, parse recording, meeting recording, VTT, SRT, captions, audio | -- | 2 | `/transcript` |
| adversarial quality review, adversarial critique, rigorous critique, formal critique, adversarial, tournament, red team, devil's advocate, steelman, pre-mortem, quality gate, quality scoring | requirements, specification, design, research, investigate | 7 | `/adversary` |
| saucer boy, mcconkey, talk like mcconkey, pep talk, roast this code, saucer boy mode | -- | 3 | `/saucer-boy` |
| voice check, voice review, persona compliance, voice rewrite, voice fidelity, voice score, framework voice, persona review | -- | 4 | `/saucer-boy-framework-voice` |

**Column Definitions:**

- **Detected Keywords:** Positive trigger keywords (existing behavior, expanded).
- **Negative Keywords:** When these terms co-occur with positive keywords, suppress the match for this skill. Enables disambiguation.
- **Priority:** Lower number = higher priority. When positive keywords match multiple skills after negative keyword filtering, the highest-priority (lowest-number) skill wins.
- **Skill:** Target skill for invocation.

**Priority Rationale:** `/orchestration` (1) is the meta-skill that invokes other skills and should coordinate. `/transcript` (2) and `/saucer-boy` (3) are narrow, domain-specific skills with low false-positive risk. `/saucer-boy-framework-voice` (4) is similarly narrow. `/nasa-se` (5) requires subject-matter context. `/problem-solving` (6) is the broadest scope. `/adversary` (7) is lowest because it is typically applied on top of other skills, not instead of them.

#### 4.1.2 Routing Resolution Algorithm

```
ROUTE(request):
  1. EXPLICIT CHECK: If request starts with "/<skill-name>", route directly.
     -> Return {method: "explicit", confidence: 1.0}

  2. KEYWORD MATCH: Scan request for positive keywords.
     For each matching skill:
       a. Check negative keywords. If any co-occur, suppress this skill.
       b. Record remaining matches with their priority.

  3. SINGLE MATCH: If exactly one skill matches after filtering:
     -> Return {method: "keyword", confidence: 0.95}

  4. MULTI-MATCH: If multiple skills match after filtering:
     a. Select the highest-priority (lowest number) skill.
     b. Apply multi-skill combination (H-22 behavior rule 2) if both
        skills are complementary (e.g., /problem-solving + /nasa-se).
     -> Return {method: "keyword", confidence: 0.80}

  5. NO MATCH: If no skill matches:
     a. If LLM fallback is available: invoke LLM router with skill
        descriptions and request text.
        -> Return {method: "llm_fallback", confidence: <llm_score>}
     b. If LLM fallback is not available (current state):
        i.  If request involves analysis or investigation:
            default to /problem-solving.
        ii. If request is ambiguous per H-31:
            ask the user which skill is appropriate.
        -> Return {method: "keyword", confidence: 0.50}
```

#### 4.1.3 LLM Fallback Interface

The LLM fallback layer is designed now but deferred for implementation until the skill count approaches 15. The interface definition ensures future addition is a non-breaking change:

```yaml
llm_routing_request:
  user_request: string            # The original user request
  available_skills:               # Skill descriptions loaded from SKILL.md
    - name: string
      description: string         # WHAT + WHEN + triggers (H-28)
      keywords: string[]          # Positive keywords
  context_signals:                # Optional contextual factors
    current_project: string       # Active JERRY_PROJECT
    recent_skills_invoked: string[] # Skills invoked in this session
    file_types_open: string[]     # Types of files currently being edited

llm_routing_response:
  selected_skill: string          # Primary skill to invoke
  secondary_skills: string[]     # Additional skills for combination
  confidence: float              # 0-1 confidence in selection
  reasoning: string              # Audit trail for routing decision
```

### 4.2 Multi-Skill Combination Protocol

When routing identifies that a request spans multiple skills (H-22 behavior rule 2: "COMBINE skills when appropriate"), the combination follows this protocol:

| Combination Pattern | Detection Signal | Sequencing | Example |
|--------------------|-----------------|------------|---------|
| Sequential (dependent) | Keywords from skill A appear in the "research/explore" phase AND keywords from skill B appear in the "design/build" phase | Invoke skill A first; pass output as input to skill B | "Research architecture options and write requirements" -> `/problem-solving` then `/nasa-se` |
| Parallel (independent) | Keywords from two skills appear in independent clauses of the request | Invoke both skills concurrently; synthesize outputs | "Analyze the code for bugs AND review the architecture for compliance" -> `/problem-solving` + `/adversary` in parallel |
| Embedded (quality layer) | `/adversary` keywords co-occur with another skill's keywords | Invoke primary skill first; apply `/adversary` as a quality layer on the output | "Do a thorough research analysis with adversarial critique" -> `/problem-solving` then `/adversary` |

---

## 5. Anti-Pattern Prevention

### 5.1 Routing Anti-Pattern Detection Heuristics

For each of the 8 routing anti-patterns identified by ps-analyst-002, the following table specifies detection heuristics that can be checked at integration points:

| Anti-Pattern | ID | Detection Heuristic | Integration Point | Enforcement Layer |
|-------------|-----|---------------------|-------------------|-------------------|
| **Keyword Tunnel** | APD-01 | Routing decision log shows > 30% of requests falling through to "no match" or "agent judgment" over a session | Post-routing audit | L4 (output inspection) |
| **Bag of Triggers** | APD-02 | Trigger map analysis shows > 10% collision rate (keywords matching multiple skills simultaneously) | Pre-deployment validation | L5 (CI/commit) |
| **Telephone Game** | APD-03 | `key_findings` in handoff N+1 contains fewer items than handoff N, OR `confidence` decreases by > 0.15 across consecutive handoffs without new blockers | Handoff delivery | L4 (output inspection) |
| **Routing Loop** | APD-04 | `routing_metadata.routing_history` contains a repeated agent name | Receive-side validation (RV-03) | L3 (deterministic gating) |
| **Over-Routing** | APD-05 | Agent invocation completes in < 3 tool calls, OR output is less than 500 tokens | Post-agent audit | L4 (output inspection) |
| **Under-Routing** | APD-06 | User manually invokes a skill (explicit `/skill` command) within 2 exchanges of a routing decision that chose a different skill | Session observation | L4 (output inspection) |
| **Tool Overload Creep** | APD-07 | Agent definition `allowed_tools` list exceeds 15 entries | Agent definition validation | L5 (CI/commit) |
| **Context-Blind Routing** | APD-08 | Same keyword routes to different skills in the same session without context change, OR routing ignores active project phase | Session observation | L4 (output inspection) |

### 5.2 Structural Anti-Pattern Detection

| Anti-Pattern | ID | Detection Heuristic | Integration Point | Enforcement Layer |
|-------------|-----|---------------------|-------------------|-------------------|
| **Telephone Game** (handoff completeness) | APD-09 | Compare total artifact count in handoff N vs. handoff N+1. If artifacts decrease without explicit rationale in `key_findings`, flag as potential information loss. | Handoff delivery | L4 |
| **Tool Overload Creep** (tool audit) | APD-10 | At agent definition time: count tools in `allowed_tools` + MCP tools assigned in TOOL_REGISTRY.yaml. Alert at 15; block at 20. | Agent registration | L5 (CI/commit) |

### 5.3 Prevention Rules Summary

| Rule ID | Prevention Rule | Source Anti-Pattern | Enforcement Mechanism |
|---------|----------------|--------------------|-----------------------|
| APR-01 | Trigger map MUST be reviewed for keyword coverage whenever a new skill is added | Keyword Tunnel (AP-01) | Checklist in skill creation template |
| APR-02 | Negative keywords MUST be defined for every skill with > 5 positive keywords | Bag of Triggers (AP-02) | Trigger map format validation |
| APR-03 | Handoff `key_findings` MUST contain 3-5 items covering the most important outputs | Telephone Game (AP-03) | Send-side validation (SV-04) |
| APR-04 | `routing_metadata.routing_history` MUST be populated in every handoff within a routing chain | Routing Loop (AP-04) | Orchestrator responsibility |
| APR-05 | Routing decisions MUST include complexity assessment before invoking multi-agent workflows | Over-Routing (AP-05) | Routing algorithm step 0 |
| APR-06 | User-initiated skill invocations SHOULD be logged as routing failure signals | Under-Routing (AP-06) | Session observability |
| APR-07 | Agent tool count MUST NOT exceed 15 (alert) or 20 (block) including MCP tools | Tool Overload Creep (AP-07) | Agent definition validation |
| APR-08 | Routing decisions SHOULD incorporate active project phase when available | Context-Blind Routing (AP-08) | LLM fallback context signals |

---

## 6. Circuit Breaker Design

### 6.1 Iteration Ceiling Enforcement

Maximum iteration counts per criticality level, complementing H-14's minimum of 3 iterations:

| Criticality | Min Iterations (H-14) | Max Iterations | Circuit Breaker Threshold | Rationale |
|-------------|----------------------|----------------|--------------------------|-----------|
| C1 (Routine) | 1 (self-review only) | 3 | Delta < 0.02 for 2 consecutive iterations | Simple work; diminishing returns after 3 |
| C2 (Standard) | 3 | 5 | Delta < 0.01 for 3 consecutive iterations | Moderate work; 5 iterations sufficient for convergence |
| C3 (Significant) | 3 | 7 | Delta < 0.01 for 3 consecutive iterations | Complex work; allow more iterations but prevent runaway |
| C4 (Critical) | 3 | 10 | Delta < 0.01 for 3 consecutive iterations | Highest-impact; most iterations but still bounded |

**Delta** = `score(iteration N) - score(iteration N-1)`. Measures quality improvement per iteration.

### 6.2 Maximum Routing Depth

Per RR-006, no request shall be routed more than 3 times without reaching a terminal agent:

| Routing Hop | Action | Example |
|-------------|--------|---------|
| Hop 1 | Normal routing via keyword or LLM fallback | User request -> `/problem-solving` |
| Hop 2 | Re-routing if first agent determines it is the wrong target | `/problem-solving` -> `/nasa-se` (agent determines the request is about requirements, not analysis) |
| Hop 3 | Final routing attempt; MUST reach a terminal agent | `/nasa-se` -> `nse-requirements-001` (terminal agent begins work) |
| Hop 4+ | BLOCKED by circuit breaker | Escalate to human per H-31 ("multiple valid interpretations") |

**Implementation via `routing_metadata.routing_history`:** Each routing hop appends the agent name to the routing history array. At receive-side validation (RV-03), if the array length exceeds 3, the circuit breaker fires.

### 6.3 Circuit Breaker Behavior

When a circuit breaker fires (either iteration ceiling or routing depth), the following behavior is mandatory:

```
Circuit Breaker Fires
       |
       v
[1. HALT current processing]
  Do NOT continue the iteration/routing chain.
       |
       v
[2. PERSIST current state]
  Write all accumulated artifacts to filesystem.
  Store state to Memory-Keeper if available.
       |
       v
[3. REPORT to orchestrator]
  Provide:
    - Which circuit breaker fired (iteration or routing)
    - Current quality score (if iteration breaker)
    - Routing history (if routing breaker)
    - Accumulated artifacts and their locations
    - Recommended next action (human review, scope reduction, etc.)
       |
       v
[4. ESCALATE to human]
  Per AE-006 extension: mandatory human escalation
  when circuit breaker triggers at C3+ criticality.
  For C1-C2: orchestrator may accept current output
  with documented quality gap.
```

### 6.4 Recovery Mechanism

After a circuit break, work can resume through one of these paths:

| Recovery Path | When to Use | Procedure |
|--------------|-------------|-----------|
| Human override | Human reviews the current state and provides direction | Human sets new constraints (revised scope, higher iteration ceiling, different approach). Resume with fresh agent context. |
| Scope reduction | Deliverable is too ambitious for the iteration budget | Reduce scope to achievable subset. Accept partial deliverable. Schedule remainder for separate task. |
| Approach change | Current approach is not converging | Restart with different methodology. Reset iteration counter. Use different agent or cognitive mode. |
| Accept with gap | Current quality is close to threshold (REVISE band: 0.85-0.91) | Accept output with documented quality gap. Mark in worktracker. Schedule improvement as follow-up. |

---

## 7. MCP Integration Patterns

### 7.1 Context7: Resolve-Then-Query Protocol

Context7 provides current documentation for external libraries and frameworks. MCP-001 mandates its use when any agent task references an external library by name.

**Protocol:**

```
Agent encounters external library reference
       |
       v
[1. resolve-library-id]
  Input: library name (e.g., "pydantic")
         + research question for relevance ranking
  Output: Context7-compatible library ID
       |
       +-- No match? Fall back to WebSearch for that library.
       |
       v
[2. query-docs]
  Input: library ID + specific question
  Output: Relevant documentation snippets
       |
       +-- Empty/irrelevant results? Fall back to WebSearch.
       |   Note "Context7 no coverage" in output.
       |
       v
[3. Integrate into reasoning]
  Cite the Context7 source in output.
  Respect the per-question call limit enforced by the tool.
```

**Call Limit Management:** The Context7 tool enforces a per-question call limit. To manage this:
- Batch related queries into a single specific question rather than making multiple narrow queries.
- Each distinct library resets the limit.
- If the limit is reached, fall back to WebSearch for remaining queries about that library.

### 7.2 Memory-Keeper: Store-at-Boundaries Pattern

Memory-Keeper provides cross-session context persistence. MCP-002 mandates store at phase boundaries and retrieve at phase start.

**Key Naming Convention:** `jerry/{project}/{entity-type}/{entity-id}`

| Entity Type | Use Case | Example Key |
|-------------|----------|-------------|
| `orchestration` | Workflow phase state | `jerry/PROJ-007/orchestration/agent-patterns-20260221-phase3` |
| `research` | Multi-session research findings | `jerry/PROJ-007/research/routing-analysis` |
| `phase-boundary` | Quality gate results at phase transitions | `jerry/PROJ-007/phase-boundary/phase2-qg-results` |
| `decision` | Architecture decisions | `jerry/PROJ-007/decision/handoff-schema-v2` |
| `requirements` | Requirements persistence | `jerry/PROJ-007/requirements/hr-001-through-hr-006` |
| `transcript` | Parsed transcript session data | `jerry/PROJ-007/transcript/standup-20260221` |

**Phase Boundary Integration:**

```
Phase N Agent(s) Complete
       |
       v
[1. Orchestrator collects phase outputs]
  Gather: artifact paths, quality scores,
          key findings, blockers, decisions
       |
       v
[2. Store to Memory-Keeper]
  Tool: context_save or context_checkpoint
  Key: jerry/{project}/orchestration/{workflow-slug}
  Value: JSON with phase summary, artifact list,
         quality scores, key decisions
       |
       v
[3. Deliver cross-pollination handoff]
  Write handoff.md to cross-pollination directory
  (filesystem persistence as backup)
       |
       v
Phase N+1 Begins
       |
       v
[4. Retrieve from Memory-Keeper]
  Tool: context_get or context_search
  Key/query: jerry/{project}/orchestration/{workflow-slug}
  Load prior phase context into new agent(s)
       |
       v
[5. Load handoff.md as supplementary context]
  Read the cross-pollination handoff for orientation
```

### 7.3 Fallback Behavior

When MCP tools fail, the following fallback chain applies:

| Failure | Primary Recovery | Filesystem Fallback | Observability |
|---------|-----------------|---------------------|---------------|
| Context7 `resolve-library-id` returns no matches | WebSearch for that library | N/A | Note "Context7 no coverage" in output |
| Context7 `query-docs` returns empty/irrelevant | WebSearch; note gap in output | N/A | Log "Context7 empty result" |
| Context7 call limit reached | WebSearch for remaining queries | N/A | Log "Context7 limit reached" |
| Memory-Keeper `context_save` fails (timeout, server down) | Persist to `work/.mcp-fallback/{key-with-slashes-replaced-by-dashes}.md` | YES | Note failure in worktracker entry |
| Memory-Keeper `context_get` returns empty | Search by partial key; if still empty, proceed without prior context | Check `work/.mcp-fallback/` for filesystem persisted state | Note "No prior context found" |
| MCP server unavailable | Continue work without MCP tools | Use filesystem-as-memory for all persistence | Log gap in session worktracker entry |

### 7.4 MCP Tool Access Governance

MCP tools are assigned to agents via TOOL_REGISTRY.yaml. The Agent Integration Matrix (mcp-tool-standards.md) defines which agents have access to which MCP tools.

**Integration Rules:**

| Rule | Specification |
|------|---------------|
| Tool access is declared, not implied | An agent only has MCP tool access if listed in TOOL_REGISTRY.yaml |
| Background subagents cannot use MCP | MCP tools are foreground-only (Claude Code constraint per R1-F5.2) |
| T4 agents must follow key pattern | `jerry/{project}/{entity-type}/{entity-id}` (no exceptions) |
| New agents must declare MCP needs | Agent definition file includes MCP tools in `capabilities.allowed_tools` (MCP-M-002) |
| MCP fallback is mandatory | Every MCP-using agent must implement the fallback chain (Section 7.3) |

---

## 8. N-Squared Interface Diagram

### 8.1 Skill-to-Skill Interface Matrix

The N-squared diagram shows interfaces between all 8 skills. Read as: the cell at row X, column Y shows what X sends to Y.

```
+==================+===============+===============+===============+===============+===============+===============+===============+===============+
|   TO ->          | /problem-     | /nasa-se      | /orchestr-    | /transcript   | /adversary    | /saucer-boy   | /sb-frmwk-    | /worktracker  |
|   FROM v         | solving       |               | ation         |               |               |               | voice         |               |
+==================+===============+===============+===============+===============+===============+===============+===============+===============+
| /problem-        |   [internal   | Research       |               |               | Deliverables  |               |               | Status        |
| solving          |   agent-to-   | findings ->    |               |               | for quality   |               |               | updates       |
|                  |   agent]      | requirements   |               |               | review        |               |               |               |
+------------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| /nasa-se         | Architecture  |   [internal    |               |               | Deliverables  |               |               | Status        |
|                  | questions ->  |   agent-to-    |               |               | for quality   |               |               | updates       |
|                  | research      |   agent]       |               |               | review        |               |               |               |
+------------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| /orchestr-       | Orchestration | Orchestration  |   [internal   | Parse         | QG triggers   |               |               | Phase         |
| ation            | -> research   | -> design      |   agent-to-   | requests      | for C2+       |               |               | state         |
|                  | tasks         | tasks          |   agent]       |               |               |               |               | updates       |
+------------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| /transcript      | Parsed data   |               |               |   [internal   |               |               |               |               |
|                  | -> analysis   |               |               |   agent-to-   |               |               |               |               |
|                  |               |               |               |   agent]       |               |               |               |               |
+------------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| /adversary       | Critique      | Critique       |               |               |   [internal   |               | Voice quality |               |
|                  | findings ->   | findings ->    |               |               |   agent-to-   |               | gate          |               |
|                  | revision      | revision       |               |               |   agent]       |               |               |               |
+------------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| /saucer-boy      |               |               |               |               |               |   [persona    |               |               |
|                  |               |               |               |               |               |   output]     |               |               |
+------------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| /sb-frmwk-       |               |               |               |               |               | Voice         |   [voice      |               |
| voice            |               |               |               |               |               | rewrite       |   gate]       |               |
|                  |               |               |               |               |               | feedback      |               |               |
+------------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
| /worktracker     |               |               | Integrity     |               |               |               |               |   [internal   |
|                  |               |               | audit ->      |               |               |               |               |   agent-to-   |
|                  |               |               | planning      |               |               |               |               |   agent]       |
+------------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+---------------+
```

### 8.2 Key Integration Points

```
LEGEND:
  [H]  = Handoff (structured handoff protocol v2)
  [QG] = Quality Gate insertion point
  [MK] = Memory-Keeper store/retrieve
  [C7] = Context7 resolve/query
  [CB] = Circuit Breaker check point

+===========================================================================+
|                    KEY INTEGRATION POINTS MAP                              |
+===========================================================================+
|                                                                           |
|  USER REQUEST                                                             |
|       |                                                                   |
|       v                                                                   |
|  +----------+                                                             |
|  | ROUTING  |----[CB: max 3 hops]                                        |
|  | DECISION |                                                             |
|  +----+-----+                                                             |
|       |                                                                   |
|       v                                                                   |
|  +-----------+    [MK: retrieve]     +-----------+                        |
|  | ORCH-     |<----------------------| Memory-   |                        |
|  | PLANNER   |                       | Keeper    |                        |
|  +-----+-----+                       +-----------+                        |
|        |                                                                  |
|        | [H: handoff v2]                                                  |
|        v                                                                  |
|  +------------+    [C7: resolve+query]    +-----------+                   |
|  | WORKER     |<--------------------------| Context7  |                   |
|  | AGENT      |                           +-----------+                   |
|  +-----+------+                                                           |
|        |                                                                  |
|        | output                                                           |
|        v                                                                  |
|  +------------+                                                           |
|  | SELF-REVIEW|----[QG: Layer 2]                                         |
|  | (S-010)    |                                                           |
|  +-----+------+                                                           |
|        |                                                                  |
|        v  (C2+ only)                                                      |
|  +------------+                                                           |
|  | CRITIC     |----[QG: Layer 3]----[CB: max iterations per C-level]     |
|  | REVIEW     |                                                           |
|  | (S-014)    |                                                           |
|  +-----+------+                                                           |
|        |                                                                  |
|        v  (C4 only)                                                       |
|  +------------+                                                           |
|  | TOURNAMENT |----[QG: Layer 4]                                         |
|  | (10 strats)|                                                           |
|  +-----+------+                                                           |
|        |                                                                  |
|        v                                                                  |
|  +------------+    [MK: store]       +-----------+                        |
|  | HANDOFF    |--------------------->| Memory-   |                        |
|  | DELIVERY   |----[QG: Layer 1]     | Keeper    |                        |
|  +-----+------+                      +-----------+                        |
|        |                                                                  |
|        | [H: handoff v2]                                                  |
|        v                                                                  |
|  +------------+                                                           |
|  | NEXT AGENT |                                                           |
|  | (or USER)  |                                                           |
|  +------------+                                                           |
|                                                                           |
+===========================================================================+
```

### 8.3 MCP Integration Points by Agent Role

| Agent Role | Context7 | Memory-Keeper | Integration Pattern |
|-----------|----------|---------------|---------------------|
| Research agents (ps-researcher, nse-explorer) | resolve + query | -- | Fetch-Cite-Integrate (C7 for library docs) |
| Analysis agents (ps-analyst, nse-architecture) | resolve + query | -- | Search-Narrow-Deep + C7 for API docs |
| Architecture agents (ps-architect) | resolve + query | store + retrieve + search | C7 for research; MK for decision persistence |
| Orchestration agents (orch-planner, orch-tracker) | -- | store + retrieve + search | Store-Checkpoint-Resume (MK at phase boundaries) |
| Synthesis agents (orch-synthesizer) | -- | retrieve + search | Retrieve prior phase context from MK |
| Transcript agents (ts-parser, ts-extractor) | -- | store + retrieve | Store parsed transcripts to MK for cross-session access |
| Requirements agents (nse-requirements) | -- | store + retrieve + search | Store requirements to MK for cross-session access |
| Adversary agents (adv-*) | -- | -- | Self-contained; no MCP integration by design |
| Worktracker agents (wt-*) | -- | -- | Read-only auditing; no MCP integration |
| Voice agents (sb-*, sbfv-*) | -- | -- | Self-contained persona operations |

---

## Traceability Matrix

### Integration Patterns to Requirements

| Integration Pattern | Requirement(s) | Source |
|--------------------|----------------|--------|
| Handoff JSON Schema v2 (Section 1) | HR-001, HR-002, HR-003, HR-005 | nse-requirements-001 |
| Send-side validation (Section 1.3.1) | HR-001 (structured format) | nse-requirements-001 |
| Receive-side validation (Section 1.3.2) | HR-003 (artifact path validation) | nse-requirements-001 |
| Gate-at-handoff (Section 3.2) | HR-006 (handoff quality gate) | nse-requirements-001 |
| State preservation via MK (Section 7.2) | HR-004 (state preservation) | nse-requirements-001 |
| Handoff completeness verification (Section 1.3.2) | HR-005 (completeness verification) | nse-requirements-001 |
| Context passing conventions (Section 2) | Architecture Section 2.1.3 | nse-architecture-001 |
| Routing resolution algorithm (Section 4.1.2) | RR-001, RR-003, RR-004, RR-005, RR-006 | nse-requirements-001 |
| Multi-skill combination (Section 4.2) | RR-007 | nse-requirements-001 |
| Quality gate integration (Section 3) | QR-001, QR-002, QR-004, QR-005, QR-008 | nse-requirements-001 |
| Circuit breaker (Section 6) | RR-006 (loop prevention) | nse-requirements-001 |
| MCP integration (Section 7) | SR-008 (MCP governance) | nse-requirements-001 |
| Anti-pattern prevention (Section 5) | AP-01 through AP-08 codification | ps-analyst-002 |
| N-squared diagram (Section 8) | Architecture Section 2.1 integration | nse-architecture-001 |

### Integration Patterns to Failure Modes

| Integration Pattern | Failure Mode(s) Mitigated | RPN | Source |
|--------------------|--------------------------|-----|--------|
| Handoff JSON Schema v2 | HF-01 (free-text info loss, RPN 336), HF-04 (telephone game, RPN 245) | 336, 245 | ps-investigator-001 |
| Circuit breaker design | RF-04 (routing loops, RPN 252) | 252 | ps-investigator-001 |
| Gate-at-handoff pattern | QF-02 (false positive scoring, RPN 280), OF-01 (cascade failure, RPN 140) | 280, 140 | ps-investigator-001 |
| Anti-leniency in quality gates | QF-02 (false positive scoring, RPN 280) | 280 | ps-investigator-001 |
| Routing resolution algorithm | RF-01 (misrouting, RPN 150), RF-02 (no-route, RPN 120), RF-03 (multi-route ambiguity, RPN 100) | 150, 120, 100 | ps-investigator-001 |
| MCP fallback behavior | TF-02 (tool unavailability, RPN 54) | 54 | ps-investigator-001 |
| Intermediate quality gates | OF-01 (cascade failure, RPN 140), QF-01 (quality gate bypass, RPN 140) | 140, 140 | ps-investigator-001 |

### Integration Patterns to Corrective Actions

| Integration Pattern | Corrective Action(s) Implemented | Source |
|--------------------|--------------------------------|--------|
| Handoff JSON Schema v2 | IA-02 (structured handoff schema) | ps-investigator-001 |
| Circuit breaker design | IA-01 (max iteration caps) | ps-investigator-001 |
| Quality gate integration | IA-03 (anti-leniency scoring) | ps-investigator-001 |
| Context passing conventions | IA-04 (context-centric decomposition) | ps-investigator-001 |
| Routing integration | SF-03 (routing enhancement) | ps-investigator-001 |
| Intermediate quality gates | SF-01 (intermediate quality gates) | ps-investigator-001 |

---

## Self-Review (S-010)

### Completeness Check

| Required Section | Status | Coverage |
|-----------------|--------|----------|
| 1. Handoff Protocol Standard | COMPLETE | Full JSON Schema with 14 fields; validation rules (9 send-side, 5 receive-side); error handling; 2 complete examples |
| 2. Context Passing Conventions | COMPLETE | 5 core conventions; artifact reference standards; confidence interpretation guide; criticality propagation rules |
| 3. Quality Gate Integration | COMPLETE | 4-layer architecture mapped to integration points; gate-at-handoff pattern; per-criticality matrix; intermediate quality gates |
| 4. Routing Integration | COMPLETE | Enhanced trigger map format with negative keywords and priority; routing resolution algorithm; LLM fallback interface; multi-skill combination protocol |
| 5. Anti-Pattern Prevention | COMPLETE | 8 routing anti-patterns + 2 structural anti-patterns with detection heuristics; 8 prevention rules; enforcement layer mapping |
| 6. Circuit Breaker Design | COMPLETE | Iteration ceilings per criticality; max routing depth of 3; circuit breaker behavior sequence; 4 recovery mechanisms |
| 7. MCP Integration Patterns | COMPLETE | Context7 resolve-then-query; Memory-Keeper store-at-boundaries; fallback chain; tool access governance |
| 8. N-Squared Interface Diagram | COMPLETE | 8x8 skill-to-skill matrix; key integration points map; MCP integration points by agent role |

### Quality Verification

| Criterion | Assessment |
|-----------|------------|
| **Source Traceability** | All integration patterns trace to Phase 2 analysis (ps-analyst-002, ps-investigator-001) and NSE Phase 2 (nse-architecture-001, nse-requirements-001). Traceability matrix maps patterns to requirements, failure modes, and corrective actions. |
| **Consistency with Existing Rules** | Patterns are consistent with quality-enforcement.md (H-13, H-14, H-15, H-16, H-17), mandatory-skill-usage.md (H-22), and mcp-tool-standards.md (MCP-001, MCP-002). No contradictions identified. |
| **Backward Compatibility** | Enhanced trigger map format extends (does not replace) the existing trigger map. Handoff Schema v2 is a superset of the AGENTS.md v1 schema. All changes are additive. |
| **Forward Compatibility** | LLM fallback interface is designed now, implemented later. Routing resolution algorithm has explicit extension points. Schema supports optional fields for future needs. |
| **Actionability** | Each section contains specific, implementable standards with validation rules, examples, and enforcement layer assignments. |
| **L0/L1/L2 Structure** | L0 executive summary (Section L0). L1 technical detail (Sections 1-8). No separate L2 section as this is an integration specification, not a strategic analysis; strategic implications are embedded in the L0 summary. |
| **Navigation** | H-23 compliant navigation table with H-24 anchor links at document top. |

### Identified Limitations

1. **Schema enforcement is prompt-level only.** The handoff schema validation rules (Section 1.3) describe what SHOULD be checked, but there is no deterministic hook (L3 enforcement) to enforce them today. Enforcement depends on agents following the schema specification in their system prompts. Hook-based enforcement (PM-02 from ps-investigator-001 corrective action plan) would make this deterministic.

2. **N-squared diagram is at skill level, not agent level.** An agent-level N-squared diagram (37x37) would be impractical to display in ASCII. The skill-level view captures the primary communication paths; intra-skill agent communication is documented in individual skill SKILL.md files.

3. **LLM fallback routing is interface-only.** The LLM fallback layer (Section 4.1.3) defines the interface but not the implementation. Implementation is deferred until the skill count approaches 15, per ps-analyst-002 recommendation.

4. **Anti-pattern detection heuristics require observability infrastructure.** Several detection heuristics (APD-01 through APD-08) depend on routing decision logging and session-level metrics that do not exist today. These heuristics become operational when routing observability (ps-analyst-002 Recommendation 5) is implemented.

5. **Circuit breaker recovery paths are advisory.** The recovery mechanisms (Section 6.4) describe options but do not mandate a specific recovery path. The appropriate recovery depends on context that cannot be fully specified in advance.

---

## References

### Phase 2 Analysis Documents

| ID | Document | Location |
|----|----------|----------|
| PS-Handoff-B2 | Barrier 2 Cross-Pollination: PS -> NSE | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/cross-pollination/barrier-2/ps-to-nse/handoff.md` |
| NSE-ARCH-001 | Agent Architecture Reference Model | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-2-analysis/nse-architecture-001/nse-architecture-001-architecture.md` |
| NSE-REQ-001 | Requirements Specification | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/nse/phase-2-analysis/nse-requirements-001/nse-requirements-001-requirements.md` |
| PS-ANALYST-002 | Routing and Trigger Architecture Analysis | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-2-analysis/ps-analyst-002/ps-analyst-002-analysis.md` |
| PS-INVEST-001 | Failure Mode Investigation | `projects/PROJ-007-agent-patterns/orchestration/agent-patterns-20260221-001/ps/phase-2-analysis/ps-investigator-001/ps-investigator-001-investigation.md` |

### Jerry Framework Rules

| ID | Document | Location |
|----|----------|----------|
| QE | Quality Enforcement SSOT | `.context/rules/quality-enforcement.md` |
| MSU | Mandatory Skill Usage | `.context/rules/mandatory-skill-usage.md` |
| MCP | MCP Tool Standards | `.context/rules/mcp-tool-standards.md` |
| AGENTS | Agent Registry | `AGENTS.md` |

### External Standards

| Standard | Relevance |
|----------|-----------|
| NPR 7123.1D Process 6 | Product Integration |
| NPR 7123.1D Process 12 | Interface Management |
| JSON Schema Draft 2020-12 | Handoff schema format |
| RFC 2119 | Priority keywords (MUST, SHOULD, MAY) |

---

*Generated by nse-integration-001 agent v1.0.0*
*NASA Processes: NPR 7123.1D Processes 6, 12*
*Self-Review (S-010) Applied: 5 limitations identified and documented*
*Criticality: C4 (integration standards are architecture-level, irreversible once adopted)*
*Traceability: Bidirectional to Phase 2 requirements (HR-001 through HR-006, RR-001 through RR-008, QR-001 through QR-009), failure modes (top 5 by RPN), and corrective actions (IA-01 through IA-04, SF-01, SF-03)*
