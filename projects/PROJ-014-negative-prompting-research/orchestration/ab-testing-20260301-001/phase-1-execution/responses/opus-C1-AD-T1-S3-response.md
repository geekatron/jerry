# Tool Tier Assignment: adv-scorer

## Assignment: T1 (Read-Only)

## Tier Evaluation (Starting from T1, Escalating Only When Required)

### T1 (Read-Only): Read, Glob, Grep

The task description states that adv-scorer:

1. **Receives a deliverable artifact as a file path** -- requires `Read` to load the artifact content.
2. **Receives a scoring rubric** -- the S-014 rubric is embedded in the agent definition itself (the `<scoring_dimensions>` section); the SSOT reference in `.context/rules/quality-enforcement.md` can be accessed via `Read`.
3. **Reads the artifact** -- `Read` tool.
4. **Applies the S-014 LLM-as-Judge rubric across 6 dimensions** -- this is pure LLM reasoning over the content already loaded via `Read`. No additional tools required.
5. **Outputs a structured score report** -- the task description explicitly states: "The calling orchestrator will handle storing the results."

Since the orchestrator handles result storage, adv-scorer does not need to write files. Its workflow is: read input, reason over it, return structured output to the caller. All three T1 tools (Read, Glob, Grep) support the read-and-evaluate workflow:

- **Read**: Load the deliverable artifact and any referenced strategy execution reports.
- **Glob**: Locate files if the deliverable path uses a pattern or if strategy reports need discovery.
- **Grep**: Search within the deliverable for specific patterns relevant to scoring (e.g., checking for presence of navigation tables, citations, traceability chains).

T1 is sufficient. The agent only reads and evaluates.

### T2 (Read-Write): Would Add Write, Edit, Bash

**Not required.** The task description explicitly delegates result storage to the calling orchestrator. adv-scorer does not need to write files, edit files, or execute shell commands. Assigning T2 would grant unnecessary write access, violating the principle of least privilege (AR-006).

**Note on the existing agent definition:** The current `adv-scorer.md` frontmatter declares `tools: Read, Write, Edit, Glob, Grep` (T2) and the governance file declares `tool_tier: T2`. This reflects an older design where adv-scorer persisted its own score reports (Step 7 in its `<scoring_process>` uses `Write`). However, the task description for this assignment explicitly states that the orchestrator handles storage, which removes the justification for T2. Under the behavioral constraint to start at T1 and escalate only when the task specifically requires a higher tier, the correct assignment based on the given task description is T1.

### T3-T5: Not Evaluated

No aspect of the task description requires external data access (T3), persistent cross-session state (T4), or agent delegation (T5). These tiers are not considered further.

## Justification Summary

| Criterion | Assessment |
|-----------|------------|
| **Reads files?** | Yes -- deliverable artifact, rubric reference, strategy reports |
| **Writes files?** | No -- orchestrator handles result persistence |
| **Needs external data?** | No -- scores against internal rubric only |
| **Needs cross-session state?** | No -- stateless evaluation per invocation |
| **Needs to delegate to other agents?** | No -- P-003 prohibits this; single-level worker |

**Conclusion:** T1 (Read-Only) is the lowest tier that satisfies adv-scorer's requirements as described in this task. The agent reads a deliverable, applies a rubric through LLM reasoning, and returns structured output. It does not write, search externally, persist state, or delegate.

## References

- Agent Development Standards, Tool Security Tiers: `.context/rules/agent-development-standards.md`
- Selection Guideline 1: "Default to T1. If an agent only reads and evaluates, T1 is sufficient."
- Tool Security Tiers table: adv-scorer is listed as a T1 example agent alongside adv-executor and wt-auditor.
- Existing agent definition: `skills/adversary/agents/adv-scorer.md` (currently T2, contains Write in tools)
- Existing governance file: `skills/adversary/agents/adv-scorer.governance.yaml` (currently declares `tool_tier: T2`)
