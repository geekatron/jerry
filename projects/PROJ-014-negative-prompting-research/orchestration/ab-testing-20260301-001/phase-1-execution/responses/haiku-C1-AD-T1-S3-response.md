# Tool Tier Selection Analysis: adv-scorer Agent

**Agent Name:** adv-scorer
**Task Context:** Receive deliverable artifact (file path) + scoring rubric → read artifact → apply S-014 LLM-as-Judge rubric (6 dimensions) → output structured score report
**Calling Pattern:** Orchestrator handles result storage; adv-scorer does not persist

---

## Tier Selection: T1 (Read-Only)

**Justification:** adv-scorer requires **T1 (Read-Only)** tier access.

---

## Analysis

### Task Requirements Decomposition

The agent's workflow involves exactly four operations:

1. **Receive input** (file path + rubric) — zero tool cost
2. **Read artifact file** — `Read` tool (T1)
3. **Analyze + score** — LLM reasoning (zero tool cost)
4. **Output structured report** — text generation (zero tool cost)

### Tier Escalation Evaluation

Applying the selection framework from `agent-development-standards.md` [Tool Security Tiers, Selection Guidelines]:

| Tier | Required For | Satisfies adv-scorer? | Evidence |
|------|---|---|---|
| **T1 (Read-Only)** | Evaluation, auditing, scoring, validation | **YES** | Agent reads artifact (Read tool) and produces evaluation output |
| T2 (Read-Write) | Producing artifacts (Write, Edit, Bash) | **NO** | Agent does NOT write files; orchestrator handles persistence |
| T3 (External) | External research (WebSearch, WebFetch, Context7) | **NO** | No external data access required; rubric is provided in-session |
| T4 (Persistent) | Cross-session state (Memory-Keeper) | **NO** | No cross-session state needed; results are scoped to current session |
| T5 (Full) | Delegation (Task tool) | **NO** | Agent must not delegate further; H-01/P-003 single-level nesting enforced |

### Constraint Verification

**Least Privilege Principle:** The agent is listed in the Tool Security Tiers table as an example T1 agent:

> | **T1** | Read-Only | Read, Glob, Grep | Evaluation, auditing, scoring, validation | **adv-executor, adv-scorer**, wt-auditor |

This confirms T1 is the intended tier for this scoring function.

**No T2 Requirements:** The agent produces a report as structured text output, not as a file artifact written to disk. The orchestrator receives the report (via agent response), manages persistence, and stores results. This delegation of write responsibility is a design pattern: agent outputs → orchestrator persists. T2 (Write access) is therefore **not required**.

**No External Tools Required:** The scoring rubric (S-014 dimensions) is provided by the caller. Scoring logic is deterministic against the artifact content and rubric schema. No WebSearch, WebFetch, Context7, or Memory-Keeper operations are needed.

