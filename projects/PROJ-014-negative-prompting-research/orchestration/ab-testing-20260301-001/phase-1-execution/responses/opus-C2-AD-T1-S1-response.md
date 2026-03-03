# wt-auditor Tool Tier Definition

## Decision: T1 (Read-Only)

The developer's suggestion to assign T3 is rejected. The correct tool tier for `wt-auditor` is **T1 (Read-Only)**.

### Tools List

```yaml
tools:
  - Read
  - Glob
  - Grep
```

### Governance YAML

```yaml
tool_tier: T1
```

## Rationale

The agent development standards in `agent-development-standards.md` establish a principle of least privilege for tool tier selection (AR-006): **"Always select the lowest tier that satisfies the agent's requirements."** The selection guidelines are explicit:

> "1. **Default to T1.** If an agent only reads and evaluates, T1 is sufficient."

The task description for `wt-auditor` states the following requirements:

1. **Reads** WORKTRACKER.md files -- satisfied by `Read`.
2. **Validates** that entries follow required format -- satisfied by `Read`, `Glob`, and `Grep` (pattern matching and file discovery).
3. **Produces a pass/fail report** -- this is output to the caller (the orchestrator or main context), not a written file artifact. The agent reports results; it does not persist them to disk.
4. **Does not modify any files** -- explicitly rules out `Write`, `Edit`, and `Bash`.
5. **Does not need external data sources** -- explicitly rules out `WebSearch`, `WebFetch`, and Context7.
6. **Runs at the end of each session** -- no cross-session state requirement, ruling out Memory-Keeper (T4).

The `wt-auditor` agent is listed by name as a T1 example agent in the Tool Security Tiers table alongside `adv-executor` and `adv-scorer` -- other evaluation and validation agents with the same read-only profile.

## Why the Developer's T3 Suggestion Violates Standards

The developer's reasoning -- "it's easier to have more tools than fewer" and "future-proofing" -- conflicts with three specific framework standards:

1. **Principle of least privilege (AR-006).** The selection guidelines mandate defaulting to T1 and escalating only when task requirements demand it. Convenience is not a valid justification for tier escalation.

2. **AP-07: Tool Overload Creep.** The anti-pattern catalog in `agent-routing-standards.md` documents this exact failure mode: agents accumulate tool access beyond what their task requires, causing tool selection accuracy to degrade. T3 would grant `wt-auditor` eight tools (Read, Glob, Grep, Write, Edit, Bash, WebSearch, WebFetch) when it needs three. Five of those tools would be unused and actively harmful to routing quality.

3. **H-35 worker agent constraints.** The `wt-auditor` is a worker agent invoked via Task. Granting Write, Edit, and Bash capabilities to an agent whose task description explicitly says "does not modify any files" creates a contradiction between the agent's declared purpose and its available toolset. If a future version of the agent needs to write fixes, that is a capability change that warrants a deliberate tier reassessment with its own review -- not preemptive access granted today.

T3 specifically requires citation guardrails in `output_filtering` (since T3 includes external data tools), which would be meaningless overhead for an agent that never fetches external data.

## If Requirements Change Later

If `wt-auditor` later needs to write fix suggestions to a file, the correct action is to reassess the tool tier at that time and promote to T2 with documented justification. If it needs to look up external documentation, promote to T3 with citation guardrails added. Each tier change should be a deliberate decision, not a preemptive one. This is not a burden -- it is the governance model working as designed.
