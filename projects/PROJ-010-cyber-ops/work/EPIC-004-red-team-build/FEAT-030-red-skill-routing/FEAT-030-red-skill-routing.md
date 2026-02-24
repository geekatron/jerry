# FEAT-030: SKILL.md & Routing

> **Type:** feature
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-22
> **Due:** ---
> **Completed:** ---
> **Parent:** EPIC-004
> **Owner:** ---
> **Target Sprint:** ---

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature description and scope |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children Stories/Enablers](#children-storiesenablers) | Enabler inventory |
| [Progress Summary](#progress-summary) | Completion tracking |
| [Dependencies](#dependencies) | Upstream and downstream links |
| [History](#history) | Status changes and key events |

---

## Summary

Create the /red-team SKILL.md with keyword trigger map, routing table, agent registry, authorization controls, and methodology workflow. Must comply with skill-standards H-25 through H-30. This is the foundational skill definition that all other EPIC-004 features depend on for agent routing and invocation.

---

## Acceptance Criteria

- [ ] SKILL.md per skill-standards (H-25 through H-30)
- [ ] Keyword trigger map for /red-team invocation
- [ ] Agent routing table (9 agents mapped to engagement phases)
- [ ] Authorization control integration in routing
- [ ] Methodology workflow definition (PTES/OSSTMM/ATT&CK)
- [ ] Passes C4 /adversary review >= 0.95

---

## Children Stories/Enablers

| ID | Title | Status | Priority | Category |
|----|-------|--------|----------|----------|
| EN-300 | SKILL.md Authoring | pending | critical | infrastructure |
| EN-301 | Routing Table & Keyword Map | pending | critical | architecture |
| EN-302 | Authorization Control Integration | pending | critical | compliance |
| EN-303 | Quality Gate: Skill Definition Review | pending | critical | compliance |

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
| Depends On | FEAT-010 | Threat modeling taxonomy |
| Depends On | FEAT-011 | Security knowledge base |
| Blocks | FEAT-031 | Recon & vulnerability agents require routing |
| Blocks | FEAT-032 | Exploitation agents require routing |
| Blocks | FEAT-033 | Post-exploitation agents require routing |
| Blocks | FEAT-034 | Reporting agent requires routing |
| Blocks | FEAT-035 | Methodology controls require routing |
| Blocks | FEAT-036 | Templates require routing context |
| Blocks | FEAT-037 | Adversary integration requires routing |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | --- | pending | Feature created during EPIC-004 decomposition |
