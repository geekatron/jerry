---
name: nuclear-sop-playbook
description: Step-by-step routing and usage guide for the /nuclear-sop skill. Covers agent
  selection, workflow sequences (3-hop and 4-hop), hold point and procedure classification
  references, integration with other Jerry skills, and common workflow patterns with examples.
version: "1.0.0"
skill: nuclear-sop
constitutional_compliance: Jerry Constitution v1.0
agents_covered:
  - sop-brief
  - sop-executor
  - sop-verifier
  - sop-capture
---

# Nuclear SOP Playbook

> **Version:** 1.0.0
> **Skill:** /nuclear-sop
> **Purpose:** Nuclear-inspired procedural execution with mandatory pre/post-execution phases, STAR self-checking, hold points, and OE capture
> **Updated:** 2026-04-16

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: The Big Picture](#l0-the-big-picture) | What /nuclear-sop does and when to use it |
| [L1: Agent Reference](#l1-agent-reference) | Agent roles, tool tiers, invocation patterns |
| [L2: Architecture and Standards](#l2-architecture-and-standards) | Circuit breaker compliance, security considerations, governance |
| [Workflow Sequences](#workflow-sequences) | 3-hop and 4-hop execution diagrams |
| [Agent Selection Guide](#agent-selection-guide) | Decision table for choosing the right agent |
| [Hold Point Reference](#hold-point-reference) | Three hold types with release conditions |
| [Procedure Classification Reference](#procedure-classification-reference) | CONTINUOUS, REFERENCE, INFORMATION |
| [PROCEDURE_STATE.yaml State Machine](#procedure_stateyaml-state-machine) | Valid statuses, transitions, and terminal states |
| [Step Limits by Criticality](#step-limits-by-criticality) | Maximum steps per sop-executor invocation |
| [OE Accumulation Thresholds](#oe-accumulation-thresholds) | WARNING and STOP thresholds for unsynthesized OE entries |
| [Integration with Other Skills](#integration-with-other-skills) | When /nuclear-sop hands off to /problem-solving, /adversary, /orchestration |
| [Common Workflows](#common-workflows) | Real invocation examples with expected artifacts |
| [Quick Reference Table](#quick-reference-table) | Fast lookup for step sequences and key rules |

---

# L0: The Big Picture

> *What /nuclear-sop does and why it matters, in plain language.*

## The Nuclear Crew Metaphor

```
+===================================================================+
|                     THE NUCLEAR CREW                               |
+===================================================================+
|                                                                   |
|   Think of /nuclear-sop like a nuclear plant procedure crew:      |
|                                                                   |
|   +------------------+                                            |
|   | PROCEDURE REQUEST |    "We need to execute this procedure"    |
|   +-------+----------+                                            |
|           |                                                        |
|           v                                                        |
|   +---------------+    Step 0 (optional): generate the procedure  |
|   |   sop-brief   |    Step 1 (mandatory): brief before you touch |
|   | (shift leader)|    anything -- load context, check prereqs,   |
|   +-------+-------+    surface prior incidents, identify traps    |
|           |                                                        |
|           v                                                        |
|   +--------------+     Step 2: execute step by step, STAR check   |
|   | sop-executor |     before every write, hold points block       |
|   | (technician) |     progress until authorized to proceed        |
|   +-------+------+                                                 |
|           |                                                        |
|           +---> C3+ only --> [sop-verifier: fresh-eyes reviewer]  |
|           |                                                        |
|           v                                                        |
|   +--------------+     Step 4: document what happened, every time |
|   | sop-capture  |     OE entry feeds future pre-job briefs       |
|   | (logkeeper)  |                                                 |
|   +--------------+                                                 |
|                                                                   |
|   The crew runs the same ritual every time:                       |
|   Brief -> Execute -> Verify (C3+) -> Capture                     |
|                                                                   |
+===================================================================+
```

## Why Does This Matter?

| Without /nuclear-sop | With /nuclear-sop |
|---------------------|-------------------|
| Context loaded mid-execution or not at all | Mandatory pre-job brief before first tool call |
| Errors discovered after irreversible actions | STAR self-check before every Write/Edit/Bash |
| No record of what was done or what deviated | Mandatory OE entry written to docs/experience/ |
| No way to pause and resume across sessions | PROCEDURE_STATE.yaml enables cross-session resume |
| Verification biased by executor's own reasoning | Context-isolated sop-verifier for C3+ workflows |

## When to Use /nuclear-sop

Use when ALL of these apply:
- Workflow has a defined procedure with numbered steps to execute in sequence
- Step-level place-keeping and sign-off are required (audit trail, pause/resume across sessions)
- Post-job operating experience capture is a required output (not optional)
- Criticality is C2+ and procedural rigor must be documented

**Do NOT use** when:
- Task is C1 routine work without a defined procedure (overhead disproportionate)
- Task is pure research or exploratory analysis (use `/problem-solving` instead)
- Task is multi-phase pipeline coordination without enumerated steps (use `/orchestration`)
- Task requires coordination of multiple Jerry skills (use `/orchestration`)
- No workflow definition exists AND user declines Step 0 generation

---

# L1: Agent Reference

> *Who does what, when to invoke them, and what they produce.*

## The Four-Agent Crew

| Agent | Role | Nuclear Patterns | Tool Tier | Model | Cognitive Mode |
|-------|------|-----------------|-----------|-------|----------------|
| `sop-brief` | Pre-job briefing: context load, prerequisite check, OE history review, error trap identification. Optionally generates workflow definition from natural language (Step 0). | F-2a, D-1, H-2, A-3 sections 1-6 | T2 | sonnet | systematic |
| `sop-executor` | Step-by-step execution: STAR self-checking before each tool call, place-keeping, hold point activation, persistent PROCEDURE_STATE.yaml | B-1, A-5, A-2, A-4, D-2, C-3, E-2 | T2 | opus | systematic |
| `sop-verifier` | Context-isolated verification: evaluates work products against acceptance criteria with fresh context (no executor reasoning). C3+ only (4-hop mode). | C-2 (approximated), C-3 | T1 (read-only) | sonnet | convergent |
| `sop-capture` | Post-job OE capture: deviation classification, schema-validated OE entry, integrated IV for C1-C2. Mandatory final step. | F-2b, H-1, H-2 infrastructure | T2 | sonnet | systematic |

**Agent definition paths:**
- `skills/nuclear-sop/agents/sop-brief.md` and `skills/nuclear-sop/agents/sop-brief.governance.yaml`
- `skills/nuclear-sop/agents/sop-executor.md` and `skills/nuclear-sop/agents/sop-executor.governance.yaml`
- `skills/nuclear-sop/agents/sop-verifier.md` and `skills/nuclear-sop/agents/sop-verifier.governance.yaml`
- `skills/nuclear-sop/agents/sop-capture.md` and `skills/nuclear-sop/agents/sop-capture.governance.yaml`

**Composition files (derived artifacts):**
- `skills/nuclear-sop/composition/sop-brief.agent.yaml` and `sop-brief.prompt.md`
- `skills/nuclear-sop/composition/sop-executor.agent.yaml` and `sop-executor.prompt.md`
- `skills/nuclear-sop/composition/sop-verifier.agent.yaml` and `sop-verifier.prompt.md`
- `skills/nuclear-sop/composition/sop-capture.agent.yaml` and `sop-capture.prompt.md`

> **Normative source note:** The agent definition files above (`agents/{name}.md` + `agents/{name}.governance.yaml`) are the normative source — they are what `plugin.json` and Claude Code load. The `composition/` files are derived artifacts; on conflict, the `agents/` pair wins.

---

## Invocation Patterns

Three patterns for invoking agents (choose based on your context):

**Pattern 1: Natural language (recommended)**

```
"Run a pre-job brief for this workflow definition"         -> sop-brief
"Execute this procedure with STAR self-checking"           -> sop-executor
"Verify the work products from this execution"             -> sop-verifier
"Capture operating experience from this execution"         -> sop-capture
"Use /nuclear-sop for this C2 procedure"                   -> sop-brief, then full sequence
```

**Pattern 2: Explicit agent name**

```
Use /nuclear-sop sop-brief to brief workflow-definition.md
Use /nuclear-sop sop-executor to execute the briefed procedure
```

**Pattern 3: Full workflow sequence (main context orchestrates)**

```
1. Invoke sop-brief -> brief/pre-job-brief.md (mandatory)
2. Invoke sop-executor -> work products + execution-log.md (mandatory)
3. C3+ only: invoke sop-verifier via Task tool -> IV report (fresh context)
4. Invoke sop-capture -> OE entry in docs/experience/ (mandatory)
```

---

# Workflow Sequences

## 3-Hop Mode (C1-C2, Unambiguously H-36 Compliant)

```
MAIN CONTEXT (orchestrator)
       |
       | Hop 1
       v
+-------------+
| sop-brief   |  Step 0 (optional): generate workflow definition from natural language
| [MANDATORY] |  Step 1: validate workflow definition, check prerequisites
|             |  Step 2: verify prerequisites (PASS/FAIL/WAIVED)
|             |  Step 3: acceptance criteria quality check
|             |  Step 4: OE history review
|             |  Step 5: error trap identification
|             |  Step 6: generate pre-job-brief.md
+------+------+
       |
       | Output: brief/pre-job-brief.md
       | Handoff: workflow definition path + criticality
       |
       | Hop 2
       v
+---------------+
| sop-executor  |  Phase 0: initialization (load brief, load workflow def)
| [MANDATORY]   |  Phase 1: per-step loop with STAR before every Write/Edit/Bash
|               |  Hold points block progress at USER-HOLD / QG-HOLD / IV-HOLD
|               |  Stop-work on any deviation; user decides CONTINUE/REVISE/ABORT
|               |  Phase 2: mark execution COMPLETED; write final execution log
+-------+-------+
        |
        | Output: PROCEDURE_STATE.yaml, execution-log.md, work product artifacts
        |
        | Hop 3
        v
+-------------+
| sop-capture |  Step 0: integrated IV (C1-C2 only, with anchoring bias disclaimer)
| [MANDATORY] |  Step 1: execution analysis vs. planned procedure
|             |  Step 2: deviation classification (NONE/MINOR/MAJOR/STOP-WORK)
|             |  Step 3: OE entry production (write-blocked if any required field missing)
|             |  Step 4: post-job brief + mark PROCEDURE_STATE.yaml COMPLETED
+-------------+
        |
        v
  OE ENTRY: docs/experience/{entry_id}.yaml (dual-write: also capture/oe-entry-*.yaml)
  POST-JOB BRIEF: capture/post-job-brief.md
```

## 4-Hop Mode (C3+, Required)

```
MAIN CONTEXT (orchestrator)
       |
       | Hop 1
       v
+-------------+       (same as 3-hop: Steps 0-6)
| sop-brief   |
| [MANDATORY] |
+------+------+
       |
       | Hop 2
       v
+-----------------+    (same as 3-hop: Phases 0-2)
| sop-executor    |    At IV-HOLD: sets PROCEDURE_STATE.yaml status = IV-PENDING
| [MANDATORY]     |    Returns to main context for verifier invocation
+-------+---------+
        |
        | PROCEDURE_STATE.yaml status: IV-PENDING
        |
        | Hop 3 (governance ambiguity -- ruling pending; 60-day deadline)
        v
+-------------------+
| sop-verifier      |  Invoked via Task tool (fresh context -- no executor reasoning)
| [C3+ REQUIRED]    |  Task prompt contains ONLY: workflow definition path,
|                   |    iv_scope paths from PROCEDURE_STATE.yaml,
|                   |    acceptance criteria reference
|                   |  SR-09: resolves expected paths from workflow definition
|                   |    independently of executor-reported paths
|                   |  Returns: ACCEPT / REJECT / ACCEPT-WITH-CONDITIONS
+-------+-----------+
        |
        | IV report returned as Task response content
        | Main context persists IV report; updates PROCEDURE_STATE.yaml
        |
        | Hop 4
        v
+-------------+
| sop-capture |  Step 0 SKIPPED (C3+ reads sop-verifier IV report instead)
| [MANDATORY] |  Steps 1-4: same as 3-hop
+-------------+
```

**Governance deadline note:** If no H-36 ruling within 60 days of Phase 1 delivery, 3-hop mode becomes permanent for all criticality levels. sop-verifier is eliminated; sop-capture integrated IV becomes the universal verification mechanism. NS-H-08 must be revised at that point. See `skills/nuclear-sop/SKILL.md` section: H-36 Circuit Breaker Compliance.

---

# Agent Selection Guide

## Decision Table

| What Do You Need? | Agent | Example Invocation |
|-------------------|-------|-------------------|
| Run full nuclear-rigor workflow from a natural language description | sop-brief (Step 0 then 1), then full sequence | "Use nuclear-sop to generate and execute a procedure for ADR authoring at C3" |
| Execute an existing workflow definition (with brief) | sop-brief then sop-executor | "Run pre-job brief for examples/c3-adr-workflow-definition.md then execute" |
| Resume a paused workflow from PROCEDURE_STATE.yaml | sop-executor (RESUME mode) | "Resume execution of workflow WF-ADR-001 using PROCEDURE_STATE.yaml in proj-0039" |
| Verify completed work products (C3+) | sop-verifier (invoked via Task) | "Use sop-verifier to evaluate work products against acceptance criteria in PROCEDURE_STATE.yaml" |
| Capture post-job OE for a completed execution | sop-capture | "Use sop-capture to write the OE entry for workflow run WF-ADR-001" |
| Check active paused workflows | main context scan | "Scan for any PROCEDURE_STATE.yaml files with non-terminal status in PROJ-0039" |

## /nuclear-sop vs. Other Skills

| Request Type | Use This Skill | Use Instead | Reason |
|--------------|---------------|-------------|--------|
| Execute a defined step-by-step procedure with sign-off | `/nuclear-sop` | -- | Core use case |
| Multi-phase research/analysis pipeline without defined steps | -- | `/orchestration` | No procedure to execute |
| Iterative improvement with creator-critic-revision loops | -- | `/problem-solving` | H-14 quality cycles are a /problem-solving pattern |
| Standalone adversarial quality review of a completed deliverable | -- | `/adversary` | /adversary applies S-001 through S-014 strategy templates |
| Threat model, security architecture, SAST review | -- | `/eng-team` | Domain-specific secure engineering methodology |
| Independent verification (IV) within a nuclear-sop execution | `sop-verifier` | -- | sop-verifier IS the IV mechanism; invoke for C3+ 4-hop sequence |

### /nuclear-sop vs. /orchestration Decision Table

| Condition | Use /nuclear-sop | Use /orchestration |
|-----------|------------------|--------------------|
| Task has a defined procedure with numbered steps | Yes | No |
| Task requires step-level place-keeping and sign-off | Yes | No |
| Task requires independent verification of work products | Yes (sop-verifier) | Partial (no context isolation guarantee) |
| Task requires post-job OE capture as a required artifact | Yes (sop-capture) | No |
| Task is multi-phase research/analysis pipeline | No | Yes |
| Task requires coordination of multiple skills | No | Yes |
| Task is C1 routine work | No -- overhead disproportionate | Optional |
| No defined procedure exists yet | Use sop-brief Step 0 to generate one | Yes, if ad-hoc coordination only |

---

# Hold Point Reference

Three blocking gate types provide authorization control at different authority levels.

| Type | Annotation | Release Condition | PROCEDURE_STATE Status | Nuclear Pattern |
|------|-----------|-------------------|------------------------|----------------|
| `USER-HOLD` | `[USER-HOLD]` | User responds APPROVE, REJECT, or WAIVE via AskUserQuestion | `status: HELD, hold_type: USER-HOLD` | P-020 -- user authority |
| `QG-HOLD` | `[QG-HOLD]` | Quality score >= 0.92 from ps-critic via /adversary S-014 (H-13). Auto-releases on PASS; escalates to user on ceiling reached. | `status: HELD, hold_type: QG-HOLD, qg_iteration tracked` | /adversary S-014 |
| `IV-HOLD` | `[IV-HOLD]` | sop-verifier produces ACCEPT disposition (fresh Task context, no executor reasoning) | `status: IV-PENDING, iv_scope: [file paths]` | C-2 (approximated), C-3 |

## USER-HOLD Display Format (exact)

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
========================
```

## IV-HOLD Rejection Protocol

After sop-verifier returns REJECT:
1. Main context passes verifier findings back to sop-executor for revision
2. sop-executor revises; updates `PROCEDURE_STATE.yaml iv_iteration`
3. Main context invokes a new sop-verifier Task (fresh context, no prior reasoning)
4. After 3 rejections: mandatory user escalation per NS-M-02

## QG-HOLD Iteration Ceilings (NS-M-03)

| Criticality | Maximum QG-HOLD Iterations |
|-------------|---------------------------|
| C1 | 3 |
| C2 | 5 |
| C3 | 7 |
| C4 | 10 |

Score plateau (delta < 0.01 for 3 consecutive iterations) triggers early halt with user escalation regardless of remaining ceiling.

---

# Procedure Classification Reference

Steps in workflow definitions are annotated with use classification. sop-executor behavior differs by classification.

| Classification | Annotation | sop-executor Behavior | Nuclear Analog | Default (unannotated) |
|---------------|------------|----------------------|----------------|----------------------|
| Continuous | `[CONTINUOUS]` | Execute exactly as written; no deviation; full STAR; step sign-off required | EOPs, STPs -- "read and follow each step in sequence" | C3+ workflows |
| Reference | `[REFERENCE]` | Consult for guidance; agent may exercise judgment within step scope | AOPs, ARPs -- "consult as needed" | C1-C2 workflows |
| Information | `[INFORMATION]` | Background context loaded; not executed; no PROCEDURE_STATE.yaml update | Reference materials -- "available for consultation" | Any criticality; context only |

**Default Assignment (NS-M-01):**
- C3+ workflows: unannotated steps default to `[CONTINUOUS]`
- C1-C2 workflows: unannotated steps default to `[REFERENCE]`
- The workflow definition metadata section SHOULD declare which default applies

---

# PROCEDURE_STATE.yaml State Machine

| Status | Meaning | Valid Next States |
|--------|---------|-------------------|
| `INITIALIZING` | sop-brief has written initial state; sop-executor not started | `IN-PROGRESS` |
| `IN-PROGRESS` | sop-executor actively executing steps | `HELD`, `IV-PENDING`, `COMPLETED`, `ABORTED` |
| `HELD` | Blocked at USER-HOLD or QG-HOLD | `IN-PROGRESS` (on APPROVE or QG PASS), `ABORTED` (on REJECT) |
| `RESUMING` | Session restart; sop-executor reconstructing position from state file | `IN-PROGRESS` |
| `IV-PENDING` | Waiting for sop-verifier Task invocation and result | `IV-PASSED`, `IV-REJECTED` |
| `IV-PASSED` | sop-verifier returned ACCEPT | `COMPLETED` (no further steps), `IN-PROGRESS` (revision steps remain) |
| `IV-REJECTED` | sop-verifier returned REJECT | `IN-PROGRESS` (revision), `ABORTED` (after 3 rejections + user decision) |
| `COMPLETED` | All steps executed; OE entry written | Terminal |
| `ABORTED` | Execution halted; OE entry written with STOP-WORK deviation_type | Terminal |

**Invalid Transitions (HARD):**
- `COMPLETED` -> any other state
- `ABORTED` -> any other state
- `IN-PROGRESS` -> `COMPLETED` without sop-capture OE entry

---

# Step Limits by Criticality

| Criticality | Maximum Steps per sop-executor Invocation |
|-------------|------------------------------------------|
| C1-C2 | 20 steps |
| C3 | 15 steps |
| C4 | 10 steps |

When a workflow exceeds the criticality-appropriate limit:
1. sop-brief Step 1 detects the overage and proposes sub-procedure splitting (NS-M-04)
2. If the user approves, the workflow is divided at natural checkpoints
3. Each sub-procedure is a separate sop-executor invocation with the current PROCEDURE_STATE.yaml
4. Sub-procedure boundaries within a single skill invocation are NOT additional hops per H-36

---

# OE Accumulation Thresholds

sop-brief enforces thresholds on unsynthesized OE entries per `workflow_type`:

| Count (per workflow_type, unsynthesized) | Action |
|------------------------------------------|--------|
| 1-10 entries | Normal operation; all entries presented as mandatory context |
| > 10 entries | WARNING: "N OE entries without synthesis -- consider /problem-solving ps-synthesizer" |
| > 20 entries | STOP: execution blocked until user explicitly OVERRIDEs per P-020 |

---

# Integration with Other Skills

## /nuclear-sop -> /adversary (QG-HOLD)

`[QG-HOLD]` activation invokes `/adversary` via S-014 (LLM-as-Judge) to score the work product at the phase boundary. The quality gate threshold is 0.92 (H-13). sop-executor does not invoke /adversary directly -- the QG-HOLD mechanism calls /adversary's scoring capability.

```
sop-executor reaches [QG-HOLD] step
    |
    v
/adversary S-014 scores work product at phase boundary
    |
    +-- Score >= 0.92 -> AUTO-RELEASED; sop-executor continues
    |
    +-- Score < 0.92 -> critic findings returned; sop-executor revises; re-score
    |
    +-- Ceiling reached without passing -> user escalation per P-020
```

## /nuclear-sop -> /problem-solving (OE Synthesis)

When sop-brief detects > 10 unsynthesized OE entries for a `workflow_type`, it recommends running `/problem-solving ps-synthesizer` to distill lessons across prior entries before proceeding. This is advisory (WARNING), not a blocking STOP (unless count > 20).

```
sop-brief OE review: count > 10 unsynthesized entries
    |
    v
WARNING: "Consider /problem-solving ps-synthesizer to synthesize OE corpus"
    |
    v
User decision: run ps-synthesizer before execution, OR proceed with WARNING in brief
```

## /nuclear-sop -> /orchestration (Multi-Procedure Coordination)

When a workflow consists of multiple related procedures that must be coordinated (e.g., procedure A's output feeds procedure B), `/orchestration` sequences the /nuclear-sop invocations. Each individual procedure uses /nuclear-sop's full 3-hop or 4-hop sequence; `/orchestration` provides the cross-procedure barrier synchronization.

```
/orchestration plans multi-procedure workflow
    |
    | Barrier 1
    v
/nuclear-sop executes Procedure A (3-hop or 4-hop)
    -> OE entry written to docs/experience/
    |
    | Barrier 2 (orchestration reads Procedure A artifacts)
    v
/nuclear-sop executes Procedure B with Procedure A artifacts as prerequisites
    -> OE entry written to docs/experience/
```

## /nuclear-sop -> /eng-team (Security Review)

When sop-executor detects a STAR bypass attempt or hold point compromise (SEC-001, SR-04), it logs the anomaly and escalates per the enforcement configuration:
```
enforcement.escalation_path: "eng-security-001 for STAR bypass or hold point compromise"
```

This routes to `/eng-team eng-security` for security code review of the anomalous behavior.

---

# Common Workflows

## Workflow 1: Generate and Execute a New Procedure

**Scenario:** No workflow definition exists. User wants to execute a C2 ADR authoring procedure.

**Invocation:**
```
Use /nuclear-sop to generate and execute a procedure for authoring an ADR for
[decision topic] at C2 criticality. Use sop-brief Step 0 to generate the workflow
definition from this description, then execute the full 3-hop sequence.
```

**Expected artifact sequence:**
1. `brief/draft-workflow-definition.md` -- generated by sop-brief Step 0; presented for user APPROVE
2. `brief/pre-job-brief.md` -- sop-brief Step 1-6 output
3. `{execution_dir}/PROCEDURE_STATE.yaml` -- initialized by sop-executor Phase 0
4. `{execution_dir}/execution-log.md` -- STAR records per step
5. Work product artifacts per workflow definition
6. `capture/oe-entry-{entry_id}.yaml` -- local OE entry
7. `docs/experience/{entry_id}.yaml` -- persistent OE entry
8. `capture/post-job-brief.md`

---

## Workflow 2: Execute an Existing Workflow Definition at C3

**Scenario:** A workflow definition file exists at `skills/nuclear-sop/examples/c3-adr-workflow-definition.md`. User wants to execute at C3 criticality (4-hop mode).

**Invocation:**
```
Use /nuclear-sop to execute skills/nuclear-sop/examples/c3-adr-workflow-definition.md
at C3 criticality. Run sop-brief first, then sop-executor, then sop-verifier via Task
for fresh-context IV at the IV-HOLD point, then sop-capture.
```

**Expected artifact sequence:**
1. `brief/pre-job-brief.md` -- sop-brief output (Steps 1-6)
2. `{execution_dir}/PROCEDURE_STATE.yaml` -- initialized; status transitions through workflow
3. `{execution_dir}/execution-log.md` -- STAR records
4. Work product artifacts
5. IV-HOLD activation: `PROCEDURE_STATE.yaml status: IV-PENDING`
6. sop-verifier Task invocation: `iv-report-{step_id}-{YYYYMMDD}.md` returned in Task response
7. Main context persists IV report; updates PROCEDURE_STATE.yaml
8. `capture/oe-entry-{entry_id}.yaml` and `docs/experience/{entry_id}.yaml`
9. `capture/post-job-brief.md`

---

## Workflow 3: Resume a Paused Execution

**Scenario:** A previous session left PROCEDURE_STATE.yaml in status `HELD` at a USER-HOLD point.

**Invocation:**
```
Resume the nuclear-sop execution for workflow WF-ADR-001. PROCEDURE_STATE.yaml is at
{execution_dir}/PROCEDURE_STATE.yaml. Use sop-executor in RESUME mode.
```

**sop-executor RESUME behavior:**
1. Load existing PROCEDURE_STATE.yaml
2. Verify `state_schema_version` matches current schema
3. Verify `status` is not COMPLETED or ABORTED
4. Present resume context: workflow ID, criticality, `current_step`, `next_step`, held step if HELD
5. Confirm continuation with user per P-020 before executing next step
6. Continue execution from `next_step`

---

## Workflow 4: Capture OE for a Completed Execution

**Scenario:** sop-executor completed execution but sop-capture was not invoked.

**Invocation:**
```
Use /nuclear-sop sop-capture to write the OE entry for workflow execution
in {execution_dir}/. PROCEDURE_STATE.yaml shows execution_log_final set
(status IN-PROGRESS; sop-capture sets COMPLETED per NS-H-06).
```

**sop-capture verifies (Step 1):**
- `PROCEDURE_STATE.yaml execution_log_final` is set and resolves to an existing file before reading the execution log
- For C3+: `iv_report_path` present and file exists

---

# Quick Reference Table

## Step Sequence by Criticality

| Step | C1-C2 (3-hop) | C3-C4 (4-hop) | Mandatory? |
|------|--------------|--------------|------------|
| Step 0 | sop-brief (workflow generation) | sop-brief (workflow generation) | Optional |
| Step 1 | sop-brief (pre-job briefing) | sop-brief (pre-job briefing) | MANDATORY |
| Step 2 | sop-executor (STAR + place-keeping) | sop-executor (STAR + place-keeping) | MANDATORY |
| Step 3 | sop-capture Step 0 (integrated IV) | sop-verifier via Task (fresh-context IV) | MANDATORY (mode differs) |
| Step 4 | sop-capture (OE entry) | sop-capture (OE entry) | MANDATORY |

## Key Rules at a Glance

| Rule ID | Rule | Consequence |
|---------|------|-------------|
| NS-H-01 | STAR MANDATORY before every Write/Edit/Bash | Unlogged state mutation; STAR catch-rate invalidated |
| NS-H-02 | USER-HOLD MUST wait for APPROVE/REJECT/WAIVE | P-020 violation; unauthorized execution |
| NS-H-03 | QG-HOLD MUST have quality score >= 0.92 | H-13 quality gate bypass |
| NS-H-04 | IV-HOLD MUST have sop-verifier ACCEPT (C3+) | Anchored verification; quality compromise |
| NS-H-05 | After STAR REVIEW failure: STOP-WORK, log deviation, escalate | Silent drift; P-020 violation |
| NS-H-06 | OE write BLOCKED if any mandatory schema field absent | Corrupted OE feedback loop |
| NS-H-07 | sop-brief Step 1 MANDATORY for every invocation | Unbriefed execution; error traps not identified |
| NS-H-08 | C3+ workflows MUST use 4-hop mode (governance deadline: 60 days from Phase 1) | Anchored verification on irreversible work |
| NS-H-09 | sop-executor MUST stop at criticality step limit and hand off | Context exhaustion; STAR compliance degrades |
| NS-H-10 | PROCEDURE_STATE.yaml MUST update after every completed step | Lost place-keeping; corrupt resume |

## Output Artifacts Summary

| Artifact | Agent | Path | When |
|----------|-------|------|------|
| Draft workflow definition | sop-brief (Step 0) | `brief/draft-workflow-definition.md` | If generated from NL |
| Pre-job brief | sop-brief (Step 6) | `brief/pre-job-brief.md` | Every invocation |
| PROCEDURE_STATE.yaml | sop-executor | `{execution_dir}/PROCEDURE_STATE.yaml` | Updated per step |
| HOLD_POINT_LOG.md | sop-executor | `{execution_dir}/HOLD_POINT_LOG.md` | If hold points activated |
| execution-log.md | sop-executor | `{execution_dir}/execution-log.md` | Every execution |
| Work product artifacts | sop-executor | Per workflow definition | Every execution |
| IV report | sop-verifier | `{workflow_dir}/iv-report-{step}-{date}.md` | C3+ IV-HOLD only |
| Local OE entry | sop-capture | `capture/oe-entry-{entry_id}.yaml` | Every invocation |
| Persistent OE entry | sop-capture | `docs/experience/{entry_id}.yaml` | Every invocation |
| Post-job brief | sop-capture | `capture/post-job-brief.md` | Every invocation |

---

# L2: Architecture and Standards

> *H-36 circuit breaker compliance, security considerations, governance rulings.*

## H-36 Circuit Breaker Compliance

The 4-agent sequence creates an ambiguous case under H-36 (max 3 routing hops). Two operating modes are defined, with mode selection bound to workflow criticality.

**3-Hop Mode (C1-C2, Unambiguously Compliant)**

| Hop | From | To |
|-----|------|-----|
| 1 | Main context | sop-brief |
| 2 | Main context | sop-executor |
| 3 | Main context | sop-capture (with integrated IV) |

Trade-off: sop-capture has access to execution log before verifying (anchoring bias). Accepted for C1-C2 because work is reversible.

**4-Hop Mode (C3+, REQUIRED until governance ruling)**

| Hop | From | To | Classification |
|-----|------|-----|---------------|
| 1 | Main context | sop-brief | HOP (skill entry) |
| 2 | Main context | sop-executor | Predetermined sequence |
| 3 | Main context | sop-verifier | Claimed: NOT a hop (quality gate analog); Strict: HOP |
| 4 | Main context | sop-capture | Exceeds limit if hop 3 is a hop |

**Governance ruling deadline:** If no H-36 ruling within 60 days of Phase 1 delivery, 3-hop mode becomes permanent for all criticality levels. NS-H-08 must be revised at that deadline.

## P-003 Compliance

All nuclear-sop agents are workers, NOT orchestrators. The MAIN CONTEXT orchestrates the workflow.

```
P-003 AGENT HIERARCHY:
======================

  +---------------------------+
  | MAIN CONTEXT              |  <-- Orchestrator (Claude session)
  | (orchestrator)            |
  +---------------------------+
     |        |        |        |
     v        v        v        v
  +-------+ +-------+ +-------+ +-------+
  | sop-  | | sop-  | | sop-  | | sop-  |  <-- Workers (max 1 level)
  | brief | | exec  | |verify | |capture|
  +-------+ +-------+ +-------+ +-------+

  Agents CANNOT invoke other agents.
  Agents CANNOT spawn subagents.
  Only MAIN CONTEXT orchestrates the sequence.
  sop-verifier invoked via Task tool (fresh context isolation).
```

## Security Considerations

**Workflow Definitions Are Executable Content.** Treat workflow definition code review with the same rigor as a shell script review. Before using any workflow definition you did not author:
- Verify author and version metadata are accurate and trustworthy
- No step targets paths outside the intended project scope
- No Bash commands execute external processes without explicit rationale
- All `[USER-HOLD]` annotations are present on state-modifying steps for C3+ workflows

**Prompt Injection Surface (TB-1).** The workflow definition file is the primary trust boundary. Content read by sop-brief and sop-executor is injected into the agent's context. A malicious workflow definition can attempt to override agent behavior through embedded instructions. SEC-001 (WARNING/CAUTION injection guard) and SEC-002 (OE injection guard) are the primary mitigations.

**STAR Validation Pre-Ship Gate.** The skill is NOT available for C3+ workflows: the QG-E4 STAR A/B evidence (2026-04-20) was a simulation walkthrough (desk-check) and was invalidated in the PROJ-032 independent review (remediation register REM-04); C3+ approval is WITHDRAWN pending re-validation with independent execution evidence. STAR self-checking is a behavioral claim, not a verified deterministic constraint. Restrict to C1-C2 only.

## References

| Resource | Path | Purpose |
|----------|------|---------|
| SKILL.md | `skills/nuclear-sop/SKILL.md` | Skill definition, routing, activation keywords, H-36 analysis |
| Behavioral rules | `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` | HARD/MEDIUM rules NS-H-01 through NS-H-10 |
| Workflow definition template | `skills/nuclear-sop/templates/WORKFLOW_DEFINITION.template.md` | 11-section procedure structure |
| Procedure state template | `skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` | Execution state schema |
| Pre-job brief template | `skills/nuclear-sop/templates/PRE_JOB_BRIEF.template.md` | Briefing output structure |
| Post-job brief template | `skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md` | OE capture output structure |
| Hold point log template | `skills/nuclear-sop/templates/HOLD_POINT_LOG.template.md` | Hold point sign-off record |
| Example: C3 ADR workflow | `skills/nuclear-sop/examples/c3-adr-workflow-definition.md` | Worked example with STAR traps (QG-E4 fixture) |
| Composition: sop-brief | `skills/nuclear-sop/composition/sop-brief.agent.yaml` and `sop-brief.prompt.md` | Derived composition artifact (normative source: `agents/`) |
| Composition: sop-executor | `skills/nuclear-sop/composition/sop-executor.agent.yaml` and `sop-executor.prompt.md` | Derived composition artifact (normative source: `agents/`) |
| Composition: sop-verifier | `skills/nuclear-sop/composition/sop-verifier.agent.yaml` and `sop-verifier.prompt.md` | Derived composition artifact (normative source: `agents/`) |
| Composition: sop-capture | `skills/nuclear-sop/composition/sop-capture.agent.yaml` and `sop-capture.prompt.md` | Derived composition artifact (normative source: `agents/`) |
| Spec synthesis | `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-research-20260319-001/ps/phase-4/ps-synthesizer-001/skill-specification-synthesis.md` | Requirements SSOT (0.922) |
| ADR-001 | `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-research-20260319-001/ps/phase-3/ps-architect-001/ADR-001-nuclear-sop-skill-architecture.md` | Architecture decisions (0.933) |

---

*Playbook Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Skill: /nuclear-sop v1.1.0*
*Created: 2026-04-16*
*Agent: eng-lead*
