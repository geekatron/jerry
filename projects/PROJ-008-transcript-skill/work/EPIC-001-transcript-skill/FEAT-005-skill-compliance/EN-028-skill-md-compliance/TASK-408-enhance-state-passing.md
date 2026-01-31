# TASK-408: Enhance State Passing section with session_context

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-408"
work_type: TASK
title: "Enhance State Passing section with session_context"
status: BACKLOG
priority: HIGH
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-028"
effort: 2
activity: DOCUMENTATION
```

---

## Description

Enhance the "State Passing Between Agents" section in SKILL.md to include session_context schema reference and versioning per PAT-SKILL-001. Addresses GAP-S-003.

**File to modify:**
- skills/transcript/SKILL.md

**Location:** Existing "State Passing Between Agents" section

---

## Acceptance Criteria

- [ ] State key registry table includes schema version column
- [ ] Session context schema reference added
- [ ] Schema version documented as "1.0.0"
- [ ] Cross-skill handoff capability documented

---

## Implementation Notes

**Enhanced State Passing section:**

```markdown
## State Passing Between Agents

### State Key Registry

| Agent | Output Key | Provides | Schema Version |
|-------|------------|----------|----------------|
| ts-parser | `ts_parser_output` | canonical_json_path, index_json_path, chunks_dir, format_detected, parsing_method | 2.0.0 |
| ts-extractor | `ts_extractor_output` | extraction_report_path, action_count, decision_count, question_count, high_confidence_ratio | 1.3.0 |
| ts-formatter | `ts_formatter_output` | packet_path, files_created, total_tokens, split_files | 1.1.0 |
| ts-mindmap-* | `ts_mindmap_output` | enabled, format_requested, mermaid.path, ascii.path, overall_status | 1.0.0 |
| ps-critic | `quality_output` | quality_score, passed, issues, recommendations | 1.0.0 |

### Session Context Schema

All transcript agents use the universal session context schema for cross-skill handoffs:

```yaml
session_context:
  schema: "docs/schemas/session_context.json"
  schema_version: "1.0.0"
  input_validation: true
  output_validation: true
```

This enables seamless handoffs to other Jerry skills:
- **problem-solving:** ps-critic validates transcript quality
- **orchestration:** Multi-skill workflow coordination
- **nasa-se:** Requirements traceability from meeting transcripts

### State Schema Example

```yaml
ts_parser_output:
  schema_version: "2.0.0"
  canonical_json_path: "output/canonical-transcript.json"
  index_json_path: "output/index.json"
  chunks_dir: "output/chunks/"
  chunk_count: 7
  format_detected: "vtt"
  parsing_method: "python"
  segment_count: 3071
  speaker_count: 4
  validation_passed: true
```

### Breaking Change Policy

- Schema version follows semver (MAJOR.MINOR.PATCH)
- MAJOR version bump = breaking change, requires migration
- MINOR version bump = backward-compatible additions
- PATCH version bump = fixes only
```

---

## Related Items

- Parent: [EN-028: SKILL.md Compliance](./EN-028-skill-md-compliance.md)
- Gap: GAP-S-003 from work-026-e-002
- Depends on: TASK-405 (session_context in agents)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| SKILL.md | Documentation | skills/transcript/SKILL.md |

### Verification

- [ ] State registry has schema version column
- [ ] Session context schema documented
- [ ] Checklist items S-019 through S-027 pass

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-028 |
