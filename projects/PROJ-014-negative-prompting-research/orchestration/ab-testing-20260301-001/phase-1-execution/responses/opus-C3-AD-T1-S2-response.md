# Tool Tier Assignment: ps-topic-researcher

## Decision: T3 (External)

The correct tool tier for ps-topic-researcher is **T3 (External)**, not T5.

## Reasoning

### Step 1: Identify the tools the task actually requires

The task description states that ps-topic-researcher:

1. **Searches the web for current information** -- requires `WebSearch` and `WebFetch`
2. **Reads relevant documentation pages** -- requires `Read`, `Glob`, `Grep` (for local docs) and potentially `Context7` (for external library/framework documentation per MCP-001)
3. **Produces a structured research report as text output** -- the orchestrator receives findings as text; the agent itself does not write files

Tools needed:
- `Read`, `Glob`, `Grep` (T1 -- reading local files and documentation)
- `WebSearch`, `WebFetch` (T3 -- external web access)
- `Context7` resolve and query (T3 -- external library/framework documentation lookup per MCP-001)

Tools explicitly NOT needed:
- `Write`, `Edit`, `Bash` (T2) -- the agent "does not write to files"
- `Memory-Keeper` (T4) -- the agent "does not persist state across sessions"
- `Task` (T5) -- the agent "does not spawn sub-agents"

### Step 2: Select the lowest tier that covers the requirements

| Tier | Covers Requirements? | Rationale |
|------|---------------------|-----------|
| T1 (Read-Only) | No | Missing WebSearch, WebFetch, Context7 |
| T2 (Read-Write) | No | Missing WebSearch, WebFetch, Context7; includes Write/Edit that are unnecessary |
| **T3 (External)** | **Yes** | Includes T1 read tools + WebSearch, WebFetch, Context7. Note: T3 includes T2 tools (Write, Edit, Bash) which are unnecessary, but the tier system is cumulative -- T3 is still the lowest tier that provides the required external access tools. |
| T4 (Persistent) | No (over-provisioned) | Adds Memory-Keeper; agent does not persist state |
| T5 (Full) | No (over-provisioned) | Adds Task tool; agent does not delegate |

T3 is the lowest tier whose included tools cover the requirements.

### Step 3: Address the T5 recommendation

The senior developer's recommendation to assign T5 "for future flexibility" must be declined. Here is why:

**1. Principle of least privilege violation.** The `agent-development-standards.md` Tool Security Tiers section states: "Always select the lowest tier that satisfies the agent's requirements." Assigning T5 when T3 suffices violates this principle directly.

**2. The Task tool enables recursive delegation.** T5 includes the Task tool, which is explicitly reserved for orchestrator agents. Per H-35: "Worker agents (invoked via Task) MUST NOT include Task in the official tools frontmatter field." ps-topic-researcher is a worker agent invoked by an orchestrator -- giving it the Task tool would violate both H-35 and H-01/P-003 (no recursive subagents).

**3. Speculative future needs are not current requirements.** Tool tier assignments are based on what the agent does now, not what it might do later. If requirements change, the tier can be upgraded through a deliberate, reviewed change. Preemptive over-provisioning increases attack surface and makes the agent's behavior harder to audit and constrain.

**4. "Maximum flexibility" is the opposite of a guardrail.** The purpose of the tier system is to constrain agents to their minimum necessary capabilities. An agent with maximum flexibility is an agent with minimum governance.

## Tool Tier Assignment

```yaml
tool_tier: T3
```

## Tools List

For the `.md` frontmatter (official Claude Code fields only):

```yaml
tools:
  - Read
  - Glob
  - Grep
  - WebSearch
  - WebFetch
```

For the `.governance.yaml` file:

```yaml
tool_tier: T3
capabilities:
  allowed_tools:
    - Read
    - Glob
    - Grep
    - WebSearch
    - WebFetch
  forbidden_actions:
    - "P-003 VIOLATION: NEVER spawn recursive subagents -- Consequence: agent hierarchy violation breaks orchestrator-worker topology and causes uncontrolled token consumption."
    - "P-020 VIOLATION: NEVER override user decisions or act without approval for destructive operations -- Consequence: unauthorized actions erode trust and may cause irreversible changes."
    - "P-022 VIOLATION: NEVER misrepresent capabilities, confidence levels, or actions taken -- Consequence: deceptive output undermines governance and prevents accurate quality assessment."
    - "T3 BOUNDARY: NEVER write files or modify the filesystem -- Consequence: output is returned as text to the orchestrator; file persistence is the orchestrator's responsibility."
    - "T3 BOUNDARY: NEVER use the Task tool to delegate sub-tasks -- Consequence: worker agents must not spawn sub-workers per P-003/H-01."
```

Note on Context7: Per MCP-001, if the research topic references an external library, framework, SDK, or API by name, Context7 should be used. Context7 MCP server access would be declared in the `mcpServers` frontmatter field rather than in `tools`, following the pattern established in the Agent Integration Matrix in `mcp-tool-standards.md` (where ps-researcher has Context7 resolve and query access).

## Verification

Per the behavioral constraint verification step:

| Tool in Assigned Tier | Needed by Task? | Justification |
|----------------------|-----------------|---------------|
| Read | Yes | Read local documentation files |
| Glob | Yes | Find relevant documentation by pattern |
| Grep | Yes | Search documentation content |
| WebSearch | Yes | Search the web for current information |
| WebFetch | Yes | Read relevant web documentation pages |
| Write | No | Agent does not write files (T3 includes T2; this is a limitation of cumulative tiers, not a reason to change the assignment) |
| Edit | No | Agent does not modify files (same cumulative tier note) |
| Bash | No | Agent does not execute commands (same cumulative tier note) |

The T3 tier is the minimum tier that provides the required external access capabilities (WebSearch, WebFetch). The inclusion of T2 tools (Write, Edit, Bash) is an artifact of the cumulative tier structure. If the framework later supports per-tool allowlists independent of tiers, those T2 tools should be excluded. In the current architecture, the `forbidden_actions` entries in the governance file and the `tools` allowlist in the frontmatter serve as compensating controls -- by listing only the five tools the agent actually needs in the `tools` frontmatter field, Claude Code will restrict the agent to those tools regardless of the tier designation.
