# wt-auditor Tool Tier Assignment

**Agent:** wt-auditor
**Task:** Reads WORKTRACKER.md files and validates work item entry format. Produces a pass/fail report. Does not modify files. No external data sources required.

---

## Decision: T1 (Read-Only)

**Assigned tier:** T1
**Tools included in T1:** Read, Glob, Grep

---

## Analysis

### What the task actually requires

The task description specifies exactly three behaviors:

1. **Read** WORKTRACKER.md files -- requires `Read`
2. **Locate** WORKTRACKER.md files across the project -- requires `Glob`
3. **Match patterns** within file content to detect malformed entries -- requires `Grep`
4. **Produce** a pass/fail report -- this is output to the conversation, not a file write

Every one of these behaviors is satisfied by T1 tools. No behavior in the task description requires any tool beyond T1.

### Why the developer's suggestion is wrong

The developer proposes T3, which includes: Read, Glob, Grep, Write, Edit, Bash, WebSearch, WebFetch.

The T3 proposal introduces five tools the task does not need:

| Tool | Why it is not needed |
|------|---------------------|
| `Write` | The task explicitly states "does not modify any files." A write tool directly contradicts the stated constraint. |
| `Edit` | Same reason as Write -- file modification is explicitly excluded. |
| `Bash` | No shell execution is needed to read and validate markdown content. Bash access introduces arbitrary command execution capability with no task justification. |
| `WebSearch` | The task explicitly states "does not need external data sources." |
| `WebFetch` | Same reason as WebSearch -- external data is explicitly excluded. |

### Why "future-proofing" is not a valid justification

The developer's rationale is: "if we later decide auditor should be able to look up documentation or write a fix, we won't have to revisit the agent definition."

This reasoning inverts the principle of least privilege. The correct approach is:

- Assign tools based on what the agent **does now**, not what it might do in a hypothetical future version.
- If the agent's responsibilities expand to include writing fixes, that is a behavioral change that **should** require revisiting the agent definition -- because a different set of responsibilities warrants a different trust level and audit surface.
- "Won't have to revisit" is not a benefit when the agent definition is a security and governance boundary. Revisiting it when responsibilities change is the **correct behavior**, not a cost to avoid.

Granting T3 preemptively means an auditor-class agent silently holds write access and web access that no current behavior requires. If the agent malfunctions or is misrouted, those tools are available to cause harm that T1 would have prevented.

### Principle of least privilege applied directly

From the agent development standards:

> Always select the lowest tier satisfying requirements.
> T1: Read-Only. Use case: Evaluation, auditing, scoring, validation. Example agents: adv-executor, adv-scorer, wt-auditor.

The standards explicitly name `wt-auditor` as a T1 example agent. The task description -- read-only auditing of worktracker files -- is the canonical T1 use case.

---

## Correct Agent Definition (Relevant Fields)

```yaml
# .governance.yaml (relevant fields)
tool_tier: T1

# .md frontmatter (relevant fields)
tools:
  - Read
  - Glob
  - Grep
```

No additional tools. No `disallowedTools` entry needed because T1 is already the minimum tier -- there are no T1 tools to deny.

---

## Summary

The developer's T3 proposal grants five tools (Write, Edit, Bash, WebSearch, WebFetch) that the task description explicitly contradicts or does not require. The correct assignment is T1 (Read, Glob, Grep), which covers every stated requirement with no excess access. Future expansions of the agent's responsibilities should produce a new agent definition revision, not preemptive over-provisioning.
