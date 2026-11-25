# /nuclear-sop How-To Guides

> Five goal-oriented guides for competent users of the `/nuclear-sop` skill.

## Document Sections

| Section | Purpose |
|---------|---------|
| [How to Write a Workflow Definition](#how-to-write-a-workflow-definition) | Create a new procedure file from the template |
| [How to Add Hold Points to a Procedure](#how-to-add-hold-points-to-a-procedure) | Add USER-HOLD, QG-HOLD, and IV-HOLD annotations to steps |
| [How to Resume a Paused Execution](#how-to-resume-a-paused-execution) | Restart execution after interruption using PROCEDURE_STATE.yaml |
| [How to Review OE Entries from Past Executions](#how-to-review-oe-entries-from-past-executions) | Search and interpret docs/experience/ entries |
| [How to Wrap Another Skill with /nuclear-sop](#how-to-wrap-another-skill-with-nuclear-sop) | Apply nuclear rigor around /problem-solving or /eng-team workflows |

---

## How to Write a Workflow Definition

> Create a new workflow definition file that sop-brief and sop-executor can execute.

### Before You Begin

You need:
- A defined goal with an observable end state
- Knowledge of the criticality level (C1-C4) for the workflow
- The template at `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md`

### Steps

#### 1. Copy the template to your target location

Place the workflow definition inside your project's working directory:

```
cp skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md \
   projects/{JERRY_PROJECT}/workflows/{workflow-id}-workflow-definition.md
```

If you need to generate the file from a natural language description instead of hand-authoring, invoke sop-brief Step 0:

```
Use /nuclear-sop sop-brief to generate a workflow definition for:
"{your natural language description of the procedure}"
at criticality C{N}. Confirm the draft before executing.
```

sop-brief writes the draft to `brief/draft-workflow-definition.md` and waits for your APPROVE before continuing.

#### 2. Fill in Section 1 Metadata

Open the file and replace all `{placeholder}` values in the Section 1 table:

| Field | What to enter |
|-------|--------------|
| `workflow_id` | `{domain}-{action}-{sequence}` — e.g., `adr-authoring-c3-001` |
| `workflow_version` | `1.0.0` for a new procedure |
| `workflow_type` | `NOMINAL` for standard conditions, `ABNORMAL` for off-normal, `EMERGENCY` for emergency response |
| `criticality` | `C1`, `C2`, `C3`, or `C4` |
| `author` | Your name or agent identifier |
| `created_date` | Today's date in `YYYY-MM-DD` format |
| `reviewed_by` | Reviewer name (or `UNREVIEWED` until review completes) |

Verify the step count against the criticality limit before adding steps: C1-C2 allows 20 steps maximum; C3 allows 15; C4 allows 10. If your procedure needs more steps, split it into sub-procedures now.

#### 3. Write Section 2 Purpose and Scope

State the initial system state, the expected end state, and the specific files or systems the procedure acts on. List at minimum one item under "Out of scope" — sop-executor uses this during STAR-STOP to detect scope violations.

#### 4. Write Section 4 Prerequisites

For each prerequisite, supply a verification method that sop-brief can execute automatically. Verification methods that rely on agent judgment ("looks correct") will be flagged by sop-brief as unverifiable.

```
| P-1 | Project directory exists | Glob `projects/{JERRY_PROJECT}/` | REQUIRED |
| P-2 | Workflow definition readable | Read Section 1 metadata successfully | REQUIRED |
```

#### 5. Write Section 8 Performance Steps

Write each step using the annotated format. Pick the classification for each step:

- `[CONTINUOUS]` — for steps that must execute exactly as written (use for all state-modifying steps at C3+)
- `[REFERENCE]` — for steps where judgment is permitted within scope
- `[INFORMATION]` — for context that loads into the brief but does not execute

Every executable step must include: **Action**, **Target**, **Expected Result**, and **Sign-off Criterion**.

```markdown
### Step 1 [CONTINUOUS]: Write the ADR context section

**Action:** Write the Context section to the ADR file using the approved outline.

**Target:** `projects/{JERRY_PROJECT}/decisions/ADR-001-example.md`

**Expected Result:** File exists; Context section contains at minimum 3 sentences.

**Sign-off Criterion:** `Grep "## Context" ADR-001-example.md` returns a match.
```

If you need to protect an irreversible action with a human gate, add `[USER-HOLD]` alongside the classification — see [How to Add Hold Points to a Procedure](#how-to-add-hold-points-to-a-procedure).

#### 6. Write Section 9 Acceptance Criteria

Provide at least one acceptance criterion per major work product. Each criterion must be verifiable without judgment:

```
| AC-1 | ADR file exists | Read target path | File readable with non-zero content |
| AC-2 | Required sections present | Grep for "## Context", "## Decision", "## Consequences" | All three headers found |
```

#### 7. Verify the completed file

Run sop-brief Step 1 validation before any execution attempt:

```
Use /nuclear-sop sop-brief to validate
projects/{JERRY_PROJECT}/workflows/{workflow-id}-workflow-definition.md
```

sop-brief checks prerequisite verifiability, acceptance criteria quality, step count against the criticality limit, and OE history for this workflow type.

### Troubleshooting

**Problem:** sop-brief reports "acceptance criterion not verifiable"
**Solution:** Rewrite the criterion with a specific, observable outcome — replace subjective assessments with file existence checks, Grep patterns, or exit codes.

**Problem:** sop-brief reports step count exceeds criticality limit
**Solution:** Identify natural checkpoint boundaries (typically at QG-HOLD or IV-HOLD steps) and split the procedure into sub-procedures. Each sub-procedure is a separate file. Pass `PROCEDURE_STATE.yaml` from each sub-procedure to the next.

### Related

- **Template:** `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` — Full 11-section structure with all annotation conventions
- **Example:** `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` — Worked C3 workflow with STAR traps
- **Reference:** `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` — NS-M-01 (annotation defaults), NS-M-04 (sub-procedure splitting), NS-M-05 (conservative defaults for generated procedures)

---

## How to Add Hold Points to a Procedure

> Insert USER-HOLD, QG-HOLD, or IV-HOLD annotations into specific steps of an existing workflow definition.

### Before You Begin

You need:
- An existing workflow definition file
- Knowledge of which steps require blocking gates and why

### Steps

#### 1. Identify which hold type each step requires

Use this decision table:

| What you need | Hold type |
|---------------|-----------|
| Human authorization before an irreversible action | `[USER-HOLD]` |
| Quality gate before advancing to the next phase | `[QG-HOLD]` |
| Independent verification of completed work products | `[IV-HOLD]` |

A single step can carry multiple annotations. For example, an irreversible step that also requires IV before execution carries `[USER-HOLD]` and then `[IV-HOLD]` after the action completes.

#### 2. Add USER-HOLD to a step

In Section 8, add `[USER-HOLD]` to the step's annotation line and add a **Hold Reason** field:

```markdown
### Step 5 [USER-HOLD] [CONTINUOUS]: Write final configuration to production path

> **WARNING:** This step writes to the production configuration file. The change
> takes effect immediately on the next agent invocation. No automatic rollback.

**Hold Reason:** Human authorization required before modifying the production
configuration path. Confirm the preceding steps produced the expected draft output
before approving.

**Action:** Write the approved configuration content to `config/production.yaml`.

**Target:** `config/production.yaml`

**Expected Result:** File updated; previous content replaced with approved draft.

**Sign-off Criterion:** `Read config/production.yaml` — content matches approved draft.
```

sop-executor displays the exact USER-HOLD format when it reaches this step and waits for APPROVE, REJECT, or WAIVE.

#### 3. Add QG-HOLD at a phase boundary

Insert a dedicated QG-HOLD step after the last work-product step in a phase. QG-HOLD steps do not carry `[CONTINUOUS]` or `[REFERENCE]` — they carry only `[QG-HOLD]`:

```markdown
### Step 6 [QG-HOLD]: Phase 1 quality gate

**Hold Reason:** Quality gate for work products from Steps 1-5. Score >= 0.92 required per H-13.

**Work Products Under Review:**
- `projects/{JERRY_PROJECT}/decisions/ADR-001-draft.md`

**Acceptance Threshold:** 0.92

**Iteration Ceiling:** C2=5, C3=7 (per RT-M-010)
```

sop-executor invokes `/adversary` S-014 automatically. The gate auto-releases when the score passes. If the score fails, sop-executor returns the critic findings and waits for a revised work product before re-scoring.

If you need a different threshold, declare it in the **Acceptance Threshold** field. Thresholds below 0.92 require documented justification in the workflow definition metadata.

#### 4. Add IV-HOLD before final acceptance

Insert an IV-HOLD step after all work products are produced and before the final sign-off. Specify the exact file paths sop-verifier should evaluate and the acceptance criteria reference:

```markdown
### Step 7 [IV-HOLD]: Independent verification of ADR

**Hold Reason:** Independent verification required before accepting the ADR as final.

**Work Products Under Verification:**
- `projects/{JERRY_PROJECT}/decisions/ADR-001-final.md` — verify all required Nygard sections
  are present and acceptance criteria AC-1 through AC-4 are satisfied

**Verification Criteria Path:** Section 9 of this workflow definition

> **NOTE:** sop-verifier receives only these file paths and the criteria path.
> It does not receive the execution log or STAR records.
```

IV-HOLD is only effective if the workflow runs in 4-hop mode (C3+). For C1-C2 workflows, sop-capture performs integrated IV in Step 0 instead.

### Troubleshooting

**Problem:** sop-executor auto-approves a USER-HOLD without asking
**Solution:** This is a NS-H-02 violation. Report it. sop-executor must never infer APPROVE from context or silence. The hold format requires an explicit APPROVE, REJECT, or WAIVE response.

**Problem:** QG-HOLD never releases despite high scores
**Solution:** Verify the acceptance threshold field in the step matches the intended value. Also verify `/adversary` is returning a composite S-014 score, not a partial score.

**Problem:** IV-HOLD is present in a C1-C2 workflow and the hold is never invoked
**Solution:** IV-HOLD activates sop-verifier in 4-hop mode, which is only required for C3+. For C1-C2, sop-capture's integrated IV step handles verification. Remove the IV-HOLD annotation from C1-C2 workflows, or upgrade the workflow criticality to C3.

### Related

- **Reference:** `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` — Hold Point Authority Table, NS-H-02 (USER-HOLD), NS-H-03 (QG-HOLD), NS-H-04 (IV-HOLD)
- **Template:** `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md` — Hold point sign-off record format

---

## How to Resume a Paused Execution

> Restart a /nuclear-sop execution that was interrupted mid-procedure using the persisted PROCEDURE_STATE.yaml.

### Before You Begin

You need:
- The `PROCEDURE_STATE.yaml` file from the interrupted execution (any non-terminal status)
- The workflow definition file referenced in `workflow_definition_path`
- The execution log from the interrupted session (`execution-log.md` in the same directory)

### Steps

#### 1. Locate the paused state file

Scan your project for non-terminal PROCEDURE_STATE.yaml files:

```
Scan projects/{JERRY_PROJECT}/**/PROCEDURE_STATE.yaml
for non-terminal status values
```

Terminal statuses (`COMPLETED`, `ABORTED`) cannot be resumed — they require a new workflow invocation. Non-terminal statuses eligible for resume: `IN-PROGRESS`, `HELD`, `RESUMING`, `IV-PENDING`, `IV-PASSED`, `IV-REJECTED`.

#### 2. Read the current state before resuming

Open the state file and note the values that determine resume behavior:

| Field | What to check |
|-------|--------------|
| `status` | Current execution status |
| `workflow_id` | Identifies the procedure |
| `current_step` | Last completed step number |
| `next_step` | Step to execute on resume |
| `hold_type` | `USER-HOLD`, `QG-HOLD`, `IV-HOLD`, or `null` |
| `hold_resolution` | Whether the hold was resolved before interruption |
| `state_schema_version` | Must match current skill schema `1.0.0` |

If `state_schema_version` does not match the current schema version, present the mismatch to the user before proceeding — do not silently resume against an incompatible schema.

#### 3. Handle status-specific resume conditions

**If status is `HELD` with `hold_type: USER-HOLD` and `hold_resolution: null`:**
The hold was not resolved before the session ended. Display the USER-HOLD format again and wait for APPROVE, REJECT, or WAIVE before advancing to `next_step`.

**If status is `IV-PENDING`:**
sop-verifier was not yet invoked or did not return a result. Invoke a fresh sop-verifier Task with the `iv_scope` paths and `iv_criteria_path` from the state file. Do not pass the execution log — sop-verifier must receive only the work products and criteria.

**If status is `IN-PROGRESS` or `HELD` with a resolved hold:**
sop-executor can resume directly from `next_step`.

#### 4. Invoke sop-executor in RESUME mode

Pass the state file path and the execution log path explicitly:

```
Use /nuclear-sop sop-executor to resume execution of workflow
{workflow_id} from step {next_step}.

PROCEDURE_STATE.yaml: {path/to/PROCEDURE_STATE.yaml}
Execution log: {path/to/execution-log.md}
Workflow definition: {path from workflow_definition_path field}
```

sop-executor reconstructs its position entirely from the filesystem state — it does not use in-context memory from the prior session.

#### 5. Verify resumed execution continues correctly

After the first step executes on resume, confirm that `PROCEDURE_STATE.yaml` shows:
- `status: IN-PROGRESS`
- `current_step` incremented from the value before resume
- `last_updated` timestamp updated

If you need to abandon the paused workflow instead of resuming, set `status: ABORTED` and invoke sop-capture to write the OE entry with `deviation_type: STOP-WORK`. The OE entry is mandatory even for aborted executions.

### Troubleshooting

**Problem:** sop-executor reports it cannot find the workflow definition
**Solution:** Read `workflow_definition_path` from PROCEDURE_STATE.yaml and verify the file exists at that exact path. If the file was moved, update `workflow_definition_path` in the state file and confirm with the user before resuming.

**Problem:** State file shows `status: COMPLETED` but the expected work products are missing
**Solution:** Check the execution log for the final sign-off record. If sop-capture's OE write was blocked (NS-H-06), the OE entry may be absent even though execution logged COMPLETED. Run sop-capture manually with the existing execution log as input.

**Problem:** Schema version mismatch between state file and current skill version
**Solution:** Present the mismatch to the user per NS-M-07. The user must explicitly confirm that resume is safe before sop-executor proceeds.

### Related

- **Reference:** `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` — PROCEDURE_STATE.yaml State Machine, NS-H-10 (per-step state updates), NS-M-07 (schema version mismatch)
- **Template:** `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` — State schema with field definitions

---

## How to Review OE Entries from Past Executions

> Search and interpret operating experience entries in `docs/experience/` to inform pre-job briefing or post-execution analysis.

### Before You Begin

You need:
- The `workflow_id` or `workflow_type` of the procedure you are researching
- Read access to `docs/experience/`

### Steps

#### 1. Search by workflow_id (primary method)

The most precise search targets prior executions of the same procedure:

```
Glob docs/experience/*.yaml
then filter entries where workflow_id matches "{your-workflow-id}"
```

This returns only entries from previous runs of this exact procedure.

#### 2. Broaden to keyword search if primary returns fewer than 3 results

Extract the `workflow_name` from Section 1 of the workflow definition and search for it:

```
Grep docs/experience/ for "{exact workflow_name value}"
```

If still fewer than 3 results, take the nouns longer than 4 characters from the first sentence of Section 2 Purpose and Grep for each:

```
Grep docs/experience/ for "{noun-1}"
Grep docs/experience/ for "{noun-2}"
```

De-duplicate results by `entry_id` before reading.

#### 3. Filter by workflow_type

After collecting matches, filter by the `workflow_type` field (`NOMINAL`, `ABNORMAL`, or `EMERGENCY`). Do not use `workflow_type` as the primary search key — entries sharing a `workflow_type` value but covering different workflows are not relevant to each other.

#### 4. Read each OE entry for actionable content

For each entry, read these fields:

| Field | What to look for |
|-------|-----------------|
| `deviation_type` | `NONE`, `MINOR`, `MAJOR`, or `STOP-WORK` — entries with `MAJOR` or `STOP-WORK` are highest priority |
| `root_cause` | The identified root cause of the most significant deviation |
| `recommendation` | Specific improvement recommendation — apply these as error traps in the next pre-job brief |
| `error_traps_encountered` | List of error traps that activated during execution — repeat traps indicate a systemic procedure weakness |
| `verification_outcome` | `ACCEPTED`, `REJECTED`, or `ACCEPTED-WITH-CONDITIONS` — rejections indicate work product quality issues |
| `quality_gate_final_score` | The final S-014 score if a QG-HOLD was activated |

#### 5. Apply OE findings to the pre-job brief

If you are preparing to execute the same workflow, copy the `recommendation` and `error_traps_encountered` values from high-priority entries into the pre-job brief's error trap section. sop-brief surfaces these automatically during Step 4 (OE history review) when you invoke sop-brief Step 1.

If you are analyzing OE entries outside of a pre-job brief, document patterns across entries:
- Repeat `root_cause` values across multiple entries signal a procedure design defect
- Repeat `error_traps_encountered` values signal a step that needs a WARNING or CAUTION annotation
- Increasing `quality_gate_final_score` values across entries indicate the procedure is maturing

#### 6. Check OE accumulation thresholds

Count the unsynthesized entries for the relevant `workflow_type`. If the count exceeds 10, run `/problem-solving ps-synthesizer` across the entry set before the next execution to distill patterns into a synthesis entry. If the count exceeds 20, the next sop-brief invocation will block until you provide an explicit override.

### Troubleshooting

**Problem:** Glob returns no results for the workflow_id
**Solution:** The workflow may not have been executed before, or prior executions may have used a different `workflow_id` value. Fall back to the keyword search in Step 2.

**Problem:** An OE entry is missing required fields (blank `root_cause`, missing `recommendation`)
**Solution:** The entry was written in violation of NS-H-06. Flag it as malformed. Do not use its content as reliable guidance — a partial OE entry indicates the capture was interrupted or bypassed.

**Problem:** All entries show `deviation_type: NONE` but the procedure still fails
**Solution:** `deviation_type: NONE` means no deviations were formally logged during execution. Check `error_traps_encountered` — traps that activated but were not logged as deviations indicate a reporting gap. Also check `verification_outcome`: `ACCEPTED-WITH-CONDITIONS` entries may carry conditions that explain recurring issues.

### Related

- **Reference:** `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` — OE Accumulation Enforcement, OE Entry Schema (mandatory fields)
- **How-To:** [How to Write a Workflow Definition](#how-to-write-a-workflow-definition) — for embedding OE-derived WARNING/CAUTION annotations in procedure steps

---

## How to Wrap Another Skill with /nuclear-sop

> Apply nuclear-rigor execution discipline around /problem-solving or /eng-team workflows.

### Before You Begin

You need:
- A defined procedure for the wrapped skill's workflow (or a natural language description to generate one)
- The criticality level for the wrapped work
- `/orchestration` available if the wrapped workflow spans multiple skill invocations

### Steps

#### 1. Decide on the wrapping pattern

| Situation | Pattern |
|-----------|---------|
| The wrapped skill follows a defined procedure with numbered steps | Direct wrap: write a workflow definition whose steps invoke the skill's agents |
| The wrapped skill is a phase in a larger multi-skill pipeline | Orchestration wrap: `/orchestration` sequences /nuclear-sop invocations around skill invocations |

Use the direct wrap when your goal is to add STAR self-checking, hold points, and OE capture to a single skill's execution. Use the orchestration wrap when multiple skills must coordinate across barrier boundaries.

#### 2. Direct wrap: write a workflow definition that calls the skill's agents

Create a workflow definition whose Section 8 steps describe the skill's procedure. Each step that invokes a skill agent becomes a `[CONTINUOUS]` step with an explicit **Action** referencing the agent:

```markdown
### Step 2 [CONTINUOUS]: Run ps-researcher phase

**Action:** Invoke /problem-solving ps-researcher to survey {domain} using the
scope and focus areas defined in Section 2 of this workflow definition.
Output to `projects/{JERRY_PROJECT}/research/phase-1-survey.md`.

**Target:** `projects/{JERRY_PROJECT}/research/phase-1-survey.md`

**Expected Result:** Survey file exists; contains L0, L1, L2 sections.

**Sign-off Criterion:** `Grep "## L0" projects/{JERRY_PROJECT}/research/phase-1-survey.md`
returns a match.
```

Add `[QG-HOLD]` at phase boundaries between skill invocations. Add `[USER-HOLD]` before any irreversible skill action (e.g., writing to a shared registry, pushing an artifact to a canonical location).

#### 3. Orchestration wrap: sequence /nuclear-sop invocations with /orchestration

When the wrapped workflow spans multiple skills with barrier synchronization, use `/orchestration` as the outer coordinator and `/nuclear-sop` for each individual procedure:

```
/orchestration plans multi-procedure workflow
    |
    | Barrier 1
    v
/nuclear-sop executes Procedure A (e.g., /problem-solving ps-researcher phase)
    -> OE entry written to docs/experience/
    -> Output artifacts available at declared paths
    |
    | Barrier 2 (orchestration reads Procedure A artifacts as prerequisites for B)
    v
/nuclear-sop executes Procedure B (e.g., /eng-team eng-architect phase)
    -> OE entry written to docs/experience/
```

Each `/nuclear-sop` invocation runs its own sop-brief, sop-executor, and sop-capture sequence. `/orchestration` handles only inter-procedure sequencing and barrier synchronization.

#### 4. Set QG-HOLD thresholds appropriate to the wrapped skill

Different skills produce different work product types. Set the QG-HOLD threshold to match the criticality and work product type:

| Wrapped skill | Typical QG-HOLD threshold |
|---------------|--------------------------|
| /problem-solving (research) | 0.85-0.90 for exploratory phases; 0.92 for final deliverables |
| /problem-solving (ADR) | 0.92 (H-13 minimum for C2+) |
| /eng-team (security review) | 0.92-0.95 depending on exposure level |
| /adversary | 0.92 (H-13 minimum for C2+) |

Thresholds below 0.92 for C2+ workflows require documented justification in the workflow definition metadata.

#### 5. Configure IV-HOLD for C3+ wrapped workflows

If the wrapped workflow is C3+, add an IV-HOLD step after each skill's primary work product is produced. The `iv_scope` should list the skill's output artifacts. The `iv_criteria_path` should point to the Section 9 acceptance criteria in the workflow definition:

```markdown
### Step 6 [IV-HOLD]: Independent verification of ps-architect output

**Work Products Under Verification:**
- `projects/{JERRY_PROJECT}/decisions/ADR-001-final.md`
  — verify Nygard sections, decision stated, consequences documented

**Verification Criteria Path:** Section 9 of this workflow definition
```

sop-verifier evaluates the artifacts against the acceptance criteria in fresh context — it does not see the execution log or the wrapped skill's reasoning chain.

#### 6. Run the full sequence

Invoke sop-brief to validate and brief, then sop-executor to execute, then sop-verifier (C3+ only), then sop-capture:

```
Use /nuclear-sop to execute
projects/{JERRY_PROJECT}/workflows/{wrapped-skill}-workflow-definition.md
at criticality C{N}.
Run the full {3-hop|4-hop} sequence.
```

The OE entry produced by sop-capture feeds future pre-job briefs for the same wrapped-skill procedure, building institutional knowledge about how that skill's workflow behaves under nuclear rigor.

### Troubleshooting

**Problem:** The wrapped skill agent is invoked but STAR is not applied because the invocation is a Read, not a Write
**Solution:** STAR applies only to Write, Edit, and Bash calls. The skill agent invocation itself is coordinated by the main context. STAR applies to the tool calls within sop-executor's execution steps, not to the skill's internal tool calls. Design the workflow definition steps so that sop-executor issues the state-modifying calls, not the wrapped skill's agent directly, if you need STAR coverage.

**Problem:** /orchestration and /nuclear-sop overlap in responsibility for coordination
**Solution:** `/orchestration` owns cross-procedure sequencing and barrier synchronization. `/nuclear-sop` owns single-procedure execution with STAR, hold points, and OE capture. When in doubt: if the work has numbered steps and needs OE capture, use /nuclear-sop. If the work coordinates multiple procedures without a defined step sequence, use /orchestration.

**Problem:** The wrapped workflow exceeds the step limit for its criticality
**Solution:** Split at the natural barrier between skill phases. Each skill agent invocation is typically one logical sub-procedure. Define separate workflow definition files for each phase and coordinate them with /orchestration.

### Related

- **Playbook:** `skills/nuclear-sop/PLAYBOOK.md` — Integration with Other Skills section (QG-HOLD -> /adversary, OE synthesis -> /problem-solving, multi-procedure coordination -> /orchestration)
- **How-To:** [How to Write a Workflow Definition](#how-to-write-a-workflow-definition) — foundation for the direct wrap pattern
- **How-To:** [How to Add Hold Points to a Procedure](#how-to-add-hold-points-to-a-procedure) — for configuring the QG-HOLD and IV-HOLD gates in the wrapped workflow

---

*Guides version: 1.0.0 | Skill: /nuclear-sop v1.1.0 | Quadrant: How-To*
