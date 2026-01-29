# TASK-243: Update SKILL.md with --mindmap Flag

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "EN-024:TASK-243"
work_type: TASK
title: "Update SKILL.md with --mindmap Flag"
description: |
  Add --mindmap and --mindmap-format parameters to the transcript SKILL.md
  definition, including documentation and invocation examples.
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
  - skill-md
  - parameters
effort: 2
acceptance_criteria: |
  - --mindmap flag added to SKILL.md Input Parameters
  - --mindmap-format parameter added with values: mermaid, ascii, both
  - Default behavior documented ("both" when --mindmap used)
  - Invocation examples updated
  - Agent pipeline diagram updated
activity: DEVELOPMENT
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## Description

Update the transcript skill SKILL.md file to include the new mindmap parameters.

### Changes Required

1. **Input Parameters Table**: Add new parameters
2. **Invocation Examples**: Add mindmap usage examples
3. **Agent Pipeline Diagram**: Show conditional mindmap step
4. **State Passing Section**: Document mindmap agent outputs

### Parameter Specification

| Parameter | Type | Required | Default | Values | Description |
|-----------|------|----------|---------|--------|-------------|
| `--mindmap` | flag | No | false | - | Enable mindmap generation |
| `--mindmap-format` | string | No | "both" | mermaid, ascii, both | Format(s) to generate |

---

## Acceptance Criteria

- [ ] --mindmap flag documented in Input Parameters section
- [ ] --mindmap-format parameter documented with allowed values
- [ ] Default behavior clearly stated
- [ ] Slash command examples updated
- [ ] Natural language invocation examples updated
- [ ] Pipeline diagram shows conditional mindmap step
- [ ] State passing updated for ts_mindmap_output

---

## Implementation Notes

### Current Parameters (from SKILL.md)

```markdown
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `input_file` | string | Yes | - | Path to transcript file |
| `output_dir` | string | No | `./transcript-output/` | Output directory for packet |
| `format` | string | No | auto-detect | Force format: `vtt`, `srt`, `txt` |
| `confidence_threshold` | float | No | 0.7 | Minimum confidence for extractions |
| `quality_threshold` | float | No | 0.9 | ps-critic quality threshold |
```

### Updated Parameters (to add)

```markdown
| `--mindmap` | flag | No | false | Enable mindmap generation |
| `--mindmap-format` | string | No | both | Format: `mermaid`, `ascii`, `both` |
```

### Example Invocations to Add

```markdown
### With Mindmap Generation
/transcript meeting.vtt --mindmap
/transcript meeting.vtt --mindmap --mindmap-format mermaid
/transcript meeting.vtt --mindmap --mindmap-format ascii
/transcript meeting.vtt --mindmap --mindmap-format both
```

---

## Related Items

- Parent: [EN-024: Mindmap Pipeline Integration](./EN-024-mindmap-pipeline-integration.md)
- Blocked By: [TASK-242: ADR-006](./TASK-242-adr-006-mindmap-integration.md)
- Target File: [skills/transcript/SKILL.md](../../../../../skills/transcript/SKILL.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated SKILL.md | Implementation | skills/transcript/SKILL.md |

### Verification

- [ ] Parameters added correctly
- [ ] Examples are valid
- [ ] Documentation clear

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation |
