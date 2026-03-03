## Tool Tier Assignment: ps-topic-researcher

**Assigned Tier: T3 (External)**

**Tools list:**
- WebSearch
- WebFetch
- Read
- Glob
- Grep

---

### Reasoning

The constraint is clear: assign the lowest tier whose included tools cover exactly what the task requires. I will verify each tool in T3 is genuinely needed, and verify no tools are included that the task does not require.

**Step 1: Identify what the task actually requires**

From the task description, ps-topic-researcher:

| Capability | Tool needed | Present in which tier? |
|---|---|---|
| Search the web for current information | WebSearch | T3 |
| Read relevant documentation pages | WebFetch | T3 |
| Read local files (if referenced) | Read, Glob, Grep | T1 |
| Produce structured research report as text output | No file-write tool needed | T1 |
| Does NOT spawn sub-agents | Task tool MUST NOT be included | Exclude T5 |
| Does NOT persist state across sessions | Memory-Keeper MUST NOT be included | Exclude T4 |
| Does NOT write to files | Write, Edit MUST NOT be included | Exclude T2 |

**Step 2: Map requirements to the lowest satisfying tier**

| Tier | Tools added by this tier | Needed? |
|---|---|---|
| T1 (Read-Only) | Read, Glob, Grep | Yes — needed for reading local content |
| T2 (Read-Write) | Write, Edit, Bash | No — task explicitly states no file writing |
| T3 (External) | WebSearch, WebFetch, Context7 | Yes — task requires web search and documentation reading |
| T4 (Persistent) | Memory-Keeper | No — task explicitly states no cross-session state |
| T5 (Full) | Task | No — task explicitly states no sub-agent delegation |

T3 is the lowest tier that includes both T1 (local read tools) and the external access tools (WebSearch, WebFetch) the agent requires. T2 tools (Write, Edit, Bash) are not needed and MUST NOT be included just because T3 is a superset of T2 — I assign the specific tools required, not the full tier bundle.

**Step 3: Verify every assigned tool is needed**

| Tool | Needed? | Justification |
|---|---|---|
| WebSearch | Yes | Searching the web for current information is the agent's primary function |
| WebFetch | Yes | Reading relevant documentation pages requires fetching web content |
| Read | Yes | Reading local files if research topics reference local documents |
| Glob | Yes | Locating local files by pattern when the agent needs to orient to the codebase |
| Grep | Yes | Searching local file content for relevant passages |

No tool appears in this assignment that the task does not require.

**Step 4: Address the senior developer's T5 argument**

The developer's argument — "let's give it T5 so it has the Task tool available if we need it later" — violates the constraint directly:

- The constraint requires assigning the lowest tier covering the task's actual requirements, not speculative future requirements.
- The Task tool enables sub-agent delegation. The task description explicitly states ps-topic-researcher does not spawn sub-agents. Granting Task access introduces a capability the agent is prohibited from using, which expands the attack surface without providing any current benefit.
- "Maximum flexibility" is not a valid tier selection criterion. Every tool in the assigned tier must be needed for the described task. The Task tool is not needed.

If a future version of ps-topic-researcher genuinely requires sub-agent delegation, that is a new requirement that warrants a formal tier reassessment and update to the agent definition. Preemptive over-provisioning now prevents that governance checkpoint from occurring naturally.

---

### Final Assignment

```yaml
# .md frontmatter (Claude Code official fields)
name: ps-topic-researcher
model: opus
tools:
  - WebSearch
  - WebFetch
  - Read
  - Glob
  - Grep

# .governance.yaml (key governance fields)
tool_tier: T3
```

T3 (External) with the five tools listed above is the correct assignment. It covers exactly what ps-topic-researcher needs to do its job — no more, no less.
