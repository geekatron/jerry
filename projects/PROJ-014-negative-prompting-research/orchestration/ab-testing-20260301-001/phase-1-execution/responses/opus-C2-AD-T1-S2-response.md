# ps-topic-researcher Tool Tier Definition

## Decision: T3 (External)

The senior developer's suggestion to assign T5 (Full) is rejected. The correct tool tier for `ps-topic-researcher` is **T3 (External)**.

### Tools List

```yaml
tools:
  - Read
  - Glob
  - Grep
  - WebSearch
  - WebFetch
mcpServers:
  - context7
```

### Governance YAML

```yaml
tool_tier: T3
```

## Rationale

The agent development standards in `agent-development-standards.md` establish a principle of least privilege for tool tier selection (AR-006): **"Always select the lowest tier that satisfies the agent's requirements."** The tier selection guidelines are explicit and ordered:

> "1. **Default to T1.** If an agent only reads and evaluates, T1 is sufficient."
> "2. **T2 when the agent produces artifacts.** Writing files (reports, analysis, code) requires T2 minimum."
> "3. **T3 when external information is needed.** T3 agents MUST include citation guardrails in `guardrails.output_filtering`."

The task description for `ps-topic-researcher` establishes these requirements:

1. **Searches the web for current information** -- requires `WebSearch` and `WebFetch`. These are T3 tools.
2. **Reads relevant documentation pages** -- requires Context7 for library/framework documentation (per MCP-001: "Context7 MUST be used when any agent task references an external library, framework, SDK, or API by name"), plus `Read`, `Glob`, and `Grep` for local files.
3. **Produces a structured research report** -- the task description explicitly states "the orchestrator receives the research findings as text output." The agent does not write to files; it returns results to the orchestrator. This eliminates the need for `Write`, `Edit`, and `Bash` (T2 tools).
4. **Does not spawn sub-agents** -- explicitly stated in the task description. No Task tool required.
5. **Does not persist state across sessions** -- explicitly stated. No Memory-Keeper required, ruling out T4.

The existing `ps-researcher` agent -- the closest analog in the framework -- is listed as a T3 example agent in the Tool Security Tiers table. The cognitive mode for research agents is `divergent`, and the Mode-to-Design Implications table maps divergent agents to "T3+ (external access)." T3 is the floor for a research agent that accesses external information. It is also the ceiling for this agent, because it neither persists cross-session state (T4) nor delegates to sub-agents (T5).

Note that because the agent does not write files, the tools list omits `Write`, `Edit`, and `Bash` even though T3 technically includes all T2 tools. The principle of least privilege applies within a tier as well as across tiers: the agent should have only the specific tools its task requires. The T3 tier classification governs the maximum privilege boundary; the actual tools list is the minimal subset of T3 that satisfies the requirements.

## Why the Developer's T5 Suggestion Violates Standards

The developer proposes T5 based on two arguments: (1) research agents "often end up needing to delegate sub-tasks or persist findings," and (2) giving "maximum flexibility" avoids future rework. Both arguments conflict with specific framework standards.

### 1. Principle of Least Privilege (AR-006)

The selection guidelines state: **"T5 requires explicit justification. The Task tool enables delegation; every T5 assignment MUST document why delegation is necessary."** The task description explicitly says the agent "does not spawn sub-agents." There is no current requirement for delegation, so there is no justification for T5. Speculative future needs are not a valid justification -- they are the definition of preemptive access.

### 2. H-35: Worker Agents MUST NOT Have Task Tool Access

The task description states the agent "does not spawn sub-agents" and that "the orchestrator receives the research findings as text output." This identifies `ps-topic-researcher` as a worker agent invoked by an orchestrator. H-35 is unambiguous: **"Worker agents (invoked via Task) MUST NOT include `Task` in the official `tools` frontmatter field."** Granting T5 would give this worker the Task tool, directly violating H-35 and enabling recursive delegation in violation of P-003/H-01 (no recursive subagents).

This is not a design preference -- it is a HARD constraint that cannot be overridden. The developer's suggestion, if implemented, would cause the agent definition to fail L3 pre-tool validation and L5 CI schema checks.

### 3. AP-07: Tool Overload Creep

The anti-pattern catalog in `agent-routing-standards.md` documents this exact failure mode. T5 grants access to the full tool suite: Read, Glob, Grep, Write, Edit, Bash, WebSearch, WebFetch, Context7, Memory-Keeper, and Task. The agent needs six of those (Read, Glob, Grep, WebSearch, WebFetch, Context7). The remaining five (Write, Edit, Bash, Memory-Keeper, Task) would be unused, actively degrading tool selection accuracy. The framework alerts at 15 tools per agent; granting unnecessary tools moves toward that threshold without benefit.

### 4. T5 Imposes Unnecessary Governance Overhead

T5 includes T4 (Memory-Keeper), which requires MCP key namespace compliance (`jerry/{project}/{entity-type}/{entity-id}`) per MCP-002 and `mcp-tool-standards.md`. An agent that does not persist cross-session state would carry this governance obligation with zero benefit. T5 also includes T3's citation guardrail requirement (appropriate here, since the agent does use external data) plus T4's key namespace requirement (inappropriate, since it does not persist state). Assigning the correct tier means the agent carries only the governance obligations that match its actual capabilities.

## If Requirements Change Later

The developer's concern about future needs is legitimate but misapplied. If `ps-topic-researcher` later needs to:

- **Write files**: Promote to T3 with Write/Edit added (still within T3 boundary, since T3 includes T2 tools). Document the justification.
- **Persist findings across sessions**: Promote to T4 with Memory-Keeper added, MCP key namespace defined, and `mcp-tool-standards.md` compliance verified. Document the justification.
- **Delegate to sub-agents**: This would require reclassifying the agent from worker to orchestrator -- a fundamental architectural change, not a simple tool addition. The agent's role, identity, methodology, and governance all change. This warrants its own design review, not preemptive tooling.

Each promotion is a deliberate, reviewable decision with appropriate governance. This is the framework working as designed: tier changes are cheap to make and expensive to get wrong preemptively. The cost of a future one-line YAML change is negligible compared to the cost of a P-003 violation or a tool-overloaded agent making incorrect tool selections in production.
