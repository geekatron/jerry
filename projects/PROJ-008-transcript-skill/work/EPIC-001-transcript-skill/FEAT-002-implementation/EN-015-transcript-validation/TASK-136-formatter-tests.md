# TASK-136: Create Formatter Test Specification

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-015 (Transcript Validation & Test Cases)
-->

---

## Frontmatter

```yaml
id: "TASK-136"
work_type: TASK
title: "Create Formatter Test Specification (formatter-tests.yaml)"
description: |
  Create YAML-based test specification for ts-formatter agent validation.
  Tests 8-file packet structure, token limits, deep linking, and file splitting.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:00:00Z"
updated_at: "2026-01-26T18:00:00Z"

parent_id: "EN-015"

tags:
  - "validation"
  - "testing"
  - "ts-formatter"
  - "ADR-002"

effort: 1
acceptance_criteria: |
  - 8-file packet structure tests (ADR-002)
  - Token limit tests (<35K per file)
  - File splitting tests for large content (ADR-004)
  - Deep linking tests (ADR-003)
  - Backlinks section tests

due_date: null

activity: TESTING
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

Create a comprehensive YAML test specification for validating the ts-formatter agent. Tests verify compliance with ADR-002 (8-file packet), ADR-003 (deep linking), and ADR-004 (file splitting).

### Acceptance Criteria

- [ ] 8-file packet structure test suite
- [ ] Token limit test suite (each file <35K)
- [ ] File splitting test suite (for large.vtt)
- [ ] Deep linking test suite (anchor resolution)
- [ ] Backlinks section test suite
- [ ] Index file completeness tests
- [ ] All tests map to ADR requirements

### 8-File Packet Tests (ADR-002)

| File | Max Tokens | Required |
|------|------------|----------|
| 00-index.md | 5K | Yes |
| 01-summary.md | 10K | Yes |
| 02-speakers.md | 35K | Yes |
| 03-topics.md | 35K | Yes |
| 04-entities.md | 35K | Yes |
| 05-timeline.md | 35K | Yes |
| 06-insights.md | 35K | Yes |
| 07-visualization.md | 35K | Yes |
| 08-workitems.md | 35K | Yes |

### Formatter Assertion Types

| Type | Description | Parameters |
|------|-------------|------------|
| file_exists | Output file created | path |
| file_count | Number of output files | expected, minimum |
| token_count | Tokens in file | path, maximum |
| packet_structure | 8-file structure valid | expected_files (list) |
| anchor_exists | Anchor tag present | file, anchor_id |
| anchor_resolves | Link target exists | source, target |
| backlinks_section | Backlinks populated | file |
| index_complete | Index lists all files | (none) |
| split_files | Large content split | original, split_count |

### Test Suite Structure

```yaml
test_suites:
  packet_structure:
    description: "8-file packet structure tests (ADR-002)"
    tests:
      - id: pkt-001
        name: "Standard meeting produces 8-file packet"
        input: "transcripts/golden/meeting-001.vtt"
        assertions:
          - type: packet_structure
            expected_files:
              - "00-index.md"
              - "01-summary.md"
              - "02-speakers.md"
              - "03-topics.md"
              - "04-entities.md"
              - "05-timeline.md"
              - "06-insights.md"
              - "07-visualization.md"
              - "08-workitems.md"
        requirements: ["ADR-002"]

  token_limits:
    description: "Token limit compliance tests"
    tests:
      - id: tok-001
        name: "All files under 35K tokens"
        input: "transcripts/golden/meeting-001.vtt"
        assertions:
          - type: token_count
            path: "01-summary.md"
            maximum: 10000
          - type: token_count
            path: "02-speakers.md"
            maximum: 35000
        requirements: ["ADR-002"]

  file_splitting:
    description: "Large content splitting tests (ADR-004)"
    tests:
      - id: split-001
        name: "Large transcript triggers file splitting"
        input: "transcripts/edge_cases/large.vtt"
        assertions:
          - type: split_files
            original: "03-topics.md"
            minimum_splits: 2
        requirements: ["ADR-004"]

  deep_linking:
    description: "Bidirectional linking tests (ADR-003)"
    tests:
      - id: link-001
        name: "Entity references resolve to speakers"
        input: "transcripts/golden/meeting-001.vtt"
        assertions:
          - type: anchor_exists
            file: "02-speakers.md"
            anchor_id: "speaker-alice"
          - type: anchor_resolves
            source: "04-entities.md#act-001"
            target: "02-speakers.md#speaker-bob"
        requirements: ["ADR-003"]

  backlinks:
    description: "Backlinks section tests"
    tests:
      - id: back-001
        name: "All files have backlinks section"
        input: "transcripts/golden/meeting-001.vtt"
        assertions:
          - type: backlinks_section
            file: "02-speakers.md"
          - type: backlinks_section
            file: "03-topics.md"
        requirements: ["ADR-003"]
```

### Related Items

- Parent: [EN-015: Transcript Validation](./EN-015-transcript-validation.md)
- Blocked By: [TASK-131: Golden dataset transcripts](./TASK-131-golden-dataset-transcripts.md)
- Tests: [EN-009: ts-formatter Agent](../EN-009-ts-formatter/EN-009-ts-formatter.md)
- References: [ADR-002: 8-File Packet](../../../docs/adrs/ADR-002-artifact-structure.md)
- References: [ADR-003: Bidirectional Deep Linking](../../../docs/adrs/ADR-003-bidirectional-deep-linking.md)
- References: [ADR-004: File Splitting Strategy](../../../docs/adrs/ADR-004-file-splitting-strategy.md)
- References: [TDD-ts-formatter.md](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| formatter-tests.yaml | Test Spec | test_data/validation/formatter-tests.yaml |

### Verification

- [ ] All ADR requirements have corresponding tests
- [ ] Token limit tests cover all file types
- [ ] Large file splitting tested
- [ ] Deep link resolution tested
- [ ] YAML syntax is valid
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-015 |

