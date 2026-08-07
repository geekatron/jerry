# STORY-028: Add Owner Alerting via an Auto-Managed Rolling GitHub Issue

> **Type:** story
> **Status:** completed
> **Priority:** medium
> **Impact:** high
> **Created:** 2026-06-22
> **Completed:** 2026-08-07
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
- [x] When a subsequent scan run finds no unaccepted CVEs, it closes the rolling issue automatically — PROVEN 2026-08-06: scheduled run [31079097567](https://github.com/geekatron/jerry/actions/runs/31079097567) ran clean (post click-fix merge) and auto-closed issue #335 at 06:58:22Z
- [x] The rolling issue is reused across multiple runs (not duplicated per run) — identified by a stable label or title search — RUNTIME-PROVEN 2026-08-07: staged controlled test (owner-authorized) dispatched the scan twice against a throwaway branch pinned to vulnerable click 8.3.1; run 1 (31207042351) created alert issue #365, run 2 (31207161180) commented on the SAME issue #365 with no duplicate created
- [x] The issue body includes at minimum: package name, affected version, CVE ID, and available fix version for each finding — RUNTIME-PROVEN 2026-08-07 (PR #364 code + staged test): composite action exposes a `vuln-details` output (pip-audit `--desc` table); `security-scan.yml` embeds it in a fenced code block and computes the date in-shell (`date -u`, replacing the non-existent `github.run_started_at` context). Alert issue #365 (from the controlled test) rendered a populated Date and the full finding (click 8.3.1 / PYSEC-2026-2132 / fix 8.3.3 / description)
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
| 2026-08-06 | in_progress | (recorded 2026-08-07 during pipeline verification) AC-2 RUNTIME-PROVEN: first clean scheduled run 31079097567 (06:57 UTC, post click-fix merge) auto-closed alert issue #335 at 06:58:22Z. **Remaining work:** AC-3 (update-existing-issue branch) unproven, AC-4 body-content defect. |
| 2026-08-07 | in_progress | AC-4 CODE-COMPLETE: fixed the two body defects — (1) empty Date (`github.run_started_at` is not a real GitHub Actions context property; replaced with in-shell `date -u`), (2) missing CVE details (composite action `security-audit` now emits a `vuln-details` multiline output carrying the pip-audit `--desc` findings table; `security-scan.yml` embeds it in a fenced block). Rendered-body simulation confirms date + findings table + column-0 fence; empty-details fallback preserves the run link. Remaining: AC-3 + AC-4 await runtime proof from the next real CVE (a vulnerability was NOT injected to force one). |
| 2026-08-07 | completed | AC-3 + AC-4 RUNTIME-PROVEN via owner-authorized staged test. PR #364 (body/date fix) merged to main. Throwaway branch pinned vulnerable click 8.3.1; scan run 31207042351 created alert issue #365 with a populated Date and the full finding (click 8.3.1 / PYSEC-2026-2132 / fix 8.3.3); scan run 31207161180 commented on the SAME #365 (no duplicate) — proving the rolling-issue reuse path. Test branch + issue #365 cleaned up; main unaffected. All 5 ACs satisfied → STORY-028 completed. |
