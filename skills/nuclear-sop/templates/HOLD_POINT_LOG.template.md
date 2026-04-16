# Hold Point Log: {WORKFLOW_ID}

> **Purpose:** Auditable record of every hold point activation during a sop-executor execution.
> **Maintained by:** sop-executor (appended at each hold point activation and resolution).
> **Security:** This log is an audit trail. Entries MUST NOT be edited or deleted after writing.
>              Resolution entries must match the corresponding PROCEDURE_STATE.yaml hold_resolution field.
>              Discrepancies between this log and PROCEDURE_STATE.yaml indicate state file tampering.

| Field | Value |
|-------|-------|
| Workflow ID | `{WORKFLOW_ID}` |
| Workflow Version | `{WORKFLOW_VERSION}` |
| Execution Started | `{ISO-8601}` |
| PROCEDURE_STATE Path | `{path/to/PROCEDURE_STATE.yaml}` |

---

## Hold Point Events

| hold_id | hold_type | step | activated_at | hold_prompt | resolution | resolved_at | resolved_by |
|---------|-----------|------|--------------|-------------|------------|-------------|-------------|
| | | | | | | | |

---

## Column Definitions

| Column | Type | Description |
|--------|------|-------------|
| `hold_id` | string | Auto-incrementing ID per execution. Format: `HP-{NNN}` where NNN is zero-padded sequence (HP-001, HP-002, ...). Reset to HP-001 on each fresh execution. |
| `hold_type` | enum | `USER-HOLD` -- requires AskUserQuestion + explicit user response. `QG-HOLD` -- requires ps-critic quality score >= 0.92. `IV-HOLD` -- requires sop-verifier ACCEPT disposition. |
| `step` | integer | Step number in the workflow definition where this hold point was activated. |
| `activated_at` | ISO-8601 | Timestamp when sop-executor entered the HELD state for this hold point. Format: `YYYY-MM-DDTHH:MM:SSZ`. |
| `hold_prompt` | string | The hold reason text from the workflow definition step annotation. Verbatim, not paraphrased. For QG-HOLD: quality gate description. For IV-HOLD: verification scope summary. |
| `resolution` | enum | `APPROVED` -- user responded APPROVE (USER-HOLD). `REJECTED` -- user responded REJECT (USER-HOLD). `WAIVED` -- user responded WAIVE (USER-HOLD, P-020 authority). `AUTO-RELEASED` -- ps-critic score >= 0.92 (QG-HOLD). `ACCEPT` -- sop-verifier returned ACCEPT disposition (IV-HOLD pass). `REJECT` -- sop-verifier returned REJECT disposition (IV-HOLD, revision required). |
| `resolved_at` | ISO-8601 | Timestamp when the hold was released and execution resumed. Format: `YYYY-MM-DDTHH:MM:SSZ`. Null if hold is currently active. |
| `resolved_by` | string | `User` (USER-HOLD). `ps-critic: {score}` (QG-HOLD: include final score). `sop-verifier: ACCEPT` (IV-HOLD ACCEPT disposition). `sop-verifier: REJECT (iteration {N})` (IV-HOLD REJECT disposition). `Pending` (hold currently active). Note: IV-HOLD resolution values (ACCEPT/REJECT) match sop-verifier output vocabulary; USER-HOLD resolution values (APPROVED/REJECTED/WAIVED) match user response vocabulary. |

---

## Example Entries

The following examples illustrate correct log entry format. Remove before use.

| hold_id | hold_type | step | activated_at | hold_prompt | resolution | resolved_at | resolved_by |
|---------|-----------|------|--------------|-------------|------------|-------------|-------------|
| HP-001 | USER-HOLD | 3 | 2026-03-26T14:30:00Z | Authorize write to projects/PROJ-0039/decisions/ADR-001.md | APPROVED | 2026-03-26T14:31:22Z | User |
| HP-002 | QG-HOLD | 7 | 2026-03-26T15:00:00Z | Phase 1 quality gate: ADR draft review. Score >= 0.92 required. | AUTO-RELEASED | 2026-03-26T15:08:45Z | ps-critic: 0.934 |
| HP-003 | IV-HOLD | 9 | 2026-03-26T15:45:00Z | Independent verification of ADR-001.md and supporting analysis | ACCEPT | 2026-03-26T16:20:00Z | sop-verifier: ACCEPT |
| HP-004 | USER-HOLD | 5 | 2026-03-26T14:45:00Z | Review draft before proceeding to implementation | WAIVED | 2026-03-26T14:45:38Z | User |
| HP-005 | IV-HOLD | 9 | 2026-03-27T09:00:00Z | Independent verification of ADR-001.md (revision 2) | REJECT | 2026-03-27T09:30:00Z | sop-verifier: REJECT (iteration 1) |

---

## Hold Point Summary

> **This section is runtime-populated by sop-executor at execution completion.**

| Metric | Count |
|--------|-------|
| Total hold points activated | `{count}` |
| USER-HOLD activations | `{count}` |
| QG-HOLD activations | `{count}` |
| IV-HOLD activations | `{count}` |
| USER-HOLD APPROVEDs | `{count}` |
| USER-HOLD REJECTs | `{count}` |
| USER-HOLD WAIVEs | `{count}` |
| QG-HOLD iterations (total) | `{count}` |
| QG-HOLD AUTO-RELEASEs | `{count}` |
| IV-HOLD REJECTs (iterations) | `{count}` |
| IV-HOLD ACCEPTs | `{count}` |
| Holds currently active (PENDING) | `{count}` |

---

*Template version: 1.0.0 | /nuclear-sop skill | sop-executor hold point audit trail*
