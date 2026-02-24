# FEAT-020: SKILL.md & Routing

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

Create the /eng-team SKILL.md file with keyword trigger map, routing table, agent registry, and workflow definitions. Must comply with H-25 and H-26 (skill standards). This is the foundational skill definition that all other EPIC-003 features depend on for agent routing and workflow orchestration.

---

## Acceptance Criteria

- [ ] SKILL.md created per skill-standards (H-25: exactly SKILL.md, case-sensitive)
- [ ] Folder uses kebab-case matching name field (H-26)
- [ ] No README.md inside skill folder (H-25)
- [ ] Description: WHAT + WHEN + triggers, <1024 chars, no XML (H-26)
- [ ] Full repo-relative paths (H-26)
- [ ] Keyword trigger map for /eng-team invocation
- [ ] Agent routing table (8 agents mapped to contexts)
- [ ] Workflow definitions (sequential, parallel, review gates)
- [ ] Passes C4 /adversary review >= 0.95

---

## Children Stories/Enablers

| ID | Title | Status | Priority | Category |
|----|-------|--------|----------|----------|
| EN-200 | SKILL.md Authoring | pending | critical | infrastructure |
| EN-201 | Routing Table & Keyword Map | pending | critical | architecture |
| EN-202 | Workflow Definition | pending | high | architecture |
| EN-203 | Quality Gate: Skill Definition Review | pending | critical | compliance |

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
| Depends On | FEAT-010 | Architecture foundation |
| Depends On | FEAT-011 | Architecture patterns |
| Blocks | FEAT-021 | Architecture agents require skill shell |
| Blocks | FEAT-022 | Implementation agents require skill shell |
| Blocks | FEAT-023 | Quality agents require skill shell |
| Blocks | FEAT-024 | Templates require skill shell |
| Blocks | FEAT-025 | Adversary integration requires skill shell |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | --- | pending | Feature created |
