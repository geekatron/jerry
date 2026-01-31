# TASK-401: Add capabilities section to all agents

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-401"
work_type: TASK
title: "Add capabilities section to all agents"
status: BACKLOG
priority: CRITICAL
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-027"
effort: 1.5
activity: DEVELOPMENT
```

---

## Description

Add the `capabilities` section to all 5 transcript skill agent YAML frontmatter per PAT-AGENT-001.

**Files to modify:**
- skills/transcript/agents/ts-parser.md
- skills/transcript/agents/ts-extractor.md
- skills/transcript/agents/ts-formatter.md
- skills/transcript/agents/ts-mindmap-mermaid.md
- skills/transcript/agents/ts-mindmap-ascii.md

**Section template:**

```yaml
capabilities:
  allowed_tools:
    - Read
    - Write
    - Glob
    - Grep
    - Bash
  output_formats: [markdown, json]
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Return transient output only (P-002)"
```

---

## Acceptance Criteria

- [ ] All 5 agent files have `capabilities` section
- [ ] All have `allowed_tools` array with agent-appropriate tools
- [ ] All have `output_formats` array
- [ ] All have `forbidden_actions` with P-003, P-020, P-002 violations listed

---

## Implementation Notes

**ts-parser capabilities:**

```yaml
capabilities:
  allowed_tools:
    - Read
    - Write
    - Bash
    - Glob
  output_formats: [json]
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Return transient output only (P-002)"
    - "Skip Python parser for VTT files"
```

**ts-extractor capabilities:**

```yaml
capabilities:
  allowed_tools:
    - Read
    - Write
    - Glob
    - Grep
  output_formats: [json]
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Return transient output only (P-002)"
    - "Read canonical-transcript.json (AP-T-001)"
    - "Extract without citations (P-001)"
```

**ts-formatter capabilities:**

```yaml
capabilities:
  allowed_tools:
    - Read
    - Write
    - Glob
  output_formats: [markdown, json]
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Return transient output only (P-002)"
    - "Exceed 35K token limit per file"
```

---

## Related Items

- Parent: [EN-027: Agent Definition Compliance](./EN-027-agent-definition-compliance.md)
- Gap: GAP-A-003 from work-026-e-002

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| All 5 agent .md files | Agent Definitions | skills/transcript/agents/ |

### Verification

- [ ] All files have capabilities section
- [ ] Checklist items A-012 through A-017 pass

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-027 |
