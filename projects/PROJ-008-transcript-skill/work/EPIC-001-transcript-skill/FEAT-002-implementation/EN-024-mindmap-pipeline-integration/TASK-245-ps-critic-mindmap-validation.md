# TASK-245: Update ps-critic Mindmap Validation Criteria

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "EN-024:TASK-245"
work_type: TASK
title: "Update ps-critic Mindmap Validation Criteria"
description: |
  Add mindmap-specific validation criteria to ps-critic so it can review
  mindmap outputs when they are generated as part of the transcript skill.
classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T00:00:00Z"
updated_at: "2026-01-28T00:00:00Z"
parent_id: "EN-024"
tags:
  - implementation
  - ps-critic
  - validation
  - quality
effort: 2
acceptance_criteria: |
  - ps-critic validates Mermaid syntax when mindmap.mmd present
  - ps-critic checks deep link validity in mindmaps
  - ps-critic validates ASCII format when mindmap.ascii.txt present
  - Mindmap validation is conditional (only when files present)
  - Validation criteria documented
activity: DEVELOPMENT
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## Description

Update ps-critic to include validation criteria for mindmap outputs when they are generated as part of the transcript skill pipeline.

### Validation Criteria to Add

#### Mermaid Mindmap Validation

| Criterion | Check | Weight |
|-----------|-------|--------|
| MM-001 | Valid Mermaid `mindmap` syntax | Required |
| MM-002 | Single root node present | Required |
| MM-003 | Consistent indentation (2 spaces) | Required |
| MM-004 | Deep links use correct anchor format (#xxx-NNN) | Required |
| MM-005 | No orphaned nodes (all connected to tree) | Required |
| MM-006 | Topic count matches extraction report | Warning |
| MM-007 | Entity count reasonable vs extraction | Warning |

#### ASCII Mindmap Validation

| Criterion | Check | Weight |
|-----------|-------|--------|
| AM-001 | No line exceeds 80 characters | Required |
| AM-002 | Valid UTF-8 box-drawing characters | Required |
| AM-003 | Legend present at bottom | Required |
| AM-004 | Entity symbols consistent ([->], [?], [!], [*]) | Required |
| AM-005 | Visual hierarchy readable | Warning |

---

## Acceptance Criteria

- [ ] Mermaid validation criteria MM-001 through MM-007 implemented
- [ ] ASCII validation criteria AM-001 through AM-005 implemented
- [ ] Validation is conditional (only when mindmap files exist)
- [ ] Quality score contribution defined
- [ ] Validation criteria documented in ps-critic or quality review

---

## Implementation Notes

### Conditional Validation Logic

```
IF 07-mindmap/mindmap.mmd exists:
    Validate Mermaid criteria MM-001 through MM-007
ENDIF

IF 07-mindmap/mindmap.ascii.txt exists:
    Validate ASCII criteria AM-001 through AM-005
ENDIF
```

### Quality Score Contribution

When mindmaps are present, they should contribute to the overall quality score:
- Core packet files: 80% weight
- Mindmap files: 20% weight (when present)

When mindmaps are not present (--mindmap not used):
- Core packet files: 100% weight

### Files to Modify

1. `skills/problem-solving/agents/ps-critic.md` - Add mindmap validation criteria
   OR
2. Create transcript-specific critic extension in `skills/transcript/`

---

## Related Items

- Parent: [EN-024: Mindmap Pipeline Integration](./EN-024-mindmap-pipeline-integration.md)
- Blocked By: [TASK-244: Pipeline Orchestration](./TASK-244-pipeline-orchestration-update.md)
- Blocks: [TASK-246: Integration Tests](./TASK-246-integration-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ps-critic Validation Update | Implementation | TBD |
| Validation Criteria Doc | Documentation | TBD |

### Verification

- [ ] Mermaid validation works
- [ ] ASCII validation works
- [ ] Conditional logic correct
- [ ] Score contribution correct

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation |
