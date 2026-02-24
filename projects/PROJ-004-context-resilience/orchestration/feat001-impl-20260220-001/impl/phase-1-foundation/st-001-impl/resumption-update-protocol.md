# Resumption Update Protocol

<!-- ST-001 | DATE: 2026-02-20 -->
<!-- Defines WHEN, WHO, and HOW the ORCHESTRATION.yaml resumption section is updated -->

> Operational protocol for maintaining the v2.0 resumption section as a living document.
> Addresses RG-6 (static resumption) from SPIKE-001 Phase 4: the root cause of all
> resumption gaps is that the section was written once and never updated during execution.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Design Principle](#design-principle) | Why this protocol exists |
| [Update Triggers](#update-triggers) | 6 lifecycle events that trigger resumption updates |
| [Sub-Section Update Matrix](#sub-section-update-matrix) | Which sub-sections are updated by which trigger |
| [Update Semantics](#update-semantics) | Append vs overwrite, merge strategy per sub-section |
| [Responsibility Assignment](#responsibility-assignment) | WHO updates each sub-section |
| [Backward Compatibility Rules](#backward-compatibility-rules) | How v1.0 fields map to v2.0 |
| [Staleness Detection](#staleness-detection) | How stale resumption data is detected |
| [Enforcement](#enforcement) | L2-REINJECT and hook-based enforcement |

---

## Design Principle

The resumption section MUST be a **living document** updated at every state transition.
A resuming session should be able to read ONLY the `resumption:` section (not the full
ORCHESTRATION.yaml) and orient itself within 2-3 prompts.

**Key insight from SPIKE-001 Phase 4 (RG-6):** The root cause of all resumption gaps
is that the section was static -- updated only at workflow completion, not incrementally.
If the section is updated at each state transition, it naturally accumulates defect
context (RG-1), decisions (RG-2), compaction records (RG-3), quality trajectory (RG-4),
and agent summaries (RG-5).

---

## Update Triggers

The orchestrator MUST update the resumption section at each of these 6 lifecycle events:

| # | Trigger | Event Description | Urgency |
|---|---------|-------------------|---------|
| T1 | **Phase Start** | A new phase begins execution | Normal |
| T2 | **Phase Complete** | All agents in a phase have completed | Normal |
| T3 | **Quality Gate Iteration** | Each QG iteration (not just final pass/fail) | Normal |
| T4 | **Agent Completion** | An individual agent finishes execution | Normal |
| T5 | **Compaction Event** | PreCompact hook fires (context compaction imminent) | Urgent |
| T6 | **Cross-Phase Decision** | A decision is made that affects downstream phases | Normal |

**Additional advisory trigger:**

| # | Trigger | Event Description | Urgency |
|---|---------|-------------------|---------|
| T7 | **Context Fill Threshold Crossing** | Context monitor detects a threshold transition (e.g., NOMINAL -> WARNING) | Advisory |

T7 is advisory: the orchestrator SHOULD update the resumption section when a threshold
is crossed to ensure data is fresh in case of unexpected compaction, but failure to
update at T7 is not a protocol violation.

---

## Sub-Section Update Matrix

Which sub-sections are updated at each trigger:

| Trigger | recovery_state | files_to_read | quality_trajectory | defect_summary | decision_log | agent_summaries | compaction_events |
|---------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| T1: Phase Start | W | - | - | - | - | - | - |
| T2: Phase Complete | W | U | - | - | - | - | - |
| T3: QG Iteration | W | - | W | W | C | - | - |
| T4: Agent Completion | W | - | - | - | - | A | - |
| T5: Compaction Event | W | - | - | - | - | - | A |
| T6: Cross-Phase Decision | W | - | - | - | A | - | - |
| T7: Threshold Crossing | W | - | - | - | - | - | - |

**Legend:**
- **W** = Overwrite (replace current values with new state)
- **A** = Append (add new entry to list/map)
- **U** = Update (modify specific fields within existing entries)
- **C** = Conditional append (add entry only if decision was made during iteration)
- **-** = No change

---

## Update Semantics

### recovery_state (Overwrite at every trigger)

All fields in `recovery_state` are overwritten with current values at every trigger.
This is the most frequently updated sub-section.

| Field | Update Action | Source |
|-------|--------------|--------|
| `last_checkpoint` | Set to latest checkpoint ID | `checkpoints.latest_id` |
| `current_phase` | Set to current phase number | Pipeline state |
| `current_phase_name` | Set to current phase name | Pipeline phase definition |
| `workflow_status` | Set to current status | Workflow lifecycle |
| `current_activity` | Set to current activity string | Execution context |
| `next_step` | Set to clear, actionable next step | Orchestrator determination |
| `context_fill_at_update` | Set to current fill % (if available) | Context monitor |
| `updated_at` | Set to current ISO 8601 timestamp | System clock |

### files_to_read (Update at phase transitions)

The `sections` hints within structured entries are updated when the phase changes, to
point resuming sessions at the most relevant sections.

- **On Phase Start (T1):** Update `sections` arrays to reference the new phase.
- **On Phase Complete (T2):** Update `sections` arrays, potentially add new relevant files.
- **Merge strategy:** Replace `sections` arrays; do not append indefinitely.

### quality_trajectory (Overwrite at QG iteration)

| Field | Update Action |
|-------|--------------|
| `gates_completed` | Append gate ID when gate passes |
| `gates_remaining` | Remove gate ID when gate passes |
| `current_gate` | Set to gate ID during iteration, null between gates |
| `current_gate_iteration` | Set to iteration number, null between gates |
| `score_history.{gate_id}` | Append new score to the gate's array |
| `lowest_dimension` | Recompute from all gate results |
| `total_iterations_used` | Increment by 1 |

### defect_summary (Overwrite at QG iteration)

| Field | Update Action |
|-------|--------------|
| `total_defects_found` | Increment by defects found in this iteration |
| `total_defects_resolved` | Increment by defects resolved in this iteration |
| `unresolved_defects` | Replace with current list of unresolved defect IDs |
| `recurring_patterns` | Append new pattern if one is identified; update resolution if resolved |
| `last_gate_primary_defect` | Set to primary defect from this iteration |

### decision_log (Append at cross-phase decisions)

New entries are appended. Existing entries are never modified except to update
`applied: true` when a deferred decision is applied.

| Field | Source |
|-------|--------|
| `id` | Sequential: RD-{NNN} |
| `gate` | Gate ID where decision was made (null if not gate-related) |
| `iteration` | Gate iteration number (null if not gate-related) |
| `decision` | Description of what was decided |
| `rationale` | Why this decision was made |
| `affects_phases` | Phase numbers affected |
| `applied` | Whether the decision has been applied yet |

### agent_summaries (Append at agent completion)

New entries are appended by agent ID. Each entry is a one-line summary string.
Completed agents are never removed or modified.

**Format:** `{agent_id}: "{status}. {key_finding_or_output}."`

**Examples:**
- `audit-executor: "PASS. All 25 deps Apache-2.0 compatible. No blockers."`
- `header-applicator: "DONE. 403 files modified with SPDX headers."`

### compaction_events (Append at compaction)

New compaction events are appended to the `events` array. The `count` field is
incremented. The `acknowledged` field is updated by the orchestrator after the
LLM processes the re-orientation prompt.

| Field | Source |
|-------|--------|
| `id` | Sequential: CX-{NNN} |
| `timestamp` | ISO 8601 from PreCompact hook |
| `trigger` | "auto" (system-initiated) or "manual" (operator-initiated) |
| `estimated_fill_before` | Fill % from context monitor state |
| `active_phase` | Current phase number |
| `active_gate` | Current gate ID (null if between gates) |
| `active_gate_iteration` | Current gate iteration (null if between gates) |
| `checkpoint_file` | Path to checkpoint JSON file |
| `acknowledged` | false initially; set to true after re-orientation |

---

## Responsibility Assignment

| Actor | Sub-Sections Updated | Trigger |
|-------|---------------------|---------|
| **Orchestrator** | recovery_state, files_to_read, quality_trajectory, defect_summary, decision_log, agent_summaries | T1-T4, T6-T7 |
| **PreCompact Hook** | compaction_events (via checkpoint file) | T5 |
| **Orchestrator (post-compaction)** | compaction_events.acknowledged, recovery_state | After re-orientation |
| **Quality Gate Scorer** | (provides data to orchestrator) | T3 |

**Key principle:** The orchestrator is the primary writer. The PreCompact hook writes
checkpoint files that the orchestrator merges into the resumption section after
re-orientation. No other actor writes to the resumption section directly.

---

## Backward Compatibility Rules

### V1.0 to V2.0 Field Mapping

| V1.0 Field | V2.0 Location | Migration Notes |
|-----------|--------------|-----------------|
| `last_checkpoint` | `recovery_state.last_checkpoint` | Moved into recovery_state sub-section |
| `current_state` | Decomposed into `recovery_state.{current_phase, current_phase_name, workflow_status, current_activity}` | Prose string replaced by structured fields |
| `next_step` | `recovery_state.next_step` | Moved into recovery_state sub-section |
| `files_to_read` (string array) | `files_to_read` (structured array) | Top-level key preserved. Simple string paths accepted alongside structured entries |
| `cross_session_portable` | `recovery_state.cross_session_portable` | Moved into recovery_state, optional |
| `ephemeral_references` | `recovery_state.ephemeral_references` | Moved into recovery_state, optional |

### Compatibility Guarantees

1. **`files_to_read` accepts both formats.** The schema validates both simple string
   paths (v1.0) and structured `{path, priority, purpose, sections}` entries (v2.0).
   Mixed arrays are valid.

2. **New sub-sections are additive.** A v1.0 reader that only knows the original 5 fields
   will still find `last_checkpoint` and `next_step` within `recovery_state`, and
   `files_to_read` at the top level. New sub-sections (`quality_trajectory`,
   `defect_summary`, `decision_log`, `agent_summaries`, `compaction_events`) are
   additive and ignored by v1.0 readers.

3. **`current_state` is decomposed, not deleted.** The prose `current_state` string is
   replaced by machine-readable structured fields. The `next_step` field preserves the
   actionable component. The `current_activity` field preserves the "what is happening"
   component. The `workflow_status` field preserves the lifecycle state.

---

## Staleness Detection

The `recovery_state.updated_at` field enables staleness detection:

| Staleness Level | Condition | Action |
|----------------|-----------|--------|
| FRESH | `updated_at` is within the current phase/activity | No action needed |
| STALE | `updated_at` is from a previous phase or > 30 minutes old | Warning injected via context monitor |
| CRITICAL | `updated_at` is from a previous session | Mandatory update before proceeding |

**Detection mechanism (dual enforcement per OQ-R5):**

1. **L2 (prompt injection):** The `<context-monitor>` tag includes a `Resumption staleness`
   field that compares `updated_at` against the current time and phase. Flagged as STALE
   if not updated since the current phase started.

2. **L3/L4 (hook-based):** The PreToolUse hook checks `updated_at` after ORCHESTRATION.yaml
   writes. If stale, injects a staleness warning. This is deterministic and immune to
   context rot.

---

## Enforcement

### L2-REINJECT Marker

A new L2-REINJECT marker in `quality-enforcement.md` reminds the orchestrator to update
the resumption section:

```html
<!-- L2-REINJECT: rank=9, tokens=25, content="Resumption update: MUST update ORCHESTRATION.yaml resumption section at every state transition (phase/QG/agent/compaction)." -->
```

- **Rank:** 9 (lowest priority among existing markers)
- **Budget:** ~25 tokens
- **Total L2 budget impact:** Existing ~600 tokens + ~25 tokens = ~625 tokens (within budget)

### Hook-Based Enforcement

The PreToolUse hook (future EN-005 implementation) checks `resumption.updated_at` on
ORCHESTRATION.yaml writes. If the timestamp indicates staleness relative to the current
phase, a warning is injected into the tool call response.
