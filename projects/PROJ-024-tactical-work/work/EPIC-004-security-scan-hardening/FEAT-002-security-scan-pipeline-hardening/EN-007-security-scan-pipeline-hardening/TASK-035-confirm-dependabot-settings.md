# TASK-035: Confirm Dependabot Security Updates + Vulnerability Alerts Are Enabled in Repo Settings

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-06-22
> **Completed:** 2026-08-05
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

- [x] Dependabot vulnerability alerts are confirmed enabled in repo Settings → Security → Code security and analysis — enabled by owner 2026-08-05; API-confirmed (alerts endpoint returns data)
- [x] Dependabot security updates (auto-PRs for vulnerable dependencies) are confirmed enabled in the same settings panel — enabled by owner 2026-08-05 (owner attestation; settings endpoint not readable with current token scope)
- [x] Current state (enabled/disabled) is documented in the Evidence section before any changes are made
- [x] If either setting was disabled, it is now enabled and the change is recorded in Evidence — see 2026-08-05 enablement row

---

## Evidence

| Verification | Method | Result | Date |
|-------------|--------|--------|------|
| Vulnerability alerts status (pre-change) | GitHub API (`GET /repos/geekatron/jerry/vulnerability-alerts`) | **NOT enabled** (endpoint returns 404) | 2026-08-05 |
| Security updates status (pre-change) | GitHub API (`GET /repos/geekatron/jerry/automated-security-fixes`) | **NOT enabled** (endpoint returns 404) | 2026-08-05 |
| Enablement (by repo owner, Settings UI) | Owner attestation: enabled **Dependabot alerts**, **Dependabot malware alerts**, **Dependabot security updates**; deliberately did NOT enable **Grouped security updates** (separate fix PRs preferred — one bad update can't block a bundle, and failures bisect cleanly) | **Enabled** | 2026-08-05 |
| Vulnerability alerts status (post-change) | GitHub API (`GET /repos/geekatron/jerry/dependabot/alerts`) | **Enabled — confirmed**: endpoint returns alert data (e.g., alert #12, pydantic-settings, state `fixed`); this endpoint only answers when the feature is on | 2026-08-05 |
| Security updates status (post-change) | Settings endpoints (`vulnerability-alerts`, `automated-security-fixes`) still return 404 with the current token — these require admin-scoped credentials, so they cannot distinguish "disabled" from "no permission"; owner attestation is the closing evidence | Owner-attested | 2026-08-05 |

> **External verification note (2026-08-05, superseded same day):** pre-change state was independently confirmed via the GitHub API — both settings NOT enabled (endpoints returned 404). Later the same day the repo owner enabled Dependabot alerts, malware alerts, and security updates (grouped updates deliberately off), alerts were API-confirmed via the `dependabot/alerts` endpoint, and the task completed — see the Evidence rows above and History below.

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
| 2026-08-05 | completed | Owner enabled Dependabot alerts, malware alerts, and security updates in Settings (grouped security updates deliberately left off). Alerts confirmed via the dependabot/alerts API endpoint returning data. All 4 acceptance criteria satisfied. |
