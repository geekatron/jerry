# Pre-Job Brief: {{WORKFLOW_NAME}}

> **Nuclear Pattern:** F-2a (Pre-Job Briefing) | **Agent:** sop-brief | **Generated:** {{BRIEF_DATE}}
> **Workflow ID:** {{WORKFLOW_ID}} | **Criticality:** {{CRITICALITY}}
> **Status:** {{BRIEF_STATUS}}
> **Brief Version:** {{BRIEF_VERSION}}

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Procedure Identity](#procedure-identity) | Workflow metadata extracted from definition |
| [Prerequisite Status](#prerequisite-status) | Pass/Fail/Waived status per prerequisite |
| [Initial Conditions](#initial-conditions) | Expected starting state confirmed by sop-brief |
| [Acceptance Criteria Assessment](#acceptance-criteria-assessment) | Verifiable/Vague classification per criterion |
| [Operating Experience Findings](#operating-experience-findings) | MANDATORY -- all prior OE entries for this workflow type |
| [Error Traps Identified](#error-traps-identified) | WARNING/CAUTION annotations and inferred traps |
| [Hold Point Summary](#hold-point-summary) | All hold points by type with release conditions |
| [Step Limit Assessment](#step-limit-assessment) | Total steps vs. criticality limit |
| [Scope Confirmation](#scope-confirmation) | Execution scope and out-of-scope boundaries |
| [Hold Point Authorities](#hold-point-authorities) | Who releases each hold point type |

---

## Procedure Identity

| Property | Value |
|----------|-------|
| **Workflow Name** | {{WORKFLOW_NAME}} |
| **Workflow ID** | {{WORKFLOW_ID}} |
| **Workflow Type** | {{WORKFLOW_TYPE}} |
| **Workflow Version** | {{WORKFLOW_VERSION}} |
| **Author** | {{WORKFLOW_AUTHOR}} |
| **Created Date** | {{WORKFLOW_CREATED_DATE}} |
| **Criticality Level** | {{CRITICALITY}} |
| **Workflow Definition Path** | `{{WORKFLOW_DEFINITION_PATH}}` |
| **CONTINUOUS Step Count** | {{CONTINUOUS_STEP_COUNT}} |
| **REFERENCE Step Count** | {{REFERENCE_STEP_COUNT}} |
| **INFORMATION Step Count** | {{INFORMATION_STEP_COUNT}} |
| **Total Steps** | {{TOTAL_STEP_COUNT}} |

> **SD-05 Compliance:** Workflow definition metadata is displayed here per security design decision SD-05 (T-1.1). Review the author, version, and date before proceeding. An unknown author or unexpected version may indicate the workflow definition was modified outside the normal review process.

---

## Prerequisite Status

> **Pattern D-1:** All prerequisites must be verified before execution begins. Failed prerequisites that are not WAIVED by the user constitute a STOP condition.

| # | Prerequisite | Type | Status | Notes |
|---|-------------|------|--------|-------|
| 1 | {{PREREQ_1_DESCRIPTION}} | {{PREREQ_1_TYPE}} | {{PREREQ_1_STATUS}} | {{PREREQ_1_NOTES}} |
| 2 | {{PREREQ_2_DESCRIPTION}} | {{PREREQ_2_TYPE}} | {{PREREQ_2_STATUS}} | {{PREREQ_2_NOTES}} |
<!-- Add rows as needed for each prerequisite in the workflow definition -->

**Prerequisite Summary:** {{PREREQ_PASS_COUNT}} PASS | {{PREREQ_FAIL_COUNT}} FAIL | {{PREREQ_WAIVED_COUNT}} WAIVED

{{#if PREREQ_WAIVED}}
> **WAIVED Prerequisites:** The following prerequisites were waived by the user with justification:
>
> {{WAIVE_JUSTIFICATION_LIST}}
{{/if}}

{{#if PREREQ_FAIL_UNRESOLVED}}
> **STOP: Unresolved prerequisite failures prevent execution from proceeding.**
{{/if}}

---

## Initial Conditions

> **Pattern A-3 Section 3:** Confirm the starting state of the environment before execution. These conditions are confirmed by sop-brief, not assumed.

| # | Condition | Confirmed | Notes |
|---|-----------|-----------|-------|
| 1 | {{INITIAL_CONDITION_1}} | {{IC_1_STATUS}} | {{IC_1_NOTES}} |
| 2 | {{INITIAL_CONDITION_2}} | {{IC_2_STATUS}} | {{IC_2_NOTES}} |
<!-- Add rows as needed -->

---

## Acceptance Criteria Assessment

> **Pattern A-3 Section 9:** Each acceptance criterion must be verifiable (has a specific, measurable outcome). Vague criteria receive a WARNING and a request for clarification. If ALL criteria are vague or missing, this is a STOP condition.

| # | Criterion | Classification | Notes |
|---|-----------|---------------|-------|
| 1 | {{CRITERION_1_TEXT}} | {{CRITERION_1_CLASSIFICATION}} | {{CRITERION_1_NOTES}} |
| 2 | {{CRITERION_2_TEXT}} | {{CRITERION_2_CLASSIFICATION}} | {{CRITERION_2_NOTES}} |
<!-- Add rows as needed -->

**Classification key:** `VERIFIABLE` = measurable, specific outcome | `VAGUE` = subjective or unmeasurable as stated

{{#if VAGUE_CRITERIA_COUNT_GT_0}}
> **WARNING:** {{VAGUE_CRITERIA_COUNT}} acceptance criteria classified as VAGUE. sop-executor cannot perform objective verification against these criteria. Proceed only if user has confirmed acceptable outcome criteria informally, and understand that post-job verification will be qualitative for these items.
{{/if}}

---

## Operating Experience Findings

> **Pattern H-2:** Operating experience from prior executions is MANDATORY CONTEXT for this brief, not optional reading. Every entry listed here represents a prior failure, deviation, or lesson learned from workflows of this type. Read all entries before proceeding.
>
> **Entries listed:** {{OE_ENTRY_COUNT}} | **Synthesis entries:** {{OE_SYNTHESIS_COUNT}} | **Unanalyzed entries:** {{OE_UNANALYZED_COUNT}}

{{#if OE_WARNING}}
> **WARNING:** {{OE_UNANALYZED_COUNT}} OE entries for workflow_type `{{WORKFLOW_TYPE}}` have not been synthesized. Consider running sop-capture synthesis before execution to consolidate these lessons.
{{/if}}

{{#if OE_STOP}}
> **STOP CONDITION TRIGGERED:** OE accumulation threshold exceeded (>20 entries without synthesis). This section was displayed to the user and an explicit override was required to proceed. Override recorded: {{OE_OVERRIDE_RECORDED}}.
{{/if}}

{{#if NO_OE_ENTRIES}}
> **No prior OE entries found** for workflow_type `{{WORKFLOW_TYPE}}`. This is informational -- the absence of OE entries does not indicate the workflow is low-risk. First executions have no prior failure data by definition.
{{/if}}

### OE Entry List

<!-- For each OE entry found, populate one block below -->

#### OE Entry: {{OE_1_ENTRY_ID}} {{OE_1_PROVENANCE_FLAG}}

| Field | Value |
|-------|-------|
| **Entry ID** | {{OE_1_ENTRY_ID}} |
| **Date** | {{OE_1_DATE}} |
| **Workflow ID** | {{OE_1_WORKFLOW_ID}} |
| **Deviation Type** | {{OE_1_DEVIATION_TYPE}} |
| **Root Cause** | {{OE_1_ROOT_CAUSE}} |
| **Recommendation** | {{OE_1_RECOMMENDATION}} |
| **Verification Outcome** | {{OE_1_VERIFICATION_OUTCOME}} |
| **Criticality** | {{OE_1_CRITICALITY}} |

{{#if OE_1_PROVENANCE_UNVERIFIED}}
> **[PROVENANCE-UNVERIFIED]:** No PROCEDURE_STATE.yaml with `status: COMPLETED` was found matching this entry's `workflow_id`. This OE entry cannot be confirmed as documenting a real completed execution. Treat its findings with appropriate caution.
{{/if}}

<!-- Repeat OE entry block for each additional entry -->

---

## Error Traps Identified

> **Pattern A-4 (WARNING/CAUTION Pre-Placement):** Error traps are known danger conditions identified from WARNING/CAUTION annotations in the workflow definition, plus patterns inferred from step content. The STAR protocol (Stop-Think-Act-Review) must be explicitly applied at each of these steps.

| # | Step | Trap Type | Description | STAR Guidance |
|---|------|-----------|-------------|---------------|
| 1 | {{TRAP_1_STEP}} | {{TRAP_1_TYPE}} | {{TRAP_1_DESCRIPTION}} | {{TRAP_1_STAR_GUIDANCE}} |
| 2 | {{TRAP_2_STEP}} | {{TRAP_2_TYPE}} | {{TRAP_2_DESCRIPTION}} | {{TRAP_2_STAR_GUIDANCE}} |
<!-- Add rows as needed -->

**Trap type key:** `WARNING` = from explicit WARNING annotation | `CAUTION` = from explicit CAUTION annotation | `INFERRED` = identified by sop-brief from step pattern (not explicitly annotated)

{{#if NO_ERROR_TRAPS}}
> No WARNING/CAUTION annotations found in the workflow definition. No inferred traps identified. This does not mean the workflow is trap-free -- first executions against new targets may reveal traps not yet annotated.
{{/if}}

---

## Hold Point Summary

> All hold points must be resolved in the order they appear. sop-executor MUST NOT advance past a hold point step until the release condition is satisfied. Hold points CANNOT be bypassed by modifying PROCEDURE_STATE.yaml directly.

| # | Step | Hold Point Type | Release Condition | Authority |
|---|------|----------------|-------------------|-----------|
| 1 | {{HP_1_STEP}} | {{HP_1_TYPE}} | {{HP_1_RELEASE}} | {{HP_1_AUTHORITY}} |
| 2 | {{HP_2_STEP}} | {{HP_2_TYPE}} | {{HP_2_RELEASE}} | {{HP_2_AUTHORITY}} |
<!-- Add rows as needed -->

**Hold point types:**
- `USER-HOLD`: Requires AskUserQuestion APPROVE/REJECT/WAIVE. Authority: **User**.
- `QG-HOLD`: Requires ps-critic quality score >= 0.92. Authority: **Quality Gate**.
- `IV-HOLD`: Requires sop-verifier ACCEPT disposition (fresh context). Authority: **sop-verifier** (C3+ only).

{{#if SR02_WARNING}}
> **SR-02 WARNING:** This C3+ workflow contains state-modifying steps with no USER-HOLD annotation in the step sequence. The sop-executor will apply the STAR protocol at those steps, but there is no mandatory pause for user review before the action executes. Consider adding USER-HOLD annotations to state-modifying steps before execution.
{{/if}}

{{#if NO_HOLD_POINTS}}
> No hold points found in this workflow definition. All steps will execute sequentially under sop-executor's STAR self-checking protocol. For C3+ workflows, the absence of hold points is unusual -- confirm this is intentional before proceeding.
{{/if}}

---

## Step Limit Assessment

> **SD-10 / nuclear-sop-behavior-rules.md:** Step count limits per criticality level exist to prevent context window exhaustion during execution. Exceeding the limit requires sub-procedure splitting.

| Property | Value |
|----------|-------|
| **Total Steps in Workflow** | {{TOTAL_STEP_COUNT}} |
| **Criticality Level** | {{CRITICALITY}} |
| **Limit for This Criticality** | {{STEP_LIMIT}} |
| **Assessment** | {{STEP_LIMIT_STATUS}} |

**Step limit status:** `PASS` = within limit | `WARN` = at limit | `FAIL` = exceeds limit (splitting required)

{{#if STEP_LIMIT_FAIL}}
> **STEP LIMIT EXCEEDED:** This workflow has {{TOTAL_STEP_COUNT}} steps but the {{CRITICALITY}} limit is {{STEP_LIMIT}}. Execution cannot proceed until the user approves a sub-procedure split. The recommended split was presented to the user during sop-brief Step 1. User decision: {{STEP_LIMIT_USER_DECISION}}.
{{/if}}

---

## Scope Confirmation

> Explicitly state what this workflow covers and what it does NOT cover. Scope boundaries prevent scope creep during execution and provide a reference point for stop-work decisions.

**In Scope:**

{{SCOPE_IN_SCOPE_DESCRIPTION}}

**Out of Scope:**

{{SCOPE_OUT_OF_SCOPE_DESCRIPTION}}

**Files and Paths in Scope:**

| Path | Permission |
|------|-----------|
| {{SCOPE_PATH_1}} | {{SCOPE_PERMISSION_1}} |
| {{SCOPE_PATH_2}} | {{SCOPE_PERMISSION_2}} |
<!-- Add rows as needed -->

> If sop-executor encounters a step that would operate outside these scope boundaries, it must invoke stop-work authority (D-2) and escalate to the user.

---

## Hold Point Authorities

> This section documents who is authorized to release each type of hold point. This is a reference for the executor and for post-job review.

| Hold Point Type | Release Mechanism | Authority | Cannot Be Released By |
|----------------|-------------------|-----------|----------------------|
| USER-HOLD | AskUserQuestion with APPROVE/REJECT/WAIVE response | User (explicit selection required) | sop-executor autonomously; PROCEDURE_STATE.yaml direct edit |
| QG-HOLD | ps-critic quality score >= 0.92 via /adversary S-014 | Quality Gate (automated scoring) | sop-executor self-assessment without ps-critic invocation |
| IV-HOLD | sop-verifier ACCEPT disposition (fresh context, 4-hop mode) | sop-verifier (C3+) | sop-capture in 3-hop mode at C3+ criticality |

> **Constitutional constraint (P-020):** No hold point may be released by modifying PROCEDURE_STATE.yaml directly to change the `hold_resolution` or `status` fields. The only valid state transition from HELD is through the hold point release mechanism listed above. SR-04 compliance requires that sop-executor enforce this constraint.

---

*Pre-job brief generated by sop-brief v1.0.0 | Pattern: F-2a (Pre-Job Briefing) | /nuclear-sop skill*
