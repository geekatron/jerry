# TASK-026: Fix pip-audit Coverage Gap in Scheduled Scan

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-15
> **Parent:** EN-006
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

CI pip-audit uses `uv export --all-extras` (covers dev, test, transcript deps). The scheduled daily scan uses bare `uv sync --frozen` (covers only base deps). During low-activity periods, CVEs in pytest, ruff, pyright, mkdocs-material, webvtt-py are invisible to the daily scan — defeating its purpose as a compensating control for Dependabot's `allow: direct` policy.

**Finding:** eng-devsecops Finding 3 (HIGH), `ci.yml:87-90` vs `security-scan.yml:67`

---

## Acceptance Criteria

- [ ] `security-scan.yml` install step uses `uv sync --frozen --all-extras`
- [ ] Scheduled scan covers the same dependency scope as CI scan
- [ ] Both invocations produce equivalent audit coverage
