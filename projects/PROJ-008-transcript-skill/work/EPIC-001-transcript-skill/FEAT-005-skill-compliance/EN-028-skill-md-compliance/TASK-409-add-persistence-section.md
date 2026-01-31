# TASK-409: Add Mandatory Persistence (P-002) section

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-409"
work_type: TASK
title: "Add Mandatory Persistence (P-002) section"
status: BACKLOG
priority: HIGH
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-028"
effort: 1
activity: DOCUMENTATION
```

---

## Description

Add the "Mandatory Persistence (P-002)" section to SKILL.md per PAT-SKILL-001. This explicitly documents the file persistence requirement. Addresses GAP-S-004.

**File to modify:**
- skills/transcript/SKILL.md

**Location:** After "Tool Invocation Examples" section, before "Constitutional Compliance"

---

## Acceptance Criteria

- [ ] "Mandatory Persistence (P-002)" section header present
- [ ] File output requirement explicitly stated
- [ ] Example output paths provided
- [ ] Transient-only output explicitly forbidden

---

## Implementation Notes

**Section to add:**

```markdown
## Mandatory Persistence (P-002)

All transcript skill agents MUST persist their output to files. This ensures:

1. **Context Rot Resistance** - Findings survive session compaction
2. **Knowledge Accumulation** - Artifacts build project knowledge base
3. **Auditability** - Processing can be traced and reviewed
4. **Collaboration** - Outputs can be shared and referenced

### Output Structure

```
transcript-{id}/
├── canonical/                  # Parser output
│   ├── canonical-transcript.json  # Full parsed transcript (reference only)
│   ├── index.json              # Chunk metadata (agents read this)
│   └── chunks/                 # Chunked segments
│       ├── chunk-000.json      # Segments 0-499
│       └── chunk-NNN.json      # Remaining segments
├── extraction-report.json      # Entity extraction results
├── 00-index.md                 # Navigation hub
├── 01-summary.md               # Executive summary
├── 02-transcript.md            # Full transcript (may split)
├── 03-speakers.md              # Speaker directory
├── 04-action-items.md          # Action items with citations
├── 05-decisions.md             # Decisions with context
├── 06-questions.md             # Open questions
├── 07-topics.md                # Topic segments
├── 08-mindmap/                 # Mindmap output
│   ├── mindmap.mmd             # Mermaid format
│   └── mindmap.ascii.txt       # ASCII format
├── _anchors.json               # Anchor registry
└── quality-review.md           # ps-critic output
```

### Anti-Pattern: Transient-Only Output

**FORBIDDEN:** Returning results without file persistence.

```python
# ❌ WRONG - P-002 VIOLATION
return {"entities": extracted_entities}  # Only in context, no file

# ✅ CORRECT - P-002 COMPLIANT
Write(file_path="output/extraction-report.json", content=json.dumps(report))
return {"path": "output/extraction-report.json", "entity_count": len(entities)}
```

**Reference:** Jerry Constitution P-002 (File Persistence - Medium enforcement)
```

---

## Related Items

- Parent: [EN-028: SKILL.md Compliance](./EN-028-skill-md-compliance.md)
- Gap: GAP-S-004 from work-026-e-002
- Reference: Jerry Constitution P-002

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| SKILL.md | Documentation | skills/transcript/SKILL.md |

### Verification

- [ ] Section present with P-002 header
- [ ] Output structure documented
- [ ] Anti-pattern explicitly shown
- [ ] Checklist items S-035 through S-037 pass

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-028 |
