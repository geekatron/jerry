# ps-topic-researcher Tool Tier Analysis

**Date:** 2026-03-01
**Criticality:** C3 (Significant)
**Analysis Type:** Tool Tier Selection (Agent Development Standards H-34)
**Agent:** ps-topic-researcher (proposed)

---

## Executive Summary

**Recommended Tool Tier:** T3 (External)

**Reasoning:** ps-topic-researcher requires external information access (web search and documentation reading) to fulfill its research mission. The principle of least privilege mandates T3 because:

1. The agent MUST access WebSearch and WebFetch tools (external data requirement)
2. The agent MUST NOT access Task tool (worker agent, not orchestrator)
3. The agent MUST NOT access Write/Edit tools (outputs research findings as text only, does not persist to files)

T3 (External) is the lowest tier satisfying these requirements. T5 (Full) would violate the principle of least privilege by granting unnecessary Task tool access and inflating the agent's attack surface.

---

## Analysis Framework

### Step 1: Identify Required Tools

From the task description:

| Requirement | Tool(s) Needed | Tier |
|-------------|---|---|
| Search the web for current information | WebSearch | T3+ |
| Read relevant documentation pages | WebFetch, Context7 (for library docs) | T3+ |
| Produce structured research report | Text output only (no file write) | T1+ |
| Does NOT spawn sub-agents | NO Task tool | T1-T4 only |
| Does NOT persist state | NO Memory-Keeper | T1-T3 only |
| Does NOT write to files | NO Write/Edit tools | T1 or T3 only |

**Tools Actually Needed:**
- WebSearch (web discovery)
- WebFetch (documentation reading)
- Context7 (library/framework docs lookup) — optional, for higher-quality research outputs
- Possibly Bash (for diagnostic queries) — optional

**Tools Explicitly NOT Needed:**
- Task tool (worker agent constraint per P-003/H-01)
- Memory-Keeper (no cross-session state)
- Write/Edit (text output, no file persistence)

### Step 2: Map to Security Tiers

