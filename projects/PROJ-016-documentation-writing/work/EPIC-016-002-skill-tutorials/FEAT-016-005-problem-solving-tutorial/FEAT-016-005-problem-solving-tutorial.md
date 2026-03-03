# FEAT-016-005: Write /problem-solving tutorial

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
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

Write a Diataxis tutorial for the /problem-solving skill — Jerry's most complex and highest-value skill with 9 specialized agents. The tutorial teaches a new user to complete a research-analysis-decision workflow step by step, with visible results at each step. No alternatives presented; one clear path.

**Value Proposition:**
- Addresses the highest-impact coverage gap (0% tutorial coverage)
- /problem-solving is the most-used skill; a tutorial here has maximum reach

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/tutorials/problem-solving-tutorial.md` created | [ ] |
| AC-2 | Prerequisites section clearly lists what the user needs before starting | [ ] |
| AC-3 | Tutorial walks through a concrete end-to-end example (research -> analysis -> decision) | [ ] |
| AC-4 | Each step produces a visible result the user can verify | [ ] |
| AC-5 | No alternatives presented — one clear path through the workflow | [ ] |
| AC-6 | Uses at least 3 different ps-agents (e.g., ps-researcher, ps-analyst, ps-architect) | [ ] |
| AC-7 | Includes ps-critic adversarial critique as a step in the tutorial | [ ] |

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
| Source | PROJ-015 P1.5 | Remediation plan item (coverage gap) |
| Reference | skills/problem-solving/SKILL.md | Skill definition for accurate content |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P1.5 |
