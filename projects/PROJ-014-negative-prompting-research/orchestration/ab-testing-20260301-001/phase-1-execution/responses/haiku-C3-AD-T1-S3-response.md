# Tool Tier Assignment: adv-scorer Agent

**Agent Name:** adv-scorer
**Task Criticality:** C3 (Significant)
**Assigned Tier:** **T1 (Read-Only)**
**Decision Date:** 2026-03-01

---

## Executive Summary

The adv-scorer agent requires **T1 (Read-Only)** tier access. The task involves reading a deliverable artifact and applying a predefined rubric to produce a scoring report. No file writing, no external research, no delegation — only artifact consumption and evaluation. T1 is the lowest tier satisfying the task requirements and therefore the correct assignment per principle of least privilege.

---

## Task Analysis

### What adv-scorer Must Do

1. **Receive** a file path to a deliverable artifact + a scoring rubric
2. **Read** the artifact from the filesystem
3. **Apply** the S-014 LLM-as-Judge rubric across 6 dimensions
4. **Evaluate** the artifact against the rubric criteria
5. **Output** a structured score report
6. **Return** the results to the calling orchestrator (orchestrator handles storage)

### What adv-scorer Does NOT Do

- Does not write files (orchestrator stores results)
- Does not edit or modify artifacts
- Does not search for external information
- Does not research or explore (evaluation only, not investigation)
- Does not delegate to sub-agents or use Task tool
- Does not persist state across sessions

---

## Tool Tier Selection

### T1 Sufficiency Analysis

**T1 (Read-Only) includes:** Read, Glob, Grep

**Required tools for this task:**

| Tool | Required? | Why |
|------|-----------|-----|
| **Read** | YES | Must read the deliverable artifact file to score it |
| **Glob** | NO | Task receives explicit file path; no need for pattern matching |
| **Grep** | NO | Evaluation is by applying a rubric, not searching code patterns |
| **Write** | NO | Orchestrator stores results, not the agent |
| **Edit** | NO | Agent does not modify artifacts |
| **Bash** | NO | No system operations needed |
| **WebSearch** | NO | Scoring is deterministic against a rubric; no external research |
| **WebFetch** | NO | All information comes from the artifact and rubric |
| **Context7** | NO | No external library/framework documentation needed |
| **Memory-Keeper** | NO | Results are single-session, returned to orchestrator |
| **Task** | NO | No sub-agent delegation required |

**Conclusion:** Only Read is required. T1 includes Read (plus Glob and Grep which are harmless additions per principle of least privilege). Therefore **T1 is sufficient and correct**.

### Why Not Higher Tiers?

- **T2 (Read-Write):** Would add Write, Edit, Bash. Not needed — orchestrator handles file storage. Adds unnecessary attack surface for a read-only evaluation task.
- **T3 (External):** Would add WebSearch, WebFetch, Context7. Not needed — scoring is deterministic against provided rubric, requires no external research.
- **T4 (Persistent):** Would add Memory-Keeper. Not needed — orchestrator manages result storage and cross-session state.
- **T5 (Full):** Would add Task. Explicitly prohibited for worker agents per H-35. Also not needed for this task.

---

## Principle of Least Privilege Verification

Per `agent-development-standards.md` Section "Tool Security Tiers":

> **Always select the lowest tier that satisfies the agent's requirements.**

**Verification checklist:**

- [ ] Every tool in T1 is needed for the described task?
  ✓ **YES** — Read is essential; Glob and Grep do not harm a scoring agent that receives explicit input.

- [ ] Is there a tool required that T1 does not provide?
  ✓ **NO** — All required functionality is covered by Read.

- [ ] Is there a higher tier required for any aspect of the task?
  ✓ **NO** — Writing, external research, delegation, and persistence are all handled by the orchestrator, not this agent.

**Conclusion:** T1 is the lowest tier satisfying requirements. Assigning T1 is compliant with principle of least privilege and H-34/H-35 constraints.

---

## Security and Governance Alignment

### H-34/H-35 Compliance

- **H-34 (Agent Definition Schema):** Tool tier will be declared in `.governance.yaml` as `tool_tier: T1` ✓
- **H-35 (Constitutional Compliance):** Agent is a worker (invoked via Task by orchestrator), not an orchestrator. Will NOT include Task in allowed_tools. Will declare constitutional triplet (P-003, P-020, P-022) ✓

### Prohibition: Unnecessary Tool Access

The prohibition constraint states:
> NEVER assign a higher tool tier than the agent's task requires.

**Verification:** Does T1 exceed the task requirement?
- Task requires: artifact reading + evaluation
- T1 provides: Read (+ harmless Glob, Grep)
- Excess tools in T1? None that would violate principle of least privilege for this narrow task.

**Conclusion:** T1 assignment is justified and does not violate the prohibition.

---

## Design Pattern Alignment

The adv-scorer agent follows the **Specialist Agent** pattern (Pattern 1, `agent-development-standards.md`):

- Single, well-defined concern: score deliverables against a rubric
- Minimal tool requirements (only Read needed) → lower security tier ✓
- Clear cognitive mode: convergent (evaluation, ranking, conclusion)
- No research, no writing, no coordination — pure evaluation

This alignment confirms that T1 is the correct tier for a specialist evaluation agent.

---

## Output Tier Assignment Summary

| Dimension | Assignment | Rationale |
|-----------|-----------|-----------|
| **Tool Tier** | **T1 (Read-Only)** | Only Read required; lowest tier satisfying requirements |
| **Cognitive Mode** | Convergent | Evaluation, ranking, conclusion-drawing against fixed rubric |
| **Model Tier** | Haiku (provisional) | Fast deterministic scoring; limited reasoning vs. synthesis |
| **Persona** | Analytical, rigorous | Clinical scoring tone; evidence-based dimension breakdown |
| **Criticality Context** | C3 | Significant deliverables scored; quality gate decision-relevant |

---

## References

- **`agent-development-standards.md`** Section [Tool Security Tiers](#tool-security-tiers) — T1 definition, selection guidelines, least privilege principle
- **`agent-development-standards.md`** Section [Structural Patterns](#structural-patterns) Pattern 1 — Specialist agent design
- **`quality-enforcement.md`** — C3 criticality, quality gate context
- **Task Prohibition Constraint** — NEVER assign higher tier than task requires

---

**Decision:** Assign **T1 (Read-Only)** to adv-scorer. This is the lowest tier satisfying the task (artifact reading + evaluation), complies with principle of least privilege, aligns with specialist agent design patterns, and correctly enforces security boundaries per H-34/H-35.
