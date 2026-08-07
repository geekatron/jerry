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

- [x] When the scheduled scan detects CVEs not on the accept-list, it creates or updates a GitHub issue with title `Security Scan: Open CVEs` (or equivalent canonical title) listing the CVE details — PASS: manual dispatch run 31039187847 auto-created issue [#335](https://github.com/geekatron/jerry/issues/335) at 2026-08-05T19:24:39Z with the `security-alert` label
- [ ] When a subsequent scan run finds no unaccepted CVEs, it closes the rolling issue automatically — code path exists but never runtime-proven (20/20 recent runs found CVEs; the clean-scan branch has never fired in production)
- [ ] The rolling issue is reused across multiple runs (not duplicated per run) — identified by a stable label or title search — create path proven (exactly one issue exists); the update-existing-issue/comment branch never runtime-proven
- [ ] The issue body includes at minimum: package name, affected version, CVE ID, and available fix version for each finding — **FAILED**: issue #335's body lacks package/version/CVE ID/fix version and has an empty Date field caused by an invalid `github.run_started_at` context expression in `security-scan.yml`
- [x] The issue creation/update step uses only the `issues:write` permission (no broader permissions needed) — PASS: workflow `permissions:` block is `contents: read` + `issues: write` only

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
| PR #302 — Scanner hardening | [geekatron/jerry#302](https://github.com/geekatron/jerry/pull/302) | 81c7c61c | Auto-issue alerting implemented. **Merged 2026-06-23** alongside PR #303 (commit e372e418, CVE remediation); reached main via merge PR #304 (merge commit 687a3214, includes docs commit 38b9d23b). All confirmed ancestors of origin/main. |
| Operational incident — missing label | Runs [30429944845](https://github.com/geekatron/jerry/actions/runs/30429944845), [30983157958](https://github.com/geekatron/jerry/actions/runs/30983157958) | — | Every scheduled run 2026-07-18 → 2026-08-05 failed at the alert step with `could not add label: 'security-alert' not found` — the label was never created (one-time setup miss), so the alert channel was silently dead for ~19 days despite the code being correct. |
| Incident remediation | Issue [#335](https://github.com/geekatron/jerry/issues/335) | — | 2026-08-05: `security-alert` label created (color B60205); manual dispatch run [31039187847](https://github.com/geekatron/jerry/actions/runs/31039187847) then auto-created alert issue #335 at 19:24:39Z (AC-1 PASS); permissions scope verified `issues: write` only (AC-5 PASS). |
| Verification report | [wt-verifier-STORY-028-20260805.md](../../verification/wt-verifier-STORY-028-20260805.md) | — | Verdict **NOT_READY, 60%** (2 pass, 2 partial, 1 fail) — below the 80% closure threshold; story remains in_progress. |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-22 | pending | Story created |
| 2026-06-23 | in_progress | PR #302 (commit 81c7c61c) delivers auto-issue alerting; merged same day (evidence trail corrected 2026-08-05) |
| 2026-07-18 | in_progress | (recorded retroactively 2026-08-05) Scheduled runs begin failing at the alert step: `could not add label: 'security-alert' not found` — label never created during setup; failures continue daily through 2026-08-05 |
| 2026-08-05 | in_progress | Label created (B60205); dispatch run 31039187847 auto-created alert issue #335 (AC-1 PASS), AC-5 PASS. wt-verifier verdict NOT_READY 60%. **Remaining work:** AC-4 FAILED (issue body lacks package/version/CVE ID/fix version; empty Date from invalid `github.run_started_at` expression in `security-scan.yml`); AC-2 (auto-close on clean scan) and AC-3 (update-existing-issue branch) never runtime-proven. |
