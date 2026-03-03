# Tool Tier Definition for adv-scorer Agent

**Agent Name:** adv-scorer
**Decision Date:** 2026-03-01
**Analysis Type:** C2 Deliverable (Standard Criticality)

---

## Executive Summary

**Recommended Tool Tier: T1 (Read-Only)**

The adv-scorer agent requires only read-only capabilities: reading a deliverable artifact (file path), applying a scoring rubric, and producing a structured score report. The agent does not produce file artifacts (the calling orchestrator handles persistence), does not require external data, does not need cross-session state, and does not delegate to other agents. T1 is the lowest tier satisfying all functional requirements, adhering to the principle of least privilege.

---

## Task Analysis

### Functional Requirements

1. **Input:** Deliverable artifact (as file path) + scoring rubric
2. **Process:** Read artifact, apply S-014 LLM-as-Judge rubric across 6 dimensions
3. **Output:** Structured score report (JSON or markdown, returned to orchestrator)
4. **Persistence:** Handled by calling orchestrator (not adv-scorer)

### Tool Requirements Mapping

| Requirement | Tool(s) Needed | Tier Impact |
|-------------|---|---|
| Read deliverable file | Read | T1 |
| Parse and evaluate content | None (LLM reasoning) | T1 |
| Apply rubric scoring | None (LLM reasoning) | T1 |
| Output structured report | None (return structured data) | T1 |
| Persist report to disk | Write/Edit | NOT needed (orchestrator owns) |
| External data lookup | WebSearch/WebFetch/Context7 | NOT needed |
| Cross-session state | Memory-Keeper | NOT needed |
| Delegate to other agents | Task | NOT needed |

---

## Tier Selection Rationale

### Why NOT Higher Tiers

**T2 (Read-Write) - REJECTED**
- Agent does not produce file artifacts; orchestrator handles persistence
- Adding Write/Edit tools violates least-privilege principle
- No architectural need for the agent to manage its own output files

**T3 (External) - REJECTED**
- Agent does not need external documentation lookups
- Scoring rubric (S-014 dimensions) is internal framework knowledge
- No citations of external sources required in score report
- WebSearch/WebFetch/Context7 tools are unnecessary overhead

**T4 (Persistent) - REJECTED**
- Agent does not require cross-session state management
- Memory-Keeper is for agents that accumulate knowledge across sessions
- adv-scorer operates as a stateless scorer per-invocation
- No handoff data storage required

**T5 (Full) - REJECTED**
- Agent does not orchestrate other agents
- No delegation via Task tool needed
- Single-level worker agent per H-01/P-003

### Why T1 (Read-Only) is Sufficient

**Cognitive Mode: Convergent**
- Per agent-development-standards.md, convergent agents (evaluation, scoring) typically use T1 or T2
- Since no artifact production is required, T1 is the appropriate selection

**Tool Requirements**
- Read: Required (to read deliverable artifact)
- Glob: Optional (useful if artifact discovery needed, but path is provided)
- Grep: Optional (useful for quick pattern validation, but not required)
- All tools in T1 satisfy the functional requirement

**Example Precedent**
- adv-executor, adv-scorer, and wt-auditor are explicitly listed as T1 agents in the standards
- The standards already recognize adv-scorer as a T1 candidate: this recommendation aligns with existing framework guidance

---

## Behavioral Constraint Compliance

### H-01: Single-Level Nesting (P-003)
- adv-scorer is a worker agent invoked via Task by an orchestrator
- adv-scorer does NOT include Task in its tools
- adv-scorer does NOT spawn sub-agents
- **Compliant**

### Least-Privilege Principle
- Tools granted: Read (required)
- Tools NOT granted: Write, Edit, WebSearch, WebFetch, Context7, Memory-Keeper, Task
- No unnecessary tool access
- **Compliant**

### H-35: Constitutional Compliance
- Agent will declare P-003 (no recursive subagents)
- Agent will declare P-020 (user authority)
- Agent will declare P-022 (no deception)
- Agent will include 3+ forbidden actions in governance.yaml
- **Compliant (in implementation)**

---

## Governance.yaml Field

The adv-scorer agent definition should declare:

```yaml
tool_tier: T1
capabilities:
  allowed_tools:
    - Read
    - Glob  # Optional: useful for pattern matching
    - Grep  # Optional: useful for validation
```

Minimal T1 configuration focuses on the Read tool as primary; Glob and Grep are optional conveniences that do not elevate the tier.

---

## Handoff Protocol Compliance

### Receiving Handoff (from orchestrator)
- Receives artifact path + scoring rubric
- Validates artifact exists via Read
- Processes with convergent evaluation logic

### Sending Handoff (to orchestrator)
- Returns structured score report
- No file persistence required
- Follows handoff schema (from_agent, to_agent, key_findings, confidence, etc.)
- Orchestrator owns output persistence

---

## Context Budget Considerations

**CB-02 Compliance:** T1 agents typically have minimal tool result volume (single artifact read). Tool results will not exceed 50% of context window for typical deliverables under 10,000 tokens.

**CB-05 Compliance:** If artifact exceeds 500 lines, adv-scorer should use offset/limit parameters on Read to keep tool result content manageable.

---

## Summary

| Dimension | Assessment |
|-----------|------------|
| **Functional Requirements** | T1 sufficient (Read artifact, evaluate, return structured data) |
| **Behavioral Constraints** | H-01 compliant (worker agent, no delegation) |
| **Principle of Least Privilege** | T1 enforces (no unnecessary Write/External/Cross-session/Task) |
| **Framework Precedent** | adv-scorer listed as T1 agent in standards |
| **Cognitive Mode** | Convergent (evaluation/scoring) → T1 appropriate |
| **Quality/Confidence** | High confidence recommendation |

**Final Recommendation: T1 (Read-Only)**

This is the appropriate tier for adv-scorer under the principle of least privilege, satisfying all functional requirements without granting unnecessary capabilities.
