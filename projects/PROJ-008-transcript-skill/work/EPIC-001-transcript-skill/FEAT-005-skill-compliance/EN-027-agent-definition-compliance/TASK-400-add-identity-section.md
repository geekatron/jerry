# TASK-400: Add identity section to all agents

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-400"
work_type: TASK
title: "Add identity section to all agents"
status: BACKLOG
priority: CRITICAL
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-027"
effort: 1
activity: DEVELOPMENT
```

---

## Description

Add the `identity` section to all 5 transcript skill agent YAML frontmatter per PAT-AGENT-001.

**Files to modify:**
- skills/transcript/agents/ts-parser.md
- skills/transcript/agents/ts-extractor.md
- skills/transcript/agents/ts-formatter.md
- skills/transcript/agents/ts-mindmap-mermaid.md
- skills/transcript/agents/ts-mindmap-ascii.md

**Section template:**

```yaml
identity:
  role: "{Role Title}"
  expertise:
    - "{expertise-1}"
    - "{expertise-2}"
    - "{expertise-3}"
  cognitive_mode: "convergent"  # All ts-* agents are convergent
```

---

## Acceptance Criteria

- [ ] ts-parser.md has `identity` section with role, expertise (3+), cognitive_mode
- [ ] ts-extractor.md has `identity` section with role, expertise (3+), cognitive_mode
- [ ] ts-formatter.md has `identity` section with role, expertise (3+), cognitive_mode
- [ ] ts-mindmap-mermaid.md has `identity` section with role, expertise (3+), cognitive_mode
- [ ] ts-mindmap-ascii.md has `identity` section with role, expertise (3+), cognitive_mode
- [ ] All cognitive_mode values are "convergent"

---

## Implementation Notes

**ts-parser identity example:**

```yaml
identity:
  role: "Transcript Parser and Orchestrator"
  expertise:
    - "VTT/SRT format parsing"
    - "Python parser delegation"
    - "Schema validation"
    - "Chunking strategy implementation"
  cognitive_mode: "convergent"
```

**ts-extractor identity example:**

```yaml
identity:
  role: "Entity Extraction Specialist"
  expertise:
    - "Named Entity Recognition"
    - "Confidence scoring with tiered extraction"
    - "Citation generation for anti-hallucination"
    - "Speaker identification using PAT-003 4-pattern chain"
  cognitive_mode: "convergent"
```

---

## Related Items

- Parent: [EN-027: Agent Definition Compliance](./EN-027-agent-definition-compliance.md)
- Gap: GAP-A-001 from work-026-e-002

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-parser.md | Agent Definition | skills/transcript/agents/ts-parser.md |
| ts-extractor.md | Agent Definition | skills/transcript/agents/ts-extractor.md |
| ts-formatter.md | Agent Definition | skills/transcript/agents/ts-formatter.md |
| ts-mindmap-mermaid.md | Agent Definition | skills/transcript/agents/ts-mindmap-mermaid.md |
| ts-mindmap-ascii.md | Agent Definition | skills/transcript/agents/ts-mindmap-ascii.md |

### Verification

- [ ] All files have identity section
- [ ] Checklist items A-005 through A-008 pass

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-027 |
