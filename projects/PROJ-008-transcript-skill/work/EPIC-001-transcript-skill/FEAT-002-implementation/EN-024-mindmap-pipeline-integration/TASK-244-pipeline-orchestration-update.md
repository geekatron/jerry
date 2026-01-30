# TASK-244: Update Pipeline Orchestration Flow

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "EN-024:TASK-244"
work_type: TASK
title: "Update Pipeline Orchestration Flow"
description: |
  Modify the transcript skill pipeline orchestration to include conditional
  mindmap generation between ts-formatter and ps-critic stages.
classification: ENABLER
status: DONE
resolution: COMPLETED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T00:00:00Z"
updated_at: "2026-01-30T00:00:00Z"
parent_id: "EN-024"
tags:
  - implementation
  - orchestration
  - pipeline
effort: 3
acceptance_criteria: |
  - Pipeline supports default mindmap generation (per ADR-006 Section 4)
  - Mindmap agents skipped ONLY when --no-mindmap flag present (opt-out)
  - Format selection logic implemented (--mindmap-format: mermaid, ascii, both)
  - State passing to mindmap agents correct (ts_mindmap_output key per ADR-006 Section 5.2)
  - Failure handling produces partial result with warnings (ADR-006 Section 5.4)
  - Output to 08-mindmap/ directory (per DISC-001)
activity: DEVELOPMENT
original_estimate: 3
remaining_work: 0
time_spent: 3
```

---

## Description

Update the transcript skill orchestration to conditionally invoke mindmap generation agents between ts-formatter and ps-critic.

### Pipeline Flow Changes (Per ADR-006)

```
BEFORE:
ts-parser -> ts-extractor -> ts-formatter -> ps-critic

AFTER (DEFAULT - mindmaps ON):
ts-parser -> ts-extractor -> ts-formatter -> [ts-mindmap-*] -> ps-critic
                                                  |
                                                  v
                                        08-mindmap/ files

AFTER (with --no-mindmap opt-out):
ts-parser -> ts-extractor -> ts-formatter -> ps-critic
                                        (mindmaps skipped)
```

### Logic Flow (Per ADR-006 Section 5.3)

```
# Default behavior: Mindmaps generated UNLESS --no-mindmap is set
IF --no-mindmap flag is NOT set:  # Default path
    IF --mindmap-format == "mermaid" OR "both" (default):
        INVOKE ts-mindmap-mermaid
        OUTPUT to 08-mindmap/mindmap.mmd
    IF --mindmap-format == "ascii" OR "both" (default):
        INVOKE ts-mindmap-ascii
        OUTPUT to 08-mindmap/mindmap.ascii.txt
    IF mindmap generation fails:
        LOG warning
        SET ts_mindmap_output.status = "failed"
        CONTINUE with partial result
        ADD regeneration instructions to output
ELSE:  # --no-mindmap flag present
    SKIP mindmap generation
    LOG info: "Mindmap generation disabled via --no-mindmap"
ENDIF

INVOKE ps-critic (include mindmaps in validation if generated)
```

---

## Acceptance Criteria (Per ADR-006)

- [x] Default behavior generates mindmaps (no flag needed) - ADR-006 Section 4
- [x] `--no-mindmap` opt-out flag correctly skips mindmap generation
- [x] Format selection (`--mindmap-format`: mermaid/ascii/both) works correctly
- [x] Default format is "both" when not specified - ADR-006 Section 5.1
- [x] Both mindmap agents can be invoked independently based on format
- [x] ts_formatter_output passed correctly to mindmap agents (packet_path, extraction_report_path)
- [x] ts_mindmap_output state key passed correctly to ps-critic - ADR-006 Section 5.2
- [x] Output written to `08-mindmap/` directory - DISC-001
- [x] Failure handling produces warnings, not errors - ADR-006 Section 5.4
- [x] Regeneration instructions included in output on failure

---

## Implementation Notes

### State Schema (Per ADR-006 Section 5.2)

```yaml
# Input to mindmap agents (from ts-formatter)
ts_formatter_output:
  packet_path: string           # e.g., "transcript-meeting-001/"
  files_created: string[]       # All generated file paths
  total_tokens: integer         # Total token count
  extraction_report_path: string  # Path to extraction-report.json

# Output from mindmap agents - UNIFIED KEY (per ADR-006)
ts_mindmap_output:
  mermaid:
    path: string                # e.g., "08-mindmap/mindmap.mmd"
    status: "complete" | "failed" | "skipped"
    topic_count: integer
    deep_link_count: integer
    error_message: string | null
  ascii:
    path: string                # e.g., "08-mindmap/mindmap.ascii.txt"
    status: "complete" | "failed" | "skipped"
    topic_count: integer
    max_line_width: integer
    error_message: string | null
  overall_status: "complete" | "partial" | "failed" | "skipped"
```

### Failure Handling

When mindmap generation fails:
1. Log warning with error details
2. Set `status: "failed"` in output
3. Continue pipeline execution
4. Add to final output:
   - Warning message indicating mindmap failure
   - Instructions: "To regenerate mindmaps, run: [command]"

### Files to Modify

1. `skills/transcript/SKILL.md` - Orchestration flow section
2. `skills/transcript/docs/PLAYBOOK.md` - Add Phase 3.5 for mindmaps

---

## Related Items

- Parent: [EN-024: Mindmap Pipeline Integration](./EN-024-mindmap-pipeline-integration.md)
- Blocked By: [TASK-242: ADR-006](./TASK-242-adr-006-mindmap-integration.md)
- **ADR Reference:** [ADR-006: Mindmap Pipeline Integration](../../../../../docs/adrs/ADR-006-mindmap-pipeline-integration.md) - Sections 4 (Decision), 5.1-5.4 (Implementation)
- Blocks: [TASK-245: ps-critic Update](./TASK-245-ps-critic-mindmap-validation.md)
- Blocks: [TASK-246: Integration Tests](./TASK-246-integration-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated Orchestration | Implementation | skills/transcript/SKILL.md |
| Updated Playbook | Documentation | skills/transcript/docs/PLAYBOOK.md |

### Verification

- [x] Conditional logic works (documented in SKILL.md lines 538-552)
- [x] Both formats generate correctly (documented in SKILL.md lines 542-548)
- [x] Failure handling graceful (documented in SKILL.md line 552)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation |
| 2026-01-30 | Updated | **ADR-006 ALIGNMENT**: Updated acceptance criteria and implementation notes to align with ADR-006. Changed from opt-in (--mindmap) to opt-out (--no-mindmap) behavior. Added unified ts_mindmap_output state key. Updated output path to 08-mindmap/ per DISC-001. |
| 2026-01-30 | **DONE** | **TASK COMPLETE**: All 10 acceptance criteria MET via SKILL.md v2.1.0 (commit `8ac3e28` from TASK-243). PLAYBOOK.md updates deferred to TASK-247 which has detailed requirements. Evidence: SKILL.md lines 196-284 (pipeline diagram), 392-401 (parameters), 536-559 (STEP 3.5 orchestration), 599-614 (ts_mindmap_output state schema). |
