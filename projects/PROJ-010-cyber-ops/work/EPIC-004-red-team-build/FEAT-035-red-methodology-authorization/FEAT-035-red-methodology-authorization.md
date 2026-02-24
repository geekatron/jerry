# FEAT-035: Methodology & Authorization Controls

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

Implement methodology enforcement and authorization controls for /red-team engagements. Integrates PTES, OSSTMM, and MITRE ATT&CK methodologies into agent workflows. Enforces scope verification, rules of engagement, and out-of-scope refusal. Built on the FEAT-015 authorization architecture.

---

## Acceptance Criteria

- [ ] PTES methodology integration (all phases mapped to agents)
- [ ] OSSTMM methodology integration (relevant sections)
- [ ] MITRE ATT&CK technique mapping per agent
- [ ] Scope verification enforcement (R-020)
- [ ] Rules of engagement template and confirmation flow
- [ ] Out-of-scope refusal mechanism
- [ ] Evidence preservation (all actions logged with timestamps)
- [ ] Passes C4 /adversary review >= 0.95

---

## Children Stories/Enablers

| ID | Title | Status | Priority | Category |
|----|-------|--------|----------|----------|
| EN-322 | Methodology Integration (PTES/OSSTMM/ATT&CK) | pending | critical | compliance |
| EN-323 | Scope Verification Implementation | pending | critical | compliance |
| EN-324 | Rules of Engagement Template | pending | high | infrastructure |
| EN-325 | Evidence Preservation & Audit Trail | pending | high | compliance |
| EN-326 | Quality Gate: Methodology & Auth Review | pending | critical | compliance |

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Enablers** | 5 |
| **Completed Enablers** | 0 |
| **Completion %** | 0% |

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | FEAT-015 | Authorization architecture provides scope verification foundation |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | --- | pending | Feature created during EPIC-004 decomposition |
