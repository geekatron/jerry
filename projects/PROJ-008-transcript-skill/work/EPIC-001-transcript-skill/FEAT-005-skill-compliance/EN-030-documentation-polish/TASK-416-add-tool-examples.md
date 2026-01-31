# TASK-416: Add tool invocation examples to SKILL.md

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-416"
work_type: TASK
title: "Add tool invocation examples to SKILL.md"
status: BACKLOG
priority: LOW
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-030"
effort: 2
activity: DOCUMENTATION
```

---

## Description

Add comprehensive tool invocation examples to SKILL.md including Read, Write, and Bash tool usage. Currently only Bash examples exist. Addresses GAP-S-006: Tool examples limited.

**File to modify:**
- skills/transcript/SKILL.md

**Location:** "Tool Invocation Examples" section

---

## Acceptance Criteria

- [ ] Read tool examples for index.json and chunks
- [ ] Write tool examples for output files
- [ ] Warning about canonical-transcript.json included
- [ ] Bash examples for CLI operations
- [ ] Examples are copy-paste ready

---

## Implementation Notes

**Content to add/enhance:**

```markdown
## Tool Invocation Examples

### Reading Transcript Files

```python
# Read the index.json to understand chunk structure
Read(file_path="output/index.json")

# Read a specific chunk for processing
Read(file_path="output/chunks/chunk-000.json")

# Read extraction report for formatting
Read(file_path="output/extraction-report.json")

# ⚠️ NEVER read canonical-transcript.json (too large for context)
# This causes 99.8% data loss - see DISC-009
```

### Writing Output Files

```python
# Write extraction report
Write(
    file_path="output/extraction-report.json",
    content=json.dumps(extraction_report, indent=2)
)

# Write formatted markdown
Write(
    file_path="output/packet/04-action-items.md",
    content=formatted_actions
)

# Write mindmap output
Write(
    file_path="output/08-mindmap/mindmap.mmd",
    content=mermaid_mindmap
)
```

### Bash for CLI Operations

```bash
# Parse transcript via CLI (Python parser)
uv run jerry transcript parse meeting.vtt --output-dir ./output

# Run with domain context
uv run jerry transcript parse standup.vtt --domain software-engineering

# Disable mindmap generation
uv run jerry transcript parse meeting.vtt --no-mindmap
```
```

---

## Related Items

- Parent: [EN-030: Documentation Polish](./EN-030-documentation-polish.md)
- Gap: GAP-S-006 (Tool examples limited)
- Reference: problem-solving SKILL.md (for tool example format)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| SKILL.md | Documentation | skills/transcript/SKILL.md |

### Verification

- [ ] Read tool examples present
- [ ] Write tool examples present
- [ ] Bash examples present
- [ ] Warning about canonical file included

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-030 |
