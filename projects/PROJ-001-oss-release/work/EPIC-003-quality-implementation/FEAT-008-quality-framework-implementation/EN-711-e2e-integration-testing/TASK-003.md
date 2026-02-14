# TASK-003: Create Rule Compliance Validation Tests

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Summary

```yaml
id: "TASK-003"
work_type: TASK
title: "Create rule compliance validation tests"
description: |
  Write tests that verify all rule files correctly reference the SSOT
  (quality-enforcement.md) and that constant values (thresholds, limits, categories)
  are consistent across all enforcement points. Catches drift between rule files and
  the canonical source of truth.
classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-711"
tags:
  - "e2e-testing"
  - "rule-compliance"
  - "ssot-validation"
activity: TESTING
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Create tests that validate rule compliance across the quality framework:

1. **SSOT reference validation** -- Verify that all rule files in `.context/rules/` and `.claude/rules/` correctly reference quality-enforcement.md as their source of truth
2. **Constant consistency** -- Verify that quality thresholds, coverage minimums, and other constants are consistent across all enforcement points (rules, hooks, CI config)
3. **Rule format validation** -- Verify that rule files follow the required format for Claude Code consumption (navigation tables, section structure)
4. **Cross-reference integrity** -- Verify that references between rules, hooks, and skills resolve correctly

### Acceptance Criteria

- [ ] Rule compliance tests validate SSOT references in all rule files
- [ ] Tests verify constant consistency across all enforcement points
- [ ] Tests verify rule file format compliance (navigation tables, structure)
- [ ] Tests verify cross-reference integrity between rules, hooks, and skills
- [ ] All tests pass via `uv run pytest tests/e2e/`

### Implementation Notes

- Parse rule files to extract referenced constants and compare against SSOT
- Use AST or regex parsing to validate references rather than string matching
- Reference EN-701 (SSOT) and EN-702 (rule optimization) for expected format
- Consider parameterized tests for each rule file

### Related Items

- Parent: [EN-711: E2E Integration Testing](EN-711-e2e-integration-testing.md)
- Blocks: TASK-007 (adversarial review of test completeness)
- Related: EN-701 (SSOT), EN-702 (rule file optimization)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Rule compliance tests | Test suite | `tests/e2e/` |

### Verification

- [ ] Acceptance criteria verified
- [ ] All rule compliance tests pass
- [ ] Tests catch intentional SSOT drift when introduced
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation from EN-711 task decomposition |
