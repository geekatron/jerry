# EN-946: Feature Request Issue Template (Worktracker-Aligned)

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-18
> **Due:** ---
> **Completed:** 2026-02-18
> **Parent:** FEAT-016
> **Owner:** ---
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How enabler supports feature delivery |
| [Technical Approach](#technical-approach) | High-level technical approach |
| [Children (Tasks)](#children-tasks) | Task inventory and tracking |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Dependencies](#dependencies) | Dependencies and items enabled |
| [History](#history) | Status changes and key events |

---

## Summary

Create a GitHub issue template for feature requests that aligns with the Jerry /worktracker Feature entity template. Form fields map directly to worktracker fields so that feature requests arrive pre-structured for intake into the project backlog.

**Technical Scope:**
- Create `.github/ISSUE_TEMPLATE/feature-request.yml` with fields aligned to the worktracker FEATURE.md template
- Update `config.yml` to position feature request prominently in the template chooser
- Include mapping guidance in the template so contributors understand how their request translates to a tracked work item

---

## Problem Statement

Contributors who want to suggest features have no structured way to submit requests. Without a template that aligns with the worktracker, feature requests arrive in varying formats requiring significant manual translation before they can be tracked as Feature entities in the project.

---

## Business Value

A worktracker-aligned feature request template provides:
- Lower barrier to structured contributions
- Feature requests arrive pre-formatted for backlog intake
- Reduced manual translation effort for maintainers
- Consistent quality of incoming feature requests

### Features Unlocked

- Structured contributor feature request pipeline
- Direct mapping from GitHub issues to worktracker Feature entities

---

## Technical Approach

1. Create `.github/ISSUE_TEMPLATE/feature-request.yml` with form fields mapped to worktracker FEATURE.md template:
   - Title → Feature title
   - Summary → Feature summary/value proposition
   - Use case/problem → Problem being solved
   - Acceptance criteria suggestions → Feature AC seeds
   - Priority suggestion → Feature priority input
   - Related features → Feature dependencies
2. Update `.github/ISSUE_TEMPLATE/config.yml` to include feature request in the chooser
3. Add form field descriptions that explain how each maps to the project's tracking structure

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| TASK-001 | Create feature-request.yml issue template | done | 1 | --- |
| TASK-002 | Update config.yml with feature request link | done | 0.5 | --- |
| TASK-003 | Add contributor guidance to CONTRIBUTING.md | done | 0.5 | --- |

---

## Acceptance Criteria

### Definition of Done

- [x] `.github/ISSUE_TEMPLATE/feature-request.yml` exists with worktracker-aligned fields
- [x] Form fields map to Feature entity template (title, summary, value proposition, AC, priority)
- [x] `config.yml` updated with feature request in template chooser
- [x] CONTRIBUTING.md updated with guidance on submitting feature requests
- [x] Template uses GitHub issue form YAML schema correctly

---

## Dependencies

### Depends On

- [EN-945](../EN-945-cross-platform-issue-templates/EN-945-cross-platform-issue-templates.md) - Establishes issue template infrastructure and config.yml

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-18 | Claude | pending | Created to provide worktracker-aligned feature request intake from GitHub Issues |
| 2026-02-18 | Claude | done | All 3 tasks complete. feature-request.yml created with 10 worktracker-aligned fields. config.yml updated with Discussions link. CONTRIBUTING.md updated with "Submitting Feature Requests" section. |
