# TASK-026: Fix pip-audit Coverage Gap in Scheduled Scan

> **Type:** task
> **Status:** completed
> **Priority:** high
> **Created:** 2026-04-15
> **Completed:** 2026-04-16
> **Parent:** EN-006
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |
| [Evidence](#evidence) | Verification record |

---

## Summary

CI pip-audit uses `uv export --all-extras` (covers dev, test, transcript deps). The scheduled daily scan uses bare `uv sync --frozen` (covers only base deps). During low-activity periods, CVEs in pytest, ruff, pyright, mkdocs-material, webvtt-py are invisible to the daily scan — defeating its purpose as a compensating control for Dependabot's `allow: direct` policy.

**Finding:** eng-devsecops Finding 3 (HIGH), `ci.yml:87-90` vs `security-scan.yml:67`

---

## Acceptance Criteria

- [x] `security-scan.yml` install step uses `uv sync --frozen --all-extras`
- [x] Scheduled scan covers the same dependency scope as CI scan
- [x] Both invocations produce equivalent audit coverage

## Evidence

| Verification | Agent | Result |
|-------------|-------|--------|
| Audit coverage parity | eng-devsecops | PASS — `--all-extras` matches CI's `uv export --all-extras` scope |
| Attack surface closed | red-recon | CLOSED — dev/test/transcript CVEs now visible in daily scan |
| Reference doc updated | diataxis-reference | Scheduled Security Scan section rewritten with `--all-extras` |
