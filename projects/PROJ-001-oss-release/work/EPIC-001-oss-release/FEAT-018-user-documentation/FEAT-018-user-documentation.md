# FEAT-018: User Documentation — Runbooks & Playbooks

> **Type:** feature
> **Status:** pending
> **Priority:** medium
> **Impact:** high
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** ---
> **Parent:** EPIC-001
> **Owner:** Adam Nowak
> **Target Sprint:** ---

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits from this feature |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done and criteria |
| [Children (Stories/Enablers)](#children-storiesenablers) | Enabler inventory and tracking |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Status changes and key events |

---

## Summary

Create a series of user-facing runbooks and playbooks that guide users on how to use Jerry. This feature addresses the documentation gap identified during the post-release planning session, where the project lead identified the need for structured user guides beyond the existing technical documentation.

**Value Proposition:**
- Step-by-step runbooks for common Jerry workflows
- Playbooks for advanced use cases (orchestration, adversarial review, transcript processing)
- Reduced onboarding time for new users

**Source:** Transcript packet `transcript-oss-post-release-20260217-001` (ACT-005)

---

## Benefit Hypothesis

**We believe that** creating user-facing runbooks and playbooks

**Will result in** faster user onboarding, reduced support requests, and higher adoption of Jerry's advanced features

**We will know we have succeeded when** users have a complete set of runbooks covering core workflows and playbooks for each major skill

---

## Acceptance Criteria

### Definition of Done

- [x] All enablers completed
- [ ] Runbook/playbook scope defined and approved
- [ ] Getting-started runbook created
- [ ] Skill usage playbooks created for major skills
- [ ] All acceptance criteria verified

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Scope document defines runbook vs playbook distinction and coverage plan | [ ] |
| AC-2 | Getting-started runbook covers initial setup through first skill invocation | [ ] |
| AC-3 | At least 3 skill playbooks created (problem-solving, orchestration, transcript) | [ ] |
| AC-4 | All documentation follows Jerry markdown navigation standards (H-23, H-24) | [ ] |

---

## Children (Stories/Enablers)

### Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| EN-942 | Enabler | Define runbook/playbook scope and structure | pending | high | 2 |
| EN-943 | Enabler | Create getting-started runbook | pending | high | 3 |
| EN-944 | Enabler | Create skill usage playbooks | pending | medium | 5 |

### Work Item Links

- [EN-942: Define runbook/playbook scope and structure](./EN-942-runbook-playbook-scope/EN-942-runbook-playbook-scope.md)
- [EN-943: Create getting-started runbook](./EN-943-getting-started-runbook/EN-943-getting-started-runbook.md)
- [EN-944: Create skill usage playbooks](./EN-944-skill-usage-playbooks/EN-944-skill-usage-playbooks.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [....................] 0% (0/3 completed)              |
| Effort:    [....................] 0% (0/10 points completed)      |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 3 |
| **Completed Enablers** | 0 |
| **Total Effort (points)** | 10 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release.md)

### Related Features

- [FEAT-016: Post-Release README & Documentation Updates](../FEAT-016-post-release-documentation/FEAT-016-post-release-documentation.md) - Complements with project-level docs
- [FEAT-017: Installation Instructions Modernization](../FEAT-017-installation-instructions/FEAT-017-installation-instructions.md) - Installation docs precede usage docs

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | FEAT-017 | Installation instructions should be updated before creating getting-started runbook |

### Transcript Source

- **Packet:** `transcript-oss-post-release-20260217-001`
- **Action Items:** ACT-005 (create epic/feature for runbooks and playbooks)
- **Topics:** TOP-004 (User Documentation: Runbooks and Playbooks)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Feature created from transcript packet analysis (ACT-005, TOP-004) |
