# TASK-138: EN-008 Deferred Minor Findings

<!--
TEMPLATE: Task (DRAFT)
SOURCE: ONTOLOGY-v1.md Section 3.4.6, DEC-003
VERSION: 0.1.0
STATUS: DRAFT
ORIGIN: EN-008 GATE-5 Quality Review (ps-critic, nse-qa)

DESCRIPTION:
  Address minor findings deferred from EN-008 quality reviews.
  These items were deemed non-blocking for GATE-5 but should be
  addressed during EN-015 implementation.

EXTENDS: DeliveryItem -> WorkItem
-->

---

## Frontmatter

```yaml
# === IDENTITY (Auto-generated, Immutable) ===
id: "TASK-138"
work_type: TASK

# === CORE METADATA ===
title: "EN-008 Deferred Minor Findings"
description: |
  Address minor findings from EN-008 GATE-5 quality reviews (ps-critic and nse-qa)
  that were deferred as non-blocking but should be remediated during EN-015
  validation framework implementation.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: BACKLOG
resolution: null

# === PRIORITY ===
priority: LOW

# === PEOPLE ===
assignee: "Claude"
created_by: "Claude"

# === TIMESTAMPS (Auto-managed) ===
created_at: "2026-01-28T08:45:00Z"
updated_at: "2026-01-28T08:45:00Z"

# === HIERARCHY ===
parent_id: "EN-015"

# === TAGS ===
tags:
  - "deferred"
  - "quality-review"
  - "en008-followup"
  - "test-enhancement"

# === DELIVERY ITEM PROPERTIES ===
effort: 1
acceptance_criteria: |
  - All F-004, F-005, QA-TD-001, QA-TD-002 findings addressed
  - Test coverage includes plain text format
  - Negative test cases added
  - Agent definition updated with performance targets
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: TESTING
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## Content

### Description

This task tracks minor findings deferred from EN-008 (Entity Extraction Core) quality
reviews. Per DEC-003, these items are non-blocking for GATE-5 but should be addressed
during EN-015 validation framework implementation.

### Deferred Findings

| ID | Source | Description | Category |
|----|--------|-------------|----------|
| F-004 | ps-critic | Plain text format not included in INT-006 cross-format integration test | Testing |
| F-005 | ps-critic | No negative test cases (malformed input, missing timestamps) | Testing |
| QA-TD-001 | nse-qa | Performance target "~500 tokens/batch" not in agent definition | Documentation |
| QA-TD-002 | nse-qa | Token budget "1200 tokens" not in agent definition | Documentation |

### Acceptance Criteria

- [ ] **AC-1:** INT-006 updated to include plain text format test case (F-004)
- [ ] **AC-2:** Negative test cases added for malformed input handling (F-005)
- [ ] **AC-3:** Negative test cases added for missing timestamp scenarios (F-005)
- [ ] **AC-4:** ts-extractor.md updated with performance target (~500 tokens/batch) (QA-TD-001)
- [ ] **AC-5:** ts-extractor.md updated with token budget constraint (1200 tokens) (QA-TD-002)

### Implementation Notes

**Timing:** These items should be addressed AFTER core EN-015 tasks (TASK-131 through TASK-137)
are complete, as they are enhancements to the validation framework.

**Dependencies:**
- TASK-135 (Extractor Tests) should be complete before adding negative test cases
- TASK-137 (Integration Tests) should be complete before updating INT-006

**Reference Documents:**
- [EN-008 ps-critic Review](../EN-008-entity-extraction/critiques/proj008-en008-implementation-critique.md)
- [EN-008 nse-qa Report](../EN-008-entity-extraction/qa/proj008-en008-implementation-qa.md)
- [DEC-003](../FEAT-002--DEC-003-orchestration-execution-order.md) - D-005 decision

### Related Items

- Parent: [EN-015](./EN-015-transcript-validation.md)
- Origin: [EN-008](../EN-008-entity-extraction/EN-008-entity-extraction.md)
- Decision: [DEC-003](../FEAT-002--DEC-003-orchestration-execution-order.md)
- Agent: [ts-extractor.md](../../../../../../skills/transcript/agents/ts-extractor.md)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 2 hours |
| Remaining Work    | 2 hours    |
| Time Spent        | 0 hours        |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated integration tests | Test | skills/transcript/test_data/validation/integration-tests.yaml |
| Updated contract tests | Test | skills/transcript/test_data/validation/contract-tests.yaml |
| Updated agent definition | Documentation | skills/transcript/agents/ts-extractor.md |

### Verification

- [ ] Acceptance criteria verified
- [ ] Plain text format test case added
- [ ] Negative test cases pass
- [ ] Agent definition includes performance targets
- [ ] Reviewed by: {REVIEWER}

---

## History

| Date       | Status      | Notes                          |
|------------|-------------|--------------------------------|
| 2026-01-28 | Created     | Deferred from EN-008 GATE-5 per DEC-003:D-005 |

---

<!--
JERRY ALIGNMENT:
  existing_type: "WorkType.TASK"
  changes_needed: "None - already exists"

DESIGN RATIONALE:
  Consolidates deferred minor findings into single task for tracking.
  Aligns with DEC-003 decision to not block GATE-5 for non-critical items.
  Trace: FEAT-002--DEC-003-orchestration-execution-order.md Section D-005
-->
