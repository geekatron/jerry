# TASK-035: Confirm Dependabot Security Updates + Vulnerability Alerts Are Enabled in Repo Settings

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-06-22
> **Parent:** EN-007
> **GitHub Issue:** [#301](https://github.com/geekatron/jerry/issues/301)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |
| [Evidence](#evidence) | Verification record |
| [Related Items](#related-items) | Hierarchy |
| [History](#history) | Status changes |

---

## Summary

Verify that GitHub Dependabot security updates and vulnerability alerts are both enabled in the `geekatron/jerry` repository Settings. These settings provide an additional detection layer independent of the `pip-audit` scan. If either setting is disabled, enable it and document the change.

---

## Acceptance Criteria

- [ ] Dependabot vulnerability alerts are confirmed enabled in repo Settings → Security → Code security and analysis
- [ ] Dependabot security updates (auto-PRs for vulnerable dependencies) are confirmed enabled in the same settings panel
- [x] Current state (enabled/disabled) is documented in the Evidence section before any changes are made
- [ ] If either setting was disabled, it is now enabled and the change is recorded in Evidence

---

## Evidence

| Verification | Method | Result | Date |
|-------------|--------|--------|------|
| Vulnerability alerts status | GitHub API (`GET /repos/geekatron/jerry/vulnerability-alerts`) | **NOT enabled** (endpoint returns 404) | 2026-08-05 |
| Security updates status | GitHub API (`GET /repos/geekatron/jerry/automated-security-fixes`) | **NOT enabled** (endpoint returns 404) | 2026-08-05 |

> **External verification note (2026-08-05):** current state independently confirmed via the GitHub API during the EPIC-004 verification pass — both Dependabot vulnerability alerts and automated security fixes are NOT enabled (both endpoints return 404). The enable action is genuinely outstanding, so this task correctly remains `pending`. AC bullets 1, 2, and 4 (enable + record) still require a human with repo admin rights; AC bullet 3 (document current state before changes) is now satisfied by this table.

> **Note:** This task requires manual owner/admin access to the `geekatron/jerry` repository Settings panel. It cannot be completed via code changes or automation. A human with repository admin rights must navigate to Settings → Security → Code security and analysis and verify/enable both settings, then record the result in the Evidence table above.

---

## Related Items

### Hierarchy

- **Parent:** [EN-007: Dependency Security-Scan Pipeline Hardening](EN-007-security-scan-pipeline-hardening.md)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-06-22 | pending | Task created |
| 2026-08-05 | pending | Externally verified via GitHub API that vulnerability alerts + automated security fixes are NOT enabled (endpoints return 404) — action genuinely outstanding; current state documented in Evidence |
