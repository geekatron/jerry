# FEAT-011: Skill Routing & Invocation Architecture

> **Type:** feature
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-22
> **Due:** —
> **Completed:** —
> **Parent:** EPIC-002
> **Owner:** —
> **Target Sprint:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature scope and value proposition |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done checklist |
| [Children Stories/Enablers](#children-storiesenablers) | Enabler inventory and tracking |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Dependencies](#dependencies) | Upstream and downstream dependencies |
| [History](#history) | Status changes and key events |

---

## Summary

Design the skill routing and invocation architecture for /eng-team and /red-team. Define keyword trigger maps, agent selection logic, workflow orchestration patterns, and integration with existing Jerry skill routing. Produce ADR.

---

## Acceptance Criteria

- [ ] Keyword trigger map for /eng-team and /red-team
- [ ] Agent selection logic (context-aware routing)
- [ ] Workflow orchestration patterns within each skill
- [ ] Integration design with Jerry routing-standards
- [ ] ADR: Skill Routing Architecture with evidence
- [ ] Passes C4 /adversary review >= 0.95

---

## Children Stories/Enablers

| ID | Title | Status | Priority | Category |
|----|-------|--------|----------|----------|
| EN-105 | Keyword Trigger Map Design | pending | critical | architecture |
| EN-106 | Agent Selection Logic Specification | pending | high | architecture |
| EN-107 | Skill Workflow Orchestration Patterns | pending | high | architecture |
| EN-108 | ADR: Skill Routing Architecture | pending | critical | architecture |

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Enablers** | 4 |
| **Completed Enablers** | 0 |
| **Completion %** | 0% |

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | FEAT-010 | Agent Team Architecture (agent definitions required) |
| Blocks | FEAT-020 | /eng-team skill implementation |
| Blocks | FEAT-030 | /red-team skill implementation |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | — | pending | Feature created |
