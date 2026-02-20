# Resumption Completeness Assessment

<!-- PS-ID: SPIKE-001 | ENTRY-ID: phase-4-resumption | DATE: 2026-02-19 -->
<!-- AGENT: ps-analyst v2.2.0 (resumption-assessor) | MODEL: claude-opus-4-6 -->

> Gap analysis of ORCHESTRATION.yaml `resumption` section, enhanced schema design, and
> checkpoint data specification for context-resilient session handoff.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Key gaps and proposed schema overview |
| [Current State Analysis](#current-state-analysis) | What exists in PROJ-001 and the template |
| [Gap Analysis](#gap-analysis) | RG-1 through RG-6 severity assessment |
| [Enhanced Resumption Schema](#enhanced-resumption-schema) | Proposed YAML additions |
| [Checkpoint Data Design](#checkpoint-data-design) | What checkpoint files contain |
| [Integration with Detection System](#integration-with-detection-system) | How Hybrid A+B triggers checkpoints |
| [WORKTRACKER.md as Resumption Aid](#worktrackmd-as-resumption-aid) | Assessment of WORKTRACKER for session recovery |
| [Open Questions](#open-questions) | For Phase 5 prompt design |
| [Self-Review Checklist](#self-review-checklist) | S-010 compliance verification |
| [References](#references) | Sources |

---

## L0 Summary

**Key Finding:** The current `resumption:` section in both the PROJ-001 completed ORCHESTRATION.yaml and the template is structurally minimal -- 5 fields occupying 12 lines. It captures *where* the workflow is (checkpoint ID, status string, next step) and *what to read* (3 files), but it captures nothing about *what happened* (defect history, decisions, quality trajectory) or *what was lost* (compaction events, agent context). A new Claude session reading only the current resumption section would know the workflow is complete and what to do next, but would lack the accumulated intelligence needed to make informed decisions if resuming mid-workflow.

**Severity Distribution:**
- CRITICAL: 2 gaps (RG-1 accumulated defect context, RG-6 static resumption / no compaction records)
- HIGH: 2 gaps (RG-2 inter-phase decisions, RG-5 agent-specific context)
- MEDIUM: 2 gaps (RG-3 compaction event records, RG-4 quality score trajectory)

**Proposed Solution:** An enhanced `resumption:` schema with 7 new sub-sections (18 additional fields) that are auto-populated during execution by the orchestrator and the Hybrid A+B detection system. The design includes a companion checkpoint file format (`.jerry/checkpoints/`) that the `PreCompact` hook writes before compaction, and the `UserPromptSubmit` hook surfaces to the LLM after compaction.

**Design Principle:** The resumption section must be a **living document** updated at every state transition (phase start, gate iteration, compaction event), not a static planning artifact. The enhanced schema makes the resumption section the single authoritative source for session recovery -- a resuming session should be able to read ONLY the `resumption:` section (not the full ORCHESTRATION.yaml) and orient itself within 2-3 prompts.

---

## Current State Analysis

### PROJ-001 Resumption Section (Completed Workflow)

Source: `projects/PROJ-001-oss-release/ORCHESTRATION.yaml`, lines 638-649.

```yaml
resumption:
  last_checkpoint: "CP-003"
  current_state: "WORKFLOW COMPLETE. All 4 phases done. All 6 enablers done. All 4 quality gates PASS (QG-1: 0.941, QG-2: 0.9505, QG-3: 0.935, QG-Final: 0.9335)."
  next_step: "Close FEAT-015 feature entity and update WORKTRACKER.md."

  files_to_read:
    - "projects/PROJ-001-oss-release/ORCHESTRATION_PLAN.md"   # Strategic context
    - "projects/PROJ-001-oss-release/ORCHESTRATION.yaml"       # This file
    - "projects/PROJ-001-oss-release/WORKTRACKER.md"           # Tactical documentation

  cross_session_portable: true
  ephemeral_references: false
```

**What it captures (5 fields):**

| Field | Value Assessment | Sufficient for Resumption? |
|-------|-----------------|---------------------------|
| `last_checkpoint` | CP-003 (links to checkpoints section) | Partially -- identifies recovery point but not what happened since |
| `current_state` | Human-readable summary with final scores | Yes for terminal state; No for mid-workflow (no structured data) |
| `next_step` | Clear single action | Yes for simple next action; No for complex remaining work |
| `files_to_read` | 3 key files listed | Partially -- lists files but not which sections matter or load priority |
| `cross_session_portable` / `ephemeral_references` | Boolean flags | Declarative but not actionable -- what should a session DO with these? |

**Critical observation:** The `current_state` field embeds quality scores as a prose string. A resuming LLM must parse natural language to extract scores. This is fragile and becomes ambiguous for mid-workflow states where multiple gates have different statuses.

### Template Resumption Section

Source: `skills/orchestration/templates/ORCHESTRATION.template.yaml`, lines 300-311.

```yaml
resumption:
  last_checkpoint: null
  current_state: "Workflow not started"
  next_step: "Execute Phase 1 agents"

  files_to_read:
    - "ORCHESTRATION_PLAN.md"
    - "ORCHESTRATION_WORKTRACKER.md"
    - "ORCHESTRATION.yaml"

  cross_session_portable: true
  ephemeral_references: false
```

**Template-specific findings:**

1. The template has the identical 5-field structure as PROJ-001. No additional fields are defined even as commented-out examples or optional expansions.
2. File paths use relative names without project prefix, which is correct for a template but means the orchestrator must resolve paths at runtime.
3. There is no guidance comment explaining when or how to update the resumption section during execution.
4. The `checkpoints:` section in the template (lines 224-233) defines the checkpoint schema but has no linkage to the resumption section -- they are independent data structures with no cross-reference protocol.

### Structural Comparison

| Aspect | PROJ-001 (Completed) | Template (Initial) | Gap |
|--------|---------------------|--------------------|----|
| Fields defined | 5 | 5 | Same -- no evolution during workflow |
| Quality data | Scores embedded in prose | None | No structured quality tracking |
| Compaction tracking | None | None | No field exists |
| Decision log | None | None | No field exists |
| Agent context | None | None | No field exists |
| Update protocol | None documented | None documented | No guidance on when to update |
| Context fill level | None | None | No field exists |
| Defect accumulation | None | None | No field exists |

---

## Gap Analysis

### RG-1: No Accumulated Defect Context

**Severity: CRITICAL**

**Current state:** Quality gate iteration findings are recorded in `quality_gates.{id}.iteration_history[].primary_defect` and strategy sub-fields within the full ORCHESTRATION.yaml. The resumption section contains zero references to these findings.

**Evidence from PROJ-001:** QG-1 had 6 major findings in iteration 1, 3 in iteration 2, before passing in iteration 3. QG-2 iter 1 found a copyright holder inconsistency (DA-001) that required cross-phase revision. QG-3 iter 1 found a shebang roster mismatch between two agents. None of these defect patterns appear in the resumption section.

**Impact of the gap:** A new session resuming mid-workflow (e.g., after compaction during QG-2) would not know:
- What defects were already found and fixed in prior gates
- What recurring patterns exist (e.g., evidence quality consistently scoring lowest)
- What cross-phase revisions were applied that affect downstream phases

**Risk:** The resumed session could re-introduce previously fixed defects, waste gate iterations re-discovering known issues, or produce output that contradicts prior revisions. For a C2 workflow this wastes tokens; for a C3+ workflow with all strategies, it could cascade into gate failures.

**What is needed:** A `defect_summary` sub-section in resumption that accumulates the primary defects and their resolutions from each completed gate iteration.

---

### RG-2: No Inter-Phase Decision Log

**Severity: HIGH**

**Current state:** Decisions made during orchestration execution are not recorded in the resumption section. The PROJ-001 ORCHESTRATION.yaml records revision actions within `iteration_history[].revisions_applied` (QG-2 iter 1 shows 3 revisions), but these are buried inside the quality gate data structure, not surfaced for resumption.

**Evidence from PROJ-001:** QG-2 iteration 1 discovered DA-001 (copyright holder inconsistency between NOTICE and header_template). The resolution -- "Aligned Phase 3 header_template to 'Adam Nowak' (matches NOTICE)" -- was a cross-phase decision that affected Phase 3 execution. This decision is only visible by parsing `quality_gates.qg-2.iteration_history[0].revisions_applied`.

**Impact of the gap:** A session resuming before Phase 3 would not know that the header template was changed during QG-2 revision. It might use the original template from the ORCHESTRATION_PLAN, re-introducing the inconsistency.

**What is needed:** A `decisions` sub-section that records orchestration-time decisions with their rationale and cross-phase impacts.

---

### RG-3: No Compaction Event Records

**Severity: MEDIUM (upgrading to HIGH when integrated with detection system)**

**Current state:** No field in the resumption section records whether compaction occurred, when it occurred, or what context was likely lost. The Phase 2 analysis predicts two compaction events for a single-session FEAT-015 run (at Steps 9 and 17), but no mechanism exists to record them.

**Evidence:** The `checkpoints:` section records phase-level checkpoints (CP-001 through CP-003) triggered by `GATE_PASS` events, but no checkpoint is triggered by compaction. The resumption section does not reference the checkpoints section except via `last_checkpoint`.

**Impact of the gap:** A post-compaction session cannot distinguish between "I am a fresh session that was asked to resume" and "I am the same session that just lost context due to compaction." The behavioral response should differ: a fresh session needs full re-orientation, while a compacted session retains some context and needs targeted re-orientation of what was lost.

**What is needed:** A `compaction_events` sub-section that records each compaction event with timestamp, estimated fill level at trigger, trigger type (auto/manual), and what orchestration state was active at the time.

---

### RG-4: Missing Quality Score Trajectory

**Severity: MEDIUM**

**Current state:** The resumption `current_state` field in PROJ-001 includes final scores as prose: "QG-1: 0.941, QG-2: 0.9505, QG-3: 0.935, QG-Final: 0.9335". The full iteration trajectory (QG-1: 0.825 -> 0.916 -> 0.941) is only in the `quality_gates` section.

**Evidence from PROJ-001:** QG-1 required 3 iterations to pass. The trajectory 0.825 -> 0.916 -> 0.941 shows steady improvement. QG-2 showed an unusual pattern: 0.960 -> 0.951 (score decreased but status changed from REVISE to PASS because the S-007 constitutional check improved). This nuance is invisible in the resumption section.

**Impact of the gap:** A resuming session that needs to run additional QG iterations (e.g., after a gate failure mid-iteration) cannot see the score trend without parsing the full quality_gates section. The trend matters: a score moving 0.825 -> 0.916 suggests the approach is converging; a score moving 0.92 -> 0.88 suggests a regression that may need a different strategy.

**What is needed:** A `quality_trajectory` sub-section with structured per-gate score arrays.

---

### RG-5: No Agent-Specific Context

**Severity: HIGH**

**Current state:** The resumption section does not record what each agent produced, what its key findings were, or what context it consumed. Agent outputs are referenced only via artifact paths in the `pipelines` section.

**Evidence from PROJ-001:** The `audit-executor` agent produced a 26,356-byte dependency audit with specific findings (MPL-2.0 legal reasoning, pip-licenses double-counting). The `header-applicator` modified 403 files. The `header-verifier` independently confirmed 100% coverage. None of these agent-level summaries are accessible from the resumption section.

**Impact of the gap:** A session resuming between Phase 2 and Phase 3 would need to read the Phase 1 audit artifact (6,589 tokens) and Phase 2 artifacts (various sizes) to understand what happened. With context at 60%+ fill, loading these artifacts may push the session toward compaction before it can start new work.

**What is needed:** An `agent_summaries` sub-section with one-line summaries of each completed agent's key output, sufficient for a resuming session to understand prior work without loading the full artifacts.

---

### RG-6: Resumption Section is Static

**Severity: CRITICAL**

**Current state:** The resumption section appears to be written once at planning time and updated only at workflow completion. In PROJ-001, the section reads as a final status report, not a dynamic recovery document. The template's resumption section is identical in structure, confirming that no incremental update protocol exists.

**Evidence:** Comparing PROJ-001's resumption section to its checkpoint entries:
- CP-001 (QG-1 PASS): No corresponding resumption update
- CP-002 (QG-2 PASS): No corresponding resumption update
- CP-003 (QG-3 PASS): No corresponding resumption update
- Final state: Resumption updated to "WORKFLOW COMPLETE"

The resumption section jumped from "not started" to "complete" with no intermediate states recorded. If a session had crashed during Phase 3, the resumption section would still say "not started" or whatever it was last set to.

**Impact of the gap:** This is the root cause of all other gaps. If the resumption section were updated at each checkpoint, it would naturally accumulate defect context (RG-1), decisions (RG-2), quality trajectory (RG-4), and agent summaries (RG-5). The static nature means ALL resumption intelligence is lost.

**What is needed:** An explicit **resumption update protocol** -- a defined set of triggers and corresponding update actions that the orchestrator MUST perform at each state transition.

---

## Enhanced Resumption Schema

### Proposed YAML Schema (v2.0)

The enhanced resumption section replaces the existing 5-field structure with 7 sub-sections containing 23 fields total. All new fields are designed for auto-population by the orchestrator during execution.

```yaml
# =============================================================================
# RESUMPTION CONTEXT (v2.0 — Context-Resilient)
# =============================================================================
# UPDATE PROTOCOL: This section MUST be updated at every state transition:
#   - Phase start/complete
#   - Quality gate iteration (each iteration, not just final)
#   - Compaction event (via PreCompact hook)
#   - Decision that affects downstream phases
#   - Agent completion
# The orchestrator is responsible for updates. The PreCompact hook additionally
# writes a checkpoint file (see checkpoint_data_design).
resumption:

  # --- 1. Recovery State (replaces original fields) ---
  last_checkpoint: "CP-002"                     # Most recent checkpoint ID
  current_phase: 3                              # Numeric phase index (machine-readable)
  current_phase_name: "Source File SPDX Header Notices"  # Human-readable
  workflow_status: "ACTIVE"                     # ACTIVE | PAUSED | COMPLETE | FAILED
  current_activity: "phase-3-agent-execution"   # What was happening: phase-N-agent-execution |
                                                # qg-N-iteration-M | compaction-recovery | idle
  next_step: "Execute header-applicator agent for EN-932"
  context_fill_at_update: 0.642                 # Fill % when this section was last updated
  updated_at: "2026-02-17T12:34:56Z"           # Timestamp of last resumption update

  # --- 2. Files to Read (enhanced with priority and purpose) ---
  files_to_read:
    - path: "projects/PROJ-001-oss-release/ORCHESTRATION.yaml"
      priority: 1                               # Load order (1 = first)
      purpose: "Machine-readable workflow state. Read resumption section first."
      sections: ["resumption", "quality_gates.{current_gate}", "next_actions"]
    - path: "projects/PROJ-001-oss-release/ORCHESTRATION_PLAN.md"
      priority: 2
      purpose: "Strategic context. Agent definitions, phase descriptions, risk mitigations."
      sections: ["agent-registry", "phase-{current_phase}"]
    - path: "projects/PROJ-001-oss-release/WORKTRACKER.md"
      priority: 3
      purpose: "Tactical documentation. Feature status, blockers, history."
      sections: ["features", "history"]

  # --- 3. Quality Trajectory (structured, not prose) ---
  quality_trajectory:
    gates_completed: ["qg-1", "qg-2"]
    gates_remaining: ["qg-3", "qg-final"]
    current_gate: null                          # null if between gates, gate ID if in-progress
    current_gate_iteration: null                # Iteration number within current gate
    score_history:
      qg-1: [0.825, 0.916, 0.941]              # Array of scores per iteration
      qg-2: [0.960, 0.951]
    lowest_dimension: "evidence_quality"         # Recurring weak dimension across gates
    total_iterations_used: 5                    # Sum of all gate iterations
    total_iterations_budget: 12                 # Sum of max_iterations across all gates

  # --- 4. Defect Summary (accumulated across gates) ---
  defect_summary:
    total_defects_found: 14                     # Major + critical across all iterations
    total_defects_resolved: 14
    unresolved_defects: []                      # List of still-open defect IDs
    recurring_patterns:
      - pattern: "Evidence quality gaps (missing URLs, unattached artifacts)"
        gates_affected: ["qg-1", "qg-2"]
        resolution: "Added source URLs and attached raw data artifacts"
      - pattern: "Cross-artifact consistency (counts, names)"
        gates_affected: ["qg-1", "qg-3"]
        resolution: "Reconciliation sections added to deliverables"
    last_gate_primary_defect: null              # Primary defect from most recent gate iteration

  # --- 5. Decision Log (cross-phase decisions made during execution) ---
  decisions:
    - id: "RD-001"
      gate: "qg-2"
      iteration: 1
      decision: "Align copyright holder to 'Adam Nowak' across NOTICE, header_template, and ORCHESTRATION_PLAN"
      rationale: "DA-001 found inconsistency. NOTICE is authoritative source."
      affects_phases: [3]                       # Phase numbers affected by this decision
      applied: true
    - id: "RD-002"
      gate: "qg-2"
      iteration: 1
      decision: "Defer README MIT reference fix to post-migration cleanup"
      rationale: "DA-002 identified split-license state in README. Branch isolation means this is not a blocking issue for migration."
      affects_phases: []
      applied: false                            # Deferred -- not yet applied

  # --- 6. Agent Summaries (one-line per completed agent) ---
  agent_summaries:
    audit-executor: "PASS. All 25 deps Apache-2.0 compatible. MPL-2.0 (certifi) compatible via Exhibit B. No blockers."
    license-replacer: "DONE. LICENSE file replaced with canonical Apache 2.0 text. SHA-256 verified."
    notice-creator: "DONE. NOTICE file created per Section 4(d). Copyright: 2026 Adam Nowak."
    metadata-updater: "DONE. pyproject.toml license field set to Apache-2.0 (SPDX). No other license refs."
    # Agents not yet executed are omitted, not listed as null

  # --- 7. Compaction Events (populated by PreCompact hook + orchestrator) ---
  compaction_events:
    count: 0
    events: []
    # Example populated entry:
    # - id: "CX-001"
    #   timestamp: "2026-02-17T11:45:00Z"
    #   trigger: "auto"                         # auto | manual
    #   estimated_fill_before: 0.886            # Fill % just before compaction
    #   active_phase: 2
    #   active_gate: "qg-2"
    #   active_gate_iteration: 1
    #   checkpoint_file: ".jerry/checkpoints/cx-001-checkpoint.json"
    #   acknowledged: false                     # Set true after LLM processes re-orientation
```

### Schema Field Summary

| Sub-section | Fields | Auto-populated? | Update Trigger |
|-------------|--------|-----------------|----------------|
| Recovery State | 8 | Yes (orchestrator) | Every state transition |
| Files to Read | 3 entries (structured) | Yes (planner at init, orchestrator updates sections) | Phase transitions |
| Quality Trajectory | 7 | Yes (orchestrator after each gate iteration) | Gate iteration complete |
| Defect Summary | 5 | Yes (orchestrator after each gate iteration) | Gate iteration complete |
| Decision Log | N entries | Semi-auto (orchestrator records, may need human input for rationale) | When cross-phase revision applied |
| Agent Summaries | N entries | Yes (orchestrator after agent completes) | Agent completion |
| Compaction Events | 2 + N entries | Yes (PreCompact hook writes, orchestrator updates `acknowledged`) | Compaction event |

### Backward Compatibility

The enhanced schema is a **superset** of the current schema. Existing fields (`last_checkpoint`, `next_step`, `files_to_read`, `cross_session_portable`, `ephemeral_references`) are preserved. `current_state` is replaced by the structured `current_phase`, `current_phase_name`, `workflow_status`, and `current_activity` fields, which provide the same information in machine-readable form.

A v1.0 resumption reader that only knows the original 5 fields will still find `last_checkpoint`, `next_step`, and `files_to_read` at their expected locations. New sub-sections are additive.

---

## Checkpoint Data Design

### Checkpoint File vs. Resumption Section

Two distinct but complementary persistence mechanisms:

| Mechanism | Purpose | Written By | When | Location |
|-----------|---------|------------|------|----------|
| `resumption:` in ORCHESTRATION.yaml | Authoritative recovery state for planned session boundaries | Orchestrator | Every state transition | In-place update of ORCHESTRATION.yaml |
| Checkpoint file (`.jerry/checkpoints/`) | Emergency state snapshot for unplanned compaction | PreCompact hook | Compaction imminent | Separate JSON file |

The checkpoint file exists because the PreCompact hook cannot reliably update ORCHESTRATION.yaml (it runs as a side-effect script with no YAML parsing/serialization guarantee). Instead, it writes a lightweight JSON file that the post-compaction re-orientation prompt instructs the LLM to read and merge into the resumption section.

### Checkpoint File Format

**Path pattern:** `.jerry/checkpoints/{event-id}-checkpoint.json`

**Example:** `.jerry/checkpoints/cx-001-checkpoint.json`

```json
{
  "schema_version": "1.0.0",
  "event_type": "compaction",
  "event_id": "cx-001",
  "timestamp": "2026-02-17T11:45:00Z",

  "trigger": {
    "type": "auto",
    "source": "PreCompact hook"
  },

  "context_state": {
    "estimated_fill_before_compaction": 0.886,
    "estimated_tokens_used": 177200,
    "context_window_size": 200000,
    "source": "transcript_heuristic"
  },

  "orchestration_state": {
    "workflow_id": "feat015-licmig-20260217-001",
    "workflow_status": "ACTIVE",
    "current_phase": 2,
    "current_phase_name": "Core License Changes",
    "current_activity": "qg-2-iteration-1",
    "last_completed_checkpoint": "CP-001",
    "phases_complete": [1],
    "phases_in_progress": [2],
    "phases_remaining": [3, 4],
    "current_gate": "qg-2",
    "current_gate_iteration": 1,
    "current_gate_score": 0.960
  },

  "accumulated_context": {
    "defect_patterns": [
      "Evidence quality gaps (missing URLs, unattached artifacts)",
      "Cross-artifact consistency (counts, names)"
    ],
    "decisions_since_last_checkpoint": [
      {
        "id": "RD-001",
        "summary": "Align copyright holder to 'Adam Nowak' across all files",
        "affects_phases": [3]
      }
    ],
    "agent_summaries": {
      "audit-executor": "PASS. All 25 deps Apache-2.0 compatible."
    }
  },

  "recovery_instructions": {
    "files_to_read": [
      {
        "path": "projects/PROJ-001-oss-release/ORCHESTRATION.yaml",
        "sections": ["resumption", "quality_gates.qg-2", "next_actions"],
        "priority": 1
      }
    ],
    "next_action": "Read ORCHESTRATION.yaml resumption section. Merge this checkpoint data. Continue qg-2 iteration 1 (re-read deliverables and re-score).",
    "critical_context": "QG-2 was scoring 3 deliverables. Score reached 0.960 but S-007 found 1 major finding (DA-001: copyright inconsistency). Revision was in progress when compaction occurred."
  },

  "metadata": {
    "written_by": "PreCompact hook (context-monitor.py)",
    "acknowledged": false,
    "acknowledged_at": null
  }
}
```

### Checkpoint Data Source Mapping

How each checkpoint field is populated:

| Checkpoint Field | Data Source | Available to PreCompact Hook? |
|------------------|------------|------------------------------|
| `estimated_fill_before_compaction` | Last `<context-monitor>` injection from Method A | Yes -- read from `.jerry/context-monitor-state.json` (written by UserPromptSubmit hook on every prompt) |
| `workflow_id`, `workflow_status` | ORCHESTRATION.yaml header | Yes -- parse YAML file |
| `current_phase`, `current_activity` | ORCHESTRATION.yaml `resumption.current_phase` / `resumption.current_activity` | Yes -- requires resumption section to be kept current (circular dependency resolved by the update protocol) |
| `last_completed_checkpoint` | ORCHESTRATION.yaml `checkpoints.latest_id` | Yes -- parse YAML |
| `current_gate`, `current_gate_iteration`, `current_gate_score` | ORCHESTRATION.yaml `quality_gates.{id}` | Yes -- parse YAML for latest in-progress gate |
| `defect_patterns` | ORCHESTRATION.yaml `resumption.defect_summary.recurring_patterns` | Yes -- requires enhanced resumption schema |
| `decisions_since_last_checkpoint` | ORCHESTRATION.yaml `resumption.decisions` (filtered by timestamp > last checkpoint) | Yes -- requires enhanced resumption schema |
| `agent_summaries` | ORCHESTRATION.yaml `resumption.agent_summaries` | Yes -- requires enhanced resumption schema |
| `recovery_instructions` | Template-based generation from orchestration state | Yes -- deterministic from state |

**Key dependency:** The checkpoint file's richness depends on the resumption section being kept current (per the update protocol). If the resumption section is stale (the RG-6 problem), the checkpoint file will also be stale. This is why the update protocol is the foundational fix -- it enables both the resumption section AND the checkpoint file to carry useful data.

### Checkpoint File Lifecycle

```
1. PreCompact hook fires
2. Hook reads ORCHESTRATION.yaml resumption section
3. Hook reads .jerry/context-monitor-state.json for fill data
4. Hook writes .jerry/checkpoints/cx-{NNN}-checkpoint.json
5. Compaction occurs (context is compressed)
6. Next user prompt triggers UserPromptSubmit hook
7. Hook detects checkpoint file (created after last acknowledged checkpoint)
8. Hook injects <compaction-alert> with checkpoint file path
9. LLM reads checkpoint file via Read tool
10. LLM merges checkpoint data into ORCHESTRATION.yaml resumption section
11. LLM sets checkpoint acknowledged=true
12. LLM continues work with re-oriented context
```

---

## Integration with Detection System

### How Hybrid A+B Triggers Resumption Updates

The Phase 3 detection evaluation designed a Hybrid A+B system with four threshold levels. Each threshold level maps to specific resumption actions:

| Detection Level | Fill % | Resumption Action |
|-----------------|--------|-------------------|
| LOW | 0-60% | No resumption action. Normal execution. Orchestrator updates resumption section at standard triggers (phase/gate transitions). |
| WARNING | 60-80% | Orchestrator SHOULD update resumption section immediately (even if not at a standard trigger). Ensures resumption data is fresh in case of unexpected compaction. |
| CRITICAL | 80-90% | Orchestrator MUST write a full resumption update AND verify all sub-sections are current. This is the "prepare for session handoff" signal. If mid-QG-iteration, complete current iteration then checkpoint. |
| COMPACTION | 90%+ / PreCompact fires | PreCompact hook writes checkpoint file. No orchestrator action possible (compaction is imminent). Post-compaction, UserPromptSubmit injects re-orientation. |

### Injection Format Integration

The Phase 3 `<context-monitor>` tag is extended to include resumption state awareness:

```xml
<context-monitor>
CONTEXT STATUS: WARNING (73.2% filled)
Tokens used: 146,400 / 200,000
Estimated remaining: 53,600 tokens (~1.8 QG iterations)
Compaction events: 0
Last checkpoint: CP-001
Resumption last updated: 2026-02-17T11:30:00Z (23 min ago)
Resumption staleness: FRESH (updated within current phase)

ACTION RECOMMENDED:
- Update ORCHESTRATION.yaml resumption section with current state
- Ensure defect_summary and agent_summaries are current
</context-monitor>
```

The `Resumption staleness` field compares the `resumption.updated_at` timestamp against the current time and the current phase. If the resumption section has not been updated since the current phase started, it is flagged as STALE, prompting the orchestrator to update.

### Post-Compaction Re-Orientation Flow

When the `UserPromptSubmit` hook detects a checkpoint file after compaction:

```xml
<compaction-alert>
COMPACTION DETECTED. Context was compressed.
Checkpoint file: .jerry/checkpoints/cx-001-checkpoint.json

IMMEDIATE ACTIONS:
1. Read the checkpoint file above using the Read tool
2. Read ORCHESTRATION.yaml resumption section
3. Merge checkpoint data into resumption section if checkpoint is newer
4. Identify what you were doing (checkpoint.orchestration_state.current_activity)
5. Resume from that point, using recovery_instructions.next_action

CRITICAL CONTEXT FROM CHECKPOINT:
- You were in: Phase 2, QG-2 iteration 1
- Last score: 0.960 (S-007 found 1 major finding)
- Decision pending: RD-001 copyright alignment affects Phase 3
</compaction-alert>
```

The `CRITICAL CONTEXT FROM CHECKPOINT` section is populated by the UserPromptSubmit hook reading the checkpoint file's `accumulated_context` and `recovery_instructions.critical_context` fields. This gives the LLM the most important context immediately, without requiring it to read the full checkpoint file first (though it should still read it for completeness).

---

## WORKTRACKER.md as Resumption Aid

### Current State Assessment

Source: `projects/PROJ-004-context-resilience/WORKTRACKER.md`

The PROJ-004 WORKTRACKER.md contains:

| Section | Content | Resumption Utility |
|---------|---------|-------------------|
| Summary | Project name, status, created date | LOW -- too high-level for session recovery |
| Epics | Single row: EPIC-001 Context Resilience, in_progress | LOW -- links to epic file but no detail |
| Decisions | Empty (no decisions recorded) | NONE |
| History | 2 entries: project creation and SPIKE-001 start | MEDIUM -- provides temporal context |

### Gap Assessment for Resumption

**Strengths:**
1. WORKTRACKER.md provides a stable entry point that persists across sessions
2. The History section records session-level events with dates
3. The Epics table links to detailed work items

**Gaps for session recovery:**

| Gap | Impact | Severity |
|-----|--------|----------|
| No in-progress activity detail | A resuming session sees "in_progress" but not WHAT is in progress at the task level | HIGH |
| No context about last session | No record of what the previous session accomplished, what it was doing when it ended, or why it ended | HIGH |
| No link to ORCHESTRATION.yaml | The WORKTRACKER does not reference the orchestration state file, so a resuming session following WORKTRACKER alone would miss the SSOT | MEDIUM |
| No blocker/issue tracking | Active blockers are not surfaced in WORKTRACKER | LOW (for PROJ-004 which has none) |

**Assessment:** WORKTRACKER.md is not designed for session resumption -- it is designed for project tracking. It answers "what is the project status?" not "where did I leave off and what do I need to know?" These are different questions. The ORCHESTRATION.yaml resumption section is the correct location for session recovery data. WORKTRACKER.md should link TO the orchestration state but not duplicate it.

**Recommendation:** Add a `Last Orchestration` field to the WORKTRACKER Summary table that points to the active ORCHESTRATION.yaml, so a session starting from WORKTRACKER can immediately navigate to the resumption section.

---

## Open Questions

### For Phase 5 (Prompt Template Design)

| ID | Question | Why It Matters |
|----|----------|----------------|
| OQ-R1 | What is the maximum token budget for the `<compaction-alert>` injection? | The alert must be concise enough to not significantly impact post-compaction context, but detailed enough for reliable re-orientation. Phase 3 budgeted <200 tokens for WARNING+ injections. The compaction alert with checkpoint summary may need 300-500 tokens. |
| OQ-R2 | Should the prompt template instruct the LLM to read the FULL ORCHESTRATION.yaml or ONLY the resumption section? | The full YAML for PROJ-001 is ~7,500 tokens. If post-compaction context is ~50K tokens (25% of window), the YAML alone consumes 15% of remaining space. Reading only the resumption section (~1,500 tokens with enhanced schema) is much cheaper. |
| OQ-R3 | How should the orchestrator handle the case where compaction occurs during a QG iteration BETWEEN strategy executions? | Example: S-014 scored at 0.92, S-007 is running, compaction occurs. Should the resumed session re-run S-014, or trust the score from the checkpoint? This is a policy question that the prompt template must address. |
| OQ-R4 | Should the resumption update protocol be enforced by the orchestrator prompt template or by a hook-based check? | Enforcement via prompt template is vulnerable to context rot (the very problem we are solving). Enforcement via a hook (e.g., PostToolUse checking if ORCHESTRATION.yaml was recently updated) is immune but more complex. |
| OQ-R5 | What is the minimum resumption section content that enables reliable re-orientation in under 3 prompts? | The "3 prompts" target is a design goal -- a resumed session should be productive by its 3rd prompt. This constrains how much data the resumption section should contain (enough for orientation, not so much that it takes multiple reads). |

---

## Self-Review Checklist

- [x] PROJ-001 resumption section analyzed with specific evidence (lines 638-649, all 5 fields assessed, comparison with checkpoint entries CP-001 through CP-003)
- [x] All 6 RG gaps assessed with severity ratings (2 CRITICAL, 2 HIGH, 2 MEDIUM)
- [x] Enhanced schema is concrete YAML format (23 fields across 7 sub-sections, complete with example values and data types)
- [x] Checkpoint data design is specific enough for Phase 5 to build a prompt template (full JSON example with field-level source mapping and lifecycle flowchart)
- [x] Integration with Hybrid A+B detection is explicit (threshold-to-action mapping, injection format extension, post-compaction re-orientation flow)
- [x] WORKTRACKER.md assessed as resumption aid with specific gaps identified
- [x] L0/L1/L2 present (L0 Summary, L1 gap analysis and WORKTRACKER assessment, L2 schema design and checkpoint format)
- [x] H-23/H-24 navigation table with anchor links present
- [x] Limitations disclosed: enhanced schema depends on update protocol being followed (context rot vulnerability); checkpoint file richness is circular dependency on resumption section freshness; token budget for post-compaction injection is estimated not measured

---

## References

| # | Source | Path | Content Used |
|---|--------|------|-------------|
| 1 | PROJ-001 ORCHESTRATION.yaml | `projects/PROJ-001-oss-release/ORCHESTRATION.yaml` | Resumption section (lines 638-649), quality gates iteration history, checkpoint entries, metrics |
| 2 | ORCHESTRATION template | `skills/orchestration/templates/ORCHESTRATION.template.yaml` | Template resumption section (lines 300-311), checkpoint schema (lines 224-233) |
| 3 | Phase 2: Run Analysis | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-2-analysis/run-analyzer/run-analysis.md` | RG-1 through RG-6 gap definitions, cumulative fill projection, token budget estimates |
| 4 | Phase 3: Detection Evaluation | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-3-detection/detection-evaluator/detection-evaluation.md` | Hybrid A+B architecture, threshold levels, `<context-monitor>` injection format, PreCompact hook design |
| 5 | PROJ-004 WORKTRACKER.md | `projects/PROJ-004-context-resilience/WORKTRACKER.md` | Current project tracking structure, history entries |
| 6 | Quality Enforcement SSOT | `.context/rules/quality-enforcement.md` | H-13 threshold, H-14 iteration cycles, S-014 dimensions |
