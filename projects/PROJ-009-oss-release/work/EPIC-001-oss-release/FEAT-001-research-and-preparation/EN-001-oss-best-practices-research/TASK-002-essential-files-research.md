# TASK-002: Essential Repository Files Research

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Frontmatter](#frontmatter) | Task metadata |
| [Content](#content) | Description and acceptance criteria |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Change log |

---

## Frontmatter

```yaml
id: "TASK-002"
work_type: TASK
title: "Essential Repository Files Research"
description: |
  Research and document the essential files required for a high-quality OSS repository
  including README, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, etc.
classification: ENABLER
status: DONE
resolution: completed
priority: HIGH
assignee: "ps-researcher"
created_by: "Claude"
created_at: "2026-01-31T16:00:00Z"
updated_at: "2026-01-31T18:00:00Z"
parent_id: "EN-001"
tags:
  - research
  - documentation
  - oss
effort: 1
acceptance_criteria: |
  - Essential files checklist created
  - .github/ directory structure documented
  - Issue/PR templates researched
  - GitHub repository settings documented
activity: RESEARCH
original_estimate: 1
remaining_work: 0
time_spent: 1
```

---

## Content

### Description

Research the essential files and directory structure required for a professional OSS repository. Sources include GitHub Open Source Guides, 10up Best Practices, and Creative Commons guidelines.

### Acceptance Criteria

- [x] README.md structure and badges documented
- [x] CONTRIBUTING.md patterns researched
- [x] CODE_OF_CONDUCT.md (Contributor Covenant) documented
- [x] SECURITY.md vulnerability disclosure policy documented
- [x] .github/ directory structure (templates, workflows) documented

### Implementation Notes

Research identified two categories:
1. **Required Files**: LICENSE, README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, SECURITY.md
2. **Recommended Files**: GOVERNANCE.md, SUPPORT.md, CHANGELOG.md, AUTHORS

**Key Sources:**
- GitHub Open Source Guides
- 10up Best Practices
- libresource/open-source-checklist
- Creative Commons GitHub Guidelines

### Related Items

- Parent: [EN-001: OSS Best Practices Research](./EN-001-oss-best-practices-research.md)
- Output: [best-practices-research.md](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher/best-practices-research.md) (Section 1.1, 1.2)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Essential Files Checklist | Research | [best-practices-research.md#essential-files](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher/best-practices-research.md) |
| .github Directory Structure | Research | [best-practices-research.md#github-config](../orchestration/oss-release-20260131-001/ps/phase-0/ps-researcher/best-practices-research.md) |

### Verification

- [x] Acceptance criteria verified
- [x] Reviewed by: ps-critic (QG-0)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-31T16:00:00Z | Created | Initial creation |
| 2026-01-31T16:30:00Z | IN_PROGRESS | Research started |
| 2026-01-31T18:00:00Z | DONE | Research complete |
