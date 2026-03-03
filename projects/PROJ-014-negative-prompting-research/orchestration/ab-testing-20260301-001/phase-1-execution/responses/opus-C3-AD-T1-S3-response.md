# Tool Tier Assignment: adv-scorer

## Assignment: T1 (Read-Only)

**Tools included:** Read, Glob, Grep

## Justification

### Task Analysis

The task description states that adv-scorer:

1. **Receives** a deliverable artifact as a file path and a scoring rubric.
2. **Reads** the artifact.
3. **Applies** the S-014 LLM-as-Judge rubric across 6 dimensions (this is LLM reasoning, not tool use).
4. **Outputs** a structured score report.
5. The **calling orchestrator** handles storing the results.

Point 5 is the decisive constraint. The task explicitly delegates persistence responsibility to the calling orchestrator. This means adv-scorer does not need Write, Edit, or Bash -- all of which are T2 tools.

### Tool-by-Tool Verification

| Tool | Needed? | Rationale |
|------|---------|-----------|
| **Read** | Yes | Must read the deliverable artifact from the file path provided. Must also read any strategy execution findings if available. |
| **Glob** | Yes | May need to locate related files (e.g., strategy reports, prior score reports) when the exact path is not provided in the handoff context. |
| **Grep** | Yes | May need to search for specific content patterns within the deliverable (e.g., verifying traceability references, checking for required sections) to inform dimension scoring. |
| **Write** | No | The task description explicitly states "the calling orchestrator will handle storing the results." adv-scorer returns the score report; it does not persist it. |
| **Edit** | No | No file modification is required. adv-scorer is an evaluator, not a producer. |
| **Bash** | No | No shell commands are required for scoring. The AST-based structural pre-check described in the current agent definition (using `uv run jerry ast ...` commands) is a convenience optimization, not a scoring necessity -- the same structural assessment can be performed by reading the file and reasoning about its structure. |
| **WebSearch/WebFetch** | No | Scoring uses the rubric already loaded in the agent definition. No external research required. |
| **Memory-Keeper** | No | No cross-session state needed. Persistence is orchestrator's responsibility. |
| **Task** | No | Worker agent. Must not spawn subagents per P-003/H-01. |

### Tier Selection Reasoning

Per the behavioral constraint: "Identify the specific tools the task requires, then assign the lowest tier whose included tools cover exactly those requirements -- defaulting to T1 unless a specific higher-tier tool is genuinely needed."

The task requires exactly three tools: Read, Glob, and Grep. These are precisely the T1 (Read-Only) tool set. No T2 or higher tools are needed because:

- **Write is unnecessary.** The task description explicitly states the orchestrator handles storage. adv-scorer's output is returned to the caller as structured data (the `verdict`, `composite_score`, and other fields in the session context protocol). The orchestrator that invoked adv-scorer via the Task tool receives this output and decides where and how to persist it.
- **Bash is unnecessary.** The AST pre-check commands are an optimization that could inform scoring, but the agent can assess structural completeness by reading the file content directly. The scoring rubric dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability) are all evaluable through reading and reasoning, not through shell execution.

### Alignment with Framework Standards

The `agent-development-standards.md` Tool Security Tiers table already lists `adv-scorer` as a T1 example agent:

> | **T1** | Read-Only | Read, Glob, Grep | Evaluation, auditing, scoring, validation | adv-executor, **adv-scorer**, wt-auditor |

The T1 use case description -- "Evaluation, auditing, scoring, validation" -- is an exact match for adv-scorer's function.

### Verification Against Behavioral Constraint

> "Every tool in the assigned tier is needed for the described task; no tool appears in the assignment that the task does not require."

- Read: needed (reads deliverable). Pass.
- Glob: needed (locates related files). Pass.
- Grep: needed (searches for content patterns within files). Pass.
- No tool in T1 is unused. No tool outside T1 is needed.

### Note on Current Implementation Discrepancy

The existing `adv-scorer.governance.yaml` declares `tool_tier: T2`, and the `.md` frontmatter declares `tools: Read, Write, Edit, Glob, Grep`. This is because the current implementation has adv-scorer persisting its own score report via Write (Step 7 in `<scoring_process>`). However, the task description as stated -- where the orchestrator handles storage -- makes T2 unnecessary. If the agent definition were updated to match this task description, the Write and Edit tools should be removed from the frontmatter, and the governance file should be changed to `tool_tier: T1`.

## Summary

| Parameter | Value |
|-----------|-------|
| **Agent** | adv-scorer |
| **Assigned Tier** | T1 (Read-Only) |
| **Tools** | Read, Glob, Grep |
| **Principle Applied** | Least privilege -- lowest tier covering all required tools |
| **Key Factor** | Orchestrator handles persistence; no write tools needed |
