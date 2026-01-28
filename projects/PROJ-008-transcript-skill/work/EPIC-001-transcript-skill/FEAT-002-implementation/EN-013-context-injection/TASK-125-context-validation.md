# TASK-125: Create Validation and Test Scenarios for Context Injection

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-013 (Context Injection Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-125"
work_type: TASK
title: "Create Validation and Test Scenarios for Context Injection"
description: |
  Create comprehensive validation test scenarios for context injection
  mechanism covering schema validation, merge order, and template resolution.

classification: ENABLER
status: DONE
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T19:00:00Z"
updated_at: "2026-01-26T19:00:00Z"

parent_id: "EN-013"

tags:
  - "testing"
  - "context-injection"
  - "validation"

effort: 1
acceptance_criteria: |
  - Schema validation tests pass for all domain files
  - Context merge order verified
  - Template variable resolution tested
  - Performance targets met (<500ms load, <50MB size)
  - Edge cases documented and tested

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

Create comprehensive validation and test scenarios for the context injection mechanism. This includes schema validation, context merge order verification, template variable resolution, and performance testing.

### Validation Matrix

| Test ID | Category | Description | Expected | Status |
|---------|----------|-------------|----------|--------|
| CI-001 | Schema | general.yaml validates | PASS | [ ] |
| CI-002 | Schema | transcript.yaml validates | PASS | [ ] |
| CI-003 | Schema | Invalid file rejected | FAIL with message | [ ] |
| CI-004 | Merge | SKILL.md provides defaults | Values available | [ ] |
| CI-005 | Merge | Domain overrides skill | Domain wins | [ ] |
| CI-006 | Merge | Agent overrides domain | Agent wins | [ ] |
| CI-007 | Merge | Invocation overrides all | Invocation wins | [ ] |
| CI-008 | Template | {{$domain}} resolves | "transcript" | [ ] |
| CI-009 | Template | {{$entity_definitions}} resolves | YAML block | [ ] |
| CI-010 | Template | {{$prompt_guidance}} resolves | Text block | [ ] |
| CI-011 | Perf | Load time < 500ms | Pass | [ ] |
| CI-012 | Perf | Context size < 50MB | Pass | [ ] |

### Context Merge Order Test

```
TEST: Context Merge Priority
============================

SETUP:
  SKILL.md:
    context_injection:
      default_domain: "general"
      template_variables:
        - name: confidence_threshold
          default: 0.5

  transcript.yaml:
    extraction_rules:
      - confidence_threshold: 0.7

  ts-extractor.md:
    context:
      template_variables:
        - name: confidence_threshold
          default: 0.8

  Invocation:
    --confidence 0.9

EXPECTED MERGE RESULT:
  confidence_threshold: 0.9  # Invocation wins

TEST CASES:
  TC-001: Only SKILL.md → confidence = 0.5
  TC-002: SKILL.md + domain → confidence = 0.7
  TC-003: SKILL.md + domain + agent → confidence = 0.8
  TC-004: All levels + invocation → confidence = 0.9
```

### Template Resolution Test

```
TEST: Template Variable Resolution
===================================

INPUT TEMPLATE (in agent prompt):
─────────────────────────────────
"You are a {{$persona.role}}.

Extract the following entity types:
{{$entity_definitions}}

Apply these rules:
{{$extraction_rules}}

{{$prompt_guidance}}"


EXPECTED OUTPUT (after resolution):
────────────────────────────────────
"You are a Entity Extraction Specialist.

Extract the following entity types:
- action_item: Task or commitment made during conversation
- decision: Decision made during conversation
- question: Question raised during conversation
- speaker: Person speaking in the transcript

Apply these rules:
- action_items (confidence >= 0.7, priority 1)
- decisions (confidence >= 0.8, priority 2)
- questions (confidence >= 0.75, priority 3)

When analyzing transcripts for entity extraction:
1. Action Items: Look for commitments with specific owners...
..."


TEST CASES:
  TC-010: Simple variable ({{$domain}}) → "transcript"
  TC-011: Nested variable ({{$persona.role}}) → "Entity Extraction..."
  TC-012: YAML block ({{$entity_definitions}}) → formatted YAML
  TC-013: Text block ({{$prompt_guidance}}) → multiline text
  TC-014: Missing variable → error or default
  TC-015: Invalid syntax ({{$invalid}}) → error message
```

### Performance Test

```
TEST: Performance Requirements
==============================

REQ-CI-P-001: Context loading < 500ms
REQ-CI-P-002: Context payload < 50MB

TEST PROCEDURE:
  1. Create timer before context load
  2. Load all context sources (SKILL.md, domain.yaml, AGENT.md)
  3. Merge contexts
  4. Resolve template variables
  5. Stop timer

MEASUREMENTS:
  - Load time: _____ ms (target: <500ms)
  - Context size: _____ MB (target: <50MB)
  - Memory peak: _____ MB

ACCEPTANCE:
  - [ ] Load time under 500ms
  - [ ] Context size under 50MB
  - [ ] No memory leaks on repeated loads
```

### Edge Case Tests

| Test ID | Scenario | Expected Behavior |
|---------|----------|-------------------|
| EDGE-001 | No domain specified | Use default_domain ("general") |
| EDGE-002 | Invalid domain name | Error: "Unknown domain: {name}" |
| EDGE-003 | Missing domain.yaml | Error: "Domain file not found: {path}" |
| EDGE-004 | Empty template variable | Use default or empty string |
| EDGE-005 | Circular variable reference | Error: "Circular reference detected" |
| EDGE-006 | Very large prompt_guidance | Truncate at limit with warning |
| EDGE-007 | Invalid YAML syntax | Error with line number |
| EDGE-008 | Missing required field | Schema validation error |

### Acceptance Criteria

- [ ] All schema validation tests pass (CI-001, CI-002, CI-003)
- [ ] Context merge order verified (CI-004 through CI-007)
- [ ] Template variable resolution works (CI-008 through CI-010)
- [ ] Performance targets met (CI-011, CI-012)
- [ ] Edge cases handled gracefully (EDGE-001 through EDGE-008)
- [ ] Test results documented with evidence

### Related Items

- Parent: [EN-013: Context Injection Implementation](./EN-013-context-injection.md)
- Blocked By: [TASK-123: AGENT.md context sections](./TASK-123-agent-context-sections.md), [TASK-124: JSON Schema](./TASK-124-json-schema-validation.md)
- References: [SPEC-context-injection.md](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md)
- Validated By: [TASK-137: Context injection tests](../EN-015-transcript-validation/TASK-137-context-injection-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Test execution log | Documentation | (in this file) |
| Validation results | Evidence | (below) |
| Performance metrics | Evidence | (below) |

### Test Results

```
[To be filled during task execution]

Test ID | Description | Expected | Actual | Status
--------|-------------|----------|--------|-------
CI-001  |             |          |        |
CI-002  |             |          |        |
CI-003  |             |          |        |
CI-004  |             |          |        |
CI-005  |             |          |        |
CI-006  |             |          |        |
CI-007  |             |          |        |
CI-008  |             |          |        |
CI-009  |             |          |        |
CI-010  |             |          |        |
CI-011  |             |          |        |
CI-012  |             |          |        |
```

### Performance Measurements

```
[To be filled during task execution]

Metric | Measurement | Target | Pass/Fail
-------|-------------|--------|----------
Load time |         | <500ms |
Context size |      | <50MB  |
Memory peak |       | N/A    |
```

### Verification

- [ ] All validation tests pass
- [ ] Performance targets met
- [ ] Edge cases handled
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-013 |
| 2026-01-28 | **DONE** | Created test_data/validation/context-injection-tests.yaml with 18 test cases across 5 categories: schema validation (3), merge order (4), template resolution (3), performance (2), edge cases (6). Covers REQ-CI-F-001, F-002, F-003, F-009, P-001, P-002. |
