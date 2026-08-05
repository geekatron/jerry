# BUG-002: Pygments CVE-2026-4539 Blocks Git Push

> **Type:** bug
> **Status:** completed
> **Priority:** critical
> **Severity:** major
> **Impact:** high
> **Created:** 2026-03-30T00:00:00Z
> **Completed:** 2026-03-30T00:00:00Z
> **Parent:** FEAT-001
> **Owner:**
> **Effort:** 1
> **GitHub Issue:** [#227](https://github.com/geekatron/jerry/issues/227)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the failure |
| [Fix](#fix) | How to resolve |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Dependencies](#dependencies) | Relationship to other work |
| [History](#history) | Status changes |

---

## Summary

`pip-audit` pre-push hook detects CVE-2026-4539 in pygments 2.19.2 and blocks all pushes. One-liner fix: upgrade pygments to patched version.

---

## Steps to Reproduce

1. With pygments 2.19.2 in `uv.lock` (state as of 2026-03-30, pre-fix), attempt `git push`.
2. The pre-push `pip-audit` hook runs and reports CVE-2026-4539 against pygments 2.19.2.
3. The push is blocked with a non-zero exit; only `--no-verify` bypasses it (forbidden).

---

## Fix

```bash
uv add pygments>=2.19.3
```

If no patched version exists yet, add a temporary `pip-audit` exclusion with tracked revisit date.

---

## Acceptance Criteria

- [ ] `pip-audit` reports zero known vulnerabilities
- [ ] Pre-push hook passes without `--no-verify`
- [ ] pygments version is >= patched release for CVE-2026-4539

---

## Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | BUG-001 | Fix BUG-001 first (more failures, more effort); BUG-002 is a quick follow-up |
| Related | BUG-003 | Both are CI health items |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-30 | adam.nowak | pending | Created from PROJ-024 session. pip-audit blocks push. |
