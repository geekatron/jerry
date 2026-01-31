# TASK-402: Add guardrails section to all agents

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-402"
work_type: TASK
title: "Add guardrails section to all agents"
status: BACKLOG
priority: CRITICAL
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-027"
effort: 3
activity: DEVELOPMENT
```

---

## Description

Add the `guardrails` section to all 5 transcript skill agent YAML frontmatter per PAT-AGENT-001. This addresses GAP-A-004 which has the highest risk score (192 RPN).

**Files to modify:**
- skills/transcript/agents/ts-parser.md
- skills/transcript/agents/ts-extractor.md
- skills/transcript/agents/ts-formatter.md
- skills/transcript/agents/ts-mindmap-mermaid.md
- skills/transcript/agents/ts-mindmap-ascii.md

**Section template:**

```yaml
guardrails:
  input_validation:
    {agent_specific_rules}
  output_filtering:
    - no_secrets_in_output
    - {agent_specific_filter}
  fallback_behavior: warn_and_retry
```

---

## Acceptance Criteria

- [ ] All 5 agent files have `guardrails` section
- [ ] All have `input_validation` with agent-specific rules
- [ ] All have `output_filtering` with at least 2 filters
- [ ] All have `fallback_behavior` set to appropriate value
- [ ] Input validation prevents known failure modes (e.g., reading canonical-transcript.json)

---

## Implementation Notes

**ts-parser guardrails example:**

```yaml
guardrails:
  input_validation:
    file_exists: true
    supported_formats: [".vtt", ".srt", ".txt"]
    max_file_size_mb: 50
  output_filtering:
    - no_secrets_in_output
    - validate_json_output
  fallback_behavior: warn_and_retry
```

**ts-extractor guardrails example:**

```yaml
guardrails:
  input_validation:
    index_json_schema: "schemas/index.schema.json"
    chunk_format: "^chunk-\\d{3}\\.json$"
    minimum_segments: 1
    forbidden_files:
      - "canonical-transcript.json"  # AP-T-001 prevention
  output_filtering:
    - no_secrets_in_citations
    - all_extractions_must_have_citations
    - confidence_range_0_to_1
    - stats_must_equal_array_lengths  # INV-EXT-001
  fallback_behavior: warn_and_retry
```

**ts-formatter guardrails example:**

```yaml
guardrails:
  input_validation:
    extraction_report_schema: "schemas/extraction-report.schema.json"
    index_json_required: true
  output_filtering:
    - no_secrets_in_output
    - token_count_under_limit
    - split_at_semantic_boundaries
  fallback_behavior: warn_and_retry
```

---

## Related Items

- Parent: [EN-027: Agent Definition Compliance](./EN-027-agent-definition-compliance.md)
- Gap: GAP-A-004 from work-026-e-002 (192 RPN - CRITICAL)
- Anti-Pattern: AP-T-001 (reading canonical-transcript.json)

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

- [ ] All files have guardrails section
- [ ] Checklist items A-018 through A-021 pass
- [ ] ts-extractor forbids canonical-transcript.json

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-027. Highest priority task (192 RPN). |
