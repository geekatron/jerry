# Nuclear SOP Behavior Rules

> Skill-scoped behavioral rules for `/nuclear-sop`. Loaded alongside agent definitions.
> These rules apply ONLY within `/nuclear-sop` invocations and do not affect other Jerry skills.
> **Version:** 1.1.0
> **Source Spec:** `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-research-20260319-001/ps/phase-4/ps-synthesizer-001/skill-specification-synthesis.md` v2.0.0 Sections 1.5 - 1.11

## Document Sections

| Section | Purpose |
|---------|---------|
| [HARD Rules](#hard-rules) | Non-overridable nuclear-sop constraints |
| [MEDIUM Standards](#medium-standards) | Overridable standards with documented justification |
| [Hold Point Authority Table](#hold-point-authority-table) | Three hold point types with release conditions |
| [Procedure Use Classification](#procedure-use-classification) | CONTINUOUS / REFERENCE / INFORMATION rules |
| [STAR Protocol](#star-protocol) | Stop-Think-Act-Review sequence and application scope |
| [Step Limits by Criticality](#step-limits-by-criticality) | Maximum steps per sop-executor invocation |
| [OE Accumulation Enforcement](#oe-accumulation-enforcement) | WARNING and STOP thresholds for OE feedback loop |
| [3-Hop vs. 4-Hop Mode Selection](#3-hop-vs-4-hop-mode-selection) | Criticality-bound verification mode rules |
| [PROCEDURE_STATE.yaml State Machine](#procedure_stateyaml-state-machine) | Valid state transitions and resume protocol |

---

## HARD Rules

> These rules CANNOT be overridden within `/nuclear-sop` skill invocations. Violations will be flagged.

| ID | Rule | Agent | Consequence |
|----|------|-------|-------------|
| NS-H-01 | STAR protocol is MANDATORY before every state-modifying tool call (Write, Edit, Bash) executed by sop-executor. No state-modifying call may proceed without a completed S-T-A-R log entry immediately preceding it. | sop-executor | Unlogged state mutation; STAR catch-rate metric invalidated; behavioral validation fails |
| NS-H-02 | USER-HOLD points MUST present the exact hold format (step, description, hold reason, preceding result) and MUST wait for APPROVE, REJECT, or WAIVE before proceeding. sop-executor MUST NOT infer APPROVE from silence or context. | sop-executor | P-020 violation; unauthorized execution past blocking gate |
| NS-H-03 | QG-HOLD points MUST NOT auto-pass without a quality score >= 0.92 from ps-critic via /adversary S-014. A QG-HOLD that generates no quality score is treated as BLOCKED, not as PASS. | sop-executor | H-13 quality gate bypass |
| NS-H-04 | IV-HOLD points MUST NOT auto-pass. A fresh sop-verifier invocation (Task tool, new context, no executor reasoning in input) is required. An IV-HOLD without a sop-verifier ACCEPT disposition is BLOCKED. | sop-executor, main context | Anchored verification; C3+ quality compromise |
| NS-H-05 | After STAR REVIEW detects a deviation (outcome did not match expectation), sop-executor MUST invoke Stop-Work: log the deviation, set PROCEDURE_STATE.yaml status to HELD, and escalate to user per P-020. sop-executor MUST NOT attempt self-correction without user authority. | sop-executor | Silent drift; deviation not captured in OE; P-020 violation |
| NS-H-06 | sop-capture's OE write is BLOCKED if any mandatory OE schema field is absent. sop-capture MUST NOT write a partial OE entry to `docs/experience/`. A warning-then-write pattern is not compliant. | sop-capture | Corrupted OE feedback loop; unsearchable entries |
| NS-H-07 | sop-brief Step 1 is MANDATORY for every `/nuclear-sop` invocation. There is no execution path that bypasses sop-brief. If a workflow definition cannot be located and the user declines Step 0 generation, the skill HALTS. | sop-brief | Unbriefed execution; OE context not loaded; error traps not identified |
| NS-H-08 | C3+ workflows MUST use 4-hop mode (sop-verifier via Task tool with fresh context). The 3-hop mode (sop-capture integrated IV) is PROHIBITED for C3+ criticality until a governance ruling permits it. **GOVERNANCE DEADLINE NOTE:** If the H-36 governance ruling eliminates sop-verifier (60-day deadline default per SKILL.md), NS-H-08 is superseded and MUST be revised to reflect 3-hop mode as the permanent architecture for all criticality levels. This revision MUST be tracked as a worktracker entity with a deadline set at the 60-day mark from Phase 1 delivery. Until that revision is completed and merged, NS-H-08 remains as written. | main context, sop-capture | Anchored verification applied to irreversible work; quality compromise |
| NS-H-09 | When sop-executor reaches the step limit for its criticality level (see [Step Limits by Criticality](#step-limits-by-criticality)), it MUST STOP, write PROCEDURE_STATE.yaml with status IN-PROGRESS, and hand off to the next sop-executor invocation with the sub-procedure definition path and current execution log path. Execution MUST NOT continue past the step limit in a single invocation. | sop-executor | Context exhaustion; STAR compliance degrades silently |
| NS-H-10 | PROCEDURE_STATE.yaml MUST be updated after every completed step. sop-executor MUST NOT batch-update state at end of invocation. State must be durable between any two tool calls. | sop-executor | Lost place-keeping; resume after interruption reconstructs incorrect position |

---

## MEDIUM Standards

> Override requires documented justification in the workflow definition or execution log.

| ID | Standard | Guidance |
|----|----------|----------|
| NS-M-01 | Unannotated steps in C3+ workflows SHOULD default to `[CONTINUOUS]`. Unannotated steps in C1-C2 workflows SHOULD default to `[REFERENCE]`. These defaults SHOULD be declared in the workflow definition metadata section. | Prevents ambiguity for sop-executor about deviation tolerance. Explicit annotation is always preferred. |
| NS-M-02 | After 3 consecutive IV-HOLD rejections from sop-verifier, main context SHOULD escalate to user with findings and ask for explicit guidance per H-31 and P-020. | Prevents indefinite IV cycling that consumes context and delays resolution. User may WAIVE or revise acceptance criteria. |
| NS-M-03 | QG-HOLD iteration ceilings SHOULD be respected: C1=3, C2=5, C3=7, C4=10. Score plateau (delta < 0.01 for 3 consecutive iterations) SHOULD trigger early halt with user escalation per RT-M-010. | Prevents quality theater -- cycles that produce no measurable score improvement. |
| NS-M-04 | For workflows exceeding the step limit, sop-brief SHOULD propose sub-procedure splitting before execution begins. The split proposal SHOULD include specific sub-procedure boundaries and pass the current execution log path as context for each subsequent invocation. | Prevents unexpected mid-execution halts; sets user expectations before sop-executor begins. |
| NS-M-05 | When generating a workflow definition from natural language (Step 0), sop-brief SHOULD default C3+ steps to `[CONTINUOUS]` and state-modifying steps (Write/Edit/Bash actions) to `[USER-HOLD]` unless the user's natural language description explicitly requests otherwise. | SR-10 requirement: conservative defaults protect against malformed generated procedures. |
| NS-M-06 | sop-capture SHOULD include an "Operating Experience Synthesis" section when writing OE entries that would push the count for a `workflow_type` above 5. The synthesis section SHOULD summarize patterns across prior entries, not just document the current execution. | Proactively manages the OE accumulation threshold before it approaches WARNING (10) or STOP (20). |
| NS-M-07 | On schema version mismatch between a paused PROCEDURE_STATE.yaml and the current schema version, sop-executor SHOULD present the mismatch to the user (P-020) and request confirmation before resuming. Silent resume against an incompatible schema is a NS-H-05 violation path. | Prevents state corruption when the skill evolves between a workflow's start and resume. |

---

## Hold Point Authority Table

Three hold point types provide blocking gates at different authority levels. Each type requires a specific release condition before sop-executor may proceed.

| Type | Annotation | Trigger | Release Condition | Authority | PROCEDURE_STATE Status |
|------|-----------|---------|-------------------|-----------|------------------------|
| `USER-HOLD` | `[USER-HOLD]` | Step requires explicit human approval | User responds APPROVE, REJECT, or WAIVE | P-020 -- user authority | `status: HELD`, `hold_type: USER-HOLD` |
| `QG-HOLD` | `[QG-HOLD]` | Phase boundary quality gate | Quality score >= 0.92 from ps-critic (H-13). Auto-releases on PASS; escalates on FAIL after ceiling iterations. | /adversary S-014 | `status: HELD`, `hold_type: QG-HOLD`, tracks `qg_iteration` and `qg_scores` |
| `IV-HOLD` | `[IV-HOLD]` | Independent verification required | sop-verifier produces ACCEPT disposition | sop-verifier via Task tool (fresh context) | `status: IV-PENDING`, `iv_scope: [file paths]` |

### USER-HOLD Display Format

sop-executor MUST display USER-HOLD points in exactly this format:

```
=== USER-HOLD POINT ===
Step: {number} - {title}
Description: {step description from workflow definition}
Hold Reason: {hold prompt from workflow definition}
Preceding Step Result: {summary of last completed step}

Please respond with:
- APPROVE to proceed with this step
- REJECT to stop and provide alternative guidance
- WAIVE to skip this hold point (P-020: your authority)
======================
```

### IV-HOLD Rejection Protocol

After sop-verifier returns REJECT:
1. Main context passes verifier findings back to sop-executor for revision
2. Sop-executor revises and updates PROCEDURE_STATE.yaml `iv_iteration`
3. Main context invokes a new sop-verifier Task (fresh context, no prior reasoning)
4. After 3 rejections: mandatory user escalation per NS-M-02

---

## Procedure Use Classification

Steps in workflow definitions are annotated with one of three use classifications. sop-executor behavior differs by classification.

| Classification | Annotation | sop-executor Behavior | Nuclear Analog | C1-C4 Default |
|---------------|------------|----------------------|----------------|---------------|
| **Continuous** | `[CONTINUOUS]` | Execute exactly as written, in sequence. No deviation. Full STAR required. Step sign-off required. | EOPs, STPs -- "read and follow each step in sequence" | Default for C3+ unannotated steps |
| **Reference** | `[REFERENCE]` | Consult step for guidance. Agent may exercise judgment on execution approach. STAR Think phase may permit adaptation within scope. | AOPs, ARPs -- "consult as needed" | Default for C1-C2 unannotated steps |
| **Information** | `[INFORMATION]` | Background context loaded into brief. Not executed as a step. | Reference materials -- "available for consultation" | Any criticality; context only |

### Default Assignment Rules (NS-M-01)

- C3+ workflows: steps without annotation default to `[CONTINUOUS]`
- C1-C2 workflows: steps without annotation default to `[REFERENCE]`
- These defaults may be overridden per-step in the workflow definition
- The workflow definition metadata section SHOULD declare which default applies

---

## STAR Protocol

STAR (Stop-Think-Act-Review) is applied by sop-executor before every state-modifying tool call: Write, Edit, and Bash.

### Four-Step Sequence

```
S - STOP:   Log current step number and target action.
            Verify: Am I on the correct step per the workflow definition?
            Verify: Is this the correct file/target per the step specification?

T - THINK:  What is the expected outcome of this action?
            What are the preconditions for this step?
            What could go wrong? (Check WARNING/CAUTION from workflow definition)
            Is this step [CONTINUOUS] (execute exactly) or [REFERENCE] (judgment permitted)?
            If uncertain: invoke conservative decision-making per H-31.

A - ACT:    Execute the tool call.
            Maintain focus on the specified target.
            Do not expand scope beyond the step specification.

R - REVIEW: Did the outcome match expectation?
            If YES: sign off step in execution log; advance place-keeper;
                    update PROCEDURE_STATE.yaml.
            If NO:  STOP WORK (NS-H-05). Log deviation. Escalate per hold point type.
```

### STAR Scope

STAR applies to: Write, Edit, Bash

STAR does NOT apply to: Read, Glob, Grep (read-only operations do not mutate state)

### STAR vs. S-010 Self-Refine

These are not the same mechanism and serve different purposes.

| Dimension | STAR (NS-H-01) | S-010 Self-Refine |
|-----------|----------------|-------------------|
| Timing | Pre-action: before each tool call | Post-completion: after entire deliverable |
| Scope | Single step / single tool call | Entire output artifact |
| Action on failure | Stop-Work immediately (NS-H-05) | Revision: re-enter reasoning loop |
| State tracking | Updates PROCEDURE_STATE.yaml per step | No state file |
| Value for CONTINUOUS steps | High -- enforces stop-check-act-review sequencing | Low -- post-hoc cannot undo executed steps |

### LLM Implementation Note

Both STAR reasoning and the tool call are generated in the same inference pass. The temporal separation is a structural constraint in the prompt, not a physical interruption as in nuclear plant operations. The value is structural (forced deliberate pause before acting) not temporal (physical delay). This limitation is disclosed per P-022.

---

## Step Limits by Criticality

sop-executor enforces a maximum step count per invocation to prevent context exhaustion during long workflows (AE-006c risk).

| Criticality | Maximum Steps per Invocation | Rationale |
|-------------|-----------------------------|-|
| C1-C2 | 20 steps | Lower-stakes work; context exhaustion has lesser consequence |
| C3 | 15 steps | Significant work; STAR compliance degrades at high context fill |
| C4 | 10 steps | Critical work; every step must execute with full STAR attention |

### Exceeding the Step Limit

When a workflow definition contains more steps than the criticality limit allows:

1. sop-brief Step 1 MUST detect the overage and propose sub-procedure splitting before execution begins (NS-M-04)
2. If the user approves splitting, the workflow is divided at natural checkpoints into sub-procedures
3. Each sub-procedure is a separate sop-executor invocation with:
   - Its own sub-procedure definition path
   - The current execution log path passed as context
   - PROCEDURE_STATE.yaml from the preceding invocation
4. Sub-procedure boundaries within a single skill invocation are NOT additional hops (H-36)

---

## OE Accumulation Enforcement

sop-brief enforces thresholds on OE entry accumulation per `workflow_type` to prevent the feedback loop from degrading into an unsynthesized backlog.

### OE Search Mechanism

sop-brief locates prior OE history using the following query protocol:

1. **Exact workflow match (primary):** Glob `docs/experience/*.yaml` then filter entries where `workflow_id` matches the current workflow's `workflow_id` field. This catches OE from previous executions of the same procedure.
2. **Keyword match (secondary, if primary returns < 3 results):** Read the workflow definition's `Purpose` section; extract the 3-5 most specific noun phrases; Grep `docs/experience/` for each phrase. Results are de-duplicated.
3. **`workflow_type` filter:** After either query, filter results by `workflow_type` field (`NOMINAL`, `ABNORMAL`, or `EMERGENCY`). The `workflow_type` value is a filter on retrieved entries, NOT the primary search key. Do not use `workflow_type` as the sole Glob pattern — entries for NOMINAL ADR workflows and NOMINAL agent-build workflows share the same `workflow_type` value but are not relevant to each other.
4. **Count:** Apply OE accumulation thresholds (WARNING/STOP) to the filtered count, not the total entry count in `docs/experience/`.

| Count (per workflow_type, unsynthesized) | Action | Authority |
|------------------------------------------|--------|-----------|
| 1-10 entries | Normal operation; present all entries as mandatory context in pre-job brief | Automatic |
| > 10 entries | WARNING displayed in pre-job brief: "N OE entries exist for this workflow_type without a synthesis entry. Consider running /problem-solving ps-synthesizer to distill lessons before proceeding." | Automatic (advisory) |
| > 20 entries | STOP: sop-brief halts and presents the count to the user. Execution MUST NOT proceed without explicit user override per P-020. User may override with stated justification. | User-gated (P-020) |

### OE Entry Schema (Mandatory Fields)

All fields below are REQUIRED. sop-capture blocks the write if any field is missing or empty (NS-H-06).

```yaml
oe_entry:
  # Identity (REQUIRED)
  entry_id: "{workflow_id}-{YYYYMMDD}-{NNN}"
  entry_version: "1.0.0"
  workflow_id: "{from PROCEDURE_STATE.yaml}"
  workflow_type: "NOMINAL | ABNORMAL | EMERGENCY"
  criticality: "C1 | C2 | C3 | C4"
  created_at: "{ISO-8601}"

  # Execution summary (REQUIRED)
  total_steps: 0
  steps_completed: 0
  steps_deviated: 0
  hold_points_activated: 0
  stop_work_events: 0
  verification_mode: "3-hop | 4-hop"

  # Deviation classification (REQUIRED)
  deviation_type: "NONE | MINOR | MAJOR | STOP-WORK"

  # Knowledge content (REQUIRED -- free text but must be non-empty)
  root_cause: "{root cause of most significant deviation, or 'N/A -- no deviation'}"
  recommendation: "{specific recommendation to improve workflow or process}"
  error_traps_encountered: []

  # Disposition (REQUIRED)
  verification_outcome: "ACCEPTED | REJECTED | ACCEPTED-WITH-CONDITIONS | N/A"
  quality_gate_final_score: null
```

OE entries are written to BOTH:
- Local capture directory for the workflow: `projects/{JERRY_PROJECT}/{workflow_id}/capture/`
- Global OE registry: `docs/experience/{entry_id}.yaml`

---

## 3-Hop vs. 4-Hop Mode Selection

Verification mode is determined by workflow criticality. Mode selection is NOT at the discretion of the executing agent.

| Criticality | Mode | Verification Agent | Anchoring Bias | H-36 Status |
|-------------|------|--------------------|----------------|-------------|
| C1-C2 | 3-hop | sop-capture integrated IV (Step 0) | Present -- capture has access to execution log before verifying | Unambiguously compliant |
| C3+ | 4-hop | sop-verifier via Task tool (fresh context) | None -- verifier sees only work products and acceptance criteria | Governance ruling pending (60-day deadline) |

### 3-Hop Sequence (C1-C2)

```
Main context -> sop-brief (Hop 1)
Main context -> sop-executor (Hop 2)
Main context -> sop-capture with integrated IV Step 0 (Hop 3)
```

### 4-Hop Sequence (C3+)

```
Main context -> sop-brief (Hop 1)
Main context -> sop-executor (Hop 2)
Main context -> sop-verifier via Task (Hop 3, governance ambiguity)
Main context -> sop-capture (Hop 4, exceeds limit if Hop 3 is a hop)
```

### Governance Deadline

If no H-36 ruling within 60 days of Phase 1 delivery: 3-hop mode becomes permanent for all criticality levels. sop-verifier is eliminated; sop-capture integrated IV is the universal verification mechanism with anchoring bias limitation documented.

---

## PROCEDURE_STATE.yaml State Machine

### Valid Statuses

| Status | Meaning | Valid Next States |
|--------|---------|-------------------|
| `INITIALIZING` | sop-brief has written initial state; sop-executor not yet started | `IN-PROGRESS` |
| `IN-PROGRESS` | sop-executor actively executing steps | `HELD`, `IV-PENDING`, `COMPLETED`, `ABORTED` |
| `HELD` | Blocked at USER-HOLD or QG-HOLD | `IN-PROGRESS` (on APPROVE or QG PASS), `ABORTED` (on REJECT) |
| `RESUMING` | Session restart; sop-executor reconstructing position from state file | `IN-PROGRESS` |
| `IV-PENDING` | Waiting for sop-verifier Task invocation and result | `IV-PASSED`, `IV-REJECTED` |
| `IV-PASSED` | sop-verifier returned ACCEPT | `COMPLETED` (if no further steps), `IN-PROGRESS` (if revision steps remain) |
| `IV-REJECTED` | sop-verifier returned REJECT | `IN-PROGRESS` (return to sop-executor for revision), `ABORTED` (after 3 rejections + user decision) |
| `COMPLETED` | All steps executed; OE entry written | Terminal (no valid transitions) |
| `ABORTED` | Execution halted before completion; OE entry written with STOP-WORK deviation_type | Terminal (no valid transitions) |

### Invalid Transitions (HARD)

- `COMPLETED` -> any other state: FORBIDDEN (must start new workflow invocation)
- `ABORTED` -> any other state: FORBIDDEN (must start new workflow invocation)
- `IN-PROGRESS` -> `COMPLETED` without sop-capture OE entry: FORBIDDEN (NS-H-06)
- Any state -> `INITIALIZING`: FORBIDDEN (INITIALIZING is a one-time entry state)

### Cross-Session Resume Protocol

At session start, the main context SHOULD scan `projects/{JERRY_PROJECT}/**/PROCEDURE_STATE.yaml` for non-terminal statuses (any status other than COMPLETED or ABORTED). If paused workflows are found:

1. Present each paused workflow to the user with: workflow_id, current step, status, criticality (P-020)
2. User selects: RESUME, ABANDON (sets status ABORTED + triggers OE capture), or DEFER (no action)
3. If RESUME: sop-executor reconstructs position from PROCEDURE_STATE.yaml
4. On schema version mismatch between state file and current schema: present to user before resuming (NS-M-07)

sop-executor MUST reconstruct execution position entirely from filesystem state. No in-context memory from prior sessions is available or relied upon.
