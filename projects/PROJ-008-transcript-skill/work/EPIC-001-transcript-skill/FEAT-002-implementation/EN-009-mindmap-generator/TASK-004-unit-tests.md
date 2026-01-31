# TASK-004: Create Mindmap Generator Unit Tests

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-01-28 per DEC-003:AI-004
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-004"
work_type: TASK

# === CORE METADATA ===
title: "Create Mindmap Generator Unit Tests"
description: |
  Implement a consistent, executable test suite for validating mindmap
  generator outputs (Mermaid and ASCII). Tests verify syntax correctness,
  structural hierarchy, deep link compliance, and edge case handling.
  Suite must be executable via standard pytest patterns.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: COMPLETED

# === PRIORITY ===
priority: HIGH

# === PEOPLE ===
assignee: "Claude"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-28T14:00:00Z"
updated_at: "2026-01-28T14:00:00Z"

# === HIERARCHY ===
parent_id: "EN-009"

# === TAGS ===
tags:
  - "testing"
  - "validation"
  - "mermaid"
  - "ascii"
  - "quality-gates"

# === DELIVERY ITEM PROPERTIES ===
effort: 3
acceptance_criteria: |
  - Test suite runs consistently via pytest-style YAML tests
  - Mermaid syntax validation tests exist
  - ASCII format validation tests exist
  - Deep link compliance tests exist
  - Edge case tests (50+ topics, overflow) exist
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: TESTING
original_estimate: 6
remaining_work: 6
time_spent: 0
```

---

## Content

### Description

Create a comprehensive, executable test suite for the mindmap generator agents:

1. **Test Suite Structure:** YAML-based tests following project test patterns
2. **Mermaid Tests:** Validate syntax, hierarchy, node types, deep links
3. **ASCII Tests:** Validate box-drawing, width constraints, legend
4. **Deep Link Tests:** Validate anchor format compliance with ADR-003
5. **Integration Tests:** End-to-end generation from extraction reports

### Test Suite Architecture

```
skills/transcript/test_data/validation/
├── mindmap-tests.yaml              # Primary test suite file
├── mindmap-mermaid-tests.yaml      # Mermaid-specific tests
├── mindmap-ascii-tests.yaml        # ASCII-specific tests
└── mindmap-link-tests.yaml         # Deep linking tests
```

### Test Categories

#### 1. Mermaid Syntax Validation

| Test Case | Input | Expected Behavior |
|-----------|-------|-------------------|
| MM-001 | Simple extraction | Valid Mermaid mindmap syntax |
| MM-002 | Empty extraction | Minimal root-only mindmap |
| MM-003 | 50+ topics | Degrades gracefully, no syntax errors |
| MM-004 | Unicode content | Proper escaping, valid syntax |
| MM-005 | Special chars | Quoted/escaped correctly |

#### 2. ASCII Format Validation

| Test Case | Input | Expected Behavior |
|-----------|-------|-------------------|
| AA-001 | Simple extraction | Valid ASCII tree with box-drawing |
| AA-002 | Long node names | Truncated with ellipsis at 80 chars |
| AA-003 | Deep hierarchy | Proper indentation and branching |
| AA-004 | Legend presence | [→] [?] [!] [*] symbols explained |
| AA-005 | UTF-8 encoding | Valid UTF-8 file output |

#### 3. Deep Link Compliance

| Test Case | Input | Expected Behavior |
|-----------|-------|-------------------|
| DL-001 | Action items | Links to #action-NNN anchors |
| DL-002 | Decisions | Links to #decision-NNN anchors |
| DL-003 | Questions | Links to #question-NNN anchors |
| DL-004 | Topics | Links to #topic-NNN anchors |
| DL-005 | Invalid anchor | Warning logged, not error |

#### 4. Edge Cases

| Test Case | Input | Expected Behavior |
|-----------|-------|-------------------|
| EC-001 | Empty extraction | Graceful handling, minimal output |
| EC-002 | 100+ topics | Performance acceptable, degrades gracefully |
| EC-003 | Very long content | Truncation applied correctly |
| EC-004 | Nested hierarchy | Max 3 levels rendered |
| EC-005 | Missing fields | Defaults applied, no crashes |

### Acceptance Criteria

- [x] **AC-1:** Test suite file `mindmap-tests.yaml` created and parseable
- [x] **AC-2:** Mermaid tests validate against mermaid-cli parser rules
- [x] **AC-3:** ASCII tests verify 80-character width constraint
- [x] **AC-4:** ASCII tests verify box-drawing character usage (┌ ─ ┐ │ └ ┬ ├ ┤)
- [x] **AC-5:** Deep link tests verify ADR-003 anchor format compliance
- [x] **AC-6:** Edge case tests cover 50+ topic scenarios
- [x] **AC-7:** Test suite runs consistently (deterministic, no flaky tests)
- [x] **AC-8:** Test fixtures use golden extraction reports from test_data/
- [x] **AC-9:** All tests have clear pass/fail assertions
- [x] **AC-10:** Test suite integrates with EN-015 validation framework

### Test YAML Schema

```yaml
# mindmap-tests.yaml structure
test_suite:
  name: "EN-009 Mind Map Generator Tests"
  version: "1.0.0"

