# TASK-104: Implement/Verify Plain Text Processing (FR-003)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-007 (ts-parser Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-104"
work_type: TASK
title: "Implement/Verify Plain Text Processing (FR-003)"
description: |
  Verify plain text format parsing in ts-parser agent handles
  speaker detection patterns: colon prefixes, brackets, capitalization.

classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-007"

tags:
  - "implementation"
  - "ts-parser"
  - "plain-text"
  - "FR-003"

effort: 1
acceptance_criteria: |
  - Colon prefix pattern (Speaker:) detected
  - Bracket prefix pattern ([Speaker]) detected
  - ALL CAPS speaker names detected
  - Fallback to "Unknown Speaker" when undetected
  - Output matches canonical schema

due_date: null

activity: DEVELOPMENT
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Implement and verify plain text format processing in the ts-parser agent per TDD-ts-parser.md Section 1.3. Plain text (5% of use cases) has no standard format, so we detect speaker patterns heuristically.

### FR-003 Requirements (from TDD)

| Req ID | Description | Priority |
|--------|-------------|----------|
| FR-003.1 | Detect `Speaker:` colon prefix | Must |
| FR-003.2 | Detect `[Speaker]` bracket prefix | Should |
| FR-003.3 | Detect ALL CAPS speaker names | Could |
| FR-003.4 | Fallback to "Unknown Speaker" | Must |
| FR-003.5 | Estimate timestamps from text position | Could |

### Plain Text Pattern Examples

**Colon prefix:**
```
Alice: Good morning everyone.
Bob: Hi Alice! Ready for the meeting?
```

**Bracket prefix:**
```
[Alice] Good morning everyone.
[Bob] Hi Alice! Ready for the meeting?
```

**ALL CAPS:**
```
ALICE
Good morning everyone.

BOB
Hi Alice! Ready for the meeting?
```

**No speaker (fallback):**
```
Good morning everyone.
Hi Alice! Ready for the meeting?
```

### Acceptance Criteria

- [ ] Colon prefix (`Name:`) extracts speaker
- [ ] Bracket prefix (`[Name]`) extracts speaker
- [ ] ALL CAPS pattern (`NAME\n`) extracts speaker
- [ ] Unknown patterns use "Unknown Speaker"
- [ ] Timestamps estimated from text position (if no timestamps)
- [ ] Output matches canonical schema (TDD Section 3)

### Test Cases (from EN-015)

Reference test cases in parser-tests.yaml:
- `txt-001`: Parse plain text with speaker prefixes

### Related Items

- Parent: [EN-007: ts-parser Agent Implementation](./EN-007-vtt-parser.md)
- Blocked By: [TASK-101: Agent alignment](./TASK-101-parser-agent-alignment.md)
- References: [TDD-ts-parser.md Section 1.3](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md)
- Validated By: [TASK-134: Parser tests](../EN-015-transcript-validation/TASK-134-parser-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-parser.md plain text section | Agent | skills/transcript/agents/ts-parser.md |
| Plain text test results | Test Evidence | (link to test output) |

### Verification

- [ ] All FR-003.x requirements implemented
- [ ] All speaker patterns detected correctly
- [ ] Fallback behavior works
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-007 |