**No Delegation:** As a worker agent invoked by an orchestrator (likely `/adversary` skill's orchestrator), adv-scorer must not include the Task tool (H-35 constraint). T1 is consistent with worker-agent constraints.

---

## Compliance Map

| Standard | Requirement | adv-scorer Compliance |
|----------|-------------|----------------------|
| **Selection Guidelines (1)** | Default to T1 for evaluation/scoring agents | PASS: T1 selected for scoring task |
| **Selection Guidelines (2)** | T2+ only when agent produces file artifacts | PASS: Orchestrator handles file persistence |
| **Tier Constraints** | Worker agents MUST NOT be T5 | PASS: T1 is not T5 |
| **Pattern 1: Specialist** | Agent addresses single concern | PASS: Single concern (scoring only, not analysis or research) |
| **Pattern 2: Orchestrator-Worker** | Workers do not delegate further | PASS: T1 provides no Task tool for delegation |
| **Mode-to-Design (Scoring)** | Scoring agents typically T1 | PASS: Consistent with taxonomy |
| **Guardrail Selection** | Scoring agents use T1 validation rules | PASS: Matches "Scoring (convergent, T1)" guardrail type |

---

## Detailed Justification

### Why Not T2?

T2 (Read-Write) adds Write, Edit, and Bash tools. These enable file creation and modification.

**Rejection:** adv-scorer produces a structured score report as LLM output text, not as a file artifact. The orchestrator calling adv-scorer is responsible for persisting the report to disk (standard handoff pattern per Handoff Protocol). The agent itself has no write requirement.

**Evidence:** The task description states: "The calling orchestrator will handle storing the results." This explicitly assigns persistence responsibility to the calling context, not to adv-scorer.

### Why Not T3?

T3 (External) adds WebSearch, WebFetch, and Context7 tools for external data access.

**Rejection:** The S-014 rubric is provided as input (session context, not external). The artifact to score is also provided as a file path (session context). No external data sources are needed to apply the rubric.

**Scope:** Scoring is deterministic evaluation of artifact content against the provided rubric dimensions. No research, exploration, or external documentation lookup is required.

### Why Not T4 or T5?

T4 (Persistent) requires cross-session state via Memory-Keeper. T5 (Full) requires orchestration capability via Task tool.

**Rejection:** Single-session scoring task with no cross-session dependencies. No delegation needed. adv-scorer is invoked by an orchestrator and returns results to that orchestrator.

---

## Tool List for adv-scorer (T1)

Based on T1 tier definition (Read-Only):

- **Read** — Load artifact file from provided path
- **Glob** — Optional: enumerate files if rubric references multiple artifacts
- **Grep** — Optional: search artifact content for specific patterns

Minimum required: `Read` tool only.

---

## Output Specification

**Output Format:** Structured text report containing:
- Dimension-by-dimension scores (each of 6 S-014 dimensions)
- Dimension-level justifications (evidence from artifact)
- Composite weighted score (0.0-1.0)
- Overall assessment statement (pass/fail relative to threshold)
- Anti-leniency statement (safeguard against score inflation)

**Output Delivery:** Agent returns report as text; orchestrator handles persistence.

**Artifact Persistence:** Orchestrator is responsible for writing the score report to disk at a path it controls. adv-scorer does not write files.

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Agent attempts to write output | Guardrails: NEVER write files without orchestrator approval (P-020) |
| Score inflation (leniency bias) | Output filtering guardrail: Anti-leniency statement REQUIRED in every report |
| Missing artifact file | Input validation: Artifact path must be validated for existence before agent invocation |
| Dimension mismatch | Input validation: Rubric schema must be validated against S-014 standard before agent invocation |

---

## Cognitive Mode Alignment

**Cognitive Mode:** Convergent (focused evaluation, criteria-based selection)

**Mode-to-Design Implication:**
> | convergent | T1 or T2 (focused input) | sonnet or opus | Balanced allocation |

adv-scorer uses convergent mode with T1 tier tools, consistent with the design implications table.

---

## Summary

**Tool Tier: T1 (Read-Only)**

**Justification:**
1. Agent's sole responsibility is evaluation and scoring (T1 use case)
2. Agent reads artifact via `Read` tool (T1 capability)
3. Agent does not produce file artifacts (no T2 requirement)
4. No external research needed (no T3 requirement)
5. No cross-session state (no T4 requirement)
6. No delegation (no T5 requirement, and T5 prohibited for workers per H-01/P-003)
7. Consistent with example agent list in Tool Security Tiers table
8. Aligns with scoring agent guardrail type

**Confidence:** High. The task is a clear-cut evaluation scenario with read-only tool requirements. No ambiguity about missing features or hidden write operations. The orchestrator explicitly assumes persistence responsibility, confirming agent scope is evaluation only.

---

## References

- `agent-development-standards.md` § Tool Security Tiers (lines 219-247)
- `agent-development-standards.md` § Selection Guidelines (lines 231-237)
- `agent-development-standards.md` § Mode-to-Design Implications (lines 272-280)
- `agent-development-standards.md` § Guardrail Selection by Agent Type (lines 340-346)
- `agent-development-standards.md` § Pattern 2: Orchestrator-Worker (lines 174-191)
- `quality-enforcement.md` § Quality Gate (quality-enforcement.md lines 130-169)
