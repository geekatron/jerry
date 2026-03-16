# Engagement Lifecycle Model

> Shared engagement lifecycle across all /rainbow sub-skills. Defines the five phases every Zone 2 and Zone 3 engagement must follow. Referenced by rainbow-orchestrator, all sub-skill agents, and the engagement scope template.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Five-phase lifecycle summary |
| [Phase 1: Scope](#phase-1-scope) | Engagement scope definition and operator approval |
| [Phase 2: Authorize](#phase-2-authorize) | Scope validation and agent authorization |
| [Phase 3: Execute](#phase-3-execute) | Tool execution within scope constraints |
| [Phase 4: Report](#phase-4-report) | Findings aggregation and report production |
| [Phase 5: Close](#phase-5-close) | Engagement closure and artifact archival |
| [Lifecycle State Machine](#lifecycle-state-machine) | Valid state transitions |
| [Emergency Stop](#emergency-stop) | Immediate engagement termination |
| [Cross-Sub-Skill Coordination](#cross-sub-skill-coordination) | How lifecycle applies across sub-skills |
| [Traceability](#traceability) | Source references |

---

## Overview

Every /rainbow engagement that involves Zone 2 (active reconnaissance/interaction) or Zone 3 (exploitation) operations MUST follow this five-phase lifecycle. Zone 1 (analysis-only) operations do NOT require an engagement lifecycle -- they operate under standard project scope (H-04).

```
SCOPE --> AUTHORIZE --> EXECUTE --> REPORT --> CLOSE
  |          |             |          |         |
  v          v             v          v         v
 Define    Validate     Run tools  Aggregate  Archive
 targets   scope +      within     findings   artifacts
 + RoE     authorize    scope      + produce  + close
            agents      gates      reports    engagement
```

### Phase Gate Requirements

Each phase has a gate that MUST be passed before proceeding to the next phase. Gates are hard boundaries -- not advisory.

| Phase | Gate | Owner | Fail Action |
|-------|------|-------|-------------|
| Scope | Scope document complete with all required fields | Operator + rainbow-orchestrator | Cannot proceed to Authorize |
| Authorize | operator_approval present, scope validation passes | rainbow-orchestrator | Cannot proceed to Execute |
| Execute | Per-operation scope checks pass (target authorized, technique on allowlist, time_window current) | Each Zone 2/3 agent | Operation rejected; agent halts |
| Report | All Zone 2/3 operations complete or time_window expired | rainbow-reporter | Cannot proceed to Close |
| Close | Operator reviews scope coverage and any escalation events | Operator | Engagement remains open |

---

## Phase 1: Scope

### Purpose

Define the engagement boundaries: what targets are authorized, what techniques are permitted, what the time constraints are, and what rules of engagement apply.

### Actions

| Action | Owner | Output |
|--------|-------|--------|
| Create engagement scope document | rainbow-orchestrator or red-lead | `skills/rainbow/output/{engagement-id}/SCOPE.md` |
| Define authorized targets | Operator (human) | `authorized_targets` field populated |
| Define excluded targets | Operator (human) | `excluded_targets` field populated (may be empty) |
| Define time window | Operator (human) | `time_window.start` and `time_window.end` set |
| Define technique allowlist | Operator (human) | `technique_allowlist` populated |
| Define rules of engagement | Operator (human) | `rules_of_engagement` populated (rate limits, stealth, data handling) |
| Define escalation authority | Operator (human) | `escalation_authority` names a human operator |

### Scope Document Location

`skills/rainbow/output/{engagement-id}/SCOPE.md`

Engagement ID format: `RBW-NNNN` (e.g., `RBW-0001`).

See `skills/rainbow/rules/engagement-scope-template.yaml` for the complete field schema.

---

## Phase 2: Authorize

### Purpose

Validate the scope document for completeness and correctness, obtain operator approval, and authorize agents for the engagement.

### Actions

| Action | Owner | Gate |
|--------|-------|------|
| Validate scope document completeness | rainbow-orchestrator | All required fields present and valid |
| Validate time_window is in the future or present | rainbow-orchestrator | `start` <= now <= `end` |
| Validate authorized_targets contains at least 1 entry | rainbow-orchestrator | Non-empty list |
| Validate technique_allowlist contains at least 1 entry | rainbow-orchestrator | Non-empty list |
| Validate escalation_authority names a human | rainbow-orchestrator | Non-empty, not an agent name |
| Operator reviews and approves scope | Operator (human) | `operator_approval` field populated with name and timestamp |
| rainbow-orchestrator records authorization | rainbow-orchestrator | Authorization logged |

### Validation Checks

Before routing any task to a Zone 2 or Zone 3 agent, rainbow-orchestrator MUST verify:

1. The scope document exists at the expected path.
2. The `time_window` includes the current time.
3. The requested target is in `authorized_targets` and NOT in `excluded_targets`.
4. The requested technique is in `technique_allowlist`.
5. `operator_approval` is present and non-empty.

If ANY validation check fails, the orchestrator MUST reject the task and inform the user with the specific failing check per P-022.

---

## Phase 3: Execute

### Purpose

Execute tool-assisted operations within the authorized scope constraints. Every tool invocation is individually gated.

### Per-Operation Gate

Before EVERY tool invocation, the executing agent MUST:

1. Extract the target from command arguments.
2. Check target against `authorized_targets` (must be present).
3. Check target against `excluded_targets` (must NOT be present).
4. Check technique against `technique_allowlist` (must be present).
5. Check time_window (current time must be within window).
6. Apply rate limits from `rules_of_engagement`.

### Zone 2 Execution

- Standard pipeline: Subfinder, httpx, dnsx, Naabu, Katana, Nuclei (detection), Amass, Maigret
- Credential filter applied to ALL tool output
- Audit log entry for EVERY operation

### Zone 3 Escalation During Execution

When a Zone 3 trigger is detected during Zone 2 execution:

1. Agent HALTS the specific operation.
2. Agent logs the escalation event.
3. Agent presents escalation details to user.
4. User either approves (Zone 3 execution proceeds) or declines (operation skipped).
5. Agent continues with remaining Zone 2 operations.

---

## Phase 4: Report

### Purpose

Aggregate findings from all Zone 2 and Zone 3 operations. Produce a structured engagement report.

### Actions

| Action | Owner | Gate |
|--------|-------|------|
| Aggregate findings from all operations | rainbow-reporter (future W3+ agent) | All Zone 2/3 tasks complete or time_window expired |
| Classify findings by severity | rainbow-reporter (future W3+ agent) | Every finding has severity rating |
| Identify Zone 3 escalation candidates | rainbow-reporter (future W3+ agent) | Findings requiring deeper exploitation flagged |
| Produce engagement report | rainbow-reporter (future W3+ agent) | Report persisted to `skills/rainbow/output/{engagement-id}/reports/` |
| Include scope compliance summary | rainbow-reporter (future W3+ agent) | Coverage percentage, any scope violations, escalation events |

> **Note:** `rainbow-reporter` is a planned future agent (W3+ wave). It is listed in the parent SKILL.md agent registry as a cross-cutting agent. Until `rainbow-reporter` is implemented, Phase 4 reporting is performed by `rainbow-orchestrator` or the operator directly.

### Report Structure

| Section | Content |
|---------|---------|
| Executive Summary (L0) | Target count, finding summary, critical/high counts, scope coverage |
| Technical Findings (L1) | Per-tool results, vulnerability details, attack surface map |
| Strategic Assessment (L2) | Risk prioritization, remediation recommendations, next-phase candidates |
| Scope Compliance | Scope coverage, time utilization, escalation events, credential filter events |

---

## Phase 5: Close

### Purpose

Close the engagement. Review scope coverage. Archive all artifacts. Ensure no ongoing operations persist beyond the engagement window.

### Actions

| Action | Owner | Gate |
|--------|-------|------|
| Review scope coverage (targets assessed vs. authorized) | Operator + rainbow-orchestrator | Coverage reported |
| Review escalation events | Operator | All escalations documented |
| Review credential filter events | Operator | All quarantines documented |
| Archive engagement artifacts | rainbow-orchestrator | All artifacts in `skills/rainbow/output/{engagement-id}/` |
| Close engagement | Operator | Explicit operator decision |

### Artifact Archive Structure

```
skills/rainbow/output/{engagement-id}/
  SCOPE.md                           # Engagement scope document
  reports/                            # Final reports
  recon/                              # Reconnaissance artifacts
  audit/                              # Audit logs
    zone-2/                           # Zone 2 operation logs
    zone-3/                           # Zone 3 operation logs (if any)
```

---

## Lifecycle State Machine

Valid state transitions:

```
[CREATED] --> [SCOPED] --> [AUTHORIZED] --> [EXECUTING] --> [REPORTING] --> [CLOSED]
                                               |                              ^
                                               |  (time_window expired)       |
                                               +------------------------------+
```

| From | To | Trigger |
|------|----|---------|
| CREATED | SCOPED | Scope document created with all required fields |
| SCOPED | AUTHORIZED | operator_approval obtained and validation passes |
| AUTHORIZED | EXECUTING | First Zone 2/3 operation begins |
| EXECUTING | REPORTING | All operations complete OR time_window expired |
| REPORTING | CLOSED | Operator reviews report and closes engagement |
| EXECUTING | REPORTING | time_window expired (forced transition) |

Invalid transitions:
- CREATED to EXECUTING (scope and authorization required)
- SCOPED to EXECUTING (authorization required)
- CLOSED to any state (engagement is terminal)

---

## Emergency Stop

The operator may trigger an emergency stop at any time during EXECUTING phase.

### Emergency Stop Procedure

1. Operator communicates stop via the communication channel defined in `rules_of_engagement`.
2. rainbow-orchestrator immediately halts all active Zone 2/3 operations.
3. All agents cease tool execution.
4. Current partial results are persisted.
5. Emergency stop is logged in audit log with timestamp and reason.
6. Engagement transitions directly to REPORTING with partial results.

### Emergency Stop Triggers

- Operator decision (any reason)
- Target system instability detected
- Unintended impact observed
- Legal or compliance concern raised
- Credential exposure detected and not quarantined

---

## Cross-Sub-Skill Coordination

The engagement lifecycle applies uniformly across all /rainbow sub-skills that operate at Zone 2 or Zone 3.

| Sub-Skill | Phase 3 Agents | Zone |
|-----------|---------------|------|
| /rainbow-recon | rainbow-recon-pipeline, rainbow-recon-osint | Zone 2 |
| /rainbow-cloud | rainbow-cloud-auditor (Kyverno mutate), rainbow-cloud-mapper | Zone 2 |
| /rainbow-runtime | rainbow-runtime-instrument (intercept mode) | Zone 2 |
| /rainbow-supply-chain | rainbow-sc-verifier (Cosign download) | Zone 2 |
| /rainbow-exploit | All exploit agents | Zone 3 |

All agents in this table share the same engagement scope document and follow the same per-operation gate checks.

---

## Audit Log Entry Schema

The following 13-field schema is the SSOT for audit log entries across all /rainbow zones. Zone 1 uses a subset (8 fields -- `engagement_id` is null, `target_authorized`/`technique_authorized`/`escalation_triggered` fields are omitted). Zone 2 and Zone 3 use all 13 fields.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Rainbow Audit Log Entry",
  "type": "object",
  "required": ["timestamp", "zone", "agent", "tool", "subcommand", "target", "result_summary", "credential_filter_status"],
  "properties": {
    "timestamp":                { "type": "string", "format": "date-time", "description": "ISO 8601 operation timestamp" },
    "zone":                     { "type": "integer", "enum": [1, 2, 3], "description": "Security zone" },
    "engagement_id":            { "type": ["string", "null"], "pattern": "^RBW-\\d{4}$", "description": "Engagement scope ref (null for Zone 1)" },
    "agent":                    { "type": "string", "description": "Agent that executed the operation" },
    "tool":                     { "type": "string", "description": "Tool name" },
    "subcommand":               { "type": "string", "description": "Specific subcommand or mode" },
    "target":                   { "type": "string", "description": "Target addressed" },
    "target_authorized":        { "type": "boolean", "description": "Whether target passed scope validation" },
    "technique":                { "type": "string", "description": "Technique category" },
    "technique_authorized":     { "type": "boolean", "description": "Whether technique passed allowlist check" },
    "result_summary":           { "type": "string", "description": "One-line summary of findings" },
    "credential_filter_status": { "type": "string", "enum": ["passed", "quarantined", "rejected"], "description": "Credential filter outcome" },
    "duration_seconds":         { "type": "integer", "minimum": 0, "description": "Operation duration" },
    "escalation_triggered":     { "type": "boolean", "description": "Whether zone escalation was triggered" }
  }
}
```

**Zone-specific requirements:**
- **Zone 1:** `engagement_id` is null. `target_authorized`, `technique_authorized`, `escalation_triggered` are omitted (not applicable). 8 fields required.
- **Zone 2:** All 13 fields required. `engagement_id` must reference a valid scope document.
- **Zone 3:** All 13 fields required. Additionally, Zone 3 audit entries include the `operator_approval` from the scope document.

---

## Traceability

| Reference | Location |
|-----------|----------|
| ADR-PROJ023-001 | `projects/PROJ-023-exploit-framework/work/design/skill-architecture.md` |
| Zone 2 Guardrail Profile | `skills/rainbow/rules/zone-2-active.md` |
| Zone 3 Guardrail Profile | `skills/rainbow/rules/zone-3-exploit.md` |
| Engagement Scope Template | `skills/rainbow/rules/engagement-scope-template.yaml` |
| Rules of Engagement Template | `skills/rainbow/rules/rules-of-engagement-template.md` |
| Credential Filter | `skills/rainbow/rules/rainbow-credential-filter.md` |
| /red-team Engagement Methodology | `skills/red-team/agents/red-lead.md` |
