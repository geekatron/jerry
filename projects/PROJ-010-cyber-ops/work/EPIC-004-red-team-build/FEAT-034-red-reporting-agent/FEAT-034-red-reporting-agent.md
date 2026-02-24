# FEAT-034: Reporting Agent (red-reporter)

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
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

Build the red-reporter agent definition. Covers finding documentation, risk scoring, remediation recommendations, executive summaries, and technical write-ups. Every finding includes actionable remediation per R-021. This agent synthesizes outputs from recon, exploitation, and post-exploitation phases into structured deliverables.

---

## Acceptance Criteria

- [ ] red-reporter agent definition with reporting capabilities
- [ ] Finding documentation format (vulnerability, evidence, impact, remediation)
- [ ] Risk scoring integration (CVSS, custom risk matrices)
- [ ] Executive summary generation capability
- [ ] Technical write-up generation capability
- [ ] Remediation guidance in every finding (R-021)
- [ ] Agent portable across LLMs (R-010)
- [ ] Passes C4 /adversary review >= 0.95

---

## Children Stories/Enablers

| ID | Title | Status | Priority | Category |
|----|-------|--------|----------|----------|
| EN-318 | red-reporter Agent Definition | pending | high | architecture |
| EN-319 | Finding Documentation Format | pending | high | architecture |
| EN-320 | Risk Scoring Integration | pending | high | architecture |
| EN-321 | Quality Gate: Reporting Agent Review | pending | high | compliance |

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
| Depends On | FEAT-031 | Recon findings provide reporting input |
| Depends On | FEAT-032 | Exploitation findings provide reporting input |
| Depends On | FEAT-033 | Post-exploitation findings provide reporting input |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | --- | pending | Feature created during EPIC-004 decomposition |
