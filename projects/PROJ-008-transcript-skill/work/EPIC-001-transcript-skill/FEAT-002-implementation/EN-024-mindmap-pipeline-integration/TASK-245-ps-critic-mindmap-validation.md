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
status: DONE
resolution: COMPLETED
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T00:00:00Z"
updated_at: "2026-01-30T00:00:00Z"
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
remaining_work: 0
time_spent: 2
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

- [x] Mermaid validation criteria MM-001 through MM-007 implemented
- [x] ASCII validation criteria AM-001 through AM-005 implemented
- [x] Validation is conditional (only when mindmap files exist)
- [x] Quality score contribution defined
- [x] Validation criteria documented in ps-critic or quality review

---

## Implementation Notes

### Conditional Validation Logic (Per ADR-006 Section 5.5)

```
# Default: Mindmaps are generated unless --no-mindmap is used
IF 08-mindmap/mindmap.mmd exists:
    Validate Mermaid criteria MM-001 through MM-007
ENDIF

IF 08-mindmap/mindmap.ascii.txt exists:
    Validate ASCII criteria AM-001 through AM-005
ENDIF

# Note: Output directory is 08-mindmap/ per DISC-001 numbering correction
```

### Quality Score Contribution (Per ADR-006 Section 5.5)

When mindmaps are present (default behavior), they contribute to overall quality score:
- Core packet files: 85% weight
- Mindmap files: 15% weight (when present)

When mindmaps are not present (`--no-mindmap` opt-out used):
- Core packet files: 100% weight
- No penalty for absence when explicitly opted out

### Implementation Approach (Per User Decision)

**Architecture Choice:** Option B - Transcript-specific critic extension (not modifying shared ps-critic.md)
**Implementation Style:** Option A - Document criteria as agent instructions (not code validators)

**Rationale:**
- Keeps shared ps-critic.md generic and reusable across skills
- Transcript-specific criteria isolated in transcript skill directory
- Agent-guided validation (LLM interprets rubrics) rather than code validators
- Aligns with Jerry's agent-first architecture

### Files Created

1. `skills/transcript/validation/ts-critic-extension.md` - Transcript-specific criteria for ps-critic
   - MM-001 through MM-007 (Mermaid validation)
   - AM-001 through AM-005 (ASCII validation)
   - Quality score composition (85/15 split)
   - Evaluation rubrics for agent guidance
   - Integration protocol with ps-critic

---

## Related Items

- Parent: [EN-024: Mindmap Pipeline Integration](./EN-024-mindmap-pipeline-integration.md)
- Blocked By: [TASK-244: Pipeline Orchestration](./TASK-244-pipeline-orchestration-update.md)
- **ADR Reference:** [ADR-006: Mindmap Pipeline Integration](../../../../../docs/adrs/ADR-006-mindmap-pipeline-integration.md) - Section 5.5 (ps-critic Integration)
- Blocks: [TASK-246: Integration Tests](./TASK-246-integration-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Transcript Critic Extension | Implementation | [skills/transcript/validation/ts-critic-extension.md](../../../../../skills/transcript/validation/ts-critic-extension.md) |
| MM-001..007 Criteria | Documentation | ts-critic-extension.md Section "Mermaid Mindmap Criteria" |
| AM-001..005 Criteria | Documentation | ts-critic-extension.md Section "ASCII Mindmap Criteria" |
| Quality Score Calculation | Documentation | ts-critic-extension.md Section "Quality Score Calculation" |

### Verification

- [x] Mermaid validation works - MM-001..007 criteria with evaluation rubrics
- [x] ASCII validation works - AM-001..005 criteria with evaluation rubrics
- [x] Conditional logic correct - IF file_exists() pattern documented
- [x] Score contribution correct - 85/15 split per ADR-006 Section 5.5

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation |
| 2026-01-30 | Updated | **ADR-006 ALIGNMENT**: Updated validation logic path from 07-mindmap/ to 08-mindmap/ per DISC-001. Updated quality score contribution (85/15) per ADR-006 Section 5.5. Added note about opt-out behavior (--no-mindmap). |
| 2026-01-30 | **DONE** | **TASK COMPLETE**: Created `skills/transcript/validation/ts-critic-extension.md` with MM-001..007 (Mermaid) and AM-001..005 (ASCII) validation criteria as agent instructions. **Architecture Decision**: Option B (transcript-specific extension) with Option A implementation (agent guidance, not code validators). Per user decision, this approach keeps shared ps-critic.md generic while providing transcript-specific validation criteria. **Evidence**: ts-critic-extension.md contains: evaluation rubrics for all 12 criteria, conditional validation logic, quality score calculation (85/15 split), integration protocol with ps-critic, L0/L1/L2 documentation. |
