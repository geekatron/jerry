# TASK-036: Component A — Add Routing Disambiguation Sections to All 13 Skills

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-02-28
> **Parent:** FEAT-003
> **Owner:** —
> **Activity:** IMPLEMENTATION

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description |
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes |

---

## Summary

Add routing disambiguation sections with consequence documentation to all 13 Jerry skills. Seven skills need new sections; six existing skills need consequence documentation additions. Each section enumerates misrouting conditions, correct alternatives, and failure consequences.

---

## Content

### Description

ADR-003 Component A (unconditional). All 13 skills must include a routing disambiguation section following the ADR-003 template. The section answers: when is this skill the wrong choice, what is the correct alternative, and what fails if misrouted. This is independent of framing vocabulary — it documents factual failure modes for routing auditability.

Group 1 (7 skills needing new sections): bootstrap, architecture, worktracker, ast, saucer-boy, saucer-boy-framework-voice, eng-team.
Group 2 (6 skills needing consequence additions): problem-solving, nasa-se, orchestration, transcript, adversary, red-team.

### Acceptance Criteria

- [ ] 7 new routing disambiguation sections added (Group 1 skills)
- [ ] 6 existing sections updated with consequence documentation (Group 2 skills)
- [ ] Each section includes: conditions, correct alternatives, consequences of misrouting
- [ ] Sections grounded in trigger map collision analysis (mandatory-skill-usage.md)
- [ ] All sections follow the ADR-003 template format

### Related Items

- Parent: [FEAT-003: Implement ADR-003](./FEAT-003-implement-adr-003-routing-disambiguation.md)
- References: ADR-003 Component A template
- References: `mandatory-skill-usage.md` trigger map collision analysis

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated SKILL.md files (13) | Skill modifications | `skills/*/SKILL.md` |

### Verification

- [ ] Acceptance criteria verified

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
