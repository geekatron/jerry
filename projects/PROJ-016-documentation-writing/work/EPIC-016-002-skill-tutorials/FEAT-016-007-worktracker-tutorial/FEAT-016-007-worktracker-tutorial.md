# FEAT-016-007: Write /worktracker tutorial

> **Type:** feature
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-03-02T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** EPIC-016-002
> **Owner:** Claude
> **Target Sprint:**

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and value proposition |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done and criteria |
| [Children Stories/Enablers](#children-storiesenablers) | Story/enabler inventory |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Status changes and key events |

---

## Summary

Write a Diataxis tutorial for the /worktracker skill — persistent work item tracking with entity hierarchy, template enforcement, and worktracker integrity rules. The tutorial teaches a new user to create a project, decompose work into entities, and track progress through completion.

**Value Proposition:**
- /worktracker is used in every Jerry session (H-04 requires active project)
- Users currently learn worktracker by trial and error

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/tutorials/worktracker-tutorial.md` created | [ ] |
| AC-2 | Prerequisites section clearly lists what the user needs | [ ] |
| AC-3 | Tutorial walks through: create project -> create epic -> create feature -> create task -> complete task | [ ] |
| AC-4 | Each step produces a visible result (entity file created, WORKTRACKER.md updated) | [ ] |
| AC-5 | Covers entity hierarchy, template usage, and WTI rules | [ ] |
| AC-6 | No alternatives presented — one clear path | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Passes /diataxis auditor with zero quadrant-mixing findings | [ ] |
| NFC-2 | ps-critic adversarial critique score >= 0.90 | [ ] |
| NFC-3 | Includes Diataxis quadrant metadata (tutorial) in frontmatter | [ ] |

### Diataxis Agent

- `diataxis-tutorial`

---

## Children Stories/Enablers

_To be decomposed when implementation begins._

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Children** | 0 |
| **Completed** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-016-002: Skill Tutorials](../EPIC-016-002-skill-tutorials.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Source | PROJ-015 P2.3 | Remediation plan item (coverage gap) |
| Reference | skills/worktracker/SKILL.md | Skill definition for accurate content |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P2.3 |
