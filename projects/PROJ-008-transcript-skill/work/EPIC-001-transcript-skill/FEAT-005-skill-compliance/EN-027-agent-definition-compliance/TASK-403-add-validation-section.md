# TASK-403: Add validation section to all agents

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-403"
work_type: TASK
title: "Add validation section to all agents"
status: BACKLOG
priority: CRITICAL
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-027"
effort: 2
activity: DEVELOPMENT
```

---

## Description

Add the `validation` section to all 5 transcript skill agent YAML frontmatter per PAT-AGENT-001. This addresses GAP-Q-001.

**Files to modify:**
- skills/transcript/agents/ts-parser.md
- skills/transcript/agents/ts-extractor.md
- skills/transcript/agents/ts-formatter.md
- skills/transcript/agents/ts-mindmap-mermaid.md
- skills/transcript/agents/ts-mindmap-ascii.md

**Section template:**

```yaml
validation:
  file_must_exist: true
  post_completion_checks:
    - verify_file_created
    - {agent_specific_check_1}
    - {agent_specific_check_2}
```

---

## Acceptance Criteria

- [ ] All 5 agent files have `validation` section
- [ ] All have `file_must_exist: true`
- [ ] All have `post_completion_checks` array with 3+ items
- [ ] All include `verify_file_created` check

---

## Implementation Notes

**ts-parser validation:**

```yaml
validation:
  file_must_exist: true
  post_completion_checks:
    - verify_file_created
    - verify_index_json_schema
    - verify_chunks_directory_exists
    - verify_segment_count_matches
```

**ts-extractor validation:**

```yaml
validation:
  file_must_exist: true
  post_completion_checks:
    - verify_file_created
    - verify_extraction_report_schema
    - verify_all_entities_have_citations
    - verify_confidence_scores_in_range
    - verify_stats_equal_array_lengths  # INV-EXT-001
```

**ts-formatter validation:**

```yaml
validation:
  file_must_exist: true
  post_completion_checks:
    - verify_file_created
    - verify_packet_structure
    - verify_token_counts_under_limit
    - verify_anchor_registry_complete
    - verify_backlinks_present
```

**ts-mindmap-mermaid validation:**

```yaml
validation:
  file_must_exist: true
  post_completion_checks:
    - verify_file_created
    - verify_mermaid_syntax_valid
    - verify_deep_links_present
    - verify_topic_count_under_limit
```

**ts-mindmap-ascii validation:**

```yaml
validation:
  file_must_exist: true
  post_completion_checks:
    - verify_file_created
    - verify_line_width_under_80
    - verify_legend_present
    - verify_utf8_box_drawing
```

---

## Related Items

- Parent: [EN-027: Agent Definition Compliance](./EN-027-agent-definition-compliance.md)
- Gap: GAP-Q-001 from work-026-e-002

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| All 5 agent .md files | Agent Definitions | skills/transcript/agents/ |

### Verification

- [ ] All files have validation section
- [ ] Checklist items A-026 through A-028 pass

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-027 |
