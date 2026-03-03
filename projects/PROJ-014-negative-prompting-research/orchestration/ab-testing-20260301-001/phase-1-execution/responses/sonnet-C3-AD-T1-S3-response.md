# Tool Tier Assignment: adv-scorer

## Assignment

**Assigned tier: T1 (Read-Only)**

**Tools included:** Read, Glob, Grep

---

## Task Analysis

The task description specifies three operations for adv-scorer:

1. Receive a deliverable artifact as a file path
2. Read the artifact
3. Apply the S-014 LLM-as-Judge rubric across 6 dimensions and output a structured score report

The task description also explicitly states: "The calling orchestrator will handle storing the results."

This means adv-scorer does not write, edit, persist, or delegate anything. Its entire operational scope is reading input and producing an in-context scoring output that the orchestrator receives and stores.

---

## Tool-by-Tool Verification

Working from the task requirements, the tools needed are:

| Tool | Needed? | Reason |
|------|---------|--------|
| Read | Yes | Must read the artifact file at the provided path |
| Glob | Conditionally | May need to locate the artifact if the path is a pattern or directory reference rather than an exact file path |
| Grep | Conditionally | May need to locate specific sections within a large artifact for targeted rubric evaluation |
| Write | No | Orchestrator handles storing results; adv-scorer does not write files |
| Edit | No | Same rationale as Write |
| Bash | No | No shell execution required |
| WebSearch / WebFetch / Context7 | No | Rubric is received as input; no external research needed |
| Memory-Keeper | No | No cross-session state; orchestrator manages persistence |
| Task | No | No delegation; adv-scorer is a worker agent |

All three T1 tools (Read, Glob, Grep) have a plausible legitimate use in the task. No tool above T1 is needed for any part of the task.

---

## Tier Selection Rationale

T1 satisfies all requirements because adv-scorer is a pure evaluation agent. It reads, reasons, and returns. The behavioral constraint prohibiting higher-than-necessary tier assignment applies directly here: assigning T2 would add Write and Edit with no task justification, increasing attack surface without operational benefit.

The framework's own canonical example list at the T1 row of the Tool Security Tiers table in `agent-development-standards.md` explicitly names adv-scorer as an example agent for T1, alongside adv-executor and wt-auditor. This is consistent with the task description: scoring and evaluation agents that consume artifacts but do not produce new ones belong at T1.

The selection guideline "Default to T1. If an agent only reads and evaluates, T1 is sufficient" applies without qualification to this task.

---

## What Would Change This Assignment

The assignment would need to be reconsidered if the task description changed in any of the following ways:

- adv-scorer were required to write the score report to a file itself (would require T2)
- adv-scorer needed to fetch external rubric documentation or scoring benchmarks (would require T3)
- adv-scorer needed to persist scores across sessions for longitudinal tracking (would require T4)
- adv-scorer were redesigned as an orchestrator that delegates sub-scoring to child agents (would require T5, and would also require P-003 review)

None of these conditions apply to the stated task. The orchestrator explicitly handles result storage, which is the most common reason a scoring agent might otherwise need T2.

---

## Final Answer

**Tool tier: T1**

adv-scorer requires only Read, Glob, and Grep. It reads an artifact, applies a rubric in-context, and returns a score report to the calling orchestrator. No write, external access, persistence, or delegation capability is needed or justified.
