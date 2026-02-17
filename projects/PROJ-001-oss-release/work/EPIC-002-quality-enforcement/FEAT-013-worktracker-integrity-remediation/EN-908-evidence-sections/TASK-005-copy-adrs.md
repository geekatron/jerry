# TASK-005: Copy ADRs to canonical decisions/ directory

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

> **Type:** task
> **Status:** BACKLOG
> **Priority:** HIGH
> **Activity:** DEVELOPMENT
> **Created:** 2026-02-16
> **Parent:** EN-908

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Description, acceptance criteria, implementation notes |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Content

### Description

Copy ADR-EPIC002-001 and ADR-EPIC002-002 to projects/PROJ-001-oss-release/decisions/ directory. These ADRs currently exist only within their respective enabler work directories and need to be copied to the canonical decisions/ directory for discoverability.

Specific files to copy:
- ADR-EPIC002-001 (Strategy Selection) -> projects/PROJ-001-oss-release/decisions/
- ADR-EPIC002-002 (Enforcement Architecture) -> projects/PROJ-001-oss-release/decisions/

### Acceptance Criteria

- [ ] ADR-EPIC002-001 exists in projects/PROJ-001-oss-release/decisions/
- [ ] ADR-EPIC002-002 exists in projects/PROJ-001-oss-release/decisions/
- [ ] Copied ADRs are identical to source versions
- [ ] decisions/ directory created if it does not exist

### Implementation Notes

Locate the source ADR files within the EN-302 and EN-402 work directories. Copy (not move) to preserve the originals in their work context. Add a note to the copied ADRs indicating the canonical source location.

### Related Items

- Parent: [EN-908: Evidence Section Remediation](EN-908-evidence-sections.md)
- Related: TASK-002 (EN-302 evidence references ADR-EPIC002-001), TASK-004 (EN-402 evidence references ADR-EPIC002-002)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ADR-EPIC002-001 in decisions/ | Code change | pending |
| ADR-EPIC002-002 in decisions/ | Code change | pending |

### Verification

- [ ] Acceptance criteria verified
- [ ] ADR files exist in decisions/ directory
- [ ] Reviewed by: --

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-16 | Created | Initial creation. Part of EN-908 evidence section remediation. |
