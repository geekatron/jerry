# TASK-004: Unit Tests for Generator and Hook Regression

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Related Items](#related-items) | Cross-references and dependencies |
| [Evidence](#evidence) | Proof of completion |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-004"
work_type: TASK
title: "Unit Tests for Generator and Hook Regression"
description: |
  Write unit tests for SessionQualityContextGenerator (content generation,
  token budget, XML structure). Verify integration with existing session
  start hook does not regress. Verify uv run pytest passes.
classification: ENABLER
status: DONE
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-706"
tags:
  - "testing"
  - "unit-tests"
  - "session-start"
  - "regression"
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Summary

Write unit tests for the `SessionQualityContextGenerator` covering content generation (all 4 sections present), token budget enforcement (under 700 tokens), and XML structure validity. Write regression tests to verify that the session start hook's existing project context resolution functionality is not broken by the quality context integration. All tests must pass via `uv run pytest`.

## Acceptance Criteria

- [ ] Unit tests for generator content (quality gate, constitutional, strategies, criticality sections present)
- [ ] Unit tests for XML structure validity (`<quality-context>` block well-formed)
- [ ] Unit tests for 700-token budget constraint
- [ ] Unit tests for token budget trimming behavior
- [ ] Regression tests for session start hook (project-context still emitted correctly)
- [ ] Regression tests for session start hook (project-required still emitted correctly)
- [ ] Test naming follows `test_{scenario}_when_{condition}_then_{expected}` convention
- [ ] `uv run pytest` passes with all new tests

## Implementation Notes

- Unit test location: `tests/unit/infrastructure/enforcement/test_session_quality_context_generator.py`
- Regression test location: `tests/integration/test_session_start_hook.py` (or add to existing)
- Use AAA (Arrange-Act-Assert) pattern
- For XML validation, use `xml.etree.ElementTree` to parse the output
- Test edge cases: generator with empty content, generator with oversized content
- Regression tests should run the actual session start hook and verify both project context and quality context appear in output

**Design Source:** testing-standards.md (BDD cycle, AAA pattern, test naming convention)

## Related Items

- Parent: [EN-706: SessionStart Quality Context Enhancement](EN-706-sessionstart-quality-context.md)
- Depends on: TASK-001 (generator), TASK-002 (budget), TASK-003 (integration)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | 0 hours |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| _None yet_ | — | — |

### Verification

- [ ] Acceptance criteria verified
- [ ] Code review passed
- [ ] Reviewed by: _pending_

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation |
