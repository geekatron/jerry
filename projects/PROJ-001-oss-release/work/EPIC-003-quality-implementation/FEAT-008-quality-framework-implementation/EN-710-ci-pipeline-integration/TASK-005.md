# TASK-005: Configure Branch Protection and Merge Requirements

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 0.1.0
-->

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this task delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Implementation Notes](#implementation-notes) | Technical guidance |
| [Time Tracking](#time-tracking) | Effort estimates and actuals |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [Evidence](#evidence) | Deliverables and verification |
| [History](#history) | Status changes and key events |

---

## Summary

```yaml
id: "TASK-005"
work_type: TASK
title: "Configure branch protection and merge requirements"
description: |
  Configure GitHub branch protection rules to require all CI quality checks to pass
  before a pull request can be merged. This is the enforcement mechanism that makes
  CI quality gates mandatory rather than advisory, completing the L5 enforcement loop.
classification: ENABLER
status: DONE
resolution: null
priority: HIGH
assignee: ""
created_by: "Claude"
created_at: "2026-02-14"
updated_at: "2026-02-14"
parent_id: "EN-710"
tags:
  - "ci-pipeline"
  - "branch-protection"
  - "merge-requirements"
activity: DEVELOPMENT
original_estimate: null
remaining_work: null
time_spent: null
```

---

## Content

### Description

Configure GitHub branch protection rules on the main branch to enforce:

- All CI quality workflow checks must pass before merge
- No direct pushes to main (all changes via pull request)
- Required status checks: architecture tests, mypy, ruff

Without branch protection, CI results are advisory only -- developers can merge despite failures. Branch protection makes quality enforcement mandatory.

### Acceptance Criteria

- [ ] Branch protection rules configured for the main branch
- [ ] CI quality workflow status checks are required for merge
- [ ] Direct pushes to main are blocked (pull request required)
- [ ] Protection rules are documented for team reference

### Implementation Notes

- Configure via GitHub repository settings or `gh api` commands
- Required status checks should match the job/step names in quality.yml
- Consider whether to require up-to-date branches before merge
- Document the configuration in the pipeline documentation (TASK-007)

### Related Items

- Parent: [EN-710: CI Pipeline Quality Integration](EN-710-ci-pipeline-integration.md)
- Depends on: TASK-001 (workflow must exist to reference status checks)
- Blocks: TASK-006 (verification requires branch protection)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | — |
| Remaining Work | 0 hours |
| Time Spent | — |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Branch protection configuration | GitHub settings | Repository settings > Branches |

### Verification

- [ ] Acceptance criteria verified
- [ ] Attempting to merge a failing PR is correctly blocked
- [ ] Direct push to main is correctly rejected
- [ ] Reviewed by: —

---

## History

| Date | Status | Notes |
|------------|-------------|--------------------------------|
| 2026-02-14 | Created | Initial creation from EN-710 task decomposition |
