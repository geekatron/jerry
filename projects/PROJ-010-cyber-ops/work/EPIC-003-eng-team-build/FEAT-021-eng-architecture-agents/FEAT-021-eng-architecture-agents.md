# FEAT-021: Architecture Agents (eng-architect, eng-lead)

> **Type:** feature
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-22
> **Due:** ---
> **Completed:** ---
> **Parent:** EPIC-003
> **Owner:** ---
> **Target Sprint:** ---

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature scope and value proposition |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done checklist |
| [Children Stories/Enablers](#children-storiesenablers) | Enabler inventory |
| [Progress Summary](#progress-summary) | Completion tracking |
| [Dependencies](#dependencies) | Upstream and downstream links |
| [History](#history) | Status changes and key events |

---

## Summary

Build eng-architect and eng-lead agent definitions. eng-architect handles system design, ADRs, threat modeling (STRIDE/DREAD/PASTA), and architecture review. eng-lead handles implementation planning, code standards enforcement, PR review criteria, and dependency decisions. These two agents establish the architectural patterns that all downstream implementation agents follow.

---

## Acceptance Criteria

- [ ] eng-architect agent definition with identity, capabilities, guardrails, constitution
- [ ] eng-architect produces STRIDE/DREAD threat models as first deliverable (R-001)
- [ ] eng-lead agent definition with identity, capabilities, guardrails, constitution
- [ ] Both agents follow agent-development-standards (R-022)
- [ ] Both agents portable across LLMs (R-010)
- [ ] YAML frontmatter schema compliance
- [ ] Passes C4 /adversary review >= 0.95

---

## Children Stories/Enablers

| ID | Title | Status | Priority | Category |
|----|-------|--------|----------|----------|
| EN-204 | eng-architect Agent Definition | pending | critical | architecture |
| EN-205 | eng-lead Agent Definition | pending | critical | architecture |
| EN-206 | Threat Modeling Integration | pending | critical | architecture |
| EN-207 | Quality Gate: Architecture Agents Review | pending | critical | compliance |

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
| Depends On | FEAT-020 | Skill shell and routing definitions |
| Blocks | FEAT-022 | Implementation agents depend on architecture patterns |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | --- | pending | Feature created |
