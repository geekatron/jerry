# TASK-001: Create validate_templates.py script

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

Create scripts/validate_templates.py that validates all strategy templates in .context/templates/adversarial/ against the requirements defined in TEMPLATE-FORMAT.md. The script should check: presence of all 8 required sections, navigation table completeness (H-23/H-24), field format compliance, scoring rubric dimension alignment with quality-enforcement.md, and finding ID format compliance.

### Acceptance Criteria
- [ ] Script created at scripts/validate_templates.py
- [ ] Validates all 8 required sections
- [ ] Checks navigation tables
- [ ] Checks field formats
- [ ] Checks scoring dimensions
- [ ] Checks finding ID format
- [ ] Exit code 0 on success, non-zero on failure
- [ ] Type hints (H-11) and docstrings (H-12) present

### Related Items
- Parent: [EN-818: Template Validation CI Gate](EN-818-template-validation-ci-gate.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| validate_templates.py | Script | --- |

### Verification
- [ ] Acceptance criteria verified
- [ ] Quality gate passed (>= 0.92)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-15 | Created | Task created from EN-818 breakdown. |
