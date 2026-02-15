# TASK-004: Add E2E test for the validation script

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** pending
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Agents:** ps-architect
> **Created:** 2026-02-15
> **Parent:** EN-818

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Create an E2E test that validates the validate_templates.py script itself by running it against the current templates and asserting it returns success, then running it against a deliberately malformed template and asserting it returns failure.

### Acceptance Criteria
- [ ] E2E test added to tests/e2e/
- [ ] Tests both success and failure cases
- [ ] Test passes with `uv run pytest`

### Related Items
- Parent: [EN-818: Template Validation CI Gate](EN-818-template-validation-ci-gate.md)
- Depends on: [TASK-001: Create validate_templates.py script](TASK-001.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| E2E test file | Test | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-818 breakdown. |
