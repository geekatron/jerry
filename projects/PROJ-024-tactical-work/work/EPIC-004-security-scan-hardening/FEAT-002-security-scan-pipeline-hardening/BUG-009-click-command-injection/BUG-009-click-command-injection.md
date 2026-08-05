# BUG-009: click 8.3.1 Transitive Command Injection in click.edit() (PYSEC-2026-2132)

> **Type:** bug
> **Status:** pending
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
- **Workaround:** None applied; owner decision is track-and-defer via this bug (no accept-list entry)

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

- [ ] `click` is constrained to `>=8.3.3` via `[tool.uv] constraint-dependencies` in `pyproject.toml` (pattern of commit e372e418)
- [ ] `uv.lock` is re-locked and resolves click at 8.3.3 or later
- [ ] Scheduled scan (`security-scan.yml`) runs green (no unaccepted CVEs)
- [ ] Rolling alert issue [#335](https://github.com/geekatron/jerry/issues/335) auto-closes on the first clean scan
- [ ] No new CVEs are introduced by the bump (scanner exits clean after re-lock)

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
