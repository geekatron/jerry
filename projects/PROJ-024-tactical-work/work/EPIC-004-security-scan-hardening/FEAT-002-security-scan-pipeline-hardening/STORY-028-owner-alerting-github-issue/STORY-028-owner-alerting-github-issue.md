# STORY-028: Add Owner Alerting via an Auto-Managed Rolling GitHub Issue

> **Type:** story
> **Status:** in_progress
> **Priority:** medium
> **Impact:** high
> **Created:** 2026-06-22
> **Parent:** FEAT-002
> **GitHub Issue:** [#301](https://github.com/geekatron/jerry/issues/301)

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | Role / goal / benefit |
| [Summary](#summary) | Scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |
| [Children (Tasks)](#children-tasks) | Task inventory |
| [Progress Summary](#progress-summary) | Status tracking |
| [Related Items](#related-items) | Hierarchy |
| [Delivery Evidence](#delivery-evidence) | PR and commit evidence |
| [History](#history) | Status changes |

---

## User Story

As a repository maintainer, I want the scheduled security scan to automatically create or update a GitHub issue when new CVEs are found, so that I am alerted without needing to check workflow run logs manually.

---

## Summary

Currently, the scheduled scan exits with a non-zero code when CVEs are found, but there is no human-visible alert outside of the Actions UI. A rolling GitHub issue ("Security Scan: Open CVEs") is created by the scan when CVEs are detected and updated (or closed) as CVE status changes. "Rolling" means the same issue is reused across runs (identified by label or title), not a new issue per run. The issue body lists the current open CVEs with package, version, CVE ID, and fix version.

---

## Acceptance Criteria

- [ ] When the scheduled scan detects CVEs not on the accept-list, it creates or updates a GitHub issue with title `Security Scan: Open CVEs` (or equivalent canonical title) listing the CVE details
- [ ] When a subsequent scan run finds no unaccepted CVEs, it closes the rolling issue automatically
- [ ] The rolling issue is reused across multiple runs (not duplicated per run) — identified by a stable label or title search
- [ ] The issue body includes at minimum: package name, affected version, CVE ID, and available fix version for each finding
- [ ] The issue creation/update step uses only the `issues:write` permission (no broader permissions needed)

---

## Children (Tasks)

| ID | Title | Status |
|----|-------|--------|
| (tasks to be decomposed during implementation) | | |

---

## Progress Summary

| Metric | Value |
|--------|-------|
| Total Tasks | 0 |
| Completed | 0 |
| Completion % | 0% |

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-002: Security-scan pipeline hardening](../FEAT-002-security-scan-pipeline-hardening.md)

### Related Items

- **Depends on:** [STORY-026: Unify CI + scheduled security audit](../STORY-026-unify-ci-scheduled-scan/STORY-026-unify-ci-scheduled-scan.md) (composite action must be in place)

---

## Delivery Evidence

| Artifact | Link | Commit | Notes |
|----------|------|--------|-------|
| PR #302 — Scanner hardening | [geekatron/jerry#302](https://github.com/geekatron/jerry/pull/302) | 81c7c61c | Auto-issue alerting implemented; pending merge — close on merge + AC verification |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-22 | pending | Story created |
| 2026-06-23 | in_progress | PR #302 (commit 81c7c61c) delivers auto-issue alerting; pending merge |
