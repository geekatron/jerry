# FEAT-036: Templates & Playbook

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

Create templates and playbooks for /red-team engagements. Includes pentest engagement template, vulnerability report template, executive summary template, remediation tracking template, and an end-to-end engagement playbook. All templates use configurable rule sets per R-011.

---

## Acceptance Criteria

- [ ] Pentest engagement template (scope, RoE, methodology, timeline)
- [ ] Vulnerability report template (finding, evidence, CVSS, remediation)
- [ ] Executive summary template
- [ ] Remediation tracking template
- [ ] /red-team engagement playbook (end-to-end workflow)
- [ ] Templates use configurable rule sets (R-011)
- [ ] Passes C4 /adversary review >= 0.95

---

## Children Stories/Enablers

| ID | Title | Status | Priority | Category |
|----|-------|--------|----------|----------|
| EN-327 | Engagement Template | pending | high | infrastructure |
| EN-328 | Vulnerability Report Template | pending | high | infrastructure |
| EN-329 | Executive Summary & Remediation Templates | pending | high | infrastructure |
| EN-330 | Engagement Playbook | pending | high | infrastructure |

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
| Depends On | FEAT-031 | Agent definitions inform template structure |
| Depends On | FEAT-032 | Agent definitions inform template structure |
| Depends On | FEAT-033 | Agent definitions inform template structure |
| Depends On | FEAT-034 | Reporting agent defines finding format |
| Depends On | FEAT-035 | Methodology controls define engagement workflow |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | --- | pending | Feature created during EPIC-004 decomposition |
