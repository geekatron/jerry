# TASK-240: Research - Current Pipeline State Analysis

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "EN-024:TASK-240"
work_type: TASK
title: "Research: Current Pipeline State Analysis"
description: |
  Analyze the current transcript skill pipeline to understand state passing,
  agent invocation patterns, and integration points for mindmap generation.
classification: ENABLER
status: DONE
resolution: COMPLETED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T00:00:00Z"
updated_at: "2026-01-28T00:00:00Z"
parent_id: "EN-024"
tags:
  - research
  - pipeline
  - state-analysis
effort: 2
acceptance_criteria: |
  - Document current pipeline stages and their inputs/outputs
  - Map state passing between agents
  - Identify integration point for mindmap agents
  - Analyze SKILL.md parameter handling
activity: RESEARCH
original_estimate: 2
remaining_work: 0
time_spent: 2
```

---

## Description

Research and document the current transcript skill pipeline architecture to understand how mindmap generation should be integrated.

### Objectives

1. **Pipeline Stage Mapping**: Document each stage (ts-parser, ts-extractor, ts-formatter, ps-critic) with inputs/outputs
2. **State Passing Analysis**: Understand how state flows between agents (output keys, file paths)
3. **Integration Point Identification**: Determine where mindmap generation fits in the flow
4. **Parameter Analysis**: Review SKILL.md parameter handling to understand how --mindmap flag should work
5. **Error Handling Patterns**: Document existing error handling for reference

### Scope

**In Scope:**
- SKILL.md current structure analysis
- Agent definition files (ts-parser.md, ts-extractor.md, ts-formatter.md)
- State schema documentation
- Invocation protocol patterns

**Out of Scope:**
- Implementation changes
- ADR creation (that's TASK-242)

---

## Acceptance Criteria

- [x] Pipeline stages documented with inputs/outputs
- [x] State passing schema documented
- [x] Integration point for mindmaps identified
- [x] SKILL.md parameter patterns analyzed
- [x] Research artifact created in `research/` subdirectory

---

## Implementation Notes

### Files to Analyze

1. `skills/transcript/SKILL.md` - Main skill definition
2. `skills/transcript/agents/ts-parser.md` - Parser agent
3. `skills/transcript/agents/ts-extractor.md` - Extractor agent
4. `skills/transcript/agents/ts-formatter.md` - Formatter agent
5. `skills/transcript/agents/ts-mindmap-mermaid.md` - Mermaid mindmap agent
6. `skills/transcript/agents/ts-mindmap-ascii.md` - ASCII mindmap agent
7. `skills/transcript/docs/PLAYBOOK.md` - Execution playbook

### Expected Deliverable

Research document at: `EN-024-mindmap-pipeline-integration/research/pipeline-state-analysis.md`

---

## Related Items

- Parent: [EN-024: Mindmap Pipeline Integration](./EN-024-mindmap-pipeline-integration.md)
- Blocks: [TASK-241: 5W2H + Ishikawa Analysis](./TASK-241-analysis-5w2h-ishikawa.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Pipeline State Analysis | Research | [research/TASK-240-pipeline-state-research.md](./research/TASK-240-pipeline-state-research.md) |

### Verification

- [x] Research document created
- [x] All pipeline stages documented
- [x] All 7 integration gaps identified (GAP-001 through GAP-007)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation |
| 2026-01-28 | DONE | Research complete. 7 gaps identified. Integration point: after ts-formatter, before ps-critic. |
| 2026-01-30 | Updated | Additional research: Discovered file numbering discrepancy (07 vs 08). Created [DISC-001](./EN-024--DISC-001-mindmap-directory-numbering-discrepancy.md). Corrected output to `08-mindmap/`. |

---

## Discoveries

- [EN-024:DISC-001](./EN-024--DISC-001-mindmap-directory-numbering-discrepancy.md) - Mindmap Directory Numbering Discrepancy (07 → 08)
