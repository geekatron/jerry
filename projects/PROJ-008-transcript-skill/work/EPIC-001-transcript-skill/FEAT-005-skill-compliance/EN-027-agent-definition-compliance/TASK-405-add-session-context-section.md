# TASK-405: Add session_context section to all agents

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-405"
work_type: TASK
title: "Add session_context section to all agents"
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

Add the `session_context` section to all 5 transcript skill agent YAML frontmatter per PAT-AGENT-001. This enables cross-skill handoffs (e.g., to ps-critic). Addresses GAP-A-009.

**Files to modify:**
- skills/transcript/agents/ts-parser.md
- skills/transcript/agents/ts-extractor.md
- skills/transcript/agents/ts-formatter.md
- skills/transcript/agents/ts-mindmap-mermaid.md
- skills/transcript/agents/ts-mindmap-ascii.md

**Section template:**

```yaml
session_context:
  schema: "docs/schemas/session_context.json"
  schema_version: "1.0.0"
  input_validation: true
  output_validation: true
  on_receive:
    - check_schema_version_matches
    - verify_target_agent_matches
    - extract_key_findings
    - process_blockers
  on_send:
    - populate_key_findings
    - calculate_confidence
    - list_artifacts
    - set_timestamp
```

---

## Acceptance Criteria

- [ ] All 5 agent files have `session_context` section
- [ ] All have `schema` and `schema_version` fields
- [ ] All have `input_validation: true` and `output_validation: true`
- [ ] All have `on_receive` and `on_send` arrays with 4+ actions each

---

## Implementation Notes

**Standard session_context section (all agents):**

```yaml
session_context:
  schema: "docs/schemas/session_context.json"
  schema_version: "1.0.0"
  input_validation: true
  output_validation: true
  on_receive:
    - check_schema_version_matches
    - verify_target_agent_matches
    - extract_key_findings
    - process_blockers
  on_send:
    - populate_key_findings
    - calculate_confidence
    - list_artifacts
    - set_timestamp
```

**Agent-specific on_send additions:**

**ts-parser:**
```yaml
on_send:
  - populate_key_findings
  - set_parsing_method  # python | llm
  - set_chunk_count
  - list_artifacts
  - set_timestamp
```

**ts-extractor:**
```yaml
on_send:
  - populate_key_findings
  - calculate_confidence
  - set_entity_counts
  - list_artifacts
  - set_timestamp
```

**ts-formatter:**
```yaml
on_send:
  - populate_key_findings
  - set_packet_path
  - set_token_counts
  - list_artifacts
  - set_timestamp
```

---

## Related Items

- Parent: [EN-027: Agent Definition Compliance](./EN-027-agent-definition-compliance.md)
- Gap: GAP-A-009 from work-026-e-002
- Reference: WI-SAO-002 (session_context spec)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| All 5 agent .md files | Agent Definitions | skills/transcript/agents/ |

### Verification

- [ ] All files have session_context section
- [ ] Checklist items A-038 through A-043 pass

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-027 |
