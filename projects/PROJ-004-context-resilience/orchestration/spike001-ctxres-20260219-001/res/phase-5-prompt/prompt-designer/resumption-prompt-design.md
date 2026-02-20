# Resumption Prompt Design

<!-- PS-ID: SPIKE-001 | ENTRY-ID: phase-5-prompt | DATE: 2026-02-19 -->
<!-- AGENT: ps-architect v2.2.0 (prompt-designer) | MODEL: claude-opus-4-6 -->

> Concrete prompt templates enabling Claude to self-orient from persistent state after context
> exhaustion. Two templates: (1) new-session resumption prompt, (2) same-session compaction alert.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Summary](#l0-summary) | Design overview and key decisions |
| [Template 1: Resumption Prompt](#template-1-resumption-prompt) | New session start after context exhaustion |
| [Template 2: Compaction Alert](#template-2-compaction-alert) | Same-session post-compaction re-orientation |
| [Variable Specification](#variable-specification) | All placeholders mapped to data sources |
| [Open Question Resolutions](#open-question-resolutions) | OQ-R1 through OQ-R5 answered |
| [Mental Test: PROJ-001](#mental-test-proj-001) | Validation against real workflow at two compaction points |
| [Integration Notes](#integration-notes) | How templates connect to detection and checkpoint systems |
| [Self-Review Checklist](#self-review-checklist) | S-010 compliance verification |
| [References](#references) | Sources |

---

## L0 Summary

**Design Decision:** Two distinct prompt templates for two distinct resumption scenarios, both structured to achieve productive work within 2-3 prompts of injection.

**Template 1 (Resumption Prompt)** is injected by the operator (or an automation layer) when starting a new Claude Code session to continue a workflow that was interrupted by context exhaustion or a deliberate session boundary. It is a `system-reminder` style injection at ~750 tokens that provides the full recovery context: checkpoint state, file read instructions with priority ordering, key decisions, quality trajectory, and the exact next action. The resuming session reads 2-3 files (resumption section of ORCHESTRATION.yaml first, then targeted sections of ORCHESTRATION_PLAN.md) and is productive by prompt 3.

**Template 2 (Compaction Alert)** is injected automatically by the `UserPromptSubmit` hook after detecting a checkpoint file written by the `PreCompact` hook. It is a `<compaction-alert>` XML tag at ~300 tokens that tells the in-session Claude what happened (compaction), what was lost (conversation history compressed), and what to do (read checkpoint file, merge data, continue from the interrupted operation). This template is smaller because the session retains some context -- it needs re-orientation, not full re-introduction.

**Key Design Principles:**

1. **Resumption section first, not full ORCHESTRATION.yaml.** The enhanced resumption schema (v2.0, Phase 4) is ~1,500 tokens. The full ORCHESTRATION.yaml is ~7,500 tokens. Reading only the resumption section saves ~6,000 tokens (3% of the 200K window), which is meaningful when context is already under pressure.

2. **Structured read instructions, not free-form.** Both templates specify exactly which files to read, in what order, and which sections within each file. This prevents the resumed session from loading unnecessary content.

3. **Self-contained context.** Both templates embed the most critical checkpoint data directly (current phase, next action, last score, key decisions), so Claude can begin reasoning immediately. File reads fill in detail, not the foundation.

4. **Deterministic over vulnerable.** Template 2 (compaction alert) is injected by a hook (immune to context rot). Template 1 (resumption prompt) is injected at session start before any context accumulation. Neither template relies on the LLM remembering to do something -- the injection mechanism forces the information into context.

---

## Template 1: Resumption Prompt

### Purpose

Injected when an operator starts a new Claude Code session to continue a workflow that was interrupted. The interruption cause may be context exhaustion (compaction made the previous session unproductive), a deliberate session boundary (operator chose to split work), or an unexpected crash.

### Injection Mechanism

The operator pastes this as the first user message in the new session, OR it is injected via an automation layer that reads the checkpoint file and populates the variables. In the future, a `SessionStart` hook could auto-inject this by detecting an unacknowledged checkpoint file.

### Template

```
You are resuming a workflow that was interrupted. Do NOT start over. Your goal is to
continue from the exact point of interruption using the persistent state below.

WORKFLOW: {WORKFLOW_ID}
PROJECT: {PROJECT_ID}
ORCHESTRATION PLAN: {ORCHESTRATION_PLAN_PATH}

RECOVERY STATE:
- Current phase: Phase {CURRENT_PHASE} ({CURRENT_PHASE_NAME})
- Workflow status: {WORKFLOW_STATUS}
- Last activity: {CURRENT_ACTIVITY}
- Last checkpoint: {LAST_CHECKPOINT}
- Context fill at interruption: {CONTEXT_FILL_AT_CHECKPOINT}%
- Compaction events in previous session: {COMPACTION_COUNT}

NEXT ACTION: {NEXT_ACTION}

QUALITY TRAJECTORY:
- Gates completed: {GATES_COMPLETED}
- Gates remaining: {GATES_REMAINING}
- Current gate: {CURRENT_GATE} (iteration {CURRENT_GATE_ITERATION})
- Last gate score: {LAST_GATE_SCORE}
- Recurring weak dimension: {LOWEST_DIMENSION}

KEY DECISIONS (carry forward):
{DECISIONS_BLOCK}

AGENT WORK COMPLETED:
{AGENT_SUMMARIES_BLOCK}

DEFECT PATTERNS (avoid re-introducing):
{DEFECT_PATTERNS_BLOCK}

READ THESE FILES IN ORDER:
1. [PRIORITY 1] {FILE_1_PATH}
   Sections: {FILE_1_SECTIONS}
   Purpose: {FILE_1_PURPOSE}
2. [PRIORITY 2] {FILE_2_PATH}
   Sections: {FILE_2_SECTIONS}
   Purpose: {FILE_2_PURPOSE}
3. [PRIORITY 3] {FILE_3_PATH}
   Sections: {FILE_3_SECTIONS}
   Purpose: {FILE_3_PURPOSE}

AFTER READING:
1. Confirm you understand the current workflow state
2. Identify what phase/step to continue from
3. Proceed with: {NEXT_ACTION}

Do NOT re-read artifacts from completed phases unless specifically needed for the current
task. Minimize context consumption -- you are resuming mid-workflow and context budget
is limited.
```

### Token Budget Analysis

| Section | Estimated Tokens | Notes |
|---------|-----------------|-------|
| Fixed instruction text | ~200 | Framing, rules, after-reading instructions |
| Recovery state block | ~80 | 8 fields with values |
| Quality trajectory block | ~60 | 5 fields with values |
| Decisions block (2-3 decisions) | ~120 | ~40 tokens per decision |
| Agent summaries (4-6 agents) | ~100 | ~15-20 tokens per agent summary |
| Defect patterns (2-3 patterns) | ~80 | ~25-30 tokens per pattern |
| File read instructions (3 files) | ~120 | Path + sections + purpose per file |
| **Total** | **~760** | Within 500-1000 target |

### Populated Example (PROJ-001 at QG-2 Compaction Point)

```
You are resuming a workflow that was interrupted. Do NOT start over. Your goal is to
continue from the exact point of interruption using the persistent state below.

WORKFLOW: feat015-licmig-20260217-001
PROJECT: PROJ-001-oss-release
ORCHESTRATION PLAN: projects/PROJ-001-oss-release/ORCHESTRATION_PLAN.md

RECOVERY STATE:
- Current phase: Phase 2 (Core License Changes)
- Workflow status: ACTIVE
- Last activity: qg-2-iteration-1
- Last checkpoint: CP-001
- Context fill at interruption: 88.6%
- Compaction events in previous session: 1

NEXT ACTION: Continue QG-2 iteration 1. Re-read the 3 Phase 2 deliverables and re-score
with S-014, S-007, S-002. The previous scoring reached 0.960 but S-007 found 1 major
finding (DA-001: copyright holder inconsistency). Apply revision, then re-score.

QUALITY TRAJECTORY:
- Gates completed: qg-1
- Gates remaining: qg-2, qg-3, qg-final
- Current gate: qg-2 (iteration 1)
- Last gate score: 0.960 (qg-2 iter 1, pre-revision)
- Recurring weak dimension: evidence_quality

KEY DECISIONS (carry forward):
- RD-001 (qg-2, iter 1): Align copyright holder to 'Adam Nowak' across NOTICE,
  header_template, and ORCHESTRATION_PLAN. NOTICE is authoritative. Affects Phase 3.

AGENT WORK COMPLETED:
- audit-executor: PASS. All 25 deps Apache-2.0 compatible. MPL-2.0 (certifi) compatible
  via Exhibit B. No blockers.
- license-replacer: DONE. LICENSE file replaced with canonical Apache 2.0. SHA-256 verified.
- notice-creator: DONE. NOTICE file created per Section 4(d). Copyright: 2026 Adam Nowak.
- metadata-updater: DONE. pyproject.toml license = Apache-2.0 (SPDX). No other refs.

DEFECT PATTERNS (avoid re-introducing):
- Evidence quality gaps: missing source URLs and unattached artifacts (qg-1, qg-2)
- Cross-artifact consistency: counts and names mismatched between deliverables (qg-1)

READ THESE FILES IN ORDER:
1. [PRIORITY 1] projects/PROJ-001-oss-release/ORCHESTRATION.yaml
   Sections: resumption, quality_gates.qg-2, next_actions
   Purpose: Machine-readable workflow state. Read resumption section first for full
   recovery context including enhanced schema data.
2. [PRIORITY 2] projects/PROJ-001-oss-release/ORCHESTRATION_PLAN.md
   Sections: agent-registry, phase-2
   Purpose: Strategic context. Agent definitions and Phase 2 description for
   understanding current work.
3. [PRIORITY 3] projects/PROJ-001-oss-release/WORKTRACKER.md
   Sections: features, history
   Purpose: Tactical documentation. Feature status and session history.

AFTER READING:
1. Confirm you understand the current workflow state
2. Identify what phase/step to continue from
3. Proceed with: Continue QG-2 iteration 1. Re-read the 3 Phase 2 deliverables and
   re-score with S-014, S-007, S-002. Apply DA-001 revision first.

Do NOT re-read artifacts from completed phases unless specifically needed for the current
task. Minimize context consumption -- you are resuming mid-workflow and context budget
is limited.
```

**Populated example token count:** ~480 tokens (measured by character count / 4). The variable-expanded version is well within the 500-1000 token budget. The populated example is at the lower end because PROJ-001 at the QG-2 point has relatively few decisions and agents completed. A later-stage resumption (e.g., Phase 4) would be closer to ~700-800 tokens with more agent summaries and decisions.

---

## Template 2: Compaction Alert

### Purpose

Injected automatically by the `UserPromptSubmit` hook when it detects that a `PreCompact` checkpoint file was written since the last acknowledged checkpoint. This means compaction occurred within the current session and some conversation history has been compressed.

### Injection Mechanism

The `UserPromptSubmit` hook:
1. Checks for files matching `.jerry/checkpoints/cx-*-checkpoint.json` with `acknowledged: false`
2. Reads the most recent unacknowledged checkpoint file
3. Extracts key fields for inline display
4. Injects the populated `<compaction-alert>` tag via `additionalContext`

### Template

```xml
<compaction-alert>
CONTEXT COMPACTION OCCURRED. Some conversation history was compressed by Claude Code.
You may have lost track of recent work. Re-orient using the data below.

CHECKPOINT: {CHECKPOINT_FILE_PATH}
TRIGGER: {COMPACTION_TRIGGER}
PRE-COMPACTION FILL: {ESTIMATED_FILL_BEFORE}%

YOU WERE DOING: Phase {ACTIVE_PHASE} ({ACTIVE_PHASE_NAME}), {ACTIVE_ACTIVITY}
LAST SCORE: {CURRENT_GATE_SCORE} ({CURRENT_GATE}, iteration {CURRENT_GATE_ITERATION})

CRITICAL CONTEXT:
{CRITICAL_CONTEXT_SUMMARY}

PENDING DECISIONS:
{PENDING_DECISIONS_SUMMARY}

IMMEDIATE ACTIONS:
1. Read checkpoint file: {CHECKPOINT_FILE_PATH}
2. Read ORCHESTRATION.yaml resumption section: {ORCHESTRATION_YAML_PATH}
3. Merge checkpoint data into resumption section if checkpoint is newer
4. Set checkpoint acknowledged=true in the checkpoint file
5. Continue from: {NEXT_ACTION}
</compaction-alert>
```

### Token Budget Analysis

| Section | Estimated Tokens | Notes |
|---------|-----------------|-------|
| Fixed instruction text | ~80 | Framing, immediate actions list |
| State fields (5 inline fields) | ~50 | Phase, activity, score, gate, iteration |
| Critical context summary | ~60 | 1-2 sentence summary from checkpoint |
| Pending decisions summary | ~40 | 1-2 key decisions with phase impacts |
| File paths and actions | ~50 | 2 paths + action descriptions |
| **Total** | **~280** | Within 200-400 target |

### Populated Example (PROJ-001 at QG-2 Compaction, Step 9)

```xml
<compaction-alert>
CONTEXT COMPACTION OCCURRED. Some conversation history was compressed by Claude Code.
You may have lost track of recent work. Re-orient using the data below.

CHECKPOINT: .jerry/checkpoints/cx-001-checkpoint.json
TRIGGER: auto (PreCompact hook)
PRE-COMPACTION FILL: 88.6%

YOU WERE DOING: Phase 2 (Core License Changes), qg-2-iteration-1
LAST SCORE: 0.960 (qg-2, iteration 1)

CRITICAL CONTEXT:
QG-2 was scoring 3 Phase 2 deliverables. S-007 found 1 major finding: DA-001 copyright
holder inconsistency between NOTICE and header_template. Revision was in progress.

PENDING DECISIONS:
- RD-001: Align copyright holder to 'Adam Nowak'. Affects Phase 3 header_template.

IMMEDIATE ACTIONS:
1. Read checkpoint file: .jerry/checkpoints/cx-001-checkpoint.json
2. Read ORCHESTRATION.yaml resumption section: projects/PROJ-001-oss-release/ORCHESTRATION.yaml
3. Merge checkpoint data into resumption section if checkpoint is newer
4. Set checkpoint acknowledged=true in the checkpoint file
5. Continue from: Complete QG-2 iteration 1 revision (apply DA-001 fix), then re-score
</compaction-alert>
```

**Populated example token count:** ~250 tokens (measured by character count / 4). Well within the 200-400 token budget.

---

## Variable Specification

### Template 1 Variables

| Variable | Data Source | Section/Field in Source | Populated By | When Updated |
|----------|------------|------------------------|--------------|--------------|
| `{WORKFLOW_ID}` | ORCHESTRATION.yaml | `header.workflow_id` | Orchestrator at init | Once |
| `{PROJECT_ID}` | ORCHESTRATION.yaml | `header.project_id` | Orchestrator at init | Once |
| `{ORCHESTRATION_PLAN_PATH}` | ORCHESTRATION.yaml | `header.plan_file` or convention | Orchestrator at init | Once |
| `{CURRENT_PHASE}` | ORCHESTRATION.yaml | `resumption.current_phase` | Orchestrator | Every phase transition |
| `{CURRENT_PHASE_NAME}` | ORCHESTRATION.yaml | `resumption.current_phase_name` | Orchestrator | Every phase transition |
| `{WORKFLOW_STATUS}` | ORCHESTRATION.yaml | `resumption.workflow_status` | Orchestrator | Every state transition |
| `{CURRENT_ACTIVITY}` | ORCHESTRATION.yaml | `resumption.current_activity` | Orchestrator | Every activity change |
| `{LAST_CHECKPOINT}` | ORCHESTRATION.yaml | `resumption.last_checkpoint` | Orchestrator | Every checkpoint |
| `{CONTEXT_FILL_AT_CHECKPOINT}` | ORCHESTRATION.yaml | `resumption.context_fill_at_update` | Orchestrator (from `<context-monitor>`) | Every resumption update |
| `{COMPACTION_COUNT}` | ORCHESTRATION.yaml | `resumption.compaction_events.count` | PreCompact hook + orchestrator merge | Each compaction event |
| `{NEXT_ACTION}` | ORCHESTRATION.yaml | `resumption.next_step` | Orchestrator | Every state transition |
| `{GATES_COMPLETED}` | ORCHESTRATION.yaml | `resumption.quality_trajectory.gates_completed` | Orchestrator | Each gate completion |
| `{GATES_REMAINING}` | ORCHESTRATION.yaml | `resumption.quality_trajectory.gates_remaining` | Orchestrator | Each gate completion |
| `{CURRENT_GATE}` | ORCHESTRATION.yaml | `resumption.quality_trajectory.current_gate` | Orchestrator | Gate entry/exit |
| `{CURRENT_GATE_ITERATION}` | ORCHESTRATION.yaml | `resumption.quality_trajectory.current_gate_iteration` | Orchestrator | Each gate iteration |
| `{LAST_GATE_SCORE}` | ORCHESTRATION.yaml | `resumption.quality_trajectory.score_history.{gate}[-1]` | Orchestrator | Each gate iteration |
| `{LOWEST_DIMENSION}` | ORCHESTRATION.yaml | `resumption.quality_trajectory.lowest_dimension` | Orchestrator | Each gate iteration |
| `{DECISIONS_BLOCK}` | ORCHESTRATION.yaml | `resumption.decisions[]` | Orchestrator (semi-auto) | Each cross-phase decision |
| `{AGENT_SUMMARIES_BLOCK}` | ORCHESTRATION.yaml | `resumption.agent_summaries` | Orchestrator | Each agent completion |
| `{DEFECT_PATTERNS_BLOCK}` | ORCHESTRATION.yaml | `resumption.defect_summary.recurring_patterns[]` | Orchestrator | Each gate iteration |
| `{FILE_N_PATH}` | ORCHESTRATION.yaml | `resumption.files_to_read[N].path` | Planner at init, orchestrator adjusts | Phase transitions |
| `{FILE_N_SECTIONS}` | ORCHESTRATION.yaml | `resumption.files_to_read[N].sections` | Orchestrator | Phase transitions |
| `{FILE_N_PURPOSE}` | ORCHESTRATION.yaml | `resumption.files_to_read[N].purpose` | Planner at init | Rarely |

### Template 2 Variables

| Variable | Data Source | Section/Field in Source | Populated By | When Updated |
|----------|------------|------------------------|--------------|--------------|
| `{CHECKPOINT_FILE_PATH}` | Filesystem | `.jerry/checkpoints/cx-{NNN}-checkpoint.json` path | PreCompact hook | Each compaction event |
| `{COMPACTION_TRIGGER}` | Checkpoint file | `trigger.type` + `trigger.source` | PreCompact hook | Each compaction event |
| `{ESTIMATED_FILL_BEFORE}` | Checkpoint file | `context_state.estimated_fill_before_compaction` | PreCompact hook (from `context-monitor-state.json`) | Each compaction event |
| `{ACTIVE_PHASE}` | Checkpoint file | `orchestration_state.current_phase` | PreCompact hook (from ORCHESTRATION.yaml `resumption`) | Each compaction event |
| `{ACTIVE_PHASE_NAME}` | Checkpoint file | `orchestration_state.current_phase_name` | PreCompact hook (from ORCHESTRATION.yaml `resumption`) | Each compaction event |
| `{ACTIVE_ACTIVITY}` | Checkpoint file | `orchestration_state.current_activity` | PreCompact hook (from ORCHESTRATION.yaml `resumption`) | Each compaction event |
| `{CURRENT_GATE_SCORE}` | Checkpoint file | `orchestration_state.current_gate_score` | PreCompact hook (from ORCHESTRATION.yaml `quality_gates`) | Each compaction event |
| `{CURRENT_GATE}` | Checkpoint file | `orchestration_state.current_gate` | PreCompact hook (from ORCHESTRATION.yaml `quality_gates`) | Each compaction event |
| `{CURRENT_GATE_ITERATION}` | Checkpoint file | `orchestration_state.current_gate_iteration` | PreCompact hook (from ORCHESTRATION.yaml `quality_gates`) | Each compaction event |
| `{CRITICAL_CONTEXT_SUMMARY}` | Checkpoint file | `recovery_instructions.critical_context` | PreCompact hook (template-based) | Each compaction event |
| `{PENDING_DECISIONS_SUMMARY}` | Checkpoint file | `accumulated_context.decisions_since_last_checkpoint` | PreCompact hook (from ORCHESTRATION.yaml `resumption.decisions` where `applied: false`) | Each compaction event |
| `{ORCHESTRATION_YAML_PATH}` | Convention | Project path + `/ORCHESTRATION.yaml` | UserPromptSubmit hook (from checkpoint `orchestration_state.workflow_id` -> path resolution) | Each compaction event |
| `{NEXT_ACTION}` | Checkpoint file | `recovery_instructions.next_action` | PreCompact hook | Each compaction event |

### Variable Population Responsibility Summary

| Populator | Variables Owned | Mechanism |
|-----------|----------------|-----------|
| **Orchestrator** | 20 (Template 1) | Updates ORCHESTRATION.yaml `resumption` section at every state transition per the update protocol |
| **PreCompact hook** | 13 (Template 2) | Reads ORCHESTRATION.yaml + `context-monitor-state.json`, writes checkpoint JSON |
| **UserPromptSubmit hook** | 1 (`{ORCHESTRATION_YAML_PATH}` resolution) | Reads checkpoint file, resolves project path, injects populated Template 2 |
| **Planner/init** | 3 (static: `{WORKFLOW_ID}`, `{PROJECT_ID}`, `{ORCHESTRATION_PLAN_PATH}`) | Set once at workflow initialization |
| **Operator/human** | Template 1 injection | Pastes populated Template 1 or triggers automation |

---

## Open Question Resolutions

### OQ-R1: Token Budget for Compaction Alerts

**Question:** What is the maximum token budget for the `<compaction-alert>` injection?

**Resolution: 300-400 tokens maximum (RECOMMENDED), with a hard ceiling of 500 tokens.**

**Reasoning:**

1. Phase 3 budgeted <200 tokens for WARNING+ `<context-monitor>` injections. The compaction alert serves a fundamentally different purpose -- it is a one-time re-orientation payload, not a recurring status line. It fires only when compaction occurs (predicted 2x per FEAT-015 workflow), not on every prompt.

2. Post-compaction context is estimated at ~50K tokens (25% of window per Phase 2 assumptions). A 400-token injection consumes 0.8% of post-compaction context. Even at the lower end of compaction reset (30K tokens), 400 tokens is 1.3% -- negligible relative to the cost of the re-orientation file reads that follow (~1,500-7,500 tokens depending on what the LLM reads).

3. The `<context-monitor>` injection (~100-200 tokens) continues to fire on every prompt post-compaction. The compaction alert is additive to that on only the first prompt after compaction. Total injection for the first post-compaction prompt: ~400-600 tokens (compaction alert + context monitor). This is comparable to the existing L2 reinject budget (~600 tokens/prompt) and is a one-time cost.

4. The Template 2 populated example above measures at ~250 tokens, well within the 300-400 budget. The template has room for slightly longer `{CRITICAL_CONTEXT_SUMMARY}` or `{PENDING_DECISIONS_SUMMARY}` values without exceeding 400 tokens.

**Budget enforcement:** The `UserPromptSubmit` hook SHOULD truncate `{CRITICAL_CONTEXT_SUMMARY}` and `{PENDING_DECISIONS_SUMMARY}` if the total populated template exceeds 500 tokens. Truncation should preserve the structured fields and abbreviate the free-text summaries.

---

### OQ-R2: Full ORCHESTRATION.yaml vs. Resumption Section Only

**Question:** Should the resumption prompt instruct the LLM to read the FULL ORCHESTRATION.yaml or ONLY the resumption section?

**Resolution: Read the resumption section FIRST, then selectively read other sections as needed. Do NOT read the full ORCHESTRATION.yaml by default.**

**Reasoning:**

1. The full ORCHESTRATION.yaml for PROJ-001 is ~7,500 tokens. The enhanced resumption section (v2.0) is estimated at ~1,500 tokens with all 7 sub-sections populated. This is an 80% token reduction for initial orientation.

2. Post-compaction context is estimated at ~50K tokens. Reading the full YAML consumes 15% of that budget. Reading only the resumption section consumes 3%. The difference (12% or ~6,000 tokens) is roughly equivalent to one QG strategy execution -- significant.

3. The enhanced resumption schema (Phase 4) was explicitly designed so that "a resuming session should be able to read ONLY the `resumption:` section and orient itself within 2-3 prompts." The schema includes structured versions of all data previously scattered across the full YAML: quality trajectory, defect summary, decisions, agent summaries.

4. **However**, the resuming session WILL need additional YAML sections in specific cases:
   - If resuming mid-QG-iteration: read `quality_gates.{current_gate}` for strategy-level detail
   - If resuming before a phase that has cross-phase dependencies: read the specific phase definition
   - If the resumption section is stale (staleness flag in `<context-monitor>`): read the full YAML as fallback

5. Template 1 implements this by specifying `Sections: resumption, quality_gates.{current_gate}, next_actions` for the ORCHESTRATION.yaml file read. This targets ~2,500 tokens instead of ~7,500.

**Instruction in templates:** Both templates instruct the LLM to "Read ORCHESTRATION.yaml resumption section" specifically, not the full file. Template 1's file read instructions include specific sections to target.

---

### OQ-R3: Compaction During Mid-QG Iteration

**Question:** If compaction occurs mid-QG iteration, should the resumed session restart the iteration or continue?

**Resolution: Restart the current iteration from the beginning (re-read deliverables, re-score with all required strategies). Do NOT attempt to continue a partially-completed iteration.**

**Reasoning:**

1. **Integrity argument.** A QG iteration applies multiple strategies (S-014, S-007, S-002 for C2). If compaction occurs after S-014 scores but before S-007 runs, the partial iteration has incomplete coverage. The S-014 score without S-007 constitutional check is not a valid quality assessment per the H-14 creator-critic cycle requirement.

2. **Context loss argument.** Even if one strategy completed before compaction, its results are in the (now-compressed) conversation context. The LLM may not accurately remember the findings. The written artifact exists on disk, but reading it back costs almost the same as re-running the strategy.

3. **Cost argument.** A single QG iteration costs ~29,000 tokens (Phase 2 data). Attempting to reconstruct partial state and continue would require: reading the checkpoint (~200 tokens), reading any completed strategy artifacts (~3,000-8,000 tokens each), determining what remains, and continuing. For a 3-strategy iteration, if one strategy completed, the "continue" path costs ~200 + ~5,000 (read artifact) + ~12,000 (run remaining 2 strategies) = ~17,200 tokens. The "restart" path costs ~29,000 tokens. The savings (~12,000 tokens) are modest relative to the complexity and fragility of the "continue" path.

4. **Simplicity argument.** The "restart iteration" policy is simple, deterministic, and always correct. The "continue partial" policy requires tracking which strategies completed, validating their results post-compaction, and handling edge cases (e.g., what if the completed strategy's score changed the iteration verdict?). The additional complexity is not justified by the modest token savings.

**Exception:** If compaction occurs AFTER all strategies have run and scored but BEFORE the revision is applied, the checkpoint will contain the strategy scores and findings. In this case, the resuming session SHOULD read the strategy artifacts and apply the revision without re-scoring. This is because the scoring is complete -- only the mechanical revision remains. The Template 1 `{NEXT_ACTION}` field should specify "Apply revision from QG-N iter M findings, then re-score" in this case.

**Template implementation:** The `{CURRENT_ACTIVITY}` field distinguishes between `qg-N-iteration-M` (scoring in progress) and `qg-N-iteration-M-revision` (revision in progress). Template 1's `{NEXT_ACTION}` is populated accordingly:
- If `qg-N-iteration-M`: "Restart QG-N iteration M. Re-read deliverables and run all required strategies."
- If `qg-N-iteration-M-revision`: "Apply revision based on QG-N iter M findings (artifacts at ...), then run iteration M+1."

---

### OQ-R4: Multiple Compaction Events in One Session

**Question:** How should the system handle multiple compaction events in a single session?

**Resolution: Each compaction event produces a new checkpoint file with an incrementing ID. The `UserPromptSubmit` hook injects alerts for ALL unacknowledged checkpoints, but the LLM only needs to process the most recent one.**

**Reasoning:**

1. **Phase 2 predicts 2 compaction events for FEAT-015** (Steps 9 and 17). These occur at QG-2 and QG-Final, which are separated by substantial work (Phases 3-4). Multiple compactions in a single session are expected, not exceptional.

2. **Each checkpoint supersedes the previous one.** Checkpoint `cx-002` contains the full orchestration state at the time of the second compaction, including all work done after the first compaction. Reading `cx-002` is sufficient; `cx-001` is historical.

3. **However, the sequence of checkpoints provides a compaction history** that should be preserved in the ORCHESTRATION.yaml `resumption.compaction_events` section. Each compaction event entry records when it occurred and what state was active, enabling post-hoc analysis of compaction patterns.

**Implementation:**

- **Checkpoint file naming:** `cx-{NNN}-checkpoint.json` with NNN incrementing per session (cx-001, cx-002, ...).
- **UserPromptSubmit hook behavior:** Check for any checkpoint files with `acknowledged: false`. If multiple exist, inject the compaction alert using data from the MOST RECENT file only. Include a note: "Note: {N} compaction events have occurred in this session. Processing most recent checkpoint."
- **LLM behavior on alert:** Read the most recent checkpoint, merge into ORCHESTRATION.yaml resumption section, set `acknowledged: true` on ALL unacknowledged checkpoints (not just the most recent).
- **Cleanup:** Checkpoint files are NOT deleted within a session. They are cleaned up when the workflow completes or when the operator explicitly clears them. This preserves the audit trail.

**Template 2 extension for multiple compactions:**

The `<compaction-alert>` tag includes the compaction count:

```
COMPACTION EVENT: {COMPACTION_EVENT_NUMBER} of {TOTAL_COMPACTION_COUNT} this session
```

This single line addition costs ~10 tokens and provides the LLM with awareness of compaction frequency, which can inform its decisions about context consumption going forward (e.g., being more aggressive about deferring non-essential reads if compaction has already occurred twice).

---

### OQ-R5: Enforcement via Hook vs. Rule File

**Question:** Should the resumption update protocol be enforced by a hook (deterministic) or by a rule file (vulnerable to context rot)?

**Resolution: Dual enforcement -- hook-based validation (L3/L4) as primary, with rule-file guidance (L1) as supplementary. The hook provides the deterministic backstop; the rule provides the behavioral guidance.**

**Reasoning:**

1. **The paradox.** The resumption update protocol is designed to protect against context rot. If the protocol itself is enforced only via a rule file, it is vulnerable to the very problem it is solving. This is the circular dependency identified in Phase 4: "The checkpoint file's richness depends on the resumption section being kept current."

2. **Hook-based enforcement (L3/L4) is immune to context rot** per the enforcement architecture in ADR-EPIC002-002. A `PostToolUse` hook that fires after every `Write` to ORCHESTRATION.yaml can verify that the resumption section was updated. If the resumption section's `updated_at` timestamp is stale (older than the current phase start), the hook can inject a warning via `additionalContext`.

3. **Rule-file guidance (L1) provides the WHY.** The hook can detect staleness, but it cannot explain the update protocol or describe what fields to update. A rule file (or a section in the orchestration skill documentation) provides this behavioral guidance. L1 rules degrade with context, but the hook backstop catches failures.

4. **L2 reinject provides the bridge.** A reinject tag at rank 7-8 can remind the orchestrator: "Update ORCHESTRATION.yaml resumption section at every state transition. Include: current_phase, current_activity, agent_summaries, quality_trajectory, decisions." At ~40 tokens, this is affordable within the L2 budget.

**Implementation architecture:**

| Layer | Enforcement | What It Does | Tokens |
|-------|------------|--------------|--------|
| L1 | Rule file / skill docs | Describes the update protocol, field definitions, update triggers | ~500 (loaded once) |
| L2 | Reinject tag | Reminds orchestrator to update resumption section | ~40/prompt |
| L3 | `PostToolUse` hook on ORCHESTRATION.yaml writes | Checks `resumption.updated_at` staleness; warns if stale | 0 (deterministic) |
| L4 | `<context-monitor>` staleness field | Displays "Resumption staleness: STALE/FRESH" in every prompt injection | ~10/prompt (within existing budget) |

**Total enforcement cost:** ~550 tokens initial + ~50 tokens/prompt ongoing. This is within the enforcement architecture budget defined in ADR-EPIC002-002 (~15,100 tokens total, 7.6% of 200K context).

---

## Mental Test: PROJ-001

### Test Scenario Setup

The Phase 2 cumulative fill projection predicts two compaction events for a single-session FEAT-015 run:

1. **Compaction Point 1:** During QG-2, around Step 9, at ~106% fill (compaction triggered)
2. **Compaction Point 2:** During QG-Final, around Step 17, at ~118% fill (second compaction)

For each compaction point, I test whether the templates provide sufficient context for the resumed/re-oriented session to continue productively.

### Test 1: QG-2 Compaction (Step 9, ~106% Fill)

**Scenario:** The orchestrator is in Phase 2, running QG-2 iteration 2. QG-2 iteration 1 scored 0.960 but S-007 found DA-001 (copyright inconsistency). Revision was applied. Iteration 2 is scoring when compaction fires at ~106% fill.

**What Template 2 (Compaction Alert) provides:**

| Information Needed | Provided? | How |
|-------------------|-----------|-----|
| What happened (compaction occurred) | Yes | First line: "CONTEXT COMPACTION OCCURRED" |
| Where we are (Phase 2, QG-2 iter 2) | Yes | "YOU WERE DOING: Phase 2 (Core License Changes), qg-2-iteration-2" |
| Last score | Yes | "LAST SCORE: 0.960 (qg-2, iteration 1)" |
| What was found in prior iterations | Partially | `{CRITICAL_CONTEXT_SUMMARY}` contains the S-007 DA-001 finding, but not the full defect list from QG-1 |
| Key decisions | Yes | `{PENDING_DECISIONS_SUMMARY}` includes RD-001 (copyright alignment) |
| What to do next | Yes | "Continue from: Restart QG-2 iteration 2 scoring" (per OQ-R3 resolution) |
| Files to read | Yes | Checkpoint file path + ORCHESTRATION.yaml path |

**Can the LLM be productive by prompt 3?**

- **Prompt 1:** Compaction alert is injected. LLM reads it, reads checkpoint file, reads ORCHESTRATION.yaml resumption section. (~1,500 + 200 + 1,500 = ~3,200 tokens consumed by reads)
- **Prompt 2:** LLM confirms understanding, reads the 3 Phase 2 deliverable artifacts for QG-2 scoring. (~5,000-8,000 tokens for deliverable reads)
- **Prompt 3:** LLM runs first QG strategy (S-014 scorer) on the deliverables.

**Verdict: YES.** The LLM reaches productive work (strategy execution) by prompt 3. Total re-orientation cost: ~3,200-11,200 tokens, or 6.4-22.4% of post-compaction context (assuming 50K tokens post-compaction). This leaves 78-94% of context for actual work.

**Risk:** If post-compaction context is lower than 50K (e.g., 30K), the re-orientation cost of ~11,200 tokens is 37% of available context. This is high but still leaves enough for at least 1 QG iteration (~29K tokens would need ~60% of a 50K window). The risk is that the QG iteration itself could trigger another compaction. This is mitigated by the OQ-R3 resolution (restart from iteration start, not partial) and the checkpoint system recording each compaction.

---

### Test 2: QG-Final Compaction (Step 17, ~118% Fill)

**Scenario:** The orchestrator is in Phase 4, running QG-Final iteration 2. Iteration 1 scored 0.906 (REVISE). This is the SECOND compaction event in the session. All phases 1-4 are complete. QG-1, QG-2, and QG-3 have passed. QG-Final is scoring ALL 6 phase deliverables.

**What Template 2 (Compaction Alert) provides:**

| Information Needed | Provided? | How |
|-------------------|-----------|-----|
| What happened (second compaction) | Yes | "COMPACTION EVENT: 2 of 2 this session" |
| Where we are (Phase 4, QG-Final iter 2) | Yes | "YOU WERE DOING: Phase 4, qg-final-iteration-2" |
| Last score | Yes | "LAST SCORE: 0.906 (qg-final, iteration 1)" |
| All prior gate results | Partially | The checkpoint includes `phases_complete: [1,2,3,4]` and `gates_completed: [qg-1, qg-2, qg-3]` with score histories |
| All accumulated decisions | Yes | `accumulated_context.decisions_since_last_checkpoint` captures decisions from QG-3 and Phase 4 (decisions from QG-1/QG-2 are in the resumption section which was updated at CP-002) |
| All agent summaries | Yes | The resumption section (updated at the last checkpoint) contains all 8 agent summaries |
| What to do next | Yes | "Restart QG-Final iteration 2. Re-read all 6 deliverables and run S-014, S-007, S-002." |

**Can the LLM be productive by prompt 3?**

- **Prompt 1:** Compaction alert injected. LLM reads checkpoint file + ORCHESTRATION.yaml resumption section. (~200 + 1,500 = ~1,700 tokens)
- **Prompt 2:** LLM reads the 6 phase deliverables for QG-Final scoring. This is the expensive step: 6 deliverables at ~1,500-6,500 tokens each = ~15,000-27,000 tokens. **This may need to be split across 2 prompts if deliverables are large.**
- **Prompt 3:** LLM begins QG-Final scoring (first strategy).

**Verdict: CONDITIONAL YES.** If the 6 deliverables total <15K tokens (reading summaries rather than full artifacts), the LLM reaches productive work by prompt 3. If the deliverables are larger, it may need prompt 4. This is a known challenge identified in Phase 2: "QG-Final is inherently expensive because it scores ALL prior deliverables."

**Mitigation:** The agent summaries in the resumption section provide one-line summaries of each agent's work. For QG-Final, the scorer can use these summaries plus targeted reads of specific deliverable sections (rather than full reads) to stay within budget. Template 1's instruction "Do NOT re-read artifacts from completed phases unless specifically needed" supports this optimization.

**Critical observation for QG-Final:** This compaction point is where the "resumption section first, not full YAML" decision (OQ-R2) pays off most strongly. At this point, the resumption section contains accumulated intelligence from 4 phases, 3 completed gates, and 8 agents. Reading this ~1,500 token section provides the LLM with the full workflow history without loading the ~7,500 token YAML. The 6,000-token saving is equivalent to ~2 deliverable reads -- a meaningful budget reduction when the LLM must read 6 deliverables.

### Mental Test Summary

| Compaction Point | Template | Productive by Prompt 3? | Re-orientation Cost (tokens) | Re-orientation Cost (% of 50K post-compact) |
|-----------------|----------|------------------------|------------------------------|----------------------------------------------|
| QG-2 (Step 9, 106%) | Template 2 | Yes | ~3,200-11,200 | 6.4-22.4% |
| QG-Final (Step 17, 118%) | Template 2 | Conditional (may need prompt 4 for 6 deliverables) | ~1,700-28,700 | 3.4-57.4% |

**Cross-session resumption (Template 1):** If instead of continuing after compaction, the operator starts a new session (Template 1), the re-orientation cost is: Template 1 itself (~760 tokens in context) + file reads (~1,500 resumption + ~2,000 ORCHESTRATION_PLAN sections + ~1,000 WORKTRACKER) = ~5,260 tokens total. In a fresh 200K context window, this is 2.6% -- negligible. The LLM would be productive by prompt 3 with ~195K tokens of headroom.

---

## Integration Notes

### How Templates Connect to the Detection System

```
                     DETECTION SYSTEM (Phase 3)
                     ==========================

    [Every Prompt]                          [Compaction Imminent]
         |                                         |
    UserPromptSubmit                         PreCompact Hook
    Hook (Method A)                          (Method B)
         |                                         |
    Computes fill %                          Writes checkpoint
    from transcript                          .jerry/checkpoints/
         |                                  cx-{NNN}-checkpoint.json
         |                                         |
    +----v-----------+                             |
    | Is fill < 60%? |--YES--> Normal ops          |
    +----+-----------+                             |
         |NO                                       |
    +----v-----------+                             |
    | Is fill 60-80%?|--YES--> Inject              |
    +----+-----------+    <context-monitor>         |
         |NO              WARNING level             |
    +----v-----------+    + "Update resumption"     |
    | Is fill 80-90%?|--YES--> Inject              |
    +----+-----------+    <context-monitor>         |
         |NO              CRITICAL level            |
    +----v-----------+    + "Checkpoint NOW"        |
    | Is fill 90%+?  |--YES--> Inject              |
    +----+-----------+    <context-monitor>         |
                          COMPACTION level           |
                                                    |
                           POST-COMPACTION           |
                                |                    |
                    +-----------v-----------+        |
                    | UserPromptSubmit hook  |<-------+
                    | detects checkpoint     |
                    | with acknowledged=false|
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    | INJECT TEMPLATE 2     |
                    | <compaction-alert>     |
                    | (populated from       |
                    |  checkpoint file)     |
                    +-----------+-----------+
                                |
                    +-----------v-----------+
                    | LLM re-orients:       |
                    | 1. Read checkpoint    |
                    | 2. Read resumption    |
                    | 3. Merge + acknowledge|
                    | 4. Continue work      |
                    +-----------------------+


                     RESUMPTION SYSTEM (this design)
                     ===============================

    [New Session Started by Operator]
                |
    +-----------v-----------+
    | Operator/automation    |
    | reads latest checkpoint|
    | + ORCHESTRATION.yaml   |
    | resumption section     |
    +-----------+-----------+
                |
    +-----------v-----------+
    | POPULATE TEMPLATE 1   |
    | (resumption prompt)   |
    | from checkpoint +     |
    | resumption data       |
    +-----------+-----------+
                |
    +-----------v-----------+
    | Paste as first message |
    | in new session         |
    +-----------+-----------+
                |
    +-----------v-----------+
    | LLM reads files in    |
    | priority order,       |
    | confirms understanding,|
    | continues work         |
    +-----------------------+
```

### Hook Modification Summary

| Hook | Current State | Required Modifications |
|------|-------------|----------------------|
| `UserPromptSubmit` (command) | Exists. Injects L2 reinforcement tags. | Add: (1) Context fill monitoring from transcript (Method A). (2) Checkpoint file detection + Template 2 injection. (3) Resumption staleness reporting in `<context-monitor>` tag. |
| `PreCompact` (command) | Does not exist. | Create: Write checkpoint file to `.jerry/checkpoints/cx-{NNN}-checkpoint.json` by reading ORCHESTRATION.yaml resumption section + `context-monitor-state.json`. |
| `PostToolUse` (command) | Does not exist for ORCHESTRATION.yaml. | Create (optional, per OQ-R5): Validate resumption section freshness after ORCHESTRATION.yaml writes. Warn if `updated_at` is stale. |

### Data Flow Dependencies

| Data | Written By | Read By | Critical Path? |
|------|-----------|---------|----------------|
| ORCHESTRATION.yaml `resumption` section | Orchestrator LLM | PreCompact hook, Template 1 populator, Template 2 populator (via checkpoint) | YES -- all templates depend on this data being current |
| `.jerry/context-monitor-state.json` | UserPromptSubmit hook (context monitor) | PreCompact hook (for `estimated_fill_before_compaction`) | YES -- checkpoint accuracy depends on this |
| `.jerry/checkpoints/cx-{NNN}-checkpoint.json` | PreCompact hook | UserPromptSubmit hook (for Template 2 injection), Template 1 populator | YES -- both templates use checkpoint data |
| Phase deliverable artifacts | Agent LLMs | Resuming LLM (for QG re-scoring) | NO -- these are existing artifacts, not new data flows |

### Failure Modes

| Failure | Impact | Detection | Recovery |
|---------|--------|-----------|----------|
| Resumption section not updated (RG-6 persists) | Template 1/2 populated with stale data | L4 staleness check in `<context-monitor>`, L3 PostToolUse hook | LLM warned to update; worst case: manual update by operator |
| PreCompact hook fails to write checkpoint | Template 2 not injected; LLM has no compaction awareness | UserPromptSubmit hook finds no checkpoint file; no alert injected | LLM continues without re-orientation; context rot risk accepted. Operator should start new session with Template 1 if quality degrades. |
| Checkpoint file corrupted or incomplete | Template 2 injected with partial data | UserPromptSubmit hook validates JSON parse; if invalid, injects generic "compaction occurred, read ORCHESTRATION.yaml" alert | Graceful degradation: minimal alert still triggers file reads |
| Operator forgets to use Template 1 in new session | New session starts without resumption context | No automated detection (unless future SessionStart hook) | Operator must manually read ORCHESTRATION.yaml and orient themselves |

---

## Self-Review Checklist

- [x] **Both templates are complete, self-contained, and within token budget.** Template 1: ~760 tokens (within 500-1000). Template 2: ~280 tokens (within 200-400). Both include all fields needed for self-orientation without external knowledge.
- [x] **All variables have clear data sources.** 23 variables for Template 1, 13 variables for Template 2. Each mapped to specific ORCHESTRATION.yaml field or checkpoint file field with populator and update trigger identified.
- [x] **OQ-R1 through OQ-R5 answered with reasoning.** OQ-R1: 300-400 tokens with 500 hard ceiling. OQ-R2: Resumption section first, selective reads after. OQ-R3: Restart current iteration. OQ-R4: Incrementing checkpoint IDs, process most recent. OQ-R5: Dual enforcement (hook + rule + reinject).
- [x] **PROJ-001 mental test covers both compaction points.** QG-2 (Step 9, 106%): productive by prompt 3, 6-22% re-orientation cost. QG-Final (Step 17, 118%): conditional yes (may need prompt 4 for 6 deliverables), 3-57% re-orientation cost.
- [x] **Templates are concrete enough to implement.** Both templates include exact text with `{VARIABLE}` placeholders, populated examples with real PROJ-001 data, and token budget measurements. Implementation requires populating variables from specified data sources and injecting the text.
- [x] **H-23/H-24 navigation table with anchor links present.**
- [x] **Limitations disclosed (P-022):**
  - Template 1 requires manual injection by operator (no SessionStart hook automation yet)
  - Template 2 depends on PreCompact hook writing successfully (no fallback if hook fails)
  - Mental test QG-Final scenario shows re-orientation cost up to 57% of post-compaction context, which is high
  - Token budget estimates use character/4 heuristic, not actual tokenizer counts
  - The entire system depends on the resumption update protocol being followed (OQ-R5 dual enforcement mitigates but does not eliminate this dependency)

---

## References

| # | Source | Path | Content Used |
|---|--------|------|-------------|
| 1 | Phase 4: Resumption Assessment | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-4-resumption/resumption-assessor/resumption-assessment.md` | Enhanced resumption schema v2.0 (7 sub-sections, 23 fields), checkpoint file format, detection integration thresholds, injection formats, open questions OQ-R1 through OQ-R5 |
| 2 | Phase 3: Detection Evaluation | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-3-detection/detection-evaluator/detection-evaluation.md` | Hybrid A+B architecture, `<context-monitor>` injection format, threshold levels (60/80/90%), hook integration plan, PreCompact hook design |
| 3 | Phase 2: Run Analysis | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-2-analysis/run-analyzer/run-analysis.md` | Cumulative fill projection (17 steps), compaction points (Steps 9, 17), token budget estimates (~29K per QG iteration, ~7,500 for full YAML), PROJ-001 workflow profile |
| 4 | Phase 1: Mechanism Inventory | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/phase-1-inventory/research-inventory/mechanism-inventory.md` | Hook event types, `$TRANSCRIPT_PATH`, `additionalContext` injection pathway, PreCompact hook capabilities |
| 5 | QG-1 Gate Result | `projects/PROJ-004-context-resilience/orchestration/spike001-ctxres-20260219-001/res/quality-gates/qg-1/gate-result.md` | QG-1 scoring example (0.91 -> 0.93 PASS), strategy execution pattern, revision guidance format |
| 6 | ORCHESTRATION_PLAN.md | `projects/PROJ-004-context-resilience/ORCHESTRATION_PLAN.md` | Workflow architecture, agent registry, phase definitions, checkpoint strategy |
| 7 | ORCHESTRATION template | `skills/orchestration/templates/ORCHESTRATION.template.yaml` | Template resumption section (lines 300-311), checkpoint schema |
| 8 | Quality Enforcement SSOT | `.context/rules/quality-enforcement.md` | H-13 threshold (0.92), H-14 iteration cycles, enforcement architecture (L1-L5), token budgets |
| 9 | ADR-EPIC002-002 | Referenced via Phase 1/2/3 findings | Context rot research (40-60% at 50K+), L2 reinject budget (~600/prompt), enforcement architecture context rot immunity |
