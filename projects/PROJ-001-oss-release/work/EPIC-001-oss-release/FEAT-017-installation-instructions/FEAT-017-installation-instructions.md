# FEAT-017: Installation Instructions Modernization

> **Type:** feature
> **Status:** pending
> **Priority:** high
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

Rewrite the installation instructions to move away from the legacy private archive-based distribution model. The new instructions cover two installation paths: (1) collaborator-based access via SSH key + Claude Code marketplace, and (2) future public repository access where users directly add the marketplace entry.

**Value Proposition:**
- Accurate installation instructions reflecting current distribution model
- Clear guidance for collaborators with SSH key setup
- Forward-looking documentation for public repository access

**Source:** Transcript packet `transcript-oss-post-release-20260217-001` (ACT-004)

---

## Benefit Hypothesis

**We believe that** modernizing the installation instructions to reflect collaborator-based and public repository access models

**Will result in** reduced onboarding friction for new users and collaborators, fewer support requests about installation

**We will know we have succeeded when** installation instructions cover both current (collaborator + SSH) and future (public repo) scenarios with no references to the private archive model

---

## Acceptance Criteria

### Definition of Done

- [x] All enablers completed
- [ ] Legacy archive-based instructions removed or deprecated
- [ ] Collaborator-based installation documented (SSH key + marketplace)
- [ ] Public repository installation path documented (future state)
- [ ] All acceptance criteria verified

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | No references to private archive distribution model remain in active instructions | [ ] |
| AC-2 | Step-by-step guide for collaborator installation (SSH key + GitHub + marketplace) | [ ] |
| AC-3 | Documentation for future public repo installation scenario | [ ] |
| AC-4 | Claude Code marketplace integration instructions included | [ ] |

---

## Children (Stories/Enablers)

### Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| EN-939 | Enabler | Remove/deprecate archive-based installation instructions | pending | high | 2 |
| EN-940 | Enabler | Document collaborator-based installation (SSH + marketplace) | pending | high | 3 |
| EN-941 | Enabler | Document public repository installation path | pending | medium | 2 |

### Work Item Links

- [EN-939: Remove/deprecate archive-based installation instructions](./EN-939-remove-archive-instructions/EN-939-remove-archive-instructions.md)
- [EN-940: Document collaborator-based installation](./EN-940-collaborator-installation/EN-940-collaborator-installation.md)
- [EN-941: Document public repository installation path](./EN-941-public-repo-installation/EN-941-public-repo-installation.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [....................] 0% (0/3 completed)              |
| Effort:    [....................] 0% (0/7 points completed)       |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 3 |
| **Completed Enablers** | 0 |
| **Total Effort (points)** | 7 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release.md)

### Related Features

- [FEAT-016: Post-Release README & Documentation Updates](../FEAT-016-post-release-documentation/FEAT-016-post-release-documentation.md) - Co-identified in post-release planning session

### Transcript Source

- **Packet:** `transcript-oss-post-release-20260217-001`
- **Action Items:** ACT-004 (installation instructions overhaul)
- **Decisions:** DEC-003 (installation model shifting from archive to repo)
- **Topics:** TOP-003 (Installation Instructions Overhaul)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Feature created from transcript packet analysis (ACT-004, DEC-003, TOP-003) |
