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
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T00:00:00Z"
updated_at: "2026-01-28T00:00:00Z"
parent_id: "EN-024"
tags:
  - implementation
  - orchestration
  - pipeline
effort: 3
acceptance_criteria: |
  - Pipeline supports conditional mindmap stage
  - Mindmap agents invoked only when --mindmap flag present
  - Format selection logic implemented
  - State passing to mindmap agents correct
  - Failure handling produces partial result with warnings
activity: DEVELOPMENT
original_estimate: 3
remaining_work: 3
time_spent: 0
```

---

## Description

Update the transcript skill orchestration to conditionally invoke mindmap generation agents between ts-formatter and ps-critic.

### Pipeline Flow Changes

```
BEFORE:
ts-parser -> ts-extractor -> ts-formatter -> ps-critic

AFTER (when --mindmap):
ts-parser -> ts-extractor -> ts-formatter -> [ts-mindmap-*] -> ps-critic
                                                  |
                                    (conditional based on flag)
```

### Logic Flow

```
IF --mindmap flag is set:
    IF --mindmap-format == "mermaid" OR "both":
        INVOKE ts-mindmap-mermaid
    IF --mindmap-format == "ascii" OR "both":
        INVOKE ts-mindmap-ascii
    IF mindmap generation fails:
        LOG warning
        CONTINUE with partial result
        ADD regeneration instructions to output
ENDIF

INVOKE ps-critic (include mindmaps in validation if generated)
```

---

## Acceptance Criteria

- [ ] Conditional logic for --mindmap flag implemented
- [ ] Format selection (mermaid/ascii/both) works correctly
- [ ] Both mindmap agents can be invoked independently
- [ ] ts_formatter_output passed correctly to mindmap agents
- [ ] ts_mindmap_output passed correctly to ps-critic
- [ ] Failure handling produces warnings, not errors
- [ ] Regeneration instructions included in output on failure

---

## Implementation Notes

### State Schema Updates

```yaml
# Input to mindmap agents (from ts-formatter)
ts_formatter_output:
  packet_path: string
  files_created: string[]
  total_tokens: integer
  extraction_report_path: string  # Need this for mindmap content

# Output from mindmap agents
ts_mindmap_mermaid_output:
  mindmap_path: string
  topic_count: integer
  deep_link_count: integer
  status: "complete" | "failed"
  error_message: string | null

ts_mindmap_ascii_output:
  ascii_path: string
  topic_count: integer
  max_line_width: integer
  status: "complete" | "failed"
  error_message: string | null
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

- [ ] Conditional logic works
- [ ] Both formats generate correctly
- [ ] Failure handling graceful

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation |
