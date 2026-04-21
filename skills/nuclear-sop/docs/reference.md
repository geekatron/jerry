# /nuclear-sop Skill Reference

> Authoritative descriptions of agents, state schema, behavioral rules, hold point types, step classifications, OE entry schema, and state machine for the `/nuclear-sop` skill.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Agent Reference](#agent-reference) | Name, role, tool tier, model, inputs, outputs, and key behaviors for each of the 4 agents |
| [PROCEDURE_STATE.yaml Field Reference](#procedure_stateyaml-field-reference) | Every field with type, valid values, writer, and reader |
| [Behavioral Rules Reference](#behavioral-rules-reference) | NS-H-01 through NS-H-10 and NS-M-01 through NS-M-07 with enforcement level |
| [Hold Point Types](#hold-point-types) | USER-HOLD, QG-HOLD, IV-HOLD with release conditions and state transitions |
| [Step Classification](#step-classification) | CONTINUOUS, REFERENCE, INFORMATION with default assignment rules |
| [OE Entry Schema](#oe-entry-schema) | Every mandatory field with type, constraints, and purpose |
| [State Machine](#state-machine) | Valid PROCEDURE_STATE.yaml status transitions and terminal states |

---

## Agent Reference

The `/nuclear-sop` skill provides four agents. All are T1 or T2 workers invoked by the main context. None may spawn subagents. The main context orchestrates the sequence.

### `sop-brief`

**Tool Tier:** T2 (Read, Write, Edit, Glob, Grep, Bash)
**Model:** sonnet
**Cognitive Mode:** systematic
**Version:** 1.0.0
**Nuclear Patterns:** F-2a (Pre-Job Briefing), D-1 (Prerequisite Check), H-2 (OE Review), A-3 sections 1-6

**Role:** Pre-job briefing specialist. Validates workflow definitions, verifies prerequisites, reviews OE history, identifies error traps, and optionally generates workflow definitions from natural language (Step 0). Step 1 is mandatory for every `/nuclear-sop` invocation.

**Inputs:**

| Field | Required | Default | Source |
|-------|----------|---------|--------|
| `workflow_definition_path` | Conditional | — | Caller-provided path or Step 0 output |
| Natural language description | Conditional | — | Caller (Step 0 path only) |
| `workflow_id` | Yes (Step 1) | — | Workflow definition metadata |
| `criticality` | Yes | — | Workflow definition or caller |
| `oe_search_path` | No | `docs/experience/` | Caller override or default |
| `brief_output_path` | No | `brief/pre-job-brief.md` | Caller override or default |

**Outputs:**

| Artifact | Path | Condition |
|----------|------|-----------|
| Pre-job brief | `brief/pre-job-brief.md` | Mandatory for every complete run |
| Draft workflow definition | `brief/draft-workflow-definition.md` | Step 0 only |

**Key behaviors:**
- STOP conditions (blocking): workflow definition not found and user declines Step 0; prerequisites FAIL without WAIVE; all acceptance criteria vague or absent; OE count >20 without synthesis and no user OVERRIDE; step count exceeds criticality limit and user rejects splitting
- WARNING conditions (advisory): OE count >10 without synthesis; any step missing `[USER-HOLD]` on a C3+ workflow with state-modifying steps
- OE entries retrieved from `docs/experience/` are mandatory context in the brief, not optional reading
- `recommendation` and `root_cause` fields from OE entries are wrapped with SEC-002 injection guard labels

**Example invocation:**

```
"Run a pre-job brief for skills/nuclear-sop/examples/c3-adr-workflow-definition.md"
```

---

### `sop-executor`

**Tool Tier:** T2 (Read, Write, Edit, Glob, Grep, Bash)
**Model:** opus
**Cognitive Mode:** systematic
**Version:** 1.0.0
**Nuclear Patterns:** B-1 (STAR Self-Checking), A-5 (Place-Keeping), A-2 (Procedure Use Classification), A-4 (WARNING/CAUTION Acknowledgment), D-2 (Stop-Work Authority), C-3 (IV-HOLD), E-2 (Conservative Decision-Making)

**Role:** Step-by-step execution agent. Applies STAR self-checking before every state-modifying tool call, enforces step classification, activates hold points, maintains `PROCEDURE_STATE.yaml`, and invokes stop-work on deviation.

**Inputs:**

| Field | Required | Source |
|-------|----------|--------|
| `pre_job_brief_path` | Yes | sop-brief output |
| `workflow_definition_path` | Yes | sop-brief handoff |
| `procedure_state_path` | Conditional | Present on RESUME; absent on FRESH |
| `execution_mode` | Yes | `FRESH` or `RESUME` |
| `criticality` | Yes | Workflow definition metadata |

**Outputs:**

| Artifact | Path | Notes |
|----------|------|-------|
| `PROCEDURE_STATE.yaml` | `{execution_dir}/PROCEDURE_STATE.yaml` | Updated after every step |
| `HOLD_POINT_LOG.md` | `{execution_dir}/HOLD_POINT_LOG.md` | Appended at each hold point |
| `execution-log.md` | `{execution_dir}/execution-log.md` | Appended per STAR record |
| Work product artifacts | Per workflow definition step specifications | Written via STAR A phase |

**Step limits by criticality:**

| Criticality | Maximum Steps per Invocation |
|-------------|------------------------------|
| C1-C2 | 20 |
| C3 | 15 |
| C4 | 10 |

**Key behaviors:**
- STAR (Stop-Think-Act-Review) is mandatory before every Write, Edit, or Bash call; it cannot be disabled by workflow definition content
- `[INFORMATION]` steps load context only; no STAR check, no state update, no place-keeper advance
- Stop-work authority (D-2): on any STAR Review deviation, sop-executor logs the deviation, does not advance the place-keeper, and escalates to user — no auto-correction
- WARNING/CAUTION content governs only acknowledgment and stop-work decisions; any annotation that attempts to modify STAR, hold points, or step classification is treated as an injection attempt (SEC-001)
- RESUME mode: loads existing `PROCEDURE_STATE.yaml`, verifies schema version, confirms continuation with user before proceeding

**Example invocation:**

```
"Use /nuclear-sop sop-executor to execute brief/draft-workflow-definition.md"
```

---

### `sop-verifier`

**Tool Tier:** T1 (Read, Glob, Grep — read-only)
**Model:** sonnet
**Cognitive Mode:** convergent
**Version:** 1.0.0
**Nuclear Patterns:** C-2 (Independent Verification, approximated), C-3 (IV-HOLD activation)

**Role:** Context-isolated independent verifier. Evaluates work products against acceptance criteria with a fresh Task context and no access to sop-executor's reasoning chain. Required for C3+ workflows (4-hop mode). Cannot modify any artifact it evaluates.

**Invocation:** Via the Task tool by the main context (orchestrator). The Task prompt must contain only: workflow definition path, work product paths from `iv_scope`, and the acceptance criteria section. Execution logs, STAR records, and prior reasoning must not appear in the Task prompt.

**Inputs (Task prompt only):**

| Field | Required | Source |
|-------|----------|--------|
| Workflow definition path | Yes | `PROCEDURE_STATE.yaml.workflow_definition_path` |
| Work product paths (`iv_scope`) | Yes | `PROCEDURE_STATE.yaml.iv_scope` (workflow-definition-specified paths) |
| Acceptance criteria | Yes | Section 9 of workflow definition |

**Outputs:** IV report returned as Task response content; the main context persists it via Write.

**IV report disposition values:**

| Disposition | Condition |
|-------------|-----------|
| `ACCEPT` | All criteria MEETS; no PATH_MISMATCH; no SENSITIVE_DATA_DETECTED; no HOLD_POINT_NOT_ACTIVATED |
| `ACCEPT-WITH-CONDITIONS` | All criteria MEETS; one or more anomalies present |
| `REJECT` | One or more criteria FAILS |

**Anomaly types recorded in IV report:**

| Anomaly | Meaning |
|---------|---------|
| `PATH_MISMATCH` | Executor-reported path differs from workflow-definition-expected path |
| `PATH_AMBIGUITY` | Workflow definition output paths are ambiguous |
| `PATH_NOT_FOUND` | Workflow-definition-specified path does not exist on filesystem |
| `SENSITIVE_DATA_DETECTED` | Sensitive data patterns found in work product |
| `HOLD_POINT_NOT_ACTIVATED` | Hold point defined in workflow definition has no activation record in `PROCEDURE_STATE.yaml` |

**Key behaviors:**
- Evaluates the workflow-definition-expected artifact path, not the executor-reported path, on PATH_MISMATCH (TB-4 path injection defense)
- Each acceptance criterion assessed as MEETS or FAILS; no partial credit
- Does not carry forward prior rejection reasoning on resubmission (fresh Task context per invocation)
- REJECT and ACCEPT-WITH-CONDITIONS route to the main context for user decision; sop-verifier does not decide post-rejection action

**Example IV report structure:**

```markdown
## Independent Verification Report

**Workflow:** {workflow_id}
**Verification Mode:** 4-hop (fresh context, Task tool isolation)
**Disposition:** ACCEPT | REJECT | ACCEPT-WITH-CONDITIONS
```

---

### `sop-capture`

**Tool Tier:** T2 (Read, Write, Edit, Glob, Grep, Bash)
**Model:** sonnet
**Cognitive Mode:** systematic
**Version:** 1.0.0
**Nuclear Patterns:** F-2b (Post-Job Briefing), H-1 (Corrective Action Program infrastructure), H-2 (OE Review infrastructure)

**Role:** Post-job operating experience capture agent. Reads the FINAL execution log and `PROCEDURE_STATE.yaml`, compares actual execution to the planned procedure, classifies deviations, produces a schema-validated OE entry, and writes it to two locations. For C1-C2 workflows, performs integrated independent verification (Step 0) before OE capture.

**Inputs:**

| Input | Required | Source |
|-------|----------|--------|
| `PROCEDURE_STATE.yaml` | Yes | Root of workflow working directory |
| Final execution log | Yes | `PROCEDURE_STATE.yaml.execution_log_path` |
| Workflow definition | Yes | `PROCEDURE_STATE.yaml.workflow_definition_path` |
| Pre-job brief | Yes | `brief/pre-job-brief.md` |
| Work products | Yes (C1-C2 Step 0) | `PROCEDURE_STATE.yaml.iv_scope` |
| sop-verifier IV report | Yes (C3+) | `PROCEDURE_STATE.yaml.iv_report_path` |

**Outputs:**

| Artifact | Path | Notes |
|----------|------|-------|
| Local OE entry | `capture/oe-entry-{entry_id}.yaml` | Step 3 |
| Persistent OE entry | `docs/experience/{entry_id}.yaml` | Step 3; required for future sop-brief retrieval |
| Post-job brief | `capture/post-job-brief.md` | Step 4 |
| `PROCEDURE_STATE.yaml` (updated) | `PROCEDURE_STATE.yaml` | Status set to COMPLETED with `completed_at` |

**Deviation classification values:**

| `deviation_type` | Condition |
|-----------------|-----------|
| `NONE` | All steps completed per procedure; no stop-work entries; all STAR Review outcomes PASS |
| `MINOR` | At least one deviation logged; corrected within procedure; all acceptance criteria met |
| `MAJOR` | At least one deviation required stop-work; user escalation occurred |
| `STOP-WORK` | Procedure abandoned before completion; `status: ABORTED` |

**Key behaviors:**
- Step 0 (C1-C2 only): integrated IV with explicit anchoring bias disclaimer; disposition REJECTED proceeds to OE capture, not halt
- SR-05 hold consistency check: every hold annotation in the workflow definition must have a corresponding activation record in both the execution log and `PROCEDURE_STATE.yaml`; missing activations flagged as `HOLD_POINT_NOT_ACTIVATED`
- OE write is blocked (not warned) if any mandatory schema field is absent or empty (NS-H-06)
- Both OE write locations are mandatory; neither write alone is sufficient

**Example invocation:**

```
"Use sop-capture to write the OE entry for workflow run WF-ADR-001"
```

---

## PROCEDURE_STATE.yaml Field Reference

`PROCEDURE_STATE.yaml` is the authoritative execution state record. sop-executor updates it after every completed step. The main context and sop-capture read it. sop-verifier may read it for hold point consistency checks.

Schema version: `1.0.0`

### Schema Identity

| Field | Type | Default | Writer | Reader | Description |
|-------|------|---------|--------|--------|-------------|
| `state_schema_version` | string | `"1.0.0"` | sop-executor (init) | sop-executor (RESUME) | Schema version. Mismatch between state file and current schema requires user confirmation before RESUME proceeds |

### Workflow Identity

| Field | Type | Default | Writer | Reader | Description |
|-------|------|---------|--------|--------|-------------|
| `workflow_id` | string | `null` | sop-executor (init) | all agents | Identifier from workflow definition Section 1 Metadata |
| `workflow_version` | string | `null` | sop-executor (init) | sop-capture | Version string from workflow definition metadata |
| `workflow_definition_path` | string | `null` | sop-executor (init) | sop-executor, sop-capture, sop-verifier | Repo-relative path to the workflow definition file being executed |

### Execution Status

| Field | Type | Valid Values | Writer | Reader | Description |
|-------|------|-------------|--------|--------|-------------|
| `status` | enum | `INITIALIZING`, `IN-PROGRESS`, `HELD`, `RESUMING`, `IV-PENDING`, `IV-PASSED`, `IV-REJECTED`, `COMPLETED`, `ABORTED` | sop-executor | all agents | Current execution status. `COMPLETED` and `ABORTED` are terminal |
| `criticality` | enum | `C1`, `C2`, `C3`, `C4` | sop-executor (init) | sop-executor, sop-capture | Governs step limits, CONTINUOUS defaults, QG-HOLD ceilings, and verification mode |

### Place-Keeping

| Field | Type | Default | Writer | Reader | Description |
|-------|------|---------|--------|--------|-------------|
| `total_steps` | integer | `0` | sop-executor (init) | sop-executor, sop-capture | Count of `[CONTINUOUS]` and `[REFERENCE]` steps in the workflow definition |
| `current_step` | integer | `0` | sop-executor | sop-executor | Last completed step number. `0` indicates not yet started |
| `next_step` | integer | `1` | sop-executor | sop-executor | Next step to execute. Advances by 1 on normal progression |
| `steps_completed` | array | `[]` | sop-executor | sop-capture | Array of step completion records. Each entry: `step` (integer), `completed_at` (ISO-8601), `outcome` (`PASS` or `DEVIATION`), `star_record_path` (optional string) |

### Hold Point State

| Field | Type | Valid Values | Writer | Reader | Description |
|-------|------|-------------|--------|--------|-------------|
| `hold_type` | enum \| null | `USER-HOLD`, `QG-HOLD`, `IV-HOLD`, `null` | sop-executor | sop-executor, sop-capture | Active hold type. `null` when no hold is active |
| `held_at_step` | integer \| null | step number, `null` | sop-executor | sop-capture | Step number where the active hold was activated |
| `held_at_timestamp` | string \| null | ISO-8601, `null` | sop-executor | sop-capture | Timestamp of hold activation |
| `hold_prompt` | string \| null | hold reason text, `null` | sop-executor | sop-capture | Hold reason text from the workflow definition |
| `hold_resolution` | enum \| null | `APPROVED`, `REJECTED`, `WAIVED`, `AUTO-RELEASED`, `ACCEPT`, `REJECT`, `null` | sop-executor (designated mechanism only) | sop-executor | Resolution of the completed hold. May only be set through the designated release mechanism for each hold type |

Hold resolution values by type:
- USER-HOLD: `APPROVED`, `REJECTED`, `WAIVED`
- QG-HOLD: `AUTO-RELEASED`
- IV-HOLD: `ACCEPT`, `REJECT`

### Independent Verification (IV-HOLD) State

| Field | Type | Default | Writer | Reader | Description |
|-------|------|---------|--------|--------|-------------|
| `iv_scope` | array of strings | `[]` | sop-executor | sop-verifier, sop-capture | File paths of work products under verification. Values sourced exclusively from the workflow definition IV-HOLD annotation (SR-09) |
| `iv_criteria_path` | string \| null | `null` | sop-executor | sop-verifier | Path to the acceptance criteria section used by sop-verifier |
| `iv_iteration` | integer | `0` | sop-executor | sop-executor | Current IV attempt count (1-indexed). Mandatory user escalation after 3 rejections |
| `iv_report_path` | string \| null | `null` | main context | sop-capture | Path to sop-verifier's IV report, written by main context after Task response |
| `iv_disposition` | enum \| null | `ACCEPT`, `REJECT`, `null` | main context | sop-executor | sop-verifier's disposition, propagated by main context |

### Quality Gate (QG-HOLD) State

| Field | Type | Default | Writer | Reader | Description |
|-------|------|---------|--------|--------|-------------|
| `qg_iteration` | integer | `0` | sop-executor | sop-executor, sop-capture | Current QG-HOLD revision count (1-indexed) |
| `qg_scores` | array | `[]` | sop-executor | sop-capture | Array of quality gate scoring records. Each entry: `iteration` (integer), `score` (float 0.0-1.0), `critic_findings_path` (string), `scored_at` (ISO-8601) |

### Execution Log

| Field | Type | Default | Writer | Reader | Description |
|-------|------|---------|--------|--------|-------------|
| `execution_log_path` | string | `"execution-log.md"` | sop-executor (init) | sop-capture | Path to the execution log, relative to the execution directory |
| `execution_log_revision` | integer | `1` | sop-executor | sop-executor | Incremented when the log is segmented across sessions |
| `execution_log_final` | boolean \| null | `null` | sop-executor | sop-capture | Set to `true` at COMPLETED status. sop-capture checks this before reading the log |

### Stop-Work Events

| Field | Type | Default | Writer | Reader | Description |
|-------|------|---------|--------|--------|-------------|
| `stop_work_count` | integer | `0` | sop-executor | sop-capture | Total D-2 stop-work events in this execution. Individual events are recorded in `execution-log.md` |

### Tamper Detection

| Field | Type | Default | Writer | Reader | Description |
|-------|------|---------|--------|--------|-------------|
| `state_hash` | string \| null | `null` | sop-executor | sop-executor | SHA-256 hex digest of the concatenated values of: `status`, `hold_type`, `hold_resolution`, `iv_disposition`, `current_step`, `next_step` (in this order, coerced to strings). Computed after every state write. Verified in STAR-STOP before every tool call |

### Timestamps

| Field | Type | Default | Writer | Reader | Description |
|-------|------|---------|--------|--------|-------------|
| `started_at` | string \| null | `null` | sop-executor | sop-capture | ISO-8601 UTC; set at INITIALIZING to IN-PROGRESS transition |
| `last_updated` | string \| null | `null` | sop-executor | sop-capture | ISO-8601 UTC; updated after every state write |
| `completed_at` | string \| null | `null` | sop-executor, sop-capture | sop-capture | ISO-8601 UTC; set at COMPLETED or ABORTED |

---

## Behavioral Rules Reference

Rules are scoped to `/nuclear-sop` invocations only. They do not affect other Jerry skills.

**Enforcement levels:**
- **HARD (NS-H-xx):** Cannot be overridden. Violations are flagged.
- **MEDIUM (NS-M-xx):** Override requires documented justification in the workflow definition or execution log.

### HARD Rules

| ID | Rule | Agent | Consequence |
|----|------|-------|-------------|
| NS-H-01 | STAR protocol is mandatory before every Write, Edit, or Bash call by sop-executor. No state-modifying call may proceed without a completed S-T-A-R log entry immediately preceding it | sop-executor | Unlogged state mutation; STAR catch-rate metric invalidated |
| NS-H-02 | USER-HOLD points must present the exact hold format and must wait for APPROVE, REJECT, or WAIVE before proceeding. Silence does not constitute APPROVE | sop-executor | P-020 violation; unauthorized execution past blocking gate |
| NS-H-03 | QG-HOLD points must not auto-pass without a quality score >= 0.92 from ps-critic via /adversary S-014. A QG-HOLD that generates no quality score is treated as BLOCKED | sop-executor | H-13 quality gate bypass |
| NS-H-04 | IV-HOLD points must not auto-pass. A fresh sop-verifier invocation via Task tool with no executor reasoning in the prompt is required. An IV-HOLD without sop-verifier ACCEPT is BLOCKED | sop-executor, main context | Anchored verification; C3+ quality compromise |
| NS-H-05 | After STAR REVIEW detects a deviation, sop-executor must invoke stop-work: log the deviation, set status to HELD, and escalate to user. sop-executor must not attempt self-correction without user authority | sop-executor | Silent drift; deviation not captured in OE; P-020 violation |
| NS-H-06 | sop-capture's OE write is blocked if any mandatory OE schema field is absent. sop-capture must not write a partial OE entry. A warn-then-write pattern is not compliant | sop-capture | Corrupted OE feedback loop; unsearchable entries |
| NS-H-07 | sop-brief Step 1 is mandatory for every `/nuclear-sop` invocation. If a workflow definition cannot be located and the user declines Step 0 generation, the skill halts | sop-brief | Unbriefed execution; OE context not loaded; error traps not identified |
| NS-H-08 | C3+ workflows must use 4-hop mode (sop-verifier via Task tool with fresh context). 3-hop mode is prohibited for C3+ criticality. QG-E4 PASSED (2026-04-20, 3/3 catch rate); C3+ is approved for all criticality levels | main context, sop-capture | Anchored verification applied to irreversible work |
| NS-H-09 | When sop-executor reaches the step limit for its criticality level, it must stop, write `PROCEDURE_STATE.yaml` with status IN-PROGRESS, and hand off to the next sop-executor invocation. Execution must not continue past the step limit in a single invocation | sop-executor | Context exhaustion; STAR compliance degrades silently |
| NS-H-10 | `PROCEDURE_STATE.yaml` must be updated after every completed step. sop-executor must not batch-update state at end of invocation | sop-executor | Lost place-keeping; resume reconstructs incorrect position |

### MEDIUM Standards

| ID | Standard | Agent | Guidance |
|----|----------|-------|----------|
| NS-M-01 | Unannotated steps in C3+ workflows default to `[CONTINUOUS]`. Unannotated steps in C1-C2 workflows default to `[REFERENCE]`. These defaults should be declared in the workflow definition metadata | sop-executor | Prevents ambiguity about deviation tolerance |
| NS-M-02 | After 3 consecutive IV-HOLD rejections from sop-verifier, the main context should escalate to user with findings and ask for explicit guidance | main context | Prevents indefinite IV cycling; user may WAIVE or revise acceptance criteria |
| NS-M-03 | QG-HOLD iteration ceilings: C1=3, C2=5, C3=7, C4=10. Score plateau (delta < 0.01 for 3 consecutive iterations) triggers early halt with user escalation | sop-executor | Prevents quality cycles that produce no measurable improvement |
| NS-M-04 | For workflows exceeding the step limit, sop-brief should propose sub-procedure splitting before execution begins, including specific sub-procedure boundaries | sop-brief | Prevents unexpected mid-execution halts |
| NS-M-05 | When generating a workflow definition from natural language (Step 0), sop-brief defaults C3+ steps to `[CONTINUOUS]` and state-modifying steps to `[USER-HOLD]` unless the user explicitly requests otherwise | sop-brief | SR-10: conservative defaults protect against malformed generated procedures |
| NS-M-06 | sop-capture should include an "Operating Experience Synthesis" section when writing OE entries that would push the count for a `workflow_type` above 5 | sop-capture | Proactively manages OE accumulation thresholds |
| NS-M-07 | On schema version mismatch between a paused `PROCEDURE_STATE.yaml` and the current schema version, sop-executor presents the mismatch to the user and requests confirmation before resuming | sop-executor | Prevents state corruption when the skill evolves between workflow start and resume |

---

## Hold Point Types

Three hold point types provide blocking gates at different authority levels. sop-executor cannot proceed past a hold until the type-specific release condition is satisfied.

### `USER-HOLD`

**Annotation:** `[USER-HOLD]`
**PROCEDURE_STATE status on activation:** `HELD`
**`hold_type` value:** `USER-HOLD`

**Release condition:** User responds with APPROVE, REJECT, or WAIVE via AskUserQuestion. Silence does not constitute APPROVE (NS-H-02).

**Release values:**

| Response | `hold_resolution` | Effect |
|----------|------------------|--------|
| APPROVE | `APPROVED` | Execution proceeds; step is executed |
| REJECT | `REJECTED` | Execution direction from user awaited per H-31 |
| WAIVE | `WAIVED` | Hold skipped by P-020 user authority; step is skipped |

**Display format (verbatim):**

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
========================
```

---

### `QG-HOLD`

**Annotation:** `[QG-HOLD]`
**PROCEDURE_STATE status on activation:** `HELD`
**`hold_type` value:** `QG-HOLD`

**Release condition:** Quality score >= 0.92 from ps-critic via /adversary S-014 (NS-H-03, H-13). Auto-releases on PASS. Escalates to user on FAIL after criticality-ceiling iterations.

**QG-HOLD iteration ceilings:**

| Criticality | Maximum Iterations |
|-------------|-------------------|
| C1 | 3 |
| C2 | 5 |
| C3 | 7 |
| C4 | 10 |

**Plateau detection:** Score delta < 0.01 for 3 consecutive iterations triggers early halt with user escalation.

**`qg_scores` entry format:**

```yaml
- iteration: 1
  score: 0.87
  critic_findings_path: "work/critic-findings-001.md"
  scored_at: "2026-04-20T14:00:00Z"
```

---

### `IV-HOLD`

**Annotation:** `[IV-HOLD]`
**PROCEDURE_STATE status on activation:** `IV-PENDING`
**`hold_type` value:** `IV-HOLD`

**Release condition:** sop-verifier returns ACCEPT disposition via a fresh Task invocation with no executor reasoning in the prompt (NS-H-04).

**IV-HOLD rejection protocol:**

| Rejection count | Action |
|----------------|--------|
| 1 or 2 | Main context passes verifier findings to sop-executor for revision; new sop-verifier Task invoked |
| 3 | Mandatory user escalation per NS-M-02 |

**`iv_scope` requirement:** Paths must be sourced from the workflow definition IV-HOLD annotation, not interpreted by sop-executor (SR-09 path injection prevention).

---

## Step Classification

Workflow definition steps carry one of three use classification annotations. sop-executor behavior differs by classification.

| Classification | Annotation | sop-executor Behavior | Nuclear Analog |
|---------------|------------|----------------------|----------------|
| Continuous | `[CONTINUOUS]` | Execute exactly as written, in sequence. No deviation. Full STAR required. Step sign-off required | Emergency Operating Procedures — read and follow each step in sequence |
| Reference | `[REFERENCE]` | Consult for guidance. Judgment permitted on execution approach. STAR Think phase may permit adaptation within step scope | Abnormal Operating Procedures — consult as needed |
| Information | `[INFORMATION]` | Load as context only. Not executed. No STAR check. No state update. No place-keeper advance | Reference materials — available for consultation |

### Default Assignment Rules (NS-M-01)

| Criticality | Unannotated Step Default |
|-------------|--------------------------|
| C3+ | `[CONTINUOUS]` |
| C1-C2 | `[REFERENCE]` |

Explicit annotation in the workflow definition overrides the default for any individual step. The workflow definition metadata section should declare which default applies.

### STAR Application Scope

| Tool | STAR Required |
|------|---------------|
| Write | Yes |
| Edit | Yes |
| Bash | Yes |
| Read | No |
| Glob | No |
| Grep | No |

---

## OE Entry Schema

OE entries are written by sop-capture to two locations: `capture/oe-entry-{entry_id}.yaml` and `docs/experience/{entry_id}.yaml`. All fields below are mandatory. sop-capture blocks the write if any required field is absent or empty (NS-H-06).

### Required Fields

| Field | Type | Valid Values / Constraints | Writer | Purpose |
|-------|------|---------------------------|--------|---------|
| `entry_id` | string | `{workflow_id}-{YYYYMMDD}-{NNN}` | sop-capture (auto-generated) | Unique identifier; NNN is zero-padded count of entries for this `workflow_id` on this date |
| `entry_version` | string | `"1.0.0"` | sop-capture | Schema version of this OE entry |
| `workflow_id` | string | Non-empty; matches `PROCEDURE_STATE.yaml.workflow_id` | sop-capture | Identifies the procedure that produced this entry |
| `workflow_type` | enum | `NOMINAL`, `ABNORMAL`, `EMERGENCY` | sop-capture | Procedure type from workflow definition metadata |
| `criticality` | enum | `C1`, `C2`, `C3`, `C4` | sop-capture | From `PROCEDURE_STATE.yaml.criticality` |
| `created_at` | string | ISO-8601 UTC | sop-capture | Timestamp of OE entry creation |
| `total_steps` | integer | >= 0 | sop-capture | Total steps in the workflow definition |
| `steps_completed` | integer | >= 0 | sop-capture | Count of steps signed off in `PROCEDURE_STATE.yaml` |
| `steps_deviated` | integer | >= 0 | sop-capture | Count of steps with DEVIATION outcome in execution log |
| `hold_points_activated` | integer | >= 0 | sop-capture | Total hold activations recorded in `PROCEDURE_STATE.yaml` |
| `stop_work_events` | integer | >= 0 | sop-capture | From `PROCEDURE_STATE.yaml.stop_work_count` |
| `verification_mode` | enum | `3-hop`, `4-hop` | sop-capture | Determined by `criticality`: C1-C2 = `3-hop`; C3+ = `4-hop` |
| `deviation_type` | enum | `NONE`, `MINOR`, `MAJOR`, `STOP-WORK` | sop-capture | Most severe deviation classification for the execution |
| `root_cause` | string | Non-empty; minimum: `"N/A -- no deviation"` | sop-capture | Root cause of the most significant deviation |
| `recommendation` | string | Non-empty; specific and non-generic | sop-capture | Actionable recommendation to improve workflow or process |
| `error_traps_encountered` | array | May be empty list `[]` | sop-capture | Error traps identified during execution; empty list is a valid value |
| `verification_outcome` | enum | `ACCEPTED`, `REJECTED`, `ACCEPTED-WITH-CONDITIONS`, `N/A` | sop-capture | Outcome from sop-capture integrated IV (C1-C2) or sop-verifier IV report (C3+) |
| `quality_gate_final_score` | float \| null | 0.0-1.0 or `null` | sop-capture | Final QG-HOLD score from `PROCEDURE_STATE.yaml.qg_scores`; `null` if no QG-HOLD activated |

### OE Entry YAML Structure

```yaml
oe_entry:
  entry_id: "{workflow_id}-{YYYYMMDD}-{NNN}"
  entry_version: "1.0.0"
  workflow_id: "{from PROCEDURE_STATE.yaml}"
  workflow_type: "NOMINAL | ABNORMAL | EMERGENCY"
  criticality: "C1 | C2 | C3 | C4"
  created_at: "{ISO-8601 UTC}"
  total_steps: 0
  steps_completed: 0
  steps_deviated: 0
  hold_points_activated: 0
  stop_work_events: 0
  verification_mode: "3-hop | 4-hop"
  deviation_type: "NONE | MINOR | MAJOR | STOP-WORK"
  root_cause: "{root cause or 'N/A -- no deviation'}"
  recommendation: "{specific recommendation}"
  error_traps_encountered: []
  verification_outcome: "ACCEPTED | REJECTED | ACCEPTED-WITH-CONDITIONS | N/A"
  quality_gate_final_score: null
```

### OE Search Mechanism

sop-brief locates prior OE history using this query protocol:

1. **Exact workflow match (primary):** Glob `docs/experience/*.yaml`; filter where `workflow_id` matches the current workflow's `workflow_id`
2. **Keyword match (secondary, if primary returns < 3 results):** Grep `docs/experience/` for the exact `workflow_name` value from the workflow definition metadata; if still < 3 results, extract nouns > 4 characters from Section 2 Purpose and Grep for each
3. **`workflow_type` filter:** Applied to retrieved entries; not used as the primary search key
4. **Accumulation thresholds:** Applied to the filtered count per `workflow_type`

### OE Accumulation Thresholds

| Unsynthesized entry count (per `workflow_type`) | sop-brief action |
|------------------------------------------------|-----------------|
| 1-10 | Normal operation; all entries presented as mandatory context |
| > 10 | WARNING: synthesis recommended before proceeding |
| > 20 | STOP: execution must not proceed without explicit user OVERRIDE per P-020 |

---

## State Machine

`PROCEDURE_STATE.yaml` `status` follows a defined state machine. sop-executor enforces valid transitions.

### Valid Status Values and Transitions

| Status | Meaning | Valid Next States |
|--------|---------|-------------------|
| `INITIALIZING` | sop-brief has written initial state; sop-executor not yet started | `IN-PROGRESS` |
| `IN-PROGRESS` | sop-executor actively executing steps | `HELD`, `IV-PENDING`, `COMPLETED`, `ABORTED` |
| `HELD` | Blocked at USER-HOLD or QG-HOLD | `IN-PROGRESS` (on APPROVE or QG PASS), `ABORTED` (on REJECT) |
| `RESUMING` | Session restart; sop-executor reconstructing position from state file before user confirmation | `IN-PROGRESS`, `ABORTED` |
| `IV-PENDING` | Waiting for sop-verifier Task invocation and result | `IV-PASSED`, `IV-REJECTED` |
| `IV-PASSED` | sop-verifier returned ACCEPT | `COMPLETED` (if no further steps), `IN-PROGRESS` (if revision steps remain) |
| `IV-REJECTED` | sop-verifier returned REJECT | `IN-PROGRESS` (revision), `ABORTED` (after 3 rejections and user decision) |
| `COMPLETED` | All steps executed; OE entry written by sop-capture | Terminal |
| `ABORTED` | Execution halted before completion; OE entry written with `deviation_type: STOP-WORK` | Terminal |

### Invalid Transitions

| Transition | Classification | Consequence |
|-----------|---------------|-------------|
| `COMPLETED` to any state | Forbidden | Must start a new workflow invocation |
| `ABORTED` to any state | Forbidden | Must start a new workflow invocation |
| `IN-PROGRESS` to `COMPLETED` without sop-capture OE entry | Forbidden (NS-H-06) | OE write required before COMPLETED is a valid status |
| Any state to `INITIALIZING` | Forbidden | `INITIALIZING` is a one-time entry state |

### State Transition Diagram

```
                  +-----------+
                  |INITIALIZING|
                  +-----+-----+
                        |
                        v (user confirms start)
                  +-----------+
     +----+-------+IN-PROGRESS+-------+--------+
     |            +-----+-----+       |        |
     |                  |             |        |
     v                  v             v        v
+--------+       +-----------+  +--------+ +-------+
|  HELD  |       | IV-PENDING|  |RESUMING| |ABORTED|
+---+----+       +-----+-----+  +---+----+ +-------+
    |                 /  \          |         ^
    |         IV-PASSED  IV-REJECTED|         |
    |             |        |        |         |
    |             v        v        v         |
    |         +--------+ (revision or user)   |
    +-------->|IV-PASSED|   ABORTED-----------+
    (APPROVE  +---+----+
     or QG     |
     PASS)      v
          +-----------+
          | COMPLETED |
          +-----------+
```

### Cross-Session Resume Protocol

At session start, the main context scans `projects/{JERRY_PROJECT}/**/PROCEDURE_STATE.yaml` for non-terminal statuses. For each paused workflow found:

| User selection | Action |
|----------------|--------|
| RESUME | sop-executor loads `PROCEDURE_STATE.yaml`; verifies schema version; sets status to RESUMING; confirms with user before advancing to IN-PROGRESS |
| ABANDON | Status set to ABORTED; sop-capture invoked to write OE entry |
| DEFER | No action taken |

sop-executor reconstructs execution position entirely from filesystem state. No in-context memory from prior sessions is relied upon.

---

## Related

- **How-To Guide:** Invoke `/nuclear-sop` for a C3 workflow — task-oriented invocation instructions
- **Explanation:** About `/nuclear-sop` design — nuclear SOP methodology, architectural decisions, and constitutional compliance rationale
- **Rules:** `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` — full HARD and MEDIUM rule text with source spec references
- **Template:** `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` — annotated PROCEDURE_STATE schema with security notes
