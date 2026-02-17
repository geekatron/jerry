# TASK-002: Add pre-commit hook entry for template format validation

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
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
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Evidence](#evidence) | Deliverables and verification |
| [Related Items](#related-items) | Parent and dependencies |
| [History](#history) | Change log |

---

## Summary

Add a pre-commit hook entry to .pre-commit-config.yaml that runs validate_templates.py when files in .context/templates/adversarial/ are modified. The hook should only trigger on changes to template files, not on unrelated changes.

### Acceptance Criteria
- [ ] Pre-commit hook entry added
- [ ] Triggers only on .context/templates/adversarial/ file changes
- [ ] Runs validate_templates.py via uv run
- [ ] Hook passes on current templates

### Related Items
- Parent: [EN-818: Template Validation CI Gate](EN-818-template-validation-ci-gate.md)
- Depends on: [TASK-001: Create validate_templates.py script](TASK-001.md)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | — |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated .pre-commit-config.yaml | Configuration | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-818 breakdown. |
