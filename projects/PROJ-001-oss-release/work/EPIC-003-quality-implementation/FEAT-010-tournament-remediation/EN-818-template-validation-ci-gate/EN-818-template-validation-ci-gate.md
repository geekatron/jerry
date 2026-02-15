# EN-818: Template Validation CI Gate

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-15 (Claude)
PURPOSE: Create automated template validation tooling with CI integration
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-15
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-010
> **Owner:** —
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Create automated template validation tooling with CI integration to enforce TEMPLATE-FORMAT.md conformance on every PR, preventing template format drift.

---

## Problem Statement

Template format compliance is currently only verified during adversarial review cycles (human/LLM review). There is no automated validation to catch format drift, missing required sections, or structural inconsistencies. This creates a risk of template degradation over time.

---

## Technical Approach

1. Create validate_templates.py script that checks all templates against TEMPLATE-FORMAT.md requirements
2. Add pre-commit hook entry for template format validation
3. Add GitHub Actions CI job for template validation on PR
4. Add E2E test to validate the validation script itself

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Create validate_templates.py script | pending | DEVELOPMENT | ps-architect |
| TASK-002 | Add pre-commit hook entry for template format validation | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Add GitHub Actions CI job for template validation | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Add E2E test for the validation script | pending | DEVELOPMENT | ps-architect |

---

## Acceptance Criteria

### Definition of Done
- [ ] validate_templates.py script created and working
- [ ] Pre-commit hook configured and tested
- [ ] GitHub Actions CI job added and passing
- [ ] E2E test for validation script passes
- [ ] All current templates pass validation
- [ ] Quality gate passed (>= 0.92)

### Technical Criteria
| # | Criterion | Verified |
|---|-----------|----------|
| 1 | Script validates all 8 required sections | — |
| 2 | Script checks navigation tables (H-23/H-24) | — |
| 3 | Script checks field format compliance | — |
| 4 | Script checks scoring rubric dimension alignment | — |
| 5 | Script checks finding ID format compliance | — |
| 6 | Pre-commit hook triggers on template file changes only | — |
| 7 | CI job runs on PR events and fails build on validation failure | — |
| 8 | E2E test covers both success and failure cases | — |

---

## Related Items

### Hierarchy
- **Parent Feature:** [FEAT-010: Tournament Remediation](../FEAT-010-tournament-remediation.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-15 | Claude | pending | Enabler created from FEAT-009 C4 Tournament findings. |
