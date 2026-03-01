# TASK-022: Phase 2: Rule files — upgrade NPT-014 to NPT-009/NPT-013 in .context/rules/

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-02-28
> **Completed:** 2026-02-28
> **Parent:** FEAT-001
> **Owner:** Claude
> **Activity:** DEVELOPMENT

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

Upgrade 8 NPT-014 instances across 7 rule files in `.context/rules/` to NPT-009 structured negation with consequence and alternative text.

---

## Content

### Description

Upgrade 8 NPT-014 instances across 7 rule files in `.context/rules/` to NPT-009 structured negation format. Each upgrade adds consequence text explaining why the prohibition exists and alternative/instead guidance.

### Acceptance Criteria

- [x] P2-01: python-environment.md header upgraded with consequence
- [x] P2-02: coding-standards.md Exception handling upgraded with consequence + alternative
- [x] P2-03: quality-enforcement.md retired rule IDs upgraded with consequence + alternative
- [x] P2-04: mandatory-skill-usage.md proactive invocation upgraded with consequence + alternative
- [x] P2-05: agent-development-standards.md worker spawn prohibition upgraded with consequence
- [x] P2-06: agent-development-standards.md Task tool prohibition upgraded with consequence
- [x] P2-07: project-workflow.md active project requirement upgraded with consequence
- [x] P2-08: agent-routing-standards.md silent drop prohibition upgraded (Option A: positive rephrasing)

### Implementation Notes

P2-08 used Option A (positive rephrasing) per the implementation plan's recommendation since the original statement was a system invariant rather than a prohibition directed at an agent.

### Related Items

- Parent: [FEAT-001: Implement ADR-001](./FEAT-001-implement-adr-001-npt-014-elimination.md)
- Depends On: [TASK-021: Baseline capture](./TASK-021-baseline-capture.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| python-environment.md | Rule file edit | `.context/rules/python-environment.md` |
| coding-standards.md | Rule file edit | `.context/rules/coding-standards.md` |
| quality-enforcement.md | Rule file edit | `.context/rules/quality-enforcement.md` |
| mandatory-skill-usage.md | Rule file edit | `.context/rules/mandatory-skill-usage.md` |
| agent-development-standards.md | Rule file edit | `.context/rules/agent-development-standards.md` |
| project-workflow.md | Rule file edit | `.context/rules/project-workflow.md` |
| agent-routing-standards.md | Rule file edit | `.context/rules/agent-routing-standards.md` |

### Verification

- [x] Acceptance criteria verified
- [x] 8 instances across 7 files upgraded
- [x] Committed in 47451ef6

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-28 | Created | Initial creation |
| 2026-02-28 | completed | 8 instances across 7 files upgraded |
