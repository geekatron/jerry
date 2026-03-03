# FEAT-016-006: Write /orchestration tutorial

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

Write a Diataxis tutorial for the /orchestration skill — multi-agent workflow coordination with state tracking, sync barriers, and checkpointing. The tutorial teaches a new user to set up and run a multi-phase pipeline, experiencing each orchestration concept hands-on.

**Value Proposition:**
- /orchestration is Jerry's most powerful coordination mechanism
- Users currently have no guided path to learn multi-agent coordination

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `docs/tutorials/orchestration-tutorial.md` created | [ ] |
| AC-2 | Prerequisites section clearly lists what the user needs | [ ] |
| AC-3 | Tutorial walks through a concrete 3-phase pipeline example | [ ] |
| AC-4 | Each step produces a visible result the user can verify | [ ] |
| AC-5 | Covers: orch-planner (planning), orch-tracker (state), sync barriers, quality gates | [ ] |
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
| Source | PROJ-015 P1.6 | Remediation plan item (coverage gap) |
| Reference | skills/orchestration/SKILL.md | Skill definition for accurate content |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | pending | Feature created from PROJ-015 remediation P1.6 |
