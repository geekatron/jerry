# Tool Tier Assignment: adv-scorer

## Assigned Tier: T1 (Read-Only)

**Tools:** Read, Glob, Grep

## Justification

### Task Analysis

The adv-scorer agent has a narrowly scoped responsibility: it receives a deliverable artifact file path and a scoring rubric, reads the artifact, applies the S-014 LLM-as-Judge rubric across 6 quality dimensions (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability), and produces a structured score report. The task description explicitly states that "the calling orchestrator will handle storing the results."

### Tier Selection Reasoning

The agent-development-standards.md Tool Security Tiers section establishes a clear principle: "Always select the lowest tier that satisfies the agent's requirements." The selection guidelines state: "Default to T1. If an agent only reads and evaluates, T1 is sufficient."

adv-scorer's operations are purely evaluative:

1. **Read** the deliverable artifact at the provided file path.
2. **Read** the scoring rubric (either the SSOT dimensions from quality-enforcement.md or a custom rubric passed by the orchestrator).
3. **Evaluate** the artifact against the rubric using LLM reasoning (no tool required -- this is the agent's core cognitive work).
4. **Return** the structured score report to the calling orchestrator.

None of these operations require writing files, accessing external resources, persisting cross-session state, or delegating to sub-agents. The orchestrator is responsible for persisting the score report, not the scorer itself.

### Why Not T2 or Higher

- **T2 (Read-Write):** Would grant Write, Edit, and Bash tools. adv-scorer does not need to create or modify files. The task description explicitly delegates storage responsibility to the calling orchestrator. Granting write access would violate the principle of least privilege (AR-006) and create an unnecessary attack surface where the scoring agent could inadvertently modify the deliverable it is evaluating.
- **T3 (External):** Would add WebSearch, WebFetch, and Context7. adv-scorer evaluates artifacts against an internal rubric. It does not need external documentation or web resources. Its scoring methodology is self-contained within the S-014 strategy definition and the SSOT quality dimensions.
- **T4 (Persistent):** Would add Memory-Keeper. adv-scorer operates statelessly within a single invocation. Cross-session persistence is not required.
- **T5 (Full):** Would add the Task tool, enabling delegation. adv-scorer is a worker agent invoked by an orchestrator. Per H-01/P-003 (no recursive subagents) and H-35 (worker agents MUST NOT include Task), T5 is prohibited for this agent.

### Standards Alignment

The Tool Security Tiers table in agent-development-standards.md explicitly lists `adv-scorer` as an example T1 agent alongside `adv-executor` and `wt-auditor`, confirming that the framework's own reference architecture classifies this agent at the Read-Only tier. The Guardrail Selection by Agent Type table further reinforces this: scoring agents (convergent, T1) require rubric schema validation for input and anti-leniency statements plus dimension-level breakdowns for output -- none of which require file-writing capabilities.

### Tool Mapping

| Tool | Purpose | Tier |
|------|---------|------|
| Read | Load the deliverable artifact and scoring rubric from file paths | T1 |
| Glob | Locate related artifacts if the deliverable references companion files | T1 |
| Grep | Search for specific patterns within the deliverable (e.g., verifying claims, checking structural elements) | T1 |

### Conclusion

T1 (Read-Only) is the correct and sufficient tier for adv-scorer. The agent's task is entirely evaluative: read an artifact, apply a rubric, return a score. Assigning any higher tier would grant unnecessary capabilities that the agent's task does not require, violating the principle of least privilege.