Per `agent-development-standards.md` [Tool Security Tiers](#tool-security-tiers):

| Tier | Tools Included | Match? | Rationale |
|------|---|---|---|
| **T1** (Read-Only) | Read, Glob, Grep | No | Missing WebSearch, WebFetch, Context7 (required for research) |
| **T2** (Read-Write) | T1 + Write, Edit, Bash | No | Task says agent does NOT write to files; T2 includes unneeded Write/Edit |
| **T3** (External) | T2 + WebSearch, WebFetch, Context7 | **YES** | Contains exactly the external tools needed; excludes Task |
| **T4** (Persistent) | T2 + Memory-Keeper | No | Task says agent does NOT persist state across sessions |
| **T5** (Full) | T3 + T4 + Task | No | Includes Task (unnecessary); violates least-privilege principle |

**Result:** T3 is the lowest tier whose tools match the agent's actual requirements.

---

## Rebuttal to T5 Argument

The senior developer's comment proposes T5 for "maximum flexibility" and "availability if we need it later." This reasoning violates core framework principles:

### Violation 1: Principle of Least Privilege (AR-006)

**Framework Standard:**
> "Always select the lowest tier that satisfies the agent's requirements." — `agent-development-standards.md`, Tool Security Tiers

**Why This Matters:**
- Each tool represents a capability boundary and potential attack surface
- Task tool allows delegation and sub-agent spawning — a capability ps-topic-researcher does not need
- Assigning T5 "just in case" creates an unconstrained agent that can later be misdirected into recursive delegation (violates P-003/H-01)

### Violation 2: Architectural Constraint P-003 (No Recursive Subagents)

**Constitutional Rule:**
> "No recursive subagents. Max ONE level: orchestrator -> worker." — quality-enforcement.md, H-01

**Current Architecture:**
```
If ps-topic-researcher is given Task tool (T5):
  ps-topic-researcher can spawn other agents
  → Those agents can spawn other agents
  → Unbounded recursion → context exhaustion → violation

If ps-topic-researcher is constrained to T3:
  ps-topic-researcher cannot spawn other agents
  → Can only return research findings to orchestrator
  → Orchestrator controls all delegation decisions
  → Single-level nesting maintained
```

**H-35 Enforcement:**
> "Worker agents (invoked via Task) MUST NOT include `Task` in the official `tools` frontmatter field." — agent-development-standards.md, HARD Rules

ps-topic-researcher will be invoked by an orchestrator (not invoked at the root level). It is a worker agent by definition. Worker agents MUST NOT have Task access. T5 would violate H-35 compliance.

### Violation 3: No Speculative Capability Assignment (Operational Standard)

**Framework Discipline:**
> "T5 requires explicit justification. The Task tool enables delegation; every T5 assignment MUST document why delegation is necessary." — agent-development-standards.md, Selection Guidelines

**Status of This Requirement:**
- Current task: "does not spawn sub-agents"
- Future task: hypothetical ("if we need it later")
- Justification: absent

Assigning T5 on speculative future need violates the documented standard. If future work genuinely requires ps-topic-researcher to delegate sub-tasks, the agent can be re-tiered at that time via a schema update and governance review.

---

## Tool Tier Decision Matrix

| Criterion | T3 | T5 | Notes |
|-----------|----|----|-------|
| Contains required tools (WebSearch, WebFetch, Context7) | ✓ Yes | ✓ Yes | T5 superset includes T3 |
| Lowest tier satisfying requirements | ✓ **Yes** | ✗ No | T3 is strictly lower than T5 |
| Includes unnecessary tools | ✗ No | ✓ Task tool | T5 adds Task, not needed |
| Respects least-privilege principle (AR-006) | ✓ **Yes** | ✗ No | Unnecessary tools = unnecessary surface area |
| Compatible with P-003 single-level nesting | ✓ **Yes** | ✗ No | T5 enables recursive delegation |
| Complies with H-35 worker constraint | ✓ **Yes** | ✗ No | H-35: workers MUST NOT have Task |
| Has documented justification for tier assignment | ✓ **Yes** | ✗ Speculative only | Decision is justified by principle, not by "maybe later" |

---

## Recommended Tool Tier Assignment

**Tool Tier:** T3 (External)

**Official Tools List (Claude Code Frontmatter):**
```yaml
tools:
  - WebSearch
  - WebFetch
  - Read
  - Glob
  - Grep
```

**MCP Servers (Claude Code Frontmatter):**
```yaml
mcpServers:
  context7: true
```

**Governance Tier (`.governance.yaml`):**
```yaml
tool_tier: T3
```

### Guardrails Required for T3 Agents

Per `agent-development-standards.md`, T3 agents MUST include citation guardrails:

```yaml
capabilities:
  allowed_tools:
    - WebSearch
    - WebFetch
    - Read
    - Glob
    - Grep
    - Context7

guardrails:
  output_filtering:
    - all_claims_must_have_citations
    - source_authority_tier_required
    - stale_data_warnings_mandatory
    - no_unsourced_conclusions
```

**Rationale:** External data (web search results, documentation pages) requires source attribution in research reports. The guardrails enforce citation discipline to prevent hallucination and ensure downstream users can verify findings.

---

## Implementation Notes

### Cognitive Mode

ps-topic-researcher performs **divergent** (exploratory) research. Per the cognitive mode guidance:

> "Divergent agents typically use T3+ tier (external access)" — agent-development-standards.md, Mode-to-Design Implications

T3 aligns with the expected cognitive mode for research agents.

### Model Selection

Divergent research agents typically use Opus for complex reasoning. Combined with T3 external access, this provides the exploration depth needed for comprehensive research without unnecessary delegation capability.

### Context Budget Considerations

Per CB-02 (Context Budget Standards):
> "Tool results SHOULD NOT exceed 50% of total context window."

Research agents that receive large WebFetch results from documentation should monitor tool result token allocation. This is a runtime concern, not a tier-selection concern — the T3 tier constraint itself does not prevent proper context budget management.

---

## Conclusion

**T3 (External) is the correct tier for ps-topic-researcher.**

This assignment:
- Grants the agent all tools required for research (WebSearch, WebFetch, Context7)
- Respects the principle of least privilege (AR-006)
- Enforces P-003 single-level nesting by excluding Task tool
- Complies with H-35 worker agent constraints
- Follows documented tier selection guidelines
- Includes appropriate guardrails for external data handling

T5 assignment would introduce unnecessary capabilities and violate the framework's architectural constraints. The senior developer's concern about "maximum flexibility" should be addressed through proper governance reviews if future work genuinely requires delegation — not through preemptive over-permission in the current agent definition.

---

## References

- `agent-development-standards.md` — Tool Security Tiers (H-34 compliance)
- `quality-enforcement.md` — H-01 (P-003), H-35 constraint, C3 criticality guidance
- Task description — "ps-topic-researcher receives a research topic..."
- Framework principles: AR-006 (least privilege), P-003 (single-level nesting), P-020 (user authority), P-022 (no deception)
