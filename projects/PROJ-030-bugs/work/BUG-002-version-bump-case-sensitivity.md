# BUG-002: Version bump regex rejects uppercase scopes like GH-NNN

> **Type:** bug
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-03-02T00:00:00Z
> **Due:**
> **Completed:**
> **Parent:** PROJ-030-bugs
> **Owner:** Claude
> **Found In:** 0.22.1
> **Fix Version:** 0.23.0

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Steps to Reproduce](#steps-to-reproduce) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause details |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related work items |
| [History](#history) | Status changes and key events |

---

## Summary

The version-bump workflow (`.github/workflows/version-bump.yml`) uses inline bash regex that only matches lowercase commit type prefixes (`^feat`, `^fix`, `^perf`). Conventional commits with uppercase scopes like `feat(GH-122):` were silently classified as "none" — no version bump occurred. PRs #125 and #128 merged without bumps. Version stuck at v0.22.1 (should be v0.23.0).

**Key Details:**
- **Symptom:** `feat(GH-122):` commit type detected as "none" instead of "minor"
- **Frequency:** Every commit with uppercase scope characters
- **Workaround:** Commit `1e82a3b0` partially fixed scope regex but inline bash remains untestable

---

## Steps to Reproduce

### Prerequisites

- Jerry Framework repository with version-bump workflow
- Conventional commit with uppercase scope (e.g., `feat(GH-122): description`)

### Steps to Reproduce

1. Create a commit with `feat(GH-122): some feature`
2. Push to main branch
3. Version-bump workflow triggers
4. Inline bash regex `^feat(\([a-z0-9_-]+\))?:` fails to match `GH-122` (uppercase)
5. Bump type resolves to "none"

### Expected Result

Version bump detects `feat(GH-122):` as MINOR bump and increments version.

### Actual Result

Bump type resolves to "none". No version increment. Version stuck at v0.22.1.

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Ubuntu (GitHub Actions) |
| **Runtime** | GitHub Actions workflow |
| **Application Version** | Jerry Framework 0.22.1 |
| **Configuration** | `.github/workflows/version-bump.yml` |
| **Deployment** | CI/CD pipeline |

---

## Root Cause Analysis

### Investigation Summary

Inline bash regex in version-bump.yml is case-sensitive and untestable.

### Root Cause

The `grep -qE` patterns in the workflow use `^[a-z]+` for the type prefix and originally used `[a-z0-9_-]+` for scope (now partially fixed to `[a-zA-Z0-9_-]+`). The core issue is: inline bash regex is untestable, fragile, and case-sensitive. The type prefix still only matches lowercase (`feat`, `fix`, `perf`).

### Contributing Factors

- No test coverage for version detection logic
- Bash regex cannot be unit tested
- No regression test for uppercase scope patterns
- Conventional Commits spec is case-insensitive by convention

---

## Acceptance Criteria

### Fix Verification

- [ ] `feat(GH-122):` detected as MINOR bump
- [ ] `FEAT(scope):` detected as MINOR bump
- [ ] `Fix(Mixed-CASE):` detected as PATCH bump
- [ ] `feat(GH-NNN)!:` detected as MAJOR bump
- [ ] Version detection extracted to `src/version/` bounded context
- [ ] Full test pyramid: unit, integration, contract, architecture, e2e
- [ ] >= 90% line coverage on `src/version/`
- [ ] Workflow updated to use `jerry ci detect-bump-type --since-tag`
- [ ] After merge: pipeline auto-heals to v0.23.0

### Quality Checklist

- [ ] All tests pass (`uv run pytest`)
- [ ] Pre-commit hooks pass
- [ ] Security review complete (ReDoS, subprocess injection)

---

## Related Items

### Hierarchy

- **Parent:** PROJ-030-bugs

### Related Items

- **GitHub Issue:** [#132](https://github.com/geekatron/jerry/issues/132)
- **Commit (partial fix):** `1e82a3b0` — scope regex updated but type still lowercase-only
- **Affected Workflow:** `.github/workflows/version-bump.yml`
- **Missed PRs:** #125 (patch), #128 (minor)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-02 | Claude | in_progress | Initial report. Fix implementation started. |
