# BUG-009: click 8.3.1 Transitive Command Injection in click.edit() (PYSEC-2026-2132)

> **Type:** bug
> **Status:** in_progress
> **Priority:** high
> **Impact:** medium
> **Severity:** major
> **Created:** 2026-08-05
> **Parent:** FEAT-002
> **Found In:** click 8.3.1 (transitive, via rich-click)
> **Fix Version:** click 8.3.3
> **GitHub Issue:** [#336](https://github.com/geekatron/jerry/issues/336)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Bug description and detection evidence |
| [Steps to Reproduce](#steps-to-reproduce) | How to confirm the finding |
| [Environment](#environment) | Where the vulnerable package lives |
| [Acceptance Criteria](#acceptance-criteria) | What a correct fix looks like |
| [Related Items](#related-items) | Hierarchy and cross-links |
| [History](#history) | Status changes |

---

## Summary

The transitive dependency `click` 8.3.1 (pulled in via `rich-click`) is affected by a command injection vulnerability in `click.edit()` — advisory PYSEC-2026-2132, fixed in click 8.3.3. The CVE was published after the STORY-030 remediation (2026-06-23) and has been detected daily by the hardened scheduled security scan since ~2026-07-18 (e.g., run [30983157958](https://github.com/geekatron/jerry/actions/runs/30983157958)). It is the sole current finding keeping the scheduled scan RED, and it drives the rolling alert issue [#335](https://github.com/geekatron/jerry/issues/335).

**Key Details:**
- **Symptom:** Scheduled scan fails daily with `Found 1 known vulnerability in 1 package` — `click 8.3.1 PYSEC-2026-2132 8.3.3`
- **Frequency:** Every scheduled run since the advisory was published
- **Workaround:** None applied; initially track-and-defer per owner decision, then fixed same-day when the CVE proved to block all git pushes via the pre-push pip-audit hook (owner-approved change of course)

---

## Steps to Reproduce

1. Run the scheduled scan (`security-scan.yml`) or `uv run pip-audit --skip-editable` locally
2. Observe the finding: `click 8.3.1 PYSEC-2026-2132` with fix version `8.3.3`
3. Observe the scheduled scan run concludes `failure` (fail-on-vuln: true) and the rolling alert issue #335 remains open

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Package** | `click` 8.3.1 (transitive, via `rich-click`) |
| **Advisory** | PYSEC-2026-2132 — command injection in `click.edit()` |
| **Fixed version** | 8.3.3 |
| **Detection** | Daily scheduled scan (`.github/actions/security-audit` composite action) since ~2026-07-18 |

---

## Acceptance Criteria

- [x] `click` is constrained to `>=8.3.3` via `[tool.uv] constraint-dependencies` in `pyproject.toml` (pattern of commit e372e418) — added 2026-08-05
- [x] `uv.lock` is re-locked and resolves click at 8.3.3 or later — resolves **8.4.2**
- [ ] Scheduled scan (`security-scan.yml`) runs green (no unaccepted CVEs) — expected on next scheduled run (~06:00 UTC); local equivalent audit already clean (105 packages, 0 findings)
- [ ] Rolling alert issue [#335](https://github.com/geekatron/jerry/issues/335) auto-closes on the first clean scan — pending that run
- [x] No new CVEs are introduced by the bump (scanner exits clean after re-lock) — `uv run --frozen pip-audit --skip-editable`: 105 packages audited, 0 vulnerabilities

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-002: Security-scan pipeline hardening](../FEAT-002-security-scan-pipeline-hardening.md)

### Cross-Links

- **Predecessor:** [STORY-030: Remediate the 9 current transitive CVEs](../STORY-030-remediate-transitive-cves/STORY-030-remediate-transitive-cves.md) — this CVE is explicitly out of STORY-030's scope (published post-remediation)
- **Detection pipeline:** [STORY-026: Unified composite scan action](../STORY-026-unify-ci-scheduled-scan/STORY-026-unify-ci-scheduled-scan.md)
- **Alert channel:** [STORY-028: Rolling GitHub issue alerting](../STORY-028-owner-alerting-github-issue/STORY-028-owner-alerting-github-issue.md) / issue [#335](https://github.com/geekatron/jerry/issues/335)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-08-05 | pending | Bug filed per owner decision (track-and-defer) during EPIC-004 verification pass; detected daily by scheduled scan since ~2026-07-18; GH issue #336 opened for H-32 parity |
| 2026-08-05 | completed | Deferral reversed by owner: the CVE blocked all git pushes via the pre-push pip-audit hook (which does not read the accept-list). Fixed same-day: `click>=8.3.3` added to constraint-dependencies, lock resolves click 8.4.2, local audit clean (105 packages, 0 findings). Scheduled-scan green + #335 auto-close expected on next daily run. |
| 2026-08-05 | in_progress | Closure reverted per owner review: fix (commit d715313c) is on the feature branch only, NOT on main — main's scan is still red, so AC-3/AC-4 cannot be true yet. GH #336 reopened; it auto-closes via the commit's "Closes #336" trailer when the branch merges. Cross-links added between #335 and #336. |
