# Workflow Definition: {WORKFLOW_TITLE}

> **IMPORTANT: Workflow definitions are executable content.** sop-executor reads this file and issues tool calls based on step descriptions, WARNING/CAUTION blocks, and acceptance criteria embedded here. Treat this file with the same security rigor as a shell script. Before use, verify that no step directs the agent to read credential files, bypass hold points, or disable STAR self-checking. See SKILL.md Security Considerations (SR-06, TB-1).

## Document Sections

| Section | Purpose |
|---------|---------|
| [Section 1: Metadata](#section-1-metadata) | Workflow identity, version, criticality, authorship |
| [Section 2: Purpose and Scope](#section-2-purpose-and-scope) | What the procedure achieves and its boundaries |
| [Section 3: References](#section-3-references) | Source documents and related procedures |
| [Section 4: Prerequisites](#section-4-prerequisites) | Conditions that must be true before execution (sop-brief Step 2) |
| [Section 5: Initial Conditions](#section-5-initial-conditions) | Expected system state before Step 1 executes |
| [Section 6: Limitations and Precautions](#section-6-limitations-and-precautions) | Constraints and safety considerations |
| [Section 7: WARNINGs, CAUTIONs, and NOTEs](#section-7-warnings-cautions-and-notes) | Pre-placed annotations and their authority scope |
| [Section 8: Performance Steps](#section-8-performance-steps) | Numbered execution steps with classifications and hold points |
| [Section 9: Acceptance Criteria](#section-9-acceptance-criteria) | Verifiable completion criteria |
| [Section 10: Sign-off and Verification Record](#section-10-sign-off-and-verification-record) | Runtime execution record (written by sop-executor) |
| [Section 11: Attachments](#section-11-attachments) | Runtime attachments incl. OE entry reference (written by sop-capture) |

---

## Section 1: Metadata

| Field | Value |
|-------|-------|
| `workflow_id` | `{WORKFLOW_ID}` |
| `workflow_version` | `1.0.0` |
| `workflow_type` | `NOMINAL` |
| `criticality` | `C2` |
| `author` | `{AUTHOR}` |
| `created_date` | `{YYYY-MM-DD}` |
| `last_revised` | `{YYYY-MM-DD}` |
| `reviewed_by` | `{REVIEWER}` |
| `review_date` | `{YYYY-MM-DD}` |
| `applicable_skill` | `/nuclear-sop` |

**workflow_id format:** `{domain}-{action}-{sequence}` (e.g., `adr-authoring-c3-001`)

**workflow_type values:**
- `NOMINAL` -- standard operating procedure under expected conditions
- `ABNORMAL` -- procedure for off-normal but anticipated conditions
- `EMERGENCY` -- procedure for emergency response; highest hold point density

**criticality values:** C1 (routine, reversible in 1 session) | C2 (standard, reversible in 1 day) | C3 (significant, >1 day to reverse) | C4 (critical, irreversible or architecture-wide)

> **Step limit enforcement:** C1-C2 workflows: maximum 20 steps. C3 workflows: maximum 15 steps. C4 workflows: maximum 10 steps. If this workflow exceeds the limit, split into sub-procedures before execution. sop-brief will flag violations at Step 1 validation.

---

## Section 2: Purpose and Scope

### Purpose

{Describe what this procedure accomplishes and why it exists. Be specific: what system state does it transition from and to? What is the expected end state?}

### Scope

**In scope:**
- {Specific systems, files, directories, or processes this procedure acts upon}

**Out of scope:**
- {Systems, files, or processes this procedure MUST NOT touch}

**Applicability conditions:**
- {Conditions that must be true for this procedure to be the correct procedure to execute. If conditions differ, reference the applicable alternative procedure.}

---

## Section 3: References

| Document | Path or Location | Relevance |
|----------|-----------------|-----------|
| {Document title} | `{path/to/document}` | {Why this document is referenced} |

> List all documents that authorized this procedure, define standards it implements, or provide technical background. Include Jerry ADRs, external standards (OWASP, NIST, etc.), and prerequisite procedures.

---

## Section 4: Prerequisites

The following must be true before execution begins. sop-brief Step 2 verifies each prerequisite. If any prerequisite is not met, execution MUST NOT start.

| # | Prerequisite | Verification Method | Required State |
|---|-------------|--------------------|--------------:|
| P-1 | {Prerequisite name} | `{How to verify: file exists, tool available, etc.}` | {REQUIRED / CONDITIONAL} |

**Prerequisite failure policy:** A failed prerequisite is a STOP condition. sop-brief presents the failure to the user with options. Execution does not begin until all REQUIRED prerequisites are satisfied or the user explicitly accepts the risk per P-020.

---

## Section 5: Initial Conditions

Describe the expected state of all affected systems before Step 1 executes. sop-executor uses this section during STAR-STOP checks to verify starting conditions.

| System / Artifact | Expected Initial State |
|-------------------|------------------------|
| {File or system} | {Expected state: exists/absent, version, content signature} |

---

## Section 6: Limitations and Precautions

**Limitations:**
- {Known constraints on this procedure: environment requirements, model version dependencies, context window size limits, etc.}

**Precautions:**
- {Actions that will cause irreversible state changes. Document explicitly so STAR-THINK can flag these as requiring extra verification.}

**Recovery:**
- {If the procedure fails mid-execution, what is the recovery path? What artifacts can be used to resume? Is the partial state recoverable?}

---

## Section 7: WARNINGs, CAUTIONs, and NOTEs

> Place WARNING, CAUTION, and NOTE annotations BEFORE the affected step(s) in Section 8.
> This section provides the taxonomy only.

**WARNING** -- Immediate risk of significant unrecoverable harm if procedure is not followed exactly.
> Format: `> **WARNING:** {Specific risk description. Exact condition that triggers this risk.}`

**CAUTION** -- Risk of recoverable harm or reduced procedure quality if care is not taken.
> Format: `> **CAUTION:** {Specific risk description. What to verify before proceeding.}`

**NOTE** -- Additional context that aids understanding but does not require action.
> Format: `> **NOTE:** {Context. Reference to related procedure or document.}`

---

## Section 8: Performance Steps

> **Annotation conventions:**
> - `[CONTINUOUS]` -- Execute exactly as written. No deviation. Full STAR. Sign-off required.
> - `[REFERENCE]` -- Consult for guidance. Judgment permitted within step scope.
> - `[INFORMATION]` -- Background context. Not executed. No place-keeper advance.
> - `[USER-HOLD]` -- Blocking gate. AskUserQuestion REQUIRED. User must APPROVE, REJECT, or WAIVE.
> - `[QG-HOLD]` -- Quality gate. ps-critic S-014 score >= 0.92 required. Auto-releases on pass.
> - `[IV-HOLD]` -- Independent verification required. sop-verifier invoked in fresh context.
> - Unannotated steps in C3+ workflows default to `[CONTINUOUS]`.
> - Unannotated steps in C1-C2 workflows default to `[REFERENCE]`.

---

### Step 1 [CONTINUOUS]: {Step Title}

> **NOTE:** {Any contextual information needed before this step.}

**Action:** {Precise description of what to do. For [CONTINUOUS] steps: be specific about file paths, exact values, and expected outcomes. Ambiguity here is an error trap.}

**Target:** `{Exact file path, command, or system element. Use full repo-relative paths.}`

**Expected Result:** {Observable outcome after this step completes. This is the STAR-THINK expected outcome.}

**Sign-off Criterion:** {What condition must be true to sign off this step in PROCEDURE_STATE.yaml? Must be verifiable.}

---

### Step 2 [REFERENCE]: {Step Title}

> **CAUTION:** {Risk description if applicable. Place here, immediately before the step.}

**Action:** {Guidance-level description. Agent may exercise judgment on execution approach within scope.}

**Target:** `{File or system element}`

**Expected Result:** {Observable outcome.}

**Sign-off Criterion:** {Verifiable completion condition.}

---

### Step N [USER-HOLD] [CONTINUOUS]: {Step Title}

> **WARNING:** {Risk description. This step has a USER-HOLD. Document the reason explicitly here.}

**Hold Reason:** {Why is human authorization required here? What risk does this hold protect against?}

**Action:** {Action to execute AFTER user APPROVE response.}

**Target:** `{Exact path or system element}`

**Expected Result:** {Observable outcome after user approves and step executes.}

**Sign-off Criterion:** {Verifiable completion condition.}

---

### Step N+1 [QG-HOLD]: Phase Quality Gate

**Hold Reason:** Quality gate for work products produced in Steps 1 through N. Quality score >= 0.92 required per H-13.

**Work Products Under Review:**
- `{path/to/work-product-1}`
- `{path/to/work-product-2}`

**Acceptance Threshold:** 0.92 (per H-13 for C2+ workflows)

**Iteration Ceiling:** C1=3, C2=5, C3=7, C4=10 (per RT-M-010)

---

### Step N+2 [IV-HOLD]: Independent Verification

**Hold Reason:** Independent verification required before final acceptance of work products.

**Work Products Under Verification:**
- `{path/to/work-product-1}` -- {what sop-verifier should verify about this file}
- `{path/to/work-product-2}` -- {verification criteria}

**Verification Criteria Path:** `{path/to/acceptance-criteria.md or Section 9 of this document}`

> **NOTE:** sop-verifier receives ONLY these file paths. It does not receive the execution log, STAR records, or any executor reasoning chain. This context isolation is intentional (TB-4 trust boundary, SD-18). The file paths above are the canonical scope; sop-executor MUST pass these exact paths as iv_scope, not executor-interpreted output paths.

---

## Section 9: Acceptance Criteria

Each criterion must be verifiable (observable and measurable). Vague criteria are flagged by sop-brief Step 3.

| # | Criterion | Verification Method | PASS Condition |
|---|-----------|--------------------|--------------:|
| AC-1 | {Criterion title} | {How to verify: file exists, content matches, test passes, etc.} | {Specific measurable condition} |

**Acceptance criteria quality standard:** Each criterion must answer: "How will we know this step/procedure succeeded?" If the answer is subjective ("looks correct", "seems done"), rewrite the criterion with a specific measurable outcome.

---

## Section 10: Sign-off and Verification Record

> **This section is runtime-written by sop-executor. Template placeholders only.**

| Field | Value |
|-------|-------|
| Execution Start | `{ISO-8601 timestamp}` |
| Execution End | `{ISO-8601 timestamp}` |
| Steps Completed | `{N} of {total}` |
| Steps Deviated | `{count}` |
| Hold Points Activated | `{count}` |
| Stop-Work Events | `{count}` |
| Verification Mode | `{3-hop or 4-hop}` |
| Final PROCEDURE_STATE | `{COMPLETED / ABORTED}` |
| Execution Log Path | `{path/to/execution-log.md}` |
| PROCEDURE_STATE.yaml Path | `{path/to/PROCEDURE_STATE.yaml}` |
| HOLD_POINT_LOG.md Path | `{path/to/HOLD_POINT_LOG.md}` |

**Executor Sign-off:**

> sop-executor certifies: All [CONTINUOUS] steps executed exactly as written. All hold points activated as annotated. PROCEDURE_STATE.yaml updated after every step. Deviations logged with specificity. STAR self-checking applied before every Write, Edit, and Bash tool call.

---

## Section 11: Attachments

> **This section is runtime-written by sop-capture (OE entry) and referenced here after post-job brief completes.**

| Attachment | Path | Description |
|------------|------|-------------|
| Post-Job Brief | `{path/to/post-job-brief.md}` | sop-capture output: OE entry, lessons learned, verification outcome |
| OE Entry Reference | `{oe_entry_id}` | Reference to `docs/experience/{oe_entry_id}.yaml` |

---

*Template version: 1.0.0 | Nuclear pattern A-3 (Standard Procedure Structure) | /nuclear-sop skill*
*11-section structure: Metadata, Purpose/Scope, References, Prerequisites, Initial Conditions, Limitations/Precautions, WARNINGs/CAUTIONs/NOTEs, Performance Steps, Acceptance Criteria, Sign-off/Verification, Attachments*
*Structure derived from Nuclear Pattern A-3 (Standard Procedure Structure), source: Phase 1 Research Survey Section 3.3 — see `projects/PROJ-0039-nuclear-engineer/orchestration/nuclear-sop-build-20260325-001/eng/phase-1/` for full pattern catalog and source traceability.*
