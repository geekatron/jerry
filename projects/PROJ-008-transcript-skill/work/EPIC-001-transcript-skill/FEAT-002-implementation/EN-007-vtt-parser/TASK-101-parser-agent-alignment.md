# TASK-101: Verify ts-parser Agent Definition Alignment

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-007 (ts-parser Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-101"
work_type: TASK
title: "Verify ts-parser Agent Definition Alignment"
description: |
  Review and verify that the existing ts-parser agent definition
  (skills/transcript/agents/ts-parser.md) aligns with TDD-ts-parser.md.
  Update if discrepancies found.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-007"

tags:
  - "implementation"
  - "ts-parser"
  - "alignment"

effort: 2
acceptance_criteria: |
  - Agent definition reviewed against TDD-ts-parser.md
  - All FR requirements mapped to agent capabilities
  - Output schema matches TDD Section 3
  - Any discrepancies documented and corrected

due_date: null

activity: DEVELOPMENT
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Review the existing ts-parser agent definition (created in EN-005) and verify alignment with the authoritative TDD-ts-parser.md document. This is the foundation task that all other EN-007 tasks depend on.

### Alignment Checklist

| TDD Section | Agent Capability | Status |
|-------------|------------------|--------|
| 1.1 VTT Processing | VTT format handling | [ ] Verify |
| 1.2 SRT Processing | SRT format handling | [ ] Verify |
| 1.3 Plain Text Processing | Plain text patterns | [ ] Verify |
| 2 Format Detection | Auto-detection logic | [ ] Verify |
| 3 Canonical Schema | Output JSON structure | [ ] Verify |
| 4 Timestamp Normalization | Millisecond conversion | [ ] Verify |
| 5 Encoding Detection | UTF-8/Windows-1252/ISO | [ ] Verify |
| 6 Error Handling | PAT-002 matrix | [ ] Verify |

### Acceptance Criteria

- [ ] Read current ts-parser.md agent definition
- [ ] Compare against TDD-ts-parser.md requirements
- [ ] Verify FormatDetector capability documented
- [ ] Verify VTTProcessor capability documented
- [ ] Verify SRTProcessor capability documented
- [ ] Verify PlainParser capability documented
- [ ] Verify Normalizer capability documented
- [ ] Verify output schema matches TDD Section 3
- [ ] Document any discrepancies in this task file
- [ ] Update agent definition if needed

### Implementation Notes

**Files to Review:**
- `skills/transcript/agents/ts-parser.md` (agent definition)
- `docs/TDD-ts-parser.md` (authoritative design)

**Key Alignment Points:**
1. Prompt structure matches TDD guidance
2. Context injection sections reference SPEC-context-injection.md
3. Error handling follows PAT-002 (defensive parsing)
4. Output format exactly matches canonical schema

### Related Items

- Parent: [EN-007: ts-parser Agent Implementation](./EN-007-vtt-parser.md)
- References: [TDD-ts-parser.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md)
- Blocks: TASK-102, TASK-103, TASK-104

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-parser.md (verified) | Agent | skills/transcript/agents/ts-parser.md |
| Alignment notes | Documentation | (in this file) |

### Verification

- [ ] TDD Section 1 requirements covered
- [ ] TDD Section 2 requirements covered
- [ ] TDD Section 3 schema matches
- [ ] TDD Section 4-6 requirements covered
- [ ] Reviewed by: (pending)

### Alignment Notes (Findings)

```
[To be filled during task execution]

TDD Section | Finding | Action Taken
------------|---------|-------------
(record findings here)
```

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-007 |

