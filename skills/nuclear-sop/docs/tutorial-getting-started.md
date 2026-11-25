# Learn /nuclear-sop by Running Your First Procedure

> **Tutorial** -- You will execute a complete C1 workflow from scratch: write the procedure,
> run the pre-job brief, execute the steps with STAR self-checking, and capture an OE entry.
> By the end you will have four output files and a working understanding of the full
> nuclear-sop sequence.
>
> **`[UNTESTED]`** -- Agent behaviors described in Steps 2-4 are derived from the
> `skills/nuclear-sop/SKILL.md` specification and agent definitions. They have not been
> author-verified by running the agents in a live session against this exact workflow definition.
> If an agent step produces output that differs from the "Visible result" description, check
> the agent's `.md` definition for current behavior.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [What you will achieve](#what-you-will-achieve) | End state and output files |
| [Prerequisites](#prerequisites) | What you need before starting |
| [Step 1: Create a C1 workflow definition](#step-1-create-a-c1-workflow-definition) | Write the procedure file from the template |
| [Step 2: Run sop-brief](#step-2-run-sop-brief) | Pre-job briefing -- load context and check prerequisites |
| [Step 3: Run sop-executor](#step-3-run-sop-executor) | Execute the steps with STAR self-checking |
| [Step 4: Run sop-capture](#step-4-run-sop-capture) | Capture operating experience |
| [Step 5: Verify the results](#step-5-verify-the-results) | Check PROCEDURE_STATE.yaml and the OE entry |
| [What to try next](#what-to-try-next) | C2 with hold points, C3 with sop-verifier |

---

## What you will achieve

By the end of this tutorial you will have run a complete /nuclear-sop sequence on a minimal
C1 workflow. Your project directory will contain:

- `work/dec-log-001/brief/pre-job-brief.md` -- the pre-job briefing report from sop-brief
- `work/dec-log-001/PROCEDURE_STATE.yaml` -- the place-keeping state file showing `COMPLETED`
- `work/dec-log-001/execution-log.md` -- the step-by-step STAR execution log
- `docs/experience/oe-dec-log-001.yaml` -- the operating experience entry

The workflow you will execute is "Record a project decision" -- a two-step C1 procedure that
creates a decision log file and records one decision in it.

---

## Prerequisites

Before starting, confirm the following are true:

- You have an active Jerry project (`JERRY_PROJECT` is set). Run `jerry projects list` if unsure.
- Your project directory follows the standard Jerry layout with a `work/` subdirectory.
- You can create files and subdirectories in your project's `work/` folder.
- You have read the `/nuclear-sop` SKILL.md Quick Reference section. You do not need to
  have used the skill before -- that is what this tutorial is for.

---

## Step 1: Create a C1 workflow definition

You will create a workflow definition file from the template. This file is the procedure
that sop-brief and sop-executor will read.

**1a.** Create the directory `work/dec-log-001/` in your project.

**1b.** Create the file `work/dec-log-001/workflow-definition.md` with this exact content:

```markdown
# Workflow Definition: Record a Project Decision

---

## Section 1: Metadata

| Field | Value |
|-------|-------|
| `workflow_id` | `dec-log-001` |
| `workflow_version` | `1.0.0` |
| `workflow_type` | `NOMINAL` |
| `criticality` | `C1` |
| `author` | `tutorial-user` |
| `created_date` | `2026-04-20` |
| `last_revised` | `2026-04-20` |
| `reviewed_by` | `tutorial-user` |
| `review_date` | `2026-04-20` |
| `applicable_skill` | `/nuclear-sop` |

---

## Section 2: Purpose and Scope

### Purpose

Create `work/dec-log-001/decisions.md` and record one decision entry in it.
This procedure transitions the project from "no decision log exists" to
"decision log created with one entry."

### Scope

**In scope:**
- Creating `work/dec-log-001/decisions.md`
- Writing one decision entry to that file

**Out of scope:**
- Any file outside `work/dec-log-001/`

**Applicability conditions:**
- Use when `work/dec-log-001/decisions.md` does not yet exist.

---

## Section 3: References

| Document | Path or Location | Relevance |
|----------|-----------------|-----------|
| Nuclear-SOP skill | `skills/nuclear-sop/SKILL.md` | Skill this procedure uses |

---

## Section 4: Prerequisites

| # | Prerequisite | Verification Method | Required State |
|---|-------------|--------------------|--------------:|
| P-1 | `work/dec-log-001/` directory exists | `Glob work/dec-log-001/` returns a result | REQUIRED |

---

## Section 5: Initial Conditions

| System / Artifact | Expected Initial State |
|-------------------|------------------------|
| `work/dec-log-001/decisions.md` | Does not exist |

---

## Section 6: Limitations and Precautions

**Limitations:**
- This is a tutorial procedure. It creates a simple decisions file.

**Precautions:**
- Step 2 writes to `work/dec-log-001/decisions.md`. Confirm the file does not
  already exist before executing.

**Recovery:**
- If the procedure fails, delete `work/dec-log-001/decisions.md` and restart from Step 1.

---

## Section 8: Performance Steps

### Step 1 [CONTINUOUS]: Create the decision log file

**Action:** Create the file `work/dec-log-001/decisions.md` with the heading
`# Project Decisions` as the only content.

**Target:** `work/dec-log-001/decisions.md`

**Expected Result:** File `work/dec-log-001/decisions.md` exists and contains
the single line `# Project Decisions`.

**Sign-off Criterion:** File exists and Read returns `# Project Decisions` as
the first line.

---

### Step 2 [CONTINUOUS]: Record the first decision entry

**Action:** Append the following block to `work/dec-log-001/decisions.md`:

```
## DEC-001: Use /nuclear-sop for C2+ workflows

**Date:** 2026-04-20
**Status:** ACCEPTED
**Rationale:** Provides mandatory pre/post-execution phases, STAR self-checking,
and OE capture that standard workflows lack.
```

**Target:** `work/dec-log-001/decisions.md`

**Expected Result:** File contains both the heading and the DEC-001 block.

**Sign-off Criterion:** Read returns both the `# Project Decisions` heading and
the `## DEC-001` section.

---

## Section 9: Acceptance Criteria

| # | Criterion | Verification Method | PASS Condition |
|---|-----------|--------------------|--------------:|
| AC-1 | Decision log file exists | `Glob work/dec-log-001/decisions.md` | File found |
| AC-2 | DEC-001 entry is present | Read file, check for `## DEC-001` heading | Heading present |

---

## Section 10: Sign-off and Verification Record

> Runtime-written by sop-executor.

---

## Section 11: Attachments

> Runtime-written by sop-capture.
```

**Visible result:** The file `work/dec-log-001/workflow-definition.md` now exists.
You can read it back to confirm the structure matches what you typed.

---

## Step 2: Run sop-brief

Now you will invoke the pre-job briefing agent. sop-brief reads your workflow definition,
verifies prerequisites, and writes a briefing report before any execution begins.

Send this prompt to Claude:

```
Use /nuclear-sop sop-brief to run the pre-job briefing for
work/dec-log-001/workflow-definition.md

Write the briefing report to work/dec-log-001/brief/pre-job-brief.md
```

sop-brief will do the following in order:

1. Read your workflow definition
2. Verify that `work/dec-log-001/` exists (prerequisite P-1)
3. Check that `work/dec-log-001/decisions.md` does not yet exist (initial conditions)
4. Confirm that acceptance criteria AC-1 and AC-2 are verifiable
5. Search `docs/experience/` for any prior OE entries related to this workflow type
6. Identify the error trap in this procedure (Step 2 appends to a file -- if Step 1
   did not create it first, Step 2 will fail)
7. Write `work/dec-log-001/brief/pre-job-brief.md`

**Visible result:** `work/dec-log-001/brief/pre-job-brief.md` exists and contains
sections for prerequisites checked, initial conditions, OE history, and identified
error traps. Read that file to confirm all three prerequisites show `SATISFIED`.

If sop-brief reports a failed prerequisite, it will stop and ask you to resolve it
before proceeding. In this tutorial, the only prerequisite is that the `work/dec-log-001/`
directory exists -- which it does because you created it in Step 1.

---

## Step 3: Run sop-executor

With the brief complete, you will now execute the two steps of the procedure.
sop-executor applies STAR self-checking before every Write, Edit, or Bash tool call.

Send this prompt to Claude:

```
Use /nuclear-sop sop-executor to execute
work/dec-log-001/workflow-definition.md

Write all state to work/dec-log-001/
```

sop-executor will execute Step 1 and Step 2 in sequence. For each step it applies
the STAR protocol before writing:

- **Stop:** Pause before acting. Verify this is the correct step to execute now.
- **Think:** Confirm the action, target, and expected result match the workflow definition.
- **Act:** Execute the tool call (Write or Edit).
- **Review:** Verify the expected result was produced.

After Step 1 completes, sop-executor writes `work/dec-log-001/PROCEDURE_STATE.yaml`
with `current_step: 1` and `next_step: 2`. You can read that file between steps
to see place-keeping in action.

After Step 2 completes, sop-executor updates `PROCEDURE_STATE.yaml` to `status: COMPLETED`
and writes the final `work/dec-log-001/execution-log.md`.

**Visible result after Step 1:** `work/dec-log-001/decisions.md` exists and contains
`# Project Decisions`.

**Visible result after Step 2:** `work/dec-log-001/decisions.md` contains both the
heading and the DEC-001 block.

**Visible result after both steps:** `work/dec-log-001/PROCEDURE_STATE.yaml` shows
`status: COMPLETED` and `steps_completed` has two entries.

If sop-executor's STAR-Think phase detects a mismatch between the workflow definition
and what it is about to do, it will stop and report the mismatch before making any
tool call. This is the error-trap detection mechanism.

---

## Step 4: Run sop-capture

The final mandatory step is operating experience capture. sop-capture reads the
execution log and writes a schema-validated OE entry to `docs/experience/`.

Send this prompt to Claude:

```
Use /nuclear-sop sop-capture to write the OE entry for workflow dec-log-001

Execution log: work/dec-log-001/execution-log.md
PROCEDURE_STATE: work/dec-log-001/PROCEDURE_STATE.yaml
OE output: docs/experience/oe-dec-log-001.yaml
```

sop-capture will:

1. Read the final execution log
2. Compare actual execution against the workflow plan
3. Record any deviations (there should be none for a clean first run)
4. Write the OE entry to `docs/experience/oe-dec-log-001.yaml`
5. Update Section 11 of your workflow definition with the OE entry reference

**Visible result:** `docs/experience/oe-dec-log-001.yaml` exists and contains the
required schema fields: `workflow_id`, `workflow_type`, `deviation_type` (NONE for
a clean run), `root_cause`, `recommendation`, and `criticality`.

If sop-capture cannot write all required fields, it will stop and report which fields
are missing. It does not write a partial OE entry.

---

## Step 5: Verify the results

Check each of the four output files that a complete nuclear-sop run produces.

**5a. Check PROCEDURE_STATE.yaml shows COMPLETED.**

Read `work/dec-log-001/PROCEDURE_STATE.yaml`. Confirm:
- `status` is `COMPLETED`
- `steps_completed` has exactly two entries (Step 1 and Step 2)
- `stop_work_count` is `0`
- `hold_type` is `null` (no hold points were activated -- this C1 workflow had none)

**5b. Check the execution log records both STAR applications.**

Read `work/dec-log-001/execution-log.md`. Confirm it contains a STAR record for
each step: Stop/Think/Act/Review entries for Step 1 and Step 2.

**5c. Check the decision log was created correctly.**

Read `work/dec-log-001/decisions.md`. Confirm it contains:
- Line 1: `# Project Decisions`
- A `## DEC-001` section with Date, Status, and Rationale fields

**5d. Check the OE entry has all required fields.**

Read `docs/experience/oe-dec-log-001.yaml`. Confirm it contains:
- `workflow_id: dec-log-001`
- `criticality: C1`
- `deviation_type: NONE`
- A `recommendation` field (even clean runs should have a recommendation,
  such as confirming the procedure worked as expected)

If all four checks pass, you have successfully completed a full /nuclear-sop execution.

---

## What to try next

**C2 with a USER-HOLD.**
Add a `[USER-HOLD]` annotation to one step in your next workflow definition. When
sop-executor reaches that step, it will pause and present an APPROVE/REJECT/WAIVE
question before executing. Try this for any step that writes to a shared or permanent
location.

**C2 with a QG-HOLD.**
Add a `[QG-HOLD]` step after your main work steps. sop-executor will invoke ps-critic
with the S-014 rubric and require a score of >= 0.92 before proceeding. If the score
is below threshold, the executor loops on revision up to 5 times (the C2 iteration ceiling).

**C3 with sop-verifier.**
The C3 ADR authoring example at `skills/nuclear-sop/examples/c3-adr-workflow-definition.md`
shows all three hold types in a 15-step procedure. C3 workflows use 4-hop mode:
sop-verifier runs in fresh context (no exposure to the executor's reasoning chain)
before sop-capture writes the OE entry. The worked example also contains three deliberate
STAR error traps -- try running it and observing how sop-executor's STAR-Think phase
catches each trap before any tool call executes.

---

*Tutorial version: 1.0.0 | Quadrant: Tutorial | Skill: /nuclear-sop v1.1.0*
