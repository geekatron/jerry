# TASK-413: Create anti-pattern catalog

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Frontmatter

```yaml
id: "TASK-413"
work_type: TASK
title: "Create anti-pattern catalog"
status: BACKLOG
priority: HIGH
assignee: "Claude"
created_at: "2026-01-30T16:00:00Z"
parent_id: "EN-029"
effort: 4
activity: DOCUMENTATION
```

---

## Description

Create anti-pattern catalog with 4+ patterns for PLAYBOOK.md per PAT-PLAYBOOK-001. Each anti-pattern should use ASCII box format with SYMPTOM, CAUSE, IMPACT, and FIX.

**File to modify:**
- skills/transcript/docs/PLAYBOOK.md

**Location:** New L2 "Architecture & Constraints" section

---

## Acceptance Criteria

- [ ] 4+ anti-patterns documented
- [ ] Each uses ASCII box format
- [ ] Each has ❌ WRONG / ✅ CORRECT diagrams
- [ ] References to related DISC-* and BUG-* documents

---

## Implementation Notes

**Anti-patterns to document:**

### AP-T-001: Reading canonical-transcript.json Directly

```
+===================================================================+
| ANTI-PATTERN: Reading canonical-transcript.json Directly         |
+===================================================================+
| SYMPTOM:    ts-extractor receives ~930KB canonical file as input |
| CAUSE:      Skipping chunked architecture (index + chunks/)      |
| IMPACT:     Context window overflow, 99.8% data loss (DISC-009)  |
| FIX:        ALWAYS use index.json + chunks/*.json                |
+===================================================================+

❌ WRONG:
ts-parser → canonical-transcript.json (930KB)
              ↓
         ts-extractor (FAIL - context overflow)

✅ CORRECT:
ts-parser → index.json (8KB) + chunks/ (130KB each)
              ↓
         ts-extractor (SUCCESS - manageable chunks)

**Reference:** DISC-009 - Large File Context Window Analysis
```

### AP-T-002: Skipping index.json Metadata

```
+===================================================================+
| ANTI-PATTERN: Skipping index.json Metadata                       |
+===================================================================+
| SYMPTOM:    Missing speaker list, transcript metadata            |
| CAUSE:      Reading chunks directly without index                |
| IMPACT:     Incomplete entity extraction, missing context        |
| FIX:        ALWAYS read index.json first, then chunks            |
+===================================================================+
```

### AP-T-003: Stats-Array Mismatch

```
+===================================================================+
| ANTI-PATTERN: Stats-Array Mismatch                               |
+===================================================================+
| SYMPTOM:    extraction_stats.questions != len(questions)         |
| CAUSE:      Counting "?" syntactically vs extracting semantically|
| IMPACT:     Quality score failure (BUG-002, 4.2x inflation)      |
| FIX:        INV-EXT-001 - Stats MUST equal array lengths         |
+===================================================================+

❌ WRONG:
questions: [...15 items...]
extraction_stats:
  questions: 63  # Counted all "?" in text

✅ CORRECT:
questions: [...15 items...]
extraction_stats:
  questions: 15  # Equals len(questions)

**Reference:** BUG-002 - Extraction Question Count Discrepancy
```

### AP-T-004: Transient-Only Output

```
+===================================================================+
| ANTI-PATTERN: Transient-Only Output                              |
+===================================================================+
| SYMPTOM:    Agent returns results but no file created            |
| CAUSE:      Not persisting to file system                        |
| IMPACT:     Output lost on context compaction (P-002 violation)  |
| FIX:        ALWAYS write output to files                         |
+===================================================================+

❌ WRONG:
return {"entities": [...]}  # Only in context, no file

✅ CORRECT:
Write(file_path="output/extraction-report.json", content=...)
return {"path": "output/extraction-report.json"}  # File persisted

**Reference:** P-002 (Jerry Constitution)
```

---

## Related Items

- Parent: [EN-029: Documentation Compliance](./EN-029-documentation-compliance.md)
- Gap: GAP-D-002 from work-026-e-002
- References: DISC-009, BUG-002, P-002

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| PLAYBOOK.md | Documentation | skills/transcript/docs/PLAYBOOK.md |

### Verification

- [ ] 4+ anti-patterns present
- [ ] ASCII box format used
- [ ] Checklist items P-024 through P-026 pass

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-30 | Created | Initial creation per EN-029 |
