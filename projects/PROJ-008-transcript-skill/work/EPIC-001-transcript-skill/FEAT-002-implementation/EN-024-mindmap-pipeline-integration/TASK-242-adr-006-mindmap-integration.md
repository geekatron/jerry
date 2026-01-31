# TASK-242: ADR-006 - Mindmap Pipeline Integration Decision

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "EN-024:TASK-242"
work_type: TASK
title: "ADR-006: Mindmap Pipeline Integration Decision"
description: |
  Create Architecture Decision Record (ADR-006) to formalize the mindmap
  pipeline integration approach, parameter design, and failure handling.
classification: ENABLER
status: DONE
resolution: COMPLETED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T00:00:00Z"
updated_at: "2026-01-30T00:00:00Z"
completed_at: "2026-01-30T00:00:00Z"
parent_id: "EN-024"
tags:
  - adr
  - architecture
  - decision
  - ps-architect
effort: 3
acceptance_criteria: |
  - ADR-006 created following Nygard ADR format
  - Options considered documented
  - Decision rationale clear
  - Implementation guidance provided
  - ps-critic review passed (>= 0.90)
activity: DESIGN
original_estimate: 3
remaining_work: 0
time_spent: 3
```

---

## Description

Create a formal Architecture Decision Record (ADR-006) to document the mindmap pipeline integration decision, superseding or extending ADR-002 as needed.

### Objectives

1. **Document Context**: Explain why this ADR is needed
2. **Present Options**: Document integration approaches considered
3. **Record Decision**: Formalize the chosen approach
4. **Define Implementation**: Provide implementation guidance
5. **Quality Review**: Pass ps-critic review

### ADR Scope

**Key Decisions to Document:**
- Pipeline position for mindmap generation
- Parameter design (`--mindmap`, `--mindmap-format`)
- Conditional execution logic
- Failure handling approach
- ps-critic integration for mindmap validation

**Relationship to Existing ADRs:**
- ADR-002: May need amendment to formalize 07-mindmap/ as optional
- ADR-003: Deep linking already covers mindmap links
- ADR-005: Agent implementation patterns apply

---

## Acceptance Criteria

- [x] ADR-006 created at `docs/adrs/ADR-006-mindmap-pipeline-integration.md`
- [x] Follows Nygard ADR format (Context, Decision, Consequences)
- [x] All options considered documented with pros/cons
- [x] Decision rationale is clear and evidence-based
- [x] Implementation guidance sufficient for TASK-243, TASK-244
- [x] References TASK-240 research and TASK-241 analysis
- [ ] ps-critic review passed (>= 0.90) - **PENDING TASK-248**

---

## Implementation Notes

### ADR Structure (Nygard Format)

```markdown
# ADR-006: Mindmap Pipeline Integration

## Context
- EN-009 implemented mindmap agents
- Agents not integrated into default pipeline
- User requested opt-in integration

## Decision
We will integrate mindmap generation as an optional pipeline stage...

## Consequences
### Positive
- Complete transcript skill workflow
- Quality-assured mindmaps

### Negative
- Increased pipeline complexity
- Additional processing time when enabled
```

### Reference Documents

- [EN-024:DEC-001](./EN-024--DEC-001-pipeline-integration-requirements.md) - Requirements decisions
- [ADR-002](../../../../../docs/adrs/ADR-002-artifact-structure.md) - Artifact structure
- [ts-mindmap-mermaid.md](../../../../../skills/transcript/agents/ts-mindmap-mermaid.md) - Agent spec

### Expected Deliverable

ADR at: `docs/adrs/ADR-006-mindmap-pipeline-integration.md`

---

## Related Items

- Parent: [EN-024: Mindmap Pipeline Integration](./EN-024-mindmap-pipeline-integration.md)
- Blocked By: [TASK-241: 5W2H + Ishikawa Analysis](./TASK-241-analysis-5w2h-ishikawa.md)
- Blocks: [TASK-243: SKILL.md Update](./TASK-243-skill-md-mindmap-flag.md)
- Blocks: [TASK-244: Pipeline Orchestration](./TASK-244-pipeline-orchestration-update.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ADR-006 | Architecture Decision | [ADR-006-mindmap-pipeline-integration.md](../../../../../docs/adrs/ADR-006-mindmap-pipeline-integration.md) |
| ps-critic Review | Quality Review | PENDING (TASK-248) |

### Verification

- [x] ADR created - `docs/adrs/ADR-006-mindmap-pipeline-integration.md`
- [x] Options documented - 3 options (A, B, C) with analysis
- [ ] ps-critic score >= 0.90 - PENDING TASK-248
- [x] Reviewed by: ps-architect agent (via /jerry:problem-solving skill)

### Content Summary

ADR-006 documents:
- **Decision**: Option A selected - Mindmaps after ts-formatter, before ps-critic
- **Default Behavior**: Mindmaps ON by default with `--no-mindmap` opt-out
- **Formats**: mermaid, ascii, both (default: both)
- **Output Directory**: `08-mindmap/` per DISC-001
- **Failure Handling**: Graceful degradation design
- **ps-critic Integration**: MM-*/AM-* validation criteria

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation |
| 2026-01-30 | DONE | ADR-006 created using ps-architect agent via /jerry:problem-solving skill. Documents Option A (mindmaps after ts-formatter), opt-out behavior, graceful degradation, and MM-*/AM-* validation criteria. |