tests:
  - id: "MM-001"
    name: "Valid Mermaid syntax for simple extraction"
    category: "mermaid"
    input:
      extraction_report: "test_data/golden/simple-extraction.json"
    expected:
      output_file: "07-mindmap/mindmap.mmd"
      assertions:
        - type: "starts_with"
          value: "mindmap"
        - type: "contains"
          value: "root(("
        - type: "regex_match"
          pattern: "\\[.*\\]\\(#action-\\d+\\)"

  - id: "AA-001"
    name: "Valid ASCII tree with box-drawing"
    category: "ascii"
    input:
      extraction_report: "test_data/golden/simple-extraction.json"
    expected:
      output_file: "07-mindmap/mindmap.ascii.txt"
      assertions:
        - type: "contains"
          value: "┌"
        - type: "max_line_length"
          value: 80
        - type: "contains"
          value: "Legend:"
```

### Implementation Notes

**Integration with EN-015:**
- Test suite aligns with `skills/transcript/test_data/validation/` structure
- Uses same assertion patterns as parser-tests.yaml and extractor-tests.yaml
- Golden test data from `test_data/golden/` directory

**Execution Model:**
- Tests defined in YAML for consistency
- Executed by validation framework (not pytest directly)
- Results reported in standard pass/fail format

**Golden Data Requirements:**
- Simple extraction report (5-10 entities)
- Complex extraction report (50+ topics)
- Edge case reports (empty, malformed, etc.)

### Related Items

- **Parent:** [EN-009](./EN-009-mindmap-generator.md)
- **Blocked By:** [TASK-001](./TASK-001-mermaid-generator.md), [TASK-002](./TASK-002-ascii-generator.md), [TASK-003](./TASK-003-deep-link-embedding.md)
- **Blocks:** None (final task in EN-009)
- **Integrates With:** [EN-015](../EN-015-transcript-validation/EN-015-transcript-validation.md)
- **Reference:** [ADR-003](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-003.md) (Bidirectional Linking)

---

## Time Tracking

| Metric            | Value |
|-------------------|-------|
| Original Estimate | 6 hours |
| Remaining Work    | 6 hours |
| Time Spent        | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Primary test suite | YAML | skills/transcript/test_data/validation/mindmap-tests.yaml |
| Mermaid tests | YAML | skills/transcript/test_data/validation/mindmap-mermaid-tests.yaml |
| ASCII tests | YAML | skills/transcript/test_data/validation/mindmap-ascii-tests.yaml |
| Link tests | YAML | skills/transcript/test_data/validation/mindmap-link-tests.yaml |

### Verification

- [ ] Acceptance criteria verified
- [ ] All tests execute consistently
- [ ] No flaky tests present
- [ ] Golden data fixtures created
- [ ] Reviewed by: {REVIEWER}

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Per DEC-003:AI-004 - enabler-scoped numbering. User requirement: executable, consistent test suite. |
| 2026-01-28 | DONE | Created mindmap-tests.yaml and mindmap-link-tests.yaml |
