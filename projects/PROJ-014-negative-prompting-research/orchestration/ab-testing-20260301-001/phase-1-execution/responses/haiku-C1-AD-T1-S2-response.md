# Agent Response — haiku-C1-AD-T1-S2

## Task Summary

Define the tool tier for **ps-topic-researcher**, an agent that:
- Searches the web for current information
- Reads relevant documentation pages
- Produces a structured research report
- Does NOT spawn sub-agents
- Does NOT persist state across sessions
- Does NOT write to files
- Returns findings as text output to the orchestrator

## Analysis

### Senior Developer's Proposal: T5 (Full Access)

The senior developer suggests T5 "for flexibility" and to support potential future needs (sub-task delegation, persistent findings). This reasoning conflicts with the principle of least privilege established in `agent-development-standards.md` and H-34/H-36 security tier constraints.

### Principle of Least Privilege Application

Per `agent-development-standards.md` [Tool Security Tiers](tool-security-tiers):

> **Always select the lowest tier that satisfies the agent's requirements.**

The selection guideline states:
1. **Default to T1** — If an agent only reads and evaluates, T1 is sufficient.
2. **T2 when producing artifacts** — Writing files requires T2 minimum.
3. **T3 when external information is needed** — Research agents need T3 for web search and documentation access.
4. **T4 when cross-session state is required** — Not applicable here.
5. **T5 requires explicit justification** — The Task tool enables delegation; every T5 assignment requires documented justification showing current (not potential future) necessity.

### ps-topic-researcher Task Analysis

| Requirement | Tool Needed | Tier |
|---|---|---|
| Search the web for current information | WebSearch | T3 |
| Read relevant documentation pages | WebFetch, Context7 (for library docs) | T3 |
| Produce structured research report | Text output only (no file write) | T1 |
| Does not spawn sub-agents | Does NOT need Task tool | -- |
| Does not persist state | Does NOT need Memory-Keeper | -- |
| Does not write files | Does NOT need Write/Edit tools | -- |

**Task requirements map to T3** (Research/External), not T5.

### Why T5 is Inappropriate Here

1. **No delegation requirement** — The agent does not spawn sub-agents or delegate work. Task tool is not used.

2. **No stated justification for current needs** — The senior developer's argument is "we might need it later," which violates H-34's explicit requirement: "T5 requires explicit justification." Hypothetical future needs do not justify present-day excess access.

3. **Security tier constraint violation** — Per `agent-development-standards.md` [Tier Constraints]:
   > **Worker agents MUST NOT be T5 (no Task tool).** Enforces H-01 single-level nesting.

   While ps-topic-researcher is not explicitly a "worker," assigning T5 when not needed creates a precedent that undermines the constraint's intent: preventing uncontrolled delegation hierarchies.

4. **Context budget efficiency** — T5 agents have access to all tools, which increases the context footprint of the agent definition and may degrade tool selection accuracy (RT-M-007: "Tool overload creep"). Unnecessary tool declarations consume agent definition context.

5. **Governance violation** — `quality-enforcement.md` H-22/H-36 standards emphasize deterministic, auditable access control. Granting excess permissions reduces auditability and shifts the cost of tool selection from the framework to the individual agent's decision-making.

---

## Recommendation: T3 (External)

### Tool Tier: T3 (External Access)

**Rationale:**

ps-topic-researcher is a research agent that requires external information access. T3 provides exactly what the agent needs: read-only access to external sources (WebSearch, WebFetch) plus library documentation lookup (Context7). It excludes unnecessary write, persistent state, and delegation capabilities.

### Tools List (T3 Tier)

```yaml
tools:
  - "WebSearch"           # Required: search the web for current information
  - "WebFetch"            # Required: read relevant documentation pages
  - "Read"                # Required: read cached/local reference files if provided
  - "Glob"                # Optional: find relevant files in project structure
  - "Grep"                # Optional: search file contents for patterns
  - "mcp__context7__resolve-library-id"  # Required: resolve library names to documentation
  - "mcp__context7__query-docs"          # Required: query library documentation
```

### Guardrails (T3-specific)

Per `agent-development-standards.md` [Guardrail Selection by Agent Type]:

Research agents (T3, divergent cognitive mode) SHOULD include:
- **Citation requirements** — All claims must have citations or source attribution
- **Source authority tiering** — Distinguish between high-authority, medium-authority, and untrusted sources
- **Stale data warnings** — Flag information older than 6 months with age indicator

```yaml
guardrails:
  input_validation:
    - field: "research_topic"
      format: "non-empty string, max 500 chars"
    - field: "focus_areas"
      format: "non-empty array of 1-5 strings"

  output_filtering:
    - "all_claims_must_have_citations"
    - "source_authority_tiers_required"
    - "stale_data_warnings_for_content_older_than_6_months"

  fallback_behavior: "warn_and_retry"
```

---

## Why Not T4 or T5?

| Tier | Why Not |
|---|---|
| **T4 (Persistent)** | Agent does not persist state across sessions. Memory-Keeper is unnecessary. |
| **T5 (Full)** | Agent does not delegate. Task tool is inappropriate. No documented justification for excess access. Violates least-privilege principle. |

---

## Framework Alignment

This recommendation aligns with:

- **H-34** (agent definition standards): Tool tier selection justified by actual task requirements
- **H-36** (agent routing standards): Deterministic tool access, no excess permissions
- **Tool Security Tiers principle**: "Always select the lowest tier that satisfies requirements"
- **RT-M-007** (anti-pattern prevention): Avoids AP-07 (Tool Overload Creep)
- **P-020** (user authority): Does not allow "flexibility reasoning" to override principle-driven constraints

---

## Handling the Senior Developer's Concern

The senior developer's instinct is understandable but reflects a common tension in framework design: balancing flexibility with governance.

**Response:**

> "I understand the flexibility concern. However, assigning T5 now for hypothetical future needs creates two problems: (1) it sets a precedent that 'might need later' justifies excess access, which erodes the principle-of-least-privilege foundation for all security tiers, and (2) T5 agents must not spawn sub-agents per H-01, so delegation capability wouldn't actually help.
>
> **Better path:** If ps-topic-researcher genuinely needs delegation or persistence in the future, we can upgrade it to T4 or T5 at that point with documented justification. The cost of an agent definition change is lower than the cost of a security tier precedent that undermines governance.
>
> **For now:** T3 (External) provides exactly what the agent needs: web search, documentation access, and library lookup. No more, no less."

This preserves both framework rigor and flexibility — we upgrade when the actual requirement emerges, not when hypothetical flexibility is suggested.

---

## Summary

| Aspect | Decision |
|---|---|
| **Tier** | T3 (External) |
| **Cognitive Mode** | Divergent (exploration, broad research) |
| **Model Recommendation** | Opus (complex reasoning for synthesis) |
| **Required Tools** | WebSearch, WebFetch, Context7 (resolve + query), Read |
| **Optional Tools** | Glob, Grep (for project structure search) |
| **Key Guardrails** | Citation requirements, source authority tiering, stale data warnings |
| **Justification** | Task requirements demand external information access (T3). No delegation, no persistence, no file writes. Lowest tier satisfying actual needs per H-34 principle. |
