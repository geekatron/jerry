# TASK-003: Add GitHub Actions CI job for template validation

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

Add a template validation step to the existing GitHub Actions CI workflow that runs validate_templates.py on every PR. The job should run after dependency installation and before the main test suite.

### Acceptance Criteria
- [ ] CI job added to GitHub Actions workflow
- [ ] Runs validate_templates.py
- [ ] Fails the build if validation fails
- [ ] Runs on PR events

### Related Items
- Parent: [EN-818: Template Validation CI Gate](EN-818-template-validation-ci-gate.md)
- Depends on: [TASK-001: Create validate_templates.py script](TASK-001.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated GitHub Actions workflow | Configuration | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-818 breakdown. |
